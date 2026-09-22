INSERT INTO partner_types (type_name) VALUES ('ЗАО')
ON CONFLICT (type_name) DO NOTHING;

ALTER TABLE partners ADD COLUMN IF NOT EXISTS address VARCHAR(255);

SELECT type_name FROM partner_types ORDER BY type_name;
