from datetime import datetime

import pytz

from .models import *
from django.utils import timezone


def change_info(request):
    count_nums = VisitNumber.objects.filter(id=1)
    if count_nums:
        count_nums = count_nums[0]
        count_nums.count += 1
    else:
        count_nums = VisitNumber()
        count_nums.count = 1
    count_nums.save()

    if 'HTTP_X_FORWARDED_FOR' in request.META:
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]
    else:
        client_ip = request.META['REMOTE_ADDR']

    ip_exist = Userip.objects.filter(ip=str(client_ip))
    if ip_exist:
        uobj = ip_exist[0]
        uobj.count += 1
        uobj.visitTime = timezone.now()
    else:
        uobj = Userip()
        uobj.ip = client_ip
        uobj.count = 1
        uobj.visitTime = timezone.now()
    uobj.save()
    return client_ip, count_nums.count
