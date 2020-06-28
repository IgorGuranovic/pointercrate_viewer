import bs4, re, time
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd
from tkinter import Button, Label, Entry, Tk, E, W
from PIL import ImageTk, Image
from helium import find_all, start_chrome, kill_browser, press, click, write, S, END

#Creates a Player object, which has "name" and "demons" attributes
class Player:
    def __init__(self, name):
        demonlist = Demonlist()
        self.name = name
        self.demons = getDemons(self.name)
        for demon in demonlist:
            if demon in self.demons:
                color = "green"
            else:
                color = "red"
        master1 = Tk()
        Label(master1, text=self.name, font="times 36").grid(row=0, column=0)
        for x in range(15):
            for y in range(10):
                number = x*10+y
                if demonlist[number] in self.demons:
                    color = "green"
                else:
                    color = "red"
                Label(master1, text=str(demonlist[number]), fg=color, font="times 12").grid(row=(x+1), column=(y+1))
        master1.mainloop()

#Returns the list of the current top 150 demons
def Demonlist ():
    demonlist = []
    uClient = uReq('https://pointercrate.com/demonlist/')
    read_page = uClient.read()
    uClient.close()
    parsed_list = soup(read_page, "html.parser")
    for x in range(150):
        level = str(parsed_list.find_all("a",{"href":"/demonlist/%d" % (x+1)}))
        start = [m.start() for m in re.finditer("-", level)][1]
        level = level[(start+2):(-5)]
        if [m.start() for m in re.finditer(" by ", level)] != []:
            end = [m.start() for m in re.finditer(" by ", level)][0]
            level = level[0:end]
        demonlist.append(level)
    return demonlist

#Inputs a player name, returns the list of top 150 demons he/she completed
def getDemons (name):
    list1 = []
    list0 = []
    start_chrome('https://pointercrate.com/demonlist/')
    press(END)
    click('Open the stats viewer!')
    write(name, into='Enter to search...')
    click(name)
    time.sleep(1)
    for x in range(75):
        counter = x + 1
        mainlist = find_all(S('//*[@id="beaten"]/b[%d]/a' % (counter)))
        extendedlist = find_all(S('//*[@id="beaten"]/span[%d]/a' % (counter)))
        verifications_main = find_all(S('//*[@id="verified"]/b[%d]/a' % (counter)))
        verifications_extended = find_all(S('//*[@id="verified"]/span[%d]/a' % (counter)))
        list0.append(mainlist)
        list0.append(extendedlist)
        list0.append(verifications_main)
        list0.append(verifications_extended)
    list0 = [element for element in list0 if element != []]
    for demon in list0:
        demon = str(demon)
        start = [m.start() for m in re.finditer(">", demon)][0]
        end = [m.start() for m in re.finditer("<", demon)][1]
        demon = demon[(start+1):end]
        list1.append(demon)
    kill_browser()
    return list1

#Creates a Player object
def init():
    if e1.get() != '':
        Player(e1.get())
        master.destroy()

#GUI Generation
master = Tk()
im1 = Image.open('images/pointercrate.png')
im1 = im1.resize((334,120), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(im1)
Label(master, image=image1).grid(row=0)
Label(master, text=" Player Display", font="times 72").grid(row=0, column=1, sticky=W)
Label(master, text="Player:", font="times 48").grid(row=1, sticky=E)
e1 = Entry(master, font="times 48", width=20)
e1.grid(row=1, column=1)
Button(master, text='Enter', font="times 48", command=init).grid(row=2, column=0, pady=4, sticky=E)
Button(master, text='Cancel', font="times 48", command=master.destroy).grid(row=2, column=1, pady=4, sticky=W)
master.mainloop()