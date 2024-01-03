#Libs/Modules
from .models import  Register
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from ML_Training import identify_words_content as idc
from .forms import RegisterForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login , logout, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import subprocess
import requests
import platform
import random


#Functions
'''Tela de Login'''
def Login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('user_page')
    else:
        form = AuthenticationForm()
    return render(request, 'index.html', {'form': form})


'''Página do Usuário'''
@login_required
def User_page(request):
    user = request.user
    return render(request, 'user_page.html', {'user':user})


'''Tela de Logout'''
def Logout_User(request):
    logout(request)
    return redirect('index')


'''Executa os arquivos de verificação de palavras'''
def Execute_verification(file_name1, file_name2, file_name3):
    if platform.system() == "Windows":
        # Se o sistema operacional for Windows
        subprocess.run(['python', file_name1])
        subprocess.run(['python', file_name2])
        subprocess.run(['python', file_name3])
    elif platform.system() == "Linux":
        # Se o sistema operacional for Linux
        subprocess.run(['python3', file_name1])
        subprocess.run(['python3', file_name2])
        subprocess.run(['python', file_name3])
    else:
        print("Sistema operacional não suportado")
    
    #Chamar arquivo identify_imgs.py


'''Atualiza o Perfil do Usuário'''
def Atualizar_Usuario(request):
    ...


'''Api'''
def Search_images(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        
        if query:
            api_key = 'AIzaSyCq2VHeLaFt7BojWWYo97wHeanOLhCVOVc'
            search_engine_id = '646f6762000414f9f'
        
            url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&searchType=image&q={query}'
            
            response = requests.get(url)
            data = response.json()
            
            detect = idc.detector
            result = detect.detect_prohibited_content(query)
            
            print(result)
            
            return render(request, 'user_page.html', {'results': data.get('items', []),
                                                      'nome': request.session.get('nome'),
                                                      'imagem': request.session.get('imagem'),
                                                      'descricao': request.session.get('descricao')}) #Corrige o bug de sumir com a imagem do usuário

'''Registro para envio do formulário'''
def Registration_Token(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False  # Assuming initially it's not verified
            user.token = str(random.random()).split('.')[1]
            user.save()

            domain_name = get_current_site(request).domain
            link = f'http://{domain_name}/verify/{user.token}'        
            send_mail(
                'Verificação de Email',
                f'Clique para completar seu cadastro: {link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return HttpResponse('Verifique a caixa de entrada do seu email para confirmar')
    else:
        form = RegisterForm()
    return render(request, 'send_token.html', {'form': form})


def Verify(request, token):
    try:
        user = Register.objects.get(token=token)
        user.is_verified = True
        user.save()
        return redirect('index')  # Redirect to your desired view after successful verification
    except Register.DoesNotExist:
        return render(request, 'register_account.html')


'''Registra o usuário'''
def Register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.status = 'regular'  # Defina o status padrão aqui
            user.save()
            return redirect('index')  # Redirecionar para a página de login após o registro
    else:
        form = CustomUserCreationForm()
    return render(request, 'register_account.html', {'form': form})

'''
#Development
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user = CadastroUsuario.objects.get(id=request.user.id)
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            post = Post.objects.create(author=user, title=title, content=content)
            return redirect('create_post')
    else:
        form = PostForm()
    posts = Post.objects.all()
    return render(request, 'posts.html', {'form': form, 'posts': posts})
'''


'''
@login_required
def create_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user = CadastroUsuario.objects.get(id=request.user.id)
            content = form.cleaned_data['content']
            comment = Comment.objects.create(user=user, title=post, content=content)
            return redirect('create_post')  # Redirecionar para a página de posts após a criação do comentário
    else:
        form = CommentForm()
    return render(request, 'posts.html', {'form': form, 'post': post})

'''

