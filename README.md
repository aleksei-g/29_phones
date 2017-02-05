# Microservice for Search Index of Phone Numbers

Данный проект позволяет нормализовать телефонные номера, хранящиется 
в произвольном формате в read-only базе данных заказов интернет магазина. 

# Установка

Для корректоной работы необходимо выполнить установку модулей, перечисленных в
файле `requirements.txt`, запустив команду: 
```
pip install -r requirements.txt
```

# Использование

**1 Шаг**

Создать копию базы данных, с помощью скрипта `copying_db.py`, предварительно
указав в файле `config.py` параметр `DEST_DATABASE_URI` - database uri 
создаваемой копии базы данных.

*Пример:*
```
DEST_DATABASE_URI = 'postgresql://postgres:postgres@localhost/shop' 
```

*Запуск скрипта для создания копии бд:*
```
python3 copying_db.py
```

**2 Шаг**

Следующим действием необходимо запустить подготовленную миграцию базы данных, 
которая добавит в созданную на 1м шаге базу данных в таблицу заказов новую
колонку для нормализованного телефонного номера. Миграция осуществляется 
средствами **alembic**, поэтому перед ее применением, необходимо в 
конфигурационном файле `alembic.ini` изменить параметр `sqlalchemy.url`, в
который необходимо передать database uri вашей базы данных.

*Пример:*
```
sqlalchemy.url = postgresql://postgres:postgres@localhost/shop
```

Для запуска миграции выполнить следующую команду в терминале находясь в 
каталоге проекта: 
```
alembic upgrade head
```

**3 Шаг**

Запуск скрипта нормализации `normalized_phone.py`, который заполнит созданную
в предыдущем шаге колонку нормализованными телефонными номерами.

```
python3 normalized_phone.py
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
