import requests
import re

# Ana kaynak listemiz
KAYNAKLAR = [
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

# -------------------------------------------------------------------------
# SADECE İZLEMEK İSTEDİĞİN ANA KANALLARI BURAYA YAZ kanka:
# Buraya yazmadığın bütün gereksiz kanallar otomatik olarak SİLİNECEKTİR.
# Kelimeyi nasıl yazarsan yaz (küçük/büyük harf fark etmez) bot yakalar.
# -------------------------------------------------------------------------
TUTULACAK_KANALLAR = [
    "TRT 1",
    "ATV",
    "Kanal D",
    "NOW TV",
    "Show TV",
    "Beyaz TV",
    "Kanal 7",
    "TV8",
    "Star TV",
    "360 TV"
    "TV 100",
    "TRT Haber",
    "CNN Türk",
    "A Haber",
    "Habertürk",
    "NTV",
    "ATV Avrupa",
    "Euro D",
    "A2",
    "teve2"
    "TRT Spor",
    "A Spor",
    "TRT Belgesel"
]

def cnn_turk_guncel_link_bul():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        url = "https://www.cnnturk.com/canli-yayin"
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            match = re.search(r'(https://[^"\']+\.m3u8\?[^"\']+)', response.text)
            if match:
                return match.group(1).replace("\\/", "/")
    except Exception as e:
        print(f"CNN Türk güncel linki aranırken hata oluştu: {e}")
    return "https://live.duhnet.tv//S2/HLS_LIVE/cnnturknp/track_4_1000/playlist.m3u8?&live=true&app=com.cnnturk&st=gh1YgWG5Ifcpkn-rXNwCnQ&e=1783535182"

def listeyi_guncelle():
    cnn_linki = cnn_turk_guncel_link_bul()

    # CNN Türk'ü her halükarda listenin en başına ekliyoruz
    ozel_kanallar = f"""#EXTM3U
#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/0/09/CNN_T%C3%BCrk_logo.png",CNN Türk
{cnn_linki}
"""

    eklenen_linkler = set()
    eklenen_linkler.add(cnn_linki)

    for url in KAYNAKLAR:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                satirlar = response.text.split("\n")
                
                i = 0
                while i < len(satirlar):
                    satir = satirlar[i].strip()
                    if satir.startswith("#EXTINF"):
                        extinf_satiri = satir
                        if i + 1 < len(satirlar):
                            link_satiri = satirlar[i+1].strip()
                            
                            if link_satiri and link_satiri not in eklenen_linkler and not link_satiri.startswith("#"):
                                
                                # Sadece izin verdiğimiz kanallar mı diye kontrol ediyoruz
                                tutulsun_mu = False
                                for ana_kanal in TUTULACAK_KANALLAR:
                                    if ana_kanal.lower() in extinf_satiri.lower():
                                        tutulsun_mu = True
                                        break
                                
                                # Eğer izin verdiğimiz listedeyse dosyaya ekle
                                if tutulsun_mu:
                                    ozel_kanallar += extinf_satiri + "\n" + link_satiri + "\n"
                                    eklenen_linkler.add(link_satiri)
                                
                            i += 1
                    i += 1
        except Exception as e:
            print(f"Havuz çekilirken hata oluştu: {e}")

    with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
        f.write(ozel_kanallar.strip())
    print("İşlem başarılı! Sadece seçtiğin kanallardan oluşan temiz liste hazırlandı.")

if __name__ == "__main__":
    listeyi_guncelle()
