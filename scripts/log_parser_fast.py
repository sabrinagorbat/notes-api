import time
import re

def parse_logs_fast(filename):
    errors = []
    error_pattern = re.compile(r"ERROR|error|ОШИБКА")
    line_count = 0
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line_count += 1
            if error_pattern.search(line):
                errors.append(f"Строка {line_count}: {line.strip()}")
    return errors

start = time.time()
result = parse_logs_fast("sample.log")
print(f"Найдено ошибок: {len(result)}")
print(f"Время выполнения: {time.time() - start:.2f} секунд")