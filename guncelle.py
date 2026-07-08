import requests
import re

# Ana havuzumuz ve senin verdiğin canavar gibi çalışan sağlam alternatif kaynak
ANA_HAVUZ = "https://iptv-org.github.io/iptv/countries/tr.m3u"
HAYAT_IPTV = "https://raw.githubusercontent.com/hayatiptv/iptv/master/index.m3u"

# Babanın jilet gibi sıralaması
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
                            # Kanal adını temizle (Örn: "TRT 1 HD" -> "trt 1")
                            kanal_adi = extinf.split(",")[-1].split("(")[0].split("[")[0].replace("HD", "").replace("FHD", "").strip().lower()
                            kanallar[kanal_adi] = (extinf, link)
                    i += 1
                i += 1
    except Exception as e:
        print(f"{url} çekilirken hata oluştu: {e}")
    return kanallar

def listeyi_guncelle():
    print("Kanallar kaynaklardan toplanıyor...")
    havuz_kanallari = kanallari_ayıkla(ANA_HAVUZ)
    hayat_kanallari = kanallari_ayıkla(HAYAT_IPTV)

    m3u_icerik = "#EXTM3U\n"
    
    for siradaki_kanal in KANAL_SIRALAMASI:
        kanal_key = siradaki_kanal.lower()
        bulundu = False
        
        # 1. ÖNCELİK: Sorun çıkaran TRT ve CNN kanallarını senin verdiğin sağlam listeden çekiyoruz
        if kanal_key in ["trt 1", "cnn türk", "trt belgesel", "trt spor", "trt haber"]:
            if kanal_key in hayat_kanallari:
                extinf, link = hayat_kanallari[kanal_key]
                m3u_icerik += f"{extinf}\n{link}\n"
                bulundu = True
                print(f"✓ {siradaki_kanal} HayatIPTV kaynağından başarıyla çekildi.")
        
        # 2. ÖNCELİK: Eğer orada yoksa veya diğer ulusal kanallarsa ana havuzdan çekiyoruz
        if not bulundu:
            # Tam veya kısmi eşleşme kontrolü
            for havuz_adi, (extinf, link) in havuz_kanallari.items():
                if kanal_key == havuz_adi or kanal_key in havuz_adi:
                    m3u_icerik += f"{extinf}\n{link}\n"
                    bulundu = True
                    print(f"✓ {siradaki_kanal} Ana havuzdan çekildi.")
                    break
                    
        # 3. ÖNCELİK: İki tarafta da anlık sorun olursa sistem kararmasın diye kemik yedekler
        if not bulundu:
            if "trt 1" in kanal_key:
                m3u_icerik += '#EXTINF:-1 tvg-id="TRT1.tr" tvg-name="TRT 1",TRT 1\nhttps://tv-trt1avrupa.medya.trt.com.tr/master.m3u8\n'
            elif "cnn türk" in kanal_key:
                m3u_icerik += '#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk",CNN Türk\nhttps://live.duhnet.tv/S2/HLS_LIVE/cnnturknp/track_4_1000/playlist.m3u8?&live=true\n'

    # Dosyayı kaydet
    with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik.strip())
    print("Mükemmel! İki kaynağın en stabil kanalları birleştirildi ve liste güncellendi.")

if __name__ == "__main__":
    listeyi_guncelle()
