from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .models import  Registro, CadastroUsuario, CadastroUsuarioHistorico, Banimento
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .forms import RegistroForm
import subprocess
import platform
import random
import sys

'''Tela de Login'''
def Login_Usuario(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']

        try:
            # Autentica o usuário
            usuario = CadastroUsuario.objects.get(complete_name=nome, complete_email=email, complete_password=senha)
            try:
                banimento = Banimento.objects.get(usuario=usuario)
                mensagem_banimento = "Sua conta foi banida por razões específicas"
                return render(request, 'index.html', {'mensagem_banimento':mensagem_banimento})
            except Banimento.DoesNotExist:
                nome = usuario.complete_name
                imagem = usuario.complete_image
                descricao = usuario.complete_description

                request.session['nome'] = nome
                request.session['imagem'] = imagem.url 
                request.session['descricao'] = descricao

                return redirect('pagina_usuario')

        except CadastroUsuario.DoesNotExist:
            mensagem_erro = "Credenciais incorretas. Tente novamente."
            messages.error(request, mensagem_erro) 
            return render(request, 'index.html')

    return render(request, 'index.html')

'''Tela de Logout'''
def Logout_Usuario(request):
    logout(request)
    return redirect('index')

'''Página do Usuário'''
def User_Page(request):
    nome = request.session.get('nome')
    imagem = request.session.get('imagem')
    descricao = request.session.get('descricao')

    if nome is None or imagem is None or descricao is None:
        return redirect('index')  

    return render(request, 'user_page.html', {'nome': nome, 'imagem': imagem, 'descricao': descricao})

'''Executa os arquivos de verificação de palavras'''
def execute_verification(file_name1, file_name2):
    if platform.system() == "Windows":
        # Se o sistema operacional for Windows
        subprocess.run(['python', file_name1])
        subprocess.run(['python', file_name2])
    elif platform.system() == "Linux":
        # Se o sistema operacional for Linux
        subprocess.run(['python3', file_name1])
        subprocess.run(['python3', file_name2])
    else:
        print("Sistema operacional não suportado")
    
    #Chamar arquivo identify_imgs.py
    
'''Atualiza o Perfil do Usuário'''
@login_required
def Atualizar_Usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        imagem = request.FILES.get('imagem')

        usuario = CadastroUsuario.objects.get(complete_email=request.user.email)

        CadastroUsuarioHistorico.objects.create(
            usuario=usuario,
            nome_anterior=usuario.complete_name,
            descricao_anterior=usuario.complete_description
        )

        usuario.complete_name = nome
        usuario.complete_description = descricao
        if imagem:
            usuario.complete_image = imagem
        usuario.save()

        request.session['nome'] = usuario.complete_name
        request.session['descricao'] = usuario.complete_description
        if usuario.complete_image:
            request.session['imagem'] = usuario.complete_image.url
        else:
            request.session['imagem'] = None

        file_name1 = 'ML_Training/identify_cols.py'
        file_name2 = 'ML_Training/identify_badwords.py'

        execute_verification(file_name1,file_name2)
    
        return redirect('pagina_usuario')

'''Registro para envio do formulário'''
def Registration_Token(request):
    form = RegistroForm()
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        user = Registro(nome=username, email=email)
        
        domain_name = get_current_site(request).domain
        token = str(random.random()).split('.')[1]
        user.token = token
        
        link = f'http://{domain_name}/verify/{token}'        
        
        send_mail(
            'Verificação de Email',
            f'Clique para completar seu cadastro : {link}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return HttpResponse('Verique a caixa de entrada do seu email para confirmar')
        
    return render(request, 'send_token.html', {'form': form})

"Redireciona a página quando o usuário clica no token"
def verify(request, token):
    try:
        user = Registration_Token.objects.filter(token = token)
        if user:
            user.is_verified = True
        return redirect('index')
    except Exception:
        return render(request, 'register_account.html')

'''Registra o usuário'''
def CadastroUsuario_1(request):
    message = 'Email já registrado'
    if request.method == 'POST':
        complete_name = request.POST.get('complete_name')
        complete_email = request.POST.get('complete_email')
        complete_password = request.POST.get('complete_password')
        complete_image = request.FILES.get('complete_image')
        complete_description = request.POST.get('complete_description')
        
        if CadastroUsuario.objects.filter(complete_email=complete_email).exists():
            return render(request, 'register_account.html', {'message':message})
        
        usuario = CadastroUsuario(
            complete_name=complete_name,
            complete_email=complete_email,
            complete_password=complete_password,
            complete_image=complete_image,
            complete_description=complete_description
        )
        
        usuario.save()
        
        return render(request, 'sucess.html')
    
    return render(request, 'register_account.html')


