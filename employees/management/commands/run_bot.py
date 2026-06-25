import time
import requests
from django.core.management.base import BaseCommand
from django.conf import settings

TOKEN = settings.TELEGRAM_BOT_TOKEN
API = f"https://api.telegram.org/bot{TOKEN}"


class Command(BaseCommand):
    help = "Telegram botni polling rejimida ishga tushiradi"

    def handle(self, *args, **kwargs):
        self.stdout.write("Bot polling rejimida ishga tushdi...")
        self.stdout.write("Toxtatish uchun: Ctrl+C\n")

        offset = None
        while True:
            try:
                params = {'timeout': 30, 'allowed_updates': ['message', 'callback_query']}
                if offset:
                    params['offset'] = offset

                r = requests.get(f"{API}/getUpdates", params=params, timeout=35)
                updates = r.json().get('result', [])

                for update in updates:
                    offset = update['update_id'] + 1
                    try:
                        from employees.bot import handle_update
                        handle_update(update)
                        self.stdout.write(f"OK: Update {update['update_id']} qayta ishlandi")
                    except Exception as e:
                        self.stdout.write(f"XATO: {e}")

            except KeyboardInterrupt:
                self.stdout.write("\nBot toxtatildi.")
                break
            except Exception as e:
                self.stdout.write(f"Ulanish xatosi: {e}")
                time.sleep(5)
