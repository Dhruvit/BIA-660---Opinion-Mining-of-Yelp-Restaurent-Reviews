#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 20:48:38 2016

"""
import simplejson as json
#To read the original business json file to get the business IDs
def read_file():
    i = 0
    jsonfilename="yelp_academic_dataset_business.json"
    jfile=open(jsonfilename)
    categories={}
    for line in jfile:
        lineRead=json.loads(line)
        if('Restaurants' in lineRead['categories']):
            categories[lineRead['business_id']]=lineRead['categories']
            i += 1
    jfile.close()
    return categories
    
#To obtain business IDs for restaurant categories
def getBusinessIdForCat(categories):
    bIds=[]
    for k in categories:
         for x in categories[k]:
           bIds.append(k)
    return bIds
    
#To obtain review text for the corresponding business IDs
def getReviewsForBId(bIds):
    reviews=[]
    ratings=[]
    reviewsBids=[]
    #To read the review json file
    jsonfilename="yelp_academic_dataset_review.json"
    jfile=open(jsonfilename)
    for line in jfile:
        lineRead=json.loads(line)
        if(lineRead['business_id'] in bIds):
             reviews.append(lineRead['text'])
             ratings.append(lineRead['stars'])
             reviewsBids.append(lineRead['business_id'])
        if(len(reviews)>=10000):break
    merged = zip(ratings,reviews)
    
    
    file = open('RatingsReviews.txt', 'w')
    for i in  merged:
        rating1 = ((str(i)).split(',',1)[0])
        review1 =  ((str(i)).split(',',1)[1])
        rating = rating1.replace('(',"")
        file.write(rating + '@@@@@')
        review2 = review1.replace(')',"")
        review3 = review2.replace("'","")
        review = review3.replace('"',"")
        file.write(review.encode('ascii', 'ignore').decode('ascii') + '@#$@#$')

    file.close()
  
    jfile.close()
    return reviews, reviewsBids
     
if __name__ == '__main__':
     #Read all Categories from file:
     categories=read_file() 
     
    #get business ids of restaurants 
     businessIDDict=getBusinessIdForCat(categories)


    
#gathering reviews for target cuisine to generate categories for target cuisine
catSpecificReviews =getReviewsForBId(businessIDDict)
print("catSpecificReviews Size: "+str(len(catSpecificReviews)))



