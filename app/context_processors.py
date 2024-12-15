from .models import Category
from django.core.cache import cache

def categories(request):
    categories = cache.get('categories')
    if categories is None:
        categories = Category.objects.all()
        cache.set('categories', categories, 60 * 15)  # Кэшируем на 15 минут
    return {
        'categories': categories
    }
