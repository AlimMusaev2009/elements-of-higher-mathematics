import math
import cmath


def power_by_multiplication(z, n):
    result = complex(1.0, 0.0)
    for _ in range(n):
        result *= z
    return result

def power_by_moivre(radius, angle, n):
    radius_power = radius ** n
    return complex(radius_power * math.cos(n * angle), radius_power * math.sin(n * angle))

def induction_step(radius, angle, k):
    radius_k = radius ** k
    real_k = radius_k * math.cos(k * angle)
    imag_k = radius_k * math.sin(k * angle)
    real_z = radius * math.cos(angle)
    imag_z = radius * math.sin(angle)
    return complex(real_k * real_z - imag_k * imag_z, real_k * imag_z + imag_k * real_z)

def show_step(z, k):
    radius, angle = abs(z), cmath.phase(z)

    by_multiplication = power_by_multiplication(z, k + 1)
    by_moivre = power_by_moivre(radius, angle, k + 1)
    by_induction = induction_step(radius, angle, k)

    print(f"k = {k}:")
    print(f"прямое умножение: {by_multiplication}")
    print(f"Муавр для n = k+1: {by_moivre}")
    print(f"индукционный шаг k -> k+1: {by_induction}")
    print(f"прямое-Муавр = {abs(by_multiplication - by_moivre):.3e}")
    print(f"шаг-Муавр = {abs(by_induction - by_moivre):.3e}")
    print()

def show_validation(test_cases, k_range):
    for z, label in test_cases:
        print(f"=== {label} ===")
        for k in k_range:
            show_step(z, k)

test_cases = [
    (1.5 + 0.0j, "z = 1.5"),
    (0.0 + 1.0j, "z = i"),
    (1.0 + 1.0j, "z = 1 + i"),
    (-2.0 + 1.5j, "z = -2 + 1.5i"),
    (0.3 - 0.7j, "z = 0.3 - 0.7i"),
]

show_validation(test_cases, range(1, 6))