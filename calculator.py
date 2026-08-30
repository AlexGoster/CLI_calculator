import argparse
import json
import os
import sys

HISTORY_FILE = "calculator_history.json"


def load_history():
    """Загружает историю из JSON-файла."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    """Сохраняет историю в JSON-файл."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def add_record(expr, result):
    """Добавляет запись в историю."""
    history = load_history()
    history.append({"expression": expr, "result": result})
    save_history(history)


def clear_history():
    """Удаляет файл с историей."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        print("История очищена.")
    else:
        print("История пуста.")


def show_history():
    """Выводит историю вычислений."""
    history = load_history()
    if not history:
        print("История пуста.")
        return
    print("История вычислений:")
    for idx, record in enumerate(history, 1):
        print(f"{idx}. {record['expression']} = {record['result']}")


def calculate(a, op, b):
    """Выполняет арифметическую операцию."""
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        print("Ошибка: операнды должны быть числами.")
        sys.exit(1)

    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            print("Ошибка: деление на ноль.")
            sys.exit(1)
        return a / b
    else:
        print(f"Ошибка: неизвестная операция '{op}'.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Калькулятор с историей")
    parser.add_argument("a", nargs="?", help="Первый операнд")
    parser.add_argument("op", nargs="?", help="Операция (+, -, *, /)")
    parser.add_argument("b", nargs="?", help="Второй операнд")
    parser.add_argument("--history", action="store_true", help="Показать историю")
    parser.add_argument("--clear", action="store_true", help="Очистить историю")
    args = parser.parse_args()

    # Обработка специальных флагов
    if args.clear:
        clear_history()
        sys.exit(0)
    if args.history:
        show_history()
        sys.exit(0)

    # Если аргументы не переданы, запускаем интерактивный режим
    if not (args.a and args.op and args.b):
        print("Интерактивный режим. Введите выражение в формате: число операция число")
        print("Например: 5 + 3")
        while True:
            expr = input("> ").strip()
            if expr.lower() in ('q', 'quit', 'exit'):
                print("Выход из калькулятора.")
                break
            if not expr:
                continue
            parts = expr.split()
            if len(parts) != 3:
                print("Неверный формат. Нужно три части: число, операция, число.")
                continue
            a, op, b = parts
            result = calculate(a, op, b)
            expr_str = f"{a} {op} {b}"
            print(f"{expr_str} = {result}")
            add_record(expr_str, result)
        sys.exit(0)

    # Обычный режим с аргументами
    expr_str = f"{args.a} {args.op} {args.b}"
    result = calculate(args.a, args.op, args.b)
    print(f"{expr_str} = {result}")
    add_record(expr_str, result)


if __name__ == "__main__":
    main()
