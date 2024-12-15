"""Definition of views.
"""
from django.shortcuts import render
from datetime import datetime, timedelta
from django.http import HttpRequest
from .forms import AnketaForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .models import Blog, Comment  # использование моделей блога и комментариев
from .forms import BlogForm, CommentForm  # использование форм ввода блога и комментария
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tour
from .forms import TourForm
from .models import News


def home(request):
    """Renders the home page."""
    latest_news = News.objects.order_by('-published_date')[:3]  # Получаем последние 3 новости
    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная',
            'year': datetime.now().year,
            'latest_news': latest_news  # Передаем последние новости в контекст
        }
    )

def news_list(request):
    """Отображает список всех новостей."""
    news_items = News.objects.order_by('-published_date')  # Изменено с 'date' на 'published_date'
    return render(
        request,
        'app/news_list.html',
        {
            'all_news': news_items,  # Также нужно изменить 'news_items' на 'all_news', чтобы отслеживать правильный контекст в шаблоне
        }
    )


def news_detail(request, news_id):
    """Отображает детальную информацию о новости."""
    news_item = News.objects.get(id=news_id)
    return render(
        request,
        'app/news_detail.html',
        {
            'news_item': news_item,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Контакты',
            'message': 'Страница с нашими контактами.',
            'year': datetime.now().year,
        }
    )


def links(request):
    resources = [
        {
            'url': 'https://vk.com/otdykh_kruglyi_god',
            'img_src': 'app/content/vk_logo.jpg',
            'alt_text': 'Официальная страница ВКонтакте'
        },
        {
            'url': 'https://2gis.ru/pskov/firm/12666903233198851',
            'img_src': 'app/content/2gis_maps_logo.png',
            'alt_text': 'Местоположение Тур.агенства "Отдых круглый год"'
        },
        {
            'url': 'https://zoon.ru/pskov/hotels/turisticheskoe_agentstvo_otdyh_kruglyj_god/',
            'img_src': 'app/content/site_logo.jpg',
            'alt_text': 'Сайт с полезной информацией про агенство'
        },
    ]
    return render(request, 'app/links.html', {'resources': resources})

def anketa(request: HttpRequest):
    adults_range = list(range(1, 16))  # Список для выбора взрослых
    children_range = list(range(0, 16))  # Список для выбора детей    
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            # Если форма валидна, обработка данных отзыва
            return success_view(request, form)
    else:
        form = AnketaForm()
    return render(request, 'app/anketa.html', {
        'form': form,
        'adults_range': adults_range,
        'children_range': children_range,
    })

def success_view(request, form):
    """Render a success page."""
    return render(request, 'app/success.html', {'form': form})



from django.http import HttpResponse
from datetime import datetime, timedelta
from .models import Tour, Category  # Предполагается, что у Вас есть модель Category
from .forms import TourForm  # Если у Вас есть отдельная форма для категорий
from django.shortcuts import redirect
from django.contrib import messages  # Для отображения сообщений пользователю
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tour, Booking
from django.contrib.auth.decorators import login_required
from .models import Tour, Category


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    return render(request, 'app/tour_detail.html', {'tour': tour})

def new_tour(request):
    categories = Category.objects.all()  # Получение всех категорий
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)  # Не забывайте про request.FILES
        if form.is_valid():
            form.save()
            return redirect('tours')
    else:
        form = TourForm()
    return render(request, 'app/NewTour.html', {'form': form, 'categories': categories})

def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    categories = Category.objects.all()  # Получение всех категорий
    if request.method == "POST":
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('tour_detail', tour_id=tour.id)
    else:
        form = TourForm(instance=tour)
    return render(request, 'app/edit_tour.html', {'form': form, 'categories': categories})


def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    tour.delete()
    return redirect('tours')  # Изменено на 'tours'

from .forms import BookingForm
from django.shortcuts import get_object_or_404
from .models import Tour
from django.shortcuts import render, get_object_or_404
from .models import Category




def tours(request):
    categories = Category.objects.all()
    tours_by_category = {category: Tour.objects.filter(category=category) for category in categories}
    return render(request, 'app/tours.html', {'tours_by_category': tours_by_category})


def base_context(request):
    categories = Category.objects.all()
    return {
        'categories': categories,
    }

def tours_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    tours = Tour.objects.filter(category=category)
    return render(request, 'app/tours.html', {'tours_by_category': {category: tours}})

def all_tours(request):
    all_tours = Tour.objects.all()
    return render(request, 'app/tours.html', {'tours_by_category': {'Все туры': all_tours}})
      




@login_required
def add_to_cart(request, tour_id):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, pk=tour_id)
        request.session['cart'] = request.session.get('cart', [])
        if tour.id not in request.session['cart']:
            request.session['cart'].append(tour.id)
            request.session.modified = True
            messages.success(request, "Выбранный тур добавлен в корзину")
        return redirect('cart')
    return redirect('tours')  # Redirect if not a POST request


def add_to_cart_redirect(request, tour_id):
    if request.user.is_authenticated:
        return add_to_cart(request, tour_id)
    else:
        messages.error(request, "Для того, чтобы Вы могли приобрести тур необходимо зарегистрироваться или войти в аккаунт, если он уже есть.")
        return redirect('tours')  # или любое другое представление, на которое Вам нужно перенаправить


@login_required
def booking(request):
    if request.method == 'POST':
        adult_count = int(request.POST.get('adult_count', 1))
        child_count = int(request.POST.get('child_count', 0))
        tour_id = request.POST.get('tour_id')

        # Проверяем, есть ли tour_id
        if not tour_id:
            return redirect('cart')  # Перенаправить на корзину, если нет tour_id

        tour = get_object_or_404(Tour, id=tour_id)

        total_cost = (adult_count * tour.price) + (child_count * (tour.price / 2))

        form = BookingForm(request.POST)
        if form.is_valid():
            booking = Booking(
                user=request.user,
                tour=tour,
                adult_count=adult_count,
                child_count=child_count,
                total_cost=total_cost,
                full_name=form.cleaned_data['ФИО'],
                phone=form.cleaned_data['Номер телефона'],
                email=form.cleaned_data['Почта'],
                passport_exists=form.cleaned_data['Есть ли у Вас загран паспорт'],
                visa_exists=form.cleaned_data['Есть ли у Вас виза'],
            )
            booking.save()

            return render(request, 'app/success_tour.html')

    return render(request, 'app/booking.html', {'form': BookingForm(), 'tour_id': tour_id})



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tour

def cart(request):
    cart_ids = request.session.get('cart', [])
    cart_items = Tour.objects.filter(pk__in=cart_ids)
    total_price = sum(tour.price for tour in cart_items)
    return render(request, 'app/cart.html', {'cart': cart_items, 'total_price': total_price})

def korsina(request):
    cart_ids = request.session.get('cart', [])
    if cart_ids:  # Check if cart is not empty
        cart_items = Tour.objects.filter(pk__in=cart_ids)
        total_price = sum(tour.price for tour in cart_items)
    else:
        cart_items = []
        total_price = 0
    return render(request, 'app/korsina.html', {'cart': cart_items, 'total_price': total_price})

def remove_from_cart(request, tour_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        if tour_id in cart:
            cart.remove(tour_id)
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, "Тур удалён из корзины.")
        else:
            messages.error(request, "Тур не найден в корзине.")
    return redirect('cart')  # Переход к странице корзины после удаления


def success_tour(request):
    return render(request, 'app/success_tour.html')  # Страница успешной отправки


from .models import Booking  
def manager_orders(request):
    bookings = Booking.objects.all()  # Получение всех бронирований
    return render(request, 'app/manager_orders.html', {'bookings': bookings})


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()  # или любая другая логика удаления бронирования
    return redirect('manager_orders')  # Замените на нужный вам редирект


def registration(request):
    """Renders the registration page."""
    
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            regform.save()
            return redirect('home')  # Здесь 'home' - это имя URL для главной страницы
    else:
        regform = UserCreationForm()
    return render(request, 'app/registration.html', {'regform': regform})

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()  # запрос на выбор всех статей блога из модели
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,  # передача списка статей в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)  # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST":  # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user  # добавляем автора комментария
            comment_f.date = datetime.now()  # добавляем текущую дату
            comment_f.post = Blog.objects.get(id=parametr)  # добавляем статью, для которой данный комментарий
            comment_f.save()  # сохраняем комментарий
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm()  # создание формы для ввода комментария
    return render(request, 'app/blogpost.html', {
        'post_1': post_1,  # передача конкретной статьи в шаблон веб-страницы
        'comments': comments,  # передача комментариев в шаблон веб-страницы
        'form': form,  # передача формы в шаблон веб-страницы
        'year': datetime.now().year,
    }
    )

def newpost(request): 
    """Renders the new post page."""
    assert isinstance(request, HttpRequest)
    blogform = BlogForm()   # инициализация переменной blogform

    if request.method == "POST":    # после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()           # сохраняем изменения после добавления полей
            return redirect('blog') # переадресация на страницу Блог после создания статьи Блога
            
    return render(
        request,
        'app/newpost.html',
        { 
            'blogform': blogform, # передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the video post page."""
    assert isinstance(request, HttpRequest)
    # Добавьте код здесь для обработки запроса и рендеринга страницы videopost
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видеостатья',
            'message': 'Это видеостатья.',
            'year': datetime.now().year,
        }
    )


