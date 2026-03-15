import uuid
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.telegram import TelegramChatState
from typing import Optional

class TelegramChatStateService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_state(self, telegram_id: int) -> Optional[TelegramChatState]:
        stmt = select(TelegramChatState).where(TelegramChatState.telegram_id == telegram_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def set_state(self, telegram_id: int, state: str, context_data: dict = None):
        chat_state = await self.get_state(telegram_id)
        if not chat_state:
            chat_state = TelegramChatState(telegram_id=telegram_id)
            self.db.add(chat_state)
        
        chat_state.state = state
        if context_data is not None:
            chat_state.context_data = context_data
            
        await self.db.commit()
        return chat_state

    async def clear_state(self, telegram_id: int):
        await self.set_state(telegram_id, "IDLE", {})
