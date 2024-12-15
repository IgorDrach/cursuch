"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    image = models.FileField(default='temp.jpg', verbose_name="Путь к картинке")
    
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])
        
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "статьи блога"

admin.site.register(Blog)

class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Дата добавления комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    post = models.ForeignKey('Blog', on_delete=models.CASCADE, verbose_name="Статья комментария")
    
    def __str__(self):
        return f'Комментарий {self.id} {self.author} к {self.post}'
    
    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарий к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"
        
    #def set_default_post(self):
        #default_post = Blog.objects.first()
        #self.post = default_post
admin.site.register(Comment)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Tour(models.Model):
    image = models.ImageField(upload_to='tour_image/', null=True, blank=True)
    country = models.CharField(max_length=255)
    days = models.IntegerField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)  # Ссылка на категорию с null=True

    def __str__(self):
        return self.country
admin.site.register(Tour)
admin.site.register(Category) 

# models.py
from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    adult_count = models.PositiveIntegerField()
    child_count = models.PositiveIntegerField()
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    passport_exists = models.BooleanField(default=False)
    visa_exists = models.BooleanField(default=False)
    total_cost = models.FloatField(default=0)


     
   
class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='news/')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


admin.site.register(News)



