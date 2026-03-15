from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.bot = Bot(token=self.token)

    async def send_message(self, chat_id: int, text: str, reply_markup=None):
        """Envia uma mensagem de texto simples ou com botões."""
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem para {chat_id}: {e}")
            raise e

    async def send_action_buttons(self, chat_id: int, text: str, buttons: list):
        """
        Envia botões inline para o usuário.
        buttons: lista de dicionários [{"text": "Nome", "callback_data": "data"}]
        """
        keyboard = [
            [InlineKeyboardButton(btn["text"], callback_data=btn["callback_data"])]
            for btn in buttons
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.send_message(chat_id, text, reply_markup=reply_markup)

    def get_main_menu_keyboard(self):
        """Retorna o teclado fixo (Menu) para a revendedora."""
        keyboard = [
            [KeyboardButton("📦 Meu Estoque"), KeyboardButton("📥 Entrada Estoque")],
            [KeyboardButton("💰 Registrar Venda"), KeyboardButton("📝 Pagamento Manual")],
            [KeyboardButton("📊 Relatório Hoje"), KeyboardButton("💳 Inadimplentes")],
            [KeyboardButton("👤 Perfil"), KeyboardButton("❓ Ajuda")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    async def send_main_menu(self, chat_id: int, welcome_text: str = "O que vamos fazer hoje? 🛡️✨"):
        """Envia o menu principal fixo para a usuária."""
        reply_markup = self.get_main_menu_keyboard()
        await self.send_message(chat_id, welcome_text, reply_markup=reply_markup)

    def create_wizard_markup(self, options: list):
        """Cria um teclado para fluxos de wizard."""
        # TODO: Implementar conforme necessidade do Agente
        pass
