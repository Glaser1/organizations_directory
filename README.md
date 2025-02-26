# directory-of-organizations
REST API application for the directory of Organizations, Buildings and Activities

## Cтек технологий:
  Python 3.12, pydantic 2.10.6, sqlalchemy 2.0.38, alembic 1.14.1, uvicorn 0.34.0

## Установка:
* Клонируйте репозиторий себе на компьютер:
  ``` git clone git@github.com:Glaser1/backend_test_homework.git ```

* Установите docker и docker-compose согласно официальной инструкции (в зависимости от операционной системы сервера):
    https://docs.docker.com/engine/install/    
    https://docs.docker.com/compose/install/

* В корневой папке проекта создайте файл .env.docker - в нем укажите переменные окружающей среды согласно шаблону .env.template;

* Создайте docker-compose.yml на основе docker-compose.template.yml и укажите в нем переменные окружения согласно ранее созданному .env

* Запустите приложения в контейнерах: 
  ``` docker-compose up -d --build ```
  
* Выполните миграцию в контейнерах: 
  ``` docker compose exec web poetry run alembic upgrade head  ```

* Загрузите тестовые данные: 
  ``` docker compose exec web python3 fastapi_application/load_data.py ```


## Использование:
API предоставляет несколько эндопинтов для взаимодействия с организациями, зданиями и видами деятельностями. Доступ к эндпоинтам предоставляется через API_KEY, который вы можете самостоятельно сгенерировать, записать в .env и использовать в заголовках с ключем "X-API-Key":

#### 1. Cписок всех организаций, находящихся в конкретном здании
    URL: /api/building/{building_id}/organizations
    Метод: GET
    
    Тело ответа:
    
    [
      {
        "title": "ООО «Рога и Копыта»",
        "building_id": 1
      }
    ]
    
#### 2. Список всех организаций, относящихся к указанному виду деятельности
    URL: /api/activities/organizations/{activity_id}
    Метод: GET
    
    Тело ответа:
    
    [
      {
        "title": "АвтоГруз Сервис",
        "building_id": 2
      }
    ]

#### 3. Список организаций, находящихся в заданном радиусе/прямоугольной области относительно указанной точки на карте
    URL: /api/organizations_by_area?center_lat=&center_lon=&delta_km=
    Метод: GET
    
    Тело ответа:
    
    [
      {
          "title": "ООО «Рога и Копыта»",
          "id": 1,
          "building_id": 1
      },
      {
          "title": "АвтоГруз Сервис",
          "id": 2,
          "building_id": 2
      },
      {
          "title": "АвтоЛюкс",
          "id": 3,
          "building_id": 2
      }
    ]

#### 4. Список зданий, находящихся в заданном радиусе/прямоугольной области относительно указанной точки на карте
    URL: /api/buildings_by_area?center_lat=&center_lon=&delta_km=
    Метод: GET
    
    Тело ответа:
    
    [
      {
          "longitude": 37.618423,
          "address": "г. Москва, ул. Блюхера, 32/1",
          "id": 1,
          "latitude": 55.751244
      },
      {
          "longitude": 37.621856,
          "address": "г. Москва, ул. Ленина 1, офис 3",
          "id": 2,
          "latitude": 55.753605
      }
    ]

#### 5. Вывод информации об организации по её идентификатору
    URL: /api/organizations/{organization_id}
    Метод: GET
    
    Тело ответа:
    
    {
        "title": "ООО «Рога и Копыта»",
        "id": 1,
        "building_id": 1
    }

#### 6. Поиск организаций по ввиду деятельности, включая вложенные (уровень вложенности видов деятельности ограничен 3 уровнями)
    URL: /api/activities/{activity_title}/organizations
    Метод: GET
    
    Тело ответа:
    
    [
      {
        "title": "АвтоГруз Сервис",
        "id": 2,
        "building_id": 2
      },
      {
        "title": "АвтоЛюкс",
        "id": 3,
        "building_id": 2
      }
    ]

#### 7. поиск организации по названию
     URL: /api/organizations/{organization_title}
     Метод: GET
    
     Тело ответа:
    
     [
      {
        "title": "АвтоГруз Сервис",
        "building_id": 2
      },
      {
        "title": "АвтоЛюкс",
        "building_id": 2
      }
    ]
### Документация доступна по адресу: 
  ``` http://127.0.0.1:8000/docs#/ ```
