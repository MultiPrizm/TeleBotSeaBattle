import random
import time
import copy

bot_ = None

def init(arg):
    global bot_
    bot_ = arg


LineDict = {}

GamesList = []

IndexDict = {}

Conections = []

ConfiShipDictH = {
    1:[[0, 0], [-1, 0],[-1, -1],[1, 0],[1, 1],[0, -1],[1, -1],[-1, 1],[0, 1],],
    2:[[2, 0],[2, 1],[2, -1],],
    3:[[3, 0],[3, 1],[3, -1],],
    4:[[4, 0],[4, 1],[4, -1],]
}

ConfiShipDictV = {
    1:[[-1, 0],[-1, -1],[1, 0],[1, 1],[0, -1],[1, -1],[-1, 1],[0, 1],],
    2:[[0, 2],[-1, 2],[1, 2],],
    3:[[0, 3],[-1, 3],[1, 3],],
    4:[[0, 4],[-1, 4],[1, 4],],
}

def foo():

    while True:
        print("черга-", len(LineDict))
        print("активних ігор-", len(GamesList))
        print("сonections-", len(Conections))
        time.sleep(7)

class Game():
    def __init__(self, first_pl_id, first_pl_name, second_pl_id, second_pl_name):

        self.first_pl_id = first_pl_id
        self.first_pl_name = first_pl_name

        self.second_pl_id = second_pl_id
        self.second_pl_name = second_pl_name

        self.GrafAsset = "⬜⬛⚫❌"

        self.first_pl_map, self.first_pl_map_conf = self.random_map()
        self.second_pl_map, self.second_pl_map_conf = self.random_map()

        self.first_pl_mes = None
        self.second_pl_mes = None

        self.first_pl_out = "📡Капітан ми наштовхнулись на ворожий флот"+"%"+"‼️Твій противник:" + str(self.second_pl_name)+"%"+self.map_to_graf(self.first_pl_map, self.second_pl_map)+"%"+"‼️Ти ходиш першим"
        self.second_pl_out = "📡Капітан ми наштовхнулись на ворожий флот"+"%"+"‼️Твій противник:" + str(self.first_pl_name)+"%"+self.map_to_graf(self.second_pl_map, self.first_pl_map)+"%‼️"+str(self.first_pl_name)+" ходить першим"

        self.status_f = True
        self.status_s = False

        self.CodeDict = {
            "a":0,
            "b":1,
            "c":2,
            "d":3,
            "e":4,
            "f":5,
            "g":6,
            "h":7,
            "i":8,
            "j":9
        }
        
        self.game = True
        self.end = False

        self.end_f = True
        self.end_s = True

        self.flag = False

        self.buffer_mess_f = ""
        self.buffer_mess_s = ""
    
    def update(self):
        if self.first_pl_mes:

            if len(self.first_pl_mes) == 3:
                self.Fire(9, self.CodeDict[self.first_pl_mes[0]], self.second_pl_map, self.second_pl_map_conf, 1)
            else:
                self.Fire(int(self.first_pl_mes[1])-1, self.CodeDict[self.first_pl_mes[0]], self.second_pl_map, self.second_pl_map_conf, 1)

            self.first_pl_out += self.map_to_graf(self.first_pl_map, self.second_pl_map)+"%"+self.buffer_mess_f
            self.second_pl_out += self.map_to_graf(self.second_pl_map, self.first_pl_map)+"%"+self.buffer_mess_s +"%"+ "📡Ваша черга"

            self.status_f = False
            self.status_s = True
            self.first_pl_mes = None

        if self.second_pl_mes:

            if len(self.second_pl_mes) == 3:
                self.Fire(9, self.CodeDict[self.second_pl_mes[0]], self.first_pl_map, self.first_pl_map_conf, 2)
            else:
                self.Fire(int(self.second_pl_mes[1])-1, self.CodeDict[self.second_pl_mes[0]], self.first_pl_map, self.first_pl_map_conf, 2)

            self.first_pl_out += self.map_to_graf(self.first_pl_map, self.second_pl_map)+"%"+self.buffer_mess_f +"%"+ "📡Ваша черга"
            self.second_pl_out += self.map_to_graf(self.second_pl_map, self.first_pl_map)+"%"+self.buffer_mess_s


            self.status_f = True
            self.status_s = False
            self.second_pl_mes = None
        
        if self.end and not self.first_pl_out and not self.second_pl_out:
            self.game = False
        
        self.flag = True

        for i in self.first_pl_map:
            for s in i:
                if s == 1:
                    self.flag = False
        
        if self.flag:
            self.first_pl_out = "📡Наший флот потерпів поразку\nМи ще повернемося\n\nПерможець:" + str(self.second_pl_name)
            self.second_pl_out = "📡Ворожий флот розгромлений, це перемога"
        
            self.end = True
        

        self.flag = True

        for i in self.second_pl_map:
            for s in i:
                if s == 1:
                    self.flag = False
        
        if self.flag:
            self.first_pl_out = "📡Ворожий флот розгромлений, це перемога"
            self.second_pl_out = "📡Наший флот потерпів поразку\nМи ще повернемося\n\nПерможець:" + str(self.first_pl_name)

            self.end = True
    
    def random_map(self):
        map = []
        ShipDict = {
            1:[],
            2:[],
            3:[],
            4:[],
        }

        for i in range(10):
            buffer = []

            for s in range(10):
                buffer.append(0)

            map.append(buffer)
        
        for i in range(4):


            for s in range(1+i):
                CheckConf = []
                BufferList = []

                o = random.randint(0, 1)

                for t in range(4-i):

                    if o==1:
                        CheckConf+=ConfiShipDictV[t+1]
                    else:
                        CheckConf+=ConfiShipDictH[t+1]
                
                flag = True

                while flag:
                    flag = False
    
                    x = random.randint(0, 6+i)
                    y = random.randint(0, 6+i)

                    for t in CheckConf:

                        if x+t[0] <= 9 and y+t[1] <= 9:
                            if map[x+t[0]][y+t[1]] == 1:
                                flag = True
                                break
                
                for t in range(4-i):

                    if o==1:
                        map[x][y+t] = 1
                        BufferList.append([x, y+t])
                    else:
                        map[x+t][y] = 1
                        BufferList.append([x+t, y])
                
                BufferList.append(o)
                
                ShipDict[4-i].append(BufferList)
        
        return map, ShipDict
    
    def map_to_graf(self, map1, map2):

        grafL = "you    1    2    3    4     5    6    7    8    9   10\n"
        grafL2 = "enem    1    2    3    4     5    6    7    8    9   10\n"

        StrL = ["||A ","||B ","||C ","||D ","||E  ","||F  ","||G ","||H ","||I   ","||J   "]

        y=0

        for i in range(10):

            grafL += StrL[y]
            for s in range(10):

                if map1[s][y] == 0:
                    grafL += self.GrafAsset[0]
                elif map1[s][y] == 1:
                    grafL += self.GrafAsset[1]
                elif map1[s][y] == 2:
                    grafL += self.GrafAsset[2]
                elif map1[s][y] == 3:
                    grafL += self.GrafAsset[3]
            
            grafL2 += StrL[y]
            
            for s in range(10):

                if map2[s][y] == 0:
                    grafL2 += self.GrafAsset[0]
                elif map2[s][y] == 1:
                    grafL2 += self.GrafAsset[0]
                elif map2[s][y] == 2:
                    grafL2 += self.GrafAsset[2]
                elif map2[s][y] == 3:
                    grafL2 += self.GrafAsset[3]
            
            y +=1
            grafL += "\n"
            grafL2 += "\n"
        
        return grafL2 + "%" + grafL
        
    def put_mess(self, id, mess):

        if id == self.first_pl_id:
            if not self.first_pl_mes:
                self.first_pl_mes = mess

        elif id == self.second_pl_id:
            if not self.second_pl_mes:
                self.second_pl_mes = mess
    
    def out(self, id):
        if id == self.first_pl_id:
            buffer = copy.copy(self.first_pl_out)
            self.first_pl_out = ""
            return buffer
        
        elif id == self.second_pl_id:
            buffer = copy.copy(self.second_pl_out)
            self.second_pl_out = ""
            return buffer
    
    def check_status(self, id):
        if id == self.first_pl_id:
            return self.status_f
        
        elif id == self.second_pl_id:
            return self.status_s
    
    def Fire(self, x, y, map, conf, player):

        self.buffer_mess_f = ""
        self.buffer_mess_s = ""
        
        if map[x][y] == 0:
            map[x][y] = 2

            if player == 1:
                self.buffer_mess_f = "📡Промах"
                self.buffer_mess_s = "📡Противник помахнувся(" + str(self.first_pl_mes) + ")"
            elif player == 2:
                self.buffer_mess_f = "📡Противник помахнувся(" + str(self.second_pl_mes) + ")"
                self.buffer_mess_s = "📡Промах"

        elif map[x][y] == 1:
            map[x][y] = 3

            if player == 1:
                self.buffer_mess_f = "📡Точно в ціль"
                self.buffer_mess_s = "📡Прильот по " + str(self.first_pl_mes)
            elif player == 2:
                self.buffer_mess_f = "📡Прильот по " + str(self.second_pl_mes)
                self.buffer_mess_s = "📡Точно в ціль"
        
        for i in range(4):


            for s in conf[1+i]:

                LenLict = len(s)-1
                DestroyedTail = 0
                
                for t in s:

                    if type(t) == type([]):
                        if map[t[0]][t[1]] == 3:

                            DestroyedTail += 1
                
                if LenLict == DestroyedTail:

                    CheckConf = []
                    o = s[len(s)-1]

                    x = s[0][0]
                    y = s[0][1]

                    for t in range(1+i):

                        if o==1:
                            CheckConf+=ConfiShipDictV[t+1]
                        else:
                            CheckConf+=ConfiShipDictH[t+1]

                    for t in CheckConf:
                        
                        if x+t[0] < 10 and x+t[0] >=0 and y+t[1] < 10 and y+t[1] >= 0:
                            if map[x+t[0]][y+t[1]] == 0:
                                map[x+t[0]][y+t[1]] = 2
                    
                    if 1+i == 1:
                        if player == 1:
                            self.buffer_mess_f += "%📡Ви потопили ворожий катер"
                            self.buffer_mess_s += "%📡Противник потопив ваший катер"
                        elif player == 2:
                            self.buffer_mess_f += "%📡Противник потопив ваший катер"
                            self.buffer_mess_s += "%📡Ви потопили ворожий катер"
                    elif 1+i == 2:
                        if player == 1:
                            self.buffer_mess_f += "%📡Ви потопили ворожий фрегат"
                            self.buffer_mess_s += "%📡Противник потопив ваший фрегат"
                        elif player == 2:
                            self.buffer_mess_f += "%📡Противник потопив ваший фрегат"
                            self.buffer_mess_s += "%📡Ви потопили ворожий фрегат"
                    elif 1+i == 3:
                        if player == 1:
                            self.buffer_mess_f += "%📡Ви потопили ворожий крейсер"
                            self.buffer_mess_s += "%📡Противник потопив ваший крейсер"
                        elif player == 2:
                            self.buffer_mess_f += "%📡Противник потопив ваший крейсер"
                            self.buffer_mess_s += "%📡Ви потопили ворожий крейсер"
                    elif 1+i == 4:
                        if player == 1:
                            self.buffer_mess_f += "%📡Ви потопили ворожий дредноут"
                            self.buffer_mess_s += "%📡Противник потопив ваший дредноут"
                        elif player == 2:
                            self.buffer_mess_f += "%📡Противник потопив ваший дредноут"
                            self.buffer_mess_s += "%📡Ви потопили ворожий дредноут"
                    
                    if player == 1:
                        self.second_pl_map_conf[1+i].remove(s)
                    elif player == 2:
                        self.first_pl_map_conf[1+i].remove(s)
    
    def exit(self, id):

        if id == self.first_pl_id:
            self.first_pl_out = "📡Ми відступаємо але це ще не все\nМи повернемося"
            self.second_pl_out = "📡Схоже " + str(self.first_pl_name) + " відступає%Ви спостерігаєте як ворожий флот повільно розтає в тумані"
        
        elif id == self.second_pl_id:
            self.first_pl_out = "📡Схоже " + str(self.first_pl_name) + " відступає%Ви спостерігаєте як ворожий флот повільно розтає в тумані"
            self.second_pl_out = "📡Ми відступаємо але це ще не все\nМи повернемося"
        
        self.end = True


def selection():
    while True:

        if len(LineDict) >= 2:
            keys = list(LineDict.keys())

            buffer = Game(LineDict[keys[0]], keys[0], LineDict[keys[1]], keys[1])

            GamesList.append(buffer)

            IndexDict[LineDict[keys[0]]] = buffer
            IndexDict[LineDict[keys[1]]] = buffer

            del LineDict[keys[0]], LineDict[keys[1]]

def Processing():
    while True:

        for i in GamesList:
            i.update()

            if i.end:

                if not i.first_pl_out and i.end_f:
                    del IndexDict[i.first_pl_id]
                    i.end_f = False
                if not i.second_pl_out and i.end_s:
                    del IndexDict[i.second_pl_id]
                    i.end_s = False

            if not i.game:
                GamesList.remove(i)


#info - туторіал
#exit - ❌здатися
#go - ⚓розпочати гру
#radio - 📡запросити зведення з фронту
#💪💥🛑🚨⚓🕖❌🚀🗿📡🖥