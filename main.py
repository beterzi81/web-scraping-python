from base64 import encode
from distutils import errors
import urllib.request
import subprocess
import os
from urllib.parse import urlparse
import re

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
    parseLink=urlparse(i)#her linki parçaladık
    if(parseLink.netloc=="filedn.eu" or  parseLink.netloc=="codesque.github.io") :#burada bir istisna var, filedn.eu şeklindeki bir link var ve tam link girilmedikçe doğru adrese gitmiyor onun için o istisnayı düzeltiyoruz.ikinci istisna da github.io linklerinde, onu da düzelttik
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
os.chdir("Indirilebilen-htmller")#deneme için şimdilik indirmeleri buraya yapıyoruz
sayac=0#bu da tamamen şimdilik indirebilen htmlleri adlandırmak için koyulmuş bir sayaç
for i in duzenliLinkler:
    r= urllib.request.urlopen(i)
    test=r.read()
    a=test.decode("utf-8",errors='ignore')#bu şekilde yazınca 8. linkte UnicodeDecodeError: 'utf-8' codec can't decode byte 0xdd in position 114: invalid continuation byte hatası alıyorum(bu hatayı, decode fonksiyonunun içinde errors='ignore' parametresi vererek çözdüm)     
    # ayrıca bu kodla çalıştırınca da 32. sitede urllib.error.HTTPError: HTTP Error 403: Forbidden hatası alıyorum
    #45-50 arası siteleri indirebiliyor muyum denemek için yazıldı simüle satırları onlar. normalde hepsini kendi klasörüne indireceğim
    
    temp=str(sayac)+".html"
    sayac+=1
    saveFile = open(temp,"w")
    saveFile.write(str(a))
    saveFile.write("*"*125)
    saveFile.close()
'''
    cmd='grep a\ href deneme.html | grep -v index | cut -d \'"\' -f 2'
    process2=subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)#o an bakıp belleğe aldığımız htmldeki bütün yönlendirme linklerini bulduk
    temp=process2.communicate()[0]
    insideLinks=temp.decode()
    unfilteredInsideLinks=insideLinks.split('\n')
    
    FilteredInsideLinksArray=[]
    
    for i in unfilteredInsideLinks:
        if re.search(r'[.]html$',i):
            FilteredInsideLinksArray.append(i)

    #Bu iç linklerin html uzantılı olanlarını bir arraye atadık çünkü arada youtube linkleri de olabiliyor, ilerde alt sayfaları gezmeye çalışırken sorun olacaktır
    FilteredInsideLinksArray=list(dict.fromkeys(FilteredInsideLinksArray))#tekrarlayan değerleri kaldırdık
    FilteredInsideLinksArray= list(filter(None, FilteredInsideLinksArray))#null yani boş string değerlerini de kaldırdık
    #print(FilteredInsideLinksArray)#bunu yaptığımızda index sayfamızda index hariç bütün referans verilen linkleri buluyor ve index olanları çıkarıyor, ardından da html isimlerini alıyor. bu print de o htmlleri tutan listeyi yazıyor

    #Şimdi her iç linke gidip oradaki htmlleri de indirip içinde index'ten ve insideLinksArray'deki linklerden başka link var mı diye bakacağız
    os.chdir("/Siteler")
    for j in FilteredInsideLinksArray:
        os.chdir("/"+j)
        req= urllib.request.urlopen(i + "/" + j)
        test=req.read()
        decoded=test.decode("utf-8")
        txtKeeper=j+".html"#her html için bir ad tutuyoruz
        saveFile = open(txtKeeper,'w')
        saveFile.write(str(decoded))
        saveFile.close()
        os.chdir("..")
'''