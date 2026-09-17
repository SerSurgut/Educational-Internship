# Интеграция с БД и агрегация данных

partner_service.py — получение партнёра из partners_db вместе с суммой его продаж
и процентом скидки. discount.py — копия функции из задания «Разработка ядра
бизнес-логики».

```bash
python3 -m pip install psycopg2-binary
python3 partner_service.py
```

Таблица sales_history из задания в нашей базе называется sales.

get_partner_with_total выполняет запрос с LEFT JOIN и SUM(quantity). LEFT JOIN
нужен, чтобы находился и партнёр без продаж, но SUM для него даёт NULL, поэтому
сумма обёрнута в COALESCE(..., 0) — иначе в функцию скидки пришёл бы None.
get_partner_with_discount собирает из строки запроса словарь и добавляет в него
процент скидки.
