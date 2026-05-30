# test_client.py
import asyncio
import websockets
import json
import sys
from shared.models.board import Board

async def receiver(ws, player_name):
    """Фоновая задача: слушает сервер и выводит сообщения"""
    current_board = Board()

    try:
        async for message in ws:
            data = json.loads(message)
            msg_type = data.get("type")

            if msg_type == "state_update":
                current_board = Board.from_dict(data["board"])

            elif msg_type == "move":
                current_board.apply_move(tuple(data["from_pos"]), tuple(data["to_pos"]))

            elif msg_type == "invalid_move" or data.get("status") == "invalid_move":
                print(f"\n {data.get('msg', 'Неверный ход')}", file=sys.stderr)
                continue

            elif data.get("status") == "error":
                print(f"\n {data.get('msg')}", file=sys.stderr)
                continue

            draw_screen(current_board, player_name)

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

def draw_screen(board: Board, player_name: str):
    # \033[2J очищает экран, \033[H возвращает курсор в левый верхний угол
    print("\033[2J\033[H", end="")
    print(f"Игрок: {player_name}\n")
    print(board.display())
    print("\nФормат хода: {\"type\": \"move\", \"from_pos\": [r,c], \"to_pos\": [r,c], \"color\": \"...\"}")
    print("Твой ход > ", end="", flush=True)


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