import urllib.request
from bs4 import BeautifulSoup
import subprocess
import os
from urllib.parse import urlparse
import re

#########################Gerekli fonksiyonların tanımlanması##########################
def lineCounter(filename):#Parametreyle verilen dosyanın satır sayısını bulan fonksiyon 
    file = open(filename, "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    return line_count
def start():
    try:
        os.mkdir("Siteler")  
        print("Gerekli klasörler oluşturuldu!")
    except FileExistsError:
        print("Gerekli klasörler zaten mevcut, işleme devam ediliyor.")
#########################Linkleri listeye aktarma##########################
#önce linkleri tek tip haline getirmemiz laızm
start()
linkler=[]
f=open('links.txt','r')#linklerin olduğu txt dosyasını açtık
linkSatirSayisi=lineCounter("links.txt")
for i in range(0,linkSatirSayisi):
    linkler.append(f.readline())#Her linki bir indexe attık
f.close()
#Artık bütün linklerimizi barındıran bir listemiz var
duzenliLinkler=[]#linklerimizi düzenleyip bu listeye koyacağız
for i in linkler:
    parseLink=urlparse(i)#her linki parçaladık
    if(re.search(r'filedn.eu',i) or re.search(r'codesque.github.io',i) or re.search(r'orgfree.com',i)) :#burada bir istisna var, filedn.eu şeklindeki bir link var ve tam link girilmedikçe doğru adrese gitmiyor onun için o istisnayı düzeltiyoruz.ikinci istisna da github.io linklerinde, onu da düzelttik. son olarak orgfree linklerinde de bazı sorunlar çıkıyordu onları da bütün şekilde almak zorunda kaldığımız için onu da ekledik
        duzenliLinkler.append(i)
    else:
        di=parseLink.scheme+"://"+parseLink.netloc  #scheme ve netloc kısmını :// stringi ile birleştirdiğimizde elimizde tertemiz bir index linki oluyor
        duzenliLinkler.append(di)
#listemizdeki bütün linkleri düzenli hale getirdik.

#########################Klasörleri oluşturma##########################
'''
Yorum satırıyla yazılan kısım güncellemeden önceki bash komutu kullanılarak işi yapan kısımdır, artık aynı işi bir python kütüphanesiyle yazarak daha gelişmiş bir uyumluluk sağlıyoruz

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
klasorIsimleri=[]
for i in duzenliLinkler:
    parseLink=urlparse(i)
    klasorIsimleri.append(parseLink.netloc)
for i in klasorIsimleri:
    try:
        os.mkdir("Siteler/"+i)  
        print(i+" adlı klasör oluşturuldu! ")
    except FileExistsError:
        print(i+ " adlı klasör zaten mevcut!")


#########################Linklere gidip html içeriğini alma##########################
#os.chdir("Indirilebilen-htmller")#deneme için şimdilik indirmeleri buraya yapıyoruz
#sayac=0#bu da tamamen şimdilik indirebilen htmlleri adlandırmak için koyulmuş bir sayaç
cwd=os.getcwd()
klasorIsimleriIterator=0
for i in duzenliLinkler:
    req = urllib.request.Request(i, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    requestingHTML= urllib.request.urlopen(req).read()
    decodedHTML=requestingHTML.decode("utf-8",errors='ignore')#bu şekilde yazınca 8. linkte UnicodeDecodeError: 'utf-8' codec can't decode byte 0xdd in position 114: invalid continuation byte hatası alıyorum(bu hatayı, decode fonksiyonunun içinde errors='ignore' parametresi vererek çözdüm)     
    # ayrıca bu kodla çalıştırınca da 32. sitede urllib.error.HTTPError: HTTP Error 403: Forbidden hatası alıyorum,hatanın sebebi doğru link ayrıştırmasını yapamamammış onu da hallettim
    
    
    indx="index.html"
    os.chdir(cwd+"/Siteler/"+klasorIsimleri[klasorIsimleriIterator])
    saveFile = open(indx,"w")
    saveFile.write(str(decodedHTML))
    saveFile.close()
    klasorIsimleriIterator+=1
    #yukardaki cwd değişkeni tanımlamasından bu yorum satırına kadar olan kısım artık bir simülasyon değil gerçek bir çalışma halinde. bütün linklerden gelen index.html içeriği ilgili klasöre index.html adı altında oluşturulup kaydediliyor.

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