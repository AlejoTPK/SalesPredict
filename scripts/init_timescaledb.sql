-- TimescaleDB initialization
-- Run automatically by docker-compose when postgres container starts

CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create hypertable for time-series sales data
-- We use the existing 'sales' table but create a materialized view
-- or hypertable for aggregated metrics. For simplicity with SQLAlchemy models,
-- we create a dedicated time-series metrics table that maps to raw sales.

CREATE TABLE IF NOT EXISTS sale_metrics (
    time TIMESTAMPTZ NOT NULL,
    product_id VARCHAR(100),
    region VARCHAR(255),
    total_amount DOUBLE PRECISION,
    total_quantity INTEGER,
    transaction_count INTEGER
);

SELECT create_hypertable('sale_metrics', 'time', if_not_exists => TRUE);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_sale_metrics_product ON sale_metrics (product_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_sale_metrics_region ON sale_metrics (region, time DESC);

-- Continuous aggregate for daily summaries
CREATE MATERIALIZED VIEW IF NOT EXISTS daily_sales_summary
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', time) AS bucket,
    product_id,
    region,
    SUM(total_amount) AS daily_amount,
    SUM(total_quantity) AS daily_quantity,
    SUM(transaction_count) AS daily_transactions
FROM sale_metrics
GROUP BY bucket, product_id, region
WITH NO DATA;

-- Add retention policy (keep 2 years of raw data, aggregated data forever)
SELECT add_retention_policy('sale_metrics', INTERVAL '2 years');
