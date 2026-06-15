**Автор: [Гусельников Денис](https://github.com/DenisLearning2)**
**Техно-стек: Python 3.10.6, Django 5.2.4, PostgreSQL, SQLite3(для теста), Docker(Desktop обязательно)**

# Первоначальная настройка проекта TeamFinder
## 1. Клонирование репозитория с GitHub
Для клонирования репозитория необходимо выполнить команду из той папки, куда нужно склонировать:
```bash
git clone https://github.com/DenisLearning2/tedt
```
И перейдите в склонированную папку:
```bash
cd tedt
```

## 2. Виртуальное окружение

Далее необходимо создать и активировать виртуальное окружение Python.  

1. **Создайте виртуальное окружение (в папке проекта):**
   -**Windows:**
   ```bash
   python -m venv venv
   ```
   -**Linux:**
   ```bash
   python3 -m venv venv
   ```
   После этого появится папка `venv`, где будут храниться зависимости проекта.

2. **Активируйте окружение:**

    - **Windows (PowerShell):**
      ```bash
      venv\Scripts\Activate.ps1
      ```
    - **Windows (cmd):**
      ```bash
      venv\Scripts\activate
      ```
    - **Linux/Mac:**
      ```bash
      source venv/bin/activate
      ```

3. **Установите зависимости из `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```

   После установки в окружении будут доступны все нужные библиотеки Django-проекта.

## 2. Создание `.env`

Файл `.env` содержит конфиденциальные настройки проекта — ключ Django, параметры БД и другие переменные.  

Особое внимание обратите на строчку `TASK_VERSION=`. Ему необходимо задать `1`
В репозитории есть пример `.env_example`, который нужно скопировать и заполнить:

```bash
cp .env_example .env
```
Остальное менять не нужно.

## 3. Запуск контейнера Docker

В проекте уже есть пример файла `docker-compose.yml`. 
Используйте готовый или измените под свои нужды, а дальше запускайте:

```bash
docker compose up -d
```

`-d` значит `detach`, то есть контейнер продолжит работать в фоне. Чтобы его остановить, надо будет ввести

```bash
docker compose down
```

---

## 4. Запуск Django

После заполнения `.env` и настройки базы данных можно запустить сервер разработки:

```bash
python manage.py runserver
```

Теперь проект доступен по адресу [http://localhost:8000](http://localhost:8000). 

Страница администратора доступна по адресу [http://localhost:8000/admin](http://localhost:8000/admin).


