import random
import time
import json
from datetime import datetime, date
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from signups.models import Signup


# Create your views here.
def index(request):
    data = Signup.objects.all()

    truncate_date = connection.ops.date_trunc_sql('month', 'signup_date')
    qs = Signup.objects.extra({'month': truncate_date})
    report = qs.values('month').annotate(Sum('count')).order_by('month')

    labels = []
    count = []
    for data in report:
        sd = datetime.strptime(str(data['month']), '%Y-%m-%d %H:%M:%S').date()
        labels.append(str(sd.strftime('%b %Y')))
        count.append(str(data['count__sum']))

    return render(request, "index.html", {'labels': labels, 'values': count})


def getSignups():

    response_data = {}


    data = Signup.objects.all()

    truncate_date = connection.ops.date_trunc_sql('month', 'signup_date')
    qs = Signup.objects.extra({'month': truncate_date})
    report = qs.values('month').annotate(Sum('count')).order_by('month')

    for data in report:
        sd = datetime.strptime(str(data['month']), '%Y-%m-%d %H:%M:%S').date()
        if 'labels' not in response_data:
            response_data['labels'] = []
        if 'count' not in response_data:
            response_data['count'] = []
        response_data['labels'].append(sd.strftime('%b %Y'))
        response_data['count'].append(data['count__sum'])
    return response_data


@csrf_exempt
def create(request):
    year = date.today().year

    #for i in range(1, 1001):
    month = random.choice(range(1, 13))
    day = random.choice(range(1, 29))
    rdate = datetime(int(year), month, day)

    su = Signup(signup_date=rdate,
                count=random.randint(1, 50),
                )

    su.save()

    response_data = getSignups()
    return HttpResponse(json.dumps(response_data), content_type="application/json")
