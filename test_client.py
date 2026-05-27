# test_client.py
import asyncio
import websockets
import json
import sys

async def receiver(ws, player_name):
    """Фоновая задача: слушает сервер и выводит сообщения"""
    try:
        async for message in ws:
            data = json.loads(message)
            sender = data.get("sender_id")
            print(f"\n[{player_name}] 📥 От сервера: {data}")
            print(f"[{player_name}] 🎮 Твой ход > ", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        print(f"\n[{player_name}] 🔌 Соединение закрыто")

async def sender(ws, player_name):
    """Задача: читает ввод пользователя и отправляет на сервер"""
    loop = asyncio.get_event_loop()
    while True:
        # Читаем строку в неблокирующем стиле
        line = await loop.run_in_executor(None, sys.stdin.readline)
        msg = line.strip()
        if not msg:
            continue
        if msg.lower() in ("exit", "quit"):
            break
        try:
            # Пытаемся парсить как JSON, если не получается — оборачиваем
            data = json.loads(msg)
        except json.JSONDecodeError:
            data = {"type": "raw", "content": msg}
        await ws.send(json.dumps(data))
        print(f"[{player_name}] 📤 Отправлено: {data}")

async def main():
    uri = "ws://localhost:8765"
    player = input("Введите ваше имя/цвет: ").strip() or "Player"
    
    async with websockets.connect(uri) as ws:
        print(f"✅ Подключен как [{player}]")
        # Запускаем две задачи параллельно
        await asyncio.gather(
            receiver(ws, player),
            sender(ws, player)
        )

if __name__ == "__main__":
    asyncio.run(main())