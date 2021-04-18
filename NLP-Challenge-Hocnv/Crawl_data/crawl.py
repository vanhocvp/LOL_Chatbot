import requests
from bs4 import BeautifulSoup

# response = requests.get("https://vi.wikipedia.org/wiki/Danh_s%C3%A1ch_t%C6%B0%E1%BB%9Bng_Li%C3%AAn_Minh_Huy%E1%BB%81n_Tho%E1%BA%A1i#Tham_kh%E1%BA%A3o")
# print (response)
# champions = []
# f = open('champions.txt', 'w')
# soup = BeautifulSoup(response.content, "html.parser")
# titles = soup.findAll('table', class_='wikitable')
# for i in titles:
#    cham = i.findAll('tr')[1:]
#    for j in cham:
#        name = j.findAll('td')[0].text.lower()
#        f.write(name)
#        champions.append(name)
# print (champions)
# f.close()
# print (len(champions))

f = open('champions.txt', "r")
reg = ""
for cham in f:
    # print (cham.split ('\n')[0])
    reg += cham.split ('\n')[0] + '|'
    # print (reg)
reg = reg[:-1]
import re, csv
k  = ['sylas', 'lee']
x = re.search(reg, "con  danh duoc  khong nhi")
print (x)
y = re.search('\sq\s|\sw\s|\se\s|\sr\s', 'conq nay len e truoc hay q truoc')
print (y)
def process_content(content): 
    content = content.lower()
    x = re.search(reg, content)
    
    if x != None:
        content = content.replace(x.group(), 'hero')
    print ('done')
    return content
content = []
intent = []              
with open('/home/vanhocvp/Code/AI/NLP/demo_submission_3 _1.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    print ('start')
    for row in reader:
        print (process_content(row[1]))
        content.append(process_content(row[1]))
        # intent.append(dict_intent[eval(row[2])['intent']])