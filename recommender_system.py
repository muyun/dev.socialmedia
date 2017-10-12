# -*- coding ntf-8 -*-
# ***************************************************************************************
# which is about a simple recommender system using the user-based collaborative filtering
# Todo: using class is better
# ***************************************************************************************
#from __future__ import division
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
        
    return nolist

def calPearsonr(list1,list2):

    from scipy.stats import pearsonr
    p = pearsonr(list1,list2)[0]
   
    if str(p) == "nan":
        p = 0.0
    #print "%f" % p

    return p
    

def similarity(ratings,u1, u2):
    print "Calculate the similarity of given users [%d,%d] based Pearson correlation coefficient:" % (u1,u2)
    # the two list record the index whose value is -1, means that user hasn't read it
    nolist1 = []
    nolist2 = []
    nolist1 = getNoRelatedItems(ratings, u1)
    nolist2 = getNoRelatedItems(ratings, u2)

    # get common list
    nolist = getUnion(nolist1, nolist2)
    #if there is common list
    if len(nolist) != 0:
        # get the u1's list, which only include the common items between u1 and u2
        list1 = [item for index, item in enumerate(ratings[u1]) if index not in nolist]
        list2 = [item for index, item in enumerate(ratings[u2]) if index not in nolist]

        # calculate pearson correlation
        # meet the function parameters, so bad ...
        pearson = calPearsonr(list1, list2)
        print "The Pearson correlation: %f" % pearson
        return  pearson
    else:
        pearson = "unknown"
        
        print "[%d,%d] arenot neighbors with each other" % (u1,u2)

def getNeighbors(ratings, u, N, b):
    # neighbors's definition:
    #1. They have rated items that X has rated
    #2. They have rated Y
    #so, we should get a sorted list of N users based on their similarity(distance) to u
    #also, the neighbor's (Assume u3 here) items include b (b is Y here) which X doesn't rate

    #similarities stores the similarity information between user and u
    similarities = []
    # get -1 index for u
    #nolist0 = []
    #nolist0 = getNoRelatedItems(ratings, u)

    print "Find the neighbors of a given user:"
    # len(ratings) is the number of users, because ratings is an array and begin from 0
    # and we use the index of array ratings as user's index
    user = 0
    while user < len(ratings):
        if user != u:
            #nolist1 = []
            #nolist1 = getNoRelatedItems(ratings, user)
            #user rated book b while u rated book b 
            if ratings[u][b] == -1 and ratings[user][b] != -1:
                #calculate pearson correlation between current user and u
                pearson = similarity(ratings, user, u)
 
                similarities.append((pearson, user))
                
        user += 1        
        
    s = sorted(similarities,key = lambda similarities: similarities[0],reverse=True)
    similarities = s[:N]
    
    userList = []
    for fields in similarities:
        userList.append(fields[1])
        #print "userid:%d" % fields[1]
    print "The neighbors of user %d are:" % u  
    print userList
    
    return userList  
 
def predict(ratings, u, b, neighbors):
    #Since the neighbours of u have been given
    #which assumes we have had similar users

    # filter neighbors because some of them might not have rated the particular book b
    # which means related item's value is not -1

    # store the pearson and user for b
    newPearson = []
        
    print "Predict the rating for a given book and neighbors:"            
    
    for neighbor in neighbors:
        # only when book b is in the neighbors but not in u
        if ratings[neighbor][b] != -1 and ratings[u][b] == -1:
            # also, the neighbor should meet the neighbor's definition
            # which means that the neighbor user should include common items with u
            # that's to say, The union of their not-readed items(-1) shouldnot be null

            # calculate pearson correlation
            pearson = similarity(ratings,neighbor, u)
            # if they are not neighbor
            if pearson == "unknown":
                continue
            else:
                newPearson.append([neighbor, pearson])
                            
    # then calculate sum of each neighbor's pearson        
    # similar to k-nearest
    
    #predicted rating
    value = 0.0
    
    #sum of pearson
    pearsonSum = 0.0

    userList = []
    sumList = []

    for fields in newPearson:
        # prepare for getting the number of neighbor
        # here we can't use len(neighbor) as the number of neighbor,
        # because some user might not be u's neighbor
        userList.append(fields[0])
        sumList.append(fields[1])

    #get the sum
    pearsonSum = sum(sumList)
    #print "pearsonSum %f" % pearsonSum
        
    for fields in newPearson:
        user = fields[0]
        pearson = fields[1]
        if pearsonSum == 0.0:
            #calculate the rated average of neighbors
            pearsonValue = pearson / float(len(userList))
        else:
            pearsonValue = pearson / pearsonSum
           
        value += ratings[user][b] * pearsonValue

    print "The predicted value is: %f" % value
    
    return value

          
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
    
    #****************************************************************
    # test the functions ...
    #calculate the correlation
    similarity(ratings,2,4)
    
    #find the neighbors of some user
    N = []
    item = 0
    getNeighbors(ratings, 0, 5, 2)
    
    # predict the rating that some user would give to a book
    # list neighbors is a list of indices of the nighbors of user u
    neighbors = [3,5,1]
    predict(ratings, 0, 2, neighbors)
    
    #****************************************************************
    # evaluation permormance
    print "*******************************************"
    print "Perform evaluation:"
    # mean rating
    # make use of other than user himslef 
    user = 0
    # record each i
    i = 0
    # rating for first two book
    b0 = 0.0
    b1 = 0.0
    
    meanRating= []
    # store the mean rating
    # for each user
    while user < len(ratings):
        # at each line
        while i < len(ratings):
            #apart from user himself
            if user != i:
                #book 0
                b0 += ratings[i][0]
                b1 += ratings[i][1]
                
            i += 1
        meanb0 = b0 / (len(ratings) -1)
        meanb1 = b1 / (len(ratings) -1)
        meanRating.append([meanb0,meanb1,user])
        
        user += 1
    print "The mean Rating of the books is:"
    print meanRating
    #predicted rating using predict function 
    # get the new ratings matrix newratings
    # remove the first two items list on martix ratings according to the instruction
    i = 0
    line = []
    # store the new ratings
    newratings = []
    while i< len(ratings):
        line = ratings[i]
        # remove the first two column
        del line[0:2]
        newratings.append(line)
        i += 1    
    
    
    #userlist store the list of neighbor when given a user
    userList05  = []
    userList010 = []
    userList15  = []
    userList110 = []

    # store predicted rating based on the above neighbor
    predictedRating05 = []
    predictedRating010 = []
    predictedRating15 = []
    predictedRating110 = []

    i = 0
    while i<len(newratings):
        #for book 0, size of neighbor is 5
        userList05 = getNeighbors(newratings, i, 5, 0)
        # size of neighbor is 10
        userList010 = getNeighbors(newratings, i,10, 0)
        
        #for book 1, size of neighbor is 5
        userList15 = getNeighbors(newratings, i, 5, 1)
        # size of neighbor is 10
        userList110 = getNeighbors(newratings, i, 10,1)
        
        # predict the rating for book 0 based on the above neighbors is 5
        if len(userList05) != 0:
            value = predict(newratings, i, 0, userList05)

            predictedRating05.append([value,i])
        #else:
            #no neighbor
            #predictedRating05.append(-1)

        # book 0 based on the size of neighbors is 10
        if len(userList010) != 0:
            value = predict(newratings, i, 0, userList010)
            predictedRating010.append([value,i])
        #else:
            #predictedRating010.append(-1)

        # predict the rating for book 1 based on the above neighbors is 5
        if len(userList15) != 0:
            value = predict(newratings, i, 0, userList15)
            predictedRating15.append([value,i])
        #else:
            #no neighbor
            #predictedRating15.append(-1)

        # book 1 based on the size of neighbors is 10
        if len(userList110) != 0:
            value = predict(newratings, i, 0, userList110)
            predictedRating110.append([value,i])
        #else:
            #predictedRating110.append(-1)

        i += 1

    # compute the RMSE(root mean squared error)for the three types of predictions
     #for mean method
    meanDist0 = meanDist1 = 0.0
    # [b0,b1,user]
    for fields in meanRating:
        meanb0 = fields[0]
        meanb1 = fields[1]
        user = fields[2]

        meanDist0 += (ratings[user][0] - meanb0) ** 2
        meanDist1 += (ratings[user][1] - meanb1) ** 2
 
     #for predictd function   
    # for book 0 based on the size of neighbors is 5
    distance05 = distance010= distance15 = distance110= 0.0
    #book 0
    for fields in predictedRating05:
        user = fields[1]
        value = fields[0]

        distance05 += (ratings[user][0] - value) ** 2

    # 
    for fields in predictedRating010:
        user = fields[1]
        value = fields[0]
        distance010 += (ratings[user][0] - value) ** 2

   # for book 1
    for fields in predictedRating15:
        user = fields[1]
        value = fields[0]
        distance15 += (ratings[user][1] - value) ** 2


    for fields in predictedRating110:
        user = fields[1]
        value = fields[0]
        distance110 += (ratings[user][1] - value) ** 2

    # get the value
    import math
    # mean method
    rmseValue0 = math.sqrt(meanDist0 / len(ratings))
    rmseValue1 = math.sqrt(meanDist1 / len(ratings))
    
    #predicted function
    rmseValue05 = math.sqrt(distance05 / len(ratings))
    rmseValue010 = math.sqrt(distance010 / len(ratings))
    
    rmseValue15 = math.sqrt(distance15 / len(ratings))
    rmseValue110 = math.sqrt(distance110 / len(ratings))
    
    print "RMSE rating of first book with mean rating: %f" % rmseValue0
    print "RMSE rating of second book with mean rating: %f" % rmseValue1
    print "RMSE rating of first book with the size of neighborhood is 5: %f" % rmseValue05
    print "RMSE rating of first book with the size of neighborhood is 10: %f" % rmseValue010
    print "RMSE rating of second book with the size of neighborhood is 5: %f" % rmseValue15
    print "RMSE rating of second book with the size of neighborhood is 10: %f" % rmseValue110

    
#The results:
#RMSE for the three types of predictions for each book
'''
RMSE rating of first book with mean rating: 0.794805
RMSE rating of second book with mean rating: 0.497917
RMSE rating of first book with the size of neighborhood is 5: 1.457574
RMSE rating of first book with the size of neighborhood is 10: 3.990158
RMSE rating of second book with the size of neighborhood is 5: 1.289845
RMSE rating of second book with the size of neighborhood is 10: 3.829169
>>> 
'''
