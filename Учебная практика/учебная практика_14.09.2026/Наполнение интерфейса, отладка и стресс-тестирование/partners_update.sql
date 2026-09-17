ALTER TABLE partners DROP COLUMN IF EXISTS partner_type_id;
ALTER TABLE partners DROP COLUMN IF EXISTS director_name;
DROP TABLE IF EXISTS partner_types;

CREATE TABLE partner_types (
    partner_type_id SERIAL      PRIMARY KEY,
    type_name       VARCHAR(10) NOT NULL UNIQUE
);

INSERT INTO partner_types (type_name) VALUES ('ООО'), ('ИП'), ('ТК');

ALTER TABLE partners
    ADD COLUMN partner_type_id INT REFERENCES partner_types (partner_type_id) ON DELETE RESTRICT,
    ADD COLUMN director_name   VARCHAR(150);

UPDATE partners
SET    partner_type_id = (SELECT partner_type_id FROM partner_types WHERE type_name = 'ООО'),
       company_name    = 'Логистик-Экспресс',
       director_name   = 'Смирнов Андрей Николаевич'
WHERE  inn = '7701234567';

UPDATE partners
SET    partner_type_id = (SELECT partner_type_id FROM partner_types WHERE type_name = 'ИП'),
       company_name    = 'Петров А.В.',
       director_name   = 'Петров Александр Владимирович'
WHERE  inn = '5001098765';

UPDATE partners
SET    partner_type_id = (SELECT partner_type_id FROM partner_types WHERE type_name = 'ТК'),
       company_name    = 'Быстрый Путь',
       director_name   = 'Кузнецова Ольга Сергеевна'
WHERE  inn = '7812345678';

UPDATE partners
SET    partner_type_id = (SELECT partner_type_id FROM partner_types WHERE type_name = 'ООО'),
       company_name    = 'Новый Партнёр',
       director_name   = 'Орлов Дмитрий Сергеевич'
WHERE  inn = '7799001122';

SELECT t.type_name, p.company_name, p.director_name
FROM      partners      p
LEFT JOIN partner_types t ON t.partner_type_id = p.partner_type_id
ORDER BY  p.partner_id;
