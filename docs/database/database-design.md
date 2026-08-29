# FactoryIQ Database Design

## 1. Overview

FactoryIQ follows a database-per-service architecture using PostgreSQL.

Each backend microservice owns its own database and is responsible for creating,
reading, updating, and deleting only its own data.

The services communicate synchronously through the Service Bridge and
asynchronously through Kafka.

---

## 2. Database Architecture

FactoryIQ uses the following PostgreSQL databases:

| Service | Database |
|---|---|
| Identity | identity_db |
| Master Data | master_data_db |
| Project | project_db |
| Engineering | engineering_db |
| Production | production_db |
| Quality | quality_db |
| Supply Chain | supply_chain_db |
| Logistics | logistics_db |
| After Sales | after_sales_db |
| Document | document_db |
| Collaboration | collaboration_db |
| Notification | notification_db |
| Analytics | analytics_db |
| Integration | integration_db |
| Audit | audit_db |

---

## 3. Database Ownership

Each service owns its database.

Example:

Identity Service
    -> identity_db

Production Service
    -> production_db

Quality Service
    -> quality_db

A service must not directly modify tables belonging to another service.

---

## 4. Cross-Service References

PostgreSQL foreign keys are used only inside the same database.

Cross-database references are represented using UUID values.

Example:

production_db.work_orders.product_id

The product belongs to engineering_db.products.

Production Service should validate the product through the Engineering Service
or through an appropriate integration/event mechanism.

---

## 5. Primary Keys

All major business tables use UUID primary keys.

Example:

id UUID PRIMARY KEY DEFAULT gen_random_uuid()

---

## 6. Timestamps

Tables should use:

created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP

updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP

---

## 7. Soft Delete

Where required, business entities can use:

is_active BOOLEAN NOT NULL DEFAULT TRUE

Hard deletion should be avoided for important business records.

---

## 8. Audit

Business services publish important changes/events.

Audit Service consumes relevant events and stores audit records in:

audit_db.audit_events

---

## 9. Analytics

Analytics does not own operational transactions.

Operational services publish events to Kafka.

Analytics Service consumes those events and builds analytical fact tables.

---

## 10. Database List

### identity_db

- users
- roles
- permissions
- user_roles
- role_permissions
- user_scopes

### master_data_db

- customers
- sites
- facilities
- locations
- items
- suppliers

### project_db

- programs
- projects
- project_members
- milestones
- dependencies
- risks
- status_history

### engineering_db

- requirements
- products
- boms
- bom_items
- ecns
- ecn_impacts
- test_plans
- test_results
- qualification_checklists

### production_db

- production_lines
- stations
- work_orders
- work_order_operations
- wip_units
- production_results
- machine_results

### quality_db

- inspections
- inspection_results
- defects
- ncrs
- ncr_actions
- capa
- audits
- audit_findings
- certifications
- spc_measurements

### supply_chain_db

- purchase_orders
- po_lines
- material_requirements
- inventory_balances
- inventory_lots
- stock_movements
- shortage_alerts

### logistics_db

- shipments
- shipment_items
- tracking_events
- customs_events
- shipment_exceptions

### after_sales_db

- service_requests
- rmas
- repair_cases
- repair_tests
- warranty_claims
- spare_part_orders
- spare_part_order_lines
- eol_notices

### document_db

- documents
- document_versions
- document_links
- document_approvals
- knowledge_articles
- article_versions

### collaboration_db

- threads
- thread_members
- messages
- message_attachments
- mentions

### notification_db

- notification_templates
- subscriptions
- notifications
- delivery_attempts

### analytics_db

- fact_production
- fact_quality
- fact_inventory
- fact_shipments

### integration_db

- systems
- mappings
- integration_messages
- retries
- dead_letters

### audit_db

- audit_events