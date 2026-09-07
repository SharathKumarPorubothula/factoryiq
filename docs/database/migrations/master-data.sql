-- =========================================================
-- FACTORYIQ - MASTER DATA DATABASE
-- =========================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS pgcrypto;


-- =========================================================
-- 1. CUSTOMERS
-- =========================================================

CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    code VARCHAR(100) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- 2. SITES
-- =========================================================

CREATE TABLE IF NOT EXISTS sites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(100) NOT NULL UNIQUE,
    address TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_sites_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(id)
);


-- =========================================================
-- 3. FACILITIES
-- =========================================================

CREATE TABLE IF NOT EXISTS facilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    site_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(100) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_facilities_site
        FOREIGN KEY (site_id)
        REFERENCES sites(id)
);


-- =========================================================
-- 4. LOCATIONS
-- =========================================================

CREATE TABLE IF NOT EXISTS locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    facility_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(100) NOT NULL UNIQUE,
    location_type VARCHAR(100),
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_locations_facility
        FOREIGN KEY (facility_id)
        REFERENCES facilities(id)
);


-- =========================================================
-- INSERT CUSTOMERS
-- =========================================================

INSERT INTO customers (name, code, status)
VALUES
    ('ABC Motors', 'CUST-001', 'ACTIVE'),
    ('XYZ Automotive', 'CUST-002', 'ACTIVE'),
    ('Global EV Systems', 'CUST-003', 'ACTIVE'),
    ('Tesla Components', 'CUST-004', 'ACTIVE'),
    ('NextGen Mobility', 'CUST-005', 'ACTIVE');


-- =========================================================
-- INSERT SITES
-- =========================================================

INSERT INTO sites (customer_id, name, code, address, status)
SELECT id, 'Hyderabad Plant', 'SITE-001',
       'Hyderabad, Telangana, India', 'ACTIVE'
FROM customers
WHERE code = 'CUST-001';

INSERT INTO sites (customer_id, name, code, address, status)
SELECT id, 'Pune Plant', 'SITE-002',
       'Pune, Maharashtra, India', 'ACTIVE'
FROM customers
WHERE code = 'CUST-001';

INSERT INTO sites (customer_id, name, code, address, status)
SELECT id, 'Bangalore Plant', 'SITE-003',
       'Bangalore, Karnataka, India', 'ACTIVE'
FROM customers
WHERE code = 'CUST-002';

INSERT INTO sites (customer_id, name, code, address, status)
SELECT id, 'Chennai Plant', 'SITE-004',
       'Chennai, Tamil Nadu, India', 'ACTIVE'
FROM customers
WHERE code = 'CUST-003';

INSERT INTO sites (customer_id, name, code, address, status)
SELECT id, 'Mumbai Plant', 'SITE-005',
       'Mumbai, Maharashtra, India', 'ACTIVE'
FROM customers
WHERE code = 'CUST-004';


-- =========================================================
-- INSERT FACILITIES
-- =========================================================

INSERT INTO facilities (site_id, name, code, status)
SELECT id, 'Battery Manufacturing Facility', 'FAC-001', 'ACTIVE'
FROM sites
WHERE code = 'SITE-001';

INSERT INTO facilities (site_id, name, code, status)
SELECT id, 'Power Electronics Facility', 'FAC-002', 'ACTIVE'
FROM sites
WHERE code = 'SITE-002';

INSERT INTO facilities (site_id, name, code, status)
SELECT id, 'Vehicle Assembly Facility', 'FAC-003', 'ACTIVE'
FROM sites
WHERE code = 'SITE-003';

INSERT INTO facilities (site_id, name, code, status)
SELECT id, 'EV Testing Facility', 'FAC-004', 'ACTIVE'
FROM sites
WHERE code = 'SITE-004';

INSERT INTO facilities (site_id, name, code, status)
SELECT id, 'Controller Manufacturing Facility', 'FAC-005', 'ACTIVE'
FROM sites
WHERE code = 'SITE-005';


-- =========================================================
-- INSERT LOCATIONS
-- =========================================================

INSERT INTO locations
    (facility_id, name, code, location_type, status)
SELECT id, 'Battery Line 01', 'LOC-001',
       'PRODUCTION_LINE', 'ACTIVE'
FROM facilities
WHERE code = 'FAC-001';

INSERT INTO locations
    (facility_id, name, code, location_type, status)
SELECT id, 'Battery Line 02', 'LOC-002',
       'PRODUCTION_LINE', 'ACTIVE'
FROM facilities
WHERE code = 'FAC-001';

INSERT INTO locations
    (facility_id, name, code, location_type, status)
SELECT id, 'Power Electronics Line 01', 'LOC-003',
       'PRODUCTION_LINE', 'ACTIVE'
FROM facilities
WHERE code = 'FAC-002';

INSERT INTO locations
    (facility_id, name, code, location_type, status)
SELECT id, 'Assembly Line 01', 'LOC-004',
       'ASSEMBLY_LINE', 'ACTIVE'
FROM facilities
WHERE code = 'FAC-003';

INSERT INTO locations
    (facility_id, name, code, location_type, status)
SELECT id, 'EV Testing Bay 01', 'LOC-005',
       'TESTING_AREA', 'ACTIVE'
FROM facilities
WHERE code = 'FAC-004';

INSERT INTO locations
    (facility_id, name, code, location_type, status)
SELECT id, 'Controller Line 01', 'LOC-006',
       'PRODUCTION_LINE', 'ACTIVE'
FROM facilities
WHERE code = 'FAC-005';


-- =========================================================
-- VERIFY DATA
-- =========================================================

SELECT * FROM customers;

SELECT * FROM sites;

SELECT * FROM facilities;

SELECT * FROM locations;