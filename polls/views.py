from django.contrib import messages  # Исправленный импорт
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, UserLoginForm
from .models import Question, Choice, UserProfile
from django.urls import reverse
from django.views import generic
from .forms import ImageUploadForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Application, Category
from .forms import ApplicationDeleteForm, CompleteApplicationForm, InProgressApplicationForm, CategoryForm
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


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
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES) # request.FILES для обработки загруженных файлов
        if form.is_valid():
            # Создаем экземпляр модели, но не сохраняем в базу сразу
            application = Application(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                photo=form.cleaned_data['photo'],
                user=request.user # Связываем заявку с текущим пользователем
            )

            messages.success(request, 'Заявка успешно создана и отправлена.')
            return redirect('polls:application_list') # Или на другую страницу успеха
        else:
            messages.error(request, 'Ошибка при создании заявки. Пожалуйста, проверьте форму.')
    else:
        form = ApplicationForm()
    return render(request, 'polls/create_application.html', {'form': form})


from .models import Application  # Импортируйте вашу модель заявки

class ApplicationCreateView(CreateView):
    model = Application
    fields = ['field1', 'field2']  # Укажите поля вашей модели
    template_name = 'polls/application_form.html'  # Укажите свой шаблон

    def form_valid(self, form):
        # Сохраните форму и перенаправьте на страницу со списком заявок
        response = super().form_valid(form)
        return redirect('application_list')  # Перенаправление на URL с именем 'application_list'

# polls/views.py
from django.views.generic import ListView
from .models import Application

class ApplicationListView(ListView):
    model = Application
    template_name = 'polls/application_list.html'  # Укажите свой шаблон
    context_object_name = 'applications'  # Имя контекста для доступа к объектам в шаблоне



def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_image')  # Замените на нужный URL
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})

#
# def home_view(request):
#     return render(request, 'base.html')

def homepage(request):
    completed_applications = Application.objects.filter(status='completed').order_by('-timestamp')[:4]
    in_progress_count = Application.objects.filter(status='in_progress').count()
    return render(request, 'polls/base.html', {
        'completed_applications': completed_applications,
        'in_progress_count': in_progress_count,
    })

@login_required
def user_applications(request):
    applications = Application.objects.filter(user=request.user).order_by('-timestamp')
    status_filter = request.GET.get('status')
    if status_filter and status_filter in dict(Application.STATUS_CHOICES):
        applications = applications.filter(status=status_filter)
    return render(request, 'polls/user_application_list.html', {
        'applications': applications,
        'status_choices': Application.STATUS_CHOICES,
        'selected_status': status_filter,
    })

@login_required
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)
    if application.status in ['in_progress', 'completed']:
        messages.error(request, "Нельзя удалить заявку со статусом 'Принято в работу' или 'Выполнена'.")
        return redirect('polls:user_applications')

    if request.method == 'POST':
        form = ApplicationDeleteForm(request.POST)
        if form.is_valid():
            application.delete()
            messages.success(request, "Заявка успешно удалена.")
            return redirect('polls:user_applications')
    else:
        form = ApplicationDeleteForm()
    return render(request, 'polls/application_confirm_delete.html', {'application': application, 'form': form})

@user_passes_test(lambda u: u.is_staff) # Ограничение доступа для администраторов
def change_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id, status='new') # Только для новых заявок
    if request.method == 'POST':
        status = request.POST.get('status_change')
        if status == 'completed':
            form = CompleteApplicationForm(request.POST, request.FILES, instance=application)
            if form.is_valid():
                application = form.save(commit=False)
                application.status = 'completed'
                application.save()
                messages.success(request, "Статус заявки изменен на 'Выполнена'. Дизайн добавлен.")
                return redirect('polls:admin_application_list') # Перенаправление на список админ заявок
        elif status == 'in_progress':
            form = InProgressApplicationForm(request.POST, instance=application)
            if form.is_valid():
                application = form.save(commit=False)
                application.status = 'in_progress'
                application.save()
                messages.success(request, "Статус заявки изменен на 'Принято в работу'. Комментарий добавлен.")
                return redirect('polls:admin_application_list') # Перенаправление на список админ заявок
        else:
            messages.error(request, "Неверный статус для изменения.")
            return redirect('polls:admin_application_list') # Перенаправление на список админ заявок
    else:
        complete_form = CompleteApplicationForm(instance=application)
        inprogress_form = InProgressApplicationForm(instance=application)
        return render(request, 'polls/application_change_status.html', {
            'application': application,
            'complete_form': complete_form,
            'inprogress_form': inprogress_form,
        })

@user_passes_test(lambda u: u.is_staff)
def admin_category_list(request):
    categories = Category.objects.all()
    return render(request, 'polls/admin_category_list.html', {'categories': categories})

@user_passes_test(lambda u: u.is_staff)
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Категория успешно добавлена.")
            return redirect('polls:admin_category_list')
    else:
        form = CategoryForm()
    return render(request, 'polls/admin_category_create.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def admin_category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Категория и все связанные с ней заявки удалены.")
        return redirect('polls:admin_category_list')
    return render(request, 'polls/admin_category_delete.html', {'category': category})

@user_passes_test(lambda u: u.is_staff)
def admin_application_list(request):
    applications = Application.objects.all().order_by('-timestamp')
    return render(request, 'polls/admin_application_list.html', {'applications': applications})