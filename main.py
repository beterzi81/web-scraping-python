import pwd
from re import sub
from bs4 import BeautifulSoup
import requests
import urllib.request
import sys
import subprocess
'''
#########################Linkleri listeye aktarma##########################
linkler=[]
f=open('links.txt','r')#linklerin olduğu txt dosyasını açtık
linkSatirSayisi=115
for i in range(0,linkSatirSayisi):
    linkler.append(f.readline())#Her linki bir indexe attık
f.close()
#Artık bütün linklerimizi barındıran bir listemiz var
f=open("htmller.txt",'w')
for i in linkler:
    print(i)
    request_url = urllib.request.urlopen(i)
    f.write(str(request_url))
    f.write('\n')
f.close()
#########################Klasörleri oluşturma##########################
#cat links.txt | cut -d "." -f 1 | cut -d "/" -f 3
cmd = "cat links.txt | cut -d '.' -f 1 | cut -d '/' -f 3"#links.txt dosyasındaki linklerin isimlendirmeye uygun kısımlarını kestik
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
temp = process.communicate()[0]
isim=temp.decode()#bytes türünde dönen isimlendirmede kullanılacak kısımlar stringe dönüştürüldü
isimArray=isim.split('\n')#string türünden string array türüne dönüştürüldü
for i in isimArray:#her isim için aynı adda bir klasör oluşturuldu,1 kez yapılmalı
    command = "cd /Users/beterzi/Desktop/Web-Scraping/Siteler; mkdir " + i
    subprocess.run(command, capture_output=True, shell=True)
'''
#########################Linklere gidip html içeriğini alma##########################
'''
r= urllib.request.urlopen("http://muzikdukkanim.eu5.org")
test=r.read()
a=test.decode("utf-8")
saveFile = open('htmller.txt','w')
saveFile.write(str(a))
saveFile.close()
'''
cmd='grep a\ href deneme.html | grep -v index | cut -d \'"\' -f 2'
process2=subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)#o an bakıp belleğe aldığımız htmldeki bütün yönlendirme linklerini bulduk
temp=process2.communicate()[0]
insideLinks=temp.decode()
insideLinksArray=insideLinks.split('\n')#Bu iç linkleri bir arraye atadık

for i in insideLinksArray:
    req= urllib.request.urlopen("http://muzikdukkanim.eu5.org")
    test=req.read()
    decoded=test.decode("utf-8")
    saveFile = open('htmller.txt','w')
    saveFile.write(str(decoded))
    saveFile.close()