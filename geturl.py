import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    webside = "https://cambridge-mt.com/ms/mtk/"
    html = requests.get(url=webside)

    bf = BeautifulSoup(html.text, "html.parser")
    genres = bf.find_all('div',class_ = 'c-mtk__genre')
    items = []
    
    for genre in genres:
        
        bfgenre = BeautifulSoup(str(genre), "html.parser")
        track_high_genre = None
        track_high_genre = bfgenre.h3.string
        
        songs = bfgenre.find_all('div',class_ = 'c-mtk__artist m-container m-container--artist')
        for song in songs:
            
            bfsong = BeautifulSoup(str(song), "html.parser")
            
            
            artist_name = None
            artist_name = bfsong.h4.string
            track_sub_genre = None
            track_sub_genre = bfsong.find('span', class_ = 'm-container__title-bar-item').string

            # one artist may have more than one song
            texts = bfsong.find_all('div', class_ = 'm-mtk-track__main')

            for text in texts:
                
                name = None
                mixurl = None
                fullurl = None
                bftext = BeautifulSoup(str(text), "html.parser")

                # get song name
                contents = bftext.find_all('span', class_ = 'm-mtk-track__name')[0].contents
                if len(contents) == 1:
                    name = contents[0].strip().strip('\'').replace(',','').replace('\n\'',' ')
                else:
                    name = contents[1].strip().strip('\'').replace(',','').replace('\n\'',' ')

                
                # get full track url
                fulls = bftext.find_all('li', class_ = 'm-mtk-download')
                for full in fulls:
                    fulltype = full.div.div
                    if fulltype and fulltype.contents[0].startswith("Full"):
                        fullurl = full.find('a')['href']
                    elif fulltype and fulltype.contents[0].startswith("Edited"):
                        fullurl = full.find('a')['href']

                mixeds = bftext.find_all('span', class_ = 'l-nowrap')
                for mix in mixeds:
                    content = mix.contents[0]
                    if content.startswith("Full"):
                        mixurl = mix.a['href']
                    elif content.startswith("Excerpt"):
                        mixurl = mix.a['href']

                if name and fullurl and  mixurl and track_high_genre and track_sub_genre and artist_name:
                    items.append((track_high_genre, track_sub_genre, name, artist_name, fullurl, mixurl))
    #print(count)
    print("{} songs in Total".format(len(items)))    
    with open("downloadurls.txt", "w",encoding = 'latin-1') as f:
        for item in items:
            f.write("{},{},{},{},{},{}\n".format(item[0], item[1], item[2], item[3], item[4], item[5]))
        