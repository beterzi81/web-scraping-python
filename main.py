linkler=[]
f=open('links.txt','r')#linklerin olduğu txt dosyasını açtık
linkSatirSayisi=115
for i in range(0,linkSatirSayisi):
    linkler.append(f.readline())#Her linki bir indexe attık
f.close()
#Artık bütün linklerimizi barındıran bir listemiz var