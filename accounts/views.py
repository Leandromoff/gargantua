from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import UserManager
from .forms import LoginForm, CreateUserForm, ChangePasswordForm
from .utils import generate_random_password, send_password_email


def login_view(request):
    """View de login"""
    if request.user.is_authenticated:
        return redirect('network_tools:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('network_tools:dashboard')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """View de logout"""
    logout(request)
    return redirect('accounts:login')


@login_required
def user_list_view(request):
    """View de listagem de usuários (apenas para admins)"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
        return redirect('accounts:change_password')
    
    user_manager = UserManager()
    users = user_manager.list_users()
    
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def create_user_view(request):
    """View de criação de usuário (apenas para admins)"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem criar usuários.')
        return redirect('accounts:user_list')
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            is_admin_site = form.cleaned_data['is_admin_site']
            
            # Gerar senha aleatória
            password = generate_random_password()
            
            try:
                user_manager = UserManager()
                user_manager.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_admin_site=is_admin_site,
                    roles=['administrator'] if is_admin_site else ['user']
                )
                
                # Tentar enviar email
                email_sent = send_password_email(email, username, password)
                
                if email_sent:
                    messages.success(request, f'Usuário {username} criado com sucesso! Email enviado com a senha.')
                else:
                    messages.warning(request, f'Usuário {username} criado com sucesso! Senha: {password} (email não pôde ser enviado)')
                
                return redirect('accounts:user_list')
                
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = CreateUserForm()
    
    return render(request, 'accounts/create_user.html', {'form': form})


@login_required
def change_password_view(request):
    """View de troca de senha"""
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            
            # Atualizar senha
            request.user.set_password(new_password)
            
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('accounts:change_password')
    else:
        form = ChangePasswordForm(user=request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
@require_POST
def toggle_user_status(request):
    """View para ativar/desativar usuário via AJAX"""
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Acesso negado'})
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        
        if not username:
            return JsonResponse({'success': False, 'error': 'Username não fornecido'})
        
        if username == request.user.username:
            return JsonResponse({'success': False, 'error': 'Você não pode desativar sua própria conta'})
        
        user_manager = UserManager()
        user = user_manager.get_user(username)
        
        if not user:
            return JsonResponse({'success': False, 'error': 'Usuário não encontrado'})
        
        # Alternar status
        new_status = not user.is_active
        user_manager.update_user(username, is_active=new_status)
        
        status_text = 'ativado' if new_status else 'desativado'
        return JsonResponse({
            'success': True, 
            'message': f'Usuário {username} {status_text} com sucesso!',
            'new_status': new_status
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

