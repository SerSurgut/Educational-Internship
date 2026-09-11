DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS partners;

CREATE TABLE partners (
    partner_id    SERIAL       PRIMARY KEY,
    company_name  VARCHAR(150) NOT NULL,
    inn           VARCHAR(12)  NOT NULL UNIQUE,
    contact_email VARCHAR(120) UNIQUE,
    phone         VARCHAR(20),
    rating        DECIMAL(3,2) CHECK (rating BETWEEN 0 AND 5)
);

CREATE TABLE products (
    product_id   SERIAL       PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE sales (
    sale_id      SERIAL        PRIMARY KEY,
    partner_id   INT           NOT NULL REFERENCES partners (partner_id) ON DELETE RESTRICT,
    product_id   INT           NOT NULL REFERENCES products (product_id) ON DELETE RESTRICT,
    sale_date    DATE          NOT NULL,
    quantity     INT           NOT NULL CHECK (quantity > 0),
    total_amount DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0)
);

CREATE INDEX idx_sales_partner ON sales (partner_id);
