                     all_stocks_5yr.csv
                              │
                              ▼
                       Python + Pandas
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
               Validation          Transformation
                    │                   │
                    └─────────┬─────────┘
                              ▼
                         PostgreSQL
                              │
                              ▼
                         STAGING
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
               Valid records       Bad records
                    │                   │
                    ▼                   ▼
               WAREHOUSE         ERROR TABLE
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
    DIMENSIONS              FACT
          │                   │
          └─────────┬─────────┘
                    ▼
                ANALYTICS
                    │
                    ▼
                 Power BI