-- İSG Takip Programı - Örnek PostgreSQL Şeması

CREATE TABLE locations (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    brand VARCHAR(100),
    risk_level VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE employees (
    id BIGSERIAL PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    national_id VARCHAR(20),
    location_id BIGINT NOT NULL REFERENCES locations(id),
    department VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    employment_start_date DATE NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE incidents (
    id BIGSERIAL PRIMARY KEY,
    incident_no VARCHAR(50) UNIQUE NOT NULL,
    location_id BIGINT NOT NULL REFERENCES locations(id),
    incident_datetime TIMESTAMPTZ NOT NULL,
    incident_place VARCHAR(100) NOT NULL,
    incident_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    cause_category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    first_aid_note TEXT,
    hospital_required BOOLEAN NOT NULL DEFAULT FALSE,
    lost_work_days INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    created_by BIGINT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE incident_employees (
    id BIGSERIAL PRIMARY KEY,
    incident_id BIGINT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    employee_id BIGINT NOT NULL REFERENCES employees(id),
    injury_note TEXT
);

CREATE TABLE corrective_actions (
    id BIGSERIAL PRIMARY KEY,
    incident_id BIGINT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    action_title VARCHAR(255) NOT NULL,
    action_detail TEXT,
    owner_employee_id BIGINT REFERENCES employees(id),
    due_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    closed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE employee_import_jobs (
    id BIGSERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    uploaded_by BIGINT,
    total_rows INTEGER NOT NULL DEFAULT 0,
    success_rows INTEGER NOT NULL DEFAULT 0,
    failed_rows INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'PROCESSING',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE employee_import_errors (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES employee_import_jobs(id) ON DELETE CASCADE,
    row_number INTEGER NOT NULL,
    raw_data JSONB,
    error_reason TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_employees_location_id ON employees(location_id);
CREATE INDEX idx_incidents_location_id ON incidents(location_id);
CREATE INDEX idx_incidents_incident_datetime ON incidents(incident_datetime);
CREATE INDEX idx_actions_incident_id ON corrective_actions(incident_id);
CREATE INDEX idx_import_errors_job_id ON employee_import_errors(job_id);
