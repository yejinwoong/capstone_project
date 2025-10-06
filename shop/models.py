from django.db import models
from django.contrib.auth.models import User

# -------------------------------
# 기본 카테고리 / 제품
# -------------------------------
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    co2_saving_g = models.IntegerField(default=0)   # 1개당 절감량(g)
    is_recycled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# -------------------------------
# 사용자별 누적 절감 데이터
# -------------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_saving_g = models.IntegerField(default=0)  # 누적 절감량(g)

    def __str__(self):
        return f"{self.user.username} 프로필"


# -------------------------------
# 결제(또는 절감) 기록 로그
# -------------------------------
class SavingLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saving_g = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.saving_g}g ({self.created_at.date()})"
