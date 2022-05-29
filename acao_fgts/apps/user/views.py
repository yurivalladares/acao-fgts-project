from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'O nome não pode ficar em branco')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'O email não pode ficar em branco')
            return redirect('cadastro')
        if senha_nao_iguais(password, password2):
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=password)
        user.save()
        messages.success(request, 'Conta criada com sucesso!')
        return redirect('login')
    else:
        return render(request, 'cadastro.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if campo_vazio(email) or campo_vazio(password):
            messages.error(request, 'É necessário prencher os campos em branco')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Login inválido')
                return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def campo_vazio(campo):
    return not campo.strip()


def senha_nao_iguais(password, password2):
    return password != password2

