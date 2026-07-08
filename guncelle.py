import requests

# -------------------------------------------------------------
# YÖNTEM A: HAZIR VE GÜNCEL TÜRK KANALLARI HAVUZLARI
# Sistem her saat bu linklere gidip en taze TRT, CNN Türk vb. linklerini toplar.
# -------------------------------------------------------------
KAYNAKLAR = [
    # Dünyanın en büyük IPTV topluluğunun sadece Türkiye kanalları havuzu (Sürekli yenilenir)
    "https://iptv-org.github.io/iptv/countries/tr.m3u", 
    
    # Gönüllülerin sürekli güncel tuttuğu bir diğer popüler Türk kanalları listesi
    "https://raw.githubusercontent.com/suphero/IPTV/master/TR.m3u8"
]

def listeyi_guncelle():
    # Çalma listesinin başlangıç etiketi
    tum_icerik = "#EXTM3U\n"
    eklenen_linkler = set() # Aynı linklerin mükerrer eklenmesini önlemek için
    
    for url in KAYNAKLAR:
        try:
            print(f"Kaynak okunuyor: {url}")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                satirlar = response.text.split("\n")
                
                # M3U formatında bir kanal iki satırdan oluşur: #EXTINF ve URL satırı
                # Bu yüzden satırları düzgünce eşleştirerek okuyoruz
                i = 0
                while i < len(satirlar):
                    satir = satirlar[i].strip()
                    
                    # Eğer satır #EXTINF (kanal ismi ve logosu içeren satır) ile başlıyorsa
                    if satir.startswith("#EXTINF"):
                        extinf_satiri = satir
                        # Bir sonraki satır yayın linkidir
                        if i + 1 < len(satirlar):
                            link_satiri = satirlar[i+1].strip()
                            
                            # Link boş değilse ve daha önce eklenmediyse listeye ekle
                            if link_satiri and link_satiri not in eklenen_linkler and not link_satiri.startswith("#"):
                                tum_icerik += extinf_satiri + "\n" + link_satiri + "\n"
                                eklenen_linkler.add(link_satiri)
                            i += 1 # Link satırını geçtiğimiz için indexi artır
                    i += 1
                print(f"Başarılı: {url} kaynağından güncel kanallar alındı.")
        except Exception as e:
            print(f"Hata oluştu, bu kaynak atlandı ({url}): {e}")

    # Toplanan tüm taze linkleri senin ana dosyana yazar
    with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
        f.write(tum_icerik.strip())
    print("İşlem tamamlandı! iptv_listem.m3u güncellendi.")

if __name__ == "__main__":
    listeyi_guncelle()
