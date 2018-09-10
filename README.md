# Sc0de_awd_platform



一个awd攻防比赛的裁判平台。

版本：beta v1.0
开发语言：python + django


平台分为两个部分

1. 裁判机
2. 靶机

通过特定接口，来实现靶机flag与服务器的通信




## 搭建流程


### 裁判机
1. 安装所需环境 裁判机：python+django
2. 全局搜索woshiguanliyuan，并修改为随机字符串，此处为管理平台地址

/untitled/urls.py
```python
    path('woshiguanliyuan/',views.admin,name='admin'),
    path('woshiguanliyuan/table/',views.admin_table,name='admin_table'),
```

/app/views.py
``` python
    if 'woshiguanliyuan' not in request.META['HTTP_REFERER']:
```

3. 修改app/management/commands/init.py，添加用户

```python
#['用户名','用户靶机token','用户靶机token']
user=[
        ['123456','FF9C92C7SDFABB71566F73422C','FF9C92C7SDFABB71566F73422C'],
        ['aaabbb','311F8A54SV9K6B5FF4EAB20536','311F8A54SV9K6B5FF4EAB20536']
    ]
```

4. 修改/app/views.py第行d89f33b18ba2a74cd38499e587cb9dcd为靶机中设置的admin_token值的md5

```python
    if('d89f33b18ba2a74cd38499e587cb9dcd'==hl.hexdigest()):
```

5. 运行

```shell

python manage.py init

python manage.py manage.py runserver --insecure

```
### 靶机
1. 安装所需环境  靶机：python+requests
2. 修改send_flag.py参数，并将其放入靶机，设权限700。
3. 靶机 `sudo python send_flag.py`。

靶机生成flag脚本，send_flag.py

```python
import requests
import time
import random
import string

#admin的token值，请务必修改复杂一点
token='woshiadmin'

# baji的token值
baji='311F8A54SV9K6B5FF4EAB20536'
def getFlag():
	return ''.join(random.sample(string.ascii_letters + string.digits, 48))

while(1):
	f=open('./flag','w')
	flag=getFlag()
	f.write(flag)
    f.close()
	data={
	'flag':flag,
	'token':token,
	'baji':baji,
	}
	r=requests.post('http://192.168.1.100/caipanflag/',data=data)
	print(r.text)
	time.sleep(300)

```

## 重要须知

最后，由于项目比较急，所以存在好多问题，勉强可以用。不建议大家使用！
数据库这一块，真的自己也很无奈，后期肯定会大改，这个只是一个beta版。后期会逐渐优化。