@echo off

pip install virtualenv

rem activate venv
if exist venv\ (
   venv\Scripts\activate
   pip install -r requirements.txt
) else (
  virtualenv venv
  venv\Scripts\activate
  pip install -r requirements.txt
)
