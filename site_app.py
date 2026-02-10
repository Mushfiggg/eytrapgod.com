"""
eytrapgod.com – Trap rap & poet kimlik sitesi.
Bjork.com tarzı: sağda stream (EYTRAPGOD + menü), solda içerik.
Admin panel: şifre ile giriş, tüm içeriği Supabase üzerinden düzenleme.
"""

import os
import json
import streamlit as st

# ============== SUPABASE (site içeriği) ==============
SITE_TABLE = "site_content"

def _get_supabase():
    try:
        url = os.environ.get("SUPABASE_URL") or (st.secrets.get("SUPABASE_URL") if hasattr(st, "secrets") else None)
        key = os.environ.get("SUPABASE_KEY") or (st.secrets.get("SUPABASE_KEY") if hasattr(st, "secrets") else None)
        if url and key:
            from supabase import create_client
            return create_client(url, key)
    except Exception:
        pass
    return None

def _get_site_data(sb, key, default):
    if sb is None:
        return default
    try:
        r = sb.table(SITE_TABLE).select("data").eq("key", key).maybe_single().execute()
        if r.data and r.data.get("data") is not None:
            return r.data["data"]
    except Exception:
        pass
    return default

def _set_site_data(sb, key, data):
    if sb is None:
        return
    try:
        sb.table(SITE_TABLE).upsert({"key": key, "data": data}, on_conflict="key").execute()
    except Exception:
        pass

# Varsayılan içerik
DEFAULT_HERO = {"title": "EYTRAPGOD", "subtitle": "trap rap · poet"}
DEFAULT_MENU = [
    {"label": "music", "url": "#"},
    {"label": "lyrics", "url": "#"},
    {"label": "shop", "url": "#"},
]
DEFAULT_ABOUT = {"heading": "about", "body": "Trap rap sanatçısı ve söz yazarı. Buraya kendi metnini admin panelden ekleyebilirsin."}
DEFAULT_STREAM = [
    {"label": "tour", "url": "#"},
    {"label": "releases", "url": "#"},
]

# ============== ADMIN GİRİŞ ==============
ADMIN_SECRET_KEY = "admin_logged_in"

def get_admin_password():
    try:
        return st.secrets.get("ADMIN_PASSWORD", os.environ.get("ADMIN_PASSWORD", "eytrapgod_admin_2025"))
    except Exception:
        return os.environ.get("ADMIN_PASSWORD", "eytrapgod_admin_2025")

def is_admin():
    return st.session_state.get(ADMIN_SECRET_KEY, False)

def set_admin_logged_in(value):
    st.session_state[ADMIN_SECRET_KEY] = value

# ============== SAYFA AYARI ==============
st.set_page_config(
    page_title="EYTRAPGOD",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============== BJORK TARZI TEMA ==============
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Libre+Baskerville:ital@0;1&display=swap" rel="stylesheet">
<style>
    .stApp { background: #0a0a0a !important; }
    .main .block-container { max-width: 100%; padding: 0 2rem 2rem; }
    /* Sağ stream alanı – sabit, bjork tarzı */
    .stream-column {
        position: fixed; top: 0; right: 0; width: 140px; height: 100vh;
        background: #0a0a0a; border-left: 1px solid #222;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        padding: 2rem 0; z-index: 100;
    }
    .stream-brand {
        font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 0.35em;
        color: #fff; writing-mode: vertical-rl; text-orientation: mixed;
        transform: rotate(180deg); margin-bottom: 2rem;
    }
    .stream-menu { display: flex; flex-direction: column; gap: 0.75rem; text-align: center; }
    .stream-menu a {
        font-family: 'Libre Baskerville', serif; font-size: 0.85rem; color: #888;
        text-decoration: none; text-transform: lowercase;
    }
    .stream-menu a:hover { color: #fff; }
    /* Ana içerik alanı – stream için sağda boşluk bırak */
    .site-main { margin-right: 160px; min-height: 80vh; }
    .site-hero { padding: 4rem 0 3rem; }
    .site-hero h1 {
        font-family: 'Bebas Neue', sans-serif; font-size: clamp(3rem, 12vw, 8rem);
        letter-spacing: 0.08em; color: #fff; margin: 0 0 0.5rem;
    }
    .site-hero .subtitle {
        font-family: 'Libre Baskerville', serif; font-size: 1rem; color: #666;
        text-transform: lowercase; letter-spacing: 0.2em;
    }
    .site-section { padding: 2rem 0; border-top: 1px solid #1a1a1a; }
    .site-section h2 {
        font-family: 'Bebas Neue', sans-serif; font-size: 1.2rem; letter-spacing: 0.3em;
        color: #444; margin-bottom: 1rem;
    }
    .site-section p {
        font-family: 'Libre Baskerville', serif; font-size: 1rem; color: #999;
        line-height: 1.7; max-width: 520px;
    }
    #MainMenu, footer, header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

sb = _get_supabase()

# ============== ADMIN PANEL (şifre ile) ==============
if is_admin():
    st.markdown("### 🔐 Admin panel")
    if st.button("Çıkış (admin)"):
        set_admin_logged_in(False)
        st.rerun()

    hero = _get_site_data(sb, "hero", DEFAULT_HERO)
    menu = _get_site_data(sb, "menu", DEFAULT_MENU)
    about = _get_site_data(sb, "about", DEFAULT_ABOUT)
    stream = _get_site_data(sb, "stream", DEFAULT_STREAM)

    with st.expander("Hero (üst başlık)", expanded=True):
        h_title = st.text_input("Başlık", value=hero.get("title", "EYTRAPGOD"), key="ah_title")
        h_sub = st.text_input("Alt başlık", value=hero.get("subtitle", "trap rap · poet"), key="ah_sub")
        if st.button("Hero kaydet"):
            _set_site_data(sb, "hero", {"title": h_title, "subtitle": h_sub})
            st.success("Kaydedildi.")
            st.rerun()

    with st.expander("Sağ menü (stream linkleri)"):
        st.caption("Her satır: label,url (örn: music,https://...)")
        menu_text = st.text_area("Menü", value="\n".join(f"{m.get('label','')},{m.get('url','')}" for m in menu), height=120, key="am_menu")
        if st.button("Menü kaydet"):
            lines = [l.strip() for l in menu_text.split("\n") if "," in l]
            new_menu = []
            for line in lines:
                parts = line.split(",", 1)
                new_menu.append({"label": parts[0].strip(), "url": parts[1].strip() if len(parts) > 1 else "#"})
            _set_site_data(sb, "menu", new_menu if new_menu else DEFAULT_MENU)
            st.success("Kaydedildi.")
            st.rerun()

    with st.expander("About bölümü"):
        ab_heading = st.text_input("Başlık", value=about.get("heading", "about"), key="ab_h")
        ab_body = st.text_area("Metin", value=about.get("body", ""), height=150, key="ab_b")
        if st.button("About kaydet"):
            _set_site_data(sb, "about", {"heading": ab_heading, "body": ab_body})
            st.success("Kaydedildi.")
            st.rerun()

    with st.expander("Stream ek öğeleri (sağda alt)"):
        stream_text = st.text_area("Stream", value="\n".join(f"{s.get('label','')},{s.get('url','')}" for s in stream), height=80, key="am_stream")
        if st.button("Stream kaydet"):
            lines = [l.strip() for l in stream_text.split("\n") if "," in l]
            new_stream = []
            for line in lines:
                parts = line.split(",", 1)
                new_stream.append({"label": parts[0].strip(), "url": parts[1].strip() if len(parts) > 1 else "#"})
            _set_site_data(sb, "stream", new_stream if new_stream else DEFAULT_STREAM)
            st.success("Kaydedildi.")
            st.rerun()

    st.stop()

# ============== GİRİŞ (admin için gizli link) ==============
with st.sidebar:
    st.caption("Admin")
    admin_pwd = st.text_input("Şifre", type="password", key="admin_pwd", label_visibility="collapsed", placeholder="Şifre")
    if st.button("Giriş") and admin_pwd and admin_pwd.strip() == get_admin_password().strip():
        set_admin_logged_in(True)
        st.rerun()

# ============== PUBLİC SİTE (bjork tarzı) ==============
hero = _get_site_data(sb, "hero", DEFAULT_HERO)
menu = _get_site_data(sb, "menu", DEFAULT_MENU)
about = _get_site_data(sb, "about", DEFAULT_ABOUT)
stream = _get_site_data(sb, "stream", DEFAULT_STREAM)

# Sağ stream – HTML ile (başlık + menü, bjork tarzı)
brand_title = hero.get("title", "EYTRAPGOD")
stream_html = f"""
<div class="stream-column">
  <div class="stream-brand">{brand_title}</div>
  <nav class="stream-menu">
"""
for m in menu:
    stream_html += f'    <a href="{m.get("url", "#")}">{m.get("label", "")}</a>\n'
for s in stream:
    stream_html += f'    <a href="{s.get("url", "#")}">{s.get("label", "")}</a>\n'
stream_html += """
  </nav>
</div>
"""
st.markdown(stream_html, unsafe_allow_html=True)

# Ana içerik
st.markdown('<div class="site-main">', unsafe_allow_html=True)

st.markdown(f"""
<div class="site-hero">
  <h1>{hero.get("title", "EYTRAPGOD")}</h1>
  <p class="subtitle">{hero.get("subtitle", "trap rap · poet")}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="site-section">
  <h2>{about.get("heading", "about").upper()}</h2>
  <p>{about.get("body", "").replace(chr(10), "<br>")}</p>
</div>
""", unsafe_allow_html=True)

# Admin girişi için küçük link (sayfa altında)
st.markdown("<div style='margin-top: 4rem; padding-top: 2rem; border-top: 1px solid #1a1a1a;'>", unsafe_allow_html=True)
st.caption("Site yönetimi için sol menüden Admin şifresi ile giriş yapabilirsin.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
