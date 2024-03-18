# Спортивный гид

**Спортивный гид** - это веб-сервис, который обеспечивает удобный поиск спортивных площадок в различных регионах. Пользователи могут находить площадки для футбола, баскетбола, тенниса, волейбола и многих других видов спорта.

Одной из основных функций **Спортивного гида** является возможность добавления новых спортивных площадок пользователями. Это создает динамично обновляемую базу данных площадок, где каждый может внести свой вклад. Помимо поиска и добавления площадок, пользователи могут договариваться о встречах, создавая собственные события или присоединяясь к уже существующим.

С помощью **Спортивного гида**, мы стремимся создать сообщество единомышленников, где каждый сможет найти идеальное место для занятий любимым видом спорта, встретить новых друзей и принять участие в спортивных событиях.

## Технологический стек

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django%20Rest%20Framework-009688?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%2337814a.svg?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Pillow](https://img.shields.io/badge/pillow-%23751816.svg?style=for-the-badge&logo=python&logoColor=white)

## Начало работы

Эти инструкции позволят вам запустить копию проекта на вашем локальном компьютере для разработки и тестирования.

<details>
<summary><strong>Запуск с использованием Docker</strong></summary>

### Предварительные требования

Убедитесь, что у вас установлены Docker и Docker Compose. Это можно сделать, следуя официальной документации Docker: https://docs.docker.com/get-docker/ и https://docs.docker.com/compose/install/

### Установка и запуск

1. Клонируйте репозиторий на компьютер:
   ```
   git clone git@github.com:Sports-Guide/Sports-Guide-Backend.git
   ```
2. Перейдите в папку infra:
   ```
   cd Sports-Guide-Backend/infra/
   ```

3. Запустите проект с помощью Docker Compose:
   ```
   docker compose -f docker-compose.local.yml up
   ```

   Теперь приложение должно быть доступно по адресу:

   http://localhost:8000
   
   А документация доступна по адресу:
   
   http://localhost:8000/api/schema/swagger-ui/

</details>
