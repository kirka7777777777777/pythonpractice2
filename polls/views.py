from django.contrib import messages  # Исправленный импорт
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, UserLoginForm, AddCategoryForm
from .models import Question, Choice, UserProfile, CategoryForm
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, redirect
from .forms import ImageUploadForm


class IndexView(generic.ListView):
    template_name = 'polls/base.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы не сделали выбор.'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polls:profile')  # Исправлено на имя URL
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль.')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    context = {
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)


@login_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()  # Сохраняем категорию
            request.user.userprofile.categories.add(category)  # Добавляем категорию к профилю пользователя
            messages.success(request, f'Категория "{category.name}" успешно добавлена.')
            return redirect('polls:profile')
        else:
            messages.error(request, 'Ошибка при добавлении категории.')
    else:
        form = AddCategoryForm()
    return render(request, 'polls/add_category.html', {'form': form})



def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_image')  # Замените на нужный URL
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})