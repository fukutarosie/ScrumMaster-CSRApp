from functools import wraps
from flask import request, jsonify
from src.entity import User, Role


def require_role(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_token = request.headers.get('Authorization')
            if not auth_token:
                return jsonify({
                    'success': False,
                    'message': 'No token provided'
                }), 401

            if auth_token.startswith('Bearer '):
                auth_token = auth_token[7:]

            user = User.verify_token(auth_token)
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'Invalid or expired token'
                }), 401

            role = Role.find(user.role_id)
            if not role:
                print(f"[AUTH] Role not found for role_id: {user.role_id}")
                return jsonify({
                    'success': False,
                    'message': 'User role not found'
                }), 403
            
            # Allow match by either role name or role code (tolerant, case-insensitive, supports aliases)
            allowed_tokens = {str(a).strip().lower() for a in allowed_roles if a}
            name = (role.role_name or "").strip()
            code = (getattr(role, 'role_code', '') or "").strip()
            name_l = name.lower()
            code_l = code.lower()
            print(f"[AUTH] User role: name='{name}', code='{code}'; Allowed tokens: {allowed_tokens}")
            
            def matches_allowed(value_lower: str) -> bool:
                if not value_lower:
                    return False
                # exact match or token substring match
                return value_lower in allowed_tokens or any(tok in value_lower for tok in allowed_tokens)
            
            if not (matches_allowed(name_l) or matches_allowed(code_l)):
                print(f"[AUTH] Access denied - role name/code did not match allowed tokens")
                return jsonify({
                    'success': False,
                    'message': 'You do not have permission for this action'
                }), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_user_from_token():
    auth_token = request.headers.get('Authorization')
    if not auth_token:
        return None

    if auth_token.startswith('Bearer '):
        auth_token = auth_token[7:]

    if not auth_token:
        return None

    user = User.verify_token(auth_token)
    if not user:
        return None

    return user