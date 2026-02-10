# EYTRAPGOD – Kimlik sitesi (eytrapgod.com)

Trap rap sanatçısı ve söz yazarı kimlik sitesi. [Bjork.com](https://www.bjork.com/) tarzı: sağda sabit **stream** (EYTRAPGOD + menü linkleri), solda içerik. Tüm metin ve linkler **admin panel** üzerinden düzenlenir.

---

## Kurulum

### 1. Bağımlılıklar

```bash
cd eytrapgod-site
pip install -r requirements.txt
```

### 2. Supabase tablosu

Aynı Supabase projesini (TrapGod_AI’deki gibi) kullanabilirsin. Supabase **SQL Editor**’da çalıştır:

```sql
create table if not exists site_content (
  key text primary key,
  data jsonb not null default '{}',
  updated_at timestamptz not null default now()
);
```

### 3. Secrets

`.streamlit/secrets.toml` oluştur:

- `SUPABASE_URL` ve `SUPABASE_KEY` (TrapGod_AI ile aynı proje olabilir)
- `ADMIN_PASSWORD` – sadece senin bildiğin admin şifresi

### 4. Çalıştırma

**Windows (kolay):** `eytrapgod-site` klasöründe **calistir.bat** dosyasına çift tıkla. Tarayıcıda http://localhost:8501 açılır.

**Terminalden:**
- Önce `eytrapgod-site` klasörüne gir:
  ```bash
  cd eytrapgod-site
  ```
- Sonra:
  ```bash
  streamlit run site_app.py
  ```
- PowerShell’de `&&` kullanma; komutları ayrı ayrı çalıştır veya `;` kullan: `cd eytrapgod-site; streamlit run site_app.py`

Tarayıcıda aç. Sol menüyü açıp **Admin** alanına şifreyi yazıp **Giriş** de; hero, menü, about ve stream linklerini oradan düzenleyebilirsin.

---

## eytrapgod.com’a bağlama

1. Bu projeyi GitHub’a at (ayrı repo veya TrapGod_AI içinde `eytrapgod-site` klasörü).
2. **Streamlit Cloud**’da yeni uygulama oluştur: repo = bu proje, main file = `site_app.py`, secrets = `SUPABASE_URL`, `SUPABASE_KEY`, `ADMIN_PASSWORD`.
3. Domain sağlayıcında (GoDaddy, Cloudflare, vb.) **eytrapgod.com** için CNAME veya A kaydını Streamlit Cloud’un verdiği `*.streamlit.app` adresine yönlendir. (Streamlit Cloud’da “Custom domain” varsa oradan da ekleyebilirsin.)

Böylece site eytrapgod.com’da yayında olur; içeriği her zaman admin panelden güncellersin.
