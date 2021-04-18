import csv, json
from PIL import Image
from app import db, models
def process_champion(name):
    name = name.lower()
    name = name.replace(" ", "")
    name = name.replace("-", "")
    name = name.replace("'", "")
    name = name.replace(".", "")
    return name
def get_counter():
    with open('/home/vanhocvp/Code/AI/NLP/API/Crawl_data/counter.csv', 'r') as file:
        reader = csv.reader(file)
        champion = []
        counter = {}
        be_countered = {}
        combine_with = {}
        for row in reader:
            champion.append(process_champion(row[0]))
            name_champ = process_champion(row[1])
            counter[name_champ] = row[2]
            be_countered[name_champ] = row[3]
            combine_with[name_champ] = row[4]
        return counter, be_countered, combine_with
def get_build_item():
    with open('/home/vanhocvp/Code/AI/NLP/API/Crawl_data/build_item.csv', 'r') as file:
        reader = csv.reader(file)
        item = {}
        for row in reader:
            # champion.append(process_champion(row[0]))
            name_champ = process_champion(row[0])
            tmp = ""
            tmp += row[1].split("'")[1]+" + "+row[2].split("'")[1]+" + "+row[3].split("'")[1]+" + "+row[4].split("'")[1]+" + "+row[5].split("'")[1]+" + "+row[6].split("'")[1]
            item[name_champ] = tmp
        return item
def get_introduce():
    with open('/home/vanhocvp/Code/AI/NLP/API/Crawl_data/introduce.json', 'r') as file:
        reader = json.load(file)
        introduce = {}
        for i in reader:
            name_champ = process_champion(i)
            if name_champ == 'ngộkhông':
                name_champ = 'wukong'
            introduce[name_champ] = reader[i]
            # print (introduce)
            # break
        return introduce
def get_combo():
    with open('/home/vanhocvp/Code/AI/NLP/API/Crawl_data/combo.json', 'r') as file:
        reader = json.load(file)
        introduce = {}
        for i in reader:
            name_champ = process_champion(i)
            if name_champ == 'nunu&willump':
                name_champ = 'nunu'
            tmp = ""
            for s in reader[i]:
                tmp += s + " "
            introduce[name_champ] = tmp
            # print (introduce)
            # break
        return introduce
def get_howtoplay():
    with open('/home/vanhocvp/Code/AI/NLP/API/Crawl_data/how_to_play.json', 'r') as file:
        reader = json.load(file)
        introduce = {}
        for i in reader:
            name_champ = process_champion(i)
            if name_champ == 'nunu&willump':
                name_champ = 'nunu'
            introduce[name_champ] = reader[i]
            # print (introduce)
            # break
        return introduce
def get_how_to_use_skill():
    with open('/home/vanhocvp/Code/AI/NLP/API/Crawl_data/how_to_use_skill.json', 'r') as file:
        reader = json.load(file)
        introduce = {}
        for i in reader:
            name_champ = process_champion(i)
            if name_champ == 'nunu&willump':
                name_champ = 'nunu'
            introduce[name_champ] = str(reader[i])
            # print (introduce)
            # break
        return introduce
def get_champion():
    with open('/home/vanhocvp/Code/AI/NLP/API/Crawl_data/champions_name.txt', 'r') as file:
        reader = csv.reader(file)
        champion = []
        # with open('/home/vanhocvp/Code/AI/NLP/API/Crawl_data/champions_name.txt', 'w') as f:
        for row in reader:
            champion.append(process_champion(row[0]))
        return champion
counter1, be_countered1, combine_with1 = get_counter()
build_item1 = get_build_item()
introduce1 = get_introduce()
combo1 = get_combo()
how_to_play1 = get_howtoplay()
how_to_use_skill1 = get_how_to_use_skill()
champions = get_champion()
def set_None():
    for c in champions:
        if c not in counter1.keys():
            counter1[c] = ""
        if c not in be_countered1.keys():
            be_countered1[c] = ""
        if c not in combine_with1.keys():
            combine_with1[c] = ""
        if c not in build_item1.keys():
            build_item1[c] = ""
        if c not in introduce1.keys():
            introduce1[c] = ""
        if c not in combo1.keys():
            combo1[c] = ""
        if c not in how_to_play1.keys():
            how_to_play1[c] = ""
        if c not in how_to_use_skill1.keys():
            how_to_use_skill1[c] = ""
def get_data():
    for c in champions:
        try:
            
            path1 = '/home/vanhocvp/Code/AI/NLP/API/Crawl_data/bang_ngoc/'+c+'.png'
            socket = open(path1, 'rb')
            path2 = '/home/vanhocvp/Code/AI/NLP/API/Crawl_data/up_skill/'+c+'.png'
            up_skill = open(path2, 'rb')
            
        except:
            print (c)
            continue
        path1 = '/home/vanhocvp/Code/AI/NLP/API/Crawl_data/bang_ngoc/'+c+'.png'
        socket = open(path1, 'rb')
        path2 = '/home/vanhocvp/Code/AI/NLP/API/Crawl_data/up_skill/'+c+'.png'
        up_skill = open(path2, 'rb')
        x = models.Message(hero = c, build_item = build_item1[c], support_socket = socket.read(),
        counter = counter1[c], be_countered = be_countered1[c], skill_up = up_skill.read(), how_to_play = how_to_play1[c],
        combo = combo1[c], combine_with = combine_with1[c], how_to_use_skill = how_to_use_skill1[c], introduce = introduce1[c])
        db.session.add(x)
        db.session.commit()
        
set_None()       
get_data()
# print (be_countered1['zed'])