# Запуск

<ol>
<li> Создать виртуальное окружение

        python3 -m venv venv

<li> Активировать виртуально окружение

        source venv/bin/activate

<li> Установить зависимости

        pip install -r req.txt

<li> Создать .env файл с конфигурацией БД с прфиксом "POSTGRESQL_". Например:

        POSTGRESQL_DSN = "postgresql+asyncpg://postgres:postgres@localhost:5432/parser"

<li> Запустить скрипт

        python3 -m main
