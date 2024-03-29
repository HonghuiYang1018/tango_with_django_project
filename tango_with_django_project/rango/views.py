from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from rango.models import UserProfile
from datetime import datetime
# Create your views here.


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('views')[:5]
    
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, cnady, cupckae'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    
    return render(request, 'index.html', context = context_dict)


def about(request):
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, cnady, cupckae', 'name':"BY Honghui Yang 2841006"}
    
    return render(request, 'about.html', context = context_dict)



def show_category(request, category_name_slug):
    
    context_dict = {}
    
    try:
        category = Category.objects.get(slug = category_name_slug)
        
        pages = Page.objects.filter(category = category)
        
        context_dict['pages'] = pages
        
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        
        context_dict['category'] = None
        
        context_dict['pages'] = None
        
    return render(request, 'category.html', context = context_dict)


def add_category(request):
    form = CategoryForm()
    
    if form.is_valid():
        form.save(commit=True)
        return redirect('/rango/')
    
    else:
        print(form.errors)
        
    return render(request, 'add_category.html', {'form' : form})



def add_page(request, category_name_slug ):
    
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    if category is None:
        return redirect('/rango/')
    
    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                
                return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
            
        else:
            print(form.errors)
                
    context_dict = {'form': form, 'category': category}
            
    return render(request, 'add_page.html', context=context_dict)




def register(request):
    
    register = False
    
    if request.method == 'POST':
        
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            user.set_passwaord(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            
            if 'picture' in request.FILES['picture']:
                profile.picture = request.Files['picture']
                
                
        else: 
            print(user_form.errors, profile_form.errors)
            
    else:
        user_form = UserForm
        profile_form = UserProfileForm
        
    
    return render(request, 'rango/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered':register})
            







def visitor_cookie_handler(request, response):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        response.set_cookie('last_visit', str(datetime.now()))
    
    else:
        response.set_cookie('last_visit', last_visit_cookie)
        response.set_cookie('visits', visits)