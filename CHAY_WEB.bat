@echo off
cd /d "%~dp0"
set GEMINI_FREE_TIER_CONFIRMED=yes
set GEMINI_MODEL=gemini-3.5-flash-lite
python -X utf8 -m streamlit run solution/ui.py
pause
