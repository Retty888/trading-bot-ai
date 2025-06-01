import tkinter as tk
from analyzer import run_signals_analysis, run_scalp_analysis, run_swing_analysis
from performance_evaluator import evaluate_all_signals
import asyncio

def run_async_task(task_func, text_widget):
    async def runner():
        summary, signals = await task_func()
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, summary + "\n\n")
        for s in signals:
            if s:
                text_widget.insert(tk.END,
                    f"{s['symbol']} | {s['direction']} | Entry: {s['entry']} | TP: {s['take_profit']} | SL: {s['stop_loss']} | Score: {s['score']}\n"
                )
    asyncio.run(runner())

def evaluate_signals(text_widget):
    result = evaluate_all_signals()
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, result)

root = tk.Tk()
root.title("💹 Crypto Signal Bot (Offline GUI)")

frame = tk.Frame(root)
frame.pack(pady=10)

output = tk.Text(root, height=25, width=100)
output.pack()

tk.Button(frame, text="📶 Основные сигналы", command=lambda: run_async_task(run_signals_analysis, output)).grid(row=0, column=0, padx=5)
tk.Button(frame, text="⚡ Скальп ETH", command=lambda: run_async_task(lambda: run_scalp_analysis(symbols=["ETHUSDT"]), output)).grid(row=0, column=1, padx=5)
tk.Button(frame, text="📈 Swing сигналы", command=lambda: run_async_task(run_swing_analysis, output)).grid(row=0, column=2, padx=5)
tk.Button(frame, text="🧠 Evaluate", command=lambda: evaluate_signals(output)).grid(row=0, column=3, padx=5)

root.mainloop()