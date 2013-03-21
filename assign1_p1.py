# -*- coding: utf-8 -*-
''' Name:     sumOfSqrt

    Function: take two positive integers as parameters,
            print the sum of the square roots to 4 decimal places
'''
import math
#import sys

def mymath(num):
    return math.sqrt(num)
    
def mysumofsqrt(num1,num2):
    sumofsqrt = mymath(num1)+mymath(num2)
    return sumofsqrt

#  TEST
num1 = int(input("Enter an positive integer: "))
num2 = int(input("Enter another positive integer: "))

print("%.4f" % mysumofsqrt(num1,num2))
