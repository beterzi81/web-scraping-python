from bs4 import BeautifulSoup as soup
import alignment
import sqlite3
import numpy as np

def tokenize(d):
  yield f'<{d.name}>'
  for i in d.contents:
     if not isinstance(i, str):
       yield from tokenize(i)
     else:
       yield from i.split()
  yield f'</{d.name}>'
np.set_printoptions(precision=4)

data=np.array([],dtype=float)

dataArrayFlag=1

databaseConnect = sqlite3.connect('siteler.db')#veritabanına bağlandık
databaseConnect.row_factory = lambda cursor, row: row[0]#bu satırın sebebi şu, id değerlerini döndürmek istediğimizde tuple veri tipinde (12,) şeklinde bir tuple döndürüyordu. bu lambda ile her döndürülen tuple'ın ilk elemanını yani id'mizi alıyor.
cursor = databaseConnect.cursor()#cursorımızı oluşturuk
dbItems = cursor.execute('SELECT id FROM siteler').fetchall()#bütün id değerlerini aldık,
dbItems.sort()#id değerleri sırasız geliyordu sıraladık
for i in dbItems:
  needleResult=[]#bu listede karşılaştırma sonuçlarını düz bir liste halinde tutacağız
  ndarrayElementForNeedleResult=np.array([],dtype=float)#bu ndarray değişkenini, sonuçlarımızı ndarray tipine çevirmek için kullanacağız
  firstHtmlContext=cursor.execute("SELECT dosya_icerigi FROM siteler WHERE id="+str(i)+"").fetchall()#database'i gezerken ihtiyacımız olan içeriği çekiyoruz
  tmp = list(tokenize(soup(str(firstHtmlContext), 'html.parser')))#parsing işlemini yapıp veriyi istediğimiz hale getiriyoruz
  tmp = [item for item in tmp if bool(soup(item, "html.parser").find())]
  firstHtmlContext=tmp#işlemleri yaptıktan sonra anlamlı değişkenimize geçiş yapıyoruz
  for j in dbItems:
    secondHtmlContext=cursor.execute("SELECT dosya_icerigi FROM siteler WHERE id="+str(j)+"").fetchall()
    tmp = list(tokenize(soup(str(secondHtmlContext), 'html.parser')))
    tmp = [item for item in tmp if bool(soup(item, "html.parser").find())]
    secondHtmlContext=tmp
    needleResult.append(alignment.needle(firstHtmlContext,secondHtmlContext))#listemizde karşılaştırma verilerini topluyoruz
  
  finalResult=np.concatenate([needleResult,ndarrayElementForNeedleResult])#burda yapılan işlemin amacı sadece needleResult değişkeninin tipini ndarray olarak tutmak
  if (dataArrayFlag):#tek sefere mahsus array boyutunu eşitlemek için bu işlemi yapmamız gerekiyor çünkü vstack işlemi aynı boyutlu arraylerde yapılabiliyor
    data=finalResult
    dataArrayFlag=0
  else:
    data=np.vstack((data,finalResult))#son olarak da her satırı ana arrayimize ekliyoruz

np.savetxt("similarity_result.txt",data,delimiter=';',fmt='%1.4f')#bir txt dosyası olarak çıktı veriyoruz

