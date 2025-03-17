Запуск локально 

git remote add origin https://github.com/ShancoVils/bee_back.git


Через сервис 

[Unit]

Description=Gunicorn instance to serve myproject

After=network.target

[Service]

User=

Group=

WorkingDirectory=/path/to/gleb/loh/

ExecStart=/path/to/gleb/loh/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 5500 --reload

Restart=on-abort