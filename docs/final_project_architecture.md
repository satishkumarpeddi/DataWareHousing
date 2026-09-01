                    S&P 500 CSV
                         │
                         ▼
                  ┌──────────────┐
                  │   EXTRACT    │
                  │   Python     │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  TRANSFORM   │
                  │   Pandas     │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   VALIDATE   │
                  │ Data Quality │
                  └──────┬───────┘
                         │
                         ▼
              ┌──────────────────────┐
              │       STAGING        │
              │   PostgreSQL         │
              │                      │
              │ stock_prices         │
              │ data_quality_errors  │
              │ load_metadata        │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │      WAREHOUSE       │
              │                      │
              │ dim_date             │
              │ dim_company          │
              │ fact_stock_prices    │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │      ANALYTICS       │
              │                      │
              │ daily_returns        │
              │ monthly_performance  │
              │ volatility           │
              │ company_performance  │
              │ market_summary       │
              └──────────┬───────────┘
                         │
                         ▼
                   ┌───────────┐
                   │  POWER BI │
                   │ Dashboard │
                   └───────────┘
