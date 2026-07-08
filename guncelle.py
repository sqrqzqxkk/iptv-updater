import requests

# Babanın listesi için 1. öncelikli güncel ana kaynağımız
ANA_KAYNAK = "https://raw.githubusercontent.com/hayatiptv/iptv/master/index.m3u"
YEDEK_HAVUZ = "https://iptv-org.github.io/iptv/countries/tr.m3u"

# Babanın istediği jilet gibi sıralama
KANAL_SIRALAMASI = [
    "TRT 1", "ATV", "Kanal D", "NOW TV", "Beyaz TV", "Kanal 7", "TV 8",
    "EuroStar TV", "TRT Haber", "CNN Türk", "A Haber", "Habertürk TV",
    "NTV", "ATV Avrupa", "Euro D", "A2TV", "TRT Spor", "A Spor", "TRT Belgesel"
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
                            # Kanal adını akıllıca temizle (Örn: "TRT 1 HD" -> "trt 1")
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
    # Dün güncellenen o taş gibi kaynağı hafızaya alıyoruz
    ana_kaynak_kanallari = kanallari_ayıkla(ANA_KAYNAK)
    # Eksik kalan olursa diye yedek havuz da kenarda bekliyor
    yedek_havuz_kanallari = kanallari_ayıkla(YEDEK_HAVUZ)

    m3u_icerik = "#EXTM3U\n"
    
    for siradaki_kanal in KANAL_SIRALAMASI:
        kanal_key = siradaki_kanal.lower()
        bulundu = False
        
        # 1. ADIM: Doğrudan dün güncellenen hayatiptv listesinde arıyoruz
        for kaynak_adi, (extinf, link) in ana_kaynak_kanallari.items():
            if kanal_key == kaynak_adi or kanal_key in kaynak_adi:
                m3u_icerik += f"{extinf}\n{link}\n"
                print(f"✓ {siradaki_kanal} -> Güncel Ana Kaynaktan Eklendi.")
                bulundu = True
                break
                
        # 2. ADIM: Eğer ana kaynakta o an yoksa yedek havuzdan tamamlıyoruz (Hata düzeltildi kanka!)
        if not bulundu:
            for yedek_adi, (extinf, link) in yedek_havuz_kanallari.items():
                if kanal_key == yedek_adi or kanal_key in yedek_adi:
                    m3u_icerik += f"{extinf}\n{link}\n"
                    print(f"⚠ {siradaki_kanal} -> Ana kaynakta yoktu, yedek havuzdan tamamlandı.")
                    bulundu = True
                    break

        # 3. ADIM: İki tarafta da bulunamazsa sistem çökmesin diye kemik link çakıyoruz
        if not bulundu:
            if "trt 1" in kanal_key:
                m3u_icerik += '#EXTINF:-1 tvg-id="TRT1.tr" tvg-name="TRT 1",TRT 1\nhttps://tv-trt1avrupa.medya.trt.com.tr/master.m3u8\n'
            elif "cnn türk" in kanal_key:
                m3u_icerik += '#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk",CNN Türk\nhttps://live.duhnet.tv/S2/HLS_LIVE/cnnturknp/track_4_1000/playlist.m3u8?&live=true\n'

    # Yeni listeyi diske yazıyoruz
    with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik.strip())
    print("Mükemmel! Liste tamamen güncel hayatiptv odaklı olarak baştan inşa edildi.")

if __name__ == "__main__":
    listeyi_guncelle()
