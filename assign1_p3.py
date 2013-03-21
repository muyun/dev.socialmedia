# -*- coding ntf-8 -*-
''' Name:     getGrtProduct
    Function: get the greatest product of seven consecutive digits
              from the file
'''
'''
import os

def removeSpace(fileName):
    f = open(fileName)
    nf = open(/tmp/file1,"w")
    for line in f.readlines():
        line.strip()
        nf.write(line)
        
    nf.close()
    f.close()
'''
          
def exists(fileName):
    try:
        f = open(fileName)
        f.close()
        #remove the trailing space on each line
                    
        return True
    except IOError:
        return False


def readFile():
    # input the file name
    #fileName = raw_input("Enter a file name: ")
    fileName = src_file
    if exists(fileName):
        fo = open(fileName, "r")
        print "File name: ", fo.name

        # read the file
        str = fo.read()
        #print "String is: ", str
        fo.close()
        return str
    else:
        print 'There is no file named', fileName


def convList( string ):
    int_list = []
    i = 0
    while i < len(string):
        #convert in a list to ints    
        int_list.append( int(string[i:(i+1)]) )
       # print(string[i:(i+1)])
        i += 1
    
    return int_list

def getProduct( string, n ):
    #position
    p1, p2 = 0, int(n)
    # init the greatest value
    pt = long(0)
    #print(str(string))
    #fetch each str based on the position
    while p2 < len(str(string)):
        eachStr = string[p1:p2]
        #print(eachStr)
        p2 += 1
        p1 += 1

        #get the product in each int list convList(eachStr)
        eachPt = long(1)
        #eachList = convList(eachStr)
        for integer in convList(eachStr):
            #print(integer)
            eachPt *= integer
        # print "Each product:", eachPt    

        #get the greatest product
        if pt < eachPt:
            pt = eachPt
            
   #print "The greatest product is:", pt
    return pt


src_file = "/home/zhaowenlong/workspace/class/social_media/1155011105_assign1/iems5723_assign1_01.dat"
def main():
    #readFile()

    print(getProduct(readFile(), 7))
#    print("The greatest product based on iems5723_assign1_01.dat is:2571912")
    
if __name__ == "__main__":
    main()
