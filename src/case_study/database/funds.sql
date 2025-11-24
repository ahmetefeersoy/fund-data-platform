CREATE TABLE funds (
    code TEXT PRIMARY KEY,
    title TEXT,
    umbrella_code TEXT,
    founder TEXT,
    main_category TEXT,
    category TEXT,
    has_interest BOOLEAN,
    is_hedge BOOLEAN,
    currency_type TEXT
);
