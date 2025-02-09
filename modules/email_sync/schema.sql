-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create email_sync schema
CREATE SCHEMA IF NOT EXISTS email_sync;

-- Provider configuration table
CREATE TABLE IF NOT EXISTS email_sync.providers (
    id TEXT PRIMARY KEY,  -- 'gmail', 'outlook', etc.
    name TEXT NOT NULL,
    auth_type TEXT NOT NULL, -- 'oauth2', 'app_password', 'password'
    imap_host TEXT,
    imap_port INTEGER,
    smtp_host TEXT,
    smtp_port INTEGER,
    use_ssl BOOLEAN DEFAULT true,
    api_base_url TEXT,  -- For providers with REST APIs
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Email accounts connected by users
CREATE TABLE IF NOT EXISTS email_sync.connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    provider_id TEXT REFERENCES email_sync.providers(id),
    email_address TEXT NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    token_expires_at TIMESTAMP WITH TIME ZONE,
    scopes TEXT[], -- Array of granted permission scopes
    settings JSONB DEFAULT '{}', -- Store provider-specific settings
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, email_address)
);

-- Email sync status tracking
CREATE TABLE IF NOT EXISTS email_sync.sync_status (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    connection_id UUID REFERENCES email_sync.connections(id) ON DELETE CASCADE,
    last_sync_at TIMESTAMP WITH TIME ZONE,
    last_sync_status TEXT, -- 'success', 'failed', etc.
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Triggers to automatically update updated_at columns
CREATE OR REPLACE FUNCTION email_sync.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_connections_updated_at
    BEFORE UPDATE ON email_sync.connections
    FOR EACH ROW
    EXECUTE FUNCTION email_sync.update_updated_at_column();

CREATE TRIGGER update_sync_status_updated_at
    BEFORE UPDATE ON email_sync.sync_status
    FOR EACH ROW
    EXECUTE FUNCTION email_sync.update_updated_at_column();

-- Insert Gmail provider configuration
INSERT INTO email_sync.providers
    (id, name, auth_type, api_base_url)
VALUES
    ('gmail', 'Google Gmail', 'oauth2', 'https://gmail.googleapis.com')
ON CONFLICT (id) DO NOTHING;
