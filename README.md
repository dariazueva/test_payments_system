# test_payments_system
Payments System — Django Webhook Processor. Тестовое задание

## Описание

Backend-сервис для приёма webhook-ов от банка с защитой от повторных операций (дублей) и корректным начислением баланса организации по ИНН.

Реализовано:
- Приём и обработка webhook от банка (POST `/api/webhook/bank/`)
- Начисление суммы на баланс организации
- Защита от повторной обработки одной и той же операции (operation_id)
- Получение текущего баланса организации по ИНН (GET `/api/organizations/<inn>/balance/`)

## Требования

- Python 3.12
- Django 5.2.1
- Django REST Framework 3.16.0
- MySQL

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:dariazueva/test_payments_system.git
cd payments_system 
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/Scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установите необходимые зависимости:

```bash
pip install -r requirements.txt

```

Создайте файл .env и заполните его своими данными по образцу:
```
MYSQL_NAME=payments_db
MYSQL_USER=payments_user
MYSQL_PASSWORD=secret
MYSQL_HOST=localhost
MYSQL_PORT=3307
```

#### Запустите проект.
```bash
python manage.py runserver
```
#### Выполните миграции.
```bash
python manage.py migrate
```
#### Создайте суперпользователя либо воспользуйтесь существующим.
```bash
python manage.py createsuperuser
```

### POST `/api/webhook/bank/`

#### Пример запроса
```json
{
  "operation_id": "ccf0a86d-041b-4991-bcf7-e2352f7b8a4a",
  "amount": 145000,
  "payer_inn": "1234567890",
  "document_number": "PAY-328",
  "document_date": "2024-04-27T21:00:00Z"
}
```

### Поведение

- Если операция уже была (`operation_id`) — ничего не делает, возвращает `200 OK`
  Требуется защита от дублей, то есть если приходит тот же самый вебхук, мы не должны заново пополнять баланс
- Если новая:
  - создаёт `Payment`
  - начисляет сумму на баланс организации с `payer_inn`
  - логирует изменение баланса (в отдельную таблицу или просто `print` / `log`)

### GET `/api/organizations/<inn>/balance/`

Возвращает текущий баланс организации по ИНН:
```json
{
  "inn": "1234567890",
  "balance": 145000
}
```

## Автор
Зуева Дарья Дмитриевна
Github https://github.com/dariazueva/