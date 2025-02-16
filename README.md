# directory-of-organizations
REST API application for the directory of Organizations, Buildings and Activities

## стек технологий:
  Python 3.12, pydantic 2.10.6, sqlalchemy 2.0.38, alembic 1.14.1, uvicorn 0.34.0

## Установка:
* Клонируйте репозиторий себе на компьютер:
  ``` git clone git@github.com:Glaser1/backend_test_homework.git ```

* Установите docker и docker-compose согласно официальной инструкции (в зависимости от операционной системы сервера):
    https://docs.docker.com/engine/install/    
    https://docs.docker.com/compose/install/

* В корневой папке проекта создайте файл .env - в нем укажите переменные окружающей среды согласно шаблону .env.template;

* Создайте docker-compose.yml на основе docker-compose.template.yml и укажите в нем переменные окружения согласно ранее созданному .env

* Запустите приложения в контейнерах: 
  ``` docker-compose up -d --build ```
  
* Выполните миграцию в контейнерах: 
  ``` docker compose exec  web poetry run alembic upgrade head  ```

* Загрузите тестовые данные: 
  ``` docker compose exec  web python3 fastapi_application/load_data.py ```
