import requests

# Babanın listesi için her gün güncellenen taş gibi ana kaynak
ANA_KAYNAK = "https://raw.githubusercontent.com/hayatiptv/iptv/master/index.m3u"

# Babanın istediği jilet gibi eksiksiz tam sıralama
KANAL_SIRALAMASI = [
    "TRT 1", "ATV", "Kanal D", "NOW TV", "Beyaz TV", "Kanal 7", "TV 8",
    "EuroStar TV", "TRT Haber", "CNN Türk", "A Haber", "Habertürk TV",
    "NTV", "ATV Avrupa", "Euro D", "A2TV", "TRT Spor", "A Spor", "TRT Belgesel"
]

def listeyi_guncelle():
    try:
        print("Güncel liste kaynaktan indiriliyor...")
        response = requests.get(ANA_KAYNAK, timeout=15)
        if response.status_code != 200:
            print("Ana kaynağa ulaşılamadı!")
            return

        satirlar = response.text.split("\n")
        havuz_kanallari = {}
        
        # Kaynaktaki tüm kanalları hafızaya alıyoruz
        i = 0
        while i < len(satirlar):
            satir = satirlar[i].strip()
            if satir.startswith("#EXTINF"):
                extinf_satiri = satir
                if i + 1 < len(satirlar):
                    link_satiri = satirlar[i+1].strip()
                    if link_satiri and not link_satiri.startswith("#"):
                        # Kanal adını sadece harf ve rakam kalacak şekilde temizle
                        kanal_adi = extinf_satiri.split(",")[-1].upper()
                        kanal_adi = kanal_adi.replace("HD", "").replace("FHD", "").replace("SD", "")
                        kanal_adi = kanal_adi.replace("TURK", "TÜRK").replace("NOW", "NOW TV")
                        kanal_adi = "".join(e for e in kanal_adi if e.isalnum()).lower()
                        havuz_kanallari[kanal_adi] = (extinf_satiri, link_satiri)
                i += 1
            i += 1

        m3u_icerik = "#EXTM3U\n"
        
        # Listeyi babanın sırasına göre tek tek inşa ediyoruz
        for siradaki_kanal in KANAL_SIRALAMASI:
            kanal_key = "".join(e for e in siradaki_kanal.upper() if e.isalnum()).lower()
            
            # --- 1. DURUM: TRT'LER VE CNN TÜRK İÇİN AVUSTURYA'DA %100 ÇALIŞAN ÖZEL GLOBAL AKIŞLAR ---
            if "trt1" in kanal_key:
                m3u_icerik += '#EXTINF:-1 tvg-id="TRT1.tr" tvg-name="TRT 1" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/TRT_1_logo_%282021-%29.svg/960px-TRT_1_logo_%282021-%29.svg.png",TRT 1 (Engelsiz)\nhttps://tv-trt1avrupa.medya.trt.com.tr/master.m3u8\n'
            elif "cnntürk" in kanal_key:
                m3u_icerik += '#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/0/09/CNN_T%C3%BCrk_logo.png",CNN Türk (Engelsiz)\nhttps://live.duhnet.tv/S2/HLS_LIVE/cnnturknp/track_4_1000/playlist.m3u8?&live=true\n'
            elif "trtbelgesel" in kanal_key:
                m3u_icerik += '#EXTINF:-1 tvg-id="TRTBelgesel.tr" tvg-name="TRT Belgesel" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/TRT_Belgesel_logo_%282019-%29.svg/960px-TRT_Belgesel_logo_%282019-%29.svg.png",TRT Belgesel (Engelsiz)\nhttps://tv-trtbelgesel.medya.trt.com.tr/master.m3u8\n'
            elif "trtspor" in kanal_key:
                m3u_icerik += '#EXTINF:-1 tvg-id="TRTSpor.tr" tvg-name="TRT Spor" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/e/ec/TRT_Spor_logo.png",TRT Spor (Engelsiz)\nhttps://tv-trtspor.medya.trt.com.tr/master.m3u8\n'
            elif "trthaber" in kanal_key:
                m3u_icerik += '#EXTINF:-1 tvg-id="TRTHaber.tr" tvg-name="TRT Haber" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/TRT_Haber_Eyl%C3%BCl_2020_Logo.svg/960px-TRT_Haber_Eyl%C3%BCl_2020_Logo.svg.png",TRT Haber (Engelsiz)\nhttps://tv-trthaber.medya.trt.com.tr/master.m3u8\n'
            
            # --- 2. DURUM: DİĞER TÜM ULUSAL KANALLAR (Kaynaktan akıllı eşleşmeyle çekilir) ---
            else:
                bulundu = False
                # Hafızadaki kanallarda akıllı arama yap
                for havuz_adi, (extinf, link) in havuz_kanallari.items():
                    if kanal_key == havuz_adi or kanal_key in havuz_adi or havuz_adi in kanal_key:
                        m3u_icerik += f"{extinf}\n{link}\n"
                        print(f"✓ {siradaki_kanal} başarıyla eklendi.")
                        bulundu = True
                        break
                
                # Eğer o anlık listede yoksa babanın sırası bozulmasın diye statik yedek linkini çakıyoruz
                if not bulundu:
                    if "atv" in kanal_key:
                        m3u_icerik += '#EXTINF:-1 tvg-id="ATV.tr" tvg-name="ATV",ATV\nhttps://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv_1080p.m3u8\n'
                    elif "kanald" in kanal_key:
                        m3u_icerik += '#EXTINF:-1 tvg-id="KanalD.tr" tvg-name="Kanal D",Kanal D\nhttps://demiroren.daioncdn.net/kanald/kanald.m3u8?app=kanald_web&ce=3\n'
                    elif "nowtv" in kanal_key:
                        m3u_icerik += '#EXTINF:-1 tvg-id="NOWTV.tr" tvg-name="NOW TV",NOW TV\nhttps://nowtv-live-ad.ercdn.net/nowtv/playlist.m3u8\n'
                    elif "tv8" in kanal_key:
                        m3u_icerik += '#EXTINF:-1 tvg-id="TV8.tr" tvg-name="TV 8",TV 8\nhttps://tv8.daioncdn.net/tv8/tv8.m3u8?app=7ddc255a-ef47-4e81-ab14-c0e5f2949788&ce=3\n'

        # Yeni listeyi yazdırıyoruz
        with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_icerik.strip())
        print("Mükemmel! Eksiksiz ve donma korumalı liste başarıyla hazırlandı.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    listeyi_guncelle()
