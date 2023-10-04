from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, PerfilUsuarioForm
from .models import  Registro, CadastroUsuario
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
import time
import random



'''Página do Usuário'''
@login_required
def User_page(request):
    try:
        user_profile = CadastroUsuario.objects.get(complete_name=request.user)
    except CadastroUsuario.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile = form.save(commit=False)
            user_profile.save()
            return redirect('pagina_usuario')
    else:
        form = PerfilUsuarioForm(instance=user_profile)
    return render(request, 'user_page.html', {'form': form})

def Login_Usuario(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        
        # Verificar se o usuário existe no banco de dados
        try:
            CadastroUsuario.objects.get(complete_name=nome, complete_email=email, complete_password=senha)
        except CadastroUsuario.DoesNotExist:
            # Se o usuário não existir, exibir mensagem de erro
            mensagem_erro = "Credenciais incorretas. Tente novamente."
            return render(request, 'index.html', {'mensagem_erro': mensagem_erro})
        
        # Se o usuário existir e as credenciais estiverem corretas, redirecionar para 'user_page.html'
        return redirect('pagina_usuario')
    
    return render(request, 'index.html')


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

'''Registra o usuário'''
def CadastroUsuario_1(request):
    mensagem = 'Usuário já cadastrado'
    if request.method == "POST":
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario_existe = CadastroUsuario.objects.filter(complete_name=usuario, complete_email=email, complete_password=senha)

        if usuario_existe:
            return render(request, 'register_account.html', {'mensagem':mensagem})
        else:
            novo_usuario = CadastroUsuario(complete_name=usuario, complete_email=email, complete_password=senha)
            time.sleep(5)
            novo_usuario.save()
            return render(request, 'sucess.html')

"Redireciona a página quando o usuário clica no token"
def verify(request, token):
    try:
        user = Registration_Token.objects.filter(token = token)
        if user:
            user.is_verified = True
        return redirect('index')
    except Exception:
        return render(request, 'register_account.html')



