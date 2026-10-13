import argparse
import json
import math
import os
import sys

HISTORY_FILE = "calculator_history.json"


def load_history():
    """Загружает историю из JSON-файла."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
            if not isinstance(history, list) or any(
                not isinstance(record, dict) or "expression" not in record or "result" not in record
                for record in history
            ):
                raise ValueError("Неверный формат истории вычислений.")
            return history
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
        raise ValueError("Операнды должны быть числами.") from None
    if not math.isfinite(a) or not math.isfinite(b):
        raise ValueError("Операнды должны быть конечными числами.")

    if op == '+':
        result = a + b
    elif op == '-':
        result = a - b
    elif op == '*':
        result = a * b
    elif op == '/':
        if b == 0:
            raise ValueError("Деление на ноль.")
        result = a / b
    else:
        raise ValueError(f"Неизвестная операция '{op}'.")
    if not math.isfinite(result):
        raise ValueError("Результат слишком велик.")
    return result


def main():
    parser = argparse.ArgumentParser(description="Калькулятор с историей")
    parser.add_argument("a", nargs="?", help="Первый операнд")
    parser.add_argument("op", nargs="?", help="Операция (+, -, *, /)")
    parser.add_argument("b", nargs="?", help="Второй операнд")
    parser.add_argument("--history", action="store_true", help="Показать историю")
    parser.add_argument("--clear", action="store_true", help="Очистить историю")
    args = parser.parse_args()
    if any(value is not None for value in (args.a, args.op, args.b)) and not all(
        value is not None for value in (args.a, args.op, args.b)
    ):
        parser.error("Нужно указать оба операнда и оператор.")

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
            try:
                expr = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
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
            try:
                result = calculate(a, op, b)
            except ValueError as exc:
                print(f"Ошибка: {exc}")
                continue
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
    try:
        main()
    except (ValueError, OSError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        sys.exit(1)
