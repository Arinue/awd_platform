#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import Score, Flag, Logs, Status
import datetime
import random
from django.utils.timezone import utc
from django.db.models import Q

import hashlib

def dict2list(dic:dict):
    ''' 将字典转化为列表 '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst

# Create your views here.

def index(request):
    utcnow = datetime.datetime.utcnow().replace(tzinfo=utc)
    message = ['success', '欢迎来到提交平台']  # "Success Message" "success"
    if request.POST:
        """ log:1:数据正确  log:0:flag错误    log:-1:用户错误     log:-2:flag过期   log:-3:未提交flag
        """
        log = -3
        # 判断是否正确用户
        score_now=0
        s = (request.POST['token']+request.POST['flag'])       
        f = open("/var/www/awd_platform/app/token+flag.txt","a")
        f.write(s+" ")
        f.close

        if Score.objects.filter(flag_num=request.POST['token']):
            # 判断是否提交flag
            if Flag.objects.filter(flag_num=request.POST['flag']):
                # 判断flag是否正确
                if Flag.objects.filter(flag_num=request.POST['flag'])[0].target_num == Status.objects.filter(player_num=Score.objects.filter(flag_num=request.POST['token'])[0].player_num)[0].target_num:
                    log = -4
                elif (utcnow - Flag.objects.filter(
                        flag_num=request.POST['flag'])[0].create_time).total_seconds() < 300:
                    log = 1
                    #Flag.objects.filter(flag_num=request.POST['flag']).update(create_time='2018-04-20 16:39:05')
                else:
                    log = -2
                with (open('/var/www/awd_platform/app/token+flag.txt', 'r')) as text:
                    words = text.read()
                m = words.count(s)
                flag = request.POST['flag']
                n = words.count(flag)
                if m<1:
                    
                    if log==1:
                        score_now = 100
                    elif log == -4:
                        score_now = 0

                    fraction = Score.objects.filter(flag_num=request.POST['token'])[0].fraction + score_now
                    Score.objects.filter(flag_num=request.POST['token']).update(fraction=fraction)
                    if n<1:
                        fraction = Score.objects.filter(flag_num=Flag.objects.filter(flag_num=request.POST['flag'])[0].target_num)[0].fraction -100
                        Score.objects.filter(flag_num=Flag.objects.filter(flag_num=request.POST['flag'])[0].target_num).update(fraction=fraction)
                    Logs(
                     player_num='服务器被攻陷',
                     flag_num=Flag.objects.filter(flag_num=request.POST['flag'])[0].target_num,
                     result=-100
                    ).save()
                    print(score_now)
                else:
                    log=-2
            else:
                log=0
            Logs(
                player_num=Score.objects.filter(flag_num=request.POST['token'])[0].player_num,
                flag_num=request.POST['flag'],
                result=score_now
            ).save()

        else:
            log = -1
        if log == -1:
            message[0], message[1] = "warning", "选手token错误"
        elif log == 0:
            message = "warning", "flag错误了"
        elif log == 1:
            message = "success", "恭喜你，拿分了呢"
        elif log == -2:
            message = "warning", "flag过期啦！再去拿一个吧！"
        elif log == -4:
            message = "warning", "亲，恭喜你，成功的交了自己的flag！"
    return render(request, 'index.html', {'message': message, 'mess': None, 'backimg': random.randint(0, 16)})


def score(request):
    message = ['success', '来查看总榜了呢']
    return render(request, 'table.html', {'message': message, 'backimg': random.randint(0, 16)})


def api1(request):
    htmls = ''
    html = {}
    for i in Status.objects.all():
        s = Score.objects.filter(player_num=i.player_num)[0]
        if i.run == 0:
            r = '已宕机'
        else:
            r = '运行正常'
        html[i.player_num] =[int(s.fraction),r]
    htm = sorted(dict2list(html), key=lambda x:x[1], reverse=True) # 按照第1个元素降序排列
    j = 1
    for i in htm:
        t = str(j)+"&emsp;&emsp;&emsp;"
        htmls += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format('&ensp;'+t+i[0],'&ensp;'+str(i[1][0]),i[1][1])
        j += 1   
    return HttpResponse(htmls)



def api2(request):
    html = ''
    if 'Arinue' not in request.META['HTTP_REFERER']:
        for i in Logs.objects.filter(Q(result=100) | Q(result=-100))[::-1][0:10]:
            if '宕机'and '攻陷' in i.player_num:
                be_hacked=Status.objects.filter(target_num=i.flag_num)[0].player_num
            else:
                be_hacked=Status.objects.filter(target_num=Flag.objects.filter(flag_num=i.flag_num)[0].target_num)[0].player_num
            html += """<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(
                i.player_num,
                be_hacked,
                i.last,
                i.result
            )
    else:
        for i in Logs.objects.all()[::-1][0:10]:
            
            html += """<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(
                i.player_num,
                i.flag_num,
                i.last,
                i.result
            )
    return HttpResponse(html)

def api3(request):
    html = ''
    utcnow = datetime.datetime.utcnow().replace(tzinfo=utc)
    if 'Arinue' in request.META['HTTP_REFERER']:
        for i in Flag.objects.all()[::-1][0:10]:
            print(utcnow)
            print(i.create_time)
            if (utcnow - i.create_time).total_seconds() < 300:
                te = '有效'
            else:
                te = '已失效'
            html += """<tr><td>{}</td><td>{}</td><td>{}</td></tr>""".format(
                i.target_num,
                i.flag_num,
                te
            )
        return HttpResponse(html)
    return HttpResponseNotFound

def api4(request):
    hl = hashlib.md5()
    str1=str(request.POST['token'])
    hl.update(str1.encode(encoding='utf-8'))
    print(hl.hexdigest())
    target_num=request.POST['baji']
    if('ebecc7988e3eed1653016aad0e6d90f2'==hl.hexdigest()):
        flag=request.POST['flag']
        Flag(
            target_num=target_num,
            flag_num=flag
        ).save()
        if Status.objects.filter(target_num=target_num)[0].run != 1:
            fraction = Score.objects.filter(flag_num=target_num)[0].fraction -100
            Score.objects.filter(flag_num=target_num).update(fraction=fraction)
            Logs(
                player_num='宕机处罚！',
                flag_num=target_num,
                result= -100
            ).save()

        return HttpResponse('The flag is received!')
    return HttpResponseNotFound
def admin(request):
    message = ['success', '欢迎管理大大的到来']
    if request.POST:
        Status.objects.filter(target_num=request.POST['target_num']).update(run=request.POST['run'])
        message = ['success', '修改成功了呢']
    status_ = Status.objects.all()
    return render(request, 'admin.html', {'status': status_, 'message': message, 'backimg': random.randint(0, 16)})


def admin_table(request):
    message = ['success', '来查看总榜了呢']
    return render(request, 'admin_table.html', {'message': message, 'backimg': random.randint(0, 16)})
