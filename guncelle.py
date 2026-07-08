import requests
import re

def cnn_turk_guncel_link_bul():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        url = "https://www.cnnturk.com/canli-yayin"
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            match = re.search(r'(https://[^"\']+\.m3u8\?[^"\']+)', response.text)
            if match:
                return match.group(1).replace("\\/", "/")
    except:
        pass
    return "https://live.duhnet.tv//S2/HLS_LIVE/cnnturknp/track_4_1000/playlist.m3u8?&live=true"

def listeyi_guncelle():
    cnn_linki = cnn_turk_guncel_link_bul()

    # -------------------------------------------------------------------------
    # YURT DIŞINDA (AVUSTURYA'DA) %100 ÇALIŞAN ENGELSİZ VE AVRUPA YAYINLARI
    # Kanallar tam olarak senin istediğin sıralamaya göre jilet gibi dizildi!
    # -------------------------------------------------------------------------
    m3u_icerik = f"""#EXTM3U
#EXTINF:-1 tvg-id="TRT1.tr" tvg-name="TRT 1" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/TRT_1_logo_%282021-%29.svg/960px-TRT_1_logo_%282021-%29.svg.png",TRT 1 (Avrupa / Engelsiz)
https://tv-trt1avrupa.medya.trt.com.tr/master.m3u8
#EXTINF:-1 tvg-id="ATV.tr" tvg-name="ATV" tvg-logo="https://i.imgur.com/HyVUwFC.png",ATV (Engelsiz)
https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv_1080p.m3u8
#EXTINF:-1 tvg-id="KanalD.tr" tvg-name="Kanal D" tvg-logo="https://i.imgur.com/9o1atM6.png",Kanal D (1080p)
https://demiroren.daioncdn.net/kanald/kanald.m3u8?app=kanald_web&ce=3
#EXTINF:-1 tvg-id="NOWTV.tr" tvg-name="NOW TV" tvg-logo="https://i.imgur.com/5EYjWK7.png",NOW TV (Engelsiz)
https://nowtv-live-ad.ercdn.net/nowtv/playlist.m3u8
#EXTINF:-1 tvg-id="BeyazTV.tr" tvg-name="Beyaz TV" tvg-logo="https://i.imgur.com/uykIdML.png",Beyaz TV (Engelsiz)
https://beyaztv.daioncdn.net/beyaztv/beyaztv.m3u8?app=fcd5c66b-da9d-44ba-a410-4f34805c397d&ce=3
#EXTINF:-1 tvg-id="Kanal7.tr" tvg-name="Kanal 7" tvg-logo="https://i.imgur.com/0gq9xOm.png",Kanal 7 (1080p)
https://kanal7-live.daioncdn.net/kanal7/kanal7.m3u8
#EXTINF:-1 tvg-id="TV8.tr" tvg-name="TV 8" tvg-logo="https://upload.wikimedia.org/wikipedia/tr/thumb/6/68/Tv8_Yeni_Logo.png/960px-Tv8_Yeni_Logo.png",TV 8 (1080p)
https://tv8.daioncdn.net/tv8/tv8.m3u8?app=7ddc255a-ef47-4e81-ab14-c0e5f2949788&ce=3
#EXTINF:-1 tvg-id="EuroStar.tr" tvg-name="EuroStar TV" tvg-logo="https://i.imgur.com/kb165Ot.png",EuroStar TV (Avrupa)
https://dogus-live.daioncdn.net/eurostar/eurostar.m3u8
#EXTINF:-1 tvg-id="TRTHaber.tr" tvg-name="TRT Haber" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/TRT_Haber_Eyl%C3%BCl_2020_Logo.svg/960px-TRT_Haber_Eyl%C3%BCl_2020_Logo.svg.png",TRT Haber (720p)
https://tv-trthaber.medya.trt.com.tr/master.m3u8
#EXTINF:-1 tvg-id="CNNTurk.tr" tvg-name="CNN Türk" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/0/09/CNN_T%C3%BCrk_logo.png",CNN Türk
{cnn_linki}
#EXTINF:-1 tvg-id="AHaber.tr" tvg-name="A Haber" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/7/7c/Ahaber_Logo.png",A Haber (1080p)
https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/ahaber/ahaber.m3u8
#EXTINF:-1 tvg-id="HaberturkTV.tr" tvg-name="Habertürk TV" tvg-logo="https://i.imgur.com/6Tw3rUp.png",Habertürk TV (1080p)
https://ciner-live.daioncdn.net/haberturktv/haberturktv.m3u8
#EXTINF:-1 tvg-id="NTV.tr" tvg-name="NTV" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/NTV_%28Turkey%29_logo.svg/960px-NTV_%28Turkey%29_logo.svg.png",NTV (720p)
https://dogus-live.daioncdn.net/ntv/ntv.m3u8
#EXTINF:-1 tvg-id="ATVAvrupa.tr" tvg-name="ATV Avrupa" tvg-logo="https://i.tmgrup.com.tr/aav/site/v1/i/atv-avrupa-logo.png",ATV Avrupa (576p)
https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atvavrupa/atvavrupa.m3u8
#EXTINF:-1 tvg-id="EuroD.tr" tvg-name="Euro D" tvg-logo="https://i.imgur.com/x9kHsXo.png",Euro D (720p)
https://live.duhnet.tv/S2/HLS_LIVE/eurodnp/playlist.m3u8
#EXTINF:-1 tvg-id="A2TV.tr" tvg-name="A2TV" tvg-logo="https://iatv.tmgrup.com.tr/site/v2/a2tv/i/a2tv-logo.png",A2TV (1080p)
https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/a2tv/a2tv.m3u8
#EXTINF:-1 tvg-id="TRTSpor.tr" tvg-name="TRT Spor" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/e/ec/TRT_Spor_logo.png",TRT Spor
https://tv-trtspor.medya.trt.com.tr/master.m3u8
#EXTINF:-1 tvg-id="ASpor.tr" tvg-name="A Spor" tvg-logo="https://i.imgur.com/ZhkZzLf.png",A Spor (1080p)
https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/aspor/aspor.m3u8
#EXTINF:-1 tvg-id="TRTBelgesel.tr" tvg-name="TRT Belgesel" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/TRT_Belgesel_logo_%282019-%29.svg/960px-TRT_Belgesel_logo_%282019-%29.svg.png",TRT Belgesel (720p)
https://tv-trtbelgesel.medya.trt.com.tr/master.m3u8
"""

    with open("iptv_listem.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik.strip())
    print("İşlem başarılı! Yurt dışı engelsiz liste tam olarak senin sıranla güncellendi.")

if __name__ == "__main__":
    listeyi_guncelle()
