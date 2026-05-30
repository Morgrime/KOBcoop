import asyncio
import websockets
import json
import logging
import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Теперь импорты будут работать
from shared.models.board import Board
from shared.models.piece import Piece
from shared.rules import validate_rook_move

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

connected_clients = set()
game_board = Board()
current_turn = "white"
game_board.set_piece(4, 5, Piece("rook", "black"))


async def handler(websocket):
    global current_turn
    connected_clients.add(websocket)
    logging.info(f"Клиент подключился. Всего {len(connected_clients)}")

    await websocket.send(json.dumps({
        "type": "state_update",
        "board": game_board.to_dict()
    }))

    try:
        async for message in websocket:
            try:
                # JSON в питон словарь
                data = json.loads(message)
                logging.info(f"Получено: {data}")

                # Кто ходил и их время
                data["sender_id"] = id(websocket)

                if data["type"] == "move":
                    try:
                        from_pos = tuple(data["from_pos"],)
                        to_pos = tuple(data["to_pos"],)

                    except KeyError:
                        # Отправка только клиенту
                        await websocket.send(json.dumps({"status": "invalid_move", "msg": "Не хватает полей"}))
                        continue

                    if validate_rook_move(game_board, from_pos, to_pos, current_turn):
                        game_board.apply_move(
                            from_pos,
                            to_pos
                            # data["from_pos"],
                            # data["to_pos"]
                        )
                        
                        current_turn == "black" if current_turn == "white" else "white"
                        data["current_turn"] = current_turn

                        if connected_clients:
                            await asyncio.gather(
                                *[c.send(json.dumps(data)) for c in connected_clients],
                                return_exceptions=True,
                            )

                    else:
                        # Отправка только клиенту
                        await websocket.send(json.dumps({"status": "invalid_move", "msg": "Ход запрещен правилами"}))
                        continue

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
