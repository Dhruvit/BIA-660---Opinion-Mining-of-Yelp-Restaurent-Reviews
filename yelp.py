"""
Title: Opinion Mining of Restaurant Reviews using NLP

This project is submitted by Group 4

Dhruvitkumar Patel,
Ishita Arora,
Karthik Balasubramanyam ,
Keven Sebastian,
Sarayu Bangalore Rajaram

"""

# Write all function below imports
import re
import math
from nltk import tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import time

start_time = time.time()

#function that load all the  lexicons of positive,negative and negation  words to a set, returns the set
def loadLexicon(fname):
    newLex=set()
    lex_conn=open(fname)
    #add every word in the file to the set
    for line in lex_conn:
        newLex.add(line.strip())
    lex_conn.close()

    return newLex
    
#function to split the sentence based on connecting words, returns individual words
def split_connecting(sentence):
    return re.split('but | and | although | however | because', sentence)

#function to convert list of features to dictionary,returns a dictionary
def listToDictionary(filename):
    d = {}
    connection = open(filename)
    for eachLine in connection:
        line = eachLine.strip().split("-")

        value = line[0].strip()
        key = line[1].strip().lower()
        d[key] = value

    connection.close()
    return d
  
#Main Algorithm

#Loading all the lexicons from the files and convert list of features to dictionary
negation_words = loadLexicon('negation-words.txt') 
features = listToDictionary('features-synonyms.txt')
positive_lex = loadLexicon('positive-words.txt')
negative_lex = loadLexicon('negative-words.txt')

mainDictionary_reviews = dict()
#priority given to each feature and stored in dictionary
priority = {'FOOD':5,'DRINKS':4,'VALUE':4,'RESTAURANT':3,'SERVICE':2,'AURA':1,'PARKING':1}

star_one = 0
star_two = 0
star_three = 0
star_four = 0
star_five = 0

counter_one = 0
counter_two = 0
counter_three = 0
counter_four = 0
counter_five = 0

fp = open("input.txt","r")
# Reading 'input.txt' line by line
for line in fp:
    #This is used to replace the Apostrophes present in the sentence
    line = line.lower().strip().replace("\x92","\'")  
    
    #Split reviews based on the delimiter
    reviews = line.split("@#$@#$")

    #To build a set of english stopwords
    stopLex = set(stopwords.words('english')) 
    review_counter = 0

    for review in reviews:
        #To get the rating from each review
        temp_review =  review.split("@@@@@") 
        review_counter = review_counter + 1 
        try:
            star = math.ceil( float(temp_review[0]) )
            #Taking one review as input
            sentences = tokenize.sent_tokenize(temp_review[1]) 
        except ValueError as err:
            print(temp_review[0])

        #Dictionary to store the value of features for each review
        mainDictionary_features = dict()
        #To split the review into individual sentences
        for sentence in sentences:

            #To Split based on punctuations
            sentence = sentence.strip()
            sub_sentences = re.split('[!?.,;]', sentence)

            for sub_sentence in sub_sentences:
                sub_sentence = sub_sentence.strip()
                if sub_sentence != '':

                #Function call to split based on connecting words
                    sub2_sentences = split_connecting(sub_sentence)

                    for sub2_sentence in sub2_sentences:
                        sub2_sentence = sub2_sentence.strip()

                        #To divide each individual sentence into words
                        words = sub2_sentence.split(' ')
                        #Dictionary to store values of features temporarily
                        tempDictionary_features = {}

                        #Extract every feature from the features lexicon and check it's present in the words list and initilize the features
                        for word in words:
                            #To ignore empty words and stopwords
                            if word == '' or word in stopLex: continue 
                            else:
                                if word in features.keys(): tempDictionary_features[features.get(word)] = 0
                                else: continue

                        if (len(tempDictionary_features) > 0):

                            counter = 0

                            for word in words:
                                #Check for positive words
                                if word in positive_lex:
                                    counter = counter + 1
                                    #Check for negation words
                                    if(words.index(word) != 0):
                                        if words[words.index(word) -1] in negation_words:
                                            counter = counter - 2

                                #Check for negative words
                                if word in negative_lex:
                                    counter = counter - 1
                                    #Check for negation words
                                    if(words.index(word) != 0):
                                        if words[words.index(word) -1] in negation_words:
                                            counter = counter + 2
              
                                for cur_feature in tempDictionary_features:
                                        tempDictionary_features[cur_feature] = counter

                            for feature in tempDictionary_features:
                                if feature in mainDictionary_features:
                                    mainDictionary_features[feature] = mainDictionary_features[feature] + tempDictionary_features[feature]
                                else:
                                    mainDictionary_features[feature] = tempDictionary_features[feature]

        
        temp = 0
        for k in mainDictionary_features:
            if k in priority.keys() : temp = temp + mainDictionary_features.get(k)*priority.get(k)   
        if star == 1 : 
            star_one = star_one + temp
            counter_one = counter_one + 1
        elif star == 2 : 
            star_two = star_two + temp
            counter_two = counter_two + 1
        elif star == 3 : 
            star_three = star_three + temp
            counter_three = counter_three + 1
        elif star == 4 : 
            star_four = star_four + temp
            counter_four = counter_four + 1
        elif star == 5 : 
            star_five = star_five + temp
            counter_five = counter_five + 1
         
    print("star_one :"+ str(star_one) + " " + "counter_one : "+ str(counter_one))
    print("star_two :"+ str(star_two) + " " + "counter_two : "+ str(counter_two))
    print("star_three :"+ str(star_three) + " " + "counter_three : "+ str(counter_three))
    print("star_four :"+ str(star_four) + " " + "counter_four : "+ str(counter_four))
    print("star_five :"+ str(star_five) + " " + "counter_five : "+ str(counter_five))
    print(star_one/counter_one)
    print(star_two/counter_two) 
    print(star_three/counter_three)
    print(star_four/counter_four)
    print(star_five/counter_five)

    total_avg = star_one + star_two + star_three + star_four + star_five
    normalization_score = total_avg/review_counter
    
    objects = ('1star', '2star', '3star', '4star', '5star')
    y_pos = np.arange(len(objects))
    
    performance = [(star_one/counter_one) + normalization_score, (star_two/counter_two) + normalization_score, 
                    (star_three/counter_three) + normalization_score, (star_four/counter_four) + normalization_score, (star_five/counter_five) + normalization_score]
    #To plot the bar chart of stars vs reviews
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Avg. Score')
    plt.axhline(y = normalization_score,color='red', linestyle='dashed', linewidth=2)
    plt.title('Restaurant Reviews Ratings')
 
    plt.show()
    #Amount of time algorithm takes to complete execution 
    print("--- %s seconds ---" % (time.time() - start_time))