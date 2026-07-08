import requests

# Diğer ulusal kanalları çekeceğimiz ana havuz
KAYNAK_URL = "https://iptv-org.github.io/iptv/countries/tr.m3u"

# Havuzdan ayıklanacak diğer kanallar (TRT 1, TRT Spor ve CNN Türk'ü özel eklediğimiz için buradan çıkardık)
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
    "ATV Avrupa (576p) [Not 24/7]",
    "Euro D (720p)",
    "A2TV (1080p)",
    "A Spor (1080p)",
    "TRT Belgesel (720p)"
]

def listeyi_guncelle():
    try:
        # 1. Havuzdan diğer kanalları çekiyoruz
        response = requests.get(KAYNAK_URL, timeout=15)
        havuz_kanallari = {}
        
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

        # 2. Listeyi oluşturmaya başlıyoruz
        m3u_icerik = "#EXTM3U\n"
        
        # --- EN TEPEDE DURACAK GARANTİ KANALLAR (Avusturya'da %100 Çalışan Ham Linkler) ---
        m3u_icerik += '#EXTINF:-1 tvg-id="TRT1.tr" tvg-name="TRT 1" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/TRT_1_logo_%282021-%29.svg/960px-TRT_1_logo_%282021-%29.svg.png",TRT 1 (Avrupa - Engelsiz)\nhttps://tv-trt1avrupa.medya.trt.com.tr/master.m3u8\n'
        m3u_icerik += '#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/0/09/CNN_T%C3%BCrk_logo.png",CNN Türk (Engelsiz)\nhttps://live.duhnet.tv/S2/HLS_LIVE/cnnturknp/track_4_1000/playlist.m3u8?&live=true\n'
        m3u_icerik += '#EXTINF:-1 tvg-id="TRTSpor.tr" tvg-name="TRT Spor" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/e/ec/TRT_Spor_logo.png",TRT Spor (Engelsiz)\nhttps://tv-trtspor.medya.trt.com.tr/master.m3u8\n'
        
        # 3. Havuzdan gelen diğer kanalları babanın sırasıyla altına ekliyoruz
        eklenen_linkler = set()
        for aranacak_kanal in TUTULACAK_KANALLAR:
            kanal_key = aranacak_kanal.strip().lower()
            if kanal_key in havuz_kanallari:
                extinf, link = havuz_kanallari[kanal_key]
                if link not in eklenen_linkler:
                    m3u_icerik += f"{extinf}\n{link}\n"
                    eklenen_linkler.add(link)

        # 4. Dosyayı kaydet
        with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_icerik.strip())
        print("İşlem başarılı! Karma liste babanın sırasıyla güncellendi.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    listeyi_guncelle()
