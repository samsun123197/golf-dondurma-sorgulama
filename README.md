# Golf Dondurma Müşteri ve Dolap Bilgisi Sorgulama Uygulaması

Bu proje, bir Flask backend'i kullanarak Golf Dondurma'nın herkese açık API'lerinden (veya belirtilen URL'lerden) müşteri adını, dolap barkod bilgilerini ve modellerini sorgulayan basit bir web uygulamasıdır.

## Özellikler

- Müşteri numarası ile müşteri adını sorgulama.
- Tüm mevcut dolap barkod ve model bilgilerini çekme.
- Kullanıcı dostu web arayüzü.

## Teknolojiler

- **Backend:** Python (Flask)
- **Veri Çekme:** `requests`, `BeautifulSoup4`, `lxml`
- **Frontend:** HTML, CSS, JavaScript

## Kurulum ve Çalıştırma

Aşağıdaki adımları takip ederek projeyi yerel bilgisayarınızda kurabilir ve çalıştırabilirsiniz:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone [https://github.com/KullaniciAdiniz/golf-dondurma-sorgulama.git](https://github.com/KullaniciAdiniz/golf-dondurma-sorgulama.git)
    cd golf-dondurma-sorgulama
    ```
    *(`KullaniciAdiniz` kısmını kendi GitHub kullanıcı adınızla, depo adını da kendi depo adınızla değiştirin.)*

2.  **Sanal Ortam Oluşturun (Önerilen):**
    Proje bağımlılıklarını izole etmek için bir sanal ortam oluşturmak iyi bir pratiktir.
    ```bash
    python -m venv venv
    ```

3.  **Sanal Ortamı Aktif Edin:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Bağımlılıkları Yükleyin:**
    `requirements.txt` dosyasında belirtilen tüm Python bağımlılıklarını yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Uygulamayı Başlatın:**
    Flask uygulamasını başlatmak için aşağıdaki komutu kullanın:
    ```bash
    python app.py
    ```
    Uygulama başarıyla başladığında terminalde `* Running on http://127.0.0.1:5000/` benzeri bir mesaj görmelisiniz.

6.  **Uygulamaya Erişin:**
    Web tarayıcınızı açın ve `http://127.0.0.1:5000` adresine gidin.

7.  **Sorgulama Yapın:**
    Müşteri numarası giriş alanına `935297` gibi bir numara girin ve "Sorgula" butonuna tıklayın.

## Önemli Notlar

-   **HTML Ayrıştırma:** `app.py` içindeki `get_barcode_and_model_from_html()` fonksiyonu, `https://vp.golfdondurma.com.tr/Asset/AssetLocation.aspx` sayfasının HTML yapısına bağlıdır. Bu sayfanın yapısı değişirse, fonksiyonun güncellenmesi gerekebilir. En doğru sonuçlar için, tarayıcınızın "Geliştirici Araçları" ile sayfa kaynağını inceleyip ilgili HTML elementlerini belirlemeniz önerilir.
-   **CORS:** Bu uygulama, tarayıcının CORS (Cross-Origin Resource Sharing) kısıtlamalarını aşmak için bir backend proxy (Flask) kullanır. Bu nedenle, projeyi doğrudan bir HTML dosyası olarak açmak yerine, Flask uygulaması üzerinden çalıştırmanız gerekmektedir.

## Katkıda Bulunma

Projeyi geliştirmek isterseniz pull request'ler gönderebilirsiniz.

## Lisans

Bu proje [Lisansınız] ile lisanslanmıştır. (Örn: MIT Lisansı)