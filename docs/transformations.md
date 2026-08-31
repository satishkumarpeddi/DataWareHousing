# Transformations Using Python Programming Language:-

                 stocks.csv
                     │
                     ▼
              ┌─────────────┐
              │  extract.py │
              └──────┬──────┘
                     │
                     ▼
              Raw DataFrame
                     │
                     ▼
             ┌──────────────┐
             │ transform.py │
             └──────┬───────┘
                    │
                    ▼
          Transformed DataFrame
                    │
                    ▼
             ┌─────────────┐
             │ validate.py │  ← NEXT
             └──────┬──────┘
                    │
             ┌──────┴───────┐
             ▼              ▼
           VALID          INVALID
             │              │
             ▼              ▼
          staging       data_quality_errors
             │
             ▼
       Warehouse Loading
             │
       ┌─────┴─────┐
       ▼           ▼
     dim_date dim_company
       │           │
       └─────┬─────┘
             ▼
     fact_stock_prices
