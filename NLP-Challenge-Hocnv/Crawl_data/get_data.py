import requests
from bs4 import BeautifulSoup
import re
from os.path  import basename
import pandas as pd
import json
def get_bangngoc():
    list_champ_false = []
    response = requests.get("https://skmoba.com/champion")
    soup = BeautifulSoup(response.content, "html.parser")
    champions = soup.findAll('div', class_="col-lg-2 col-md-2 col-sm-2 col-xs-4 list_champ_home mb15")
    dem = 1
    for champion in champions:
        link = champion.find('a').attrs["href"]
        name_champ = link.split('/')[-1]
        print ("{}/{} : {}".format(dem,154, name_champ))
        link = 'https://skmoba.com/champions/huong-dan-choi-cach-len-do-' + name_champ
        res = requests.get(link)
        soup1 = BeautifulSoup(res.content, "html.parser")
        link_img = soup1.find_all('img')
        regex = '_sk'
        flag = 0
        for l in link_img:
            # print (l)
            source = l.get('src')
            # print (source)
            if re.search(regex, source) != None:
                path_img = '/home/vanhocvp/Code/AI/NLP/API/Crawl_data/up_skill/' + name_champ + '.png'
                flag = 1
                with open(path_img,"wb") as f:
                    f.write(requests.get(l['src']).content)
                break
        if flag == 0:
            list_champ_false.append(name_champ)
            
        dem += 1   
    f = open("/home/vanhocvp/Code/AI/NLP/API/Crawl_data/up_skill/champ_fall.txt", "w")
    for i in list_champ_false:
        f.write(i + '\n')
    f.close()
    print ("done")
def get_iem():
    list_champ_false = []
    list_item = {}
    build_item = {}
    response = requests.get("https://tranvanthong.com/tuong-lien-minh/")
    soup = BeautifulSoup(response.content, "html.parser")
    champions = soup.findAll('figcaption', class_="wp-caption-text gallery-caption")
    dem = 1
    for champion in champions:
        link = champion.find('a').attrs["href"]
        name_champ = link.split('/')[-2]
        if name_champ in build_item.keys():
            continue
        print ("{}/{} : {}".format(dem,len(champions), name_champ))
        res = requests.get(link)
        soup1 = BeautifulSoup(res.content, "html.parser")
        try:
            id =  soup1.find('article').attrs["id"].split('-')[-1]
            all_item = soup1.find('div', class_='gallery galleryid-'+id+ ' gallery-columns-6 gallery-size-thumbnail')
            tmp = [] #store all item to save to dict
            for i in all_item:
                item = i.text.strip()
                # print (item)
                path_img = '/home/vanhocvp/Code/AI/NLP/API/Crawl_data/all_item/' + i.a['href'].split('/')[-2] + '.png' 
                if item not in list_item.keys():
                    with open(path_img,"wb") as f:
                            f.write(requests.get(i.img['src']).content)
                    #save dict
                    list_item[item] = i.a['href'].split('/')[-2] + '.png'
                tmp.append(item)
            build_item[name_champ] = tmp
            # print (list_item)
            # print (build_item)
            dem += 1   
        except:
            list_champ_false.append(name_champ)
        
        
        # break
    f = open("/home/vanhocvp/Code/AI/NLP/API/Crawl_data/champ_fall_build_item.txt", "w")
    for i in list_champ_false:
        f.write(i + '\n')
    f.close()
    with open('build_item.csv', 'w') as f:
            for key in build_item.keys():
                f.write("%s, %s\n" % (key, build_item[key]))
    with open('key_item.csv', 'w') as f:
            for key in list_item.keys():
                f.write("%s, %s\n" % (key, list_item[key]))
    print ("done")
def get_counter():
    response = requests.get("https://skmoba.com/tuong-khac-che")
    soup = BeautifulSoup(response.content, "html.parser")
    champions = soup.findAll('div', class_="col-lg-2 col-md-2 col-sm-2 col-xs-4 list_champ_home mb15")
    dem = 1
    list_champ = []
    list_champ_false = []
    list_counter = []
    list_becounter = []
    list_combine = []
    for champion in champions:
        link = champion.find('a').attrs["href"]
        name_champ = link.split('-')[-1]
        print ("{}/{} : {}".format(dem,154, name_champ))
        try:
            res = requests.get(link)
            soup1 = BeautifulSoup(res.content, "html.parser")
            counter = soup1.find('div', class_='col-sm-12 col-xs-12 box_list_champs_c')
            be_counter, combine_with = soup1.find_all('div', class_='col-sm-12 col-xs-12 box_list_champs_c box_list_champs_str')
            #counter
            tmp = ""
            for i in counter.find_all('span', class_='title_champ_c title_champ_c1'):
                tmp += i.text.strip()+','
            list_counter.append(tmp[:-1])
            #be_counter
            tmp = ""
            for i in be_counter.find_all('span', class_='title_champ_c title_champ_c1'):
                tmp += i.text.strip()+','
            list_becounter.append(tmp[:-1])
            #combine
            tmp = ""
            for i in combine_with.find_all('span', class_='title_champ_c title_champ_c1'):
                tmp += i.text.strip()+','
            list_combine.append(tmp[:-1])
            dem += 1
            list_champ.append(name_champ)
            # break
        except:
            list_champ_false.append(name_champ)
    submission = pd.DataFrame({                                            
            "champion": list_champ,  "counter": list_counter, 'be_counter': list_becounter , 'combine_with': list_combine
        })
    submission.to_csv('counter.csv')
    f = open("/home/vanhocvp/Code/AI/NLP/API/Crawl_data/champ_fall_counter.txt", "w")
    for i in list_champ_false:
        f.write(i + '\n')
    f.close()
    print ("done")
def get_introduce():
    list_champ_introduce = []
    list_content = []
    json_kq = {}
    response = requests.get('https://lienminh.garena.vn/game-info/champions/')
    soup = BeautifulSoup(response.content, "html.parser")
    champions  = soup.findAll('span', class_ = 'content-border')
    dem = 1
    count = len(champions)
    for champion in champions:
        link = 'https://lienminh.garena.vn/' + champion.a['href']
        res = requests.get(link)
        soup1 = BeautifulSoup(res.content, "html.parser")
        name_champ = soup1.find('div', class_='default-2-3')
        name_champ = name_champ.h3.text.lower()
        print ("{}/{} : {}".format(dem,count, name_champ))
        # content  = soup1.findAll('div', class_= 'gs-container')[-1]
        # content  = content.find('div', class_= 'default-1-2').text.strip()
        # json_kq[name_champ] = content
        list_champ_introduce.append(name_champ)
        dem += 1
    f = open("/home/vanhocvp/Code/AI/NLP/API/Crawl_data/champ_introduce.txt", "w")
    for i in list_champ_introduce:
        f.write(i + '\n')
    f.close()
    #     if  dem == 3: break
    #     # break
    # print (json_kq)   
    # with open('introduce.json', 'w') as fp:
    #     json.dump(json_kq, fp)
def get_howtoplay():
    list_champ_false = []
    response = requests.get("https://skmoba.com/champion")
    soup = BeautifulSoup(response.content, "html.parser")
    champions = soup.findAll('div', class_="col-lg-2 col-md-2 col-sm-2 col-xs-4 list_champ_home mb15")
    dem = 1
    for champion in champions:
        link = champion.find('a').attrs["href"]
        name_champ = link.split('/')[-1]
        print ("{}/{} : {}".format(dem,len(champions), name_champ))
        link = 'https://skmoba.com/champions/huong-dan-bang-ngoc-len-do-sett'
        res = requests.get(link)
        soup1 = BeautifulSoup(res.content, "html.parser")
        content = soup1
        # x = content.split('Cách chơi Sett')[-1]
        print ((soup1.split('a')))
        # x  = soup1.findAll('h2')
        # for i in x:
        #     if (re.search('Cách chơi', i.text)) != None:
        #         print (i)
        
        break
        dem += 1   
    # f = open("/home/vanhocvp/Code/AI/NLP/API/Crawl_data/up_skill/champ_fall.txt", "w")
    # for i in list_champ_false:
    #     f.write(i + '\n')
    # f.close()
    print ("done")
def get_how_to_use_skill():
    list_champ_introduce = []
    list_content = []
    json_kq = {}
    response = requests.get('https://lienminh.garena.vn/game-info/champions/')
    soup = BeautifulSoup(response.content, "html.parser")
    champions  = soup.findAll('span', class_ = 'content-border')
    dem = 1
    count = len(champions)
    for champion in champions:
        link = 'https://lienminh.garena.vn/' + champion.a['href']
        res = requests.get(link)
        soup1 = BeautifulSoup(res.content, "html.parser")
        name_champ = soup1.find('div', class_='default-2-3')
        name_champ = name_champ.h3.text.lower()
        print ("{}/{} : {}".format(dem,count, name_champ))
        content  = soup1.findAll('p', class_= 'spell-description')
        list_skill = []
        tmp = {}
        for i in content:
            list_skill.append(i.text)
        nt, q, w, e, r = list_skill
        tmp['noi_tai']  = nt
        tmp['q'] = q
        tmp['w'] = w
        tmp['e'] = e
        tmp['r'] = r 
        json_kq[name_champ] = tmp

        list_champ_introduce.append(name_champ)
        dem += 1
    f = open("/home/vanhocvp/Code/AI/NLP/API/Crawl_data/champ_use_skill.txt", "w")
    for i in list_champ_introduce:
        f.write(i + '\n')
    f.close()
    with open('how_to_use_skill.json', 'w') as fp:
        json.dump(json_kq, fp)
def get_socket():
    list_champ_false = []
    list_item = {}
    build_item = {}
    response = requests.get("https://tranvanthong.com/tuong-lien-minh/")
    soup = BeautifulSoup(response.content, "html.parser")
    champions = soup.findAll('figcaption', class_="wp-caption-text gallery-caption")
    dem = 1
    for champion in champions:
        link = champion.find('a').attrs["href"]
        name_champ = link.split('/')[-2]
        if name_champ in build_item.keys():
            continue
        print ("{}/{} dd: {}".format(dem,len(champions), name_champ))
        res = requests.get(link)
        soup1 = BeautifulSoup(res.content, "html.parser")
        try:
            id =  soup1.find('article').attrs["id"].split('-')[-1]
            all_item = soup1.findAll('figure', class_='wp-block-image size-large')[1]
            # print (all_item)
            tmp = [] #store all item to save to dict
            # for i in all_item:
            #     item = i.text.strip()
            #     # print (item)
            path_img = '/home/vanhocvp/Code/AI/NLP/API/Crawl_data/bang_ngoc/' + name_champ + '.png' 
            print (all_item.img['src'])
            with open(path_img,"wb") as f:
                            f.write(requests.get(all_item.img['src']).content)
            #     break
            # build_item[name_champ] = tmp
            # print (list_item)
            # print (build_item)
            dem += 1   
        except:
            list_champ_false.append(name_champ)
        
        
        # break
    f = open("/home/vanhocvp/Code/AI/NLP/API/Crawl_data/champ_fall_socket.txt", "w")
    for i in list_champ_false:
        f.write(i + '\n')
    f.close()
    # with open('build_item.csv', 'w') as f:
    #         for key in build_item.keys():
    #             f.write("%s, %s\n" % (key, build_item[key]))
    # with open('key_item.csv', 'w') as f:
    #         for key in list_item.keys():
    #             f.write("%s, %s\n" % (key, list_item[key]))
    # print ("done")
get_socket()