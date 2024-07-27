from copy import deepcopy

myMatrix = [
    [4, 2, 8, 8],
    [1, 3, 1, 2],
    [2, 4, 1, 6],
    [1, 5, 2, 8]
]

def GetDeterminant(matrix):

    def GetSubmatrix(pivot, inputMatrix):
        subMat = deepcopy(inputMatrix)
        for i in range(0, pivot[0]):
            del subMat[i][pivot[1]]

        for i in range(pivot[0] + 1, len(subMat)):
            del subMat[i][pivot[1]]

        del subMat[pivot[0]]

        return subMat
    
    if len(matrix) == 1:
        return matrix[0][0]
    
    value = 0
    for i in range(0, len(matrix[0])):
        value += pow(-1, i) * matrix[0][i] * GetDeterminant(GetSubmatrix([0, i], matrix))
    return value

print(GetDeterminant(myMatrix))