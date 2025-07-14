from flask import Flask, request, jsonify, render_template
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Golf Dondurma API URL'leri
CUSTOMER_API_BASE_URL = "https://vp.golfdondurma.com.tr/AjaxContent/AjaxContent.aspx?id=11&Text="
ASSET_LOCATION_URL = "https://vp.golfdondurma.com.tr/Asset/AssetLocation.aspx"

# Müşteri Adı Çekme Fonksiyonu
def get_customer_name_from_api(customer_no):
    """
    Belirtilen müşteri numarasına göre müşteri adını Golf Dondurma API'sinden çeker.
    """
    api_url = f"{CUSTOMER_API_BASE_URL}{customer_no}"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status() # HTTP hataları için istisna fırlatır (4xx veya 5xx)

        root = ET.fromstring(response.content)
        customer_name_element = root.find(".//Müşteri_x0020_Adı")
        if customer_name_element is not None:
            return customer_name_element.text
        return "Müşteri Adı Bulunamadı"
    except requests.exceptions.RequestException as e:
        print(f"Müşteri adı API hatası: {e}")
        return "API Erişilemiyor (Müşteri Adı)"
    except ET.ParseError as e:
        print(f"XML Ayrıştırma Hatası (Müşteri Adı): {e}")
        return "XML Hatası"
    except Exception as e:
        print(f"Beklenmedik Hata (Müşteri Adı): {e}")
        return "Hata Oluştu (Müşteri Adı)"

# Barkod ve Model Çekme Fonksiyonu
def get_barcode_and_model_from_html():
    """
    Golf Dondurma'nın AssetLocation sayfasından barkod ve model bilgilerini çeker.
    Bu kısım, hedef HTML sayfasının yapısına göre özelleştirilmelidir.
    """
    try:
        response = requests.get(ASSET_LOCATION_URL, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')
        extracted_data = []
        # Barkod formatı için basit bir regex (9 ila 12 basamaklı sayılar)
        barcode_pattern = re.compile(r'\b\d{9,12}\b')

        # HTML'deki tüm tablo satırlarını (<tr>) dolaş
        for row in soup.find_all('tr'):
            cols = row.find_all('td') # Her satırdaki tüm sütunları (<td>) bul
            if len(cols) > 0:
                row_text = row.get_text() # Satırın tüm metin içeriğini al

                # Satır metninde barkod kalıbını ara
                found_barcodes = barcode_pattern.findall(row_text)
                
                for barcode in found_barcodes:
                    model = "Model (HTML Parse)" # Varsayılan model bilgisi
                    
                    # Eğer model bilgisi aynı satırda "Model: XYZ" gibi bir formatta geçiyorsa
                    model_match = re.search(r'Model:\s*([^\n\r]+)', row_text, re.IGNORECASE)
                    if model_match:
                        model = model_match.group(1).strip()
                    
                    extracted_data.append({'barkod_no': barcode, 'model': model})
        
        # Çekilen verilerde tekrar eden barkodları elemek için
        unique_data = {item['barkod_no']: item for item in extracted_data}.values()
        
        return list(unique_data)

    except requests.exceptions.RequestException as e:
        print(f"Barkod HTML API hatası: {e}")
        return []
    except Exception as e:
        print(f"Beklenmedik Hata (Barkod/Model): {e}")
        return []

# Ana sayfa route'u
@app.route('/')
def index():
    return render_template('index.html')

# Sorgulama API endpoint'i
@app.route('/sorgula', methods=['POST'])
def sorgula():
    musteri_no = request.form.get('musteriNo')
    if not musteri_no:
        return jsonify({'error': 'Müşteri numarası girilmedi.'}), 400

    # Müşteri adını ve dolap bilgilerini çek
    customer_name = get_customer_name_from_api(musteri_no)
    barcode_and_model_data = get_barcode_and_model_from_html()

    # Eğer API'lerden birinde hata oluştuysa, istemciye hata mesajı gönder
    if "Hata" in customer_name or "Erişilemiyor" in customer_name or "XML Hatası" in customer_name:
        return jsonify({'error': f'Müşteri bilgileri alınırken sorun oluştu: {customer_name}'}), 500
    
    # Başarılı yanıtı hazırla
    response_data = {
        'musteri_no': musteri_no,
        'customer_name': customer_name,
        'dolap_bilgileri': barcode_and_model_data
    }
    
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True) # Geliştirme aşamasında hata ayıklama için debug=True