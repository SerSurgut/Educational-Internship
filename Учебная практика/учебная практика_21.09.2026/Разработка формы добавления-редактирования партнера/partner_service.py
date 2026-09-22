import psycopg2

from discount import calculate_partner_discount

PARTNER_TOTAL_QUERY = """
SELECT p.partner_id,
       t.type_name,
       p.company_name,
       p.director_name,
       p.inn,
       p.contact_email,
       p.phone,
       p.rating,
       COALESCE(SUM(s.quantity), 0) AS total_quantity
FROM      partners      p
LEFT JOIN partner_types t ON t.partner_type_id = p.partner_type_id
LEFT JOIN sales         s ON s.partner_id = p.partner_id
WHERE     p.partner_id = %s
GROUP BY  p.partner_id, t.type_name, p.company_name, p.director_name,
          p.inn, p.contact_email, p.phone, p.rating
"""


def get_partner_with_total(connection, partner_id):
    cursor = connection.cursor()
    cursor.execute(PARTNER_TOTAL_QUERY, (partner_id,))
    row = cursor.fetchone()
    cursor.close()
    return row


def get_partner_with_discount(connection, partner_id):
    row = get_partner_with_total(connection, partner_id)
    if row is None:
        return None
    return {
        "partner_id": row[0],
        "partner_type": row[1],
        "company_name": row[2],
        "director_name": row[3],
        "inn": row[4],
        "contact_email": row[5],
        "phone": row[6],
        "rating": row[7],
        "total_quantity": row[8],
        "discount": calculate_partner_discount(row[8]),
    }


def get_partner_ids(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT partner_id FROM partners ORDER BY partner_id")
    rows = cursor.fetchall()
    cursor.close()
    return [row[0] for row in rows]


def get_partner_types(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT type_name FROM partner_types ORDER BY type_name")
    rows = cursor.fetchall()
    cursor.close()
    return [row[0] for row in rows]


def get_partners_with_discount(connection):
    partners = []
    for partner_id in get_partner_ids(connection):
        partners.append(get_partner_with_discount(connection, partner_id))
    return partners


if __name__ == "__main__":
    connection = psycopg2.connect(dbname="partners_db", host="localhost")
    for partner in get_partners_with_discount(connection):
        print(partner)
    connection.close()
