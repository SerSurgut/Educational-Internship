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


PARTNER_QUERY = """
SELECT p.partner_id,
       t.type_name,
       p.company_name,
       p.rating,
       p.address,
       p.director_name,
       p.phone,
       p.contact_email
FROM      partners      p
LEFT JOIN partner_types t ON t.partner_type_id = p.partner_type_id
WHERE     p.partner_id = %s
"""

INSERT_PARTNER = """
INSERT INTO partners (company_name, partner_type_id, rating, address,
                      director_name, phone, contact_email)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

UPDATE_PARTNER = """
UPDATE partners
SET    company_name    = %s,
       partner_type_id = %s,
       rating          = %s,
       address         = %s,
       director_name   = %s,
       phone           = %s,
       contact_email   = %s
WHERE  partner_id = %s
"""


def get_partner(connection, partner_id):
    cursor = connection.cursor()
    cursor.execute(PARTNER_QUERY, (partner_id,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        return None
    return {
        "partner_id": row[0],
        "partner_type": row[1],
        "company_name": row[2],
        "rating": row[3],
        "address": row[4],
        "director_name": row[5],
        "phone": row[6],
        "contact_email": row[7],
    }


def get_partner_type_id(connection, type_name):
    if type_name is None:
        return None
    cursor = connection.cursor()
    cursor.execute("SELECT partner_type_id FROM partner_types "
                   "WHERE type_name = %s", (type_name,))
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise ValueError(f"Тип партнера {type_name} не найден в справочнике."
                         "\n\nВыберите тип из списка и повторите попытку.")
    return row[0]


def get_partner_values(connection, partner):
    partner_type_id = get_partner_type_id(connection,
                                          partner["partner_type"])
    return [partner["company_name"], partner_type_id, partner["rating"],
            partner["address"], partner["director_name"], partner["phone"],
            partner["contact_email"]]


def add_partner(connection, partner):
    with connection:
        values = get_partner_values(connection, partner)
        cursor = connection.cursor()
        cursor.execute(INSERT_PARTNER, values)
        cursor.close()


def update_partner(connection, partner_id, partner):
    with connection:
        values = get_partner_values(connection, partner)
        cursor = connection.cursor()
        cursor.execute(UPDATE_PARTNER, values + [partner_id])
        updated = cursor.rowcount
        cursor.close()
        if updated == 0:
            raise ValueError(f"Партнер {partner_id} не найден в базе.\n\n"
                             "Закройте карточку и откройте партнера "
                             "из списка заново.")


if __name__ == "__main__":
    connection = psycopg2.connect(dbname="partners_db", host="localhost")
    for partner in get_partners_with_discount(connection):
        print(partner)
    connection.close()
