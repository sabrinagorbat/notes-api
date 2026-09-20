import random

with open("sample.log", "w", encoding="utf-8") as f:
    for i in range(100000):
        status = random.choices(["INFO", "WARNING", "ERROR"], weights=[80, 15, 5])[0]
        f.write(f"[{status}] Событие #{i}: Описание операции\n")
print("Файл sample.log успешно создан!")