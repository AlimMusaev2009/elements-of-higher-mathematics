from calculator import compute, save_csv

METHODS = {
    "1": ("left", "Левые прямоугольники"),
    "2": ("right", "Правые прямоугольники"),
    "3": ("mid", "Средние прямоугольники"),
    "4": ("trap", "Трапеции"),
}


def ask(prompt: str) -> str:
    return input(prompt).strip()


def main():
    print("=== Калькулятор интегралов ===")
    expr = ask("f(x) = ")
    try:
        a = float(ask("a = "))
        b = float(ask("b = "))
    except ValueError:
        print("Ошибка: a и b должны быть числами")
        return
    if a >= b:
        print("Ошибка: требуется a < b")
        return

    print("Режим сетки:")
    print("  1) По числу шагов N")
    print("  2) По шагу h")
    mode = ask("Выбор [1/2]: ")
    steps = None
    h = None
    try:
        if mode == "1":
            steps = int(ask("N = "))
        elif mode == "2":
            h = float(ask("h = "))
        else:
            print("Ошибка: неверный выбор режима")
            return
    except ValueError:
        print("Ошибка: некорректное число")
        return

    print("Метод:")
    for k, (_, name) in METHODS.items():
        print(f"  {k}) {name}")
    m = ask("Выбор [1-4]: ")
    if m not in METHODS:
        print("Ошибка: неверный метод")
        return
    method = METHODS[m][0]

    try:
        res = compute(expr, a, b, steps, h, method)
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    # вывод таблицы
    print("\n" + "-" * 40)
    print(f"{'x':>15} | {'f(x)':>15}")
    print("-" * 40)
    for x, y in res.table:
        ytxt = "  (ошибка)" if y is None else f"{y:.8g}"
        print(f"{x:>15.8g} | {ytxt:>15}")
    print("-" * 40)
    print(f"Интеграл ≈ {res.integral:.10g}")

    # сохранение
    if ask("\nСохранить в CSV? [y/N]: ").lower() == "y":
        path = ask("Путь к файлу (например, out.csv): ")
        header = [
            f"f(x) = {expr}",
            f"a = {a}, b = {b}",
            f"Режим: {'N=' + str(steps) if steps else 'h=' + str(h)}",
            f"Метод: {METHODS[m][1]}",
            f"Значение интеграла: {res.integral:.10g}",
        ]
        try:
            save_csv(path, res, header)
            print(f"Сохранено: {path}")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")


if __name__ == "__main__":
    main()
