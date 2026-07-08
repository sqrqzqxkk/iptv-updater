import requests

# Güncel linkleri aldığınız kaynak adresleri
KAYNAKLAR = [
    "https://example.com/guncel_kaynak1.m3u",
    "https://raw.githubusercontent.com/ornek-kullanici/havuz/main/liste.m3u"
]

def listeyi_guncelle():
    tum_icerik = "#EXTM3U\n"
    
    for url in KAYNAKLAR:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Başlık satırını kaldırarak içeriği ekle
                satirlar = response.text.split("\n")
                for satir in satirlar:
                    if satir.strip() and not satir.startswith("#EXTM3U"):
                        tum_icerik += satir + "\n"
        except Exception as e:
            print(self, f"Hata oluştu ({url}): {e}")

    # Yeni listeyi dosyaya yaz
    with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
        f.write(tum_icerik.strip())

if __name__ == "__main__":
    listeyi_guncelle()
