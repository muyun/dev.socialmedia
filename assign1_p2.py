# -*- coding: utf-8 -*-
#  Name:     sum3n5Multiples
#  Function: print the sum of all the multiples of 3 or 5
#             that are smaller that number (excluding the number)

#import sys


def number():
    n = input("Please input the integer:")
    # try:
    return long(n)
    '''except:
        print("The input is not an integer")
        sys.exit(1)
    '''


def mysum(n):
    #count
    i, j = 1, 1
    #init value
    value3 = 3
    value5 = 5
    #init sum
    sum3, sum5 = long(0), long(0)

    while True:
        if value3 < n:
            sum3 += value3
            i += 1
            value3 = 3 * i
            #print("i: %o" % i)
            
        else:
            break

    while True:
        if value5 < n:
            #remove the common multiples of 3 and 5 (like 15)
            if value5 % 3 != 0:
                sum5 += value5
            j += 1
            value5 = 5 * j
            #print("j: %o" % j)
        else:
            break

        #print("sum3: %o" % sum3)
        #print("sum5: %o" % sum5)
    sum = sum3 + sum5
    print(sum)

def main():
    n = number()
    #print(n)

    mysum(n)
# magic name __name__
if __name__ == "__main__":
# when we run this module by itself or import it, it is 'True',
# wehn the module is imported,the condition evaluates to 'False'
    main()
