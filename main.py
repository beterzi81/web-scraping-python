import urllib.request
import subprocess
import os
from urllib.parse import urlparse

#########################Linkleri listeye aktarma##########################
#önce linkleri tek tip haline getirmemiz laızm
linkler=[]
f=open('links.txt','r')#linklerin olduğu txt dosyasını açtık
linkSatirSayisi=115
for i in range(0,linkSatirSayisi):
    linkler.append(f.readline())#Her linki bir indexe attık
f.close()
#Artık bütün linklerimizi barındıran bir listemiz var
duzenliLinkler=[]#linklerimizi düzenleyip bu listeye koyacağız
for i in linkler:
    parseLink=urlparse(i)#her linksi parçaladık
    if(parseLink.netloc=="filedn.eu"):#burada bir istisna var, filedn.eu şeklindeki bir link var ve tam link girilmedikçe doğru adrese gitmiyor onun için o istisnayı düzeltiyoruz
        duzenliLinkler.append(i)
    else:
        di=parseLink.scheme+"://"+parseLink.netloc  #scheme ve netloc kısmını :// stringi ile birleştirdiğimizde elimizde tertemiz bir index linki oluyor
        duzenliLinkler.append(di)
#listemizdeki bütün linkleri düzenli hale getirdik.




'''
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

cmd='grep a\ href deneme.html | grep -v index | cut -d \'"\' -f 2'
process2=subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)#o an bakıp belleğe aldığımız htmldeki bütün yönlendirme linklerini bulduk
temp=process2.communicate()[0]
insideLinks=temp.decode()
insideLinksArray=insideLinks.split('\n')#Bu iç linkleri bir arraye atadık
insideLinksArray=list(dict.fromkeys(insideLinksArray))#tekrarlayan değerleri kaldırdık
insideLinksArray= list(filter(None, insideLinksArray))#null yani boş string değerlerini de kaldırdık
#print(insideLinksArray)#bunu yaptığımızda index sayfamızda index hariç bütün referans verilen linkleri buluyor ve index olanları çıkarıyor, ardından da html isimlerini alıyor. bu print de o htmlleri tutan listeyi yazıyor

#Şimdi her iç linke gidip oradaki htmlleri de indirip içinde index'ten ve insideLinksArray'deki linklerden başka link var mı diye bakacağız
os.chdir("/Siteler/muzikdukkanim")
for i in insideLinksArray:
    #os.chdir("/"+i)
    req= urllib.request.urlopen("http://muzikdukkanim.eu5.org" + i)
    test=req.read()
    decoded=test.decode("utf-8")
    txtKeeper=i+".txt"#her html için bir txt uzantılı ad tutuyoruz
    saveFile = open(txtKeeper,'w')
    saveFile.write(str(decoded))
    saveFile.close()
    os.chdir("..")
'''