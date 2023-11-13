from dataclasses import dataclass

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.chat.models import Message
from src.db import async_session_maker, get_async_session

router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def send_personal_message(self, msg: str, ws: WebSocket):
        if ws in self.active_connections:
            await ws.send_text(msg)

    async def broadcast(self, msg: str, add_to_db: bool):
        if add_to_db:
            await self.add_messages_to_db(msg)

        for connection in self.active_connections:
            await connection.send_text(msg)

    @staticmethod
    async def add_messages_to_db(msg: str):
        async with async_session_maker() as session:
            stmt = insert(Message).values(
                message=msg
            )

            await session.execute(stmt)
            await session.commit()


manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages(session: AsyncSession = Depends(get_async_session)):
    query = select(Message).order_by(Message.id.desc()).limit(5)
    messages = await session.execute(query)

    return messages.scalars().all()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(ws: WebSocket, client_id: int):
    await manager.connect(ws)

    try:
        while True:
            data = await ws.receive_text()
            await manager.broadcast(f'Client #{client_id} says: {data}', add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(ws)
        await manager.broadcast(f'Client #{client_id} left the chat', add_to_db=False)
