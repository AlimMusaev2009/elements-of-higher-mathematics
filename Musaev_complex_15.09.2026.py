# -*- coding: utf-8 -*-
"""
ДЗ: Геометрия комплексных чисел. Формула Муавра.
"""
import math
import random
import matplotlib.pyplot as plt


# ============================================================
# Функции из шаблона (только math)
# ============================================================
def to_polar(a, b):
    """(a, b) -> (r, phi)."""
    return math.sqrt(a * a + b * b), math.atan2(b, a)


def to_algebraic(r, phi):
    """(r, phi) -> (a, b)."""
    return r * math.cos(phi), r * math.sin(phi)


def power_demoivre(a, b, n):
    """(a+bi)^n по формуле Муавра. Без ** и без cmath."""
    r, phi = to_polar(a, b)
    r_n = math.exp(n * math.log(r)) if r != 0 else 0.0
    phi_n = n * phi
    return to_algebraic(r_n, phi_n)


def rotate_shape(points, angle_deg):
    """Поворот точек на angle_deg через комплексное умножение."""
    a = math.radians(angle_deg)
    out = []
    for x, y in points:
        r, phi = to_polar(x, y)
        out.append(to_algebraic(r, phi + a))
    return out


def spirograph(turns=8, points_per_turn=200, growth=0.02, r0=1.0):
    """r_k = r0*(1+g)^k, phi_k = k*delta_phi; возвращает xs, ys."""
    delta_phi = 2 * math.pi / points_per_turn
    xs, ys = [], []
    r = r0
    for k in range(turns * points_per_turn + 1):
        phi = k * delta_phi
        xs.append(r * math.cos(phi))
        ys.append(r * math.sin(phi))
        r *= (1 + growth)
    return xs, ys


# ============================================================
# Задача 1. z = 1 + i*sqrt(3) -> тригонометрическая форма
# ============================================================
def task1():
    r, phi = to_polar(1.0, math.sqrt(3.0))
    print("Задача 1: r = {:.4f}, phi = {:.4f} рад ({}°)".format(
        r, phi, round(math.degrees(phi), 2)))


# ============================================================
# Задача 2. (1+i)^10
# ============================================================
def task2():
    a, b = power_demoivre(1.0, 1.0, 10)
    print("Задача 2: (1+i)^10 = {:.6f} + {:.6f}i".format(a, b))


# ============================================================
# Задача 3. Модуль и аргумент z1 = -1+3i, z2 = -sqrt(3)-2i
# ============================================================
def task3():
    for name, a, b in (("z1", -1.0, 3.0),
                       ("z2", -math.sqrt(3.0), -2.0)):
        r, phi = to_polar(a, b)
        print("Задача 3: {}: r = {:.4f}, phi = {:.4f} рад ({}°)".format(
            name, r, phi, round(math.degrees(phi), 2)))


# ============================================================
# Задача 4. z1 = 2(cos40°+i sin40°), z2 = 5(cos20°+i sin20°)
# ============================================================
def task4():
    r1, p1 = 2.0, math.radians(40)
    r2, p2 = 5.0, math.radians(20)

    rp, pp = r1 * r2, p1 + p2
    rq, pq = r1 / r2, p1 - p2

    ap, bp = to_algebraic(rp, pp)
    aq, bq = to_algebraic(rq, pq)
    print("Задача 4: z1*z2 = {:.3f}*(cos{}°+i sin{}°) = ({:.4f}, {:.4f})".format(
        rp, round(math.degrees(pp), 2), round(math.degrees(pp), 2), ap, bp))
    print("Задача 4: z1/z2 = {:.3f}*(cos{}°+i sin{}°) = ({:.4f}, {:.4f})".format(
        rq, round(math.degrees(pq), 2), round(math.degrees(pq), 2), aq, bq))


# ============================================================
# Задача 5. (3/2 + sqrt(3)/2 * i)^12
# ============================================================
def task5():
    a, b = power_demoivre(1.5, math.sqrt(3.0) / 2.0, 12)
    print("Задача 5: результат = {:.6f} + {:.6f}i".format(a, b))


# ============================================================
# Уровень 2: проверка Муавра (эталон — повторное умножение)
# ============================================================
def check_demoivre():
    for _ in range(5):
        a, b = random.uniform(-5, 5), random.uniform(-5, 5)
        n = random.randint(1, 8)
        got = power_demoivre(a, b, n)

        exp_a, exp_b = 1.0, 0.0
        for _ in range(n):
            exp_a, exp_b = exp_a * a - exp_b * b, exp_a * b + exp_b * a

        print("Муавр: ({:.3f}{:+.3f}i)^{} = ({:.6f}, {:.6f}) | "
              "эталон ({:.6f}, {:.6f})".format(
                  a, b, n, got[0], got[1], exp_a, exp_b))


# ============================================================
# Уровень 2: поворот корабля
# ============================================================
def demo_rotation():
    ship = [(0, 1), (-0.6, -1), (0, -0.5), (0.6, -1)]
    rotated = rotate_shape(ship, 40)

    def draw(pts, color, label):
        xs, ys = zip(*(pts + [pts[0]]))
        plt.plot(xs, ys, color=color, marker='o', label=label)

    plt.figure(figsize=(6, 6))
    draw(ship, 'gray', 'до поворота')
    draw(rotated, 'purple', 'после поворота на 40°')
    plt.gca().set_aspect('equal')
    plt.legend()
    plt.savefig("ship_rotation.png", dpi=120)
    plt.show()


# ============================================================
# BOSS: спирограф
# ============================================================
def demo_spirograph():
    xs, ys = spirograph(turns=8, points_per_turn=200, growth=0.02)
    plt.figure(figsize=(5, 5))
    plt.plot(xs, ys, linewidth=0.8, color='indigo')
    plt.axis('off')
    plt.gca().set_aspect('equal')
    plt.savefig("spirograph.png", dpi=150)
    plt.show()



if __name__ == "__main__":
    task1()
    task2()
    task3()
    task4()
    task5()
    check_demoivre()
    demo_rotation()
    demo_spirograph()
