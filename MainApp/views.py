from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm
from django.contrib import auth



def index_page(request):
    context = {'pagename': 'PythonBin'}
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
        form = SnippetForm(request.POST)
        if form.is_valid():
#            form.save()
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
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
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def login_page(request):             #аторизация
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
#       print("username =", username)
#       print("password =", password)

       user = auth.authenticate(request, username=username,
                                password=password)
       if user is not None:
           auth.login(request, user)
       else:
           # Return error message
           pass
       return redirect('home')


def logout_page(request):  #разлогирование
    auth.logout(request)
    return redirect('home')