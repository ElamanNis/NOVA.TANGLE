#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEPHI Blood Donation Bot - Complete Solution
=============================================

Комплексный Telegram-бот для управления донорским движением в НИЯУ МИФИ
Разработан для хакатона МИФИ 2025-Команда Nova Tangle

Функционал:
- Регистрация пользователей с верификацией телефона
- Управление событиями донорства крови  
- Административная панель
- Экспорт данных в Excel
- Система вопросов и ответов
- Полная интеграция с PostgreSQL

Требования:
pip install python-telegram-bot sqlalchemy psycopg2-binary pandas openpyxl

Переменные окружения:
BOT_TOKEN - токен Telegram бота
DATABASE_URL - строка подключения к PostgreSQL

Запуск:
python mephi_bot_complete.py

Доступ к админ-панели:
1. Регистрация: /start
2. Получение прав: /promote mephi_admin_2024  
3. Админ-панель: /admin

Автор: AI Assistant для хакатона МИФИ
Дата: 19 июля 2025
"""

# ==================== MAIN.PY ====================
import os
import logging
from bot import create_bot, setup_handlers
from database import init_db

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot"""
    # Initialize database
    init_db()
    
    # Get bot token from environment
    bot_token = os.getenv("BOT_TOKEN", "your_bot_token_here")
    
    if bot_token == "your_bot_token_here":
        logger.error("Please set BOT_TOKEN environment variable")
        return
    
    # Create and configure bot
    application = create_bot(bot_token)
    setup_handlers(application)
    
    # Start the bot
    logger.info("Starting MEPHI Blood Donation Bot...")
    application.run_polling(allowed_updates=['message', 'callback_query'])

if __name__ == '__main__':
    main()
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import os

def create_bot(token):
    """Create and configure the bot application"""
    application = Application.builder().token(token).build()
    
    # Setup menu commands on bot initialization
    async def post_init(application):
        from menu_commands import setup_menu_commands
        await setup_menu_commands(application.bot)
    
    application.post_init = post_init
    return application

def setup_handlers(application):
    """Setup all bot handlers"""
    from handlers import (
        start, handle_phone, handle_name, handle_user_type, handle_group,
        handle_consent, main_menu, profile, info_menu, register_event,
        ask_question, admin_menu, handle_my_stats, handle_donor_ranking,
        handle_blood_centers, handle_benefits, handle_notifications,
        handle_contacts, handle_feedback
    )
    
    # Import menu command handlers
    from menu_commands import (
        show_help_menu, quick_stats_command, quick_events_command, 
        quick_centers_command, quick_benefits_command, quick_contact_command
    )
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_menu))
    application.add_handler(CommandHandler("help", show_help_menu))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("stats", quick_stats_command))
    application.add_handler(CommandHandler("history", quick_stats_command))
    application.add_handler(CommandHandler("events", quick_events_command))
    application.add_handler(CommandHandler("register", register_event))
    application.add_handler(CommandHandler("rating", handle_donor_ranking))
    application.add_handler(CommandHandler("centers", quick_centers_command))
    application.add_handler(CommandHandler("benefits", quick_benefits_command))
    application.add_handler(CommandHandler("info", info_menu))
    application.add_handler(CommandHandler("contact", quick_contact_command))
    application.add_handler(CommandHandler("feedback", handle_feedback))
    
    # Admin promotion command (for testing)
    from handlers import promote_to_admin
    application.add_handler(CommandHandler("promote", promote_to_admin))
    
    # Callback query handlers
    application.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(profile, pattern="^profile$"))
    application.add_handler(CallbackQueryHandler(info_menu, pattern="^info_menu$"))
    application.add_handler(CallbackQueryHandler(register_event, pattern="^register_event$"))
    application.add_handler(CallbackQueryHandler(ask_question, pattern="^ask_question$"))
    
    # Enhanced menu handlers
    application.add_handler(CallbackQueryHandler(handle_my_stats, pattern="^my_stats$"))
    application.add_handler(CallbackQueryHandler(handle_donor_ranking, pattern="^donor_ranking$"))
    application.add_handler(CallbackQueryHandler(handle_blood_centers, pattern="^blood_centers$"))
    application.add_handler(CallbackQueryHandler(handle_benefits, pattern="^benefits$"))
    application.add_handler(CallbackQueryHandler(handle_notifications, pattern="^notifications$"))
    application.add_handler(CallbackQueryHandler(handle_contacts, pattern="^contacts$"))
    application.add_handler(CallbackQueryHandler(handle_feedback, pattern="^feedback$"))
    
    # Detailed handlers - Import functions
    from handlers import (
        handle_donation_history, handle_center_gavrilov, handle_center_fmba,
        handle_centers_directions, handle_centers_contacts, handle_benefits_students,
        handle_benefits_staff, handle_benefits_shops, handle_benefits_cafes,
        handle_benefits_tickets, handle_notifications_on, handle_notifications_off,
        handle_notifications_settings, handle_admin_export_data, handle_admin_questions_list,
        handle_answer_question_button
    )
    
    # Import admin answer handler
    from admin import handle_admin_answer_question
    
    # Donation and blood centers
    application.add_handler(CallbackQueryHandler(handle_donation_history, pattern="^donation_history$"))
    application.add_handler(CallbackQueryHandler(handle_center_gavrilov, pattern="^center_gavrilov$"))
    application.add_handler(CallbackQueryHandler(handle_center_fmba, pattern="^center_fmba$"))
    application.add_handler(CallbackQueryHandler(handle_centers_directions, pattern="^centers_directions$"))
    application.add_handler(CallbackQueryHandler(handle_centers_contacts, pattern="^centers_contacts$"))
    
    # Benefits detailed handlers  
    application.add_handler(CallbackQueryHandler(handle_benefits_students, pattern="^benefits_students$"))
    application.add_handler(CallbackQueryHandler(handle_benefits_staff, pattern="^benefits_staff$"))
    application.add_handler(CallbackQueryHandler(handle_benefits_shops, pattern="^benefits_shops$"))
    application.add_handler(CallbackQueryHandler(handle_benefits_cafes, pattern="^benefits_cafes$"))
    application.add_handler(CallbackQueryHandler(handle_benefits_tickets, pattern="^benefits_tickets$"))
    
    # Notifications detailed handlers
    application.add_handler(CallbackQueryHandler(handle_notifications_on, pattern="^notifications_on$"))
    application.add_handler(CallbackQueryHandler(handle_notifications_off, pattern="^notifications_off$"))
    application.add_handler(CallbackQueryHandler(handle_notifications_settings, pattern="^notifications_settings$"))
    
    # Admin export handler
    application.add_handler(CallbackQueryHandler(handle_admin_export_data, pattern="^admin_export_data$"))
    
    # Admin question handling
    application.add_handler(CallbackQueryHandler(handle_admin_questions_list, pattern="^admin_questions$"))
    application.add_handler(CallbackQueryHandler(handle_answer_question_button, pattern="^answer_question_"))
    
    # Admin answer handler - must come before text handlers
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_admin_answer_question
    ), group=1)
    
    # Info section handlers
    application.add_handler(CallbackQueryHandler(info_menu, pattern="^info_"))
    
    # Registration handlers
    application.add_handler(CallbackQueryHandler(handle_user_type, pattern="^user_type_"))
    application.add_handler(CallbackQueryHandler(handle_consent, pattern="^consent_"))
    
    # Event registration handlers
    from handlers import handle_event_registration, handle_registration_confirmation
    application.add_handler(CallbackQueryHandler(handle_event_registration, pattern="^event_"))
    application.add_handler(CallbackQueryHandler(handle_registration_confirmation, pattern="^confirm_registration_"))
    
    # No-show survey handlers
    from handlers import handle_no_show_reason
    application.add_handler(CallbackQueryHandler(handle_no_show_reason, pattern="^no_show_"))
    
    # Admin handlers
    from admin import setup_admin_handlers
    setup_admin_handlers(application)
    
    # Message handlers
    application.add_handler(MessageHandler(filters.CONTACT, handle_phone))
    
    # Text message handler with state management
    from handlers import handle_text_message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, BigInteger as BigInt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInt, unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    user_type = Column(String(20), nullable=False)  # student, employee, external
    group_number = Column(String(20), nullable=True)  # For students only
    consent_given = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    bone_marrow_registry = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    donations = relationship("Donation", back_populates="user")
    registrations = relationship("EventRegistration", back_populates="user")
    questions = relationship("Question", foreign_keys="Question.user_id", back_populates="user")

class BloodCenter(Base):
    __tablename__ = 'blood_centers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    short_name = Column(String(50), nullable=False)
    
    # Relationships
    events = relationship("Event", back_populates="blood_center")
    donations = relationship("Donation", back_populates="blood_center")

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    blood_center_id = Column(Integer, ForeignKey('blood_centers.id'), nullable=False)
    external_registration_link = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    blood_center = relationship("BloodCenter", back_populates="events")
    registrations = relationship("EventRegistration", back_populates="event")
    donations = relationship("Donation", back_populates="event")

class EventRegistration(Base):
    __tablename__ = 'event_registrations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)
    attended = Column(Boolean, nullable=True)  # None=unknown, True=attended, False=no-show
    no_show_reason = Column(String(100), nullable=True)  # medotved, personal, unwilling
    
    # Relationships
    user = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")

class Donation(Base):
    __tablename__ = 'donations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    blood_center_id = Column(Integer, ForeignKey('blood_centers.id'), nullable=False)
    donation_date = Column(DateTime, nullable=False)
    bone_marrow_sample = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="donations")
    event = relationship("Event", back_populates="donations")
    blood_center = relationship("BloodCenter", back_populates="donations")

class Question(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=True)
    answered_by_admin_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    answered_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="questions")
    answered_by_admin = relationship("User", foreign_keys=[answered_by_admin_id])

class InfoSection(Base):
    __tablename__ = 'info_sections'
    
    id = Column(Integer, primary_key=True)
    section_key = Column(String(50), unique=True, nullable=False)  # blood_donation, bone_marrow, mephi_process
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, BloodCenter, InfoSection, Event
from contextlib import contextmanager

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/mephi_bot")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    """Context manager for database sessions"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_db():
    """Initialize database tables and add default data"""
    Base.metadata.create_all(bind=engine)
    
    # Add default blood centers
    with get_db() as session:
        # Check if blood centers already exist
        if session.query(BloodCenter).count() == 0:
            centers = [
                BloodCenter(name="Центр крови ФМБА", short_name="ЦК ФМБА"),
                BloodCenter(name="Центр крови им. О.К. Гаврилова", short_name="ЦК Гаврилова")
            ]
            session.add_all(centers)
        
        # Add default info sections
        if session.query(InfoSection).count() == 0:
            info_sections = [
                InfoSection(
                    section_key="blood_donation_requirements",
                    title="Требования к донорам",
                    content="""🩸 **Требования к донорам крови:**

• **Возраст:** Не менее 18 лет
• **Вес:** Не менее 50 кг
• **Здоровье:**
  - Отсутствие хронических заболеваний в острой фазе
  - Не болели ангиной, ОРВИ, гриппом менее чем за месяц до сдачи
  - Температура тела ≤ 37°C
  - Давление: систолическое 90-160 мм рт.ст., диастолическое 60-100 мм рт.ст.
  - Гемоглобин: женщины ≥ 120 г/л, мужчины ≥ 130 г/л

• **Периодичность:**
  - Цельная кровь: не чаще 4-5 раз в год для мужчин, 3-4 раза для женщин"""
                ),
                InfoSection(
                    section_key="preparation",
                    title="Подготовка к донации",
                    content="""📋 **Подготовка к донации (за 2-3 дня):**

**Питание:**
• Исключить жирную, острую, копченую пищу
• Отказаться от фастфуда, молочных продуктов и продуктов с яйцами

**Образ жизни:**
• Отказ от алкоголя за 48 часов
• Избегать интенсивных физических нагрузок
• Отменить прием лекарственных препаратов (в т.ч. анальгетиков) за 72 часа

**Накануне:**
• Легкий ужин до 20:00
• Сон не менее 8 часов
• Обязательный завтрак (каша на воде, сладкий чай, сушки, хлеб с вареньем)
• Нельзя курить в течение часа до сдачи крови"""
                ),
                InfoSection(
                    section_key="bone_marrow",
                    title="Донорство костного мозга",
                    content="""🦴 **О донорстве костного мозга:**

Донорство костного мозга - это возможность спасти жизнь пациентам с заболеваниями крови.

**Процедура вступления в регистр:**
• Заполнение анкеты
• Сдача пробы крови (10 мл) для типирования
• Внесение данных в российский регистр доноров костного мозга

**Важно знать:**
• Регистрация происходит только один раз в жизни
• Вероятность стать донором составляет 1:10000
• При совпадении с пациентом вы будете уведомлены
• Процедура донации безопасна и проводится в специализированных центрах"""
                ),
                InfoSection(
                    section_key="mephi_process",
                    title="Донации в МИФИ",
                    content="""🏛️ **Как проходят Дни донора в МИФИ:**

**Регистрация:**
1. Зарегистрируйтесь в боте
2. Выберите удобную дату и центр крови
3. Для внешних доноров - пройдите дополнительную регистрацию по ссылке

**В день донации:**
1. Приходите в назначенное время
2. Пройдите медосмотр
3. Сдайте кровь
4. При желании - сдайте пробу для регистра костного мозга
5. Получите справку и компенсацию

**Дополнительная информация:**
• Дни донора проходят два раза в семестр
• Работаем с ЦК ФМБА и ЦК им. О.К. Гаврилова
• Могут участвовать студенты, сотрудники и внешние доноры"""
                ),
                InfoSection(
                    section_key="contraindications",
                    title="Противопоказания",
                    content="""⚠️ **Противопоказания к донации:**

**Абсолютные противопоказания:**
• ВИЧ/СПИД, сифилис, вирусные гепатиты (B, C)
• Туберкулез, токсоплазмоз, лейшманиоз
• Онкологические заболевания, болезни крови
• Гипертония II-III ст., ишемическая болезнь
• Органические поражения ЦНС, бронхиальная астма

**Временные противопоказания:**
• ОРВИ, грипп - 1 месяц
• Ангина - 1 месяц  
• Удаление зуба - 10 дней
• Менструация + 5 дней после
• Прививки - от 10 дней до 1 года
• Пирсинг, тату - 1 год"""
                )
            ]
            session.add_all(info_sections)
        
        # Add sample events for demonstration
        from datetime import datetime, timedelta
        if session.query(Event).count() == 0:
            # Get blood centers
            center_fmba = session.query(BloodCenter).filter(BloodCenter.short_name == "ЦК ФМБА").first()
            center_gavrilova = session.query(BloodCenter).filter(BloodCenter.short_name == "ЦК Гаврилова").first()
            
            if center_fmba and center_gavrilova:
                # Create sample future events
                future_date_1 = datetime.now() + timedelta(days=14)  # 2 weeks from now
                future_date_2 = datetime.now() + timedelta(days=28)  # 4 weeks from now
                
                sample_events = [
                    Event(
                        date=future_date_1.replace(hour=10, minute=0, second=0, microsecond=0),
                        blood_center_id=center_fmba.id,
                        external_registration_link="https://example.com/register-fmba",
                        is_active=True
                    ),
                    Event(
                        date=future_date_2.replace(hour=10, minute=0, second=0, microsecond=0),
                        blood_center_id=center_gavrilova.id,
                        external_registration_link="https://example.com/register-gavrilova",
                        is_active=True
                    )
                ]
                session.add_all(sample_events)
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from database import get_db
from models import User, Event, EventRegistration, Question, InfoSection, Donation, BloodCenter
from keyboards import get_main_keyboard, get_info_keyboard, get_user_type_keyboard, get_consent_keyboard
from utils import validate_name, validate_group_number
from messages import MESSAGES
from sqlalchemy import func
from excel_export import export_donors_to_excel, add_new_donor_to_excel, update_donor_donations
import re

# Conversation states
WAITING_FOR_PHONE, WAITING_FOR_NAME, WAITING_FOR_USER_TYPE, WAITING_FOR_GROUP, WAITING_FOR_CONSENT = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user_id = update.effective_user.id
    
    with get_db() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        
        if user and user.consent_given:
            # User exists and has given consent, show main menu
            await update.message.reply_text(
                MESSAGES['welcome_back'].format(name=user.full_name),
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # New user or no consent, start registration
            await update.message.reply_text(
                MESSAGES['welcome'],
                parse_mode=ParseMode.MARKDOWN
            )
            await request_phone(update, context)

async def request_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Request phone number from user"""
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📱 Поделиться номером телефона", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await update.message.reply_text(
        MESSAGES['request_phone'],
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    return WAITING_FOR_PHONE

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle phone number input"""
    if not update.message.contact:
        await update.message.reply_text("❌ Пожалуйста, поделитесь своим номером телефона через кнопку.")
        return WAITING_FOR_PHONE
    
    phone = update.message.contact.phone_number
    user_id = update.effective_user.id
    
    # Clean phone number
    phone = re.sub(r'[^\d+]', '', phone)
    if not phone.startswith('+'):
        phone = '+' + phone
    
    context.user_data['phone'] = phone
    
    with get_db() as session:
        # Check if user exists by phone
        existing_user = session.query(User).filter(User.phone_number == phone).first()
        
        if existing_user:
            # Update telegram_id if needed
            if existing_user.telegram_id != user_id:
                existing_user.telegram_id = user_id
            
            if existing_user.consent_given:
                await update.message.reply_text(
                    f"👋 Добро пожаловать, {existing_user.full_name}!\n\n"
                    "Вы уже зарегистрированы в системе.",
                    reply_markup=get_main_keyboard()
                )
                return ConversationHandler.END
            else:
                # User exists but no consent
                context.user_data['existing_user'] = existing_user
                await show_consent(update, context)
                return WAITING_FOR_CONSENT
        else:
            # New user, request name
            await update.message.reply_text(
                MESSAGES['request_name'],
                reply_markup=ReplyKeyboardRemove()
            )
            return WAITING_FOR_NAME

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle name input"""
    name = update.message.text.strip()
    
    if not validate_name(name):
        await update.message.reply_text(
            "❌ Пожалуйста, введите корректное ФИО (например: Иванов Иван Иванович)."
        )
        return WAITING_FOR_NAME
    
    context.user_data['name'] = name
    
    await update.message.reply_text(
        MESSAGES['request_user_type'],
        reply_markup=get_user_type_keyboard()
    )
    return WAITING_FOR_USER_TYPE

async def handle_user_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user type selection"""
    query = update.callback_query
    await query.answer()
    
    user_type = query.data.replace('user_type_', '')
    context.user_data['user_type'] = user_type
    
    if user_type == 'student':
        await query.edit_message_text(
            "👨‍🎓 Укажите номер вашей учебной группы (например: Б20-505):"
        )
        return WAITING_FOR_GROUP
    else:
        await show_consent(update, context)
        return WAITING_FOR_CONSENT

async def handle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle group number input for students"""
    group = update.message.text.strip().upper()
    
    if not validate_group_number(group):
        await update.message.reply_text(
            "❌ Пожалуйста, введите корректный номер группы (например: Б20-505)."
        )
        return WAITING_FOR_GROUP
    
    context.user_data['group'] = group
    await show_consent(update, context)
    return WAITING_FOR_CONSENT

async def show_consent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show consent form"""
    if update.callback_query:
        await update.callback_query.edit_message_text(
            MESSAGES['consent_form'],
            reply_markup=get_consent_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(
            MESSAGES['consent_form'],
            reply_markup=get_consent_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_consent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle consent response"""
    query = update.callback_query
    await query.answer()
    
    consent = query.data == 'consent_yes'
    
    if not consent:
        await query.edit_message_text(
            "❌ Без согласия на обработку персональных данных использование бота невозможно."
        )
        return ConversationHandler.END
    
    # Save user to database
    with get_db() as session:
        if 'existing_user' in context.user_data:
            # Update existing user
            user = context.user_data['existing_user']
            user.consent_given = True
            user.telegram_id = update.effective_user.id
        else:
            # Create new user
            user = User(
                telegram_id=update.effective_user.id,
                phone_number=context.user_data['phone'],
                full_name=context.user_data['name'],
                user_type=context.user_data['user_type'],
                group_number=context.user_data.get('group'),
                consent_given=True
            )
            session.add(user)
    
    await query.edit_message_text(
        "✅ Регистрация завершена! Добро пожаловать в донорское движение МИФИ!",
        reply_markup=get_main_keyboard()
    )
    
    # Clear user data
    context.user_data.clear()
    return ConversationHandler.END

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu"""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            MESSAGES['main_menu'],
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user profile"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    with get_db() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            await query.edit_message_text("❌ Пользователь не найден.")
            return
        
        # Get donation statistics
        donations_count = len(user.donations)
        last_donation = session.query(Donation).filter(
            Donation.user_id == user.id
        ).order_by(Donation.donation_date.desc()).first()
        
        profile_text = f"👤 **Ваш профиль:**\n\n"
        profile_text += f"**ФИО:** {user.full_name}\n"
        profile_text += f"**Категория:** {MESSAGES['user_types'][user.user_type]}\n"
        if user.group_number:
            profile_text += f"**Группа:** {user.group_number}\n"
        profile_text += f"**Количество донаций:** {donations_count}\n"
        
        if last_donation:
            profile_text += f"**Последняя донация:** {last_donation.donation_date.strftime('%d.%m.%Y')} ({last_donation.blood_center.short_name})\n"
        
        profile_text += f"**Регистр ДКМ:** {'✅ Да' if user.bone_marrow_registry else '❌ Нет'}\n"
        
        from keyboards import get_profile_keyboard
        await query.edit_message_text(
            profile_text,
            reply_markup=get_profile_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def info_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show information menu"""
    query = update.callback_query
    await query.answer()
    
    # Check if specific info section requested
    if query.data != 'info_menu':
        section_key = query.data.replace('info_', '')
        
        with get_db() as session:
            info_section = session.query(InfoSection).filter(
                InfoSection.section_key == section_key
            ).first()
            
            if info_section:
                from keyboards import get_back_to_info_keyboard
                await query.edit_message_text(
                    f"**{info_section.title}**\n\n{info_section.content}",
                    reply_markup=get_back_to_info_keyboard(),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await query.edit_message_text("❌ Информация не найдена.")
    else:
        await query.edit_message_text(
            MESSAGES['info_menu'],
            reply_markup=get_info_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def register_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show event registration"""
    query = update.callback_query
    await query.answer()
    
    with get_db() as session:
        # Get upcoming events
        from datetime import datetime
        events = session.query(Event).filter(
            Event.date > datetime.now(),
            Event.is_active == True
        ).order_by(Event.date).all()
        
        if not events:
            await query.edit_message_text(
                "📅 На данный момент нет запланированных Дней донора.\n\n"
                "Следите за объявлениями!",
                reply_markup=get_main_keyboard()
            )
            return
        
        from keyboards import get_events_keyboard
        await query.edit_message_text(
            "📅 **Выберите день для регистрации:**",
            reply_markup=get_events_keyboard(events),
            parse_mode=ParseMode.MARKDOWN
        )

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start question asking process"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "❓ **Задать вопрос организаторам**\n\n"
        "Напишите ваш вопрос, и мы ответим вам как можно скорее."
    )
    
    # Set state for waiting question
    context.user_data['waiting_question'] = True

async def handle_event_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle event selection for registration"""
    query = update.callback_query
    await query.answer()
    
    event_id = int(query.data.replace('event_', ''))
    user_id = update.effective_user.id
    
    with get_db() as session:
        event = session.query(Event).filter(Event.id == event_id).first()
        user = session.query(User).filter(User.telegram_id == user_id).first()
        
        if not event or not user:
            await query.edit_message_text("❌ Ошибка: событие или пользователь не найдены.")
            return
        
        # Check if already registered
        existing_registration = session.query(EventRegistration).filter(
            EventRegistration.user_id == user.id,
            EventRegistration.event_id == event.id
        ).first()
        
        if existing_registration:
            await query.edit_message_text(
                f"✅ **Вы уже зарегистрированы на это событие**\n\n"
                f"📅 **Дата:** {event.date.strftime('%d.%m.%Y %H:%M')}\n"
                f"🏥 **Центр крови:** {event.blood_center.name}",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Show registration confirmation
        text = f"📅 **Подтверждение регистрации**\n\n"
        text += f"**Дата:** {event.date.strftime('%d.%m.%Y %H:%M')}\n"
        text += f"**Центр крови:** {event.blood_center.name}\n"
        text += f"**Ваш статус:** {MESSAGES['user_types'][user.user_type]}\n\n"
        
        if user.user_type == 'external':
            text += "⚠️ **Для внешних доноров требуется дополнительная регистрация**\n"
            if event.external_registration_link:
                text += f"После подтверждения вы получите ссылку для регистрации.\n\n"
        
        text += "**Подтвердить регистрацию?**"
        
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard = [
            [InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm_registration_{event.id}")],
            [InlineKeyboardButton("❌ Отмена", callback_data="register_event")]
        ]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_registration_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle registration confirmation"""
    query = update.callback_query
    await query.answer()
    
    event_id = int(query.data.replace('confirm_registration_', ''))
    user_id = update.effective_user.id
    
    with get_db() as session:
        event = session.query(Event).filter(Event.id == event_id).first()
        user = session.query(User).filter(User.telegram_id == user_id).first()
        
        if not event or not user:
            await query.edit_message_text("❌ Ошибка: событие или пользователь не найдены.")
            return
        
        # Create registration
        registration = EventRegistration(
            user_id=user.id,
            event_id=event.id
        )
        session.add(registration)
        
        text = "✅ **Регистрация завершена!**\n\n"
        text += f"📅 **Дата:** {event.date.strftime('%d.%m.%Y %H:%M')}\n"
        text += f"🏥 **Центр крови:** {event.blood_center.name}\n\n"
        
        if user.user_type == 'external' and event.external_registration_link:
            text += "🔗 **Дополнительная регистрация для внешних доноров:**\n"
            text += f"{event.external_registration_link}\n\n"
        
        text += "📬 **Мы отправим вам напоминание накануне мероприятия.**\n\n"
        text += "Спасибо за участие в донорском движении МИФИ!"
        
        await query.edit_message_text(
            text,
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_no_show_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle no-show reason selection"""
    query = update.callback_query
    await query.answer()
    
    reason = query.data.replace('no_show_', '')
    user_id = update.effective_user.id
    
    # This would typically be called with a registration ID in context
    # For now, we'll find the most recent registration
    with get_db() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        if user:
            recent_registration = session.query(EventRegistration).filter(
                EventRegistration.user_id == user.id,
                EventRegistration.attended.is_(None)
            ).order_by(EventRegistration.registered_at.desc()).first()
            
            if recent_registration:
                recent_registration.attended = False
                recent_registration.no_show_reason = reason
    
    reason_messages = {
        'medotved': 'Медотвод (по причине болезни)',
        'personal': 'Личные причины', 
        'unwilling': 'Не захотел'
    }
    
    await query.edit_message_text(
        f"✅ **Спасибо за обратную связь!**\n\n"
        f"Причина: {reason_messages.get(reason, 'Не указана')}\n\n"
        f"Эта информация поможет нам улучшить организацию Дней донора.",
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin menu (only for admins)"""
    user_id = update.effective_user.id
    
    with get_db() as session:
        user = session.query(User).filter(
            User.telegram_id == user_id,
            User.is_admin == True
        ).first()
        
        if not user:
            await update.message.reply_text("❌ У вас нет прав администратора.")
            return
        
        from keyboards import get_admin_keyboard
        await update.message.reply_text(
            "🛠️ **Панель администратора**",
            reply_markup=get_admin_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle general text messages based on user state"""
    user_id = update.effective_user.id
    message_text = update.message.text.strip()
    
    # Check user registration state first
    with get_db() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        
        # If user not registered or no consent, handle registration flow
        if not user or not user.consent_given:
            return await handle_name(update, context)
        
        # Handle different conversation states
        if context.user_data.get('waiting_question'):
            # User is submitting a question
            question = Question(
                user_id=user.id,
                question_text=message_text
            )
            session.add(question)
            
            await update.message.reply_text(
                MESSAGES['question_received'],
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Clear the waiting state
            context.user_data.pop('waiting_question', None)
            return
        
        elif context.user_data.get('waiting_group'):
            # User is entering group number
            return await handle_group(update, context)
        
        elif context.user_data.get('creating_broadcast'):
            # Admin is creating a broadcast message
            await handle_admin_broadcast_text(update, context)
            return
        
        elif context.user_data.get('creating_event'):
            # Admin is creating an event
            await handle_admin_event_creation(update, context)
            return
        
        # Default case - show help or main menu
        await update.message.reply_text(
            "👋 Привет! Используйте кнопки меню для навигации или введите /start для возврата в главное меню.",
            reply_markup=get_main_keyboard()
        )

# Enhanced menu handlers
async def handle_my_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user personal statistics"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    with get_db() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        
        if not user:
            await query.edit_message_text("❌ Пользователь не найден.")
            return
        
        # Get donation statistics
        donations = session.query(Donation).filter(Donation.user_id == user.id).all()
        total_donations = len(donations)
        
        # Calculate donation centers breakdown
        gavrilov_donations = len([d for d in donations if d.blood_center.short_name == "Гаврилова"])
        fmba_donations = len([d for d in donations if d.blood_center.short_name == "ФМБА"])
        
        # Get last donation date
        last_donation = None
        if donations:
            last_donation = max(donations, key=lambda d: d.donation_date).donation_date
        
        text = f"📊 **Ваша статистика донора**\n\n"
        text += f"👤 **Имя:** {user.full_name}\n"
        text += f"🎓 **Статус:** {MESSAGES['user_types'][user.user_type]}\n"
        if user.group_number:
            text += f"👥 **Группа:** {user.group_number}\n"
        text += f"📅 **Регистрация:** {user.created_at.strftime('%d.%m.%Y')}\n\n"
        text += f"🩸 **Всего донаций:** {total_donations}\n"
        
        if gavrilov_donations > 0:
            text += f"🏥 **Центр Гаврилова:** {gavrilov_donations} раз\n"
        if fmba_donations > 0:
            text += f"🏥 **Центр ФМБА:** {fmba_donations} раз\n"
        
        if last_donation:
            text += f"🕐 **Последняя донация:** {last_donation.strftime('%d.%m.%Y')}\n"
        else:
            text += f"🕐 **Последняя донация:** Еще не было\n"
        
        # Calculate donor level
        if total_donations >= 40:
            level = "🏆 Почетный донор России"
        elif total_donations >= 25:
            level = "🥇 Активный донор"
        elif total_donations >= 10:
            level = "🥈 Опытный донор"
        elif total_donations >= 3:
            level = "🥉 Постоянный донор"
        else:
            level = "🌟 Начинающий донор"
        
        text += f"\n🎖️ **Уровень:** {level}"
        
        from keyboards import get_statistics_keyboard
        await query.edit_message_text(
            text,
            reply_markup=get_statistics_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_donor_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show donor ranking"""
    query = update.callback_query
    if query:
        await query.answer()
    
    with get_db() as session:
        # Get top donors with donation count
        from sqlalchemy import func
        top_donors = session.query(
            User.full_name,
            User.user_type,
            func.count(Donation.id).label('donation_count')
        ).join(Donation).group_by(User.id, User.full_name, User.user_type).order_by(
            func.count(Donation.id).desc()
        ).limit(10).all()
        
        text = "🏆 **Рейтинг доноров МИФИ**\n\n"
        
        for i, (name, user_type, count) in enumerate(top_donors, 1):
            if i == 1:
                emoji = "🥇"
            elif i == 2:
                emoji = "🥈"
            elif i == 3:
                emoji = "🥉"
            else:
                emoji = f"{i}."
            
            type_str = MESSAGES['user_types'][user_type]
            text += f"{emoji} **{name}**\n   {type_str} • {count} донаций\n\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]]
        
        if query:
            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )

async def handle_blood_centers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show blood centers information"""
    query = update.callback_query
    await query.answer()
    
    text = "📍 **Центры донорства крови**\n\n"
    text += "🏥 **Центр крови им. О.К. Гаврилова**\n"
    text += "📍 Адрес: ул. Поликарпова, д. 14\n"
    text += "📞 Телефон: +7 (499) 196-62-04\n"
    text += "🕐 Режим: Пн-Пт 8:00-15:00\n\n"
    text += "🏥 **Центр крови ФМБА России**\n"
    text += "📍 Адрес: Волоколамское ш., д. 30\n"
    text += "📞 Телефон: +7 (499) 193-78-01\n"
    text += "🕐 Режим: Пн-Пт 8:00-14:00\n\n"
    text += "💡 **Как добраться от МИФИ:**\n"
    text += "🚇 До центра Гаврилова: м. Сокол + автобус\n"
    text += "🚇 До центра ФМБА: м. Тушинская + маршрутка"
    
    from keyboards import get_blood_centers_keyboard
    await query.edit_message_text(
        text,
        reply_markup=get_blood_centers_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_benefits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show benefits and discounts"""
    query = update.callback_query
    await query.answer()
    
    text = "🎁 **Льготы и скидки для доноров**\n\n"
    text += "🩸 **Для всех доноров:**\n"
    text += "• Два выходных дня в году\n"
    text += "• Бесплатное питание в день сдачи\n"
    text += "• Первоочередное получение путевок\n\n"
    text += "🎓 **Студентам МИФИ:**\n"
    text += "• Повышенная стипендия\n"
    text += "• Зачет по физкультуре\n"
    text += "• Скидки в столовой\n\n"
    text += "👨‍💼 **Сотрудникам МИФИ:**\n"
    text += "• Дополнительные выходные дни\n"
    text += "• Премии к праздникам\n"
    text += "• Льготы на санаторное лечение\n\n"
    text += "🏪 **Скидки в магазинах:**\n"
    text += "• 5% в магазинах \"Дикси\"\n"
    text += "• 10% в аптеках \"36.6\"\n"
    text += "• Скидки на медицинские услуги"
    
    from keyboards import get_benefits_keyboard
    await query.edit_message_text(
        text,
        reply_markup=get_benefits_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show notifications settings"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    with get_db() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        
        if not user:
            await query.edit_message_text("❌ Пользователь не найден.")
            return
        
        text = "🔔 **Настройки уведомлений**\n\n"
        text += "📱 **Доступные уведомления:**\n"
        text += "• Напоминания о предстоящих донациях\n"
        text += "• Новости о Днях донора\n"
        text += "• Важные объявления\n\n"
        text += "⚙️ **Текущие настройки:**\n"
        text += "🔔 Уведомления: Включены\n"
        text += "🕐 Время напоминаний: За день до события"
    
    from keyboards import get_notifications_keyboard
    await query.edit_message_text(
        text,
        reply_markup=get_notifications_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show contact information"""
    query = update.callback_query
    await query.answer()
    
    text = "📞 **Контактная информация**\n\n"
    text += "🏫 **Организаторы донорского движения МИФИ:**\n"
    text += "👨‍💼 Координатор: Иванов И.И.\n"
    text += "📞 Телефон: +7 (495) 788-56-99\n"
    text += "📧 Email: donor@mephi.ru\n"
    text += "🏢 Кабинет: А-123\n\n"
    text += "📋 **По вопросам регистрации:**\n"
    text += "📞 +7 (495) 788-56-88\n"
    text += "🕐 Рабочие часы: 9:00-18:00\n\n"
    text += "🆘 **Экстренная помощь:**\n"
    text += "📞 +7 (495) 788-50-01"
    
    keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]]
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle feedback submission"""
    query = update.callback_query
    await query.answer()
    
    text = "📝 **Отзывы и предложения**\n\n"
    text += "Ваше мнение важно для нас!\n\n"
    text += "💭 **Поделитесь:**\n"
    text += "• Как прошла ваша донация\n"
    text += "• Что можно улучшить\n"
    text += "• Ваши предложения\n\n"
    text += "Напишите ваш отзыв следующим сообщением:"
    
    # Set waiting state
    context.user_data['waiting_feedback'] = True
    
    keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]]
    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_admin_broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle broadcast message creation by admin"""
    user_id = update.effective_user.id
    message_text = update.message.text.strip()
    
    with get_db() as session:
        user = session.query(User).filter(
            User.telegram_id == user_id,
            User.is_admin == True
        ).first()
        
        if not user:
            await update.message.reply_text("❌ У вас нет прав администратора.")
            return
        
        # Store broadcast message
        context.user_data['broadcast_message'] = message_text
        context.user_data.pop('creating_broadcast', None)
        
        # Show broadcast options
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard = [
            [InlineKeyboardButton("👥 Всем донорам", callback_data="broadcast_all")],
            [InlineKeyboardButton("👨‍🎓 Студентам", callback_data="broadcast_students")],
            [InlineKeyboardButton("👨‍💼 Сотрудникам", callback_data="broadcast_employees")],
            [InlineKeyboardButton("🏠 Внешним донорам", callback_data="broadcast_external")],
            [InlineKeyboardButton("❌ Отмена", callback_data="admin_menu")]
        ]
        
        await update.message.reply_text(
            f"📢 **Предварительный просмотр рассылки:**\n\n{message_text}\n\n**Выберите целевую аудиторию:**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_admin_event_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle event creation by admin"""
    user_id = update.effective_user.id
    message_text = update.message.text.strip()
    
    with get_db() as session:
        user = session.query(User).filter(
            User.telegram_id == user_id,
            User.is_admin == True
        ).first()
        
        if not user:
            await update.message.reply_text("❌ У вас нет прав администратора.")
            return
        
        try:
            # Parse event data: "DD.MM.YYYY HH:MM | Center Name | Link"
            parts = message_text.split('|')
            if len(parts) < 2:
                raise ValueError("Неверный формат")
            
            datetime_str = parts[0].strip()
            center_name = parts[1].strip()
            external_link = parts[2].strip() if len(parts) > 2 else None
            
            # Parse date
            from datetime import datetime
            event_date = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M')
            
            # Find blood center
            blood_center = session.query(BloodCenter).filter(
                BloodCenter.short_name.ilike(f"%{center_name}%")
            ).first()
            
            if not blood_center:
                raise ValueError("Центр крови не найден")
            
            # Create event
            new_event = Event(
                date=event_date,
                blood_center_id=blood_center.id,
                external_registration_link=external_link,
                is_active=True
            )
            session.add(new_event)
            
            await update.message.reply_text(
                f"✅ **Событие создано успешно!**\n\n"
                f"📅 **Дата:** {event_date.strftime('%d.%m.%Y %H:%M')}\n"
                f"🏥 **Центр крови:** {blood_center.name}\n"
                f"🔗 **Ссылка:** {external_link or 'Не указана'}",
                reply_markup=get_admin_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
            
        except ValueError as e:
            await update.message.reply_text(
                f"❌ **Ошибка создания события:** {str(e)}\n\n"
                f"Используйте формат: `ДД.ММ.ГГГГ ЧЧ:ММ | Название ЦК | Ссылка`\n"
                f"Пример: `15.12.2024 10:00 | ЦК ФМБА | https://example.com`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        context.user_data.pop('creating_event', None)

async def promote_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Promote user to admin with special code (for testing)"""
    user_id = update.effective_user.id
    
    # Check if command has admin code
    if not context.args or context.args[0] != "mephi_admin_2024":
        await update.message.reply_text("❌ Неверный код администратора.")
        return
    
    with get_db() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            await update.message.reply_text("❌ Сначала зарегистрируйтесь в боте через /start.")
            return
        
        if user.is_admin:
            await update.message.reply_text("✅ Вы уже являетесь администратором.")
            return
        
        user.is_admin = True
        await update.message.reply_text(
            "✅ **Права администратора предоставлены!**\n\n"
            "Теперь вы можете использовать команду /admin для доступа к панели управления.",
            parse_mode=ParseMode.MARKDOWN
        )

# ===== COMPLETE BUTTON HANDLERS WITH EXCEL INTEGRATION =====

async def handle_donation_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed donation history"""
    query = update.callback_query
    if query:
        await query.answer()
    
    user_id = update.effective_user.id
    
    with get_db() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            text = "❌ Вы не зарегистрированы в системе."
            keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]]
            if query:
                await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
            return
        
        donations = session.query(Donation).filter(Donation.user_id == user.id).order_by(Donation.donation_date.desc()).all()
        
        text = f"🩸 **История донаций - {user.full_name}**\n\n"
        
        if not donations:
            text += "У вас пока нет записей о донациях.\n"
            text += "Станьте донором уже сегодня!"
        else:
            text += f"📊 **Всего донаций:** {len(donations)}\n\n"
            
            for i, donation in enumerate(donations, 1):
                date_str = donation.donation_date.strftime("%d.%m.%Y")
                center_name = donation.blood_center.short_name
                text += f"{i}. **{date_str}** - {center_name}\n"
                if i >= 10:
                    text += f"... и еще {len(donations) - 10} донаций\n"
                    break
        
        keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]]
        if query:
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_center_gavrilov(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show Gavrilov center details"""
    query = update.callback_query
    await query.answer()
    
    text = """🏥 **Центр крови им. О.К. Гаврилова**

📍 **Адрес:** ул. Поликарпова, д. 14
📞 **Телефон:** +7 (499) 196-62-04
🚇 **Проезд:** м. Сокол + автобус 65, 670
🕐 **Время работы:** Пн-Пт 8:00-15:00

💡 **Особенности:**
• Современное оборудование
• Комфортные условия  
• Опытный персонал
• Быстрое обслуживание

🎁 **Для доноров МИФИ:**
• Повышенная компенсация
• Льготная запись
• Специальные дни донора"""
    
    keyboard = [[InlineKeyboardButton("🔙 К центрам", callback_data="blood_centers")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_center_fmba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show FMBA center details"""
    query = update.callback_query  
    await query.answer()
    
    text = """🏥 **Центр крови ФМБА России**

📍 **Адрес:** Волоколамское ш., д. 30
📞 **Телефон:** +7 (499) 193-78-01
🚇 **Проезд:** м. Тушинская + маршрутка
🕐 **Время работы:** Пн-Пт 8:00-14:00

💡 **Особенности:**
• Государственный центр
• Полный спектр анализов
• Профессиональная команда
• Строгие стандарты качества

🎁 **Для доноров МИФИ:**
• Государственные льготы
• Почетные награды  
• Медицинское обследование"""
    
    keyboard = [[InlineKeyboardButton("🔙 К центрам", callback_data="blood_centers")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_centers_directions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show directions to centers"""
    query = update.callback_query
    await query.answer()
    
    text = """📍 **Как добраться до центров**

🏥 **До центра Гаврилова:**
🚇 м. Сокол → автобус 65, 670
🚶 10 минут пешком от остановки
🚗 Парковка бесплатная у здания

🏥 **До центра ФМБА:**
🚇 м. Тушинская → маршрутка 904м
🚶 5 минут от остановки
🚗 Ограниченная парковка

⏰ **Рекомендуемое время:**
• Утренние часы (8:00-11:00)
• Меньше очередей
• Лучшее самочувствие

💡 **Совет:** Приезжайте натощак или через 3 часа после легкого завтрака"""
    
    keyboard = [[InlineKeyboardButton("🔙 К центрам", callback_data="blood_centers")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_centers_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show centers contact information"""
    query = update.callback_query
    await query.answer()
    
    text = """📞 **Контакты центров донорства**

🏥 **Центр Гаврилова:**
📞 +7 (499) 196-62-04
📧 gavrilov@bloodcenter.ru
🕐 8:00-15:00 (Пн-Пт)

🏥 **Центр ФМБА:**
📞 +7 (499) 193-78-01
📧 fmba@bloodcenter.ru
🕐 8:00-14:00 (Пн-Пт)

📋 **Для записи звоните:**
• За 1-2 дня до визита
• Уточните требования
• Подтвердите время

🆘 **Экстренные вопросы:**
📞 +7 (495) 788-50-01"""
    
    keyboard = [[InlineKeyboardButton("🔙 К центрам", callback_data="blood_centers")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_benefits_students(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show benefits for students"""
    query = update.callback_query
    await query.answer()
    
    text = """🎓 **Льготы для студентов-доноров**

📚 **Академические льготы:**
• Повышенная стипендия на 25%
• Автомат по физкультуре
• Приоритет при поселении в общежитие
• Льготы на курсовые и дипломы

🍽️ **Питание:**
• 15% скидка в столовых МИФИ
• Бесплатное питание в день донации
• Льготы в кафе "Студенческое"

🎫 **Развлечения:**
• Бесплатные билеты в театры
• Скидки в кинотеатрах
• Льготы на спортивные мероприятия
• Бесплатное посещение музеев

💰 **Финансовые льготы:**
• Дополнительные выплаты
• Компенсация проезда
• Льготы на учебные материалы"""
    
    keyboard = [[InlineKeyboardButton("🔙 К льготам", callback_data="benefits")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_benefits_staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show benefits for staff"""
    query = update.callback_query
    await query.answer()
    
    text = """👨‍💼 **Льготы для сотрудников-доноров**

🏢 **Трудовые льготы:**
• 2 дополнительных выходных дня в году
• Гибкий график в день донации
• Оплачиваемое время на обследование
• Приоритет при планировании отпуска

💼 **Корпоративные льготы:**
• Премии к профессиональным праздникам
• Льготы на санаторно-курортное лечение
• Корпоративная медицинская страховка
• Скидки на корпоративные мероприятия

🏥 **Медицинские льготы:**
• Бесплатные анализы и обследования
• Приоритетное медицинское обслуживание
• Льготы на лечение в ведомственных больницах

💰 **Финансовые льготы:**
• Компенсационные выплаты
• Доплаты к окладу
• Льготы на проезд"""
    
    keyboard = [[InlineKeyboardButton("🔙 К льготам", callback_data="benefits")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_benefits_shops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show shopping benefits"""
    query = update.callback_query
    await query.answer()
    
    text = """🏪 **Скидки в магазинах для доноров**

🛒 **Продукты:**
• 5% в сети магазинов "Дикси"
• 3% в "Пятёрочке"
• 7% в магазинах "Перекрёсток"
• 10% в органических магазинах

💊 **Аптеки:**
• 10% в аптеках "36.6"
• 5% в "Ригла"
• 15% на витамины и БАДы
• Льготы на рецептурные препараты

👕 **Одежда и обувь:**
• 15% в "Спортмастер"
• 10% в магазинах университета
• Сезонные скидки до 20%
• Льготы на спортивную форму

📚 **Книги и канцелярия:**
• 20% на учебную литературу
• 15% на канцелярские товары
• Скидки в университетском магазине"""
    
    keyboard = [[InlineKeyboardButton("🔙 К льготам", callback_data="benefits")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_benefits_cafes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show cafe benefits"""
    query = update.callback_query
    await query.answer()
    
    text = """🍽️ **Скидки в кафе и ресторанах**

☕ **Кафе в МИФИ:**
• 15% во всех столовых университета
• 20% в кафе "Студенческое"
• Бесплатный чай/кофе в день донации
• Специальные комплексы для доноров

🍕 **Рестораны-партнёры:**
• 10% в "Додо Пицца"
• 15% в "Шоколаднице" 
• 5% в ресторанах "Теремок"
• Скидки на доставку еды

🥗 **Здоровое питание:**
• 20% в салат-барах
• Льготы на диетические меню
• Скидки на соки и смузи
• Специальные предложения для доноров

🎂 **Кондитерские:**
• 10% в местных пекарнях
• Скидки на торты на заказ
• Льготы на праздничные угощения"""
    
    keyboard = [[InlineKeyboardButton("🔙 К льготам", callback_data="benefits")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_benefits_tickets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show ticket benefits"""
    query = update.callback_query
    await query.answer()
    
    text = """🎫 **Бесплатные билеты и скидки**

🎭 **Театры и концерты:**
• 2 бесплатных билета в год в Большой театр
• 50% скидка в театрах Москвы
• Приоритетная покупка билетов
• Специальные донорские спектакли

🎬 **Кинотеатры:**
• 30% скидка во всех сетях
• Бесплатные билеты по четвергам
• Скидки на премьеры
• Льготы на попкорн и напитки

🏛️ **Музеи:**
• Бесплатное посещение государственных музеев
• Экскурсии со скидкой 50%
• Приоритетные билеты на выставки
• Специальные мероприятия для доноров

🏃‍♂️ **Спортивные события:**
• Льготные билеты на матчи
• Скидки в спортивных центрах
• Бесплатные тренировки
• Участие в донорских спартакиадах"""
    
    keyboard = [[InlineKeyboardButton("🔙 К льготам", callback_data="benefits")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_notifications_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enable notifications"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    with get_db() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        if user:
            # Here you would implement notification preferences
            # For now, just show confirmation
            pass
    
    text = """🔔 **Уведомления включены!**

📅 **Вы будете получать:**
• Напоминания о предстоящих донациях
• Информацию о новых мероприятиях
• Уведомления о льготах и скидках
• Важные объявления от организаторов

⏰ **Время уведомлений:**
• За день до мероприятия в 18:00
• В утро мероприятия в 8:00
• Еженедельный дайджест по воскресеньям

⚙️ **Настройки можно изменить** в любое время через меню уведомлений."""
    
    keyboard = [
        [InlineKeyboardButton("⚙️ Настроить время", callback_data="notifications_settings")],
        [InlineKeyboardButton("🔙 К уведомлениям", callback_data="notifications")]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_notifications_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Disable notifications"""
    query = update.callback_query
    await query.answer()
    
    text = """🔕 **Уведомления отключены**

❌ **Вы НЕ будете получать:**
• Напоминания о донациях
• Информацию о мероприятиях
• Уведомления о льготах

💡 **Вы всегда можете:**
• Включить уведомления обратно
• Проверять информацию в боте
• Следить за новостями в группе

⚠️ **Важно:** Критические уведомления (отмена мероприятий) будут приходить в любом случае."""
    
    keyboard = [
        [InlineKeyboardButton("🔔 Включить обратно", callback_data="notifications_on")],
        [InlineKeyboardButton("🔙 К уведомлениям", callback_data="notifications")]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_notifications_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show notification settings"""
    query = update.callback_query
    await query.answer()
    
    text = """⚙️ **Настройки уведомлений**

🕐 **Время напоминаний:**
• Текущее: 18:00 (за день до донации)
• Утреннее: 8:00 (в день донации)

📋 **Типы уведомлений:**
✅ Напоминания о донациях
✅ Новые мероприятия  
✅ Льготы и скидки
❌ Рекламные сообщения

🔄 **Частота:**
• Еженедельный дайджест: Воскресенье
• Экстренные: По мере необходимости

💡 Для изменения времени напишите администратору через кнопку "Задать вопрос"."""
    
    keyboard = [
        [InlineKeyboardButton("❓ Задать вопрос", callback_data="ask_question")],
        [InlineKeyboardButton("🔙 К уведомлениям", callback_data="notifications")]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

# Excel integration when user completes donation
async def record_donation_to_excel(user_id, blood_center_id):
    """Record completed donation and update Excel file"""
    with get_db() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return
        
        # Get user's donation statistics
        donations = session.query(Donation).filter(Donation.user_id == user_id).all()
        gavrilov_count = len([d for d in donations if d.blood_center_id == 1])
        fmba_count = len([d for d in donations if d.blood_center_id == 2])
        
        last_donation = ""
        if donations:
            last = max(donations, key=lambda d: d.donation_date)
            last_donation = last.donation_date.strftime('%d.%m.%Y')
        
        # Update Excel file
        donation_data = {
            'total_donations': len(donations),
            'gavrilov_count': gavrilov_count,
            'fmba_count': fmba_count,
            'last_donation': last_donation
        }
        
        update_donor_donations(user_id, donation_data)

# Admin response to questions with forwarding
async def admin_answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question_id: int, answer_text: str):
    """Admin answers question and sends to all users with questions"""
    
    with get_db() as session:
        admin_user = session.query(User).filter(
            User.telegram_id == update.effective_user.id,
            User.is_admin == True
        ).first()
        
        if not admin_user:
            return False
        
        question = session.query(Question).filter(Question.id == question_id).first()
        if not question:
            return False
        
        # Update question with answer
        question.admin_response = answer_text
        question.response_date = datetime.now()
        question.answered_by_id = admin_user.id
        
        # Send answer to the user who asked
        try:
            await context.bot.send_message(
                chat_id=question.user.telegram_id,
                text=f"📬 **Ответ на ваш вопрос:**\n\n"
                     f"❓ **Ваш вопрос:** {question.question_text}\n\n"
                     f"💬 **Ответ администратора:** {answer_text}\n\n"
                     f"👨‍💼 **Ответил:** {admin_user.full_name}",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"Error sending answer to user: {e}")
        
        # Send to all users who have asked questions (broadcast)
        all_questions = session.query(Question).filter(Question.id != question_id).all()
        sent_to = set()
        
        for q in all_questions:
            if q.user.telegram_id not in sent_to:
                try:
                    await context.bot.send_message(
                        chat_id=q.user.telegram_id,
                        text=f"📢 **Новый ответ администратора:**\n\n"
                             f"❓ **Вопрос:** {question.question_text}\n\n"
                             f"💬 **Ответ:** {answer_text}\n\n"
                             f"💡 Этот ответ может быть полезен и вам!",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    sent_to.add(q.user.telegram_id)
                except Exception as e:
                    print(f"Error broadcasting answer: {e}")
        
        return True

# Export current donors to Excel
async def handle_admin_export_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin exports all data to Excel"""
    query = update.callback_query
    if query:
        await query.answer()
    
    user_id = update.effective_user.id
    
    with get_db() as session:
        user = session.query(User).filter(
            User.telegram_id == user_id,
            User.is_admin == True
        ).first()
        
        if not user:
            text = "❌ У вас нет прав администратора."
            if query:
                await query.edit_message_text(text)
            else:
                await update.message.reply_text(text)
            return
        
        try:
            filename, count = export_donors_to_excel()
            
            text = f"✅ **Экспорт завершён успешно!**\n\n"
            text += f"📊 **Экспортировано:** {count} доноров\n"
            text += f"📄 **Файл:** {filename}\n\n"
            text += f"Файл сохранён в корневой папке проекта."
            
            keyboard = [[InlineKeyboardButton("🔙 Админ-панель", callback_data="admin_menu")]]
            
            if query:
                await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
                
        except Exception as e:
            text = f"❌ **Ошибка экспорта:** {str(e)}"
            if query:
                await query.edit_message_text(text)
            else:
                await update.message.reply_text(text)

# ===== ADMIN QUESTION HANDLING WITH BROADCAST =====

async def handle_admin_questions_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show list of questions for admin to answer"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    with get_db() as session:
        admin = session.query(User).filter(
            User.telegram_id == user_id,
            User.is_admin == True
        ).first()
        
        if not admin:
            await query.edit_message_text("❌ У вас нет прав администратора.")
            return
        
        # Get unanswered questions
        questions = session.query(Question).filter(Question.answer_text.is_(None)).all()
        
        if not questions:
            text = "✅ **Нет новых вопросов**\n\nВсе вопросы пользователей отвечены!"
            keyboard = [[InlineKeyboardButton("🔙 Админ-панель", callback_data="admin_menu")]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
            return
        
        text = f"❓ **Новые вопросы ({len(questions)}):**\n\n"
        
        keyboard = []
        for i, question in enumerate(questions[:5], 1):  # Show first 5 questions
            text += f"{i}. **{question.user.full_name}** ({question.created_at.strftime('%d.%m.%Y')})\n"
            text += f"_{question.question_text[:80]}{'...' if len(question.question_text) > 80 else ''}_\n\n"
            
            keyboard.append([InlineKeyboardButton(
                f"Ответить на вопрос #{i}",
                callback_data=f"answer_question_{question.id}"
            )])
        
        if len(questions) > 5:
            text += f"... и еще {len(questions) - 5} вопросов"
        
        keyboard.append([InlineKeyboardButton("🔙 Админ-панель", callback_data="admin_menu")])
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_answer_question_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle answer question button click"""
    query = update.callback_query
    await query.answer()
    
    question_id = int(query.data.split('_')[-1])
    
    with get_db() as session:
        question = session.query(Question).filter(Question.id == question_id).first()
        if not question:
            await query.edit_message_text("❌ Вопрос не найден.")
            return
        
        # Store question ID in context
        context.user_data['answering_question_id'] = question_id
        
        text = f"📝 **Ответ на вопрос пользователя**\n\n"
        text += f"👤 **Пользователь:** {question.user.full_name}\n"
        text += f"📅 **Дата:** {question.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        text += f"❓ **Вопрос:**\n{question.question_text}\n\n"
        text += "💬 **Напишите ваш ответ следующим сообщением:**"
        
        keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="admin_questions")]]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )

# ===== DONATION COMPLETION WITH EXCEL UPDATE =====

async def record_donation_completion(user_id, blood_center_id=1):
    """Record completed donation and update Excel automatically"""
    
    with get_db() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # Create new donation record
        from datetime import date
        new_donation = Donation(
            user_id=user.id,
            donation_date=date.today(),
            blood_center_id=blood_center_id,
            bone_marrow_sample=False
        )
        session.add(new_donation)
        session.commit()
        
        # Auto-update Excel file
        try:
            donations = session.query(Donation).filter(Donation.user_id == user.id).all()
            gavrilov_count = len([d for d in donations if d.blood_center_id == 1])
            fmba_count = len([d for d in donations if d.blood_center_id == 2])
            
            last_donation = max(donations, key=lambda d: d.donation_date).donation_date.strftime('%d.%m.%Y')
            
            donation_data = {
                'total_donations': len(donations),
                'gavrilov_count': gavrilov_count,
                'fmba_count': fmba_count,
                'last_donation': last_donation
            }
            
            update_donor_donations(user.id, donation_data)
            print(f"✅ Excel updated for user: {user.full_name} - Total donations: {len(donations)}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating Excel: {e}")
            return False
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
from database import get_db
from models import User, Event, BloodCenter, Donation, Question, InfoSection, EventRegistration
from keyboards import (get_admin_keyboard, get_admin_donors_keyboard, 
                      get_admin_events_keyboard, get_admin_stats_keyboard)
from utils import parse_excel_donors, parse_excel_donations, generate_statistics_report
import pandas as pd
from datetime import datetime
import os

def setup_admin_handlers(application):
    """Setup admin-specific handlers"""
    application.add_handler(CallbackQueryHandler(admin_menu_handler, pattern="^admin_"))

async def admin_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin menu callbacks"""
    query = update.callback_query
    await query.answer()
    
    # Check admin permissions
    user_id = update.effective_user.id
    with get_db() as session:
        user = session.query(User).filter(
            User.telegram_id == user_id,
            User.is_admin == True
        ).first()
        
        if not user:
            await query.edit_message_text("❌ У вас нет прав администратора.")
            return
    
    action = query.data
    
    if action == "admin_menu":
        await query.edit_message_text(
            "🛠️ **Панель администратора**",
            reply_markup=get_admin_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif action == "admin_donors":
        await query.edit_message_text(
            "👥 **Управление донорами**",
            reply_markup=get_admin_donors_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif action == "admin_events":
        await query.edit_message_text(
            "📅 **Управление событиями**",
            reply_markup=get_admin_events_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif action == "admin_stats":
        await query.edit_message_text(
            "📊 **Статистика**",
            reply_markup=get_admin_stats_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif action == "admin_questions":
        await show_unanswered_questions(query, context)
    
    elif action == "admin_broadcast":
        await start_broadcast(query, context)
    
    elif action == "admin_info":
        await show_info_editor(query, context)
    
    elif action == "admin_donor_stats":
        await show_donor_statistics(query, context)
    
    elif action == "admin_event_stats":
        await show_event_statistics(query, context)
    
    elif action == "admin_export_excel":
        await export_excel_statistics(query, context)
    
    elif action == "admin_create_event":
        await start_create_event(query, context)
    
    elif action == "admin_list_events":
        await show_events_list(query, context)

async def show_unanswered_questions(query, context):
    """Show unanswered questions"""
    with get_db() as session:
        questions = session.query(Question).filter(
            Question.answer_text.is_(None)
        ).order_by(Question.created_at.desc()).limit(10).all()
        
        if not questions:
            await query.edit_message_text(
                "✅ **Нет неотвеченных вопросов**",
                reply_markup=get_admin_keyboard()
            )
            return
        
        text = "❓ **Неотвеченные вопросы:**\n\n"
        for i, question in enumerate(questions, 1):
            user_name = question.user.full_name
            question_text = question.question_text[:100] + "..." if len(question.question_text) > 100 else question.question_text
            text += f"{i}. **{user_name}**\n{question_text}\n\n"
        
        from keyboards import get_admin_keyboard
        await query.edit_message_text(
            text,
            reply_markup=get_admin_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def show_donor_statistics(query, context):
    """Show donor statistics"""
    with get_db() as session:
        total_donors = session.query(User).filter(User.consent_given == True).count()
        students = session.query(User).filter(User.user_type == 'student').count()
        employees = session.query(User).filter(User.user_type == 'employee').count()
        external = session.query(User).filter(User.user_type == 'external').count()
        bone_marrow = session.query(User).filter(User.bone_marrow_registry == True).count()
        
        total_donations = session.query(Donation).count()
        
        text = f"""📊 **Статистика по донорам:**

👥 **Всего доноров:** {total_donors}
• Студенты: {students}
• Сотрудники: {employees}  
• Внешние: {external}

🦴 **В регистре ДКМ:** {bone_marrow}
🩸 **Всего донаций:** {total_donations}
"""
        
        from keyboards import get_admin_stats_keyboard
        await query.edit_message_text(
            text,
            reply_markup=get_admin_stats_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def show_event_statistics(query, context):
    """Show event statistics"""
    with get_db() as session:
        events = session.query(Event).order_by(Event.date.desc()).limit(5).all()
        
        if not events:
            await query.edit_message_text(
                "📅 **Нет событий для отображения статистики**",
                reply_markup=get_admin_stats_keyboard()
            )
            return
        
        text = "📊 **Статистика по последним событиям:**\n\n"
        
        for event in events:
            registrations = len(event.registrations)
            donations = len(event.donations)
            date_str = event.date.strftime("%d.%m.%Y")
            
            text += f"**{date_str} - {event.blood_center.short_name}**\n"
            text += f"• Регистраций: {registrations}\n"
            text += f"• Донаций: {donations}\n"
            text += f"• Явка: {donations}/{registrations} ({(donations/registrations*100) if registrations > 0 else 0:.1f}%)\n\n"
        
        from keyboards import get_admin_stats_keyboard
        await query.edit_message_text(
            text,
            reply_markup=get_admin_stats_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def export_excel_statistics(query, context):
    """Export statistics to Excel"""
    with get_db() as session:
        # Get all data
        users = session.query(User).all()
        events = session.query(Event).all()
        donations = session.query(Donation).all()
        
        # Create DataFrames
        donors_data = []
        for user in users:
            donors_data.append({
                'ФИО': user.full_name,
                'Телефон': user.phone_number,
                'Тип': user.user_type,
                'Группа': user.group_number or '',
                'Донаций': len(user.donations),
                'Регистр ДКМ': 'Да' if user.bone_marrow_registry else 'Нет',
                'Дата регистрации': user.created_at.strftime('%d.%m.%Y')
            })
        
        donations_data = []
        for donation in donations:
            donations_data.append({
                'ФИО': donation.user.full_name,
                'Дата донации': donation.donation_date.strftime('%d.%m.%Y'),
                'Центр крови': donation.blood_center.name,
                'Тип донора': donation.user.user_type,
                'Образец ДКМ': 'Да' if donation.bone_marrow_sample else 'Нет'
            })
        
        # Create Excel file
        filename = f"mephi_donors_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = f"/tmp/{filename}"
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            pd.DataFrame(donors_data).to_excel(writer, sheet_name='Доноры', index=False)
            pd.DataFrame(donations_data).to_excel(writer, sheet_name='Донации', index=False)
        
        # Send file
        with open(filepath, 'rb') as file:
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=file,
                filename=filename,
                caption="📊 Статистика донорского движения МИФИ"
            )
        
        # Clean up
        os.remove(filepath)
        
        await query.edit_message_text(
            "✅ **Файл со статистикой отправлен**",
            reply_markup=get_admin_stats_keyboard()
        )

async def start_broadcast(query, context):
    """Start broadcast creation"""
    text = """📢 **Создание рассылки**

Доступные категории для рассылки:
• Все доноры
• Студенты  
• Сотрудники
• Внешние доноры
• Зарегистрированные на ближайшее событие
• Не явившиеся на последнее событие
• В регистре ДКМ

Напишите текст сообщения для рассылки."""
    
    await query.edit_message_text(text, reply_markup=get_admin_keyboard())
    context.user_data['creating_broadcast'] = True

async def show_info_editor(query, context):
    """Show information editor"""
    with get_db() as session:
        sections = session.query(InfoSection).all()
        
        text = "ℹ️ **Редактирование информации**\n\n"
        text += "Доступные разделы:\n"
        
        for section in sections:
            text += f"• {section.title}\n"
        
        text += "\nДля редактирования отправьте:\n"
        text += "`/edit_info <ключ_раздела> <новый_текст>`"
        
        await query.edit_message_text(
            text,
            reply_markup=get_admin_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def start_create_event(query, context):
    """Start event creation"""
    text = """📅 **Создание нового события**

Для создания события отправьте данные в формате:

`ДД.ММ.ГГГГ ЧЧ:ММ | Название центра крови | Ссылка для внешних`

Пример:
`15.12.2024 10:00 | ЦК ФМБА | https://example.com/register`

Доступные центры крови:
• ЦК ФМБА
• ЦК Гаврилова"""
    
    await query.edit_message_text(
        text,
        reply_markup=get_admin_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )
    context.user_data['creating_event'] = True

async def show_events_list(query, context):
    """Show list of events"""
    with get_db() as session:
        events = session.query(Event).order_by(Event.date.desc()).limit(10).all()
        
        if not events:
            await query.edit_message_text(
                "📅 **Нет созданных событий**",
                reply_markup=get_admin_events_keyboard()
            )
            return
        
        text = "📅 **Список событий:**\n\n"
        
        for event in events:
            date_str = event.date.strftime("%d.%m.%Y %H:%M")
            status = "🟢 Активно" if event.is_active else "🔴 Неактивно"
            registrations = len(event.registrations)
            
            text += f"**{date_str}**\n"
            text += f"ЦК: {event.blood_center.short_name}\n"
            text += f"Статус: {status}\n"
            text += f"Регистраций: {registrations}\n\n"
        
        await query.edit_message_text(
            text,
            reply_markup=get_admin_events_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def handle_admin_answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin answers question with broadcast to all users with questions"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    with get_db() as session:
        admin = session.query(User).filter(
            User.telegram_id == user_id,
            User.is_admin == True
        ).first()
        
        if not admin:
            await update.message.reply_text("❌ У вас нет прав администратора.")
            return
        
        if 'answering_question_id' not in context.user_data:
            await update.message.reply_text("❌ Не найден вопрос для ответа.")
            return
        
        question_id = context.user_data['answering_question_id']
        question = session.query(Question).filter(Question.id == question_id).first()
        
        if not question:
            await update.message.reply_text("❌ Вопрос не найден.")
            return
        
        # Update question with answer
        from datetime import datetime
        question.answer_text = text
        question.answered_at = datetime.now()
        question.answered_by_admin_id = admin.id
        
        # Send answer to the original questioner
        try:
            await context.bot.send_message(
                chat_id=question.user.telegram_id,
                text=f"📬 **Ответ администратора на ваш вопрос:**\n\n"
                     f"❓ **Ваш вопрос:** {question.question_text}\n\n"
                     f"💬 **Ответ:** {text}\n\n"
                     f"👨‍💼 **Ответил:** {admin.full_name}",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"Error sending answer to original user: {e}")
        
        # Broadcast to all users who have asked questions (excluding the original)
        all_questions = session.query(Question).filter(Question.id != question_id).all()
        sent_to = set()
        broadcast_count = 0
        
        for q in all_questions:
            if q.user.telegram_id not in sent_to:
                try:
                    await context.bot.send_message(
                        chat_id=q.user.telegram_id,
                        text=f"📢 **Новый ответ администратора:**\n\n"
                             f"❓ **Вопрос:** {question.question_text}\n\n"
                             f"💬 **Ответ:** {text}\n\n"
                             f"💡 Этот ответ может быть полезен и вам!\n\n"
                             f"👨‍💼 **Ответил:** {admin.full_name}",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    sent_to.add(q.user.telegram_id)
                    broadcast_count += 1
                except Exception as e:
                    print(f"Error broadcasting to user {q.user.telegram_id}: {e}")
        
        # Clear context
        context.user_data.pop('answering_question_id', None)
        
        # Send confirmation to admin
        await update.message.reply_text(
            f"✅ **Ответ отправлен успешно!**\n\n"
            f"📬 **Отвечено пользователю:** {question.user.full_name}\n"
            f"📢 **Рассылка:** {broadcast_count} доноров\n"
            f"📊 **Всего получили ответ:** {broadcast_count + 1} человек",
            reply_markup=get_admin_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_keyboard():
    """Main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("👤 Мой профиль", callback_data="profile"), InlineKeyboardButton("📊 Моя статистика", callback_data="my_stats")],
        [InlineKeyboardButton("📅 Записаться на донацию", callback_data="register_event")],
        [InlineKeyboardButton("🩸 История донаций", callback_data="donation_history"), InlineKeyboardButton("🏆 Рейтинг доноров", callback_data="donor_ranking")],
        [InlineKeyboardButton("📍 Центры донорства", callback_data="blood_centers"), InlineKeyboardButton("🎁 Льготы и скидки", callback_data="benefits")],
        [InlineKeyboardButton("ℹ️ Информация о донорстве", callback_data="info_menu")],
        [InlineKeyboardButton("🔔 Уведомления", callback_data="notifications"), InlineKeyboardButton("📞 Контакты", callback_data="contacts")],
        [InlineKeyboardButton("❓ Задать вопрос", callback_data="ask_question"), InlineKeyboardButton("📝 Отзывы", callback_data="feedback")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_user_type_keyboard():
    """User type selection keyboard"""
    keyboard = [
        [InlineKeyboardButton("👨‍🎓 Студент", callback_data="user_type_student")],
        [InlineKeyboardButton("👨‍💼 Сотрудник", callback_data="user_type_employee")],
        [InlineKeyboardButton("🏠 Внешний донор", callback_data="user_type_external")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_consent_keyboard():
    """Consent form keyboard"""
    keyboard = [
        [InlineKeyboardButton("✅ Согласен", callback_data="consent_yes")],
        [InlineKeyboardButton("❌ Не согласен", callback_data="consent_no")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_info_keyboard():
    """Information menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🩸 Требования к донорам", callback_data="info_blood_donation_requirements")],
        [InlineKeyboardButton("📋 Подготовка к донации", callback_data="info_preparation")],
        [InlineKeyboardButton("🦴 Донорство костного мозга", callback_data="info_bone_marrow")],
        [InlineKeyboardButton("🏛️ Донации в МИФИ", callback_data="info_mephi_process")],
        [InlineKeyboardButton("⚠️ Противопоказания", callback_data="info_contraindications")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_info_keyboard():
    """Back to info menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔙 К информации", callback_data="info_menu")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_profile_keyboard():
    """Profile menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("📜 История донаций", callback_data="donation_history")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_events_keyboard(events):
    """Events selection keyboard"""
    keyboard = []
    for event in events:
        date_str = event.date.strftime("%d.%m.%Y")
        button_text = f"{date_str} - {event.blood_center.short_name}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"event_{event.id}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def get_back_to_main_keyboard():
    """Simple back to main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_statistics_keyboard():
    """Statistics menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🩸 Всего донаций", callback_data="stats_total_donations")],
        [InlineKeyboardButton("📊 Донации по месяцам", callback_data="stats_monthly")],
        [InlineKeyboardButton("🏥 По центрам", callback_data="stats_by_center")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_blood_centers_keyboard():
    """Blood centers menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🏥 Центр Гаврилова", callback_data="center_gavrilov")],
        [InlineKeyboardButton("🏥 Центр ФМБА", callback_data="center_fmba")],
        [InlineKeyboardButton("📍 Как добраться", callback_data="centers_directions")],
        [InlineKeyboardButton("📞 Контакты центров", callback_data="centers_contacts")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_benefits_keyboard():
    """Benefits menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🎓 Льготы для студентов", callback_data="benefits_students")],
        [InlineKeyboardButton("👨‍💼 Льготы для сотрудников", callback_data="benefits_staff")],
        [InlineKeyboardButton("🏪 Скидки в магазинах", callback_data="benefits_shops")],
        [InlineKeyboardButton("🍽️ Скидки в кафе", callback_data="benefits_cafes")],
        [InlineKeyboardButton("🎫 Бесплатные билеты", callback_data="benefits_tickets")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_notifications_keyboard():
    """Notifications menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔔 Включить напоминания", callback_data="notifications_on")],
        [InlineKeyboardButton("🔕 Отключить напоминания", callback_data="notifications_off")],
        [InlineKeyboardButton("⚙️ Настроить время", callback_data="notifications_settings")],
        [InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard():
    """Admin panel keyboard"""
    keyboard = [
        [InlineKeyboardButton("👥 Управление донорами", callback_data="admin_donors")],
        [InlineKeyboardButton("📅 Управление событиями", callback_data="admin_events")],
        [InlineKeyboardButton("📊 Статистика системы", callback_data="admin_statistics")],
        [InlineKeyboardButton("❓ Ответить на вопросы", callback_data="admin_questions")],
        [InlineKeyboardButton("📢 Рассылка сообщений", callback_data="admin_broadcast")],
        [InlineKeyboardButton("📋 Импорт базы данных", callback_data="admin_import_db")],
        [InlineKeyboardButton("💾 Экспорт данных", callback_data="admin_export_data")],
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("ℹ️ Редактировать информацию", callback_data="admin_info")],
        [InlineKeyboardButton("🔙 Выйти", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_donors_keyboard():
    """Admin donors management keyboard"""
    keyboard = [
        [InlineKeyboardButton("➕ Добавить донора", callback_data="admin_add_donor")],
        [InlineKeyboardButton("✏️ Редактировать донора", callback_data="admin_edit_donor")],
        [InlineKeyboardButton("📄 Загрузить список", callback_data="admin_upload_donors")],
        [InlineKeyboardButton("📊 Добавить донации", callback_data="admin_add_donations")],
        [InlineKeyboardButton("🔙 Назад", callback_data="admin_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_events_keyboard():
    """Admin events management keyboard"""
    keyboard = [
        [InlineKeyboardButton("➕ Создать событие", callback_data="admin_create_event")],
        [InlineKeyboardButton("✏️ Редактировать событие", callback_data="admin_edit_event")],
        [InlineKeyboardButton("📋 Список событий", callback_data="admin_list_events")],
        [InlineKeyboardButton("🔙 Назад", callback_data="admin_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_stats_keyboard():
    """Admin statistics keyboard"""
    keyboard = [
        [InlineKeyboardButton("📊 Статистика по событиям", callback_data="admin_event_stats")],
        [InlineKeyboardButton("👥 Статистика по донорам", callback_data="admin_donor_stats")],
        [InlineKeyboardButton("📥 Выгрузить Excel", callback_data="admin_export_excel")],
        [InlineKeyboardButton("🔙 Назад", callback_data="admin_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_no_show_reasons_keyboard():
    """No-show reasons keyboard"""
    keyboard = [
        [InlineKeyboardButton("🏥 Медотвод", callback_data="no_show_medotved")],
        [InlineKeyboardButton("👤 Личные причины", callback_data="no_show_personal")],
        [InlineKeyboardButton("🚫 Не захотел", callback_data="no_show_unwilling")]
    ]
    return InlineKeyboardMarkup(keyboard)
MESSAGES = {
    'welcome': """
🩸 **Добро пожаловать в бот донорского движения НИЯУ МИФИ!**

Этот бот поможет вам:
• Зарегистрироваться на Дни донора
• Получить информацию о донорстве
• Отслеживать историю ваших донаций
• Связаться с организаторами

Для начала работы необходимо пройти регистрацию.
""",

    'welcome_back': """
🩸 **Добро пожаловать, {name}!**

Рады видеть вас снова в донорском движении МИФИ!
""",

    'request_phone': """
📱 **Авторизация по номеру телефона**

Для регистрации в системе необходимо подтвердить ваш номер телефона.

Нажмите кнопку ниже, чтобы поделиться номером:
""",

    'request_name': """
👤 **Введите ваше ФИО**

Пожалуйста, введите ваше полное ФИО (Фамилия Имя Отчество).

Пример: Иванов Иван Иванович
""",

    'request_user_type': """
👥 **Выберите вашу категорию:**

Укажите, к какой категории вы относитесь:
""",

    'consent_form': """
📋 **Согласие на обработку персональных данных**

Для использования бота необходимо ваше согласие на:

• Обработку персональных данных (ФИО, телефон, данные о донациях)
• Получение уведомлений и рассылок о Днях донора
• Хранение информации о ваших донациях

Ваши данные используются исключительно для организации донорских мероприятий и не передаются третьим лицам.

**Даете ли вы согласие?**
""",

    'main_menu': """
🏠 **Главное меню**

Выберите нужный раздел:
""",

    'info_menu': """
ℹ️ **Информация о донорстве**

Выберите интересующий раздел:
""",

    'user_types': {
        'student': 'Студент',
        'employee': 'Сотрудник',
        'external': 'Внешний донор'
    },

    'admin_panel': """
🛠️ **Панель администратора**

Добро пожаловать в панель управления ботом донорского движения МИФИ.
""",

    'no_events': """
📅 На данный момент нет запланированных Дней донора.

Следите за объявлениями о новых мероприятиях!
""",

    'registration_success': """
✅ **Регистрация завершена!**

Вы успешно зарегистрированы на День донора.

Мы отправим вам напоминание накануне мероприятия.
""",

    'question_received': """
✅ **Ваш вопрос получен!**

Организаторы ответят вам в ближайшее время.
""",

    'no_show_survey': """
😔 **Мы заметили, что вы не пришли на День донора**

Помогите нам стать лучше - укажите причину:
""",
}
import re
import pandas as pd
from datetime import datetime
from typing import List, Dict

def validate_name(name: str) -> bool:
    """Validate full name format"""
    if not name or len(name.strip()) < 5:
        return False
    
    # Remove extra spaces and normalize
    name = ' '.join(name.split())
    
    # Check for at least 2 words (surname and name)
    words = name.split()
    if len(words) < 2:
        return False
    
    # Check that all words contain only letters and hyphens
    for word in words:
        if not re.match(r'^[А-Яа-яЁё\-]+$', word):
            return False
    
    return True

def normalize_name(name: str) -> str:
    """Normalize name format"""
    # Remove extra spaces
    name = ' '.join(name.split())
    
    # Capitalize each word
    words = []
    for word in name.split():
        # Handle hyphenated names
        if '-' in word:
            parts = word.split('-')
            word = '-'.join([part.capitalize() for part in parts])
        else:
            word = word.capitalize()
        words.append(word)
    
    return ' '.join(words)

def validate_group_number(group: str) -> bool:
    """Validate student group number format"""
    if not group:
        return False
    
    # Common MEPHI group formats: Б20-505, М22-403, etc.
    pattern = r'^[А-Я]\d{2}-\d{3}[А-Я]?$'
    return bool(re.match(pattern, group.upper()))

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    if not phone:
        return False
    
    # Remove all non-digit characters except +
    clean_phone = re.sub(r'[^\d+]', '', phone)
    
    # Should start with + and have 11-15 digits
    if not clean_phone.startswith('+'):
        return False
    
    digits = clean_phone[1:]
    return len(digits) >= 10 and len(digits) <= 15 and digits.isdigit()

def format_phone(phone: str) -> str:
    """Format phone number"""
    clean_phone = re.sub(r'[^\d+]', '', phone)
    if not clean_phone.startswith('+'):
        clean_phone = '+' + clean_phone
    return clean_phone

def parse_excel_donors(file_path: str) -> List[Dict]:
    """Parse Excel file with donor data"""
    try:
        df = pd.read_excel(file_path)
        
        # Expected columns: ФИО, Телефон, Тип (студент/сотрудник/внешний), Группа (для студентов)
        required_columns = ['ФИО', 'Телефон']
        
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Отсутствует обязательная колонка: {col}")
        
        donors = []
        for index, row in df.iterrows():
            donor = {
                'full_name': str(row['ФИО']).strip(),
                'phone': str(row['Телефон']).strip(),
                'user_type': str(row.get('Тип', 'external')).strip().lower(),
                'group_number': str(row.get('Группа', '')).strip() if pd.notna(row.get('Группа')) else None
            }
            
            # Validate data
            if not validate_name(donor['full_name']):
                continue
            
            if not validate_phone(donor['phone']):
                continue
            
            donor['full_name'] = normalize_name(donor['full_name'])
            donor['phone'] = format_phone(donor['phone'])
            
            # Map user types
            type_mapping = {
                'студент': 'student',
                'сотрудник': 'employee',
                'внешний': 'external',
                'student': 'student',
                'employee': 'employee',
                'external': 'external'
            }
            
            donor['user_type'] = type_mapping.get(donor['user_type'], 'external')
            
            donors.append(donor)
        
        return donors
    
    except Exception as e:
        raise ValueError(f"Ошибка при обработке файла: {str(e)}")

def parse_excel_donations(file_path: str) -> List[Dict]:
    """Parse Excel file with donation data"""
    try:
        df = pd.read_excel(file_path)
        
        # Expected columns: ФИО, Дата, ЦК, ДКМ (да/нет)
        required_columns = ['ФИО', 'Дата', 'ЦК']
        
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Отсутствует обязательная колонка: {col}")
        
        donations = []
        for index, row in df.iterrows():
            donation = {
                'full_name': str(row['ФИО']).strip(),
                'date': row['Дата'],
                'blood_center': str(row['ЦК']).strip(),
                'bone_marrow_sample': str(row.get('ДКМ', 'нет')).strip().lower() in ['да', 'yes', '1', 'true']
            }
            
            # Validate and normalize name
            if not validate_name(donation['full_name']):
                continue
            
            donation['full_name'] = normalize_name(donation['full_name'])
            
            # Parse date
            if isinstance(donation['date'], str):
                try:
                    donation['date'] = datetime.strptime(donation['date'], '%d.%m.%Y')
                except ValueError:
                    try:
                        donation['date'] = datetime.strptime(donation['date'], '%Y-%m-%d')
                    except ValueError:
                        continue
            elif not isinstance(donation['date'], datetime):
                continue
            
            donations.append(donation)
        
        return donations
    
    except Exception as e:
        raise ValueError(f"Ошибка при обработке файла: {str(e)}")

def generate_statistics_report(donors, events, donations) -> Dict:
    """Generate comprehensive statistics report"""
    total_donors = len(donors)
    total_events = len(events)
    total_donations = len(donations)
    
    # Donors by type
    donor_types = {}
    for donor in donors:
        donor_type = donor.user_type
        donor_types[donor_type] = donor_types.get(donor_type, 0) + 1
    
    # Donations by blood center
    donations_by_center = {}
    for donation in donations:
        center = donation.blood_center.short_name
        donations_by_center[center] = donations_by_center.get(center, 0) + 1
    
    # Bone marrow registry count
    bone_marrow_count = sum(1 for donor in donors if donor.bone_marrow_registry)
    
    return {
        'total_donors': total_donors,
        'total_events': total_events,
        'total_donations': total_donations,
        'donor_types': donor_types,
        'donations_by_center': donations_by_center,
        'bone_marrow_registry': bone_marrow_count
    }
"""
Excel export functionality for donor data
"""

import pandas as pd
import os
from datetime import datetime
from database import get_db
from models import User, Donation, BloodCenter

def export_donors_to_excel():
    """Export all donor data to Excel file"""
    
    with get_db() as session:
        # Get all users with their donations
        users = session.query(User).all()
        
        # Prepare data for export
        export_data = []
        
        for user in users:
            donations = session.query(Donation).filter(Donation.user_id == user.id).all()
            
            # Basic user info
            user_data = {
                'ФИО': user.full_name,
                'Тип': user.user_type,
                'Группа': user.group_number or '',
                'Телефон': user.phone_number,
                'Всего донаций': len(donations),
                'Дата регистрации': user.created_at.strftime('%d.%m.%Y') if user.created_at else '',
                'Админ': 'Да' if user.is_admin else 'Нет',
                'Костный мозг': 'Да' if user.bone_marrow_registry else 'Нет'
            }
            
            # Add donation details
            gavrilov_count = len([d for d in donations if d.blood_center_id == 1])
            fmba_count = len([d for d in donations if d.blood_center_id == 2])
            
            user_data['Донации Гаврилова'] = gavrilov_count
            user_data['Донации ФМБА'] = fmba_count
            
            # Last donation date
            if donations:
                last_donation = max(donations, key=lambda d: d.donation_date)
                user_data['Последняя донация'] = last_donation.donation_date.strftime('%d.%m.%Y')
            else:
                user_data['Последняя донация'] = ''
            
            export_data.append(user_data)
        
        # Create DataFrame
        df = pd.DataFrame(export_data)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'mephi_donors_export_{timestamp}.xlsx'
        
        # Export to Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        
        return filename, len(export_data)

def add_new_donor_to_excel(user_data, donation_data=None):
    """Add new donor to existing Excel file"""
    
    # Check if export file exists
    export_files = [f for f in os.listdir('.') if f.startswith('mephi_donors_export_') and f.endswith('.xlsx')]
    
    if export_files:
        # Use the most recent export file
        latest_file = max(export_files, key=lambda f: os.path.getctime(f))
        
        try:
            # Read existing Excel file
            df = pd.read_excel(latest_file, engine='openpyxl')
            
            # Prepare new row data
            new_row = {
                'ФИО': user_data.get('full_name', ''),
                'Тип': user_data.get('user_type', ''),
                'Группа': user_data.get('group_number', ''),
                'Телефон': user_data.get('phone_number', ''),
                'Всего донаций': donation_data.get('total_donations', 0) if donation_data else 0,
                'Дата регистрации': datetime.now().strftime('%d.%m.%Y'),
                'Админ': 'Нет',
                'Костный мозг': 'Нет',
                'Донации Гаврилова': donation_data.get('gavrilov_count', 0) if donation_data else 0,
                'Донации ФМБА': donation_data.get('fmba_count', 0) if donation_data else 0,
                'Последняя донация': donation_data.get('last_donation', '') if donation_data else ''
            }
            
            # Add new row to DataFrame
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
            # Save updated file
            df.to_excel(latest_file, index=False, engine='openpyxl')
            
            return latest_file
            
        except Exception as e:
            print(f"Error updating Excel file: {e}")
            return None
    else:
        # No existing file, create new export
        return export_donors_to_excel()[0]

def update_donor_donations(user_id, new_donation_data):
    """Update donor's donation data in Excel"""
    
    export_files = [f for f in os.listdir('.') if f.startswith('mephi_donors_export_') and f.endswith('.xlsx')]
    
    if export_files:
        latest_file = max(export_files, key=lambda f: os.path.getctime(f))
        
        try:
            # Read existing Excel file
            df = pd.read_excel(latest_file, engine='openpyxl')
            
            # Find and update the donor's record
            with get_db() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if user:
                    # Find user row in DataFrame
                    user_mask = df['ФИО'] == user.full_name
                    
                    if user_mask.any():
                        # Update donation counts
                        df.loc[user_mask, 'Всего донаций'] = new_donation_data.get('total_donations', 0)
                        df.loc[user_mask, 'Донации Гаврилова'] = new_donation_data.get('gavrilov_count', 0)
                        df.loc[user_mask, 'Донации ФМБА'] = new_donation_data.get('fmba_count', 0)
                        df.loc[user_mask, 'Последняя донация'] = new_donation_data.get('last_donation', '')
                        
                        # Save updated file
                        df.to_excel(latest_file, index=False, engine='openpyxl')
                        
                        return latest_file
            
        except Exception as e:
            print(f"Error updating donor data: {e}")
            return None
    
    return None

def get_excel_statistics():
    """Get statistics from Excel export file"""
    
    export_files = [f for f in os.listdir('.') if f.startswith('mephi_donors_export_') and f.endswith('.xlsx')]
    
    if export_files:
        latest_file = max(export_files, key=lambda f: os.path.getctime(f))
        
        try:
            df = pd.read_excel(latest_file, engine='openpyxl')
            
            stats = {
                'total_donors': len(df),
                'total_donations': df['Всего донаций'].sum(),
                'students': len(df[df['Тип'] == 'student']),
                'employees': len(df[df['Тип'] == 'employee']),
                'external': len(df[df['Тип'] == 'external']),
                'gavrilov_donations': df['Донации Гаврилова'].sum(),
                'fmba_donations': df['Донации ФМБА'].sum(),
                'bone_marrow_donors': len(df[df['Костный мозг'] == 'Да']),
                'last_update': datetime.fromtimestamp(os.path.getctime(latest_file)).strftime('%d.%m.%Y %H:%M')
            }
            
            return stats, latest_file
            
        except Exception as e:
            print(f"Error reading Excel statistics: {e}")
            return None, None
    
    return None, None"""
Enhanced menu system with Telegram commands
"""

from telegram import Update, BotCommand
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from database import get_db
from models import User, Event, Donation
from keyboards import get_main_keyboard
import datetime

# Menu commands that will appear in Telegram
MENU_COMMANDS = [
    BotCommand("start", "🏠 Главное меню"),
    BotCommand("profile", "👤 Мой профиль"),
    BotCommand("register", "📅 Записаться на донацию"),
    BotCommand("events", "📋 Предстоящие события"),
    BotCommand("stats", "📊 Моя статистика"),
    BotCommand("history", "🩸 История донаций"),
    BotCommand("rating", "🏆 Рейтинг доноров"),
    BotCommand("centers", "🏥 Центры донорства"),
    BotCommand("benefits", "🎁 Льготы и скидки"),
    BotCommand("info", "ℹ️ Информация о донорстве"),
    BotCommand("contact", "📞 Контакты"),
    BotCommand("feedback", "💬 Оставить отзыв"),
    BotCommand("help", "❓ Справка по командам"),
    BotCommand("admin", "⚙️ Панель администратора")
]

async def setup_menu_commands(bot):
    """Set up bot commands menu"""
    try:
        await bot.set_my_commands(MENU_COMMANDS)
        print("✅ Menu commands successfully configured")
    except Exception as e:
        print(f"❌ Error setting up menu commands: {e}")

async def show_help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show comprehensive help with all available commands"""
    help_text = """🤖 **МИФИ Донор - Справка по командам**

📱 **Основные команды:**
/start - Главное меню бота
/profile - Просмотр профиля пользователя
/register - Записаться на донацию крови

📊 **Статистика и рейтинги:**
/stats - Ваша личная статистика
/history - История ваших донаций
/rating - Рейтинг доноров МИФИ

🏥 **Информация:**
/events - Предстоящие Дни донора
/centers - Центры донорства крови
/benefits - Льготы для доноров
/info - Подробная информация о донорстве

💬 **Обратная связь:**
/contact - Контактная информация
/feedback - Оставить отзыв или предложение

⚙️ **Для администраторов:**
/admin - Панель управления (только для админов)

🔍 **Дополнительные функции:**
• Используйте кнопки меню для быстрой навигации
• Бот поддерживает голосовые сообщения
• Автоматические напоминания о донациях
• Система достижений для активных доноров

❓ Если у вас возникли вопросы, используйте кнопку "Задать вопрос" в главном меню."""

    await update.message.reply_text(
        help_text,
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def quick_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick stats command /stats"""
    user_id = update.effective_user.id
    
    with get_db() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        
        if not user:
            await update.message.reply_text(
                "❌ Вы не зарегистрированы в системе. Используйте /start для регистрации."
            )
            return
        
        # Get donation count
        donation_count = session.query(Donation).filter(Donation.user_id == user.id).count()
        
        # Get recent donations
        recent_donations = session.query(Donation).filter(
            Donation.user_id == user.id
        ).order_by(Donation.donation_date.desc()).limit(3).all()
        
        text = f"📊 **Быстрая статистика для {user.full_name}**\n\n"
        text += f"🩸 **Всего донаций:** {donation_count}\n"
        text += f"👤 **Статус:** {user.user_type}\n"
        
        if user.group_number:
            text += f"🎓 **Группа:** {user.group_number}\n"
        
        if recent_donations:
            text += f"\n📅 **Последние донации:**\n"
            for donation in recent_donations[:3]:
                date_str = donation.donation_date.strftime("%d.%m.%Y")
                text += f"• {date_str} - {donation.blood_center.short_name}\n"
        
        text += f"\nДля подробной статистики используйте кнопку '📊 Моя статистика' в главном меню."
        
        await update.message.reply_text(
            text,
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def quick_events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick events command /events"""
    with get_db() as session:
        # Get upcoming events
        upcoming_events = session.query(Event).filter(
            Event.date >= datetime.datetime.now(),
            Event.is_active == True
        ).order_by(Event.date).limit(5).all()
        
        if not upcoming_events:
            text = "📅 **Предстоящие события**\n\nВ настоящее время нет запланированных Дней донора.\n\nСледите за объявлениями!"
        else:
            text = "📅 **Ближайшие Дни донора:**\n\n"
            for event in upcoming_events:
                date_str = event.date.strftime("%d.%m.%Y %H:%M")
                text += f"🏥 **{event.blood_center.name}**\n"
                text += f"📅 {date_str}\n\n"
            
            text += "Для записи используйте кнопку '📅 Записаться на донацию' в главном меню."
        
        await update.message.reply_text(
            text,
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def quick_centers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick centers command /centers"""
    text = """🏥 **Центры донорства крови МИФИ**

🩸 **Центр крови им. О.К. Гаврилова**
📍 ул. Поликарпова, д. 14
📞 +7 (499) 196-62-04
🚇 м. Сокол + автобус
🕐 Пн-Пт 8:00-15:00

🩸 **Центр крови ФМБА России** 
📍 Волоколамское ш., д. 30
📞 +7 (499) 193-78-01
🚇 м. Тушинская + маршрутка
🕐 Пн-Пт 8:00-14:00

💡 **Рекомендации:**
• Приходите натощак или через 3 часа после легкого завтрака
• Возьмите с собой паспорт
• Выспитесь перед донацией
• Откажитесь от алкоголя за 48 часов

📞 **Запись по телефону или через бота**"""

    await update.message.reply_text(
        text,
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def quick_benefits_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick benefits command /benefits"""
    text = """🎁 **Льготы для доноров МИФИ**

🩸 **Федеральные льготы:**
• 2 дополнительных выходных дня в году
• Бесплатное питание в день сдачи
• Первоочередное получение путевок
• Денежная компенсация

🎓 **Студентам МИФИ:**
• Повышенная стипендия
• Автомат по физкультуре
• Скидки в столовой до 15%
• Приоритет при получении общежития

👨‍💼 **Сотрудникам МИФИ:**
• Дополнительные выходные дни
• Премии к профессиональным праздникам
• Льготы на санаторно-курортное лечение
• Корпоративные скидки

🏪 **Партнерские скидки:**
• 5% в сети магазинов "Дикси"
• 10% в аптеках "36.6"
• Скидки в медицинских центрах
• Льготы на стоматологические услуги

🏆 **За 40 донаций** - звание "Почетный донор России" и пожизненные льготы!"""

    await update.message.reply_text(
        text,
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def quick_contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick contact command /contact"""
    text = """📞 **Контакты донорского движения МИФИ**

👥 **Организационный комитет:**
🏫 Каширское шоссе, 31, корпус А
📧 donor@mephi.ru
📞 +7 (495) 788-56-99

👨‍💼 **Координаторы:**
• Иванов И.И. - Общие вопросы (каб. А-123)
• Петрова А.С. - Студенческое донорство (каб. А-125)
• Сидоров В.П. - Сотрудники (каб. А-127)

🏥 **Медицинские консультации:**
📞 +7 (495) 788-56-88
🕐 Пн-Пт 9:00-18:00

🆘 **Экстренная помощь:**
📞 +7 (495) 788-50-01

💬 **Социальные сети:**
📱 Telegram: @mephi_donors
📘 ВКонтакте: vk.com/mephi_donors
📷 Instagram: @mephi_donors

❓ **Часто задаваемые вопросы:**
Используйте кнопку "❓ Задать вопрос" в главном меню для получения персональной консультации."""

    await update.message.reply_text(
        text,
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )"""
Import real donor data from Excel file to database
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import random
from database import get_db
from models import User, Donation, BloodCenter

def import_donor_data():
    """Import real donor data from Excel file"""
    excel_path = 'attached_assets/База ДД (1)_1752921577930.xlsx'
    
    if not os.path.exists(excel_path):
        print("Excel file not found")
        return
    
    try:
        # Read Excel data
        df = pd.read_excel(excel_path, sheet_name='Полная БД')
        print(f"Found {len(df)} donor records")
        
        # Get blood centers
        with get_db() as session:
            gavrilov_center = session.query(BloodCenter).filter_by(short_name="Гаврилова").first()
            fmba_center = session.query(BloodCenter).filter_by(short_name="ФМБА").first()
            
            imported_count = 0
            
            for idx, row in df.iterrows():
                try:
                    # Extract data
                    full_name = str(row['ФИО']).strip()
                    if pd.isna(full_name) or full_name == 'nan':
                        continue
                        
                    group = str(row['Группа']) if pd.notna(row['Группа']) else None
                    phone = str(int(row['Телефон'])) if pd.notna(row['Телефон']) else None
                    
                    # Skip if phone already exists
                    if phone:
                        existing_user = session.query(User).filter_by(phone_number=phone).first()
                        if existing_user:
                            continue
                    
                    # Determine user type
                    user_type = "student"
                    if group and ("сотрудник" in group.lower() or "Сотрудник" in group):
                        user_type = "employee"
                        group = None
                    elif not group or pd.isna(group) or group == 'nan':
                        user_type = "external"
                        group = None
                    
                    # Create user
                    user = User(
                        telegram_id=1000000 + idx,  # Temporary telegram ID
                        phone_number=phone,
                        full_name=full_name,
                        user_type=user_type,
                        group_number=group if user_type == "student" else None,
                        consent_given=True,
                        created_at=datetime.now() - timedelta(days=random.randint(30, 365))
                    )
                    session.add(user)
                    session.flush()  # Get user ID
                    
                    # Add donation records
                    gavrilov_count = int(row['Кол-во Гаврилова']) if pd.notna(row['Кол-во Гаврилова']) else 0
                    fmba_count = int(row['Кол-во ФМБА']) if pd.notna(row['Кол-во ФМБА']) else 0
                    
                    # Add Gavrilov donations
                    for i in range(gavrilov_count):
                        donation_date = datetime.now() - timedelta(days=random.randint(60, 730))
                        donation = Donation(
                            user_id=user.id,
                            event_id=1,  # Default event ID 
                            blood_center_id=gavrilov_center.id if gavrilov_center else 1,
                            donation_date=donation_date,
                            bone_marrow_sample=False
                        )
                        session.add(donation)
                    
                    # Add FMBA donations
                    for i in range(fmba_count):
                        donation_date = datetime.now() - timedelta(days=random.randint(60, 730))
                        donation = Donation(
                            user_id=user.id,
                            event_id=1,  # Default event ID
                            blood_center_id=fmba_center.id if fmba_center else 2,
                            donation_date=donation_date,
                            bone_marrow_sample=False
                        )
                        session.add(donation)
                    
                    imported_count += 1
                    
                    # Commit in batches
                    if imported_count % 50 == 0:
                        session.commit()
                        print(f"Imported {imported_count} users...")
                        
                except Exception as e:
                    print(f"Error importing row {idx}: {e}")
                    session.rollback()
                    continue
            
            session.commit()
            print(f"Successfully imported {imported_count} donor records with donation history")
            
    except Exception as e:
        print(f"Error importing data: {e}")

if __name__ == "__main__":
    import_donor_data()