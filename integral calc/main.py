from calculator import compute, save_csv

METHODS = {
    "1": ("left", "Левые прямоугольники"),
    "2": ("right", "Правые прямоугольники"),
    "3": ("mid", "Средние прямоугольники"),
    "4": ("trap", "Трапеции"),
}


def ask(prompt: str) -> str:
    return input(prompt).strip()


def ask_float(prompt: str, hint: str) -> float:
    while True:
        val = ask(f"{prompt} ({hint}): ")
        try:
            return float(val)
        except ValueError:
            print("  ⚠ Ошибка: нужно ввести число. Попробуйте ещё раз.")


def ask_int(prompt: str, hint: str) -> int:
    while True:
        val = ask(f"{prompt} ({hint}): ")
        try:
            return int(val)
        except ValueError:
            print("  ⚠ Ошибка: нужно ввести целое число. Попробуйте ещё раз.")


def main():
    print("=" * 50)
    print("       КАЛЬКУЛЯТОР ОПРЕДЕЛЁННЫХ ИНТЕГРАЛОВ")
    print("=" * 50)
    print("Программа вычислит интеграл функции на отрезке [a, b]")
    print("и построит таблицу значений с заданным шагом.\n")

    # --- Ввод функции ---
    print("[1] Введите функцию f(x).")
    print("    Можно использовать: + - * / **, а также sin, cos, tan,")
    print("    exp, log, sqrt, pi и другие из модуля math.")
    print("    Примеры:  x**2 + 2*x + 1    |    sin(x) + exp(-x)    |    sqrt(x)")
    expr = ask("f(x) = ")
    if not expr:
        print("  ⚠ Ошибка: функция не задана.")
        return

    # --- Ввод границ ---
    print("\n[2] Введите границы интегрирования a и b.")
    print("    Требование: a < b.")
    a = ask_float("a", "нижняя граница, число")
    b = ask_float("b", "верхняя граница, число")
    if a >= b:
        print(f"  ⚠ Ошибка: a = {a} должно быть меньше b = {b}.")
        return

    # --- Ввод сетки ---
    print("\n[3] Выберите способ задания сетки:")
    print("    1) По числу шагов N (точек будет N+1)")
    print("    2) По фиксированному шагу h")
    mode = ask("Выбор [1/2]: ")
    steps = None
    h = None
    if mode == "1":
        steps = ask_int("N", "целое число > 0, например 10")
        if steps <= 0:
            print("  ⚠ Ошибка: N должно быть > 0.")
            return
    elif mode == "2":
        h = ask_float("h", "шаг > 0, например 0.1")
        if h <= 0:
            print("  ⚠ Ошибка: h должно быть > 0.")
            return
    else:
        print("  ⚠ Ошибка: неверный выбор режима.")
        return

    # --- Ввод метода ---
    print("\n[4] Выберите метод численного интегрирования:")
    for k, (_, name) in METHODS.items():
        print(f"    {k}) {name}")
    m = ask("Выбор [1-4]: ")
    if m not in METHODS:
        print("  ⚠ Ошибка: неверный метод.")
        return
    method = METHODS[m][0]

    # --- Расчёт ---
    try:
        res = compute(expr, a, b, steps, h, method)
    except Exception as e:
        print(f"\n  ⚠ Ошибка вычисления: {e}")
        return

    # --- Вывод таблицы ---
    print("\n" + "-" * 40)
    print(f"{'x':>15} | {'f(x)':>15}")
    print("-" * 40)
    for x, y in res.table:
        ytxt = "  (ошибка)" if y is None else f"{y:.8g}"
        print(f"{x:>15.8g} | {ytxt:>15}")
    print("-" * 40)
    print(f"Значение интеграла ≈ {res.integral:.10g}")

    # --- Сохранение ---
    ans = ask("\n[5] Сохранить результат в CSV? [y/N]: ").lower()
    if ans == "y":
        print("    Укажите имя файла, например: result.csv")
        path = ask("Путь к файлу: ")
        if not path:
            print("  ⚠ Файл не сохранён (пустой путь).")
            return
        header = [
            f"f(x) = {expr}",
            f"a = {a}, b = {b}",
            f"Режим: {'N=' + str(steps) if steps else 'h=' + str(h)}",
            f"Метод: {METHODS[m][1]}",
            f"Значение интеграла: {res.integral:.10g}",
        ]
        try:
            save_csv(path, res, header)
            print(f"  ✓ Сохранено: {path}")
        except Exception as e:
            print(f"  ⚠ Ошибка сохранения: {e}")


if __name__ == "__main__":
    main()
