import requests
import re

# Ana kaynak listemiz
KAYNAKLAR = [
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

# -------------------------------------------------------------------------
# SADECE HAVUZDAN ÇEKİLECEK DİĞER KANALLAR
# TRT 1, TRT Spor ve CNN Türk'ü özel kazıdığımız için bu listeden çıkardık.
# -------------------------------------------------------------------------
TUTULACAK_KANALLAR = [
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
    "TRT Belgesel (720p)",
    "A2TV (1080p)",
    "Euro D (720p)",
    "ATV Avrupa (576p) [Not 24/7]"
]

def trt1_guncel_link_bul():
    """ TRT 1 sitesinden yurt dışı engelini aşan güncel m3u8 linkini kazır """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        # TRT'nin resmi canlı yayın izleme sayfası
        url = "https://www.trtizle.com/canli/tv/trt-1"
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            # Sayfa kaynağındaki daioncdn m3u8 linkini arıyoruz
            match = re.search(r'(https://trt\.daioncdn\.net/trt1/[^"\']+\.m3u8\?[^"\']+)', response.text)
            if match:
                print("Başarılı: Yurt dışı uyumlu TRT 1 Linki Bulundu.")
                return match.group(1).replace("\\/", "/")
    except Exception as e:
        print(f"TRT 1 canlı linki kazınırken hata oluştu: {e}")
    # Siteden çekemezse yurt dışına açık genel CDN yedek linki:
    return "https://tv-trt1.medya.trt.com.tr/master.m3u8"

def cnn_turk_guncel_link_bul():
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
    # Dinamik olarak canlı/yurt dışı uyumlu linkleri çekiyoruz
    trt1_linki = trt1_guncel_link_bul()
    cnn_linki = cnn_turk_guncel_link_bul()
    trt_spor_linki = trt_spor_guncel_link_bul()

    # Önce havuzdaki diğer kanalları geçici hafızaya alıyoruz
    havuz_kanallari = {}
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
                            if link_satiri and not link_satiri.startswith("#"):
                                kanal_adi = extinf_satiri.split(",")[-1].strip().lower()
                                havuz_kanallari[kanal_adi] = (extinf_satiri, link_satiri)
                            i += 1
                    i += 1
        except Exception as e:
            print(f"Havuz çekilirken hata oluştu: {e}")

    # SIRALAMA BAŞLIYOR: TRT 1'i en canlı haliyle en başa çakıyoruz
    ozel_kanallar = "#EXTM3U\n"
    ozel_kanallar += f'#EXTINF:-1 tvg-id="TRT1.tr" tvg-name="TRT 1" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/TRT_1_logo_%282021-%29.svg/960px-TRT_1_logo_%282021-%29.svg.png",TRT 1 (1080p)\n{trt1_linki}\n'
    
    eklenen_linkler = set([trt1_linki, cnn_linki, trt_spor_linki])

    # Diğer ulusal kanalları sırayla ekliyoruz
    for aranacak_kanal in TUTULACAK_KANALLAR:
        kanal_key = aranacak_kanal.strip().lower()
        if kanal_key in havuz_kanallari:
            extinf, link = havuz_kanallari[kanal_key]
            if link not in eklenen_linkler:
                ozel_kanallar += extinf + "\n" + link + "\n"
                eklenen_linkler.add(link)

    # TRT Spor ve CNN Türk'ü de listenin altına canlı kazınmış halleriyle ekliyoruz
    if trt_spor_linki not in eklenen_linkler:
        ozel_kanallar += f'#EXTINF:-1 tvg-id="TRTSpor.tr" tvg-name="TRT Spor" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/e/ec/TRT_Spor_logo.png",TRT Spor\n{trt_spor_linki}\n'
    if cnn_linki not in eklenen_linkler:
        ozel_kanallar += f'#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/0/09/CNN_T%C3%BCrk_logo.png",CNN Türk\n{cnn_linki}\n'

    with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
        f.write(ozel_kanallar.strip())
    print("İşlem başarılı! TRT 1 yurt dışı koruması aşılarak başa eklendi.")

if __name__ == "__main__":
    listeyi_guncelle()
