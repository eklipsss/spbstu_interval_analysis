import numpy as np
np.float_ = np.float64
from intvalpy import Interval, mid, subset, intersection
from tabulate import tabulate


# вывод интервальной матрицы
def print_table(matrix, headers):
    print('print_table')
    output = [
        [str(matrix[0][0]), str(matrix[0][1])],
        [str(matrix[1][0]), str(matrix[1][1])]
    ]
    print(tabulate(output, headers, tablefmt="simple_grid", stralign='center'))

# создание интервальной матрицы с радиусом eps
def create_intval_matrix(eps):
    A = Interval([
          [[1.05-eps, 1.05+eps], [0.95-eps, 0.95+eps]],
          [[1-eps, 1+eps], [1-eps, 1+eps]]
        ])

    print(f"\n---------------------------------------------------------\neps = {eps}")
    print_table(A, headers=[])

    return A

# вычисление определителя матрицы
def determinant_matrix(A):
    a = A[0][0]*A[1][1]
    b = A[0][1]*A[1][0]
    res = a - b
    print("Calc det(A):")
    print(f"\n  1) A[0][0]*A[1][1] = {A[0][0]}*{A[1][1]} = {a}")
    print(f"\n  2) A[0][1]*A[1][0] = {A[0][1]}*{A[1][0]} = {b}")
    print(f"\n  3) A[0][0]*A[1][1] - A[0][1]*A[1][0] = {a}*{b} = {res}")
    return res

# преобразование матрицы: в столбцы или строки записывается пересечение исходных интервалов
def intersection_row_or_columns(A):
    # пересечение в столбцах
    print(intersection(A[0][0], A[0][1]))
    print ('YYYYY')
    print(intersection(A[0][0], A[0][1]) == nan)
    if intersection(A[0][0], A[1][0]) != nan:
        if intersection(A[1][1], A[0][1]) != nan:
            res = [
                [intersection(A[0][0], A[1][0]), intersection(A[1][1], A[0][1])],
                [intersection(A[0][0], A[1][0]), intersection(A[1][1], A[0][1])]
            ]
            return res
    # пересечение в строчках
    if intersection(A[0][0], A[0][1]) != nan:
        if intersection(A[1][1], A[1][0]) != nan:
            res = [
                [intersection(A[0][0], A[0][1]), intersection(A[0][0], A[0][1])],
                [intersection(A[1][1], A[1][0]), intersection(A[1][1], A[1][0])]
            ]
            return res
    return None


def get_singular_matrices(A):
    step = 0.001
    arr_matrix = []
    print(f"Введите левую границу данного интервала {A[0][0]}: ")
    a00_left = float(input())
    print(f"Введите правую границу данного интервала {A[0][0]}: ")
    a00_right = float(input())

    # a00_left, a00_right = 1.025, 1.025

    A1 = []
    A2 = []
    if intersection(A[0][0], A[1][0]) != nan:
        while a00_left <= a00_right:
            A1.append(a00_left)
            a00_left += step
        print(f"Введите левую границу данного интервала {A[0][1]}: ")
        a01_left = float(input())
        print(f"Введите правую границу данного интервала {A[0][1]}: ")
        a01_right = float(input())
        # a01_left, a01_right = 0.975, 0.975

        while a01_left <= a01_right:
            A2.append(a01_left)
            a01_left += step
        print(A2)
        for a1 in A1:
            for a2 in A2:
                dot_A = [[a1, a2],
                         [a1, a2]]
                arr_matrix.append(dot_A)

    # if intersection(A[0][0], A[0][1]) != nan:
    else:
        while a00_left <= a00_right:
            A1.append(a00_left)
            a00_left += step
        print(f"Введите левую границу данного интервала {A[1][0]}: ")
        a10_left = float(input())
        print(f"Введите правую границу данного интервала {A[1][0]}: ")
        a10_right = float(input())
        while a10_left <= a10_right:
            A2.append(a10_left)
            a10_left += step
        for a1 in A1:
            for a2 in A2:
                dot_A = [[a1, a1],
                         [a2, a2]]
                arr_matrix.append(dot_A)

    return arr_matrix



precision = 3
eps_start = 0
step = 0.01
print("STEP = ", step)

A = create_intval_matrix(eps_start)
det_interval = determinant_matrix(A)

iter_count = 0
count = 0

nan = intersection(Interval(1, 1), Interval(2, 2))



while 0 not in det_interval:
    count += 1
    print("\ndet(A) = ", det_interval)
    eps = eps_start + step*count
    A = create_intval_matrix(eps)
    det_interval = determinant_matrix(A)
    iter_count += 1

eps_start = eps
step = 0.0001
print("STEP = ", step)

count = 0

while 0 in det_interval:
    count += 1
    print("\ndet(A) = ", det_interval)
    eps = eps_start - step*count
    A = create_intval_matrix(eps)
    det_interval = determinant_matrix(A)
    iter_count += 1

print("iter_count", iter_count)
eps_min = round(eps + step, precision)
A = create_intval_matrix(eps_min)
det_interval = determinant_matrix(A)
print("\nMinimal eps = ", eps_min)

eps_max = chr(4113)
print(f"\ndiapason eps = [{eps_min}, +{eps_max}]")

print_table(A, headers=[])

print(f"\ndet(A) for minimal eps = {det_interval}")

new_A = intersection_row_or_columns(A)
if new_A:
    print("\nПересечение не пусто ")
    print("Уточненная интервальная матрица:")
    print_table(new_A, headers=[])
    print("Точечные особые матрицы A', принадлежащие интервальной матрице A:")
    arr_matrix = get_singular_matrices(new_A)
    for matrix in arr_matrix:
        print_table(matrix, headers=[])

else:
    print("\nПересечение пусто")
