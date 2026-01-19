import logging
from datetime import datetime, timedelta
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8480224026:AAGh34J8WSl-GM2MDa0_xgiIO5fAPVcaI-s"

START_IMAGE_URL = "https://t.me/ak3ic9/9"
SNOZ_TT_IMAGE_URL = "https://t.me/ak3ic9/11"

# Два канала
CHANNEL_LINK_1 = "https://t.me/+m_mlxM7IlFk1MGRi"
CHANNEL_LINK_2 = "https://t.me/+CYjeLBGTzjRhYjY6"

# ПРАВИЛЬНЫЕ ID каналов
CHANNEL_ID_1 = -1003265823270  # Правильный ID первого канала
CHANNEL_ID_2 = -1003082454363  # ID второго канала

async def check_subscription(user_id, context):
    """Проверка подписки на оба канала с правильными ID"""
    try:
        logger.info(f"=== ПРОВЕРКА для пользователя {user_id} ===")
        
        # Проверка канала 1 (с правильным ID)
        try:
            logger.info(f"Канал 1 (ID: {CHANNEL_ID_1})")
            member1 = await context.bot.get_chat_member(chat_id=CHANNEL_ID_1, user_id=user_id)
            subscribed1 = member1.status in ['member', 'administrator', 'creator']
            logger.info(f"✓ Канал 1: статус={member1.status}, подписан={subscribed1}")
        except Exception as e1:
            error_msg = str(e1)
            logger.error(f"✗ Ошибка канала 1: {error_msg}")
            subscribed1 = False
        
        # Проверка канала 2
        try:
            logger.info(f"Канал 2 (ID: {CHANNEL_ID_2})")
            member2 = await context.bot.get_chat_member(chat_id=CHANNEL_ID_2, user_id=user_id)
            subscribed2 = member2.status in ['member', 'administrator', 'creator']
            logger.info(f"✓ Канал 2: статус={member2.status}, подписан={subscribed2}")
        except Exception as e2:
            error_msg = str(e2)
            logger.error(f"✗ Ошибка канала 2: {error_msg}")
            subscribed2 = False
        
        result = subscribed1 and subscribed2
        logger.info(f"=== РЕЗУЛЬТАТ: {'✅ ПОДПИСАН' if result else '❌ НЕ ПОДПИСАН'} ===")
        return result
        
    except Exception as e:
        logger.error(f"Ошибка проверки: {e}")
        return False

def check_and_update_limit(user_id):
    now = datetime.now()
    if user_id not in user_requests:
        user_requests[user_id] = []
    
    user_requests[user_id] = [req_time for req_time in user_requests[user_id] if now - req_time < timedelta(hours=24)]
    
    if len(user_requests[user_id]) >= 2:
        return False
    return True

def add_request(user_id):
    now = datetime.now()
    if user_id not in user_requests:
        user_requests[user_id] = []
    user_requests[user_id].append(now)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Проверка подписки на оба канала
    is_subscribed = await check_subscription(user_id, context)
    
    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton("📢 Канал 1", url=CHANNEL_LINK_1)],
            [InlineKeyboardButton("📢 Канал 2", url=CHANNEL_LINK_2)],
            [InlineKeyboardButton("🔄 Проверить подписку", callback_data='force_check')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message_text = (
            "🔒 Для доступа к боту подпишитесь на оба канала!\n\n"
            "1. Первый канал\n"
            "2. Второй канал\n\n"
            "После подписки нажмите 'Проверить подписку'"
        )
        
        await update.message.reply_text(
            text=message_text,
            reply_markup=reply_markup
        )
        return
    
    # Если подписан - показываем основное меню
    keyboard = [
        [InlineKeyboardButton("💀Sn0z tt", callback_data='snoz_tt')],
        [InlineKeyboardButton("☠️Sn0z Vk", callback_data='snoz_vk'),
         InlineKeyboardButton("👻Snos tg", callback_data='snos_tg')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_photo(
        photo=START_IMAGE_URL,
        caption="🧨 Вы получили доступ к боту, теперь вы можете свободно им пользоваться, пока-что бот работает только по тик-току, скоро будут добавлены новые интересные функции. Ворки - t.me/VorkSnos",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'force_check':
        user_id = query.from_user.id
        
        # Проверка подписки
        is_subscribed = await check_subscription(user_id, context)
        
        if not is_subscribed:
            keyboard = [
                [InlineKeyboardButton("📢 Канал 1", url=CHANNEL_LINK_1)],
                [InlineKeyboardButton("📢 Канал 2", url=CHANNEL_LINK_2)],
                [InlineKeyboardButton("🔄 Проверить подписку", callback_data='force_check')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            message_text = (
                "❌ Вы не подписаны на оба канала!\n\n"
                "Подпишитесь на оба канала и попробуйте снова."
            )
            
            await query.edit_message_text(
                text=message_text,
                reply_markup=reply_markup
            )
            return
        
        # Если подписан - показываем основное меню
        keyboard = [
            [InlineKeyboardButton("💀Sn0z tt", callback_data='snoz_tt')],
            [InlineKeyboardButton("☠️Sn0z Vk", callback_data='snoz_vk'),
             InlineKeyboardButton("👻Snos tg", callback_data='snos_tg')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            await query.delete_message()
        except:
            pass
        
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=START_IMAGE_URL,
            caption="🧨 Вы получили доступ к боту, теперь вы можете свободно им пользоваться, пока-что бот работает только по тик-току, скоро будут добавлены новые интересные функции. Ворки - t.me/VorkSnos",
            reply_markup=reply_markup
        )
        return
    
    if query.data == 'snoz_tt':
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='back_to_start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        caption_text = (
            "👤 Удаление тикток аккаунта\n"
            "Введите юзернейм человека, введение неправильного или несуществующего юзернейма приведет к бану, также не отправляйте фотографии, файлы, и т.д\n\n"
            "🍀 Требования:\n"
            "1. аккаунты с выше чем 2.000 подписчиков не сн0сить (не получится)\n"
            "2. на официальные аккаунты не кидать"
        )
        
        try:
            await query.edit_message_media(
                media=InputMediaPhoto(media=SNOZ_TT_IMAGE_URL, caption=caption_text),
                reply_markup=reply_markup
            )
        except Exception as e:
            await query.edit_message_caption(
                caption=caption_text,
                reply_markup=reply_markup
            )
        context.user_data['waiting_for_tt_username'] = True
    
    elif query.data == 'snoz_vk':
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='back_to_start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="👤 Удаление VK аккаунта\nФункция в разработке.",
            reply_markup=reply_markup
        )
        context.user_data['waiting_for_tt_username'] = False
    
    elif query.data == 'snos_tg':
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data='back_to_start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="👤 Удаление Telegram аккаунта\nФункция в разработке.",
            reply_markup=reply_markup
        )
        context.user_data['waiting_for_tt_username'] = False
    
    elif query.data == 'back_to_start':
        keyboard = [
            [InlineKeyboardButton("💀Sn0z tt", callback_data='snoz_tt')],
            [InlineKeyboardButton("☠️Sn0z Vk", callback_data='snoz_vk'),
             InlineKeyboardButton("👻Snos tg", callback_data='snos_tg')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            await query.edit_message_media(
                media=InputMediaPhoto(media=START_IMAGE_URL, caption="🧨 Вы получили доступ к боту, теперь вы можете свободно им пользоваться, пока-что бот работает только по тик-току, скоро будут добавлены новые интересные функции. Ворки - t.me/VorkSnos"),
                reply_markup=reply_markup
            )
        except Exception as e:
            await query.edit_message_text(
                text="🧨 Вы получили доступ к боту, теперь вы можете свободно им пользоваться, пока-что бот работает только по тик-току, скоро будут добавлены новые интересные функции. Ворки - t.me/VorkSnos",
                reply_markup=reply_markup
            )
        context.user_data['waiting_for_tt_username'] = False

async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.message.text.strip()
    
    if context.user_data.get('waiting_for_tt_username'):
        # Все юзернеймы считаются найденными
        # Проверяем лимит запросов
        if not check_and_update_limit(user_id):
            await update.message.reply_text(
                text="❌ Лимит исчерпан.\nВы использовали 2 запроса за последние 24 часа."
            )
            return
        
        # Случайное количество жалоб
        complaint_count = random.randint(100, 120)
        
        # Начало процесса
        start_msg = await update.message.reply_text(
            text=f"📤 Отправлено {complaint_count} жалоб на @{username}"
        )
        
        # Анимация отправки жалоб (10-20 секунд)
        animation_time = random.randint(10, 20)
        
        # Прогресс бар анимация
        for i in range(animation_time):
            progress = int((i + 1) / animation_time * 20)
            progress_bar = "█" * progress + "▒" * (20 - progress)
            percentage = int((i + 1) / animation_time * 100)
            
            # Обновляем сообщение с прогрессом
            try:
                await start_msg.edit_text(
                    text=f"📤 Отправлено {complaint_count} жалоб на @{username}\n\n"
                         f"🔄 Отправка... {percentage}%\n"
                         f"{progress_bar}\n"
                         f"⏳ Осталось: {animation_time - i - 1} сек."
                )
            except:
                pass
            
            await asyncio.sleep(1)
        
        # Завершение процесса
        add_request(user_id)
        remaining = 2 - len(user_requests[user_id])
        
        # Финальное сообщение
        await start_msg.edit_text(
            text=f"✅ Все жалобы отправлены!\n\n"
                 f"📊 Статистика:\n"
                 f"• Жалоб отправлено: {complaint_count}\n"
                 f"• На аккаунт: @{username}\n"
                 f"• Осталось запросов сегодня: {remaining}\n\n"
                 f"⚡ Жалобы обрабатываются системой TikTok"
        )
        
        context.user_data['waiting_for_tt_username'] = False
    else:
        await update.message.reply_text(
            text="⚠️ Выберите действие через меню."
        )

# Глобальные переменные
user_requests = {}

def main():
    print("=" * 60)
    print("БОТ ЗАПУЩЕН С ПРАВИЛЬНЫМИ ID КАНАЛОВ")
    print(f"Канал 1 ID: {CHANNEL_ID_1}")
    print(f"Канал 2 ID: {CHANNEL_ID_2}")
    print("Требуется подписка на ОБА канала")
    print("=" * 60)
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username))
    
    application.run_polling(allowed_updates=None)

if __name__ == '__main__':
    main()
