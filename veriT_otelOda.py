import sqlite3



class oda:
    odaBilgileri=[]
    def __init__(self,odaNo,kisiSayisi,musaitlik):
        self.odaNo=odaNo
        self.kisiSayisi=kisiSayisi
        self.musaitlik=musaitlik
        self.odaBilgileri.append(self)
    
    def bilgiYazdir(self):
        print("Oda numarasi: {}, kisi sayisi: {}, musait mi? : {}".format(self.odaNo,self.kisiSayisi,self.musaitlik))

    @classmethod
    def odalariYazdir(cls):
        for i in cls.odaBilgileri:
            i.bilgiYazdir()


class veritabaniBaglanti:
    def __init__(self,veritabani,tablo):
        self.veritabani=sqlite3.connect(veritabani)
        self.tabloAdi=tablo
        self.imlec=self.veritabani.cursor()
        self.imlec.execute("CREATE TABLE IF NOT EXISTS {}(OdaNo INTEGER PRIMARY KEY AUTOINCREMENT,KisiSayisi INTEGER NOT NULL,OdaMusaitlik INTEGER)".format(self.tabloAdi))

    def odalariGetir(self):
        self.imlec.execute("SELECT * FROM {}".format(self.tabloAdi))
        oda.odaBilgileri.clear()
        for i in self.imlec:
            oda(i[0],i[1],i[2])
    def OdaEkle(self,oda,kisi,mus):
        self.imlec.execute("INSERT INTO {}(OdaNo,KisiSayisi,OdaMusaitlik) VALUES({},{},{})".format(self.tabloAdi,oda,kisi,mus))
        self.veritabani.commit()
        self.odalariGetir()
    def OdaRezerve(self,no):
        kontrol=0
        self.imlec.execute("SELECT OdaNo FROM {}".format(self.tabloAdi))
        for a in self.imlec:
            if a[0]==no:
                kontrol=1
                break

        if kontrol==1:
            self.imlec.execute("SELECT OdaMusaitlik FROM {} WHERE OdaNo={}".format(self.tabloAdi,no))
            if self.imlec.fetchone()[0]==1:
                self.imlec.execute("UPDATE {} SET OdaMusaitlik=0 WHERE OdaNo={}".format(self.tabloAdi,str(no)))
                self.veritabani.commit()
                self.odalariGetir()
                print("Oda rezerve edildi.")
            else:
                print("Oda musait degildir!!!")
        else:
            print("Oda bulunamadi!")
    
    def OdaCikis(self,no):
        kontrol=0
        self.imlec.execute("SELECT OdaNo FROM {}".format(self.tabloAdi))
        for a in self.imlec:
            if a[0]==no:
                kontrol=1
                break

        if kontrol==1:
            self.imlec.execute("SELECT OdaMusaitlik FROM {} WHERE OdaNo={}".format(self.tabloAdi,no))
            if self.imlec.fetchone()[0]==0:
                self.imlec.execute("UPDATE {} SET OdaMusaitlik=1 WHERE OdaNo={}".format(self.tabloAdi,str(no)))
                self.veritabani.commit()
                self.odalariGetir()
                print("Oda cikisi yapildi.")
            else:
                print("Oda zaten bostur!!!")
        else:
            print("Oda bulunamadi!")

    def OdaAra(self,kisi):
        self.imlec.execute("SELECT * FROM {} WHERE KisiSayisi={} and OdaMusaitlik=1".format(self.tabloAdi,kisi))
        for a in self.imlec:
            print("Oda numarasi: {}, kisi sayisi: {}, musaitlik : musait".format(a[0],a[1]))




       

vt1=veritabaniBaglanti("veriOtel.db","Odalar")
vt1.odalariGetir()
oda.odalariYazdir()
vt1.OdaRezerve(18)
vt1.OdaCikis(16)
vt1.OdaAra(3)
