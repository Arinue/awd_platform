#coding=utf-8
"""
check所有靶机，判断是否宕机并发送到系统进行扣分操作
"""
import requests,time

ip = [183]	#设置所有靶机ip
port = "80" #靶机端口
url = "http://192.168.1."
admin_url = 'http://192.168.1.183/Arinue+2-1/'
target_num = {183:'311F8A54SV9K6B5FF4EAB20536'} #设置所有靶机ip和对应靶机token

headers = {
'Content-Type':'application/x-www-form-urlencoded',

         }
while (1):
    for i in ip:
        re = requests.get(url+str(i)+':'+port)
        if re.status_code != 200:
            data = {'target_num':target_num[i],'run':'0'}
            r = requests.post(admin_url,data=data,headers=headers)
        else:
            data = {'target_num':target_num[i],'run':'1'}
            r = requests.post(admin_url,data=data,headers=headers)
            print("宕机地址：192.168.1."+str(i))
            time.sleep(20)
