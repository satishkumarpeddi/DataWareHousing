```
        INSERT INTO staging.load_metadata (
        source_file,
        status
    )
    VALUES (
        'all_stocks_5yr.csv',
        'RUNNING'
    )
    RETURNING load_id;

    Note:-
    """
        returning is used to return the value from the "tuple".

        The above query returns the value `load_id` from the "tuple"/"row"
    """
```