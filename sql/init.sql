-- BetterPrompt Database Initialization
-- This script sets up the initial database structure and indexes

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search

-- Create custom types
CREATE TYPE user_plan_type AS ENUM ('free', 'basic', 'pro', 'enterprise');
CREATE TYPE subscription_status AS ENUM ('active', 'canceled', 'past_due', 'unpaid', 'incomplete');
CREATE TYPE prompt_status AS ENUM ('processing', 'completed', 'failed');

-- Create indexes for performance (will be created after tables via migrations)
-- These are documented here for reference

-- Users table indexes:
-- CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
-- CREATE INDEX CONCURRENTLY idx_users_provider ON users(provider, provider_id);
-- CREATE INDEX CONCURRENTLY idx_users_plan_type ON users(plan_type);
-- CREATE INDEX CONCURRENTLY idx_users_created_at ON users(created_at);

-- Prompts table indexes:
-- CREATE INDEX CONCURRENTLY idx_prompts_user_id ON prompts(user_id);
-- CREATE INDEX CONCURRENTLY idx_prompts_created_at ON prompts(created_at);
-- CREATE INDEX CONCURRENTLY idx_prompts_is_favorite ON prompts(is_favorite) WHERE is_favorite = true;
-- CREATE INDEX CONCURRENTLY idx_prompts_tags ON prompts USING GIN(tags);
-- CREATE INDEX CONCURRENTLY idx_prompts_search ON prompts USING GIN(to_tsvector('english', original_prompt || ' ' || optimized_prompt));

-- Usage logs indexes:
-- CREATE INDEX CONCURRENTLY idx_usage_logs_user_id ON usage_logs(user_id);
-- CREATE INDEX CONCURRENTLY idx_usage_logs_created_at ON usage_logs(created_at);
-- CREATE INDEX CONCURRENTLY idx_usage_logs_action ON usage_logs(action);

-- Subscriptions indexes:
-- CREATE INDEX CONCURRENTLY idx_subscriptions_user_id ON subscriptions(user_id);
-- CREATE INDEX CONCURRENTLY idx_subscriptions_stripe_id ON subscriptions(stripe_subscription_id);
-- CREATE INDEX CONCURRENTLY idx_subscriptions_status ON subscriptions(status);

-- Performance settings for development
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log slow queries (1 second+)
ALTER SYSTEM SET log_checkpoints = on;
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;

-- Apply settings
SELECT pg_reload_conf();

-- Create a function to update updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Log successful initialization
INSERT INTO pg_stat_statements_reset();
SELECT 'Database initialization completed successfully' AS status;
