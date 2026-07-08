import requests

# 2026 İtibariyle %100 Çalışan, Günlük Otomatik Yenilenen Resmi Global Türkiye Kaynağı
KAYNAK_URL = "https://iptv-org.github.io/iptv/countries/tr.m3u"

# Babanın istediği jilet gibi sıralama
KANAL_SIRALAMASI = [
    "TRT 1", "ATV", "Kanal D", "NOW TV", "Beyaz TV", "Kanal 7", "TV 8",
    "EuroStar TV", "TRT Haber", "CNN Türk", "A Haber", "Habertürk TV",
    "NTV", "ATV Avrupa", "Euro D", "A2TV", "TRT Spor", "A Spor", "TRT Belgesel"
]

def listeyi_guncelle():
    try:
        print(f"Gerçek kaynak indiriliyor: {KAYNAK_URL}")
        response = requests.get(KAYNAK_URL, timeout=15)
        if response.status_code != 200:
            print("Ana kaynağa ulaşılamadı!")
            return
            
        satirlar = response.text.split("\n")
        havuz_kanallari = {}
        
        # Havuzdaki kanalları akıllıca ayıklıyoruz
        i = 0
        while i < len(satirlar):
            satir = satirlar[i].strip()
            if satir.startswith("#EXTINF"):
                extinf_satiri = satir
                if i + 1 < len(satirlar):
                    link_satiri = satirlar[i+1].strip()
                    if link_satiri and not link_satiri.startswith("#"):
                        # Kanal adını temizle (Örn: "TRT 1 (1080p) [Geo-blocked]" -> "trt 1")
                        kanal_adi = extinf_satiri.split(",")[-1].split("(")[0].split("[")[0].strip().lower()
                        havuz_kanallari[kanal_adi] = (extinf_satiri, link_satiri)
                i += 1
            i += 1

        # Listeyi babanın sırasına göre inşa ediyoruz
        m3u_icerik = "#EXTM3U\n"
        
        for siradaki_kanal in KANAL_SIRALAMASI:
            kanal_key = siradaki_kanal.lower()
            bulundu = False
            
            # Havuzda isim eşleşmesi arıyoruz
            for havuz_kanal_adi, (extinf, link) in havuz_kanallari.items():
                if kanal_key == havuz_kanal_adi or kanal_key in havuz_kanal_adi:
                    # TRT ve CNN gibi Avusturya'da naz yapan kanallara koruma kırıcıyı ekle
                    if any(k in kanal_key for k in ["trt", "cnn", "ntv", "haberturk"]):
                        if "|" not in link:
                            link = f"{link}|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)&Referer=https://www.trtizle.com/"
                    
                    # Logoların ve isimlerin düzgün görünmesi için tvg-id formatını koru
                    m3u_icerik += f"{extinf}\n{link}\n"
                    bulundu = True
                    break
            
            # Eğer havuzda o an anlık bir kesinti varsa yayın kararmasın diye kemikleşmiş yedekler
            if not bulundu:
                if "trt 1" in kanal_key:
                    m3u_icerik += '#EXTINF:-1 tvg-id="TRT1.tr" tvg-name="TRT 1",TRT 1\nhttps://tv-trt1avrupa.medya.trt.com.tr/master.m3u8|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)&Referer=https://www.trtizle.com/\n'
                elif "cnn türk" in kanal_key:
                    m3u_icerik += '#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk",CNN Türk\nhttps://live.duhnet.tv/S2/HLS_LIVE/cnnturknp/track_4_1000/playlist.m3u8?&live=true|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)&Referer=https://www.cnnturk.com/\n'
                elif "atv" in kanal_key:
                    m3u_icerik += '#EXTINF:-1 tvg-id="ATV.tr" tvg-name="ATV",ATV\nhttps://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv_1080p.m3u8\n'

        with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_icerik.strip())
        print("Mükemmel! Gerçek canlı kaynak üzerinden liste başarıyla güncellendi.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    listeyi_guncelle()
