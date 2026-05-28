"""
Лабораторный шаблон: Линейные операторы в Computer Vision
Студент: [Фамилия И.О.]
Группа: [Номер группы]
"""

import numpy as np
from scipy.linalg import null_space, orth
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Задание 1: Проекция ---
print("--- Задание 1: Ортогональная проекция ---")

# Матрица проекции на плоскость XY
P = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])

print("Матрица P:\n", P)

# 1. Ядро (Null Space)
# null_space возвращает базис ядра (столбцы матрицы)
ker_P = null_space(P)
print("\nБазис ядра (Ker P):\n", ker_P)
print("Размерность ядра (Defect):", ker_P.shape[1])

# 2. Образ (Column Space / Range)
# Используем QR-разложение или SVD для нахождения базиса образа
# Здесь просто возьмем линейно независимые столбцы
rank_P = np.linalg.matrix_rank(P)
print("Ранг (Rank):", rank_P)

# Проверка теоремы о ранге и дефекте
dim_V = 3
print(f"Проверка: Rank ({rank_P}) + Defect ({ker_P.shape[1]}) = {rank_P + ker_P.shape[1]} == Dim V ({dim_V})")

# --- Задание 2: Обратимость оператора A ---
print("\n--- Задание 2: Анализ обратимости ---")

# Параметр k
k = 1.0 

A = np.array([
    [2, -1, 0],
    [1,  0, 0],
    [0,  0, k]
])

print(f"Матрица A (при k={k}):\n", A)

# 1. Определитель
det_A = np.linalg.det(A)
print(f"Определитель det(A): {det_A:.4f}")

if abs(det_A) > 1e-10:
    print("Оператор обратим (det != 0)")
    
    # 2. Обратная матрица
    A_inv = np.linalg.inv(A)
    print("Обратная матрица A^-1:\n", np.round(A_inv, 4))
    
    # Проверка: A * A_inv = E
    E_check = np.dot(A, A_inv)
    print("Проверка (A * A_inv):\n", np.round(E_check, 4))
else:
    print("Оператор вырожден (необратим)")

# Исследование при k -> 0
k_small = 1e-9
A_degen = np.array([
    [2, -1, 0],
    [1,  0, 0],
    [0,  0, k_small]
])
print(f"\nПри k={k_small}: det(A) = {np.linalg.det(A_degen):.2e}")
ker_A_degen = null_space(A_degen)
print("Базис ядра вырожденного оператора:\n", ker_A_degen)

# --- Задание 3: Восстановление координат ---
print("\n--- Задание 3: Система уравнений ---")

# Уравнение P * x = y
y = np.array([2, 1, 0])

# Частное решение (можно взять псевдообратную матрицу Пэнроуза)
# x_part = P^+ * y
x_part = np.linalg.pinv(P) @ y
print(f"Частное решение (ближайшее к началу координат): {x_part}")

# Общее решение: x = x_part + c * v_ker
v_ker = ker_P[:, 0] # Базисный вектор ядра
print(f"Вектор ядра: {v_ker}")

# Если известно, что z = 5
z_target = 5
# x_part имеет z=0. Нам нужно добавить столько вектора ядра, чтобы z стало 5.
# v_ker = [0, 0, 1]. Значит, коэффициент c = 5.
c = z_target / v_ker[2] if v_ker[2] != 0 else 0
x_final = x_part + c * v_ker
print(f"Решение при условии z={z_target}: {x_final}")

# --- Задание 4: Визуализация (Опционально) ---
"""
Постройте луч зрения, проходящий через точку (2,1) на экране.
"""
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Плоскость экрана (Z=0)
xx, yy = np.meshgrid(np.linspace(-1, 3, 10), np.linspace(-1, 3, 10))
zz = np.zeros_like(xx)
ax.plot_surface(xx, yy, zz, alpha=0.2, color='cyan')

# Луч зрения (линия вдоль оси Z через точку (2,1))
z_line = np.linspace(0, 5, 10)
x_line = np.full_like(z_line, 2)
y_line = np.full_like(z_line, 1)
ax.plot(x_line, y_line, z_line, 'r-', linewidth=2, label='Луч зрения (Ker shift)')

# Точки
ax.scatter([2], [1], [0], color='blue', s=100, label='Проекция (2,1,0)')
ax.scatter([2], [1], [5], color='green', s=100, label='Реальная точка (2,1,5)')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Геометрическая интерпретация ядра проекции')
ax.legend()
ax.set_xlim([0, 3])
ax.set_ylim([0, 3])
ax.set_zlim([0, 6])

plt.show()