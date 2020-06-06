import tenpy.utility.operators as op
import tenpy.vector as vec
import copy

class CreateMatrix:

    def __init__(self, info =[]):
        self.info = info
        if (len(self.info) != 1):
            for i in range(len(self.info)):
                if (len(self.info[i]) != len(self.info[i-1])):
                    print("Error: Not a Real Matrix. Make sure it is a perfect rectangle")
                    break
                else:
                    continue
        else:
            print("Error: Not a Real Matrix. Needs 2 dimensions")

########################################################################################################################
### GENERAL MATRIX UTILITY
########################################################################################################################

    def val(self):
        return copy.deepcopy(self.info)

    def dimensions(self):
        value = []
        value.append(len(copy.deepcopy(self.info)))
        value.append(len(self.info[0].copy()))
        return value

########################################################################################################################
### OPERATE MATRIX COLUMNS
########################################################################################################################

    def get_column(self, index):
        result = []
        matrix = copy.deepcopy(self.info)

        for i in range(len(matrix)):
            result.append(matrix[i][index])
        return result

    def delete_column(self, index):
        result = copy.deepcopy(self.info)
        for i in range(len(result)):
            result[i].pop(index)
        return CreateMatrix(result)

########################################################################################################################
### SPECIAL MATRICES
########################################################################################################################

    def get_zero_matrix(self, rows, cols):
        temp = []
        result = []
        for i in range(rows):
            for j in range(cols):
                temp.append(0)
            result.append(temp)
            temp = []
        return CreateMatrix(result)

    def get_null_matrix(self, rows, cols):
        temp = []
        result = []
        for j in range(cols):
            temp.append(None)
        for i in range(rows):
            result.append(temp)
        return CreateMatrix(result)

    def get_identity_matrix(self, size):
        index = 0
        temp = []
        result = []
        for i in range(size):
            for j in range(size):
                if (j == index):
                    temp.append(1)
                    continue
                temp.append(0)
            result.append(temp)
            temp = []
            index += 1
        return CreateMatrix(result)

########################################################################################################################
### GENERAL MATRIX EVALUATION
########################################################################################################################

    # Operates on vectors by element
    def element_eval(self, other=[], sign="+"):
        if len(self.info[0]) == len(other.info[0]):
            a = []
            result = []
            for i in range(len(self.info)):
                for j in range(len(self.info[i])):
                    a.append(op.get_operator_fn(sign)(self.info[i][j], other.info[i][j]))
                result.append(a)
                a = []
            return CreateMatrix(result)
        else:
            return "Matrix Not Operatable"

########################################################################################################################
### CONSTANT MULTIPLICATION
########################################################################################################################

    def constmul(self, const = 1):
        result = copy.deepcopy(self.info)
        for i in range(self.dimensions()[0]):
            for j in range(self.dimensions()[1]):
                result[i][j] *= const
        return CreateMatrix(result)

########################################################################################################################
### MATRIX-VECTOR MULTIPLICATION
########################################################################################################################

    def matvecmul(self, other):
        save_matrix = copy.deepcopy(self.info)
        other_mat = other.val()
        rows = self.dimensions()[0]
        cols = self.dimensions()[1]
        result = []
        component = 0
        if (len(self.info[0]) == len(other.val())):
            for i in range(rows):
                for j in range(cols):
                    component += save_matrix[i][j] * other_mat[j]
                result.append(component)
                component = 0
            return vec.CreateVector(result)
        else:
            return "Error: Cannot multiply matrix with vector. Number of Components in vector not equal to number of columns in matrix"

########################################################################################################################
### MATRIX MULTIPLICATION
########################################################################################################################

    # WORK IN PROGRESS
    def matmul(self, other):
        cols = other.dimensions()[1]
        rows = self.dimensions()[0]
        if self.dimensions()[1] == other.dimensions()[0]:
            matrix_temp = []
            matrix = []
            for i in range(rows):
                a = vec.CreateVector(self.info[i].copy())
                for j in range(cols):
                    b = vec.CreateVector(other.get_column(j))
                    c = a.dot_prod(b)
                    matrix_temp.append(c)
                matrix.append(matrix_temp)
                matrix_temp = []
            return CreateMatrix(matrix)
        else:
            return "Error: Cannot multiply matrices"

########################################################################################################################
### MATRIX DETERMINANT
########################################################################################################################

    def determ(self):
        matrix_save = copy.deepcopy(self.info)
        if (self.dimensions()[0] == self.dimensions()[1]):
            if (self.dimensions()[0] == 1):
                return "Error: Cannot Find Determinant. Not Enough Dimensions"
            elif (self.dimensions()[0] == 2):
                return self.info[0][0] * self.info[1][1] - self.info[0][1] * self.info[1][0]
            else:
                first_row = matrix_save[0].copy()

                matrix_copy = copy.deepcopy(matrix_save)
                matrix_copy.pop(0)

                matrix_first = CreateMatrix(matrix_copy).delete_column(0)
                determ = first_row[0]*matrix_first.determ()

                matrix_copy = copy.deepcopy(matrix_save)
                matrix_copy.pop(0)

                copy_matrix = CreateMatrix(matrix_copy)
                for i in range(1, copy_matrix.dimensions()[1]):
                    if (i % 2) != 0: sign = -1
                    else: sign = 1
                    matrix_copy = copy.deepcopy(matrix_save)
                    matrix_copy.pop(0)
                    a = CreateMatrix(matrix_copy).delete_column(i)
                    determ += sign * (first_row[i]*(a.determ()))
                return determ
        else:
            return "Error: Cannot Find Determinant. Need Square Matrix"

########################################################################################################################
### MATRIX COFACTORS
########################################################################################################################

    def cofactor(self):
        sign = -1
        temp = []
        result = []
        matrix_save = copy.deepcopy(self.info)

        a = CreateMatrix(matrix_save)

        for i in range(a.dimensions()[0]):
            matrix_save = copy.deepcopy(self.info)
            matrix_save.pop(i)
            a = CreateMatrix(matrix_save)

            for j in range(a.dimensions()[1]):
                sign *= -1
                temp.append(sign * a.delete_column(j).determ())
                matrix_save = copy.deepcopy(self.info)
                matrix_save.pop(i)
                a = CreateMatrix(matrix_save)
            result.append(temp)
            temp = []
        return CreateMatrix(result)

########################################################################################################################
### MATRIX INVERSION
########################################################################################################################

    def inverse(self):
        if (self.dimensions()[0] == self.dimensions()[1]):
            transpose = self.cofactor().transpose()
            determ = self.determ()
            if determ != 0:
                result = transpose.constmul(1/determ)
                return result
            else:
                print("Error: Cannot Find Inverse. Cannot invert a matrix with determinant O")
                return self.get_zero_matrix(self.dimensions()[0], self.dimensions()[1])
        else:
            return "Error: Cannot Find Inverse. Need square matrix."


########################################################################################################################
### MATRIX TRANSPOSITION
########################################################################################################################

    def transpose(self):
        result = []
        for i in range(len(self.info[0])):
            result.append(self.get_column(i))
        return CreateMatrix(result)