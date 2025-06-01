Crypto Signal Bot (Offline GUI)
-------------------------------
Этот проект позволяет запускать сигнальный анализатор без Telegram, прямо в Windows через интерфейс.

📁 Состав:
- interface.py — графический интерфейс
- analyzer.py, performance_evaluator.py и другие должны быть добавлены вами
- Установите зависимости: pip install ta pandas numpy httpx openai telegram

🏗️ Как собрать .exe:
1. Установите pyinstaller: pip install pyinstaller
2. Выполните команду: pyinstaller interface.py --onefile --noconsole
3. Найдите .exe в папке dist/