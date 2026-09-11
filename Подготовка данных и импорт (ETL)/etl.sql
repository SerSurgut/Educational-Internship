DROP TABLE IF EXISTS stg_partners;
CREATE TABLE stg_partners (
    partner_id text, company_name text, inn text,
    contact_email text, phone text, rating text
);

DROP TABLE IF EXISTS stg_sales;
CREATE TABLE stg_sales (
    sale_id text, partner_id text, product_name text,
    sale_date text, quantity text, total_amount text
);

\copy stg_partners FROM 'data/import_partners.csv' WITH (FORMAT csv, HEADER true, QUOTE E'\b')
\copy stg_sales    FROM 'data/import_sales.txt'    WITH (FORMAT csv, HEADER true, DELIMITER E'\t', QUOTE E'\b')

INSERT INTO partners (partner_id, company_name, inn, contact_email, phone, rating)
SELECT partner_id::int,
       trim(company_name),
       inn,
       lower(trim(contact_email)),
       nullif('+7' || right(regexp_replace(phone, '[^0-9]', '', 'g'), 10), '+7'),
       nullif(trim(rating), '')::decimal
FROM   stg_partners;

INSERT INTO products (product_name)
SELECT DISTINCT trim(product_name)
FROM   stg_sales;

INSERT INTO sales (sale_id, partner_id, product_id, sale_date, quantity, total_amount)
SELECT s.sale_id::int,
       s.partner_id::int,
       p.product_id,
       CASE WHEN s.sale_date LIKE '__.__.____'
            THEN to_date(s.sale_date, 'DD.MM.YYYY')
            ELSE to_date(s.sale_date, 'YYYY-MM-DD')
       END,
       s.quantity::int,
       s.total_amount::decimal
FROM   stg_sales s
JOIN   products p ON p.product_name = trim(s.product_name)
WHERE  s.partner_id::int IN (SELECT partner_id FROM partners);

SELECT setval('partners_partner_id_seq', (SELECT max(partner_id) FROM partners));
SELECT setval('products_product_id_seq', (SELECT max(product_id) FROM products));
SELECT setval('sales_sale_id_seq',       (SELECT max(sale_id)    FROM sales));

SELECT COUNT(*) AS partners_count FROM partners;
SELECT COUNT(*) AS products_count FROM products;
SELECT COUNT(*) AS sales_count    FROM sales;

SELECT s.sale_id, s.partner_id, 'нет такого партнёра в справочнике' AS reason
FROM   stg_sales s
WHERE  s.partner_id::int NOT IN (SELECT partner_id FROM partners);
