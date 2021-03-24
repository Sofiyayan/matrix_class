import random


class MatrixError(Exception):
    pass


class Matrix:
    def __init__(self, lists):
        if not isinstance(lists, (list, tuple)):
            raise MatrixError(
                "ERROR: Expected type list or tuple found {}".format(type(lists))
            )

        for rows in lists:
            if isinstance(rows, (list, tuple)):
                if not all(isinstance(num, (int, float)) for num in rows):
                    raise MatrixError(
                        "ERROR: Expected type int or float for matrix components"
                    )
            else:
                raise MatrixError(
                    "ERROR: Expected type list or tuple found {}".format(type(rows))
                )

        for rows in lists:
            if len(rows) != len(lists[0]):
                raise MatrixError("ERROR: Lengths of rows in matrix are not equal")

        self.lists = lists

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise MatrixError(
                "ERROR: Expected type Matrix for addition found {}".format(type(other))
            )

        if not self.same_dimension_with(other):
            raise MatrixError("ERROR: matrices should have same dimension for addition")
        return [
            [self.lists[i][j] + other.lists[i][j] for j in range(len(self.lists[i]))]
            for i in range(len(self.lists))
        ]

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise MatrixError(
                "ERROR: Expected type Matrix for subtraction found {}".format(
                    type(other)
                )
            )

        if not self.same_dimension_with(other):
            raise MatrixError(
                "ERROR: matrices should have same dimension for subtraction"
            )
        return [
            [self.lists[i][j] - other.lists[i][j] for j in range(len(self.lists[i]))]
            for i in range(len(self.lists))
        ]

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            raise MatrixError(
                "ERROR: Expected type Matrix for multiplication found {}".format(
                    type(other)
                )
            )
        if len(self.lists[0]) != len(other.lists):
            raise MatrixError(
                "ERROR: matrices' dimension requirement for multiplication is not satisfied"
            )

        return [
            [
                sum(a * b for a, b in zip(self_row, other_column))
                for other_column in zip(*other.lists)
            ]
            for self_row in self.lists
        ]

    def __str__(self):
        matrix_str = [" ".join(map(str, row)) for row in self.lists]
        matrix_str[0] = " ".join(["⌈", matrix_str[0], "⌉"])
        matrix_str[-1] = " ".join(["⌊", matrix_str[-1], "⌋"])
        if len(matrix_str) > 2:
            for row_num in range(1, len(matrix_str) - 1):
                matrix_str[row_num] = " ".join(["|", matrix_str[row_num], "|"])
        return "\n".join(matrix_str)

    def __minor(self, i, j):
        return [
            row[:j] + row[j + 1:] for row in (self.lists[:i] + self.lists[i + 1:])
        ]

    def determinant(self):
        if not self.is_square():
            raise MatrixError("ERROR: Matrix should be square to have determinant")
        if len(self.lists) == 2:
            return (
                self.lists[0][0] * self.lists[1][1]
                - self.lists[0][1] * self.lists[1][0]
            )

        det = 0
        for element in range(len(self.lists)):
            matrix_det = Matrix(self.__minor(0, element))
            det += ((-1) ** element) * self.lists[0][element] * matrix_det.determinant()
        return det

    def inverse(self):
        if not self.is_square():
            raise MatrixError("ERROR: Matrix should be square to have inverse")
        det = self.determinant()
        if det == 0:
            raise MatrixError(
                "ERROR: Matrix does not have an inverse, determinant of matrix is 0"
            )
        if len(self.lists) == 2:
            return [
                [self.lists[1][1] / det, -1 * self.lists[0][1] / det],
                [-1 * self.lists[1][0] / det, self.lists[0][0] / det],
            ]

        cofactors = []

        for row in range(len(self.lists)):
            cofactor_row = []
            for column in range(len(self.lists)):
                minor_matrix = Matrix(self.__minor(row, column))
                cofactor_row.append(
                    ((-1) ** (row + column)) * minor_matrix.determinant(),
                )
            cofactors.append(cofactor_row)
        cof = Matrix(cofactors)
        cof = list(map(list, zip(*cof.lists)))
        for row in range(len(cof)):
            for column in range(len(cof)):
                cof[row][column] = round(cof[row][column] / det, 2)
        return cof

    def same_dimension_with(self, other):
        if not isinstance(other, Matrix):
            raise MatrixError(
                "ERROR: Expected type Matrix for comparison found {}".format(
                    type(other)
                )
            )
        if len(self.lists) == len(other.lists) and len(self.lists[0]) == len(
            other.lists[0]
        ):
            return True
        return False

    def is_square(self):
        if len(self.lists) == len(self.lists[0]):
            return True
        return False

    @staticmethod
    def random_matrix(rows, columns):
        if not isinstance(rows, int) or not isinstance(columns, int):
            raise MatrixError("ERROR: Matrix dimensions should be integers")
        return Matrix([
            [round(random.random() * 100, 3) for _ in range(columns)]
            for _ in range(rows)
        ])


if __name__ == "__main__":
    pass
