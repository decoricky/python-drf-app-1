# drf-app

## Django(DRF)プロジェクト構築手順

```bash
django-admin startproject config .
python manage.py startapp account
python manage.py startapp apiv1
python manage.py startapp bmonster
```

## 環境変数の設定

### ホストマシン上でローカル実行時

```bash
# 下記または.envにて設定
export SECRET_KEY=???
export DJANGO_SETTINGS_MODULE=config.settings.local
```