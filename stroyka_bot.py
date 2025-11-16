from telegram import Update
import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pathlib import Path

# Загружаем переменные из .env файла
def load_env() -> None:
    try:
        from dotenv import load_dotenv, find_dotenv
        env_start = Path(__file__).parent
        env_file = find_dotenv(filename=".env", usecwd=True) or str(env_start / ".env")
        load_dotenv(dotenv_path=env_file, override=False)
    except Exception:
        # Если нет python-dotenv или произошла ошибка — пропускаем, полагаемся на внешние переменные
        pass

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def resolve_token() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if token:
        return token
    # Фолбэк: попробуем прочитать токен напрямую из .env рядом со скриптом
    try:
        direct_env = (Path(__file__).parent / ".env")
        if direct_env.exists():
            for line in direct_env.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

def main() -> None:
    load_env()
    token = resolve_token()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("hello", hello))
    app.run_polling()

if __name__ == "__main__":
    main()