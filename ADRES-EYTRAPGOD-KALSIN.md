# Adres hep www.eytrapgod.com / eytrapgod.com kalsın (hosting adresi görünmesin)

Şu an yönlendirme kullandığın için tarayıcı **streamlit.app** (veya hosting) adresine gidiyor ve amatör görünüyor.  
Aşağıdaki adımlarla siteyi **Render** üzerinde **custom domain** ile yayınlayıp, adres çubuğunun **hep eytrapgod.com** kalmasını sağlayacaksın.

---

## Adım 1: Cloudflare’daki yönlendirmeyi kaldır

1. **dash.cloudflare.com** → **eytrapgod.com** sitesini seç.
2. **Rules** → **Redirect Rules** (veya **Redirects**).
3. eytrapgod.com / www’yi streamlit.app’e yönlendiren kuralı **sil** veya **devre dışı bırak**.  
   Böylece domain artık sadece DNS ile kullanılacak, adres değişmeyecek.

---

## Adım 2: Siteyi Render’da yayınla

1. **https://render.com** → **Sign up** (GitHub ile giriş yap).
2. **New +** → **Web Service**.
3. **Connect** ile eytrapgod-site’ın olduğu GitHub repo’yu bağla (veya repo zaten listedeyse seç).
4. Ayarlar:
   - **Name:** `eytrapgod` (istersen başka isim).
   - **Region:** Frankfurt veya Oregon.
   - **Branch:** `main`.
   - **Root Directory:** Repo kökü TrapGod_AI ve site `eytrapgod-site` klasöründeyse buraya `eytrapgod-site` yaz. (Sadece eytrapgod-site repo’su ise boş bırak.)
   - **Build Command:**  
     `pip install -r requirements.txt`
   - **Start Command:**  
     `streamlit run site_app.py --server.port=$PORT --server.address=0.0.0.0`
5. **Advanced** → **Environment** (Environment Variables):
   - `SUPABASE_URL` = `https://juxnxccpmblixellwtrp.supabase.co`
   - `SUPABASE_KEY` = (kendi key’in)
   - `ADMIN_PASSWORD` = (admin şifren)
6. **Create Web Service** → Build ve deploy bitsin.  
   Adresin şöyle olacak: **https://eytrapgod.onrender.com** (veya verdiği isim). Bu adresi not al.

---

## Adım 3: Render’da custom domain ekle

1. Render’da oluşturduğun **Web Service** sayfasında **Settings**.
2. **Custom Domains** bölümüne in.
3. **Add Custom Domain**:
   - Önce **www.eytrapgod.com** ekle → Render sana bir CNAME hedefi verecek (örn. `eytrapgod.onrender.com`). Not al.
   - Sonra **eytrapgod.com** (root) ekle → Gerekirse ek CNAME veya A bilgisi verir. Not al.

---

## Adım 4: Cloudflare DNS’i Render’a yönlendir

1. **dash.cloudflare.com** → **eytrapgod.com** → **DNS** → **Records**.
2. **www için:**
   - **Add record**
   - Type: **CNAME**
   - Name: **www**
   - Target: Render’ın söylediği adres (örn. `eytrapgod.onrender.com`)
   - Proxy status: **Proxied** (turuncu bulut) veya **DNS only** (gri) – Render SSL için bazen **DNS only** ister; Render’daki talimata bak.
   - Save.
3. **Kök domain (eytrapgod.com) için:**  
   Cloudflare’da root’u Render’a vermek için:
   - **CNAME** kullanıyorsan: Name **@**, Target **eytrapgod.onrender.com**, Proxy **DNS only** (Render dokümanına göre).
   - Veya Render’ın verdiği **A** kaydı varsa: Type **A**, Name **@**, Value **216.24.57.1** (Render’ın load balancer IP’si).
4. Eski **Redirect Rule**’ları eklemediğinden emin ol (Adım 1).

---

## Adım 5: SSL (HTTPS)

Render, custom domain için **ücretsiz TLS** verir. DNS doğru gidince birkaç dakika – birkaç saat içinde https://www.eytrapgod.com ve https://eytrapgod.com çalışır. Cloudflare’da **SSL/TLS** modu **Full** veya **Full (strict)** yapabilirsin.

---

## Sonuç

- Ziyaretçi **www.eytrapgod.com** veya **eytrapgod.com** yazar.
- Adres çubuğu **hep eytrapgod.com** kalır; streamlit.app / onrender.com görünmez.
- Site tamamen senin domain’inde, profesyonel görünür.

Takıldığın adımı (örn. “Render Start Command”, “Cloudflare CNAME”) yazarsan, o adımı tek tek tarif edebilirim.
