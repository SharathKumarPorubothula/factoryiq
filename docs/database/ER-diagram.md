======================================================================
                    FACTORYIQ - DATABASE ER DIAGRAM
======================================================================

Architecture:
    React Frontend
          |
          v
    Nginx / Apache
          |
          v
    Service Bridge
          |
          +---- Identity Service
          +---- Master Data Service
          +---- Project Service
          +---- Engineering Service
          +---- Production Service
          +---- Quality Service
          +---- Supply Chain Service
          +---- Logistics Service
          +---- After Sales Service
          +---- Document Service
          +---- Collaboration Service
          +---- Notification Service
          +---- Analytics Service
          +---- Integration Service
          +---- Audit Service
          |
          v
        Kafka


======================================================================
                         DATABASE OWNERSHIP
======================================================================

+----------------------+--------------------------+
| SERVICE              | DATABASE                 |
+----------------------+--------------------------+
| Identity             | identity_db              |
| Master Data          | master_data_db           |
| Project              | project_db               |
| Engineering          | engineering_db           |
| Production           | production_db            |
| Quality              | quality_db               |
| Supply Chain         | supply_chain_db          |
| Logistics            | logistics_db             |
| After Sales          | after_sales_db           |
| Document             | document_db              |
| Collaboration        | collaboration_db         |
| Notification         | notification_db          |
| Analytics             | analytics_db             |
| Integration          | integration_db           |
| Audit                | audit_db                 |
+----------------------+--------------------------+


======================================================================
1. IDENTITY SERVICE
======================================================================

Database: identity_db


+---------------------------+
|          users            |
+---------------------------+
| PK  id UUID               |
|     username              |
|     email                 |
|     password_hash         |
|     first_name            |
|     last_name             |
|     is_active             |
|     last_login_at         |
|     created_at            |
|     updated_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|        user_roles         |
+---------------------------+
| PK/FK user_id             |
| PK/FK role_id             |
|     created_at             |
+-------------+-------------+
              |
              | N:1
              v
+---------------------------+
|           roles           |
+---------------------------+
| PK  id UUID               |
|     name                  |
|     description           |
|     is_active              |
|     created_at             |
|     updated_at             |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|     role_permissions      |
+---------------------------+
| PK/FK role_id             |
| PK/FK permission_id       |
|     created_at             |
+-------------+-------------+
              |
              | N:1
              v
+---------------------------+
|        permissions        |
+---------------------------+
| PK  id UUID               |
|     name                  |
|     resource              |
|     action                |
|     description           |
|     created_at             |
+---------------------------+


users
  |
  | 1:N
  v
+---------------------------+
|       user_scopes         |
+---------------------------+
| PK  id UUID               |
| FK  user_id               |
|     scope_type            |
|     scope_id              |
|     created_at            |
+---------------------------+


Identity Relationships:

    users
      |
      +----< user_roles >---- roles
                                |
                                +----< role_permissions >---- permissions

    users
      |
      +----< user_scopes


======================================================================
2. MASTER DATA SERVICE
======================================================================

Database: master_data_db


+---------------------------+
|        customers          |
+---------------------------+
| PK  id UUID               |
|     name                  |
|     code                  |
|     status                |
|     created_at            |
|     updated_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|          sites            |
+---------------------------+
| PK  id UUID               |
| FK  customer_id          |
|     name                  |
|     code                  |
|     address               |
|     status                |
|     created_at            |
|     updated_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|        facilities         |
+---------------------------+
| PK  id UUID               |
| FK  site_id              |
|     name                  |
|     code                  |
|     status                |
|     created_at            |
|     updated_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|         locations         |
+---------------------------+
| PK  id UUID               |
| FK  facility_id          |
|     name                  |
|     code                  |
|     location_type         |
|     status                |
|     created_at            |
|     updated_at            |
+---------------------------+


+---------------------------+
|           items           |
+---------------------------+
| PK  id UUID               |
|     item_number           |
|     name                  |
|     description           |
|     item_type             |
|     unit_of_measure       |
|     status                |
|     created_at            |
|     updated_at            |
+---------------------------+


+---------------------------+
|         suppliers         |
+---------------------------+
| PK  id UUID               |
|     name                  |
|     supplier_code         |
|     contact_email         |
|     phone                 |
|     status                |
|     created_at            |
|     updated_at            |
+---------------------------+


Master Data Relationships:

    customers
        |
        +----< sites
                 |
                 +----< facilities
                          |
                          +----< locations

    items

    suppliers


======================================================================
3. PROJECT SERVICE
======================================================================

Database: project_db


+---------------------------+
|         programs          |
+---------------------------+
| PK  id UUID               |
|     name                  |
|     description           |
|     status                |
|     start_date            |
|     end_date              |
|     created_at            |
|     updated_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|         projects          |
+---------------------------+
| PK  id UUID               |
| FK  program_id            |
|     project_code          |
|     name                  |
|     description           |
|     status                |
|     start_date            |
|     end_date              |
|     created_at            |
|     updated_at            |
+-------------+-------------+
              |
              +---------------------+----------------------+----------------+
              |                     |                      |                |
              | 1:N                 | 1:N                  | 1:N            | 1:N
              v                     v                      v                v
+--------------------+   +------------------+   +------------------+   +------------------+
|  project_members   |   |    milestones    |   |      risks       |   |  status_history  |
+--------------------+   +------------------+   +------------------+   +------------------+
| PK id              |   | PK id            |   | PK id            |   | PK id            |
| FK project_id      |   | FK project_id    |   | FK project_id    |   | FK project_id    |
| user_id            |   | name             |   | title            |   | old_status       |
| role               |   | description      |   | description      |   | new_status       |
| created_at         |   | due_date         |   | probability      |   | changed_by       |
+--------------------+   | status           |   | impact           |   | changed_at       |
                         | created_at       |   | status           |   +------------------+
                         +------------------+   | created_at       |
                                                +------------------+


projects
    |
    | 1:N
    v
+---------------------------+
|       dependencies        |
+---------------------------+
| PK  id UUID               |
| FK  project_id            |
|     predecessor_id        |
|     successor_id          |
|     dependency_type       |
|     created_at            |
+---------------------------+


Project Relationships:

    programs
       |
       +----< projects
                |
                +----< project_members
                +----< milestones
                +----< dependencies
                +----< risks
                +----< status_history


======================================================================
4. ENGINEERING SERVICE
======================================================================

Database: engineering_db


+---------------------------+
|         products          |
+---------------------------+
| PK  id UUID               |
|     product_code          |
|     name                  |
|     description           |
|     revision              |
|     status                |
|     created_at            |
|     updated_at            |
+-------------+-------------+
              |
              +---------------------------+
              |                           |
              | 1:N                       | 1:N
              v                           v
+---------------------------+   +---------------------------+
|           boms            |   |        test_plans         |
+---------------------------+   +---------------------------+
| PK  id UUID               |   | PK  id UUID               |
| FK  product_id            |   | FK  product_id            |
|     revision              |   |     name                  |
|     status                |   |     description           |
|     effective_date        |   |     status                |
|     created_at            |   |     created_at            |
+-------------+-------------+   +-------------+-------------+
              |                               |
              | 1:N                           | 1:N
              v                               v
+---------------------------+   +---------------------------+
|         bom_items         |   |       test_results         |
+---------------------------+   +---------------------------+
| PK  id UUID               |   | PK  id UUID               |
| FK  bom_id                |   | FK  test_plan_id          |
|     item_id               |   |     result                |
|     quantity              |   |     measured_value        |
|     unit_of_measure       |   |     unit                  |
|     created_at            |   |     remarks               |
+---------------------------+   |     executed_at           |
                                +---------------------------+


+---------------------------+
|       requirements        |
+---------------------------+
| PK  id UUID               |
|     project_id            |
|     requirement_code      |
|     title                 |
|     description           |
|     status                |
|     priority              |
|     created_at            |
|     updated_at            |
+---------------------------+


+---------------------------+
|           ecns            |
+---------------------------+
| PK  id UUID               |
|     ecn_number            |
|     title                 |
|     description           |
|     status                |
|     created_at            |
|     updated_at             |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|        ecn_impacts        |
+---------------------------+
| PK  id UUID               |
| FK  ecn_id                |
|     impact_area           |
|     description           |
|     created_at             |
+---------------------------+


products
    |
    | 1:N
    v
+---------------------------+
| qualification_checklists  |
+---------------------------+
| PK  id UUID               |
| FK  product_id            |
|     checklist_name        |
|     status                |
|     created_at             |
+---------------------------+


Engineering Relationships:

    products
       |
       +----< boms
       |       |
       |       +----< bom_items
       |
       +----< test_plans
       |       |
       |       +----< test_results
       |
       +----< qualification_checklists

    requirements

    ecns
       |
       +----< ecn_impacts


======================================================================
5. PRODUCTION SERVICE
======================================================================

Database: production_db


+---------------------------+
|     production_lines     |
+---------------------------+
| PK  id UUID               |
|     name                  |
|     code                  |
|     status                |
|     created_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|         stations          |
+---------------------------+
| PK  id UUID               |
| FK  production_line_id    |
|     name                  |
|     code                  |
|     status                |
|     created_at            |
+-------------+-------------+
              |
              +-------------------------+
              |                         |
              | 1:N                     | 1:N
              v                         v
+---------------------------+   +---------------------------+
| work_order_operations     |   |     machine_results       |
+---------------------------+   +---------------------------+
| PK  id UUID               |   | PK  id UUID               |
| FK  work_order_id         |   | FK  station_id            |
| FK  station_id            |   |     parameter_name        |
|     operation_sequence    |   |     parameter_value      |
|     status                |   |     unit                  |
|     started_at            |   |     result_status         |
|     completed_at          |   |     recorded_at           |
+---------------------------+   +---------------------------+


+---------------------------+
|       work_orders         |
+---------------------------+
| PK  id UUID               |
|     work_order_number     |
|     product_id            |
|     quantity              |
|     status                |
|     planned_start         |
|     planned_end           |
|     created_at            |
|     updated_at            |
+-------------+-------------+
              |
              +------------------------+
              |                        |
              | 1:N                    | 1:N
              v                        v
+---------------------------+   +---------------------------+
|         wip_units         |   |    production_results     |
+---------------------------+   +---------------------------+
| PK  id UUID               |   | PK  id UUID               |
| FK  work_order_id         |   | FK  work_order_id         |
|     serial_number         |   |     quantity_produced     |
|     status                |   |     quantity_rejected     |
|     current_station_id    |   |     produced_at           |
|     created_at            |   +---------------------------+
+---------------------------+


Production Relationships:

    production_lines
         |
         +----< stations
                    |
                    +----< work_order_operations
                    |
                    +----< machine_results

    work_orders
         |
         +----< work_order_operations
         |
         +----< wip_units
         |
         +----< production_results


======================================================================
6. QUALITY SERVICE
======================================================================

Database: quality_db


+---------------------------+
|        inspections        |
+---------------------------+
| PK  id UUID               |
|     inspection_number     |
|     product_id            |
|     inspection_type       |
|     status                |
|     created_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|    inspection_results     |
+---------------------------+
| PK  id UUID               |
| FK  inspection_id         |
|     parameter_name        |
|     expected_value        |
|     actual_value          |
|     result                |
+---------------------------+


+---------------------------+
|           ncrs            |
+---------------------------+
| PK  id UUID               |
|     ncr_number            |
|     description           |
|     severity              |
|     status                |
|     created_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|        ncr_actions        |
+---------------------------+
| PK  id UUID               |
| FK  ncr_id                |
|     action                |
|     owner_id              |
|     due_date              |
|     status                |
|     created_at            |
+---------------------------+


+---------------------------+
|          audits           |
+---------------------------+
| PK  id UUID               |
|     audit_number          |
|     audit_type            |
|     audit_date            |
|     status                |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|      audit_findings       |
+---------------------------+
| PK  id UUID               |
| FK  audit_id              |
|     description           |
|     severity              |
|     status                |
+---------------------------+


+---------------------------+
|          defects          |
+---------------------------+
| PK  id UUID               |
|     name                  |
|     description           |
|     severity               |
|     created_at             |
+---------------------------+


+---------------------------+
|           capa            |
+---------------------------+
| PK  id UUID               |
|     capa_number           |
|     description           |
|     corrective_action     |
|     preventive_action     |
|     status                |
|     created_at             |
+---------------------------+


+---------------------------+
|      certifications       |
+---------------------------+
| PK  id UUID               |
|     name                  |
|     certificate_number    |
|     issue_date             |
|     expiry_date            |
|     status                |
+---------------------------+


+---------------------------+
|     spc_measurements      |
+---------------------------+
| PK  id UUID               |
|     parameter_name        |
|     measured_value        |
|     specification_min     |
|     specification_max     |
|     measured_at            |
+---------------------------+


Quality Relationships:

    inspections
        |
        +----< inspection_results

    ncrs
        |
        +----< ncr_actions

    audits
        |
        +----< audit_findings

    defects

    capa

    certifications

    spc_measurements


======================================================================
7. SUPPLY CHAIN SERVICE
======================================================================

Database: supply_chain_db


+---------------------------+
|     purchase_orders       |
+---------------------------+
| PK  id UUID               |
|     po_number             |
|     supplier_id           |
|     order_date            |
|     status                |
|     created_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|         po_lines          |
+---------------------------+
| PK  id UUID               |
| FK  purchase_order_id     |
|     item_id               |
|     quantity              |
|     unit_price             |
|     created_at            |
+---------------------------+


+---------------------------+
|      inventory_lots       |
+---------------------------+
| PK  id UUID               |
|     item_id               |
|     lot_number            |
|     quantity              |
|     expiry_date           |
|     status                |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|      stock_movements      |
+---------------------------+
| PK  id UUID               |
|     item_id               |
| FK  lot_id                |
|     movement_type         |
|     quantity              |
|     movement_date         |
+---------------------------+


+---------------------------+
|    inventory_balances     |
+---------------------------+
| PK  id UUID               |
|     item_id               |
|     location_id           |
|     quantity              |
|     updated_at            |
+---------------------------+


+---------------------------+
|   material_requirements   |
+---------------------------+
| PK  id UUID               |
|     item_id               |
|     required_quantity     |
|     required_date         |
|     status                |
|     created_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|      shortage_alerts      |
+---------------------------+
| PK  id UUID               |
|     item_id               |
|     required_quantity     |
|     available_quantity    |
|     severity              |
|     status                |
|     created_at            |
+---------------------------+


Supply Chain Relationships:

    purchase_orders
        |
        +----< po_lines

    inventory_lots
        |
        +----< stock_movements

    inventory_balances

    material_requirements
        |
        +----< shortage_alerts


======================================================================
8. LOGISTICS SERVICE
======================================================================

Database: logistics_db


+---------------------------+
|         shipments         |
+---------------------------+
| PK  id UUID               |
|     shipment_number       |
|     status                |
|     origin                |
|     destination           |
|     shipped_at            |
|     expected_delivery     |
|     actual_delivery       |
|     created_at            |
+-------------+-------------+
              |
              +-----------------------+----------------------+------------------+
              |                       |                      |
              | 1:N                   | 1:N                  | 1:N
              v                       v                      v
+---------------------+   +---------------------+   +------------------------+
|   shipment_items    |   |   tracking_events   |   |    customs_events     |
+---------------------+   +---------------------+   +------------------------+
| PK id               |   | PK id               |   | PK id                 |
| FK shipment_id      |   | FK shipment_id      |   | FK shipment_id        |
| item_id             |   | event_type          |   | event_type             |
| quantity             |   | location            |   | status                 |
+---------------------+   | event_time          |   | event_time             |
                          +---------------------+   +------------------------+


shipments
    |
    | 1:N
    v
+---------------------------+
|    shipment_exceptions    |
+---------------------------+
| PK  id UUID               |
| FK  shipment_id           |
|     exception_type        |
|     description           |
|     status                |
|     created_at            |
+---------------------------+


Logistics Relationships:

    shipments
        |
        +----< shipment_items
        |
        +----< tracking_events
        |
        +----< customs_events
        |
        +----< shipment_exceptions


======================================================================
9. AFTER SALES SERVICE
======================================================================

Database: after_sales_db


+---------------------------+
|     service_requests      |
+---------------------------+
| PK  id UUID               |
|     request_number        |
|     customer_id           |
|     description           |
|     priority              |
|     status                |
|     created_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|           rmas            |
+---------------------------+
| PK  id UUID               |
|     rma_number            |
| FK  service_request_id    |
|     reason                |
|     status                |
|     created_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|       repair_cases        |
+---------------------------+
| PK  id UUID               |
| FK  rma_id                |
|     description           |
|     status                |
|     created_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|        repair_tests       |
+---------------------------+
| PK  id UUID               |
| FK  repair_case_id        |
|     test_name             |
|     result                |
|     remarks               |
|     tested_at             |
+---------------------------+


+---------------------------+
|      warranty_claims      |
+---------------------------+
| PK  id UUID               |
|     claim_number          |
|     customer_id           |
|     product_id            |
|     claim_date            |
|     status                |
|     description           |
+---------------------------+


+---------------------------+
|    spare_part_orders      |
+---------------------------+
| PK  id UUID               |
|     order_number          |
|     customer_id           |
|     status                |
|     created_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|  spare_part_order_lines  |
+---------------------------+
| PK  id UUID               |
| FK  order_id              |
|     item_id               |
|     quantity              |
+---------------------------+


+---------------------------+
|        eol_notices        |
+---------------------------+
| PK  id UUID               |
|     product_id            |
|     notice_date            |
|     effective_date        |
|     description           |
|     status                |
+---------------------------+


After Sales Relationships:

    service_requests
        |
        +----< rmas
                 |
                 +----< repair_cases
                          |
                          +----< repair_tests

    warranty_claims

    spare_part_orders
        |
        +----< spare_part_order_lines

    eol_notices


======================================================================
10. DOCUMENT SERVICE
======================================================================

Database: document_db


+---------------------------+
|         documents         |
+---------------------------+
| PK  id UUID               |
|     document_number       |
|     title                 |
|     document_type         |
|     status                |
|     created_by            |
|     created_at            |
|     updated_at            |
+-------------+-------------+
              |
              +----------------------+-----------------------+
              |                      |                       |
              | 1:N                  | 1:N                   | 1:N
              v                      v                       v
+----------------------+  +----------------------+  +----------------------+
|  document_versions   |  |  document_links      |  | document_approvals   |
+----------------------+  +----------------------+  +----------------------+
| PK id                |  | PK id                |  | PK id                |
| FK document_id       |  | FK document_id       |  | FK document_id       |
| version_number       |  | entity_type          |  | approver_id          |
| file_path            |  | entity_id            |  | status               |
| file_name            |  | created_at           |  | comments             |
| file_size            |  +----------------------+  | approved_at          |
| checksum             |                             +----------------------+
| created_by           |
| created_at           |
+----------------------+


+---------------------------+
|     knowledge_articles    |
+---------------------------+
| PK  id UUID               |
|     title                 |
|     category              |
|     status                |
|     created_by            |
|     created_at            |
+-------------+-------------+
              |
              | 1:N
              v
+---------------------------+
|      article_versions     |
+---------------------------+
| PK  id UUID               |
| FK  article_id            |
|     version_number        |
|     content               |
|     created_by            |
|     created_at            |
+---------------------------+


Document Relationships:

    documents
        |
        +----< document_versions
        |
        +----< document_links
        |
        +----< document_approvals

    knowledge_articles
        |
        +----< article_versions


======================================================================
11. COLLABORATION SERVICE
======================================================================

Database: collaboration_db


+---------------------------+
|          threads          |
+---------------------------+
| PK  id UUID               |
|     subject               |
|     created_by            |
|     created_at            |
+-------------+-------------+
              |
              +-------------------------+
              |                         |
              | 1:N                     | 1:N
              v                         v
+---------------------------+   +---------------------------+
|      thread_members       |   |         messages          |
+---------------------------+   +-------------+-------------+
| PK/FK thread_id           |   | PK  id UUID               |
| PK/FK user_id             |   | FK  thread_id             |
|     joined_at             |   |     sender_id             |
+---------------------------+   |     message               |
                                |     created_at             |
                                +-------------+-------------+
                                              |
                              +---------------+---------------+
                              |                               |
                              | 1:N                           | 1:N
                              v                               v
                 +---------------------------+   +----------------------+
                 |   message_attachments     |   |       mentions       |
                 +---------------------------+   +----------------------+
                 | PK  id UUID               |   | PK  id UUID          |
                 | FK  message_id            |   | FK  message_id       |
                 |     document_id           |   |     mentioned_user_id|
                 |     file_name             |   |     created_at       |
                 |     created_at            |   +----------------------+
                 +---------------------------+


Collaboration Relationships:

    threads
        |
        +----< thread_members
        |
        +----< messages
                 |
                 +----< message_attachments
                 |
                 +----< mentions


======================================================================
12. NOTIFICATION SERVICE
======================================================================

Database: notification_db


+------------------------------+
|    notification_templates    |
+------------------------------+
| PK  id UUID                  |
|     name                     |
|     channel                  |
|     subject                  |
|     body                     |
|     created_at               |
+--------------+---------------+
               |
               | 1:N
               v
+------------------------------+
|        notifications         |
+------------------------------+
| PK  id UUID                  |
|     user_id                  |
| FK  template_id              |
|     title                    |
|     message                  |
|     status                   |
|     created_at               |
+--------------+---------------+
               |
               | 1:N
               v
+------------------------------+
|      delivery_attempts       |
+------------------------------+
| PK  id UUID                  |
| FK  notification_id          |
|     channel                  |
|     status                   |
|     attempted_at              |
|     error_message             |
+------------------------------+


+------------------------------+
|       subscriptions          |
+------------------------------+
| PK  id UUID                  |
|     user_id                  |
|     event_type               |
|     channel                  |
|     enabled                  |
|     created_at               |
+------------------------------+


Notification Relationships:

    notification_templates
        |
        +----< notifications
                 |
                 +----< delivery_attempts

    subscriptions


======================================================================
13. ANALYTICS SERVICE
======================================================================

Database: analytics_db


+------------------------------+
|       fact_production        |
+------------------------------+
| PK  id UUID                  |
|     date_key                 |
|     product_id               |
|     production_line_id       |
|     quantity_produced        |
|     quantity_rejected        |
|     created_at               |
+------------------------------+


+------------------------------+
|         fact_quality         |
+------------------------------+
| PK  id UUID                  |
|     date_key                 |
|     product_id               |
|     defect_count             |
|     inspection_count         |
|     ncr_count                |
|     created_at               |
+------------------------------+


+------------------------------+
|        fact_inventory        |
+------------------------------+
| PK  id UUID                  |
|     date_key                 |
|     item_id                  |
|     location_id              |
|     quantity                 |
|     created_at               |
+------------------------------+


+------------------------------+
|        fact_shipments        |
+------------------------------+
| PK  id UUID                  |
|     date_key                 |
|     shipment_id              |
|     delivery_status           |
|     delivery_delay_hours     |
|     created_at               |
+------------------------------+


Analytics Data Flow:

    Production Service
            |
            | Production Events
            v
          Kafka
            |
            v
    Analytics Service
            |
            v
       analytics_db
            |
            +---- fact_production
            +---- fact_quality
            +---- fact_inventory
            +---- fact_shipments


IMPORTANT:

    Analytics database contains analytical/read-model data.

    It does NOT directly own or modify operational data from
    production_db, quality_db, supply_chain_db or logistics_db.


======================================================================
14. INTEGRATION SERVICE
======================================================================

Database: integration_db


+------------------------------+
|           systems            |
+------------------------------+
| PK  id UUID                  |
|     name                     |
|     system_type              |
|     base_url                 |
|     status                   |
|     created_at               |
+--------------+---------------+
               |
               +-----------------------------+
               |                             |
               | 1:N                         | 1:N
               v                             v
+------------------------------+  +------------------------------+
|          mappings            |  |    integration_messages      |
+------------------------------+  +--------------+---------------+
| PK  id UUID                  |  | PK  id UUID                  |
| FK  system_id               |  | FK  system_id                |
|     source_entity            |  |     message_type             |
|     target_entity            |  |     payload JSONB             |
|     mapping_config JSONB     |  |     status                   |
|     created_at               |  |     created_at               |
+------------------------------+  |     processed_at             |
                                   +--------------+---------------+
                                                  |
                                  +---------------+---------------+
                                  |                               |
                                  | 1:N                           | 1:N
                                  v                               v
                     +------------------------+       +------------------------+
                     |        retries         |       |     dead_letters      |
                     +------------------------+       +------------------------+
                     | PK id                  |       | PK id                 |
                     | FK integration_message |       | FK integration_message|
                     |    _id                 |       |    _id                |
                     | attempt_number         |       | reason                |
                     | attempted_at           |       | created_at            |
                     | error_message          |       +------------------------+
                     +------------------------+


Integration Relationships:

    systems
        |
        +----< mappings
        |
        +----< integration_messages
                 |
                 +----< retries
                 |
                 +----< dead_letters


======================================================================
15. AUDIT SERVICE
======================================================================

Database: audit_db


+--------------------------------------------------------------+
|                       audit_events                           |
+--------------------------------------------------------------+
| PK  id UUID                                                  |
|     user_id                                                  |
|     service_name                                             |
|     entity_type                                              |
|     entity_id                                                |
|     action                                                   |
|     old_value JSONB                                          |
|     new_value JSONB                                          |
|     ip_address INET                                          |
|     correlation_id UUID                                      |
|     created_at TIMESTAMPTZ                                   |
+--------------------------------------------------------------+


Audit Data Flow:

    Identity Service
          |
    Production Service
          |
    Quality Service
          |
    Project Service
          |
          | Audit Events
          v
        Kafka
          |
          v
    Audit Service
          |
          v
       audit_db
          |
          v
    audit_events


Audit Purpose:

    WHO      -> user_id
    WHAT     -> action
    SERVICE  -> service_name
    ENTITY   -> entity_type + entity_id
    BEFORE   -> old_value
    AFTER    -> new_value
    WHEN     -> created_at
    SOURCE   -> ip_address
    TRACE    -> correlation_id


======================================================================
16. COMPLETE SERVICE-TO-DATABASE MAP
======================================================================


+----------------------+--------------------------+
| SERVICE              | DATABASE                 |
+----------------------+--------------------------+
| Identity Service     | identity_db              |
| Master Data Service  | master_data_db           |
| Project Service      | project_db               |
| Engineering Service  | engineering_db           |
| Production Service   | production_db            |
| Quality Service      | quality_db               |
| Supply Chain Service | supply_chain_db          |
| Logistics Service    | logistics_db             |
| After Sales Service  | after_sales_db           |
| Document Service     | document_db              |
| Collaboration       | collaboration_db         |
| Notification Service | notification_db          |
| Analytics Service    | analytics_db             |
| Integration Service  | integration_db           |
| Audit Service        | audit_db                 |
+----------------------+--------------------------+


======================================================================
17. COMPLETE TABLE INVENTORY
======================================================================


identity_db
-----------

    users
    roles
    permissions
    user_roles
    role_permissions
    user_scopes


master_data_db
--------------

    customers
    sites
    facilities
    locations
    items
    suppliers


project_db
----------

    programs
    projects
    project_members
    milestones
    dependencies
    risks
    status_history


engineering_db
--------------

    requirements
    products
    boms
    bom_items
    ecns
    ecn_impacts
    test_plans
    test_results
    qualification_checklists


production_db
-------------

    production_lines
    stations
    work_orders
    work_order_operations
    wip_units
    production_results
    machine_results


quality_db
----------

    inspections
    inspection_results
    defects
    ncrs
    ncr_actions
    capa
    audits
    audit_findings
    certifications
    spc_measurements


supply_chain_db
---------------

    purchase_orders
    po_lines
    material_requirements
    inventory_balances
    inventory_lots
    stock_movements
    shortage_alerts


logistics_db
------------

    shipments
    shipment_items
    tracking_events
    customs_events
    shipment_exceptions


after_sales_db
--------------

    service_requests
    rmas
    repair_cases
    repair_tests
    warranty_claims
    spare_part_orders
    spare_part_order_lines
    eol_notices


document_db
-----------

    documents
    document_versions
    document_links
    document_approvals
    knowledge_articles
    article_versions


collaboration_db
----------------

    threads
    thread_members
    messages
    message_attachments
    mentions


notification_db
---------------

    notification_templates
    subscriptions
    notifications
    delivery_attempts


analytics_db
------------

    fact_production
    fact_quality
    fact_inventory
    fact_shipments


integration_db
--------------

    systems
    mappings
    integration_messages
    retries
    dead_letters


audit_db
--------

    audit_events


======================================================================
18. COMPLETE FACTORYIQ DATABASE ARCHITECTURE
======================================================================


                              +--------------------+
                              |   React Frontend   |
                              +---------+----------+
                                        |
                                        v
                              +--------------------+
                              |   Nginx / Apache   |
                              +---------+----------+
                                        |
                                        v
                              +--------------------+
                              |   Service Bridge   |
                              +---------+----------+
                                        |
             +--------------------------+--------------------------+
             |                          |                          |
             v                          v                          v

      +--------------+           +--------------+           +--------------+
      | Identity     |           | Master Data  |           | Project      |
      | Service      |           | Service      |           | Service      |
      +------+-------+           +------+-------+           +------+-------+
             |                          |                          |
             v                          v                          v
      +--------------+           +--------------+           +--------------+
      | identity_db  |           | master_data  |           | project_db   |
      |              |           | _db          |           |              |
      +--------------+           +--------------+           +--------------+


      +--------------+           +--------------+           +--------------+
      | Engineering  |           | Production   |           | Quality      |
      | Service      |           | Service      |           | Service      |
      +------+-------+           +------+-------+           +------+-------+
             |                          |                          |
             v                          v                          v
      +--------------+           +--------------+           +--------------+
      | engineering  |           | production_db|           | quality_db   |
      | _db          |           |              |           |              |
      +--------------+           +--------------+           +--------------+


      +--------------+           +--------------+           +--------------+
      | Supply Chain |           | Logistics    |           | After Sales  |
      | Service      |           | Service      |           | Service      |
      +------+-------+           +------+-------+           +------+-------+
             |                          |                          |
             v                          v                          v
      +--------------+           +--------------+           +--------------+
      | supply_chain |           | logistics_db |           | after_sales  |
      | _db          |           |              |           | _db          |
      +--------------+           +--------------+           +--------------+


      +--------------+           +--------------+           +--------------+
      | Document     |           | Collaboration|           | Notification |
      | Service      |           | Service      |           | Service      |
      +------+-------+           +------+-------+           +------+-------+
             |                          |                          |
             v                          v                          v
      +--------------+           +--------------+           +--------------+
      | document_db  |           | collaboration|           | notification |
      |              |           | _db          |           | _db          |
      +--------------+           +--------------+           +--------------+


                              +----------------+
                              |     Kafka      |
                              +-------+--------+
                                      |
                    +-----------------+-----------------+
                    |                 |                 |
                    v                 v                 v
             +-------------+   +-------------+   +-------------+
             | Analytics   |   | Audit       |   | Notification|
             | Service     |   | Service     |   | Events      |
             +------+------+   +------+------+   +-------------+
                    |                 |
                    v                 v
             +-------------+   +-------------+
             | analytics_db|   | audit_db    |
             +-------------+   +-------------+


======================================================================
19. CROSS-DATABASE RELATIONSHIP RULE
======================================================================


IMPORTANT:

    Foreign keys are allowed ONLY inside the same database.

    Cross-service database references use UUID values.

Example:

    engineering_db
        |
        +---- products
                |
                +---- id = 8f4c...

                         |
                         | product_id
                         | NO DATABASE FK
                         v

    production_db
        |
        +---- work_orders
                |
                +---- product_id = 8f4c...


The Production Service validates the product through the
appropriate service/API/event mechanism.

DO NOT create:

    production_db.work_orders
          |
          X
          |
          +---- FOREIGN KEY
          |
          v
    engineering_db.products


This is intentionally avoided because each service owns its
own database.


======================================================================
20. DATA FLOW BETWEEN SERVICES
======================================================================


Synchronous Request:

    React
      |
      v
    Nginx / Apache
      |
      v
    Service Bridge
      |
      v
    Required Service
      |
      v
    Service-owned Database


Asynchronous Event:

    Service
      |
      | Domain Event
      v
    Kafka
      |
      +------------------+
      |                  |
      v                  v
    Analytics           Audit
    Service             Service
      |                  |
      v                  v
 analytics_db          audit_db


Example:

    Production Service
          |
          | WorkOrderCompleted
          v
        Kafka
          |
          +------------------------+
          |                        |
          v                        v
    Analytics Service        Audit Service
          |                        |
          v                        v
    analytics_db              audit_db


======================================================================
21. DATABASE DESIGN PRINCIPLES
======================================================================


1. Database per service.

2. Each service owns its database.

3. No direct cross-database foreign keys.

4. UUID is used for primary keys.

5. created_at and updated_at are used for auditability.

6. Important business records should not be hard deleted.

7. Use is_active where soft deletion is appropriate.

8. Use JSONB only where flexible/semi-structured data is required.

9. Operational data remains inside operational service databases.

10. Analytics uses separate analytical/read-model tables.

11. Kafka is used for asynchronous domain events.

12. Service Bridge is used for synchronous service routing.

13. Audit events are centralized in audit_db.

14. Documents and document versions are owned by document_db.

15. Each service should connect only to its own database.


======================================================================
                         END OF ER DIAGRAM
======================================================================