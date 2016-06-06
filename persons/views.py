from django.shortcuts import render, get_object_or_404, Http404, redirect
from .forms import UserForm, PersonForm, CreateUserForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.models import User
from .models import *
from django.views.generic.edit import CreateView
# Create your views here.

def loginForm(request):
    if not request.user.is_authenticated:
        return redirect('/')
    return render(request, 'persons/login.html')

def logoutView(request):
    if not request.user.is_authenticated:
        raise Http404

    if not request.user.is_superuser:
        user = request.user
        user.is_active = False
        user.save()
        return redirect('/', {'message': 'desactivado'})
    logout(request)
    return redirect('/')

def persons_list_creator(request, pk_user):
    if not request.user.is_authenticated and (pk_user != request.user.pk):
        raise Http404

    persons = Person.objects.filter(userCreator_id=pk_user)
    return render(request, 'persons/person_list.html', {'persons': persons})

def person_list(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        raise Http404

    persons = Person.objects.all()
    return render(request, 'persons/person_list.html', {'persons': persons})

def person_create(request):

    if not request.user.is_authenticated:
        raise Http404

    form = PersonForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.userCreator = request.user
        instance.save()
        if request.user.is_superuser:
            return redirect('/persons/successful')
        return redirect(('/persons/personsuser/{0}'.format(request.user.pk)))

    context = {
        'form': form,
        'message': 'invalid'
    }
    return render(request, "persons/create.html", context)

def person_update(request, pk=None):
    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Person, pk=pk)
    form = PersonForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        if request.user.is_superuser:
            return redirect('/persons/successfuledition')
        return redirect(persons_list_creator(request, request.user.pk), {'message': 'exitoso'})

    context = {
        "person": instance,
        "form": form,
        'message': 'invalid'
    }

    return render(request, 'persons/create.html', context)

def person_delete(request, pk=None):
    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Person, pk=pk)
    instance.delete()
    if request.user.is_superuser:
        return redirect('/persons/successfuldeletion')
    return redirect(persons_list_creator(request, request.user.pk), {'message': 'borrado'})

def users_list(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        raise Http404

    users = User.objects.all()
    return render(request, 'persons/users_list.html', {'users': users})

def disable_user(request, pk):
    if not request.user.is_authenticated and not request.user.is_superuser:
        raise Http404

    user = User.objects.get(pk=pk)
    user.is_active = False
    user.save()
    return redirect('/persons/users')

def enable_user(request, pk):
    if not request.user.is_authenticated and not request.user.is_superuser:
        raise Http404

    user = User.objects.get(pk=pk)
    user.is_active = True
    user.save()
    return redirect('/persons/users')

def search(request):
    if not request.user.is_authenticated:
        raise Http404
    if not request.user.is_superuser:
        return redirect('/persons/personsuser/{0}'.format(request.user.pk))
    return render(request, 'persons/search.html')

def results(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        raise Http404

    name = request.GET['name']
    email = request.GET['email']
    phone = request.GET['phone']

    persons = Person.objects.filter(name__icontains=name, email__icontains=email, phone__icontains=phone)
    return render(request, 'persons/person_list.html', {'persons': persons})

def successful(request):
    if not request.user.is_authenticated:
        raise Http404
    return render(request, 'persons/successful.html', {'message': 'person'})

def successful_edition(request):
    if not request.user.is_authenticated:
        raise Http404
    return render(request, 'persons/successful.html', {'message': 'edited'})

def successful_deletion(request):
    if not request.user.is_authenticated:
        raise Http404
    return render(request, 'persons/successful.html', {'message': 'deleted'})

def successful_user(request):
    if not request.user.is_authenticated and not request.user.is_superuser:
        raise Http404
    return render(request, 'persons/successful.html', {'message': 'user'})

class UserLoginView(View):

    def post(self, request):
        form_class = UserForm(data={'username': self.request.POST['username'],
                                    'password': self.request.POST['password']})

        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/')
        return render(request, 'persons/login.html', {'message': 'invalid'})


class UserCreateView(View):

    form_class = CreateUserForm
    template_name = 'persons/create_user.html'

    def get(self, request):
        if not request.user.is_authenticated and not request.user.is_superuser:
            raise Http404
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if not request.user.is_authenticated and not request.user.is_superuser:
            raise Http404
        form = self.form_class(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            instance.set_password(password)
            instance.save()

            return redirect('/persons/users')

        return render(request, self.template_name, {'form': form, 'message': 'error'})

