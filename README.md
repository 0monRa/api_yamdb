### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/0monRa/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение.

Windows:
```
python -m venv env
```

```
source env/bin/activate
```

Linux:
```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt.

Windows:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Linux:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции.

Windows:
```
python manage.py migrate
```

Linux:
```
python3 manage.py migrate
```

Запустить проект.

Windows:

```
python manage.py runserver
```

Linux:

```
python3 manage.py runserver
```