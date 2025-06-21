import time
from functools import wraps
from services.translations import tr  # ← переклад

cooldown_storage = {}

def cooldown(action_type: str, seconds: int = 5):
    def decorator(func):
        @wraps(func)
        async def wrapper(update, context):
            user_id = update.effective_user.id
            chat_id = update.effective_chat.id
            key = (user_id, action_type)
            now = time.time()

            if key in cooldown_storage and now - cooldown_storage[key] < seconds:
                msg_key = f"cooldown_{action_type}"
                await update.message.reply_text(tr(chat_id, msg_key))
                return

            cooldown_storage[key] = now
            return await func(update, context)
        return wrapper
    return decorator





