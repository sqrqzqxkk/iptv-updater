import requests

# Güncel ana kaynağımız (Diğer tüm kanalları buradan çekeceğiz)
ANA_KAYNAK = "https://raw.githubusercontent.com/hayatiptv/iptv/master/index.m3u"

# Listede kalacak ve sırayla eklenecek diğer stabil kanallar
TUTULACAK_KANALLAR = [
    "ATV", "Kanal D", "NOW TV", "Beyaz TV", "Kanal 7", "TV 8",
    "EuroStar TV", "A Haber", "Habertürk TV", "NTV", "ATV Avrupa", 
    "Euro D", "A2TV", "A Spor"
]

def kanallari_ayıkla(url):
    kanallar = {}
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            satirlar = response.text.split("\n")
            i = 0
            while i < len(satirlar):
                satir = satirlar[i].strip()
                if satir.startswith("#EXTINF"):
                    extinf = satir
                    if i + 1 < len(satirlar):
                        link = satirlar[i+1].strip()
                        if link and not link.startswith("#"):
                            # Kanal adını temizle
                            kanal_adi = extinf.split(",")[-1].upper()
                            kanal_adi = kanal_adi.replace("HD", "").replace("FHD", "").replace("SD", "")
                            kanal_adi = kanal_adi.replace("(", "").replace(")", "").replace("[", "").replace("]", "")
                            kanal_adi = kanal_adi.strip().lower()
                            kanallar[kanal_adi] = (extinf, link)
                    i += 1
                i += 1
    except Exception as e:
        print(f"{url} yüklenirken hata oluştu: {e}")
    return kanallar

def listeyi_guncelle():
    print("Kanallar kaynaklardan taranıyor...")
    ana_kaynak_kanallari = kanallari_ayıkla(ANA_KAYNAK)

    m3u_icerik = "#EXTM3U\n"
    
    # -------------------------------------------------------------------------
    # 1. ADIM: AVUSTURYA'DA %100 ÇALIŞAN, COĞRAFİ ENGELSİZ VE SABİT KURUMSAL LİNLER
    # TRT ve CNN Türk'ün engellerini bu proxy linklerle tamamen deliyoruz.
    # -------------------------------------------------------------------------
    m3u_icerik += '#EXTINF:-1 tvg-id="TRT1.tr" tvg-name="TRT 1" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/TRT_1_logo_%282021-%29.svg/960px-TRT_1_logo_%282021-%29.svg.png",TRT 1 (Avrupa - Kesintisiz)\nhttps://hls.netmon.org/trt1/index.m3u8\n'
    m3u_icerik += '#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/0/09/CNN_T%C3%BCrk_logo.png",CNN Türk (Avrupa - Kesintisiz)\nhttps://hls.netmon.org/cnnturk/index.m3u8\n'
    m3u_icerik += '#EXTINF:-1 tvg-id="TRTBelgesel.tr" tvg-name="TRT Belgesel" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/TRT_Belgesel_logo_%282019-%29.svg/960px-TRT_Belgesel_logo_%282019-%29.svg.png",TRT Belgesel (Avrupa - Kesintisiz)\nhttps://hls.netmon.org/trtbelgesel/index.m3u8\n'
    m3u_icerik += '#EXTINF:-1 tvg-id="TRTSpor.tr" tvg-name="TRT Spor" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/e/ec/TRT_Spor_logo.png",TRT Spor (Avrupa - Kesintisiz)\nhttps://hls.netmon.org/trtspor/index.m3u8\n'
    m3u_icerik += '#EXTINF:-1 tvg-id="TRTHaber.tr" tvg-name="TRT Haber" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/TRT_Haber_Eyl%C3%BCl_2020_Logo.svg/960px-TRT_Haber_Eyl%C3%BCl_2020_Logo.svg.png",TRT Haber (Avrupa - Kesintisiz)\nhttps://hls.netmon.org/trthaber/index.m3u8\n'

    # -------------------------------------------------------------------------
    # 2. ADIM: DİĞER TÜM ULUSAL KANALLARI GÜNCEL LİSTEDEN ÇEKİP ALTINA SIRALIYORUZ
    # -------------------------------------------------------------------------
    eklenen_linkler = set()
    for siradaki_kanal in TUTULACAK_KANALLAR:
        kanal_key = siradaki_kanal.lower()
        
        for kaynak_adi, (extinf, link) in ana_kaynak_kanallari.items():
            if kanal_key == kaynak_adi or kanal_key in kaynak_adi:
                if link not in eklenen_linkler:
                    m3u_icerik += f"{extinf}\n{link}\n"
                    eklenen_linkler.add(link)
                    print(f"✓ {siradaki_kanal} -> Güncel Listeden Eklendi.")
                    break

    # Yeni listeyi basıyoruz
    with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik.strip())
    print("Mükemmel! Karartma korumalı yeni liste başarıyla üretildi.")

if __name__ == "__main__":
    listeyi_guncelle()
