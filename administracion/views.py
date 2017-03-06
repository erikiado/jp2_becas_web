from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import UserForm
from perfiles_usuario.utils import is_administrador


@user_passes_test(is_administrador, login_url='tosp_auth:login')
def admin_main_dashboard(request):
    """View to render the main control dashboard.

    """
    return render(request, 'administracion/dashboard_main.html')


@user_passes_test(is_administrador, login_url='tosp_auth:login')
def admin_users_dashboard(request):
    """View to render the users control dashboard.

    """
    users = User.objects.all()
    create_user_form = UserForm()

    return render(request, 'administracion/dashboard_users.html',
                  {'all_users': users, 'create_user_form': create_user_form})


@user_passes_test(is_administrador, login_url='tosp_auth:login')
def admin_users_create(request):
    """ View to create users.

    """
    if request.method == 'POST':
        forma = UserForm(request.POST)
        if forma.is_valid():
            forma.save()
            return redirect('administracion:users')


@user_passes_test(is_administrador, login_url='tosp_auth:login')
def admin_users_edit_form(request, user_id):
    """ View to send the form to edit users.

    """
    if request.is_ajax():
        user = User.objects.get(pk=user_id)
        form = UserForm(instance=user, initial={'rol_usuario': user.groups.all()[0].name})
        return render(request, 'administracion/user_form.html',
                      {'user_form': form, 'from_user': user})


@user_passes_test(is_administrador, login_url='tosp_auth:login')
def admin_users_edit(request):
    """ View to edit users.

    """
    if request.method == 'POST':
        user_id = request.POST['user_id']
        instance = User.objects.get(pk=user_id)
        form = UserForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('administracion:users')


@user_passes_test(is_administrador, login_url='tosp_auth:login')
def admin_users_delete_modal(request, user_id):
    """ View to send the form to delete users.

    """
    if request.is_ajax():
        user = User.objects.get(pk=user_id)
        return render(request, 'administracion/user_delete_modal.html',
                      {'delete_user': user})


@user_passes_test(is_administrador, login_url='tosp_auth:login')
def admin_users_delete(request):
    """ View to delete users.

    """
    if request.method == 'POST':
        user_id = request.POST['user_id']
        instance = User.objects.get(pk=user_id)
        instance.delete()
        return redirect('administracion:users')
