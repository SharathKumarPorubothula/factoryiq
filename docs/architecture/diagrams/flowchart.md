1. Projects Architecture

                 React
                   │
                   │ /api/v1/projects/*
                   ▼
              Custom Apache
                   │
                   ▼
             Service Bridge
                   │
                   ▼
             Project Service
                   │
                   ▼
             business_rules.py
                   │
                   ▼
               project_db
                   │
              ┌────┴────┐
              │         │
          transaction  outbox
                        │
                        ▼
                       Kafka
                        │
            ┌───────────┼────────────┐
            ▼           ▼            ▼
         Search     Analytics    Notification
                                      │
                                      ▼
                                    Audit