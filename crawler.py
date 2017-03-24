"""<An script to scrape data of Trip-advisor Website>
    Copyright (C) <2015>  <Bhaumik Shah, Avinash Reddy, Adarsh Chavakula>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>

"""

import pickle
import requests,os
from bs4 import BeautifulSoup
import urllib,urllib2
import time
url__dict={"chennai":"none",
"mumbai":"http://www.tripadvisor.in/Hotels-g304554-oa0-Mumbai_Bombay_Maharashtra-Hotels.html#ACCOM_OVERVIEW",
"bengaluru":"http://www.tripadvisor.in/Hotels-g297628-oa0-Bengaluru_Bangalore_Karnataka-Hotels.html#ACCOM_OVERVIEW",
"chennai":"http://www.tripadvisor.in/Hotels-g304556-oa0-Chennai_Madras_Tamil_Nadu-Hotels.html#ACCOM_OVERVIEW",
"goa":"http://www.tripadvisor.in/Hotels-g297604-oa0-Goa-Hotels.html#ACCOM_OVERVIEW",
"hyderabad":"http://www.tripadvisor.in/Hotels-g297586-oa0-Hyderabad_Telangana-Hotels.html#ACCOM_OVERVIEW"
}

path_root=os.path.dirname(os.path.realpath(__file__)) 

def get_hotel_names(city,number_of_hotels=5):
    print "downloading for the city:",city    
    url=url__dict.get(city)
    number_hotels=0
    f=open(path_root+"\city\\bad\\"+city+".txt","w")
    pickle.dump([],f)
    f.close()
    while number_hotels<number_of_hotels:
           left=number_of_hotels-number_hotels
           count=per_url(url,city,left)
           number_hotels+=count
           tok=url.split("-")
           tok[2]='oa'+str(int(tok[2][2:])+30)
           url='-'.join(tok)
    return 0
    
def per_url(url,city,left):
    r=requests.get(url)
    soup=BeautifulSoup(r.content)
    g_data=soup.find_all("div",{"class":"listing_title"})
    f_data=soup.find_all("div",{"class":"metaLocationInfo"})
    if left>=len(g_data):
        num=len(g_data)
    else:
        num=left
    lis=0
    for item,span in zip(g_data[0:num],f_data[0:num]):
        f=open(path_root+"\city\\bad\\"+city+".txt","r+")
        final=pickle.load(f)
        f.close()
        number_f=BeautifulSoup(str(span))
        span=number_f.find("span",{"class":"more"})
        hrefs=BeautifulSoup(str(item.contents[1]))
        ref=hrefs.find_all("a")
        link=ref[0].get("href")
        review_links=BeautifulSoup(str(span.contents[1]))
        review_link=review_links.find_all("a")
        review_ref=review_link[0].get("href")
        propid=int(ref[0].get("id").split('_')[1])
        hotelname=item.text         #String Processing required:format-u'\n\nThe Oberoi, Mumbai\n\n\n\n'
        hotelname=hotelname[2:len(hotelname)-4]
                                    #String Processing required format :'/Hotel_Review-g304554-d304225-Reviews-The_Oberoi_Mumbai-Mumbai_Bombay_Maharashtra.html'
        if len(span)!=0 :        
            number=span.text    #String Processing required:format-u'\n\n1,075 reviews\n\n'
            number=number.split(" ")[0]
            number=[str(a) for a in number.split(",")]
            number=int(''.join(number))
            reviews=get_review_hotel(review_ref,number)
            print len(reviews),hotelname,number
            lis=(hotelname,link,reviews,propid,number)
        else:
            lis=(hotelname,link,[("NA",0,0,0)],propid,0)
        final.append(lis)
        f=open(path_root+"\city\\bad\\"+city+".txt","r+")          
        pickle.dump(final,f)
        f.close()    
    return len(g_data)

def get_review_hotel(url,number):
    spli=url.split("-")
    spli=spli[0:4]+['or10']+spli[4:]
    url='-'.join(spli)
    url="http://www.tripadvisor.in"+url
    tot_reviews=[]
    i=0
    l=0
    while i<number and i<1000 :
       r=requests.get(url,timeout=1000)
       soup=BeautifulSoup(r.content)
       g_data=soup.find_all("div",{"class":"quote"})
       while l<len(g_data): 
           reviewlink=BeautifulSoup(str(g_data[l].contents[1]))
           hyper=reviewlink.find_all("a")
           linkling= hyper[0].get("href")
           reviewid= hyper[0].get("id")
           reviewid=int(reviewid[2:])
           review,count=get_review(linkling)
           i+=count
           l+=count
           tot_reviews+=review
       l=l-len(g_data)
       tok=url.split("-")
       tok[4]='or'+str(int(tok[4][2:])+10)
       url='-'.join(tok)
    return tot_reviews
    
def pre_process(review):
    review=review[1:len(review)-1]
    return review
    
def get_review(url_hotel_review):  
    review=[]
    url = "http://www.tripadvisor.in" + url_hotel_review   
    r=requests.get(url)
    soup=BeautifulSoup(r.content)
    g_data=soup.find_all("div",{"class":"entry"})#for review text
    f_data=soup.find_all("div",{"class":"col1of2"}) # for user info
    h_data=soup.find_all("div",{"class":"rating reviewItemInline"})
    count=0
    for a,b,c in zip(g_data,f_data,h_data):
        count+=1
        userinfo=BeautifulSoup(str(f_data[0]))
        rating_all=BeautifulSoup(str(c))
        rating=rating_all.find_all("img")        
        link_rating=int(rating[0].get("alt")[0])        
        nouserdata=userinfo.find_all("div",{"class":"contributionReviewBadge"})
        nohelpful1=userinfo.find_all("div",{"class":"helpfulVotesBadge badge no_cpu"})
        rev= a.text
        process_rev=pre_process(rev)        
        if len(nouserdata)==1:
            userreviews=nouserdata[0].text#String Processing required:format-u'\n\n5 hotel reviews\n'
            userreviews=int(userreviews[2:-14])# Are you sure what if reviews are >100 check!!!
            helpfulvotes=0
        else:
            userreviews=1
        if len(nohelpful1)==1:
            helpfulvotes=nohelpful1[0].text#String Processing required:format-u'\n\n19 helpful votes\n
            helpfulvotes=str(helpfulvotes)
            list1=helpfulvotes.split(" ")
            finalvotes=list1[0][2:]
            number=[str(a) for a in finalvotes.split(",")]
            finalvotes=int(''.join(number))
        else:
            finalvotes=0
        review.append((process_rev,userreviews,finalvotes,link_rating))
    return review,count
#a=get_hotel_names("hyderabad",30)



#lis returns a list of tuples (hotelname,hotellink,propertyid,no.of reviews)
#to get the hotelink 'http://www.tripadvisor.com' needs to be added as a prefix

    
    