import time
import hashlib

#url = 'http://cdnlms2.lge.com/mmd/ext/020/E004/2021/06/04/652e0fad-9245-4a5a-bb0c-fb8d9de6f4ec.mp4/manifest.m3u8'
#url = 'https://cdnlms2.lge.com/mmd/ext/020/E004/2021/06/04/652e0fad-9245-4a5a-bb0c-fb8d9de6f4ec.mp4/manifest.m3u8'
url = 'http://cdnlms2.lge.com/int/020/E004/2017/11/12/c9ae36eb-1bc8-44a9-bc61-8990f9d70c8c.mp4/manifest.m3u8'
url = 'https://cdnlms2.lge.com/int/020/E004/2017/11/12/c9ae36eb-1bc8-44a9-bc61-8990f9d70c8c.mp4/manifest.m3u8'
url = 'https://cdnlms2.lge.com/mmd/ext/020/E004/2021/06/04/652e0fad-9245-4a5a-bb0c-fb8d9de6f4ec.mp4/manifest.m3u8'

if url[:5] == 'https':
  p = 24
else:
  p = 23


now = int(time.time())
#timeout = now+60*60*6 # 6 hour
timeout = now+60*60*24*30 # 6 hour
#timeout = now+60*5 # 5min
text = 'cdnlms123%s?p=%i&ci=30&cd=30&e=%i&cf=%i'%(url[:p],p,timeout, timeout)
enc = hashlib.md5()
enc.update(text)
md5 = enc.hexdigest()

url_full = '%s?p=%i&ci=30&cd=30&e=%i&cf=%i&h=%s'%(url, p, timeout, timeout, md5)
print(text)
print(url_full)

