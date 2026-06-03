-- =========================================
-- Extensions
-- =========================================
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
-- =========================================
-- 1. Auth & Identity
-- =========================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- 2. User Profile (profile schema)
-- =========================================
CREATE TABLE profiles (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    first_name TEXT,
    last_name TEXT,
    current_title TEXT,
    github_url TEXT,
    location TEXT,
    long_resume TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE job_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    target_years_experience TEXT,
    target_roles JSONB,
    employment_types JSONB,
    experience_levels JSONB
);

CREATE TABLE professional_background (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    education TEXT,
    experience TEXT,
    skills TEXT,
    soft_skills TEXT,
    certificates TEXT,
    languages TEXT
);

-- =========================================
-- 3. Web Scraper System (scraper schema)
-- =========================================
CREATE TABLE raw_scraped_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_url TEXT,
    source_website TEXT,
    raw_html TEXT,
    extracted_data JSONB,
    status TEXT DEFAULT 'Pending',
    scraped_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- 4. Job Catalog (catalog schema)
-- =========================================
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_job_id UUID REFERENCES raw_scraped_jobs(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    employment_type TEXT,
    contract_type TEXT,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE job_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    tag_name TEXT NOT NULL
);
CREATE INDEX idx_job_tags_name ON job_tags(tag_name);

-- =========================================
-- 5. Application Tracker (tracker schema)
-- =========================================
CREATE TABLE applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    status TEXT NOT NULL,
    interview_date TIMESTAMP,
    date_added TIMESTAMP DEFAULT NOW(),
    last_updated TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- 6. AI Integrations (ai schema)
-- =========================================
CREATE TABLE ai_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    endpoint TEXT,
    tokens_used INT DEFAULT 0,
    request_payload JSONB,
    response_payload JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE parsed_resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    document_hash TEXT,
    extracted_data JSONB,
    parsed_at TIMESTAMP DEFAULT NOW()
);