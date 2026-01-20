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

# Все каналы для подписки (теперь 7 каналов)
CHANNEL_LINKS = [
    ("📢 Канал 1", "https://t.me/+m_mlxM7IlFk1MGRi"),
    ("📢 Канал 2", "https://t.me/+CYjeLBGTzjRhYjY6"),
    ("📢 Канал 3", "https://t.me/+6M0_d3RtYFs1NWUy"),
    ("📢 Канал 4", "https://t.me/+_PnxbVSghKVmM2Y6"),
    ("📢 Канал 5", "https://t.me/+QHnpKS09KtRjNTgy"),
    ("📢 Канал 6", "https://t.me/+r5haWSZxlCg0MzZk"),
    ("📢 Канал 7", "https://t.me/solntsevpage")  # Последний публичный канал
]

# ID всех каналов (последний публичный по юзернейму)
CHANNEL_IDS = [
    -1003265823270,  # Канал 1
    -1003082454363,  # Канал 2
    -1003536146111,  # Канал 3
    -1003080893872,  # Канал 4
    -1002999004769,  # Канал 5
    -1003067663410,  # Канал 6
    "@solntsevpage"  # Канал 7 (публичный по юзернейму)
]

async def check_subscription(user_id, context):
    """Проверка подписки на все каналы"""
    try:
        subscribed_channels = 0
        total_channels = len(CHANNEL_IDS)
        
        for i, channel_id in enumerate(CHANNEL_IDS, 1):
            try:
                member = await context.bot.get_chat_member(chat_id=channel_id, user_id=user_id)
                if member.status in ['member', 'administrator', 'creator']:
                    subscribed_channels += 1
                    logger.info(f"✓ Канал {i}: подписан")
                else:
                    logger.info(f"✗ Канал {i}: не подписан (статус: {member.status})")
            except Exception as e:
                error_msg = str(e)
                if "USER_NOT_PARTICIPANT" in error_msg or "user not found" in error_msg.lower():
                    logger.info(f"✗ Канал {i}: не подписан")
                elif "Chat not found" in error_msg:
                    logger.warning(f"⚠ Канал {i}: не найден (бот не админ?)")
                elif "Forbidden" in error_msg:
                    logger.warning(f"⚠ Канал {i}: нет доступа (бот не админ)")
                else:
                    logger.error(f"⚠ Канал {i}: ошибка {error_msg}")
        
        # Требуется подписка на ВСЕ каналы
        result = subscribed_channels == total_channels
        logger.info(f"Подписан на {subscribed_channels}/{total_channels} каналов: {'✅ ДОСТУП' if result else '❌ НЕТ ДОСТУПА'}")
        return result
        
    except Exception as e:
        logger.error(f"Общая ошибка проверки подписки: {e}")
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
    
    # Проверка подписки на все каналы
    is_subscribed = await check_subscription(user_id, context)
    
    if not is_subscribed:
        # Создаем кнопки для всех каналов (максимум 8 кнопок в ряду для лучшего отображения)
        keyboard = []
        for name, link in CHANNEL_LINKS:
            keyboard.append([InlineKeyboardButton(name, url=link)])
        keyboard.append([InlineKeyboardButton("🔄 Проверить подписку", callback_data='force_check')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message_text = (
            "🔒 ДЛЯ ДОСТУПА ПОДПИШИСЬ НА ВСЕ 7 КАНАЛОВ!\n\n"
            "📌 После подписки нажми 'Проверить подписку'"
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
            # Создаем кнопки для всех каналов
            keyboard = []
            for name, link in CHANNEL_LINKS:
                keyboard.append([InlineKeyboardButton(name, url=link)])
            keyboard.append([InlineKeyboardButton("🔄 Проверить подписку", callback_data='force_check')])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            message_text = (
                "❌ ТЫ НЕ ПОДПИСАН НА ВСЕ 7 КАНАЛОВ!\n\n"
                "Требуется подписка на все каналы.\n"
                "Подпишись и попробуй снова."
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
    print("БОТ ЗАПУЩЕН С 7 КАНАЛАМИ")
    print(f"Всего каналов для подписки: {len(CHANNEL_IDS)}")
    print("Требуется подписка на ВСЕ 7 каналов")
    print("=" * 60)
    print("ВАЖНОЕ ЗАМЕЧАНИЕ:")
    print("1. Для приватных каналов (1-6) бот должен быть АДМИНИСТРАТОРОМ")
    print("2. Для публичного канала (7) бот может проверять без прав админа")
    print("3. Добавь бота @Snoztt_bot как админа в каналы 1-6")
    print("=" * 60)
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username))
    
    application.run_polling(allowed_updates=None)

if __name__ == '__main__':
    main()
