from django.shortcuts import render

from django.http import JsonResponse
from django.core.cache import cache
from lib.sms import send_sms
from common import keys,errors
from lib.http import render_json
from .models import User
# Create your views here.

#发送验证码
def submit_phone(request):
    phone = request.POST.get('phone')
    send_sms(phone)
    return render_json()

def submit_vcode(request):
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    cache_vcode = cache.get(keys.VCODE_KEYS % phone)
    print(cache_vcode)
    if vcode == cache_vcode:
        user, _ = User.objects.get_or_create(phonenum=phone,defaults={'nickname':phone})
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    return render_json(code=errors.VCODE_ERROR,data='验证码错误')
