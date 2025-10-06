from django.apps import AppConfig

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        # 앱 로드 시 signals.py 자동 실행
        from . import signals
