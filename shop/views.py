from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.db.models import Sum
from .models import Product, Category
import json
from django.http import HttpResponse


# 홈
def home(request):
    users = 123
    saving_g = 125000
    return render(request, 'shop/home.html', {
        'users': users,
        'saving_kg': f"{saving_g/1000:.2f}",
    })

# 대시보드
def dashboard(request):
    by_cat = (Product.objects
              .values('category__name')
              .annotate(total=Sum('co2_saving_g'))
              .order_by('category__name'))
    labels = [r['category__name'] for r in by_cat]
    values = [r['total'] or 0 for r in by_cat]
    metrics = {
        'product_count': Product.objects.count(),
        'category_count': Category.objects.count(),
        'total_saving_g': Product.objects.aggregate(s=Sum('co2_saving_g'))['s'] or 0,
    }
    return render(request, 'shop/dashboard.html', {
        'labels_json': json.dumps(labels, ensure_ascii=False),
        'values_json': json.dumps(values),
        'metrics': metrics,
    })

# 제품 목록
def product_list(request):
    q = request.GET.get('q', '')
    cat = request.GET.get('cat', '')
    qs = Product.objects.all()
    if cat:
        qs = qs.filter(category__name=cat)
    if q:
        qs = qs.filter(name__icontains=q)
    cats = Category.objects.all()
    return render(request, 'shop/products.html', {
        'products': qs, 'cats': cats, 'q': q, 'cat': cat
    })

# 장바구니 담기
def add_to_cart(request):
    if request.method == 'POST':
        pid = str(request.POST['pid'])
        qty = int(request.POST.get('qty', 1))
        cart = request.session.get('cart', {})
        cart[pid] = cart.get(pid, 0) + qty
        request.session['cart'] = cart
    return redirect('cart')

# 장바구니 보기
def cart(request):
    cart = request.session.get('cart', {})
    items, total_price, total_saving = [], 0, 0
    for pid, qty in cart.items():
        p = get_object_or_404(Product, id=int(pid))
        items.append({
            'p': p, 'qty': qty,
            'line_price': p.price * qty,
            'line_saving': p.co2_saving_g * qty
        })
        total_price += p.price * qty
        total_saving += p.co2_saving_g * qty
    return render(request, 'shop/cart.html', {
        'items': items, 'total_price': total_price, 'total_saving': total_saving
    })
 
# 성과 알림 & 인사이트
def home(request):
    m = {
        'product_count': Product.objects.count(),
        'category_count': Category.objects.count(),
        'total_saving_kg': round((Product.objects.aggregate(s=Sum('co2_saving_g'))['s'] or 0)/1000, 2),
    }
    insights = {
        "weekly": {
            "title": "이번 주 성과",
            "icon": "🌱",
            "headline": f"{m['total_saving_kg']}kg CO₂ 절감!",  # 예: 누적 기준으로 보여줌
            "desc": "지난주 대비 친환경 선택이 증가했습니다. 작은 선택이 모여 큰 변화를 만듭니다.",
        },
        "monthly": {
            "title": "월간 리포트",
            "icon": "📊",
            "headline": "목표 달성률 112%",
            "desc": "이달 누적 절감량이 개인 목표를 초과했습니다. 재활용 소재 제품의 비중이 높았습니다.",
        },
        "tips": [
            "업사이클링 트렌드: 재활용 플라스틱 소재 신발이 인기입니다.",
            "계절별 추천: 난방비 절약과 탄소 절감을 동시에 하는 방법.",
            "지역 소식: 제로웨이스트 매장에서 신제품이 출시되었습니다."
        ],
    }
    return render(request, 'shop/home.html', {'m': m, 'insights': insights})
