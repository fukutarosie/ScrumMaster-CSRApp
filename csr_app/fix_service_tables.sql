-- ============================================
-- DATABASE CLEANUP AND STANDARDIZATION SCRIPT
-- ============================================

-- Option 1: If you want to keep BOTH tables (recommended)
-- Rename service_type to service_types for consistency with the code
ALTER TABLE IF EXISTS public.service_type RENAME TO service_types;

-- Ensure service_category table exists with correct structure
CREATE TABLE IF NOT EXISTS public.service_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_service_types_name ON public.service_types(service_name);
CREATE INDEX IF NOT EXISTS idx_service_category_name ON public.service_category(name);

-- Enable RLS on both tables
ALTER TABLE public.service_types ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.service_category ENABLE ROW LEVEL SECURITY;

-- Drop existing policies
DROP POLICY IF EXISTS "Allow all operations" ON public.service_types;
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON public.service_category;

-- Create policies for service_types
CREATE POLICY "Allow all operations" ON public.service_types
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Create policies for service_category
CREATE POLICY "Allow all operations for authenticated users" ON public.service_category
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Insert default service categories if they don't exist
INSERT INTO public.service_category (name, description) VALUES
    ('Technology', 'Technology-related services and support'),
    ('Healthcare', 'Healthcare and medical services'),
    ('Education', 'Educational services and training'),
    ('Finance', 'Financial services and consulting'),
    ('Legal', 'Legal services and consultation')
ON CONFLICT (name) DO NOTHING;

-- ============================================
-- SUMMARY:
-- - service_types: Used for CSR request categories (e.g., "Grocery Shopping")
-- - service_category: Used for platform-level service categories
-- Both tables serve different purposes and should coexist
-- ============================================
