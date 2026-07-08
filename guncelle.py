import requests
import re

# Ana kaynak listemiz (Diğer ulusal kanalları buradan çekeceğiz)
KAYNAKLAR = [
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

# -------------------------------------------------------------------------
# SADECE HAVUZDAN ÇEKİLECEK DİĞER ULUSAL KANALLARIN TAM ADLARI:
# TRT Spor ve CNN Türk'ü yukarıda özel kazıdığımız için bu listeden çıkardık.
# -------------------------------------------------------------------------
TUTULACAK_KANALLAR = [
    "TRT 1 (1080p)",
    "ATV (1080p)",
    "Kanal D (1080p)",
    "NOW TV (720p)",
    "Beyaz TV (1080p)",
    "Kanal 7 (1080p) [Not 24/7]",
    "TV 8 (1080p)",
    "EuroStar TV (1080p)",
    "TRT Haber (720p)",
    "A Haber (1080p)",
    "Habertürk TV (1080p)",
    "NTV (720p) [Not 24/7]",
    "ATV Avrupa (576p) [Not 24/7]",
    "Euro D (720p)",
    "A2TV (1080p)",
    "A Spor (1080p)",
    "TRT Belgesel (720p)"
]

def cnn_turk_guncel_link_bul():
    """ CNN Türk sitesinden o anki şifreli güncel linki bulur """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        url = "https://www.cnnturk.com/canli-yayin"
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            match = re.search(r'(https://[^"\']+\.m3u8\?[^"\']+)', response.text)
            if match:
                return match.group(1).replace("\\/", "/")
    except Exception as e:
        print(f"CNN Türk güncel linki aranırken hata oluştu: {e}")
    return "https://live.duhnet.tv//S2/HLS_LIVE/cnnturknp/track_4_1000/playlist.m3u8?&live=true&app=com.cnnturk&st=gh1YgWG5Ifcpkn-rXNwCnQ&e=1783535182"

def trt_spor_guncel_link_bul():
    """ TRT Spor sitesinden o anki şifreli güncel daioncdn linkini bulur """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        url = "https://www.trtspor.com.tr/canli-yayin-izle/trt-spor"
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            match = re.search(r'(https://trt\.daioncdn\.net/[^"\']+\.m3u8\?[^"\']+)', response.text)
            if match:
                return match.group(1).replace("\\/", "/")
    except Exception as e:
        print(f"TRT Spor güncel linki aranırken hata oluştu: {e}")
    return "https://trt.daioncdn.net/trtspor/master_720p.m3u8?platform=trtspor&sid=8kbjje2e022o&app=9b65474e-8197-4899-aabb-321fcf6dd9eb&ce=2"

def listeyi_guncelle():
    # Sitelerden en taze dinamik linkleri çekiyoruz
    cnn_linki = cnn_turk_guncel_link_bul()
    trt_spor_linki = trt_spor_guncel_link_bul()

    # TRT Spor ve CNN Türk'ü listenin en tepesine jilet gibi ekliyoruz
    ozel_kanallar = f"""#EXTM3U
#EXTINF:-1 tvg-id="TRTSpor.tr" tvg-name="TRT Spor" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/e/ec/TRT_Spor_logo.png",TRT Spor
{trt_spor_linki}
#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/0/09/CNN_T%C3%BCrk_logo.png",CNN Türk
{cnn_linki}
"""
    # Mükerrer eklemeyi önlemek için hafızaya alıyoruz
    eklenen_linkler = set([cnn_linki, trt_spor_linki])

    # Diğer ulusal kanalları havuzdan süzerek altına ekliyoruz
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
                                kanal_adi_bul = extinf_satiri.split(",")[-1].strip().lower()
                                
                                tutulsun_mu = False
                                for ana_kanal in TUTULACAK_KANALLAR:
                                    if ana_kanal.strip().lower() == kanal_adi_bul:
                                        tutulsun_mu = True
                                        break
                                
                                if tutulsun_mu:
                                    ozel_kanallar += extinf_satiri + "\n" + link_satiri + "\n"
                                    eklenen_linkler.add(link_satiri)
                                
                            i += 1
                    i += 1
        except Exception as e:
            print(f"Havuz çekilirken hata oluştu: {e}")

    # Hepsini tek bir dosyaya yazıp kaydediyoruz
    with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
        f.write(ozel_kanallar.strip())
    print("İşlem başarılı! Liste tamamen güncellendi ve eksikler kapatıldı.")

if __name__ == "__main__":
    listeyi_guncelle()
