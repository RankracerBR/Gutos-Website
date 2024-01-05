#Libs/Modules
from .forms import RegisterForm, CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from ML_Training import identify_words_content as idc
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .models import  Register, CustomUser, UserProfileHistory
import subprocess
import requests
import platform
import random


#Functions
'''Login page'''
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


'''User page'''
@login_required
def User_page(request):
    user = request.user
    return render(request, 'user_page.html', {'user':user})


'''Logout function'''
@login_required
def Logout_user(request):
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
    

'''Update the profile'''
@login_required
def Update_user(request):
    file_name1 = 'ML_Training/identify_cols.py'
    file_name2 = 'ML_Training/identify_badwords.py'
    file_name3 = 'ML_Training/identify_imgs.py'
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            old_user = CustomUser.objects.get(pk=request.user.pk)
            form.save()

            if (
                old_user.last_name != request.user.last_name or
                old_user.description != request.user.description or
                old_user.image != request.user.image
            ):
                UserProfileHistory.objects.create(
                    user=request.user,
                    last_name=old_user.last_name,
                    description=old_user.description,
                    image=old_user.image
                )

            Execute_verification(file_name1, file_name2, file_name3)
            return redirect('user_page')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'alter_user.html', {'form': form})


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
                                                      'name': request.session.get('name'),
                                                      'image': request.session.get('image'),
                                                      'description': request.session.get('description')}) #Corrige o bug de sumir com a imagem do usuário


'''Send the email of the form to the user'''
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


'''Verification'''
def Verify(request, token):
    try:
        user = Register.objects.get(token=token)
        user.is_verified = True
        user.save()
        return redirect('register_account')
    except Register.DoesNotExist:
        return render(request, 'register_account.html')


'''Register the user'''
def Register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.status = 'regular'
            user.save()
            messages.success(request, 'Usuário cadastrado com sucesso! Faça o login para acessar.')
            return redirect('index') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'register_account.html', {'form': form})
