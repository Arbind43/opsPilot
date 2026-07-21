-- PostgreSQL initialization script for OpsPilot
-- Sets up the uuid-ossp extension for UUID generation

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Additional setup can be added here if needed,
-- but Alembic will handle table creation.
