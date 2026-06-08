# DevSpace
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-5-green)
![DRF](https://img.shields.io/badge/DRF-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue)
![Docker](https://img.shields.io/badge/Docker-blue)
![Status](https://img.shields.io/badge/Status-Active-success)

> Социальная платформа для разработчиков, построенная на Django, Django REST Framework, PostgreSQL и React.

[🌐 Демонстрация проекта](https://in-devspace.ru) • [📦 Репозиторий GitHub](https://github.com/mrDisa/Devspace)

---

## 🎬 Демонстрация 

![Demo](docs/demo.gif)
---

## 📖 О проекте

DevSpace — социальная платформа для разработчиков, предназначенная для публикации контента, общения и обмена опытом между участниками сообщества.

Проект разрабатывается командой из двух разработчиков и представляет собой полноценное веб-приложение с frontend, backend и production-инфраструктурой.

---

## ✨ Возможности платформы

### Пользователи

* Регистрация и авторизация
* Управление профилем пользователя
* Система ролей и прав доступа

### Социальные функции

* Создание и публикация постов
* Взаимодействие пользователей с контентом
* Лента публикаций
* Просмотр профилей пользователей

### Администрирование

* Административная панель Django
* Управление пользователями и контентом
* Модерация данных

### Инфраструктура

* Docker-окружение для разработки
* Развёртывание на VPS-сервере
* Reverse Proxy через Nginx
* Gunicorn в качестве WSGI-сервера

---

## 🛠 Технологический стек

### Backend

* Python
* Django
* Django REST Framework
* PostgreSQL

### Frontend

* React
* JavaScript
* HTML5
* CSS3

### Инфраструктура

* Docker
* Docker Compose
* Nginx
* Gunicorn
* Linux VPS

### Инструменты разработки

* Git
* GitHub

---

## 🏗 Архитектура проекта

```text
Frontend (React)
        │
        ▼
Django REST API
        │
        ▼
PostgreSQL

Docker → Gunicorn → Nginx → VPS
```

Проект построен по клиент-серверной архитектуре, где frontend взаимодействует с backend через REST API.

---

## 📂 Структура проекта

```text
DevSpace/
├── docker/nginx
│   ├── defa
│   ├── config/
│   ├── requirements/
│   └── manage.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── nginx/
├── docker-compose.yml
└── README.md
```

---

## 🚀 Локальный запуск

### ⚙️ Настройка переменных окружения.

Перед запуском проекта необходимо создать файл `.env` в корневой директории проекта.

Скопируйте содержимое из `.env.example`:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DATABASE_URL=postgresql://postgres:password@db:5432/devspace

ALLOWED_HOSTS=localhost,127.0.0.1
```

### Генерация SECRET_KEY

Для генерации безопасного ключа Django выполните команду:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Полученный ключ вставьте в переменную:

```env
SECRET_KEY=generated-secret-key
```

### Пример для dev

```env
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://user:password@host:5432/database_name
```

### Клонирование репозитория

```bash
git clone https://github.com/mrDisa/Devspace.git
cd Devspace
```

### Запуск через Docker

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```text
http://localhost или http://localhost:8000
```

---

## 🔌 API

Backend предоставляет REST API для взаимодействия клиентской части приложения с сервером.

Основные возможности API:

* Аутентификация пользователей
* Управление профилями
* Работа с публикациями
* Система прав доступа

---

## ⚡ Технические задачи проекта

В процессе разработки были реализованы:

* Проектирование архитектуры REST API
* Реализация аутентификации и авторизации пользователей
* Проектирование структуры базы данных PostgreSQL
* Контейнеризация приложения с использованием Docker
* Настройка production-окружения на Linux VPS
* Настройка Nginx в качестве Reverse Proxy
* Развёртывание приложения через Gunicorn
* Организация командной разработки с использованием Git

---

## 🗺 Планы развития

* [ ] Система уведомлений в реальном времени
* [ ] Личные сообщения
* [ ] Расширенный поиск
* [ ] Рекомендации контента
* [ ] Документация API
* [ ] Автоматизированное тестирование
* [ ] CI/CD pipeline

---

## 👥 Команда

### Даниил Исавердов

Backend Developer

* Проектирование backend-архитектуры
* Разработка REST API
* Работа с PostgreSQL
* Контейнеризация приложения
* Развёртывание проекта на VPS

### Богдан Максименко

Frontend Developer



* Разработка клиентской части на JS
* Пользовательский интерфейс
* Интеграция с backend API

---

## 📈 Цели проекта

Основная цель DevSpace — создание платформы для взаимодействия разработчиков и обмена знаниями, а также применение современных подходов к разработке веб-приложений в условиях, максимально приближенных к коммерческой разработке.

---

## 📬 Контакты

### Даниил Исавердов

GitHub: [клик](https://github.com/mrDisa)

Telegram: [@disawithgod](https://t.me/disawithgod)

Email: [daniil.isaverdov@gmail.com](mailto:daniil.isaverdov@gmail.com)

### Богдан Максименко

GitHub: [клик](https://github.com/Pantihen)

Telegram: [@Pantihen](https://t.me/Pantihen)

Email: [bogdanmaksimenko51@gmail.com](mailto:bogdanmaksimenko51@gmail.com)
