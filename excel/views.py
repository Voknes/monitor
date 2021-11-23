from django.shortcuts import render, redirect
from django.http import HttpResponse
from .resources import RatingResource
from tablib import Dataset
from app.models import Rating
from users.models import Profile
import datetime
from django.contrib import messages
from collections import Counter
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

def not_agent(user):
    if user:
        return user.groups.filter(name='agent').count() == 0
    return False

@login_required
@user_passes_test(not_agent)
def simple_upload(request):
    if request.method == 'POST':
        rating_resource = RatingResource()
        dataset = Dataset()
        new_ratings = request.FILES['file']

        imported_data = dataset.load(new_ratings.read(),format='xlsx')
        imported_data.headers = ['agent', 'type']

        from collections import defaultdict
        res = defaultdict(list)
        results = []
        for v, k in imported_data:
            res[k].append(v)
        data = {k:{'name':v} for k,v in res.items()}

        count_pr = Counter(data['TV приставка']['name'])
        count_rout = Counter(data['Wi-Fi роутер']['name'])
        count_shpd = Counter(data['ШПД']['name'])

        name_list = []
        for key in count_shpd:
            name_list.append(key)


        super_id = request.user.id
        fio = Profile.objects.filter(super_id=super_id).values('name')
        
        fio_list = []
        for value in fio:
            fio_list.append(value['name'])


        error_name = list(set(fio_list) ^ set(name_list))
        error_message = ", ".join(error_name) 

        result_name=list(set(fio_list) & set(name_list))
        
        for name in result_name:
            rating = Rating.objects.get(author__profile__super_id=super_id, author__profile__name=name)

            rating.faсt_shpd = count_shpd[name]
            rating.date = datetime.datetime.now()

            rating.faсt_rout = count_rout[name]
            rating.date = datetime.datetime.now()

            rating.faсt_pr = count_pr[name]
            rating.date = datetime.datetime.now()

            rating.save()

        if error_name:
            messages.warning(request, f'Внимание! Рейтинг для следующих полльзователей не обновился: {error_message}. По одной из следующих причин: у пользователя нет результатов, ошибка в написании ФИО или пользователь не зарегистрирован.')
            return redirect('rating-input')

    return render(request, 'app/rating_input.html')
