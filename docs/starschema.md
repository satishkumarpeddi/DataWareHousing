                         ┌─────────────────────┐
                         │      dim_date       │
                         ├─────────────────────┤
                         │ PK date_key         │
                         │ full_date           │
                         │ day_number          │
                         │ day_name            │
                         │ month_number        │
                         │ month_name          │
                         │ quarter_number      │
                         │ year_number         │
                         │ day_of_week         │
                         │ is_weekend          │
                         └──────────┬──────────┘
                                    │
                                    │
                                    │
                                    ▼
┌─────────────────────┐   ┌─────────────────────────┐
│    dim_company      │   │   fact_stock_prices     │
├─────────────────────┤   ├─────────────────────────┤
│ PK company_key      │◄──│ FK company_key          │
│ ticker              │   │ FK date_key             │
│ company_name        │   │ open_price              │
│ sector              │   │ high_price              │
│ industry            │   │ low_price               │
│ effective_date      │   │ close_price             │
│ expiry_date         │   │ volume                  │
│ is_current          │   └─────────────────────────┘
└─────────────────────┘