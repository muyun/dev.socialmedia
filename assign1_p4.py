# -*- coding utf-8 -*-
''' Name:     get_plot.py
    Function: present the bar chart based on the defined rules
'''
import nltk
nltk.data.path.append('/home/zhaowenlong/workspace/lib/nltk_data')

def get_freq_dist(src_file):
    #load the txt
    text = nltk.data.load(src_file,format='raw')
    #tokenize the txt
    tokens = nltk.word_tokenize(text)
    #ignore the words with 2 or less characters
    new_tokens = []
    for value in tokens:
        if len(value) > 2:
            new_tokens.append(value)

    #get the frequency distribution
    freq_dist = nltk.FreqDist(new_tokens)
    #get the sorted words in decreasing order of frequency
    vocabulary = freq_dist.keys()
    
    #get the num sorted in decreasing order of frequency
    num = freq_dist.values()
    
    return {'vocabulary':vocabulary[:20],'num':num[:20]}

    
def present_plot(dict):
    import matplotlib.pyplot as plt
    #a bar chart
    print(dict['vocabulary'])
    print(dict['num'])

    import numpy as np
    N = len(dict['vocabulary'])
    #x locations for the groups
    ind = np.arange(N)
    # the width of the bars
    width = 0.35
    p = plt.bar(ind,dict['num'], width,color='r')
    plt.ylabel('Number')
    plt.title('Number by vocabulary')
    plt.xticks(ind+width/2.,(dict['vocabulary']))
    plt.yticks(np.arange(0,5000,300))

    plt.show()

def main():
    src_file = "corpora/custombook/The_Memoirs_of_Sherlock_Holmes.txt"
    #get_freq_dist(src_file)
    present_plot(get_freq_dist(src_file))
    
if __name__ == "__main__":
    main()
