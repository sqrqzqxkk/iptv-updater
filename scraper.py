import requests
from bs4 import BeautifulSoup
import re

def get_live_link():
    # 1. Siteye sanki gerçek bir tarayıcıymış gibi istek göndermek için Header tanımlıyoruz
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    url = "https://tv.vin" # Yayının bulunduğu tam sayfa adresi
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # 2. Sayfa kaynağını analiz ediyoruz
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 3. Sayfa içindeki JavaScript kodlarında ".m3u8" geçen yerleri regex (düzenli ifadeler) ile arıyoruz
            # Genellikle token'lı linkler script etiketlerinin içinde gömülüdür
            script_tags = soup.find_all('script')
            for tag in script_tags:
                if tag.string and 'm3u8' in tag.string:
                    # m3u8 uzantılı ve dinamik tokenlı linki ayıklıyoruz
                    match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', tag.string)
                    if match:
                        return match.group(1)
        return None
    except Exception as e:
        print(print(f"Hata oluştu: {e}"))
        return None

def create_m3u(stream_url):
    if stream_url:
        # 4. Standart M3U formatında dosyayı oluşturuyoruz
        m3u_content = f"#EXTM3U\n#EXTINF:-1,TV VIN CANLI\n{stream_url}\n"
        with open("yayinlarim.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("M3U Dosyası başarıyla güncellendi!")
    else:
        print("Güncel yayın linki bulunamadı.")

if __name__ == "__main__":
    current_link = get_live_link()
    create_m3u(current_link)