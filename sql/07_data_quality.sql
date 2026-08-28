Check total records:-
===================

select count(*) as total_records from staging.stock_price;

Check NULL values:-
=================

select 
    count(*) filter (where date is null) as null_date,
    count(*) filter (where open_price is null) as null_open,
    count(*) filter (where high_price is null) as null_high,
    count(*) filter (where low_price is null) as null_low,
    count(*) filter (where close_price is null) as 
    null_close,
    count(*) filter (where volume is null) as null_volume,
    count(*) filter (where ticker is null) as null_ticker
from staging.stock_prices;

Check duplicate records:-
=======================

select ticker,  
       date,
       count(*) ad duplicate_count
from staging.stock_prices
group by ticker, date
having count(*) > 1
order by duplicate_count desc;

Note:-
"""
    Before deleting the duplicate tuples / rows check wheather they are `True Duplicate Values Or Not`
"""

Checking True Duplicate Values:-
==============================

```
    SELECT *
    FROM staging.stock_prices
    WHERE (ticker, date) IN (
        SELECT ticker, date
        FROM staging.stock_prices
        GROUP BY ticker, date
        HAVING COUNT(*) > 1
    )
    ORDER BY ticker, date;
```

Count duplicate rows:-
====================

```
    select 
        count(*) - count(distinct (ticker,date)) as duplicate_rows 
    from staging.stock_prices;
```

Validate OHLC Prices:-
====================

```
    select * from staging.stock_prices
    where open_price <=0
        or high_price <=0
        or low_price <=0 
        or close_price <=0;
```

Validate High >= Low:-
====================

```
    select * from staging.stock_prices 
    where high_price < low_price;
```

Validate High against Open and Close:-
====================================

```
    select * 
    from staging.stock_prices
    where high_price<  low_price
        or high_price < close_price;
```

Validate Low against Open and Close:-
===================================

```
    select * from staging.stock_prices
    where low_price > open_price
        or low_price > close_price;
```

Validate Volume:-
===============

```
    select * from staging.stock_price 
    where volume < 0;
```

Check ticker quality:-
====================

```
    select count(distinct ticker) as total_companies
    from staging.stock_prices;
```

Check data range:-
================

```
    select min(date) as first_trading_date,
    max(date) as last_trading_date
    from staging.stock_prices;
```

Check the date types:-
====================

```
    select column_name,data_type 
    from information_schema.columns
    where table_schema = 'staging'
        and table_name = 'stock_prices'
        order by ordinal_position;

    Note:-
    """
        ordinal_position--> It is the structure in which the stock_prices is been defined.
    """
```

