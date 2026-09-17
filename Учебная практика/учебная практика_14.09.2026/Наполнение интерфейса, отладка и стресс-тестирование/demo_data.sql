BEGIN;

INSERT INTO partners (partner_type_id, company_name, director_name, inn, contact_email, phone, rating)
VALUES ((SELECT partner_type_id FROM partner_types WHERE type_name = 'ООО'),
        'Тихая Гавань', 'Васильев Игорь Петрович', '7811223344', 'harbor@partner.ru', NULL, 3.00);

INSERT INTO partners (partner_type_id, company_name, director_name, inn, contact_email, phone, rating)
VALUES ((SELECT partner_type_id FROM partner_types WHERE type_name = 'ООО'),
        'Оптовый Двор', 'Морозова Елена Андреевна', '7811556677', 'opt@partner.ru', '+78123334455', 9.50);

INSERT INTO sales (partner_id, product_id, sale_date, quantity, unit_price)
VALUES ((SELECT partner_id FROM partners WHERE inn = '7811556677'), 1, CURRENT_DATE, 7000, 450.00),
       ((SELECT partner_id FROM partners WHERE inn = '7811556677'), 2, CURRENT_DATE, 5000, 450.00);

COMMIT;
