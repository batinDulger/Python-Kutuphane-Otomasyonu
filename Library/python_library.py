import sqlite3
import random
import time

class Library():

    def __init__(self):
        self.Database()
        self.kayitTable()
        self.admin_Table()
        self.kutuphaneTable()
        self.secim()

    def Database(self):

        self.con = sqlite3.connect("Library.db")
        self.cursor = self.con.cursor()

    def kayitTable(self):

        self.cursor.execute("CREATE TABLE IF NOT EXISTS kayit_ogrenci(isim TEXT, soyisim TEXT, e_mail TEXT, sifre TEXT, id INT)")
    
    def admin_Table(self):

        self.cursor.execute("CREATE TABLE IF NOT EXISTS admin_girisi(admin TEXT, sifre TEXT)")

    def kutuphaneTable(self):

        self.cursor.execute("CREATE TABLE IF NOT EXISTS kutuphane_ekle(yazar TEXT, kitap_adi TEXT, Kategori TEXT)")

    def secim(self):

        secim = input("1-) Kayıt ol - 2-) Giriş - 3-) Admin girişi   \n")

        if secim == "1":
            self.Kayit_ol()
        elif secim == "2":
            self.giris()
        elif secim == "3":
            self.admin_girisi()


    def Kayit_ol(self):

        isim = input("İsim:")
        soyisim = input("Soyisim:")
        e_mail = input("Email:")
        sifre = input("Şifre:")
        id = random.randint(100,10000)

        print("Kayıt tamamlandı\nGiriş sayfasına yönlendiriliyorsunuz")
        time.sleep(1)

        def kayit_Table2():

            self.cursor.execute("INSERT INTO kayit_ogrenci VALUES(?,?,?,?,?)",(isim,soyisim,e_mail,sifre,id))
            self.con.commit()

        kayit_Table2()
        self.giris()

    def giris(self):

        e_mail = input("E mail adresi:")
        sifre = input("Şifre:")

        self.cursor.execute("SELECT * FROM kayit_ogrenci WHERE e_mail = ? AND sifre = ?",(e_mail,sifre))

        kullanici = self.cursor.fetchone()

        if(kullanici):
            secim = input("1-) Kitapları Listele - 2-) Yazara göre kitap ara - 3-) Kategoriye göre kitap ara  \n")
            if secim == "1":
                self.listele()
            elif secim == "2":
                self.yazara_gore_ara()
            elif secim == "3":
                self.kategori_kitap()
        else:
            self.giris()

    def listele(self):

        self.cursor.execute("SELECT * FROM kutuphane_ekle")
        kitaplar = self.cursor.fetchall()
        for i in kitaplar():
            print(i[1])

    def yazara_gore_ara(self):

        while True:
            yazar = input("Yazarın adını giriniz:")
            self.cursor.execute("SELECT * FROM kutuphane_ekle WHERE yazar = ?",(yazar,))

            yazar_kitap = self.cursor.fetchall()
            found_books = False  

            for i in yazar_kitap:
                print(i[1])
                found_books = True  

            if not found_books:
                print("Yazar bulunamadı")
                continue
            secim = input("1-) Devam - 2-) Çıkış:\n")
            if secim == "1":
                continue
            elif secim == "2":
                break

    def kategori_kitap(self):

        while True:
            kategori = input("Kategori giriniz:")
            self.cursor.execute("SELECT * FROM kutuphane_ekle WHERE kategori = ?",(kategori,))

            kitaplar = self.cursor.fetchall()
            for kitap in kitaplar:

                print(kitap[1])
            secim = input("1-) Devam - 2-) Çıkış:\n")
            if secim == "1":
                continue
            elif secim == "2":
                break

    def admin_girisi(self):
        while True:
            admin = input("Admin:")
            sifre = input("Şifre:")

            self.cursor.execute("SELECT * FROM admin_girisi WHERE admin = ? AND sifre = ?", (admin, sifre))

            kullanici = self.cursor.fetchone()

            if (kullanici):
                secim = input("1-) Kitap ekle - 2-) Kitap sil - 3-) Kitap güncelle  \n")
                if secim == "1":
                    self.kitap_ekle()
                elif secim == "2":
                    self.kitap_sil()
                elif secim == "3":
                    self.kitap_guncelle()
                break
            else:
                print("Hatalı giriş denemesi")
                self.admin_girisi()


    def kitap_ekle(self):

        while True:
            yazar = input("Yazar: ")
            kitap_adi = input("Kitap adı: ")
            kategori = input("Kategori: ")

            self.cursor.execute("INSERT INTO kutuphane_ekle VALUES(?,?,?)",(yazar,kitap_adi,kategori))
            self.con.commit()

            secim = input("1-) Devam - 2-) Çıkış:\n")
            if secim == "1":
                continue
            elif secim == "2":
                break

    def kitap_sil(self):
        while True:
            self.cursor.execute("SELECT * FROM kutuphane_ekle")
            listele = self.cursor.fetchall()
            for kitap in listele:
                print(kitap[1])
            silinecek = input("Silinecek kitabın adını giriniz:")
            self.cursor.execute("DELETE FROM kutuphane_ekle WHERE kitap_adi = ?",(silinecek,))
            deleted_rows = self.cursor.rowcount

            if deleted_rows > 0:
                print("{} isimli kitap silindi".format(silinecek))
            else:
                print("Aradığınız kitap bulunamadı")
                continue
            secim = input("1-) Devam - 2-) Çıkış:\n")
            if secim == "1":
                continue
            elif secim == "2":
                break

    def kitap_guncelle(self):
        while True:
            guncellenecek_kitap = input("Değiştirilecek kitabın adını giriniz:")
            self.cursor.execute("SELECT * FROM kutuphane_ekle WHERE kitap_adi = ?", (guncellenecek_kitap,))

            kitaplar = self.cursor.fetchall()
            if len(kitaplar) == 0:
                print("Kitap bulunamadı.")
            else:
                for kitap in kitaplar:
                    print("Kitap bulundu")
                    print(kitap[1])

                degistir = input("Hangi kitap ile değiştirmek istersiniz:")
                self.cursor.execute("UPDATE kutuphane_ekle SET kitap_adi = ? WHERE kitap_adi = ?", (degistir, guncellenecek_kitap))
                self.con.commit()
                print("Kitap başarıyla güncellendi.")
                continue
            secim = input("1-) Devam - 2-) Çıkış:\n")
            if secim == "1":
                continue
            elif secim == "2":
                break

Library()