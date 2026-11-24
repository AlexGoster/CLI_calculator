# CLI Calculator

Калькулятор в командной строке: +, -, *, /; история в calculator_history.json. Ошибка ввода в интерактивном режиме не завершает сеанс. Повреждённая история сохраняется без перезаписи. NaN/Infinity и переполнение результата отклоняются.

Требуется Python 3.10+. Графический интерфейс и сторонние зависимости не нужны.

```bash
python calculator.py 5 + 3
python calculator.py --history
python calculator.py --clear
python calculator.py
```

Проверка:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

Тесты проверяют CLI, восстановление после ошибочного ввода и сохранность истории во временных файлах.
