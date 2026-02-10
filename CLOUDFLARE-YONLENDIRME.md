# eytrapgod.com (Cloudflare) → Siteye yönlendirme

Domain’i Cloudflare’dan aldıysan, eytrapgod.com’a giren herkesi Streamlit sitene yönlendirmek için aşağıdakileri yap.

---

## Önce: Site yayında mı?

1. **https://share.streamlit.io** → GitHub ile giriş.
2. **New app** → Repo: eytrapgod-site (veya bu klasörün olduğu repo), Main file: `site_app.py`.
3. **Secrets** ekle: `SUPABASE_URL`, `SUPABASE_KEY`, `ADMIN_PASSWORD`.
4. Deploy et → Adresin şöyle olsun: **https://eytrapgod.streamlit.app** (veya seçtiğin isim). Bu adresi kopyala.

---

## Cloudflare’da yönlendirme (Redirect Rule)

1. **https://dash.cloudflare.com** → Giriş yap.
2. Soldan **Websites** → **eytrapgod.com**’u seç.
3. Üst menüden **Rules** → **Redirect Rules** (veya **Redirects**).
4. **Create rule** / **Add rule**.
5. Kuralı şöyle ayarla:
   - **Rule name:** `eytrapgod → streamlit` (istediğin isim)
   - **When:** “Incoming request” / “If…”
     - **Field:** Hostname
     - **Operator:** equals
     - **Value:** `eytrapgod.com`
   - **Then:** Redirect
     - **Type:** Dynamic (veya 302 Temporary)
     - **URL:** `https://eytrapgod.streamlit.app` (kendi Streamlit adresini yapıştır)
     - **Preserve path:** Kapalı
     - **Preserve query string:** İstersen açık
6. **Save** / **Deploy**.

### www için de yönlendirme

Aynı şekilde ikinci bir kural ekle:

- **When:** Hostname equals `www.eytrapgod.com`
- **Then:** Redirect → `https://eytrapgod.streamlit.app`

Kaydet.

---

## Kontrol

Birkaç dakika sonra tarayıcıda **https://eytrapgod.com** aç. Streamlit sitene yönlenmesi gerekir.

---

## Not

Bu yöntemde adres çubuğu yönlendirme sonrası `streamlit.app` olarak değişir. Adresin **hep eytrapgod.com** kalmasını istiyorsan, siteyi Render (veya custom domain destekleyen bir yerde) yayınlayıp Cloudflare DNS’te CNAME ile oraya yönlendirmen gerekir (DOMAIN.md’deki “Seçenek B”).
