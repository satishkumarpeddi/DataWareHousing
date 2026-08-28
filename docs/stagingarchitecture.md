staging
│
├── stock_prices
├── data_quality_errors
└── load_metadata 

                    STAGING
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
stock_prices    quality_errors    load_metadata
       │               │                │
       │               │                │
       └───────────────┴────────────────┘
                       │
                       ▼
                  WAREHOUSE

Day2: Task 5
============


       staging.stock_prices
              │
              ▼
       Extract unique
       tickers
              │
              ▼
       dim_company
              │
              ▼
       Map ticker → company_key
              │
              ▼
       Map date → date_key
              │
              ▼
       fact_stock_prices