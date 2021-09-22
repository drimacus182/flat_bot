# olxbot

## Встановлення
```sh
git clone git@github.com:drimacus182/flat_bot.git
cd flat_bot
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Як користуватись 
Створити бота, отримати токен.

Перейменувати ```config-example.py``` в ```config.py``` і заповнити налаштування

Запустити python3 echo.py, і написати боту, щоб отримати chat_id

Потім треба періодично запускати ```bot.sh```. Я запускав кожні дві хвилини за допомогою crontab

