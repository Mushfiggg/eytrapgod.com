@echo off
cd /d "%~dp0"
echo Eytrapgod site baslatiliyor...
python -m streamlit run site_app.py
if errorlevel 1 (
    echo.
    echo Hata olustu. Streamlit yuklu mu? Terminalde su komutu dene:
    echo   pip install streamlit supabase
    echo.
)
pause
