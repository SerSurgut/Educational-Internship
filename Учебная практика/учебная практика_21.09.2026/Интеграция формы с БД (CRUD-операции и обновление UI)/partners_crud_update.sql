ALTER TABLE partners ALTER COLUMN inn DROP NOT NULL;

ALTER TABLE partners ALTER COLUMN rating TYPE INT USING ROUND(rating);

SELECT company_name, inn, rating FROM partners ORDER BY partner_id;
