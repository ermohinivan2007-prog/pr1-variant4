# Практическая работа №1

## Описание

Прототип веб-приложения, в котором данные хранятся в памяти (не на диске). Реализована модель слоя доступа к данным и REPL для работы с ней.

Вариант №4. ER-диаграмма содержит три сущности: Member, Assignment, Output. Между ними связи: задание ссылается на участника, а вывод — на задание.

## Требования

- Python 3.10+

## Как запустить

На Linux или Mac:

python3 -m src.data_model

## Как пользоваться

После запуска открывается консоль (REPL), куда можно вводить команды. Доступные команды:

- create_member — создаёт нового участника (спрашивает timestamp, locale, platform, user_agent)
- get_members — показывает всех участников
- get_member_by_id — ищет участника по uid
- update_member — редактирует участника (пустая строка — поле не меняется)
- create_assignment — создаёт задание (спрашивает timestamp, input, uid участника, status)
- get_assignments — показывает все задания
- get_assignment_by_id — ищет задание по uid
- update_assignment — редактирует задание
- create_output — создаёт вывод (спрашивает timestamp, response, status, exception, uid задания, cache_hit)
- get_outputs — показывает все выводы
- get_output_by_id — ищет вывод по uid
- update_output — редактирует вывод
- select_recent_assignments — сложный запрос: соединяет таблицы Member и Assignment и фильтрует по времени
- exit — завершает программу

## Про сущности

Member — участник. Хранит timestamp, locale, platform и user_agent.

Assignment — задание. Хранит member (uid участника), timestamp, input и status.

Output — вывод. Хранит assignment (uid задания), timestamp, response, status, exception и cache_hit.

Данные лежат в списках: каждая запись — список полей в порядке, определённом ER-диаграммой.

## Что сделано на данный момент

- Модель слоя доступа к данным (пункты 1, 2 задания)
- Сложный запрос с соединением таблиц (пункт 3)
- REPL с обработкой ошибок (пункты 4 и 5)
- Скриншоты работы в docs/screenshots