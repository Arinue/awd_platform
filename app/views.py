#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import Score, Flag, Logs, Status, Flags
import datetime
import random
from django.utils.timezone import utc
from django.db.models import Q

import hashlib

Year, month, day,Hour, Minute, Second = 2018,9,29,22,20,20  #在此设置比赛结束的时间 年月日时分秒

def dict2list(dic:dict):
    ''' 将字典转化为列表 '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst

# Create your views here.

def index(request):
    utcnow = datetime.datetime.now()
    log = -3
    message = ['success', '欢迎来到提交平台']  # "Success Message" "success"
    ti = datetime.datetime(Year, month, day,Hour, Minute, Second)	
    if utcnow > ti:
        log = -4 
        message = "warning", "比赛已结束！" 
    elif log !=-4 and request.POST:
        """ log:1:数据正确  log:0:flag错误    log:-1:用户错误     log:-2:flag过期   log:-3:未提交flag
        """

        # 判断是否正确用户
        score_now=0
        tok = request.POST['token']
        flag = request.POST['flag']
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
                for i in Flags.objects.all():
                    if tok+flag != i.player_num +i.flag_num:
                        if log==1:
                            score_now = 100
                        elif log == -4:
                            score_now = 0
                    else:
                        log=-2
                        score_now = 0
                #for i in Flags.objects.all():
                if not Flags.objects.filter(flag_num=flag):
                    fraction = Score.objects.filter(flag_num=Flag.objects.filter(flag_num=request.POST['flag'])[0].target_num)[0].fraction -100
                    Score.objects.filter(flag_num=Flag.objects.filter(flag_num=request.POST['flag'])[0].target_num).update(fraction=fraction)
                Flags(
                         player_num = request.POST['token'],
                         flag_num = request.POST['flag']
                ).save()
            else:
                log=0
            fraction = Score.objects.filter(flag_num=request.POST['token'])[0].fraction + score_now
            Score.objects.filter(flag_num=request.POST['token']).update(fraction=fraction)
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
            message = "warning", "flag错误"
        elif log == 1:
            message = "success", "恭喜，获得100分！"
        elif log == -2:
            message = "warning", "flag过期啦！再去拿一个吧！"
        elif log == -4:
            message = "warning", "不允许提交自己的flag，第二次扣100分！"
    return render(request, 'index.html', {'message': message, 'Year':Year, 'month':month, 'day':day,'Hour':Hour, 'Minute':Minute, 'Second':Second,'mess': None, 'backimg': random.randint(0, 4)})


def score(request):
    message = ['success', '来查看总榜了呢']
    return render(request, 'table.html', {'message': message,'Year':Year, 'month':month, 'day':day,'Hour':Hour, 'Minute':Minute, 'Second':Second, 'backimg': random.randint(0, 4)})


def api1(request):
    htmls = ''
    html = {}
    for i in Status.objects.all():
        s = Score.objects.filter(player_num=i.player_num)[0]
        if i.run == 0:
            r = '<font face="arial" color="#FF0000">已宕机</font>'
        else:
            r = '<font face="arial" color="#00FF00">运行正常</font>'
        html[i.player_num] =[int(s.fraction),r]
    htm = sorted(dict2list(html), key=lambda x:x[1], reverse=True) # 按照第1个元素降序排列
    j = 1
    for i in htm:
        if j==1:
            t = str(j)
            htmls += """<tr><td><font face = "行楷" size="6" color="#ffff00">第{}名</font></td><td><font size="6" color="#ffff00">{}</font></td><td>{}</td><td>{}</td></tr>""".format(t,i[0],'&ensp;'+str(i[1][0]),i[1][1])
            j += 1
            continue
        if j==2:
            t = str(j)
            htmls += """<tr><td><font size="5" color="#c0c0c0">&ensp;第{}名</font></td><td><font size="5" color="#c0c0c0">{}</font></td><td>{}</td><td>{}</td></tr>""".format(t,i[0],'&ensp;'+str(i[1][0]),i[1][1])
            j += 1
            continue
        if j==3:
            t = str(j)
            htmls += """<tr><td><font size="4" color="#b87333">&emsp;第{}名</font></td><td><font size="4" color="#b87333">{}</font></td><td>{}</td><td>{}</td></tr>""".format(t,i[0],'&ensp;'+str(i[1][0]),i[1][1])
            j += 1
            continue
        else:
            t = str(j)
            htmls += "<tr><td>&emsp;第{}名</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(t,i[0],'&ensp;'+str(i[1][0]),i[1][1])
            j += 1  
    return HttpResponse(htmls)



def api2(request):
    html = ''
    if 'Arinue' not in request.META['HTTP_REFERER']:
        for i in Logs.objects.filter(Q(result=100) | Q(result=-100))[::-1][0:10]:
            if '宕机' in i.player_num:
                be_hacked=Status.objects.filter(target_num=i.flag_num)[0].player_num
                html += """<tr><td><font face="arial" color="#FFC107">{}</font></td><td><font face="arial" color="#FFC107">{}</font></td><td>{}</td><td><font size="5" face="arial" color="#FF0000">{}</font></td></tr>""".format(
                i.player_num,
                be_hacked,
                i.last,
                i.result
                )
            else:
                be_hacked=Status.objects.filter(target_num=Flag.objects.filter(flag_num=i.flag_num)[0].target_num)[0].player_num
                html += """<tr><td><font face="arial" color="#00FF00">{}</font></td><td><font face="arial" color="#FF0000">{}</font></td><td>{}</td><td><font size="5" face="arial" color="#00FF00">{}</font></td></tr>""".format(
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
    utcnow = datetime.datetime.now()
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
    if('9ae4b5837377c159d8b898f44d8740ef'==hl.hexdigest()):
        flag=request.POST['flag']
        Flag(
            target_num=target_num,
            flag_num=flag
        ).save()
        if Status.objects.filter(target_num=target_num)[0].run != 1:
            fraction = Score.objects.filter(flag_num=target_num)[0].fraction -100
            Score.objects.filter(flag_num=target_num).update(fraction=fraction)
            Logs(
                player_num='系统提示：服务器宕机！',
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


