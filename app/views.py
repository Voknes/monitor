from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
import base64
import calendar
import datetime
from django.db.models.functions import TruncDate
from django.db.models import Sum, Max
from django.core.files.base import ContentFile
from .models import *
from dadata.models import Address
from users.models import Profile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic.edit import FormMixin

from django import forms
from django.views.decorators.csrf import csrf_exempt

class CreateTarifsForm(forms.ModelForm):
    class Meta:
        model = Tarifs
        fields = ['img']
        widgets = {
            'img': forms.FileInput()
            }

# class CreateTarifsView(LoginRequiredMixin, CreateView):
#     form_class = CreateTarifsForm
#     model = Tarifs
#     template_name = 'app/tarifs_add.html'
    
#     def get_success_url(self):
#         return reverse_lazy('tarifs-add')

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)



class CreateTarifsView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CreateTarifsForm
    # model = Tarifs
    # success_url = '/home/tarifs-add/'
    template_name = 'app/tarifs_add.html'
    # context_object_name = 'tarifs'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        kwargs['tarifs'] = Tarifs.objects.filter(author=self.request.user).order_by('-date')[:2]
        return super(CreateTarifsView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tarifs-add')
    
    def test_func(self):
        if self.request.user.groups.filter(name='supervisor').count() == 0:
            return False
        return True


    # def get_queryset(self):
    #     author = self.request.user
    #     # users = User.objects.all().select_related('profile')
    #     return Tarifs.objects.filter(author=author).order_by('-date')

def not_agent(user):
    if user:
        return user.groups.filter(name='agent').count() == 0
    return False

@login_required
@user_passes_test(not_agent)
def rating_input(request):
    super_id = request.user.id
    all_rating = Rating.objects.filter(author__profile__super_id=super_id).order_by('-faсt_shpd')

    return render(request,"app/rating_input.html",{'ratings':all_rating})

@login_required
@user_passes_test(not_agent)
@csrf_exempt
def saverating(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    rating=Rating.objects.get(id=id)
    if type == "plan_shpd":
        rating.plan_shpd = value
        rating.date = datetime.datetime.now()

    if type == "faсt_shpd":
        rating.faсt_shpd = value
        rating.date = datetime.datetime.now()

    if type == "plan_rout":
        rating.plan_rout = value
        rating.date = datetime.datetime.now()

    if type == "faсt_rout":
        rating.faсt_rout = value
        rating.date = datetime.datetime.now()

    if type == "plan_pr":
        rating.plan_pr = value
        rating.date = datetime.datetime.now()

    if type == "faсt_pr":
        rating.faсt_pr = value
        rating.date = datetime.datetime.now()

    rating.save()
    return JsonResponse({"success":"Updated"})


@login_required
@csrf_exempt
def savecheck(request):
    lat=request.POST.get('lat','')
    lng=request.POST.get('lng','')

    CheckIn.objects.create(author=request.user, latitude=lat, longitude=lng)

    return JsonResponse({"success":"Updated"})

# @login_required
# def home(request):
#     data = {
#         'reports': Reports.objects.all(),
#     }
#     return render(request, 'app/home.html', data)

# @login_required
# def check_in(request):
#     return render(request, 'app/check_in.html')


class ShowAddressView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'app/address.html'
    context_object_name = 'addresses'
    paginate_by = 10

class ShowRatingView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Rating
    template_name = 'app/rating.html'
    context_object_name = 'ratings'
    paginate_by = 10

    def get_queryset(self):
        super_id = self.request.user.profile.super_id
        # users = User.objects.all().select_related('profile')
        return Rating.objects.filter(author__profile__super_id=super_id).order_by('-faсt_shpd')
    
    def test_func(self):
        if self.request.user.groups.filter(name='agent').count() == 0:
            return False
        return True

class ShowUserTarifsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Tarifs
    template_name = 'app/tarifs_show.html'
    context_object_name = 'tarifs'
    paginate_by = 2

    def get_queryset(self):
        super_id = self.request.user.profile.super_id
        # users = User.objects.all().select_related('profile')
        return Tarifs.objects.filter(author_id=super_id)
    
    def test_func(self):
        if self.request.user.groups.filter(name='agent').count() == 0:
            return False
        return True

class ShowHomeView(LoginRequiredMixin, ListView):
    model = Reports
    template_name = 'app/home.html'
    context_object_name = 'reports'

@login_required
@csrf_exempt
def map(request):
    id=request.POST.get('id')
    output = []

    if request.user.groups.filter(name = 'supervisor').exists():
        location = CheckIn.objects.get(id=id)
        output.append({"lat_data": location.latitude, "lng_data": location.longitude})
        
    return JsonResponse(output, safe=False)
    # return JsonResponse({"success":"Updated"})
    # return JsonResponse(output, safe=False)

@login_required
def chart_area(request):
    reports_data = []
    rating_data = []
    output = [reports_data, rating_data]
    if request.user.groups.filter(name = 'supervisor').exists():
        reports = Reports.objects.filter(author__profile__super_id=request.user.id).annotate(date_value=TruncDate('date')).values('date_value').annotate(sum=Sum('shpd')).order_by('-date_value')
        rating = Rating.objects.filter(author__profile__super_id=request.user.id).values('author__profile__super_id').annotate(plan_shpd=Sum('plan_shpd'), faсt_shpd=Sum('faсt_shpd'), plan_rout=Sum('plan_rout'), faсt_rout=Sum('faсt_rout'), plan_pr=Sum('plan_pr'), faсt_pr=Sum('faсt_pr'), date=Max('date'))
        now = rating[0]['date']
        all_days = calendar.monthrange(now.year, now.month)[1]
        today = now.day
        output[1].append({"plan_shpd": rating[0]['plan_shpd'], "faсt_shpd": rating[0]['faсt_shpd'], "plan_rout": rating[0]['plan_rout'], "faсt_rout": rating[0]['faсt_rout'], "plan_pr": rating[0]['plan_pr'], "faсt_pr": rating[0]['faсt_pr'], "all_days": all_days, "today": today})
        # output[1].append({"plan_shpd": 1, "faсt_shpd": 1, "plan_rout": 1, "faсt_rout": 1, "plan_pr": 1, "faсt_pr": 1, "all_days": 1, "today": 1})
        for elem in reports:
            output[0].append(
                {"shpd": elem['sum'], "date": elem['date_value'].strftime("%d.%m")})
    else:
        reports = Reports.objects.filter(author=request.user).order_by('-date')[:30]
        rating = Rating.objects.get(author=request.user)
        now = rating.date
        all_days = calendar.monthrange(now.year, now.month)[1]
        today = now.day
        output[1].append({"plan_shpd": rating.plan_shpd, "faсt_shpd": rating.faсt_shpd, "plan_rout": rating.plan_rout, "faсt_rout": rating.faсt_rout, "plan_pr": rating.plan_pr, "faсt_pr": rating.faсt_pr, "all_days": all_days, "today": today})
        for elem in reports:
            output[0].append(
                {"shpd": elem.shpd, "date": elem.date.strftime("%d.%m")})
    return JsonResponse(output, safe=False)

# Показ отчетов своей группы (руководитель) - Готово
class ShowReportView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Reports
    template_name = 'app/reports.html'
    context_object_name = 'reports'
    paginate_by = 10

    def get_queryset(self):
        super_id = self.request.user.id
        # users = User.objects.all().select_related('profile')
        return Reports.objects.filter(author__profile__super_id=super_id).order_by('-date')

    def test_func(self):
        if self.request.user.groups.filter(name='supervisor').count() == 0:
            return False
        return True


class ShowSuperTimetableForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address']
        widgets = {
            'address': forms.TextInput(attrs={'id': 'address', 'type': 'text', 'name':'address', 'style':'width: 300px;', 'class':'form-control', 'placeholder': 'Поиск по адресу',}),
            }

class ShowUserTimetableView(LoginRequiredMixin, FormMixin, ListView):
    model = Address
    form_class = ShowSuperTimetableForm
    template_name = 'app/address.html'
    context_object_name = 'addresses'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        super_id = Profile.objects.filter(user=user).values('super_id')
        print(super_id)
        form = self.form_class(self.request.GET)
        if user == self.request.user or super_id[0]['super_id'] == self.request.user.id:
            if form.is_valid():
                return Address.objects.filter(author=user, address__icontains=form.cleaned_data['address'])
            return Address.objects.filter(author=user).order_by('-date')
        else:
            return Address.objects.filter(author=self.request.user).order_by('-date')
        
    
    # def test_func(self):
    #     if self.request.user.groups.filter(name='agent').count() == 0 or :
    #         return False
    #     return True


class ShowSuperTimetableView(LoginRequiredMixin, UserPassesTestMixin, FormMixin, ListView):
    model = Address
    form_class = ShowSuperTimetableForm
    template_name = 'app/address.html'
    context_object_name = 'addresses'
    paginate_by = 10
    addresses = []

    def get_queryset(self):
        super_id = self.request.user.id
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Address.objects.filter(address__icontains=form.cleaned_data['address'])
        return Address.objects.filter(author__profile__super_id=super_id).order_by('-date')
    
    def test_func(self):
        if self.request.user.groups.filter(name='supervisor').count() == 0:
            return False
        return True


class ShowUserReportView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Reports
    template_name = 'app/reports.html'
    context_object_name = 'reports'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        super_id = self.request.user.id
        return Reports.objects.filter(author=user, author__profile__super_id=super_id).order_by('-date')

    def test_func(self):
        if self.request.user.groups.filter(name='supervisor').count() == 0:
            return False
        return True
        

class CreateReportForm(forms.ModelForm):
    class Meta:
        model = Reports
        fields = ['shpd','rout', 'tv']
        widgets = {
            'shpd': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'ШПД',}),
            'rout': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Роутеры',}),
            'tv': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Приставки',}),
            }

class CreateObhodForm(forms.ModelForm):
    class Meta:
        model = Obhod
        fields = ['kv','ne_otkrito', 'kv_prezentacii','kv_zayavki']
        widgets = {
            'kv': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Кол-во пройденных квартир',}),
            'ne_otkrito': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Кол-во неоткрытых квартир',}),
            'kv_prezentacii': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Кол-во презентаций',}),
            'kv_zayavki': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Кол-во заявок',}),
            }

class CreateObzvonForm(forms.ModelForm):
    class Meta:
        model = Obzvon
        fields = ['zvonki','nedozvon', 'zv_prezentacii','zv_zayavki']
        widgets = {
            'zvonki': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Кол-во звонков',}),
            'nedozvon': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Кол-во недозвонов',}),
            'zv_prezentacii': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Кол-во презентаций',}),
            'zv_zayavki': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Кол-во заявок',}),
            }

class CreateRaskleykaForm(forms.ModelForm):
    class Meta:
        model = Raskleyka
        fields = ['doma','obyavleniya']
        widgets = {
            'doma': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Кол-во домов',}),
            'obyavleniya': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Кол-во объявлений',}),
            }

# class CreateReportView(LoginRequiredMixin, CreateView):
#     form_class = CreateReportForm
#     model = Reports
#     template_name = 'app/report_add.html'
    
#     def get_success_url(self):
#         username = self.request.user
#         return reverse_lazy('user-reports', kwargs={'username': username})

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

def not_supervisor(user):
    if user:
        return user.groups.filter(name='supervisor').count() == 0
    return False

@login_required
@user_passes_test(not_supervisor)
def report_update(request):
    if request.method == "POST":
        report = CreateReportForm(request.POST)
        obhod = CreateObhodForm(request.POST)
        obzvon = CreateObzvonForm(request.POST)
        raskleyka = CreateRaskleykaForm(request.POST)
        if report.is_valid():
            shpd = form.cleaned_data.get('shpd')
            rout = form.cleaned_data.get('rout')
            tv = form.cleaned_data.get('tv')
            date_now = datetime.datetime.now()
            Reports.objects.update_or_create(author_id=request.user.id, date__date=date_now, defaults={"shpd": shpd, "rout": rout, "tv": tv, "date": date_now})
            messages.success(request, f'Отчет успешно отправлен!')
            return redirect('home')
        
        if form.is_valid():
            shpd = form.cleaned_data.get('shpd')
            rout = form.cleaned_data.get('rout')
            tv = form.cleaned_data.get('tv')
            date_now = datetime.datetime.now()
            Reports.objects.update_or_create(author_id=request.user.id, date__date=date_now, defaults={"shpd": shpd, "rout": rout, "tv": tv, "date": date_now})
            messages.success(request, f'Отчет успешно отправлен!')
            return redirect('home')

        if form.is_valid():
            shpd = form.cleaned_data.get('shpd')
            rout = form.cleaned_data.get('rout')
            tv = form.cleaned_data.get('tv')
            date_now = datetime.datetime.now()
            Reports.objects.update_or_create(author_id=request.user.id, date__date=date_now, defaults={"shpd": shpd, "rout": rout, "tv": tv, "date": date_now})
            messages.success(request, f'Отчет успешно отправлен!')
            return redirect('home')

        if form.is_valid():
            shpd = form.cleaned_data.get('shpd')
            rout = form.cleaned_data.get('rout')
            tv = form.cleaned_data.get('tv')
            date_now = datetime.datetime.now()
            Reports.objects.update_or_create(author_id=request.user.id, date__date=date_now, defaults={"shpd": shpd, "rout": rout, "tv": tv, "date": date_now})
            messages.success(request, f'Отчет успешно отправлен!')
            return redirect('home')
    else:
        form = CreateReportForm()
    return render(request, 'app/report_add.html', {'form': form})

# class CreateReportView(LoginRequiredMixin, CreateView):
#     form_class = CreateReportForm
#     template_name = 'app/report_add.html'
    
#     def form_valid (self, form):
#         # report = form.save(commit=False)
#         # report.save()

#         data = form.cleaned_data
#         Reports.objects.update_or_create(author_id=55, date='2020-05-21', defaults={"shpd": 31})

#         messages.success(self.request, 'The Delivered Docket was created with success!')
#         return super().form_valid(form)
    # def get_success_url(self):
    #     username = self.request.user
    #     return reverse_lazy('user-reports', kwargs={'username': username})

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

# class CreateReportView(LoginRequiredMixin, CreateView):
#     model = Reports
#     fields = ['shpd', 'tv']
#     template_name = 'app/report_add.html'


#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

class UpdateReportView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = CreateReportForm
    model = Reports
    template_name = 'app/report_add.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.groups.filter(name='supervisor').count() == 0:
            return False
        return True

# class InputRatingView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Rating
#     fields = ['plan_shpd', 'faсt_shpd', 'plan_rout', 'faсt_rout', 'plan_pr', 'faсt_pr']
#     template_name = 'app/rating_input.html'
    
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         rait = self.get_object()
#         if self.request.user == rait.author:
#             return True
#         return False
class CreateRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['author', 'plan_shpd', 'faсt_shpd', 'plan_rout', 'faсt_rout', 'plan_pr', 'faсt_pr']
        widgets = {
            'author': forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Агент',}),
            'plan_shpd': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'plan_shpd',}),
            'faсt_shpd': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'faсt_shpd',}),
            'plan_rout': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'plan_rout',}),
            'faсt_rout': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'faсt_rout',}),
            'plan_pr': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'plan_pr',}),
            'faсt_pr': forms.NumberInput(attrs={'class':'form-control form-control-user', 'placeholder': 'faсt_pr',}),
            }

class InputRatingView(LoginRequiredMixin, CreateView):
    form_class = CreateRatingForm
    model = Rating
    template_name = 'app/rating_input.html'
    context_object_name = 'ratings'
    paginate_by = 10

    def get_success_url(self):
        username = self.request.user
        return reverse_lazy('user-reports', kwargs={'username': username})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ShowCheckView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CheckIn
    template_name = 'app/check_show.html'
    context_object_name = 'checks'
    paginate_by = 10

    # def get_queryset(self):
    #     user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     return CheckIn.objects.filter(author=user).order_by('-date')
    def get_queryset(self):
        super_id = self.request.user.id
        return CheckIn.objects.filter(author__profile__super_id=super_id).order_by('-date')

    def test_func(self):
        if self.request.user.groups.filter(name='supervisor').count() == 0:
            return False
        return True

class CreateCheckForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['latitude', 'longitude']
        widgets = {
            'latitude': forms.NumberInput(attrs={'class': 'disabled', 'id': 'latitude',}),
            'longitude': forms.NumberInput(attrs={'class':'disabled', 'id': 'longitude',}),
            # 'img': forms.FileInput()
            }

class CreateCheckView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CreateCheckForm
    model = CheckIn
    template_name = 'app/check_in.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        if self.request.user.groups.filter(name='agent').count() == 0:
            return False
        return True

# def create_post(request):
#     checks = CheckIn.objects.all()
#     response_data = {}

#     if request.POST.get('action') == 'post':
#         author = request.user
#         latitude = request.POST.get('latitude')
#         longitude = request.POST.get('longitude')
#         data = request.POST.get('img')
#         format, imgstr = data.split(';base64,')
#         ext = format.split('/')[-1]
#         data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

#         response_data['latitude'] = latitude

#         CheckIn.objects.create(
#             author = author,
#             latitude = latitude,
#             longitude = longitude,
#             img = data,
#             )
#         return JsonResponse(response_data)

#     return render(request, 'app/check_in.html', {'checks':checks})        

