1. All Projects
Route
/projects
UI
┌──────────────────────────────────────────────────────────────────────────────┐
│ Projects                                      [+ Create Project]             │
│ Manage and track all projects                                                │
├──────────────────────────────────────────────────────────────────────────────┤
│ Search projects...                                                           │
│                                                                              │
│ Customer ▼   Site ▼   Program ▼   Status ▼   Health ▼   Owner ▼   Date ▼    │
├──────────────────────────────────────────────────────────────────────────────┤
│ Project    Name                    Customer   Site   Owner   Status   Health │
├──────────────────────────────────────────────────────────────────────────────┤
│ P-001      EV Battery Management   ABC        S01    Ravi    Active   GREEN  │
│ P-002      EV Power Electronics    XYZ        S02    John    Active   AMBER  │
│ P-003      Smart Assembly Line     ABC        S03    Kumar   Active   GREEN  │
│ P-004      Vision Inspection       XYZ        S02    Priya   Delayed  RED    │
│ P-005      Next Gen Controller     ABC        S01    Ravi    Draft    —      │
├──────────────────────────────────────────────────────────────────────────────┤
│ Showing 1–5 of 25                         ◀ 1  2  3  4  5 ▶                  │
└──────────────────────────────────────────────────────────────────────────────┘
API
GET /api/v1/projects
2. My Projects
Route
/projects/my
Purpose

Only projects where the logged-in user is a member/owner.

UI
┌──────────────────────────────────────────────────────────────────────────────┐
│ My Projects                                                                  │
│ Projects assigned to you                                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│ Search my projects...                                                        │
│                                                                              │
│ Status ▼   Health ▼   Role ▼   Date ▼                                       │
├──────────────────────────────────────────────────────────────────────────────┤
│ Project   Name                     My Role          Status     Health        │
├──────────────────────────────────────────────────────────────────────────────┤
│ P-001     EV Battery Management    Project Manager   Active     GREEN         │
│ P-002     EV Power Electronics     Engineering Lead  Active     AMBER         │
│ P-004     Vision Inspection        Project Manager   Delayed    RED           │
├──────────────────────────────────────────────────────────────────────────────┤
│ 3 Projects                                                                  │
└──────────────────────────────────────────────────────────────────────────────┘
API
GET /api/v1/projects/my
3. Create Project
Route
/projects/new
UI
┌──────────────────────────────────────────────────────────────┐
│ Create Project                                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Project Code *       [ P-006                         ]        │
│                                                              │
│ Project Name *       [ _____________________________ ]        │
│                                                              │
│ Program *            [ Select Program ▼              ]        │
│                                                              │
│ Customer *           [ Select Customer ▼             ]        │
│                                                              │
│ Site *               [ Select Site ▼                 ]        │
│                                                              │
│ Facility             [ Select Facility ▼             ]        │
│                                                              │
│ Owner *              [ Select Owner ▼                ]        │
│                                                              │
│ Start Date *         [ DD/MM/YYYY                    ]        │
│                                                              │
│ Target Date *        [ DD/MM/YYYY                    ]        │
│                                                              │
│ Description          [                              ]         │
│                      [                              ]         │
│                                                              │
│ Status               [ Draft ▼                       ]        │
│                                                              │
│                         [Cancel]  [Create Project]            │
└──────────────────────────────────────────────────────────────┘
API
POST /api/v1/projects
Flow
Create Project
      ↓
Validation
      ↓
Project DB transaction
      ↓
Outbox
      ↓
ProjectCreated
      ↓
Kafka
4. Programs
Route
/projects/programs
UI
┌─────────────────────────────────────────────────────────────────────┐
│ Programs                                      [+ Create Program]     │
├─────────────────────────────────────────────────────────────────────┤
│ Search programs...                                                  │
│                                                                     │
│ Status ▼   Start Date ▼   End Date ▼                                │
├─────────────────────────────────────────────────────────────────────┤
│ Program                  Projects   Status       Start       End     │
├─────────────────────────────────────────────────────────────────────┤
│ EV Platform Program      2          Active       Jan 2026    Dec 27  │
│ Industrial Automation    2          Active       Mar 2026    Sep 27  │
│ Next Generation Ctrl     1          Planning     Sep 2026    Mar 28  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
API
GET /api/v1/programs

Create:

POST /api/v1/programs
5. Milestones

This is the global milestone page.

Route
/projects/milestones
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ Milestones                                      [+ Add Milestone]            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Search milestones...                                                        │
│                                                                             │
│ Project ▼   Status ▼   Due Date ▼   Owner ▼                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Project   Milestone              Due Date      Status       Progress        │
├─────────────────────────────────────────────────────────────────────────────┤
│ P-001     Requirements Complete  15 Sep 2026   Completed     100%           │
│ P-001     BOM Release             15 Oct 2026   In Progress    60%           │
│ P-001     Prototype Build         30 Nov 2026   Pending         0%           │
│ P-002     Architecture            01 Oct 2026   Completed     100%           │
│ P-003     Equipment Installation  15 Nov 2026   In Progress    40%           │
│ P-004     AI Model Training       15 Oct 2026   Delayed         20%           │
└─────────────────────────────────────────────────────────────────────────────┘
API

Global:

GET /api/v1/milestones

Project-specific:

GET  /api/v1/projects/{id}/milestones
POST /api/v1/projects/{id}/milestones
6. Dependencies
Route
/projects/dependencies
UI
┌─────────────────────────────────────────────────────────────────────┐
│ Project Dependencies                                                │
├─────────────────────────────────────────────────────────────────────┤
│ Search...                                                           │
│                                                                     │
│ Project ▼   Dependency Type ▼   Status ▼                            │
├─────────────────────────────────────────────────────────────────────┤
│ Predecessor          Dependency       Successor          Status      │
├─────────────────────────────────────────────────────────────────────┤
│ P-001 EV Battery     Finish→Start    P-002 Power Elec   Active      │
│ P-001 EV Battery     Finish→Start    P-003 Assembly     Active      │
│ P-003 Assembly       Finish→Start    P-004 Vision       Active      │
└─────────────────────────────────────────────────────────────────────┘
API
GET /api/v1/dependencies

For a project:

GET  /api/v1/projects/{id}/dependencies
POST /api/v1/projects/{id}/dependencies
7. Risks
Route
/projects/risks
UI
┌──────────────────────────────────────────────────────────────────────────┐
│ Project Risks                                      [+ Add Risk]           │
├──────────────────────────────────────────────────────────────────────────┤
│ Search risks...                                                           │
│                                                                          │
│ Project ▼   Severity ▼   Probability ▼   Impact ▼   Status ▼              │
├──────────────────────────────────────────────────────────────────────────┤
│ Project   Risk                     Probability   Impact     Status        │
├──────────────────────────────────────────────────────────────────────────┤
│ P-001     Battery Supplier Delay   High          High       Open          │
│ P-001     Component Availability   Medium        High       Open          │
│ P-002     Thermal Performance     Medium        High       Open          │
│ P-003     Equipment Installation  High          High       Open          │
│ P-004     Insufficient Training   High          Critical   Open          │
└──────────────────────────────────────────────────────────────────────────┘
API
GET /api/v1/risks

Project-specific:

GET  /api/v1/projects/{id}/risks
POST /api/v1/projects/{id}/risks
8. Project Reports
Route
/projects/reports
UI
┌──────────────────────────────────────────────────────────────────────┐
│ Project Reports                                                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ Project              [ Select Project ▼ ]                            │
│                                                                      │
│ Report Type          [ Project Status ▼ ]                            │
│                                                                      │
│ Date Range            [ From ]  [ To ]                               │
│                                                                      │
│                              [Generate Report]                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ Project Status Summary                                               │
│                                                                      │
│ Total Projects          25                                           │
│ Active                  18                                           │
│ Delayed                  4                                           │
│ Completed                2                                           │
│ Draft                    1                                           │
│                                                                      │
│                    [Export PDF] [Export Excel]                       │
└──────────────────────────────────────────────────────────────────────┘
API
GET /api/v1/projects/{id}/reports
Now Project Detail Pages

When the user clicks:

P-001

navigate to:

/projects/P-001/overview

The project header should remain visible across all tabs.

9. Project Detail — Overview
Route
/projects/:id/overview
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ ← Projects                                                                  │
│                                                                             │
│ P-001 — EV Battery Management System                    ● GREEN             │
│ ABC Corp | Site S01 | Program: EV Platform | Owner: Ravi                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ PROJECT INFORMATION                                                        │
│ ┌─────────────────────┐  ┌─────────────────────┐                            │
│ │ Status              │  │ Health              │                            │
│ │ Active              │  │ GREEN               │                            │
│ └─────────────────────┘  └─────────────────────┘                            │
│                                                                             │
│ ┌─────────────────────┐  ┌─────────────────────┐                            │
│ │ Start Date          │  │ Target Date         │                            │
│ │ 15 Jan 2026         │  │ 30 Jun 2027         │                            │
│ └─────────────────────┘  └─────────────────────┘                            │
├──────────────────────────────┬──────────────────────────────────────────────┤
│ Milestones                   │ Risks                                        │
│                              │                                              │
│ Total       5                │ Open Risks               2                   │
│ Completed   1                │ High                     2                   │
│ In Progress 1                │ Critical                 0                   │
│ Pending     3                │                                              │
├──────────────────────────────┴──────────────────────────────────────────────┤
│ Domain Status                                                               │
│                                                                             │
│ Engineering       ● GREEN                                                   │
│ Production        ● AMBER                                                   │
│ Quality           ● GREEN                                                   │
│ Supply Chain      ● RED                                                     │
│ Logistics         ● GREEN                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
API
GET /api/v1/projects/{id}
10. Project Detail — Milestones
Route
/projects/:id/milestones
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ P-001 — EV Battery Management System                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Milestones                                      [+ Add Milestone]           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Milestone              Due Date       Status          Description           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Requirements Complete  15 Sep 2026    Completed       System requirements   │
│ BOM Release             15 Oct 2026    In Progress     Release BOM          │
│ Prototype Build         30 Nov 2026    Pending         Build prototype      │
│ Qualification           30 Jan 2027    Pending         Product qualification│
│ NPI Release             15 Mar 2027    Pending         NPI release          │
└─────────────────────────────────────────────────────────────────────────────┘
APIs
GET  /api/v1/projects/{id}/milestones
POST /api/v1/projects/{id}/milestones
11. Project Detail — Requirements
Route
/projects/:id/requirements

This is Engineering Service, not Project Service.

UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ P-001 — Requirements                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Requirements                                      [+ Add Requirement]       │
├─────────────────────────────────────────────────────────────────────────────┤
│ ID        Requirement              Priority    Status       Owner           │
├─────────────────────────────────────────────────────────────────────────────┤
│ REQ-001   Battery voltage range    High        Approved     Ravi            │
│ REQ-002   Thermal protection       Critical    Approved     John            │
│ REQ-003   Communication protocol   Medium      In Review    Priya           │
│ REQ-004   Safety requirement       Critical    Draft        Kumar           │
└─────────────────────────────────────────────────────────────────────────────┘
API
GET /api/v1/requirements?project_id={id}

Service:

Engineering Service
12. Project Detail — Engineering
Route
/projects/:id/engineering
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ P-001 — Engineering                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Engineering Status                                                         │
│                                                                             │
│ Products       3             BOMs             4                            │
│ Drawings       18            Revisions        7                            │
│ Open ECO       2             Open ECR          1                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Product / BOM Status                                                       │
│                                                                             │
│ Product       BOM         Revision       Status                            │
│ Battery ECU   BOM-001     Rev C         Released                           │
│ Power Unit    BOM-002     Rev B         In Review                          │
│ Controller    BOM-003     Rev A         Draft                              │
└─────────────────────────────────────────────────────────────────────────────┘
API

Examples:

GET /api/v1/products?project_id={id}
GET /api/v1/boms?project_id={id}
GET /api/v1/drawings?project_id={id}
GET /api/v1/revisions?project_id={id}
GET /api/v1/ecos?project_id={id}
GET /api/v1/ecrs?project_id={id}
13. Project Detail — Production
Route
/projects/:id/production
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ P-001 — Production                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Production KPIs                                                            │
│                                                                             │
│ Planned       12,500        Actual        11,980                           │
│ Achievement      95.8%      Yield            97.2%                         │
│ WIP                630      Scrap              125                         │
│ Rework              84                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Work Orders                                                                │
│                                                                             │
│ WO        Product       Line       Qty       Status                         │
│ WO-001    Battery ECU   Line 01    2,000     Released                       │
│ WO-002    Battery ECU   Line 02    3,000     In Progress                    │
│ WO-003    Power Unit    Line 01    1,500     Completed                      │
└─────────────────────────────────────────────────────────────────────────────┘
APIs
GET /api/v1/production/summary?project_id={id}
GET /api/v1/work-orders?project_id={id}
GET /api/v1/wip?project_id={id}
GET /api/v1/production-results?project_id={id}
14. Project Detail — Quality
Route
/projects/:id/quality
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ P-001 — Quality                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Quality KPIs                                                               │
│                                                                             │
│ Pass Rate       96.4%       Defect Rate       2.1%                         │
│ Open NCR            12       Open CAPA            7                         │
│ Critical NCR         3       Overdue CAPA         2                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Quality Issues                                                             │
│                                                                             │
│ NCR        Type              Severity      Status                           │
│ NCR-001    Assembly defect   High          Open                             │
│ NCR-002    Material defect   Critical      Open                             │
│ NCR-003    Process issue     Medium        CAPA                             │
└─────────────────────────────────────────────────────────────────────────────┘
APIs
GET /api/v1/quality/summary?project_id={id}
GET /api/v1/inspections?project_id={id}
GET /api/v1/ncrs?project_id={id}
GET /api/v1/capas?project_id={id}
15. Project Detail — Supply Chain
Route
/projects/:id/supply-chain
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ P-001 — Supply Chain                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Supply Chain KPIs                                                          │
│                                                                             │
│ Material Requirements     42                                               │
│ Available                 31                                               │
│ Shortages                  8                                               │
│ Pending POs               12                                               │
│ Supplier Delays            3                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Material Shortages                                                          │
│                                                                             │
│ Part          Required     Available     Shortage      Status                │
│ BAT-CELL-01   10,000       8,000        2,000         Critical              │
│ SENSOR-02      5,000       4,700          300         Open                  │
│ PCB-100        3,000       2,800          200         Open                  │
└─────────────────────────────────────────────────────────────────────────────┘
APIs
GET /api/v1/supply-chain/summary?project_id={id}
GET /api/v1/material-requirements?project_id={id}
GET /api/v1/purchase-orders?project_id={id}
GET /api/v1/shortages?project_id={id}
16. Project Detail — Logistics
Route
/projects/:id/logistics
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ P-001 — Logistics                                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Shipment Summary                                                           │
│                                                                             │
│ Total Shipments     18        In Transit       7                            │
│ Delivered            9        Delayed          2                            │
│ Customs Pending      1        Exceptions       2                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Shipments                                                                   │
│                                                                             │
│ Shipment    Destination     Mode       ETA          Status                  │
│ SH-001      Hyderabad       Road       10 Sep       In Transit               │
│ SH-002      Pune            Air        08 Sep       Delivered                │
│ SH-003      Chennai         Road       15 Sep       Delayed                  │
└─────────────────────────────────────────────────────────────────────────────┘
APIs
GET /api/v1/shipments?project_id={id}
GET /api/v1/shipment-exceptions?project_id={id}
17. Project Detail — Documents
Route
/projects/:id/documents
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ P-001 — Documents                                      [+ Upload Document]  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Search documents...                                                        │
│ Type ▼    Status ▼    Version ▼    Owner ▼                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Document             Type          Version    Status        Updated          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Battery Specification Engineering   v3         Approved      30 Aug 2026     │
│ Design Drawing       Drawing        v5         Released      29 Aug 2026     │
│ Test Plan            Test           v2         Review        28 Aug 2026     │
│ Quality Plan         Quality        v1         Approved      27 Aug 2026     │
└─────────────────────────────────────────────────────────────────────────────┘
API
GET /api/v1/documents?project_id={id}

Document Service owns this.

18. Project Detail — Risks
Route
/projects/:id/risks
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ P-001 — Risks                                        [+ Add Risk]           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Risk Register                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Risk                     Probability    Impact      Status                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Battery Supplier Delay   High           High        Open                    │
│ Component Availability   Medium         High        Open                    │
│ Prototype Delay          Medium         Medium      Mitigated                │
└─────────────────────────────────────────────────────────────────────────────┘
APIs
GET  /api/v1/projects/{id}/risks
POST /api/v1/projects/{id}/risks
19. Project Detail — Collaboration
Route
/projects/:id/collaboration
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ P-001 — Collaboration                                   [+ New Thread]      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Project Discussions                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ 🔵 BOM Release Discussion                              8 messages           │
│    Ravi: Please review BOM revision C.                  2 hours ago         │
│                                                                             │
│ 🔵 Supplier Delay                                      12 messages          │
│    Priya: Supplier confirmed 3-day delay.               4 hours ago         │
│                                                                             │
│ 🔵 Prototype Test Plan                                  5 messages          │
│    John: Test plan uploaded for review.                  1 day ago          │
└─────────────────────────────────────────────────────────────────────────────┘
API
GET /api/v1/threads?project_id={id}

Thread messages:

GET  /api/v1/threads/{thread_id}/messages
POST /api/v1/threads/{thread_id}/messages
20. Project Detail — Audit
Route
/projects/:id/audit
UI
┌─────────────────────────────────────────────────────────────────────────────┐
│ P-001 — Audit History                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Overview | Milestones | Requirements | Engineering | Production | Quality  │
│ Supply Chain | Logistics | Documents | Risks | Collaboration | Audit       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Filter: User ▼   Action ▼   Date ▼                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Date/Time          User       Action                 Object                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 31 Aug 10:30       Ravi       Project Updated        P-001                  │
│ 30 Aug 15:20       John       Milestone Completed    MS-001                 │
│ 29 Aug 11:40       Priya      Risk Created           RISK-002               │
│ 28 Aug 09:15       Ravi       Project Created        P-001                  │
└─────────────────────────────────────────────────────────────────────────────┘
API
GET /api/v1/audit/events?project_id={id}

Audit Service owns this.

Final Project UI Navigation

Your actual sidebar should therefore look like:

Projects
│
├── Overview
│
├── All Projects
│
├── My Projects
│
├── Programs
│
├── Milestones
│
├── Dependencies
│
├── Risks
│
└── Reports

And when a project is opened:

P-001 — EV Battery Management System
│
├── Overview
├── Milestones
├── Requirements
├── Engineering
├── Production
├── Quality
├── Supply Chain
├── Logistics
├── Documents
├── Risks
├── Collaboration
└── Audit
The implementation order I recommend

Don't build these 20 pages randomly. Build them in this order:

1.  All Projects
        ↓
2.  Create Project
        ↓
3.  Project Overview
        ↓
4.  My Projects
        ↓
5.  Programs
        ↓
6.  Milestones
        ↓
7.  Dependencies
        ↓
8.  Risks
        ↓
9.  Project Reports
        ↓
10. Requirements
        ↓
11. Engineering
        ↓
12. Production
        ↓
13. Quality
        ↓
14. Supply Chain
        ↓
15. Logistics
        ↓
16. Documents
        ↓
17. Collaboration
        ↓
18. Audit

The first 9 pages belong primarily to the Projects experience, while pages 10–18 are project-context views of other microservices.

Most importantly, when we start coding, we should not create one giant Projects backend containing all those domains. For example:

/projects/P-001/engineering
        ↓
Service Bridge
        ↓
Engineering Service
        ↓
engineering_db

while:

/projects/P-001/milestones
        ↓
Service Bridge
        ↓
Project Service
        ↓
project_db

That distinction will keep the FactoryIQ architecture exactly aligned with the design you provided.