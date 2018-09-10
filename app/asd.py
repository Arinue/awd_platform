s = 'adf'
f = open("/var/www/awd_platform/app/qwe.txt","a")
f.write(s)
f.close

with (open('/var/www/awd_platform/app/qwe.txt', 'r')) as text:
	words = text.read()
n = words.count("33a")
print(n)
