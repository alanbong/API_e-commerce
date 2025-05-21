`Python` `Django` `Django Rest Framework`

# E-commerce API

Простое backend-приложение интернет-магазина продуктов питания на Django + DRF.

## Описание

REST API для интернет-магазина продуктов питания.  
Позволяет управлять товарами, категориями и корзиной покупателя.  
Поддерживает авторизацию по токену, пагинацию, документацию через Swagger.

### Основные возможности

- Категории и подкатегории с изображениями
- Продукты с ценами и изображениями в 3-х размерах
- Публичный просмотр каталога
- Корзина пользователя:
  - добавление товара
  - изменение количества
  - удаление товара
  - очистка всей корзины
- Авторизация через токены
- Swagger-документация
- Поддержка фикстур
- Пагинация в списках

## Установка
1. Клонируйте репозиторий и создайте `.env` по примеру:
    ```
    git clone https://github.com/alanbong/API_e-commerce.git
    cd api_e-commerce
    ```

    ```
    project/
    │── .env
    ```

2. Пример `.env.example`:
    ```
    SECRET_KEY=django-insecure-key
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    ```

3. Установите зависимости и запустите проект:
    ### Linux/MacOS
    ```
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt

    python3 manage.py migrate
    python3 manage.py createsuperuser
    python3 manage.py runserver
    ```
    ### Windows
    ```
    cd backend
    python -m venv venv
    . venv/Scripts/activate
    pip install -r requirements.txt

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    ```

4. (Опционально) Загрузите фикстуры:
    ### Linux/MacOS
    ```
    python3 manage.py import_csv
    ```
    ### Windows
    ```
    python manage.py import_csv
    ```

5. (Опционально) После запуска сервера полная версия документации API будет доступна по адресу:
  [http://127.0.0.1:8000/api/v1/redoc/](http://127.0.0.1:8000/api/v1/redoc/)
  [http://127.0.0.1:8000/api/v1/swagger/](http://127.0.0.1:8000/api/v1/swagger/)



### Авторизация:
Для авторизированных запросов используйте токен:
```
key: Authorization
value: Token <ваш_токен>
```
Получение токена:
```
POST api/v1/api-token-auth/
{
  "username": "your_username",
  "password": "your_password"
}
```

### Примеры запросов
| Метод    | URL                    | Описание                          |
| -------- | ---------------------- | --------------------------------- |
| `GET`    | `/api/v1/products/`    | Список продуктов с пагинацией     |
| `GET`    | `/api/v1/categories/`  | Список категорий с подкатегориями |
| `GET`    | `/api/v1/cart/`        | Просмотр корзины                  |
| `POST`   | `/api/v1/cart/add/`    | Добавить товар в корзину          |
| `PATCH`  | `/api/v1/cart/update/` | Изменить количество товара        |
| `DELETE` | `/api/v1/cart/remove/` | Удалить товар из корзины          |
| `DELETE` | `/api/v1/cart/clear/`  | Очистить всю корзину              |


## Авторы
Backend:
- [alanbong](https://github.com/alanbong)
