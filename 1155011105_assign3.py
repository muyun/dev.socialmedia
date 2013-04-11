# -*- coding ntf-8 -*-
# ***************************************************************************************
# This is the homework3 for social media in cuhk
# which is about a simple recommender system using the user-based collaborative filtering
# Todo: using class is better
# ***************************************************************************************
from __future__ import division
import re, numpy
from sets import Set

def getData():
    # i is used to flag the user's index, which connects user name
    #i = 1

    f = open("books_ratings.txt", 'r')
    for line in f:
        name = re.match(r"^[a-zA-z]", line);
        if ( name is not None):
            name = line.strip('\n')
            users.append(name)

        else:
            #line = line.strip()
            newList = []
            # convert the rating scale accordint to defined rule    
            for k in line.split():
                for key in conv.keys(): 
                    if int(k) == int(key):
                        new = conv[key]
                        newList.append(new)
                        
            #store the new rating scale in list data            
            ratings.append(newList)        
            #rating = [int(k) for k in line.split()]
            #ratings.append(rating)

    f.close()        
    #    print(users)
    print "The ratings Matrix:"
    print(ratings)

    f = open('books_list.txt', 'r')
    for line in f:
        #line = line.strip()
        fields = line.strip().split(',')
        author = fields[0]
        title = fields[1]
        
        title = title + ' by ' + author
        books.append(title)

    f.close()
    
    return ratings
    # print books

# get the common elements in two list    
def getUnion(list1, list2):
    
    return Set(list1) | Set(list2)

# get the difference in two list
def getDifference(list1, list2):
    
    return Set(list1) - Set(list2)

# get the items' indices that user hasn't read
def getNoRelatedItems(ratings, u):
    #Todo: so urgly solution ...
    
    i=0
    #record the index whose value is -1, means that user hasn't read it
    nolist = []

    for k in ratings[u]:
       
        #ignore -1, record the order
        if k == -1:
            nolist.append(i)
        #else:
            #list.append(k)
        i += 1
    #print nolist

    return nolist

def calPearsonr(list1,list2):

    from scipy.stats import pearsonr
    p = pearsonr(list1,list2)[0]
    if str(p) == "nan":
        p = 0
    #print "%f" % p

    return p
    

def similarity(ratings,u1, u2):
    print "Calculate the similarity of given two users based Pearson correlation coefficient:"
    # the two list record the index whose value is -1, means that user hasn't read it
    nolist1 = []
    nolist2 = []
    nolist1 = getNoRelatedItems(ratings, u1)
    nolist2 = getNoRelatedItems(ratings, u2)

    # get common list
    nolist = getUnion(nolist1, nolist2)
    #print nolist
    
    # get the u1's list, which only include the common items between u1 and u2
    list1 = [item for index, item in enumerate(ratings[u1]) if index not in nolist]
    #print list1
    list2 = [item for index, item in enumerate(ratings[u2]) if index not in nolist]
    #print list2

    # calculate pearson correlation
    # meet the function parameters, so bad ...
    pearsonr = calPearsonr(list1, list2)
    print "%f" % pearsonr
    return  pearsonr

def getNeighbors(ratings, u, N, b):
    # neighbors's definition:
    #1. They have rated items that X has rated
    #2. They have rated Y
    #so, we should get a sorted list of N users based on their similarity(distance) to u
    #also, the neighbor's (Assume u3 here) items include u's items and b (b is Y)

    #similarity
    similarities = []
    # get -1 index for u
    nolist0 = []
    nolist0 = getNoRelatedItems(ratings, u)

    print "Find the neighbors of a given user:"
    # len(ratings) is the number of users, because ratings is an array and begin from 0
    # and we use the index of array ratings as user's index
    user = 0
    while (user < len(ratings)):
        if user != u:
            nolist1 = []
            nolist1 = getNoRelatedItems(ratings, user)
            # because this is no related items, so it is contary
            # test whether nolist1 is subset of nolist
            # which equals that current user is superset of u
            if Set(nolist1).issubset(Set(nolist0)):
                # get common list
                nolist = getUnion(nolist1, nolist0)
                #print "nolist"
                #print nolist
                # get the current user's list, which only include the common items between current user and required u
                list1 = [item for index, item in enumerate(ratings[user]) if index not in nolist]
                list2 = [item for index, item in enumerate(ratings[u]) if index not in nolist]

                # calculate pearson correlation
                # meet the function parameters, so bad ...
                pearsonr = calPearsonr(list1, list2)

                similarities.append((pearsonr, user))
                
        user += 1        
        
    s = sorted(similarities,key = lambda similarities: similarities[0],reverse=True)

    similarities = s[:N]

    userList = []
    for similarity in similarities:
        userList.append(similarity[1])
        #print "userid:%d" % similarity[1]
    print userList          
            
    return userList  

def predict(ratings, u, b, neighbors):
    #Since the neighbours of u have been given
    #which assumes we have had similar users

    # filter neighbors because some of them might not have rated the particular book b
    # which means related item's value is not -1

    # get the -1's index list of u
    nolist0 = []
    nolist0 = getNoRelatedItems(ratings, u)
    
    # store the pearson and user for b
    newPearson = []
    # store the indices in neighbors but not in u
    allList = []
        
    print "Predict the rating for a given book and neighbors:"            
    
    for neighbor in neighbors:
        if ratings[neighbor][b] != -1:
            #print "neighbor: %d" % neighbor
            # also, the neighbor should meet the neighbor's definition
            # which means that the neighbor user should be superset of u
            # that's to say, -1 items should be subset of u's
            nolist1 = []
            nolist1 = getNoRelatedItems(ratings, neighbor)
            if Set(nolist1).issubset(Set(nolist0)):
                # current indices in current neighbors but not in u
                list = []
                # get common list
                nolist = getDifference(nolist0, nolist1)
                #get the indices which are not included by u
                # this list stores the indices in current neighbor and not in u
                # in this list, we only care index b,so
                list = [item for index, item in enumerate(ratings[neighbor]) if index in nolist and index == b]
                allList = allList + list
             
                if len(list) != 0:
                    #only when current neighbor rated book b and required user u didn't ( in nolist)
                    # then we calculate the pearson between current neighbor and u                
                    # the same code
                    # get common list
                    nolist = getUnion(nolist1, nolist0)
                    # get the current user's list, which only include the common items between current user and required u
                    list1 = [item for index, item in enumerate(ratings[neighbor]) if index not in nolist]
                    list2 = [item for index, item in enumerate(ratings[u]) if index not in nolist]

                    # calculate pearson correlation
                    pearson = calPearsonr(list1, list2)
                    newPearson.append((pearson,neighbor))
                    #print "pearson: %f" % pearson
                    
    #only when book b is in the neighbors but not in u
    if len(allList) != 0:                
        #print newPearson
        # then calculate pearson for each neighbor        
        # similar to k-nearest
        value = 0

        #have to add a new list for sum
        sumList = []
        for fields in newPearson:
            pearson = fields[0]
            sumList.append(pearson)

        #get the sum
        pearsonSum = sum(sumList)
        #print "pearsonSum %f" % pearsonSum
        
        for fields in newPearson:
            pearson = fields[0]
            user = fields[1]
            pearsonValue = pearson / pearsonSum
           
            value += ratings[user][b] * pearsonValue
            #print "value1: %f" % value
    
        print "%f" % value
        return value
        
    # or return u's rating
    else:
        print "%f" % ratings[u][b]
        return ratings[u][b]
          
if  __name__ == "__main__":
    #Global variable
    # list ratings is used to store the ratings in the user-item array
    ratings = []
    # list users is used to store the related user name
    users = []
    # list books is used to store the related books
    books = []

    # define the rule to convert the rating scale according to the table
    conv = {}
    conv['0'] = -1
    conv['-5'] = 0
    conv['-3'] = 0.25
    conv['1'] = 0.50
    conv['3'] = 0.75
    conv['5'] = 1

    #get the matrix 
    ratings = getData()
    
    # test the functions
    #calculate the correlation
    similarity(ratings,2,4)
    
    #find the neighbors of some user
    N = []
    item = 5
    getNeighbors(ratings, 3, 5, item)
    
    # predict the rating that some user would give to a book
    # list neighbors is a list of indices of the nighbors of user u
    neighbors = [4,5,6,7,8,9]
    predict(ratings, 3, 4, neighbors)

    # evaluation
    
