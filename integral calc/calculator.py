import math
import csv
from dataclasses import dataclass

ALLOWED_NAMES = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}


@dataclass
class Result:
    integral: float
    table: list[tuple[float, float | None]]


def parse_function(expr: str):
    if not expr.strip():
        raise ValueError("Функция не задана")
    try:
        code = compile(expr, "<func>", "eval")
    except SyntaxError as e:
        raise ValueError(f"Синтаксическая ошибка: {e}")

    # Разрешаем переменную x наравне с функциями из math
    allowed = set(ALLOWED_NAMES.keys())
    allowed.add("x")

    for name in code.co_names:
        if name not in allowed:
            raise ValueError(f"Неизвестное имя: {name}")

    def f(x):
        return eval(code, {"__builtins__": {}}, {**ALLOWED_NAMES, "x": x})

    return f


def build_grid(a: float, b: float, steps: int | None = None, h: float | None = None):
    if steps is not None:
        if steps <= 0:
            raise ValueError("Число шагов должно быть > 0")
        return [a + i * (b - a) / steps for i in range(steps + 1)]
    if h is not None:
        if h <= 0:
            raise ValueError("Шаг должен быть > 0")
        n = int(math.floor((b - a) / h))
        xs = [a + i * h for i in range(n + 1)]
        if xs[-1] < b - 1e-12:
            xs.append(b)
        return xs
    raise ValueError("Не задан шаг или число точек")


def evaluate_table(f, xs):
    table = []
    for x in xs:
        try:
            y = f(x)
            if not isinstance(y, (int, float)) or math.isnan(y) or math.isinf(y):
                table.append((x, None))
            else:
                table.append((x, float(y)))
        except ZeroDivisionError:
            table.append((x, None))
        except Exception:
            table.append((x, None))
    return table


def integrate(method: str, xs, ys) -> float:
    s = 0.0
    if method == "left":
        for i in range(len(xs) - 1):
            if ys[i] is not None:
                s += ys[i] * (xs[i + 1] - xs[i])
    elif method == "right":
        for i in range(len(xs) - 1):
            if ys[i + 1] is not None:
                s += ys[i + 1] * (xs[i + 1] - xs[i])
    elif method in ("mid", "trap"):
        for i in range(len(xs) - 1):
            if ys[i] is not None and ys[i + 1] is not None:
                s += ((ys[i] + ys[i + 1]) / 2) * (xs[i + 1] - xs[i])
    else:
        raise ValueError(f"Неизвестный метод: {method}")
    return s


def compute(expr: str, a: float, b: float,
            steps: int | None, h: float | None, method: str) -> Result:
    if a >= b:
        raise ValueError("Требуется a < b")
    f = parse_function(expr)
    xs = build_grid(a, b, steps, h)
    table = evaluate_table(f, xs)
    integral = integrate(method, [x for x, _ in table], [y for _, y in table])
    return Result(integral=integral, table=table)


def save_csv(path: str, result: Result, header: list[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for line in header:
            w.writerow([line])
        w.writerow([])
        w.writerow(["x", "f(x)"])
        for x, y in result.table:
            w.writerow([f"{x:.8g}", "" if y is None else f"{y:.8g}"])
        w.writerow([])
        w.writerow(["Интеграл", f"{result.integral:.10g}"])
