import json
import requests
from pathlib import Path 
from bs4 import BeautifulSoup

PAGE_URL = "https://fehpass.fire-emblem-heroes.com/en-US/"
FIRE_EMBLEM_FILENAME = "emblem_characters.json"
FILE_PATH = Path(FIRE_EMBLEM_FILENAME)

# Request main page html 
source_html = requests.get(PAGE_URL).text
# Parse main page html 
soup = BeautifulSoup(source_html, "lxml") 
# print(soup.prettify())

def getArchivedCharacterList():
    ref_links = []
    characters = soup.findAll("li", class_="cahra_list_item")
    for c in characters:
        name =  c.find('dl',class_="chara_txt").dd.text
        link = c.find('p',class_="more_link").a['href']
        ref_links.append({'name': name, 'link': link})

    return ref_links


def getCharacterDetails(char_ref_link):
    character_url = PAGE_URL + char_ref_link + "/"
    # Request character html 
    source = requests.get(character_url).text
    # Parse character html 
    soup = BeautifulSoup(source, "lxml") 

    name = soup.find('p', class_="chara_name").text
    title = soup.find('p', class_="chara_catch").text
    icon = soup.find('p', class_="chara_icon").img['src']
    mini_img = soup.find('p', class_="mini_img").img['src']
    img = soup.find('p', class_="chara_img").a.img['src']
    voices = [x['data-vfile'] for x in soup.find('ul', class_="btn_voice_wrap").find_all('li')]
    summary = soup.find('section', class_='chara_wrap').find_all('p')[-1].text

    return {'name': name, 'title': title, 'ref_link': char_ref_link, 'icon_link': icon, 'mini-img': mini_img, 'miniImageLink': img, 'voice_1': voices[0], 'voice_2': voices[1],'summary': summary}


def getCurrentHeroDetails():
    # type = ['new', 'next']
    character = soup.find("section", class_="new")
    ref_link = character.find('p',class_="more_link").a['href']
    details = getCharacterDetails(ref_link)

    return details


def saveCharacterInfo(character):
    characters = []
    if FILE_PATH.is_file():
        with open(FIRE_EMBLEM_FILENAME) as json_file:
            characters = json.load(json_file)
    
    characters.append(character)
    with open(FIRE_EMBLEM_FILENAME, 'w') as outfile:
        outfile.write(json.dumps(characters, indent = 2))


if __name__ == "__main__":
    if not FILE_PATH.is_file():
        ref_links = getArchivedCharacterList()
        for link in ref_links:
            char_details = getCharacterDetails(link['link'])
            r = requests.post('http://127.0.0.1:8000/characters/', json=char_details)
            saveCharacterInfo(char_details)
    else:
        char_details = getCurrentHeroDetails()
        r = requests.post('http://127.0.0.1:8000/characters/', json=char_details)
        saveCharacterInfo(char_details)