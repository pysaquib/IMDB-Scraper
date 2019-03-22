'''
This program scrape list and details of Top 250 rated movies of India according to IMDB and analyse them
categorically in different aspects like, language, directors, genre etc.
'''


import requests # Importing requests to get request data from a Web URL
from bs4 import BeautifulSoup # Importing BeautifulSoup from BS4, BeautifulSoup is a scraping tool
import pprint # Importing pprint for pretty print
import json # Importing JSON module to load and dump from json file and dump dictionary in json respectively
import os
import time # Importing time library to 'sleep' our program between two requests
import random

# Task 1
# This function returns list of Top 250 movies according to IMDB with minor details

def scrape_top_list():
    url = "https://www.imdb.com/india/top-rated-indian-movies/"  # Scraping data of this URL
    sleep = random.randint(1,3)
    time.sleep(sleep)
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser') # Parsing data that we get from requests
    tbody = soup.find("tbody", class_="lister-list") # Finding the first 'tbody' tag whose class is "lister-list"
    trs = tbody.findAll("tr") # Finding all 'tr' tags
    master_list = []
    index = 0
    for tr in trs:
        movie = {}
        Rank = tr.find('td', class_ = "titleColumn").get_text().strip().split()[0].strip(".") # Getting Rank from 'td' tag
        Name = tr.find('td', class_ = "titleColumn").a.get_text() # Getting Name from 'td' tag
        Year = tr.find('td', class_ = "titleColumn").span.get_text().strip('(').strip(")") # Getting Year from 'td' tag
        Rating = tr.find('td', class_= "ratingColumn").strong.get_text() # Geting Rating from 'td' tag
        Url = "https://www.imdb.com"+tr.find('td', class_ = "titleColumn").a["href"] # Getting URL of the movie
        movie['Rank'] = int(Rank)
        movie['Name'] = Name
        movie['Year'] = int(Year)
        movie['Rating'] = float(Rating)
        movie['Url'] = Url[:37]
        master_list.append(movie)
    return master_list
Top250movies = scrape_top_list()

if(os.path.exists("Top250MoviesJSON.json") == False):
    list1 = scrape_top_list()
    print("LIST OF MOVIES")
    pprint.pprint(list1)
    x = json.dumps(list1, indent=4, sort_keys=True)
    with open("Top250MoviesJSON.json", "w+") as data:
        data.write(x)

#Task 2
#This functions returns Top 250 movies sorted in a list according to year they are released in

def sortByYear(moviesList):
    mainDict = {}
    for i in moviesList:
        if(i['Year'] not in mainDict):
            mainDict[i['Year']] = [] #Creating keys of every year in which movies are released

    for j in mainDict:
        index = 0
        smallList = []
        for k in moviesList:
            if(k['Year'] == j):
                smallList.append(k) #Appending movies in the key of the year they were released in
                mainDict[j] = smallList
    return mainDict
byYear = sortByYear(Top250movies)

#Task 3
#This function return Top 250 movies sorted in decades they are released in

def groupByDecades(movieList):
    decadeDict = {}
    for i in movieList:
        if(i['Year'] not in decadeDict):
            x = int(i['Year']/10)*10
            if(x not in decadeDict):
                decadeDict[x] = []   #Creating keys of the decades in which the movies were released
    for j in decadeDict:
        smallList = []
        for k in movieList:
            if(k['Year'] >= j and k['Year'] < (j+10)):
                smallList.append(k)     #Appending all movies of same decades in a list
                decadeDict[j] = smallList #Assigning the corresponding value to its key
    return decadeDict
byDecades = groupByDecades(Top250movies)

#Task 12
#This function returns a list of full cast of a movie
def scrapeMovieCast(url_link):
    url = url_link
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'lxml')
    castDiv = soup.find('div', {'class' : "article", 'id' : "titleCast"})
    urlDiv = castDiv.find('div', class_="see-more")
    link = urlDiv.find('a')['href']
    moreUrl = url+link

    newPageData = requests.get(moreUrl).text
    soup = BeautifulSoup(newPageData, 'lxml')
    mainList = []
    mainDiv = soup.find('table', class_="cast_list") #Finding 'table' tag
    trs = mainDiv.findAll('tr') #Finding all 'tr' tags
    index = 0
    for i in trs:
        a = i.find('a') #Finding 'a' tag in each 'tr' tag
        if(a != None):
            subDict = {}
            td = i.find('td', class_="primary_photo")
            name = td.find('img')['title']  #Getting name of the cast
            id = td.find('a')['href']  #Getting IMDB ID of the cast
            id = id[6:15]
            subDict['Name'] = name  #Creating key as Name and assigning its value
            subDict['IMDB_ID'] = id  #Creating key as IMDB_ID and assigning its value
            mainList.append(subDict)  #Appending the dictionary in a main list
    return mainList

#Task 4 and Task 8 and Task 9 and Task 13
# This movie returns major details of a movies from the file if it exists,
# otherwise it scrapes and write the data into a file and then returns the data

def scrapeMovieDetails(url):
    fileName = url[27:(len(url)-1)]
    fileName = "MovieCache/"+fileName+".json"
    if(os.path.exists(fileName)): #Checks whether JSON file already exists or not
        f = open(fileName, 'r+')
        data = f.read()
        detailsFromFile = json.loads(data)
        return detailsFromFile      #Returns JSON data as dictionary
    sleep = random.randint(1,3)     #Generate a random number between 1 and 3, both inclusive
    time.sleep(sleep)               #Sleeping the program for the randomly generated seconds
    data = requests.get(url).text   #Requesting data from URL
    soup = BeautifulSoup(data, 'lxml')
    nameDiv = soup.find('div', class_="title_wrapper")      #Finding 'div' tag
    name = (nameDiv.find('h1').get_text().split())          #Finding 'h1' tag, getting the text from it, then splitting it
    name.pop()          #Removing last element
    finalName = " ".join(name) #Name
    posterMain = soup.find('div', class_="poster").img['src'] #Poster
    mainDiv = soup.find('div', class_="credit_summary_item")
    dir = mainDiv.findAll('a')        #Finding all 'a' tags from mainDiv
    directors = [] #Directors
    country = "" #Country
    lang = ""
    langList = [] #Languages
    for i in dir:
        directors.append(i.get_text())      #Appending directors name in list
    mainDivfor = soup.find('div',{'class' : "article", 'id' : "titleDetails"})

    divs = mainDivfor.findAll('div', class_="txt-block")
    for i in divs:
        a = i.find('h4', class_="inline") #Finding all 'h4' tag whose class is "inline" in 'div' whose class is "txt-block"
        if(a == None):
            pass
        else:       # Finding Countries and Languages if 'a' tag is not None
            if(a.get_text()=="Country:"):
                country = i.find('a').get_text()    #Finding country
            elif((a.get_text())=="Language:"):
                l = i.findAll('a')         #Finding all 'a' tags to get all languages
                for j in l:
                    lang = j.get_text()
                    langList.append(lang)   #Appending languages in a list
    bio = soup.find('div', class_="summary_text").get_text().strip() #Bio
    timeAndGenre = soup.find('div', class_="subtext")
    runTimeL = timeAndGenre.find('time').get_text().strip()
    runTimeL = runTimeL.split()
    totalRunTime = 0 #Runtime
    if(len(runTimeL)>1):
        totalRunTime = totalRunTime + int(runTimeL[0][0])*60 +int(runTimeL[1].strip("min"))
    else:
        totalRunTime = totalRunTime + int(runTimeL[0][0])*60
    genre = timeAndGenre.findAll('a')   #Finding all genres
    ghost = timeAndGenre.find()
    genreList = []
    for g in range(0, len(genre)-1):
        genreList.append(genre[g].get_text())   #Appending all genres in list
    castList = scrapeMovieCast(url)        #Calling 12th function to get full cast of this movie
    movie_details = {                      #Creating dictionary and assigning values to its respective keys
        'Name' : finalName,
        'Directors' : directors,
        'Languages' : langList,
        'Country' : country,
        'Bio' : bio,
        'Runtime' : totalRunTime,
        'Genre' : genreList,
        'Cast_List' : castList
    }
    f = open(fileName, 'w+')
    raw = json.dumps(movie_details, indent = 4, sort_keys = True)
    f.write(raw)                #Dumping the dictionary and writing it into a JSON file
    f.close()
    return movie_details

# Task 5
#This function returns a list with many major details of many movies
def getMovieListDetails(moviesList):
    detail_list = []
    r = int(input("How many movies do you want to scrape?\n"))
    if(r <= 250):
        for i in range(0, r):
             details = scrapeMovieDetails(moviesList[i]['Url'])     #Calling 4th function for 250 movies
             detail_list.append(details)         #Appending the returned data into a list
        return detail_list
    else:
        return ("Sorry. We only have movies details for top 250 movies")
movies = getMovieListDetails(Top250movies)

#Task 6
#This function returns a dictionary that states how many movies fall in a particular language
def analyseMoviesLanguage(movies):
        langDict = {}
        for i in movies:
            for j in i["Languages"]:
                if(j not in langDict):
                    langDict[j] = 0     #Creating key of every language and assigning its initial value 0
        for j in langDict:  #Iterating loop over the keys of the above mentioned dictionary
            for k in movies:    #Iterating loop over all movies while holding one dictionary key in 'j' at a time
                for m in k['Languages']: #Iterating loop over the 'Languages' key of each movie dictionary
                    if(m == j):
                        langDict[j]+=1    #Incrementing the value if languages match
        return langDict
byLang = analyseMoviesLanguage(movies)

#Task 7
#This function returns a dictionary that states how many movies each director made
def analyseMoviesDirectors(movies):
        directorsDict = {}
        for i in movies:        #Iterating loop over all movies
            for j in i["Directors"]:        #Iterating loop over 'Directors' list of each movie
                if(j not in directorsDict):
                    directorsDict[j] = 0
        for j in directorsDict:     #Iterating loop over newly created dictionary
            for k in movies:        #Iterating loop over movies
                for m in k['Directors']:       #Iterating loop over 'Directors' list of each movie
                    if(m == j):
                        directorsDict[j]+=1         #Incrementing the value if directors match
        return(directorsDict)
# pprint.pprint(analyseMoviesDirectors(movies))

#for Task 8 refer to line 124

#for Task 9 refer to line 124

#Task 10
#This function returns a dictionary stating numbers of movies in each language for each directors
def analyseLangAndDirectors(movies):
    newDict = {}
    for i in movies:
        for j in i['Directors']:
            if(j not in newDict):
                newDict[j] = {}     #Creating dictionary key for each director
    for nD in newDict:      #Iterating loop over newly created dictionary
        langList = {}
        for m in movies:    #Iterating loop over all movies
            for d in m['Directors']:    #Iterating loop over 'Directors' key of each movie
                if(d == nD):
                    for l in m['Languages']:    #Iterating loop over 'Languages' if directors match
                        if(l not in langList):
                            langList[l] = 1     #Creating a new key of the language
                        else:
                            langList[l]+= 1     #Incrementing the value if it already exists
        newDict[nD] = langList
    return (newDict)
dirWithLang = (analyseLangAndDirectors(movies))


#Task 11
#This function returns a dictionary that provides the number of movies of each Genre
def analyseMoviesGenre(movies):
    genreDict = {}
    for i in movies:        #Iterating loop over all movies
        for j in i['Genre']:        #Iterating lop over 'genre' key of each movie
            if(j not in genreDict):
                genreDict[j] = 0       #Creating a key of the genre if it doesn't exist in genreDict dictionary
    for k in genreDict:           #Iterating loop over genreDict dictionary
        for m in movies:          #Iterating loop over all movies
            for mL in m['Genre']:       #Iterating loop of 'genre' of each movie
                if(mL == k):
                    genreDict[k]+= 1    #Incrementing the value of the key
    return genreDict
# pprint.pprint(analyseMoviesGenre(movies))

#for Task 12 refer to line 85
#for Task 13 refer to line 124

#Task 14
#This function returns a dictionary with list of frequent_co actors with which lead actor of every movie has woked with
def analyseCoActors(movies):
    moviesW = movies[0:250]
    dicById = {}
    for i in moviesW:   #Iterating loop over all movies
        cast = i['Cast_List']
        dicById[cast[0]['IMDB_ID']] = {'name' : cast[0]['Name'],'frequent_co_actors' : []} #Creating a dictionary key for the lead actor

    for j in dicById:       #Iterating loop over the newly created dictionary
        for k in movies:    #Iterating loop over all movies
            for l in k:
                if(l == 'Cast_List'):
                    index = 0
                    main = k[l][0]['IMDB_ID']
                    if(main == j):      #Checking if lead actor key matches
                        for cast in k[l][1:6]:    #Iterating loop over next five actors
                            count = 1
                            for idmatch in dicById[j]['frequent_co']:
                                if(idmatch['id']==cast['IMDB_ID']):
                                    count+=idmatch['num_movies']    #Incrementing the count of the movies if actor already exist in the dictionary
                            n = {'id' : cast['IMDB_ID'], 'name' : cast['Name'], 'num_movies' : count}      #Creating a new dictionary for every new co-actor
                            dicById[j]['frequent_co'].append(n)     #Appending the dictionary in frequent_co_actors list of the main dictionary
    return dicById
# pprint.pprint(analyseCoActors(movies))

#Task 15
#This function returns dictionary with the ID, name etc of all actors appearing in more than one movie
def analyseActorsMovies(movies):
    newDic = {}
    for i in range(len(movies)):      #Iterating loop over the length of the movie list
        count = 1
        for j in movies[i]['Cast_List']:       #Iterating loop over 'Cast_List' pf each movie
            one = j['IMDB_ID']
            for i2 in range(i+1 ,len(movies)):      #Iterating loop over the next movies of the list
                for j2 in movies[i2]['Cast_List']:  #Iterating loop over its cast
                    two = j2['IMDB_ID']
                    if(one == two):
                        count+=1        #Incrementing if actors match
                        newDic[j['IMDB_ID']] = ({'name' : j['Name'], 'num_movies' : count})
    return newDic
# pprint.pprint(analyseActorsMovies(movies))
