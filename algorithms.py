import numpy as np
from numpy.linalg import matrix_power
import sympy
from sympy import simplify, Matrix
from fractions import Fraction


def create_matrix(rows, columns, input_string):
    matrix = []
    for row in range(rows):
        matrix.append([])
    if rows == 0 or columns == 0:
        matrix.append("Матрицы всегда размером минимум 1х1")
        return matrix
    if '.' in input_string or '/' in input_string:
        string = list(map(Fraction, input_string.split()))
        row = 0
        column = 0
        for j in range(len(string)):
            matrix[row].append(Fraction(string[j]))
            column += 1
            if column % columns == 0:
                column = 0
                row += 1
    else:
        string = list(map(int, input_string.split()))
        row = 0
        column = 0
        for j in range(len(string)):
            matrix[row].append(int(string[j]))
            column += 1
            if column % columns == 0:
                column = 0
                row += 1
    return matrix


def matrix_to_array(matrix):
    matrix = np.array(matrix).astype(np.float64)
    matrix = matrix.tolist()
    return matrix


# def matrix_output(matrix):
#     if type(matrix) != list:
#         matrix = matrix.tolist()
#     matrix = DataFrame(matrix)
#     return str(matrix)

def matrix_output(matrix):
    matrix2 = intify(np.array(matrix))
    s = [[str(e) for e in row] for row in matrix2]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '    '.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)


def jordan_normal_form(matrix):
    matrix = Matrix(matrix)
    P, J = matrix.jordan_form()
    P = simplify(P)
    ans = [P, J]
    return ans


def determinant(matrix):
    matrix2 = matrix[:]
    return sympy.Matrix(matrix2).det()


def const_multiplication(matrix, num):
    return matrix * num


def matrix_multiplication(matrix_1, matrix_2):
    return np.matmul(matrix_1, matrix_2)


def matrix_sum(matrix_1, matrix_2, operation):
    if operation == "+":
        matrix_1 = np.array(matrix_1)
        matrix_2 = np.array(matrix_2)
        return (matrix_1 + matrix_2).tolist()

    if operation == "-":
        matrix_1 = np.array(matrix_1)
        matrix_2 = np.array(matrix_2)
        return (matrix_1 - matrix_2).tolist()


def inverse_matrix(matrix):
    matrix = Matrix(matrix)
    result = matrix.inv().tolist()
    return result


def intify(matrix):
    matrix2 = []
    all_ints = 1
    for i in range(len(matrix)):
        matrix2.append([])
    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            if matrix[row][column] % 1 != 0:
                all_ints = 0
                if matrix[row][column] % 10 != 0:
                    matrix[row][column] = "%.2f" % matrix[row][column]
                else:
                    matrix[row][column] = "%.1f" % matrix[row][column]
    if all_ints:
        for k in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix2[k].append(int(matrix[k][j]))
        return matrix2
    return matrix


def intify_arr(arr):
    arr_copy = arr[:]
    arr2 = []
    all_ints = 1
    for i in range(len(arr_copy)):
        if arr_copy[i] % 1 != 0:
            all_ints = 0
            arr_copy[i] = round(arr_copy[i], 2)
    if all_ints:
        for k in range(len(arr)):
            arr2.append(int(arr[k]))
        return arr2
    return arr_copy


def white_power(matrix, n):
    matrix = np.array(matrix)
    result = matrix_power(matrix, n)
    return result


def swap_rows(matrix, row1, row2):
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]


def divide_row(matrix, row, divider):
    matrix[row] = [a / divider for a in matrix[row]]


def combine_rows(matrix, row, source_row, weight):
    matrix[row] = [(a + k * weight) for a, k in zip(matrix[row], matrix[source_row])]


def multiply_array(arr):
    print(arr)
    result = 1
    for elem in arr:
        result *= float(elem)
    return result


def output_array(arr):
    output = "["
    for elem in arr:
        output += f" {str(elem)},"
    output += " ]"
    return output
