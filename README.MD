Deploy status:

[![Deploy](https://github.com/jmblx/rksi2025/actions/workflows/deploy.yml/badge.svg)](https://github.com/jmblx/rksi2025/actions/workflows/deploy.yml)

# Кейс "Лучшее мобильное приложение" Международный онлайн Хакатон IT-Tech 2025

---

# Деплой

## Сконфигурируйте по шаблонам кофиги в проекте:

https://github.com/jmblx/rksi2025/blob/main/.env.template

https://github.com/jmblx/rksi2025/blob/main/backend/config/config.template.toml

## Первый деплой (с миграцией БД):

```
docker compose --profile migrate up
```

## Последующие деплои:

```
docker compose up -d
```

---
# Разработка

## Установка зависимостей 

### uv:
```shell
pip install uv
```

### Рабочие зависимости:

#### Windows:
```shell
cd backend
uv venv .venv
.venv\Scripts\activate
uv pip install -e .
```

#### Linux/macOS:
```shell
cd backend
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```

### Для разработки backend:
```shell
uv pip install -e ".[dev]"
```

---

## Запуск для локальной разработки

В корне проекта можно использовать:

```bash
make run
```

Эта команда запускает Gunicorn с `uvicorn.workers.UvicornWorker` и считывает параметры из конфигурационного файла (`config.toml`).  
Используется `main:app` из FastAPI.

> ⚠️ Для Windows вместо `make` можно запускать эквивалентную команду вручную:
> ```bash
> uvicorn main:app --reload
> ```

---

## ERD (Entity Relationship Diagram)

![erd.png](readme_assets/erd.png)

---
