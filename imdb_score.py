from bs4 import BeautifulSoup
import requests
import re
import tkinter

def search_Title(title):
    URL_IMDB = 'https://www.imdb.com/find?s=all&q='
    TITLE = title.replace(' ','+')
    print('### REPLACED TITLE BY: %s ###' %(TITLE)) 
    print('### REQUESTING PAGE ###')
    page= requests.get(URL_IMDB+TITLE)
    print('### REQUESTING PAGE: SUCCESSFUL ###')
    print('### CREATING BS4 OBJECT###')
    soup = BeautifulSoup(page.content,'html.parser')
    print('### CREATING BS4 OBJECT: SUCCESFUL ###')
    
    return soup

def select_Movie(soup):
    print('### GETTING MATCHES ###')
    results = soup.find_all('td',class_='result_text')
    print('### GETTING MATCHES: SUCCESFUL ### ')
     
    for index,link in enumerate(results):
        re_match = re.findall(r">(.*?)<",str(link))
        tit = re_match[1]
        year= re_match[2]
        if index==0:
            title_and_year = tit + year
        url=link.find_all('a',href=True)[0] 
        print(str(index)+'   '+tit +"  "+ year)
    try:
        print('### URL FIRST RESULT:  '+str(results[0].find_all('a',href=True)[0]['href']) + ' ###')      
        return str(results[0].find_all('a',href=True)[0]['href']),title_and_year
    except IndexError as Error:
        print('MovieError: Could not find Movie. Are you sure the spelling is right?')
def get_score(href):
    url = 'https://www.imdb.com/'
    print('### RETRIEVING SCORE PAGE ###')
    page = requests.get(url + href)
    print('### RETRIEVING SCORE PAGE: SUCCESSFUL ###')
    soup = BeautifulSoup(page.content, 'html.parser')
    print('### FINDING SCORE ###')
    try:
        result = soup.find_all('div',class_='ratingValue')[0]
        score = re.findall(r'title=\"(.*?)\">',str(result))
        print('### FINDING SCORE: SUCCESSFUL ###')
        return score[0]
    except IndexError as Error:
        print('ScoreError: Could not find IMDB-Score of movie. Are you sure there is a score available?')

def get_entry_value():
    T.delete(1.0,'end')
    try:
        url, title =  select_Movie(search_Title(entry.get()))
        solution = get_score(url)
    except TypeError: 
        solution,title = ' ', 'not found'
    entry.delete(0,'end')
    T.insert('end',str(title) + ':  '+str(solution))

top = tkinter.Tk()
top.title('IMDB finder')
tkinter.Label(top, text='Movie').grid(row=1,column=0)
entry = tkinter.Entry(top)
entry.grid(row=1,column=1)
T=tkinter.Text(top,height=2,width=70)
T.grid(row=4,column=0,columnspan=4)

tkinter.Button(top, text='QUIT',command=top.quit).grid(row=3,column=2)
tkinter.Button(top,text='FIND SCORE',command=get_entry_value).grid(row=3)
top.mainloop()







