# Unit Тести CinemaHub Проєкту

## Огляд

Цей проєкт включає комплексну систему unit тестів для Django backend з використанням **pytest** та **pytest-django**.

## Структура тестів

Тести організовані в наступних файлах:

### 1. **test_models.py** - Тести моделей (18 тестів)
Тестування бізнес-логіки Django моделей:

- **TestUserModel** (4 тести)
  - `test_create_user` - Створення нового користувача
  - `test_user_email_unique` - Перевірка унікальності email
  - `test_user_str_representation` - String представлення користувача
  - `test_user_password_hashing` - Хешування паролів

- **TestGenreModel** (2 тести)
  - `test_create_genre` - Створення жанру
  - `test_genre_unique_name` - Унікальність назви жанру

- **TestMovieModel** (4 тести)
  - `test_create_movie` - Створення фільму
  - `test_movie_with_genres` - Фільм з жанрами
  - `test_movie_string_representation` - String представлення
  - `test_movie_now_showing_filter` - Фільтрування за статусом

- **TestHallModel** (5 тестів)
  - `test_create_hall` - Створення залу
  - `test_hall_auto_creates_seats` - Автогенерація місць
  - `test_hall_vip_seats_last_row` - VIP місця в останньому ряду
  - `test_hall_standard_seats_not_vip` - Звичайні місця не VIP
  - `test_seat_unique_constraint` - Унікальність комбінації місць

- **TestSessionModel** (2 тести)
  - `test_create_session` - Створення сеансу
  - `test_session_end_time_calculation` - Розрахунок часу закінчення
  - `test_session_string_representation` - String представлення

- **TestBookingModel** (5 тестів)
  - `test_create_booking` - Створення бронювання
  - `test_booking_status_choices` - Валідні статуси
  - `test_booking_unique_session_seat` - Запобігання двійному бронюванню
  - `test_booking_has_uuid_id` - UUID як ID
  - `test_booking_string_representation` - String представлення

### 2. **test_serializers.py** - Тести серіалізаторів (13 тестів)
Тестування Django REST Framework серіалізаторів:

- **TestUserSerializer** (2 тести)
- **TestUserRegisterSerializer** (3 тести)
- **TestGenreSerializer** (2 тести)
- **TestMovieSerializer** (4 тести)
- **TestSessionSerializer** (3 тести)
- **TestBookingSerializer** (1 тест)

### 3. **test_views.py** - Тести API views (26 тестів)
Тестування всіх API endpoints:

- **TestUserRegisterView** (3 тести)
- **TestUserProfileView** (3 тести)
- **TestGenreViewSet** (3 тести)
- **TestMovieViewSet** (6 тестів)
- **TestHallViewSet** (2 тести)
- **TestSessionViewSet** (2 тести)
- **TestBookingViewSet** (7 тестів)

### 4. **test_integration.py** - Інтеграційні тести (7 тестів)
Комплексні сценарії з використанням кількох компонентів:

- **TestCinemaBookingFlow** (4 тести)
  - `test_complete_booking_workflow` - Повний цикл бронювання
  - `test_multiple_users_different_seats` - Кілька користувачів
  - `test_session_has_available_and_booked_seats` - Доступні/забронь ані місця
  - `test_user_can_cancel_booking` - Скасування бронювання

- **TestGenreMovieRelationship** (3 тести)
  - Відносини між жанрами та фільмами

- **TestDataValidation** (3 тести)
  - Валідація даних у моделях

## Всього: 69+ unit тестів

## Встановлення

### Крок 1: Встановлення залежностей

```bash
cd backend
pip install -r requirements.txt
```

Або встановіть тільки тестові пакети:

```bash
pip install pytest==7.4.3 pytest-django==4.7.0 pytest-cov==4.1.0
```

### Крок 2: Налаштування Django

Переконайтесь, що у вас є `config/settings.py` з правильним `INSTALLED_APPS`.

## Запуск тестів

### Запустити ВСІ тести:
```bash
pytest tests/ -v
```

### Запустити тести з покриттям коду:
```bash
pytest tests/ --cov=api --cov-report=html
```

### Запустити специфічний файл тестів:
```bash
pytest tests/test_models.py -v
```

### Запустити специфічний клас тестів:
```bash
pytest tests/test_models.py::TestUserModel -v
```

### Запустити специфічний тест:
```bash
pytest tests/test_models.py::TestUserModel::test_create_user -v
```

### Запустити з більш детальною інформацією:
```bash
pytest tests/ -vv --tb=long
```

### Запустити паралельно (якщо встановлено pytest-xdist):
```bash
pip install pytest-xdist
pytest tests/ -n auto
```

## Конфігураційні файли

### `pytest.ini`
Налаштування для pytest:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_tests.py
addopts = --verbose --cov=api
testpaths = tests
```

### `conftest.py`
Фіксчури для використання в тестах:
- `api_client` - API клієнт
- `authenticated_user` - Тестовий користувач
- `authenticated_client` - Авторизований API клієнт
- `movie`, `genre`, `hall`, `session`, `booking` - Тестові об'єкти

## Приклади використання

### Тест моделі:
```python
@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='pass123'
        )
        assert user.email == 'test@example.com'
```

### Тест API view:
```python
@pytest.mark.django_db
class TestMovieViewSet:
    def test_list_movies(self, api_client, movie):
        response = api_client.get('/api/movies/')
        assert response.status_code == status.HTTP_200_OK
```

### Інтеграційний тест:
```python
def test_complete_booking_workflow(self, authenticated_client, movie, hall):
    # 1. Get movies
    # 2. View sessions
    # 3. Book seat
    # 4. Verify booking
```

## Покриття коду

Після запуску `pytest --cov=api --cov-report=html` буде створено:
- `htmlcov/index.html` - HTML звіт про покриття
- Вбудований звіт в консоль

## Корисні команди

```bash
# Запустити тести, що пройшли останній раз
pytest --lf

# Запустити тести, що не пройшли
pytest --ff

# Зупинити після першого failsafe
pytest -x

# Зупинити після 3-х помилок
pytest --maxfail=3

# Показати повній вивід принтів (не приховувати)
pytest -s

# Виділити певні тести по ключовому слову
pytest -k "booking" -v

# Запустити з поточною базою даних (прискорює тести)
pytest --reuse-db
```

## Поточне покриття тестів

- ✅ User моделі та аутентифікація
- ✅ Genre моделі та фільтрування
- ✅ Movie CRUD операції та фільтрування
- ✅ Hall та Seat автогенерація
- ✅ Session управління та розрахунки
- ✅ Booking логіка та запобігання double-booking
- ✅ API endpoints авторизація
- ✅ Інтеграційні сценарії
- ✅ Валідація даних

## Що тестується

### Моделі:
- ✓ Створення об'єктів
- ✓ Валідація унікальності
- ✓ Отримання та фільтрування
- ✓ Відносини між моделями
- ✓ Auto-generated поля

### Serializers:
- ✓ Серіалізація даних
- ✓ Десеріалізація та валідація
- ✓ Пов'язані поля
- ✓ Custom методи

### API Views:
- ✓ GET запити (list, retrieve)
- ✓ POST запити (create)
- ✓ PATCH запити (update)
- ✓ DELETE запити (destroy)
- ✓ Custom actions
- ✓ Авторизація та дозволи
- ✓ Фільтрування та пошук

### Business Logic:
- ✓ Попередження double-booking
- ✓ Автогенерація місць в залі
- ✓ VIP/Standard розрізнення
- ✓ Booking статуси
- ✓ UUID для bilety

## Розширення тестів

Для додавання нових тестів:

1. Створіть новий тестовий файл або додайте до існуючого
2. Використовуйте фіксчури з `conftest.py`
3. Декоруйте класи з `@pytest.mark.django_db`
4. Запустіть `pytest --collect-only` для перевірки

## Проблеми та вирішення

### "ModuleNotFoundError: No module named 'django'"
```bash
pip install Django
```

### "No database detected"
```bash
pytest --create-db
```

### Тесты повільні
```bash
pytest --reuse-db  # Переиспользовать БД
pytest -n auto      # Запустити паралельно
```

## Корисні посилання

- [pytest документація](https://docs.pytest.org/)
- [pytest-django документація](https://pytest-django.readthedocs.io/)
- [Django тестування](https://docs.djangoproject.com/en/5.2/topics/testing/)
- [DRF тестування](https://www.django-rest-framework.org/api-guide/testing/)

## Контроль якості

Рекомендовані мінімальні стандарти:
- ✓ 80% код покриття
- ✓ Всі моделі протестовані
- ✓ Всі API endpoints протестовані
- ✓ Критична бізнес-логіка протестована
- ✓ Помилки та edge cases покриті

## Ліцензія

Цей проєкт є частиною CinemaHub 🎬
