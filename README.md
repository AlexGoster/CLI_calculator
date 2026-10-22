# CLI Calculator

Калькулятор в командной строке: +, -, *, /; история в calculator_history.json. Ошибка ввода в интерактивном режиме не завершает сеанс. Повреждённая история сохраняется без перезаписи. NaN/Infinity и переполнение результата отклоняются.

Требуется Python с Tkinter для GUI-проектов.

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

GUI-тесты создают настоящие виджеты в скрытых окнах.
