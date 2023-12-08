from django.db import models

# Create your models here.

class Registro(models.Model):
    nome = models.CharField(max_length=50, default=None)
    email = models.EmailField()

    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length = 100, default=None)

class CadastroUsuario(models.Model):
    complete_name = models.CharField(max_length=80,default=None)
    complete_email = models.EmailField()
    complete_password = models.CharField(max_length=20, default=None)
    complete_image = models.ImageField(upload_to='media/')
    complete_description = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CadastroUsuario'

    def __str__(self):
        return self.complete_email

    def __str__(self):
        return self.complete_name

class CadastroUsuarioHistorico(models.Model):
    usuario = models.ForeignKey(CadastroUsuario, on_delete=models.CASCADE)
    nome_anterior = models.CharField(max_length=80)
    descricao_anterior = models.TextField()
    data_atualizacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'CadastroUsuarioHistorico'

    def get_email(self):
        return self.usuario.complete_email

    def __str__(self):
        return f"{self.usuario.complete_name} - {self.usuario.complete_email} - {self.data_atualizacao}"
    

class Post(models.Model):
    author= models.ForeignKey(CadastroUsuario, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Post'
    
    def __str__(self):
        return f"{self.title} - {self.author.complete_name}"


class Comment(models.Model):
    user = models.ForeignKey(CadastroUsuario, on_delete=models.CASCADE, related_name='comments')
    title = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Comment'
    
    def __str__(self):
        return f"Comment by {self.user.complete_name}"
    

##Manutenção
#Criar conta de banimento
class Banimento(models.Model):
    usuario = models.ForeignKey(CadastroUsuario, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=255)
    data_banimento = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.complete_name} - {self.motivo}"