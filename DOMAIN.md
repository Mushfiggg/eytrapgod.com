# eytrapgod.com domain’i siteye bağlama

Domain’in hazır; siteyi yayına alıp adresi eytrapgod.com yapmak için iki seçenek var.

---

## Seçenek A: Streamlit Cloud + yönlendirme (en kolay)

**Sonuç:** Ziyaretçi eytrapgod.com yazınca otomatik olarak `eytrapgod.streamlit.app` adresine gider. Tarayıcı çubuğunda bir süre sonra streamlit.app görünür (yönlendirme ile).

### 1. Siteyi Streamlit Cloud’da yayınla

1. **https://share.streamlit.io** → GitHub ile giriş yap.
2. **New app** → Repo: `eytrapgod-site` (veya bu klasörün olduğu repo), Branch: `main`, Main file: `site_app.py`.
3. **Advanced settings** → Secrets’a yapıştır:
   ```
   SUPABASE_URL = "https://juxnxccpmblixellwtrp.supabase.co"
   SUPABASE_KEY = "sb_publishable_..."
   ADMIN_PASSWORD = "Eytrapgod1001"
   ```
4. **Deploy** → Birkaç dakika sonra `https://eytrapgod.streamlit.app` (veya seçtiğin alt alan adı) açılır.

### 2. Domain’i bu adrese yönlendir

Domain’i nereden aldıysan (GoDaddy, Namecheap, Cloudflare, Google Domains, vb.) orada:

- **Domain forwarding / URL redirect** bölümünü aç.
- **eytrapgod.com** ve **www.eytrapgod.com** için hedef adres olarak `https://eytrapgod.streamlit.app` yaz (HTTPS, gizli yönlendirme varsa onu seç).
- Kaydet.

Böylece eytrapgod.com’a giren herkes otomatik olarak Streamlit sitesine gider.

---

## Seçenek B: Render + kendi domain (adres hep eytrapgod.com kalsın)

**Sonuç:** Site doğrudan eytrapgod.com’da açılır; tarayıcıda adres hep eytrapgod.com olur.

### 1. Render’da hesap ve servis

1. **https://render.com** → Sign up (GitHub ile kolay).
2. **New** → **Web Service**.
3. Repo: eytrapgod-site’ın olduğu GitHub repo’su.
4. Ayarlar:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `streamlit run site_app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Environment:** Secret files → `SUPABASE_URL`, `SUPABASE_KEY`, `ADMIN_PASSWORD` ekle.
5. **Create Web Service** → Render bir URL verir (örn. `https://eytrapgod-site.onrender.com`).

### 2. Custom domain ekle

1. Render’da uygulamanın **Settings** → **Custom Domain**.
2. **eytrapgod.com** ve istersen **www.eytrapgod.com** ekle.
3. Render sana CNAME hedefi söyler (örn. `xxx.onrender.com`).

### 3. Domain sağlayıcında DNS

Domain’i yönettiğin yerde (GoDaddy, Cloudflare, vb.) DNS kayıtları:

| Tür   | Ad / Host | Değer (Render’ın söylediği) |
|-------|-----------|-----------------------------|
| CNAME | www       | `xxx.onrender.com`          |
| A     | @         | Render’ın verdiği IP (veya CNAME @ destekliyorsa CNAME) |

(Çoğu sağlayıcı “apex” için A kaydı veya ALIAS/ANAME ister; Render dokümanına bak.)

Bir süre sonra (birkaç dakika – 48 saat) eytrapgod.com doğrudan bu siteyi açar.

---

## Özet

| Yöntem              | Zorluk   | Adres çubuğu      |
|---------------------|----------|--------------------|
| A: Streamlit + redirect | Kolay    | Yönlendirme sonrası streamlit.app |
| B: Render + custom domain | Biraz teknik | Hep eytrapgod.com |

Domain’i nereden aldığını (örn. GoDaddy, Cloudflare) söylersen, o panel için adım adım “tıkla şuraya, şunu yaz” diye tarif edebilirim.
