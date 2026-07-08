import requests
import re

# Ana kaynak listemiz (Diğer kanallar için iptv-org'dan çekmeye devam ediyoruz)
KAYNAKLAR = [
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

def cnn_turk_guncel_link_bul():
    """ CNN Türk'ün web sitesindeki o anki aktif tokenli linki bulan fonksiyon """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # CNN Türk'ün canlı yayın sayfasının kaynak kodlarına gidiyoruz
        url = "https://www.cnnturk.com/canli-yayin"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Sayfa kodlarının içinde 'playlist.m3u8?st=' veya 'duhnet.tv' geçen linki arıyoruz
            match = re.search(r'(https://[^"\']+\.m3u8\?[^"\']+)', response.text)
            if match:
                guncel_link = match.group(1).replace("\\/", "/")
                print(f"Başarılı: Güncel CNN Türk Linki Bulundu -> {guncel_link}")
                return guncel_link
    except Exception as e:
        print(f"CNN Türk güncel linki aranırken hata oluştu: {e}")
    
    # Eğer siteden çekemezse yedek olarak senin verdiğin linki döner
    return "https://live.duhnet.tv//S2/HLS_LIVE/cnnturknp/track_4_1000/playlist.m3u8?&live=true&app=com.cnnturk&st=gh1YgWG5Ifcpkn-rXNwCnQ&e=1783535182"

def listeyi_guncelle():
    # En güncel CNN Türk linkini canlı olarak çekiyoruz
    cnn_linki = cnn_turk_guncel_link_bul()

    # Çalma listemizin başına CNN Türk'ü ekliyoruz
    ozel_kanallar = f"""#EXTM3U
#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/0/09/CNN_T%C3%BCrk_logo.png",CNN Türk
{cnn_linki}
"""

    eklenen_linkler = set()
    eklenen_linkler.add(cnn_linki)

    # iptv-org havuzundan diğer tüm Türkiye kanallarını çekiyoruz
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
                                ozel_kanallar += extinf_satiri + "\n" + link_satiri + "\n"
                                eklenen_linkler.add(link_satiri)
                            i += 1
                    i += 1
        except Exception as e:
            print(f"Havuz çekilirken hata oluştu: {e}")

    # Hepsini tek bir m3u dosyasında birleştirip kaydediyoruz
    with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
        f.write(ozel_kanallar.strip())
    print("İşlem başarılı! CNN Türk canlı kazındı ve liste güncellendi.")

if __name__ == "__main__":
    listeyi_guncelle()
