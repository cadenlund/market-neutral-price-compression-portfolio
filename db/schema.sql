-- 1) Metadata table for all tickers
CREATE TABLE IF NOT EXISTS ticker_metadata (
    ticker       TEXT        PRIMARY KEY,
    active       BOOLEAN     NOT NULL,
    market_cap   DOUBLE PRECISION,
    list_date    DATE,
    sic_code     TEXT
);

-- 2) OHLCV table, linked by a foreign key to ticker_metadata
CREATE TABLE IF NOT EXISTS ohlcv_data (
    time         TIMESTAMPTZ NOT NULL,
    ticker       TEXT        NOT NULL
        REFERENCES ticker_metadata(ticker)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    open         DOUBLE PRECISION NOT NULL,
    high         DOUBLE PRECISION NOT NULL,
    low          DOUBLE PRECISION NOT NULL,
    close        DOUBLE PRECISION NOT NULL,
    volume       DOUBLE PRECISION NOT NULL,
    transactions BIGINT       NOT NULL,
    PRIMARY KEY (time, ticker)
);

SELECT create_hypertable('ohlcv_data', 'time');