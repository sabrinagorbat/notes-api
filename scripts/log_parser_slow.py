import time

def parse_logs_slow(filename):
    errors = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            for word in ["ERROR", "error", "ОШИБКА"]:
                if word in line:
                    for char in line:
                        if char == ":":
                            errors.append(f"Строка {i}: {line.strip()}")
                            break
                    break
    return errors

start = time.time()
result = parse_logs_slow("sample.log")
print(f"Найдено ошибок: {len(result)}")
print(f"Время выполнения: {time.time() - start:.2f} секунд")