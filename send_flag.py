#coding=utf-8
import requests,time
from datetime import datetime
import random
import string
import hashlib

token='Arinue1?'
# 红队
baji='311F8A54SV9K6B5FF4EAB20536'
def getFlag():
	#return ''.join(random.sample(string.ascii_letters + string.digits, 48))
	
	m = hashlib.md5(''.join(random.sample(string.ascii_letters + string.digits, 48)).encode(encoding="utf-8")).hexdigest()
	return m

ti = datetime(2018,9,13,19,11)#设置开始发送flag的时间
while True:
	if datetime.now()>=ti:
		while(1):
			f=open('flag','w')
			flag=getFlag()
			f.write(flag)
			data={
			'flag':flag,
			'token':token,
			'baji':baji,
			}
			r=requests.post('http://127.0.0.1:8000/caipanflag/',data=data)
			print(r.text)
			f.close()
			time.sleep(300)
	else:
		time.sleep(5)
	
