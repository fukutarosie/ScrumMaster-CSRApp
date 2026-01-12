import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

# Load environment variables
load_dotenv('environment.env')

# Create Flask app with static folder configured
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Configure Flask
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
app.config['JSON_SORT_KEYS'] = False

# Enable CORS
# Allow Vercel deployment domains and local development
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001,http://localhost:3002').split(',')
CORS(app, 
     resources={r"/api/*": {
         "origins": cors_origins,
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True
     }})

# Import and register blueprints
# Auth API Endpoints
from src.api.auth.login import login_boundary
from src.api.auth.logout import logout_boundary
from src.api.auth.verify_token import verify_token_boundary

# User Account API Endpoints
from src.api.userAccount.create_user_account import create_user_account_boundary
from src.api.userAccount.view_user_account import view_user_account_boundary
from src.api.userAccount.update_user_account import update_user_account_boundary
from src.api.userAccount.suspend_user_account import suspend_user_account_boundary
from src.api.userAccount.search_user_account import search_user_account_boundary

# User Profile API Endpoints
from src.api.userProfile.create_user_profile import create_user_profile_boundary
from src.api.userProfile.view_user_profile import view_user_profile_boundary
from src.api.userProfile.update_user_profile import update_user_profile_boundary
from src.api.userProfile.suspend_user_profile import suspend_user_profile_boundary
from src.api.userProfile.search_user_profile import search_user_profile_boundary

# PIN Request API Endpoints
from src.api.request.create_new_pin_request import create_pin_new_request_boundary
from src.api.request.view_pin_request import view_pin_request_boundary
from src.api.request.update_pin_request import update_pin_request_boundary
from src.api.request.suspend_pin_request import suspend_pin_request_boundary
from src.api.request.search_pin_request import search_pin_request_boundary
from src.api.request.get_pin_requests import get_pin_requests_boundary
from src.api.request.get_request_analytics import get_request_analytics_boundary
from src.api.request.increment_view_count import increment_view_count_boundary
from src.api.request.get_completed_matches import get_completed_matches_boundary
from src.api.request.get_request_lookups import get_request_lookups_boundary

# CSR Shortlist API Endpoints
from src.api.shortlist.add_to_shortlist import add_to_shortlist_boundary
from src.api.shortlist.get_shortlist import get_shortlist_boundary
from src.api.shortlist.update_shortlist_status import update_shortlist_status_boundary
from src.api.shortlist.remove_from_shortlist import remove_from_shortlist_boundary
from src.api.shortlist.get_shortlist_stats import get_shortlist_stats_boundary

# Role API Endpoints
from src.api.role.get_public_roles import get_public_roles_boundary
from src.api.role.get_all_roles import get_all_roles_boundary
from src.api.role.get_role import get_role_boundary
from src.api.role.create_role import create_role_boundary
from src.api.role.update_role import update_role_boundary
from src.api.role.delete_role import delete_role_boundary

# Platform API Endpoints
from src.api.platform.create_category_page import create_category_page
from src.api.platform.update_category_page import update_category_page
from src.api.platform.delete_category_page import delete_category_page
from src.api.platform.view_categories_page import view_categories_page
from src.api.platform.search_categories_page import search_categories_page
from src.api.platform.daily_reports_page import daily_reports_page
from src.api.platform.weekly_reports_page import weekly_reports_page
from src.api.platform.monthly_reports_page import monthly_reports_page

# Register Auth API Endpoints
app.register_blueprint(login_boundary)
app.register_blueprint(logout_boundary)
app.register_blueprint(verify_token_boundary)

# Register User Account API Endpoints
app.register_blueprint(create_user_account_boundary)
app.register_blueprint(view_user_account_boundary)
app.register_blueprint(update_user_account_boundary)
app.register_blueprint(suspend_user_account_boundary)
app.register_blueprint(search_user_account_boundary)

# Register User Profile API Endpoints
app.register_blueprint(create_user_profile_boundary)
app.register_blueprint(view_user_profile_boundary)
app.register_blueprint(update_user_profile_boundary)
app.register_blueprint(suspend_user_profile_boundary)
app.register_blueprint(search_user_profile_boundary)

# Register PIN Request API Endpoints
app.register_blueprint(create_pin_new_request_boundary)
app.register_blueprint(view_pin_request_boundary)
app.register_blueprint(update_pin_request_boundary)
app.register_blueprint(suspend_pin_request_boundary)
app.register_blueprint(search_pin_request_boundary)
app.register_blueprint(get_pin_requests_boundary)
app.register_blueprint(get_request_analytics_boundary)
app.register_blueprint(increment_view_count_boundary)  # US-27: Track CSR views
app.register_blueprint(get_completed_matches_boundary)
app.register_blueprint(get_request_lookups_boundary)

# Register CSR Shortlist API Endpoints
app.register_blueprint(add_to_shortlist_boundary)
app.register_blueprint(get_shortlist_boundary)
app.register_blueprint(update_shortlist_status_boundary)
app.register_blueprint(remove_from_shortlist_boundary)
app.register_blueprint(get_shortlist_stats_boundary)

# Register Role API Endpoints
app.register_blueprint(get_public_roles_boundary)
app.register_blueprint(get_all_roles_boundary)
app.register_blueprint(get_role_boundary)
app.register_blueprint(create_role_boundary)
app.register_blueprint(update_role_boundary)
app.register_blueprint(delete_role_boundary)

# Register Platform API Endpoints
app.register_blueprint(create_category_page)
app.register_blueprint(update_category_page)
app.register_blueprint(delete_category_page)
app.register_blueprint(view_categories_page)
app.register_blueprint(search_categories_page)
app.register_blueprint(daily_reports_page)
app.register_blueprint(weekly_reports_page)
app.register_blueprint(monthly_reports_page)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return {
        'status': 'healthy',
        'message': 'CSR App Backend is running'
    }, 200

# Error handlers
@app.errorhandler(404)
def not_found(_error):
    return {
        'success': False,
        'message': 'Endpoint not found'
    }, 404

@app.errorhandler(500)
def internal_error(_error):
    return {
        'success': False,
        'message': 'Internal server error'
    }, 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'

    app.run(host=host, port=port, debug=debug)