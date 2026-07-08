import requests
import re

# Ana kaynak listemiz
KAYNAKLAR = [
    "https://iptv-org.github.io/iptv/countries/tr.m3u"
]

# -------------------------------------------------------------------------
# BURADAKİ SIRALAMA TELEVİZYONDA BİREBİR AYNI ŞEKİLDE ÇIKACAK kanka:
# TRT 1 birinci sırada, ATV ikinci sırada olacak şekilde ayarlandı.
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
    cnn_linki = cnn_turk_guncel_link_bul()
    trt_spor_linki = trt_spor_guncel_link_bul()

    # Önce havuzdaki tüm kanalları geçici bir hafızaya (sözlüğe) topluyoruz
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

    # Dosya yazma sırasını burası belirliyor
    ozel_kanallar = "#EXTM3U\n"
    eklenen_linkler = set()

    # SIRALAMA MOTORU: Kanalları senin listedeki sırayla tek tek çeker
    for aranacak_kanal in TUTULACAK_KANALLAR:
        kanal_key = aranacak_kanal.strip().lower()
        
        # Havuzda bu isimde kanal varsa sırayla listeye ekle
        if kanal_key in havuz_kanallari:
            extinf, link = havuz_kanallari[kanal_key]
            if link not in eklenen_linkler:
                ozel_kanallar += extinf + "\n" + link + "\n"
                eklenen_linkler.add(link)

    # Canlı sitelerden kazınan TRT Spor ve CNN Türk'ü de listenin EN ALTINA ekliyoruz.
    # (Eğer listenin EN BAŞINDA olmasını istersen bu iki bloğu yukarıdaki #EXTM3U satırının hemen altına taşıyabiliriz kanka)
    if trt_spor_linki not in eklenen_linkler:
        ozel_kanallar += f'#EXTINF:-1 tvg-id="TRTSpor.tr" tvg-name="TRT Spor" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/e/ec/TRT_Spor_logo.png",TRT Spor\n{trt_spor_linki}\n'
    if cnn_linki not in eklenen_linkler:
        ozel_kanallar += f'#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/0/09/CNN_T%C3%BCrk_logo.png",CNN Türk\n{cnn_linki}\n'

    with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
        f.write(ozel_kanallar.strip())
    print("İşlem başarılı! Kanallar listendeki sırayla jilet gibi dizildi.")

if __name__ == "__main__":
    listeyi_guncelle()
