SELECT p.company_name,
       p.inn,
       p.phone,
       COUNT(s.sale_id) AS deliveries
FROM      partners p
LEFT JOIN sales    s ON s.partner_id = p.partner_id
GROUP BY  p.partner_id, p.company_name, p.inn, p.phone
ORDER BY  p.company_name;

BEGIN;

INSERT INTO partners (company_name, inn, contact_email, phone, rating)
VALUES ('ООО "Новый Партнёр"', '7799001122', 'new@partner.ru', '+79012345678', 4.50);

INSERT INTO sales (partner_id, product_id, sale_date, quantity, total_amount)
VALUES (currval('partners_partner_id_seq'), 1, CURRENT_DATE, 10, 4990.00);

COMMIT;

SELECT p.company_name, s.sale_date, s.total_amount
FROM      partners p
JOIN      sales    s ON s.partner_id = p.partner_id
WHERE     p.inn = '7799001122';

\set ON_ERROR_STOP off
BEGIN;
    INSERT INTO partners (company_name, inn) VALUES ('ООО "Откат"', '7700000000');
    INSERT INTO sales (partner_id, product_id, sale_date, quantity, total_amount)
    VALUES (1, 999, CURRENT_DATE, 1, 100.00);
ROLLBACK;
\set ON_ERROR_STOP on

SELECT COUNT(*) FROM partners WHERE inn = '7700000000';

SELECT s.sale_date,
       pr.product_name,
       s.quantity,
       s.total_amount
FROM   sales    s
JOIN   products pr ON pr.product_id = s.product_id
WHERE  s.partner_id = 1
  AND  s.sale_date BETWEEN '2026-03-01' AND '2026-03-31'
ORDER BY s.sale_date;

SELECT SUM(s.quantity) AS total_quantity,
       SUM(s.total_amount) AS total_sum
FROM   sales s
WHERE  s.partner_id = 1
  AND  s.sale_date BETWEEN '2026-03-01' AND '2026-03-31';
