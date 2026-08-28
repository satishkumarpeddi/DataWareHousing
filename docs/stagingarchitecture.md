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