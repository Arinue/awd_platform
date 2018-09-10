import requests
import time
import random
import string


token='woshiwuxudong'
# 红队
baji='311F8A54SV9K6B5FF4EAB20536'
def getFlag():
	return ''.join(random.sample(string.ascii_letters + string.digits, 48))



while(1):
	f=open('./flag','w')
	flag=getFlag()
	f.write(flag)
	data={
	'flag':flag,
	'token':token,
	'baji':baji,
	}
	r=requests.post('http://192.168.1.100/caipanflag/',data=data)
	print(r.text)
	f.close()
	time.sleep(300)