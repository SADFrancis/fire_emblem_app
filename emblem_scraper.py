import json
import requests
from pathlib import Path 
from bs4 import BeautifulSoup
import re
import datetime
import math
import jsonlines
import sys


headers = {'Authorization': 'Token e4f2558a0794b8e6cdc65325c5c48a9425622e59'}

PAGE_URL = "https://fehpass.fire-emblem-heroes.com/en-US/"
BASE_URL = "https://fehpass.fire-emblem-heroes.com"
FIRE_EMBLEM_FILENAME = "emblem_characters.json"
FILE_PATH = Path(FIRE_EMBLEM_FILENAME)

HEROKU_DATABASE_URL = 'https://feh-resplendent.herokuapp.com/'
LOCAL_DATABASE_URL = 'http://127.0.0.1:8000/'
POST_CHARA_DETAILS_URL = HEROKU_DATABASE_URL+ 'characters/'
UPDATE_CHARA_DETAILS_URL = HEROKU_DATABASE_URL+'updatelatestarchived'

# first release was February 6, 2020, 7 AM UTC is reset time
# standard string formatting: 
# start_date.strftime('%Y-%m-%dT%H:%M:%SZ') '2020-02-06T07:00:00Z' where Z is UTC timezone
start_date = datetime.datetime(2020,2,6,7,0,0,0,datetime.timezone.utc)

# Keywords to check to find the kingdom theme
askr = ["Askr","Askran"]
embla = ["Embla","Emblan","Emblian"]
nifl = ["Nifl","Kingdom of Ice","land of ice"]
muspell = ["Múspell","Kingdom of Flame", "kingdom of flame"]
hel = ["Hel","realm of the dead"]
light_fairy = ["Ljósálfheimr","realm of dreams","ljósálfar","ljósálfr"]
dark_fairy = ["Dökkálfheimr","realm of nightmares","dökkálfar","dökkálfr"]
mecha = ["Niðavellir","realm of dvergar", "dvergar","Seiðjárn","seiðjárn"]
giant = ["Jötunheimr","kingdom of the Jötnar","realm of jötnar","land of the jötnar","jötnar"]

game_title_dict = {
    "game_title1":"Fire Emblem Heroes",
    "game_title2":"Fire Emblem: Mystery of the Emblem",
    "game_title3":"Fire Emblem: New Mystery of the Emblem",
    "game_title4":"Fire Emblem Echoes: Shadows of Valentia",
    "game_title5":"Fire Emblem: Genealogy of the Holy War",
    "game_title6":"Fire Emblem: Thracia 776",
    "game_title7":"Fire Emblem: The Binding Blade",
    "game_title8":"Fire Emblem: The Blazing Blade",
    "game_title9":"Fire Emblem: The Sacred Stones",
    "game_title10":"Fire Emblem: Path of Radiance",
    "game_title11":"Fire Emblem: Radiant Dawn",
    "game_title12":"Fire Emblem Awakening",
    "game_title13":"Fire Emblem Fates",
    "game_title14":"Fire Emblem: Three Houses",
    "game_title15":"Tokyo Mirage Sessions ＃FE Encore"
}


separator = '|'
askr_regex = re.compile(separator.join(askr))
embla_regex = re.compile(separator.join(embla))
nifl_regex = re.compile(separator.join(nifl))
muspell_regex = re.compile(separator.join(muspell))
hel_regex = re.compile(separator.join(hel))
light_fairy_regex = re.compile(separator.join(light_fairy))
dark_fairy_regex = re.compile(separator.join(dark_fairy))
mecha_regex = re.compile(separator.join(mecha))
giant_regex = re.compile(separator.join(giant))

kingdom_regex_dict = {
    askr_regex:askr[0],
    embla_regex:embla[0],
    nifl_regex: nifl[0],
    muspell_regex: muspell[0],
    hel_regex:hel[0],
    light_fairy_regex:light_fairy[0],
    dark_fairy_regex:dark_fairy[0],
    mecha_regex:mecha[0],
    giant_regex:giant[0]
}

# Request main page html 
source_html = requests.get(PAGE_URL)
# Parse main page html
# requests default encoding is ISO-8859-1, site charaset is utf-8
soup = BeautifulSoup(source_html.content.decode('utf-8','ignore'), "lxml") 
# print(soup.prettify())


def getArchivedCharacterList():
    ref_links = []
    characters = soup.findAll("li", class_="cahra_list_item")
    for c in characters:
        name =  c.find('dl',class_="chara_txt").dd.text
        ref = c.find('p',class_="more_link").a['href']
        game_title = c['data-title']
        ref_links.append({'name': name, 'game_origin':game_title_dict[game_title], 'ref_id': ref})
    return ref_links

def getMostRecentArchivedCharacterRef():
    characters = soup.findAll("li", class_="cahra_list_item")
    c = characters[0]
    name =  c.find('dl',class_="chara_txt").dd.text
    link = c.find('p',class_="more_link").a['href']
    game_title = c['data-title']
    return ({'name': name, 'game_origin':game_title_dict[game_title], 'ref_id': link})

def getCharacterDetails(char_ref_link, game_origin='',release_index=525):
    '''
        only archived units have game_origin assigned thus,
        initial parameters need to be assigned. Index is based off of character release order 
        Example parsed link
        ../../common/img/chara_img_00099002000247_01.png?time=1637825767692
        regex_append cleans the timestamp (it seems to be time uploaded to site,
         not published for public viewership)
        regex_url cleans the ../../
    '''
    regex_append = re.compile(r'\?.*')
    regex_url = re.compile(r'\.\.\/\.\.') # not necessary, but it's cleaner
    
    # Get charaId, Ex:'00099002000247', call via charaId.group(0), needed for voice lines
    charaId = re.search(re.compile(r'\d{14}'),char_ref_link)

    character_url = PAGE_URL + char_ref_link
    # Request character html 
    source = requests.get(character_url)
    # Parse character html in correct encoding
    soup = BeautifulSoup(source.content.decode('utf-8','ignore'), "lxml") 

    name = soup.find('p', class_="chara_name").text
    title = soup.find('p', class_="chara_catch").text

    # Find Icon   
    icon = soup.find('p', class_="chara_icon").img['src']
    icon_base = re.sub(regex_append,'', re.sub(regex_url,'',icon))
    icon = BASE_URL + icon_base

    # Find sprite
    sprite = soup.find('p', class_="mini_img").img['src']
    sprite_base = re.sub(regex_append,'', re.sub(regex_url,'',sprite))
    sprite = BASE_URL + sprite_base  

    # Find 4 piece artwork set
    # In order: Neutral, Attack, Special, Damaged
    art_set = []
    for art_piece in soup.find_all("li", class_="slider_item"):
        piece = art_piece.img['src']
        art_piece_link = re.sub(regex_append,'', re.sub(regex_url,'',piece))
        art_set.append(BASE_URL+art_piece_link)

    # Grab voice links
    voices = [
            "https://fehpass.fire-emblem-heroes.com/common/voice/" + "chara_" +charaId.group(0)+"_1.mp3",
            "https://fehpass.fire-emblem-heroes.com/common/voice/" + "chara_" +charaId.group(0)+"_2.mp3"
    ]

    # Grab voice lines in text form
    lines_soup = soup.find("dl",class_='chara_selif').find_all("dd")
    lines = [lines_soup[0].text,lines_soup[1].text]

    # Sharena's Fashion Check
    summary = soup.find('section', class_='chara_wrap').find_all('p')[-1].text

    # Check realm theme based on lines and summary (why encoding was necessary)
    realm = ""
    realm_index = 0
    for regex in kingdom_regex_dict:    
        if regex.search(summary):
            realm = kingdom_regex_dict[regex]
            break
        realm_index +=1     
        for line in lines:
            if regex.search(line):
                print("found em")
                realm = kingdom_regex_dict[regex]
                break        
    

    return {'name': name, 
            'title': title, 
            'game_origin':game_origin, 
            'ref_id': char_ref_link,
            'ref_link': character_url,
            'icon_link': icon, 
            'sprite': sprite, 
            'portrait': art_set[0], 
            'attack':art_set[1], 
            'special':art_set[2],
            'damaged':art_set[3], 
            'voice_1': voices[0], 
            'voice_2': voices[1],
            'line_1': lines[0],
            'line_2': lines[1],
            'summary': summary,
            'realm': realm,
            'realm_index': realm_index,
            'release_date':assignReleaseDate(release_index),
            'index': release_index
            }


def getCurrentAndNextHeroDetails(current_archived_index):
    # type = ['new', 'next']
    # index = how many units already exist in the archive already
    ref_links = []
    current_character = soup.find("section", class_="new")
    ref_links.append(current_character.find('p',class_="more_link").a['href'])
    next_characters = soup.find("section", class_="next")
    ref_links.append(next_characters.find('p',class_="more_link").a['href'])
    char_details = [] 
    current_and_next_index = current_archived_index+1
    for link in ref_links:
        char_details.append(getCharacterDetails(link,str(''),current_and_next_index))
        current_and_next_index +=1

    return char_details


def saveCharacterInfo(character):
    characters = []
    if FILE_PATH.is_file():
        with open(FIRE_EMBLEM_FILENAME) as json_file:
            characters = json.load(json_file)
    
    characters.append(character)
    with open(FIRE_EMBLEM_FILENAME, 'w') as outfile:
        outfile.write(json.dumps(characters, indent = 2))

def assignReleaseDate(index):
#if(n.even -> day == 10)
# #if (n.odd -.day == 25)
#if(floor(2+ n*0.5)%12 -> month)   
#if(2020+ floor((2+ n*0.5)/12) -> Year)    
    if(index == 0):
        # Lyn released 2020-02-06
        return start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        release_day = 10 if index % 2 == 0 else 25   # (index % 2 == 0) ? 10: 25
        release_month = math.floor(1+ index*0.5) %12+1 # 2 resplendents per month, starting Feb(start with 2, but split with 1 outside of % operation to avoid month==0)
        release_year = 2020 + math.floor((1+index*0.5)/12) # 24 resplendents per year
        release_date = datetime.datetime(release_year,release_month,release_day,7,0,0,0,datetime.timezone.utc)
        return release_date.strftime('%Y-%m-%dT%H:%M:%SZ')

if __name__ == "__main__":
    if not FILE_PATH.is_file():
        print("initializing json database file")
        # intialize and reverse the dictionary list in one go, [start:stop:step]
        ref_links = getArchivedCharacterList()[::-1] 
        index =0 # counting up the roster size for assignReleasedate
        for link in ref_links:
            char_details = getCharacterDetails(link['ref_id'],link['game_origin'],index)
            index +=1
            saveCharacterInfo(char_details)
            r = requests.post(POST_CHARA_DETAILS_URL, json=char_details, headers=headers)
        print(f"Done! Updated the file with all previously released and archived units as of: \n {datetime.datetime.now()} \n See {FILE_PATH} for details!")
    else:
        print(f"Going to check {FILE_PATH} to find current and upcoming entries \n as of {datetime.datetime.now()}")
        with open(FILE_PATH) as json_file:
            scraped_data = json.load(json_file)
        current_index = scraped_data[-1]['index'] # get last uploaded count

        # Create JSON objects of most recently archived+current+future units to be released
        current_and_next_details = getCurrentAndNextHeroDetails(current_index)
        latest_archived_unit_ref = getMostRecentArchivedCharacterRef()
        #print(json.dumps(current_and_next_details,sort_keys=False,ensure_ascii=False,indent=4))
        '''
            First, check to make sure the current_and_next_details are
            not already in the database. If the latest "next" unit is not in the database,
            we definitely have stuff to update.

            Then, there are times when the site doesn't simultaneously archive a character and update the site with a new character due to
            release date timing. For instance, it might reveal a new character on the 23rd Jan., and the site would have
            a unit for the 25th-9th rotation (which was revealed back in Jan 9th) and the just revealed Feb. 10th-25th rotation follwing it on top of the unit currently
            currently in distribution (Jan. 10th-25th, and the date of this hypothetical scenario would still be Jan 23rd.) 
            So you may have to check again on the 25th or even 26th.

            Then, when it finally updates, we need to grab the most recent archived unit reference info
            dict {name,game_origin,ref_id} for the game origin data.
            Remember, current and next don't have game_origin details until they end up
            in the archived list, so the most recently archived unit must be updated

        '''
        
        ## first checking to update game origin of most recently archived unit
        ## with the last 5 units in the dataset.

        print(f"let's see if we need to update the latest archived unit {latest_archived_unit_ref}")       
        did_site_updated_latest_archived_unit = False  
        for char_in_db in scraped_data[-5:]:
            if char_in_db['ref_id'] == latest_archived_unit_ref['ref_id'] and char_in_db['game_origin'] == "":
                char_in_db['game_origin'] = latest_archived_unit_ref['game_origin']
                with open(FILE_PATH, 'w') as json_file:
                    print(f"Updating game origin of {char_in_db['name']} - {char_in_db['title']}: ref_id {char_in_db['ref_id']}")
                    json_file.write(json.dumps(scraped_data,sort_keys=False,ensure_ascii=False,indent=2))
                    # UPDATE CHARACTER IN DJANGO DATABASE
                    r = requests.post(UPDATE_CHARA_DETAILS_URL, json=char_in_db, headers=headers)
                    did_site_updated_latest_archived_unit = True        
        
        if scraped_data[-1]['ref_id'] == current_and_next_details[-1]['ref_id']:
            if not did_site_updated_latest_archived_unit:
                print("Database is already up to date with the site, logging out!")
            sys.exit(0)

        # Now to update with brand new units
        print(f"Found {len(current_and_next_details)} new site entries to update database with")
        #print(json.dumps(latest_archived_unit_ref,sort_keys=False,ensure_ascii=False,indent=4))
            
        is_in_already = False
        for char_details in current_and_next_details:
            for char_in_db in scraped_data: 
                # now check if the new character is in the database already in (sanity check)
                if char_in_db['ref_id'] == char_details['ref_id']:
                    is_in_already = True
                    break
            if not is_in_already:
                saveCharacterInfo(char_details)
                r = requests.post(POST_CHARA_DETAILS_URL, json=char_details, headers=headers)
            is_in_already = False
        print("Database updated with new entries!")

        ######### dummy junk

        # with open("trydd.json",'r') as dummy_file:
        #     dummy_dd = json.load(dummy_file)

        # for scraped in scraped_data:
        #     if scraped['name'] == dummy_dd['name']:
        #         scraped['game_origin'] = dummy_dd['game_origin']
        #         print(json.dumps(scraped_data,sort_keys=False,ensure_ascii=False,indent=4))
        #         with open("tryharder.json", 'w') as json_file:
        #         #new_file = open(FILE_PATH,'w')
        #         #json.dump(scraped_data,new_file,ensure_ascii=False,indent=4)
        #         #new_file.close()
        #             json_file.write(json.dumps(scraped_data,sort_keys=False,ensure_ascii=False,indent=2))
        #             #updated_r = requests.post(f"http://127.0.0.1:8000/characters/{scraped['name']}",json=scraped_data)
