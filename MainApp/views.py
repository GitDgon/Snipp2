from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required



def index_page(request):
#    print("User:", request.user)
    if request.user.is_authenticated:
        errors = []
    else:
        errors = ["password or username not correct"]  # если не авторизован

    context = {
        'pagename': 'PythonBin',
        "errors": errors
    }

    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "POST":  #если пришел запрос на страничку pages/add_snippet.html POST
#        form_data = request.POST
#        snippet = Snippet(
#            name = form_data['name'],
#            lang = form_data['lang'],
#            code = form_data['code']
#        )
#        snippet.save() #сохраняем введенные данные
        form = SnippetForm(request.POST) #получение информации от формы
        if form.is_valid():     #проверка на валидность
#            form.save()
            snippet = form.save(commit=False) #данные не сохраняем, но возвращаем объект
                                               # сниппета через snippet
            snippet.user = request.user  #добавляем пользователя
            snippet.save()                #сохраняем в BD
        return redirect('snippet-list')
        #print(f'{form_data=}')
        #обработка данных формы
    elif request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета!!!',\
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()   #запрос из базы всех объектов
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    context = {
        'pagename': 'Страница сниппета',
        "snippet": snippet,
    }
    return render(request, 'pages/snippet_page.html', context)


@login_required()    #для обеспечения отображения кнопки Мои снипеты только авторизованным пользователям
def snippet_my(request):
    snippets = Snippet.objects.filter(user=request.user)  #запрос из базы
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def login_page(request):             #аторизация
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
#       print("username =", username)
#       print("password =", password)

       user = auth.authenticate(request, username=username, #проверяем пользователя
                                password=password)
       if user is not None:
           auth.login(request, user)  #если пользователь ОК, то авторизуем
#       else:
 #          # Return error message
 #          pass
       return redirect('home')


def logout_page(request):  #разлогирование
    auth.logout(request)
    return redirect('home')

def registration(request):
    if request.method == "POST":    #Создаем пользователя
        form = UserRegistrationForm(request.POST) #данная форма - валидация введенных пользователь данных user password
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
#            print("errors=", form.errors.items())   #еслм при валидации ошибки, то они запишутся в
#                                             #словарик form.errors
            context = {'form': form}
            return render(request, 'pages/registration.html', context)
    elif request.method == "GET":   #Создаем страницу с формой
        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, 'pages/registration.html', context)



