import asyncio
import websockets
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

connected_clients = set()


async def handler(websocket):
    connected_clients.add(websocket)
    logging.info(f"Клиент подключился. Всего {len(connected_clients)}")

    try:
        async for message in websocket:
            try:
                # JSON в питон словарь
                data = json.loads(message)
                logging.info(f"Получено: {data}")

                # Пока эхо ответ, потом валидация будет
                response = {"status": "ok", "received_type": data.get("type")}
                await websocket.send(json.dumps(response))

            except json.JSONDecodeError:
                logging.warning("Пришла некорректная json строка")
                await websocket.send(json.dumps({"status": "error", "msg": "bad json"}))

    except websockets.exceptions.ConnectionClosed:
        logging.info("Клиент отключился (нормально)")
    finally:
        # Всегда очищаем список сокетов, чтобы не хранить мертвые соединения
        connected_clients.discard(websocket)
        logging.info(f"Клиент удален. Онлайн: {len(connected_clients)}")


async def main():
    HOST = "localhost"
    PORT = 8765
    logging.info(f"Запуск сервера на ws://{HOST}:{PORT}")

    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
