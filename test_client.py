import asyncio
import websockets
import json

async def test_client():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as ws:
        # Отправка словаря
        msg = {"type": "ping", "player": "white", "payload": "hello"}
        await ws.send(json.dumps(msg))
        print(f"Отправлено: {msg}")

        # Ждем
        response = await ws.recv()
        print(f"Получено от сервера: {json.loads(response)}")

if __name__ == "__main__":
    asyncio.run(test_client())