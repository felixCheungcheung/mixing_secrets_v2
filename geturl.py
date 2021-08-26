import requests
from bs4 import BeautifulSoup
#Poor Boy
#Mystery
if __name__ == "__main__":
    webside = "https://cambridge-mt.com/ms/mtk/"
    html = requests.get(url=webside)

    bf = BeautifulSoup(html.text, "html.parser")
    texts = bf.find_all('div', class_ = 'm-mtk-track__main')

    items = []

    for text in texts:
        
        bftext = BeautifulSoup(str(text), "html.parser")
        name = None
        mixurl = None
        fullurl = None

        # get project name
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

        mixeds = bftext.find_all('span', class_ = 'l-nowrap')
        for mix in mixeds:
            content = mix.contents[0]
            if content.startswith("Full"):
                mixurl = mix.a['href']

        if name and fullurl and  mixurl:
            items.append((name, fullurl, mixurl))
    with open("downloadurls.txt", "w") as f:
        for item in items:
            f.write("{},{},{}\n".format(item[0], item[1], item[2]))
        