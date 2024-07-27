from __future__ import annotations 
from math import sqrt

class Vector:
    def __init__(self, array):
        self.array = array
        self.vectorDimentions = len(self.array)

    def Scale(self, scaler: float):   
        newArray = []

        for i in range(self.vectorDimentions):
            newArray.append(scaler * self.array[i])

        return Vector(newArray)
        
    def Sum(self, other : Vector):
        if self.vectorDimentions == other.vectorDimentions:
            
            newArray = []

            for i in range(self.vectorDimentions):
                newArray.append(self.array[i] + other.array[i])

            return Vector(newArray)
        
    def Subtract(self, other : Vector):
        return self.Sum(other.Scale(-1))
    
    def Dot(self, other):
        if self.vectorDimentions == other.vectorDimentions:
            value = 0

            for i in range(self.vectorDimentions):
                value += self.array[i] * other.array[i]

            return value
    
    def FindLength(self):
        return sqrt(self.Dot(self))
    
    def GetCrossProduct(self, other):
        if self.vectorDimentions == other.vectorDimentions and self.vectorDimentions == 3:
            pass
            
        

v1 = Vector([2, 4, 2])
v2 = Vector([1, 2, 3])

v3 = v1.FindLength()

print(v3)