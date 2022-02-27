# python-app

## 環境変数設定

```bash
# 下記または.envにて設定
export SECRET_KEY=secretkey
export DJANGO_SETTINGS_MODULE=config.settings.local
```

## Python環境構築

```bash
pip install pipenv
pipenv shell
pipenv sync
```

## Django(DRF)

### プロジェクト構築

```bash
django-admin startproject config .
python manage.py startapp account
python manage.py startapp apiv1
python manage.py startapp bmonster
```

### DB起動

```bash
docker-compose --file docker-compose-db-only.yml up --build
```

### DB初期化

```bash
python manage.py makemigrations account
python manage.py makemigrations bmonster
python manage.py migrate
```

### 管理サイトユーザー作成

```bash
python manage.py createsuperuser
```

### ホストマシン

```bash
python manage.py runserver
```

### docker

```bash
docker-compose up --build
```