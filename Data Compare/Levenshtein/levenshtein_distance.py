from Levenshtein import distance
import numpy as np
import sqlite3

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
  for j in dbItems:
    secondHtmlContext=cursor.execute("SELECT dosya_icerigi FROM siteler WHERE id="+str(j)+"").fetchall()
    needleResult.append(distance(firstHtmlContext,secondHtmlContext))#listemizde karşılaştırma verilerini topluyoruz
    print(i,j)
  finalResult=np.concatenate([needleResult,ndarrayElementForNeedleResult])#burda yapılan işlemin amacı sadece needleResult değişkeninin tipini ndarray olarak tutmak
  if (dataArrayFlag):#tek sefere mahsus array boyutunu eşitlemek için bu işlemi yapmamız gerekiyor çünkü vstack işlemi aynı boyutlu arraylerde yapılabiliyor
    data=finalResult
    dataArrayFlag=0
  else:
    data=np.vstack((data,finalResult))#son olarak da her satırı ana arrayimize ekliyoruz

#np.savetxt("similarity_result.txt",data,delimiter=';')
#bir txt dosyası olarak çıktı veriyoruz
print(data)

