# Наполнение интерфейса, отладка и стресс-тестирование

main_window.py — главное окно CRM, партнёры и их скидки загружаются из
partners_db. partner_service.py, discount.py и partners_update.sql — код
прошлых заданий, demo_data.sql — два партнёра для проверки.

```bash
python3 -m pip install psycopg2-binary
psql -d partners_db -f partners_update.sql
psql -d partners_db -f demo_data.sql
python3 main_window.py
```

Для каждого партнёра вызывается get_partner_with_discount из прошлого
задания, запрос дополнен типом из partner_types и ФИО директора. Таблица
sales_history из задания в нашей базе называется sales.

У партнёра без продаж SUM(quantity) даёт NULL. Без COALESCE в запросе в
функцию скидки пришёл бы None, и программа упала бы с TypeError.
demo_data.sql добавляет партнёра без продаж и партнёра с двумя продажами
на 12 000 шт. — в окне у них 0% и 5%.

Все карточки в окно не помещаются, поэтому список сделан через Canvas
с полосой прокрутки: обычный Frame прокручивать нельзя.
