# 🚀 Швидкий посібник по запуску unit тестів

## Передумови
- Python 3.8+
- pip
- Git (для клонування репо)

---

## Крок 1️⃣: Клонування та навігація

```bash
git clone https://github.com/your-repo/CinemaHub_ComandProject.git
cd CinemaHub_ComandProject/backend
```

---

## Крок 2️⃣: Встановлення залежностей

### Опція A: Встановити ВСЕ з requirements.txt
```bash
pip install -r requirements.txt
```

### Опція B: Встановити тільки тестові залежності
```bash
pip install pytest==7.4.3 pytest-django==4.7.0 pytest-cov==4.1.0 factory-boy==3.3.0
```

### Опція C: Встановити в віртуальному середовищі (рекомендується)
```bash
# На Windows
python -m venv venv
venv\Scripts\activate

# На Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Потім встановити
pip install -r requirements.txt
```

---

## Крок 3️⃣: Запуск тестів

### Базовий запуск (ВСІ тести):
```bash
pytest tests/ -v
```

### З детальним виводом:
```bash
pytest tests/ -vv --tb=long
```

### Тільки тести моделей:
```bash
pytest tests/test_models.py -v
```

### Тільки API тести:
```bash
pytest tests/test_views.py -v
```

### З покриттям коду (HTML звіт):
```bash
pytest tests/ --cov=api --cov-report=html --cov-report=term
# Отримаєте: htmlcov/index.html
```

---

## Результати виконання

Успішна команда повинна показати щось таке:

```
============================= test session starts ==============================
collected 69 items

tests/test_models.py::TestUserModel::test_create_user PASSED                [ 1%]
tests/test_models.py::TestUserModel::test_user_email_unique PASSED          [ 2%]
tests/test_models.py::TestUserModel::test_user_str_representation PASSED    [ 3%]
tests/test_models.py::TestUserModel::test_user_password_hashing PASSED      [ 4%]
tests/test_models.py::TestGenreModel::test_create_genre PASSED              [ 5%]
...
========================== 69 passed in 2.34s ==================================
```

---

## Порядок навчання

### День 1: Основи
1. Запустити: `pytest tests/test_models.py::TestUserModel -v`
2. Прочитати вихід
3. Подивитися на код тесту
4. Розуміти, що тестується

### День 2: API Тести
1. Запустити: `pytest tests/test_views.py::TestMovieViewSet -v`
2. Подивитися, як тестуються API endpoints
3. Розуміти перевірку status codes

### День 3: Інтеграція
1. Запустити: `pytest tests/test_integration.py -v`
2. Подивитися комплексні сценарії
3. Розуміти workflow бронювання

---

## 🆘 Розв'язання проблем

### ❌ "pytest: command not found"
```bash
python -m pip install pytest
# Або
pip install pytest
```

### ❌ "ModuleNotFoundError: No module named 'django'"
```bash
pip install Django
# Або переустановити все
pip install -r requirements.txt
```

### ❌ "ERRORS django.core.exceptions.ImproperlyConfigured"
```bash
# Переконайтесь, що DJANGO_SETTINGS_MODULE встановлений
# Це робиться автоматично в pytest.ini
# Якщо ні, вручну:
export DJANGO_SETTINGS_MODULE=config.settings
# Потім запустити тести
```

### ❌ Тесты повільні
```bash
# Використовуйте кешування БД
pytest tests/ --reuse-db

# Або паралельне виконання
pip install pytest-xdist
pytest tests/ -n auto
```

### ❌ "database is locked" (SQLite)
```bash
# Перезапустіть тести
pytest tests/ --create-db

# Або видаліть старі БД
rm -f db.sqlite3 .pytest_cache
pytest tests/
```

---

## 📚 Корисні прапори pytest

| Флаг | Що робить | Приклад |
|------|-----------|---------|
| `-v` | Verbose (детальний вивід) | `pytest -v` |
| `-vv` | Дуже детальний | `pytest -vv` |
| `-s` | Показати print() | `pytest -s` |
| `-k` | Запустити по імені | `pytest -k "booking"` |
| `--tb=short` | Скорочений traceback | `pytest --tb=short` |
| `-x` | Зупинити на першій помилці | `pytest -x` |
| `--maxfail=3` | Зупинити після 3-х помилок | `pytest --maxfail=3` |
| `--lf` | Тільки то, що не прошли | `pytest --lf` |
| `--ff` | Спочатку невдалі | `pytest --ff` |
| `--collect-only` | Тільки показати тести | `pytest --collect-only` |

---

## 📖 Приклади команд

### Запустити один конкретний тест:
```bash
pytest tests/test_models.py::TestUserModel::test_create_user -v
```

### Запустити клас тестів:
```bash
pytest tests/test_models.py::TestUserModel -v
```

### Запустити весь файл:
```bash
pytest tests/test_models.py -v
```

### Запустити все з лог-виводом:
```bash
pytest tests/ -v -s
```

### Запустити з тайм-аутом (якщо тести зависають):
```bash
pytest tests/ --timeout=10
```

### Генерувати HTML звіт:
```bash
pytest tests/ --html=report.html --self-contained-html
```

---

## 🔄 Розробка: Додавання нових тестів

### Приклад 1: Добавити тест до існуючого класу

Файл: `tests/test_models.py`

```python
@pytest.mark.django_db
class TestUserModel:
    # ... існуючі тести ...
    
    # НОВИЙ ТЕСТ:
    def test_user_full_name(self):
        """Тест, що повне ім'я користувача утворюється правильно"""
        user = User.objects.create_user(
            email='john@example.com',
            username='john',
            password='pass123',
            first_name='John',
            last_name='Doe'
        )
        assert user.get_full_name() == 'John Doe'
```

### Приклад 2:創新новий тестовий клас

```python
@pytest.mark.django_db
class TestMovieRating:
    """Тести для рейтингу фільмів"""
    
    def test_average_rating(self, movie):
        """Розрахунок середнього рейтингу"""
        # Підготовка
        # ...
        
        # Дія
        avg = movie.get_average_rating()
        
        # Перевірка
        assert avg == 8.5
```

### Приклад 3: API тест

```python
@pytest.mark.django_db
class TestMovieRatingAPI:
    
    def test_get_movie_rating(self, api_client, movie):
        """API endpoint для отримання рейтингу"""
        response = api_client.get(f'/api/movies/{movie.id}/rating/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['rating'] == 8.5
```

### Як додати новий тест:

1. Відкрити потрібний файл в `tests/`
2. Додати метод до класу з префіксом `test_`
3. Додати docstring з описом тесту
4. Написати тест (AAA Pattern: Arrange → Act → Assert)
5. Запустити: `pytest tests/your_file.py::YourClass::test_your_test -v`

---

## ✨ Best Practices

### 1. Розміщення тестів
```
tests/
├── test_models.py        # Тести моделей
├── test_serializers.py   # Тести серіалізаторів
├── test_views.py         # Тести API views
├── test_integration.py   # Інтеграційні тести
└── __init__.py
```

### 2. Назви тестів
```python
def test_<component>_<scenario>_<expected_result>():
    pass

# Приклади:
def test_user_registration_success():
    pass

def test_movie_filtering_by_genre_returns_only_matching():
    pass

def test_booking_double_booking_prevention_raises_error():
    pass
```

### 3. Використання фіксчур
```python
# ✓ ХОРОШО
def test_create_movie(self, genre):
    movie = Movie.objects.create(...)
    movie.genres.add(genre)

# ✗ ПОГАНО (дублювання)
def test_create_movie(self):
    genre = Genre.objects.create(name='Action')
    movie = Movie.objects.create(...)
```

### 4. AAA Pattern (Arrange-Act-Assert)
```python
def test_complete_booking(self, authenticated_client, session, hall):
    # ARRANGE (Підготовка)
    seat = hall.seats.first()
    booking_data = {'session': session.id, 'seat': seat.id}
    
    # ACT (Дія)
    response = authenticated_client.post('/api/bookings/', booking_data)
    
    # ASSERT (Перевірка)
    assert response.status_code == status.HTTP_201_CREATED
    assert Booking.objects.filter(user=authenticated_client.user).exists()
```

### 5. Використання маркерів
```python
@pytest.mark.django_db
class TestUserModel:
    pass

@pytest.mark.slow
def test_heavy_operation():
    pass

# Запустити тільки slow тести
pytest tests/ -m slow
```

---

## 📊 Моніторинг якості

### Генерувати звіт про покриття:
```bash
pytest tests/ --cov=api --cov-report=html
# Результат: htmlcov/index.html
```

### Мета для проєкту:
- ✅ **Мінімум 80%** покриття коду
- ✅ **100%** покриття моделей
- ✅ **90%** покриття views
- ✅ **75%** покриття сервісів

---

## 🎓 Подальше навчання

1. **Pytest документація**: https://docs.pytest.org/
2. **Django тестування**: https://docs.djangoproject.com/en/5.2/topics/testing/
3. **DRF тестування**: https://www.django-rest-framework.org/api-guide/testing/
4. **TDD методологія**: Test-Driven Development

---

## ✅ Checklist перед комітом

- [ ] Запустив `pytest tests/ -v`
- [ ] Всі тести проходять
- [ ] Покриття не менше 80%
- [ ] Немає "TODO" коментарів у тестах
- [ ] Код слідує PEP 8
- [ ] Написав docstrings для тестів

---

## 🤝 Контрибьютинг

Якщо хочеш додати більше тестів:

1. Fork репо
2. Створи гілку: `git checkout -b feature/more-tests`
3. Добавь тести з хорошим покриттям
4. Запустіть: `pytest tests/ --cov=api`
5. Commit: `git commit -m "Add tests for <feature>"`
6. Push: `git push origin feature/more-tests`
7. Відкрий PR

---

**Готово! Твої тести чекають! 🚀**

Для питань чи проблем - див. TESTING.md або TESTS_SUMMARY.md
