import tkinter as tk
from functools import partial


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.player = 0
        

    def create_widgets(self):
        #盤面作成
        self.buttons = []
        for x in range(8):
            yButtons = []
            for y in range(8):
                button = tk.Button(
                                   height=3,
                                   width=7,
                                   compound="center")
                button["command"] = partial(self.click,x,y)
                button.place(x=5+x*60,y=5+y*60)
                yButtons.append(button)
            self.buttons.append(yButtons)
        
        #初期値
        self.buttons[3][3]["text"] = "●"
        self.buttons[3][4]["text"] = "○"
        self.buttons[4][3]["text"] = "○"
        self.buttons[4][4]["text"] = "●"

        self.label = tk.Label(root, text="黒のターンです。")
        self.label.place(x=550, y=250, width=120, height=50)
        self.blacknum = tk.Label(root, text="黒２個")
        self.blacknum.place(x=550, y=400, width=120, height=50)
        self.whitenum = tk.Label(root, text="白２個")
        self.whitenum.place(x=550, y=450, width=120, height=50)

        



    def click(self,x,y):
        put_ok = False              #駒を置けるかのフラグ
        print("othero", x, y)

        #クリックした位置にすでに駒があったら何もせず抜ける
        if self.buttons[x][y]["text"] != "":
            return

        if self.player % 2 == 0:
            myMark = "●"
            othMark = "○" 
        else:
            myMark = "○"
            othMark = "●"   

        self.buttons[x][y]["text"] = myMark
        
        if checkUpper( self, x, y, myMark, othMark ) == True:
            put_ok = True
        if checkDown( self, x, y, myMark, othMark ) == True:
            put_ok = True
        if checkleft( self, x, y, myMark, othMark ) == True:
            put_ok = True
        if checkright( self, x, y, myMark, othMark ) == True:
            put_ok = True
        if checkupperright( self, x, y, myMark, othMark ) == True:
            put_ok = True
        if checkdownright( self, x, y, myMark, othMark ) == True:
            put_ok = True
        if checkupperleft( self, x, y, myMark, othMark ) == True:
            put_ok = True
        if checkdownleft( self, x, y, myMark, othMark ) == True:
            put_ok = True

        if put_ok == True:
            #駒が置けたら次のプレイヤーに交代
            self.player = self.player + 1
        else:
            #駒が置けなければ駒を消す
            self.buttons[x][y]["text"] = ""

        if self.player % 2 == 0:
            self.label["text"] = "黒のターンです。"
        else:
            self.label["text"] = "白のターンです。"
            
        counttip(self)
        judge(self)

#upper check
def checkUpper( self, x, y, myMark, othMark ):
    #相手のマークが続く回数をカウントする
    result = False
    count = 0
    findMyMark = False
    cy = y - 1
    while cy >= 0:
        if self.buttons[x][cy]["text"] == othMark:
            count = count + 1
        elif self.buttons[x][cy]["text"] == myMark:
            findMyMark = True
            break
        else:
            break
        cy = cy - 1

    #自分のマークを見つけた場合は、相手のマークを自分のマークに変える
    if findMyMark == True:
        cy = y - 1
        for ii in range(count):
            self.buttons[x][cy]["text"] = myMark
            cy = cy - 1
    #マークを変えたことを返す
    if (findMyMark == True) and (count != 0):
        result = True
    return result
  
 #down check
def checkDown( self, x, y, myMark, othMark ):
    #相手のマークが続く回数をカウントする
    result = False
    findMyMark = False
    count = 0
    cy = y + 1
    while cy <= 7:
        if self.buttons[x][cy]["text"] == othMark:
            count = count + 1
        elif self.buttons[x][cy]["text"] == myMark:
            findMyMark = True
            break
        else:
            break
        cy = cy + 1

    #自分のマークを見つけた場合は、相手のマークを自分のマークに変える
    if findMyMark == True:
        cy = y + 1
        for ii in range(count):
            self.buttons[x][cy]["text"] = myMark
            cy = cy + 1
    #マークを変えたことを返す
    if (findMyMark == True) and (count != 0):
        result = True
    return result
       
def checkleft( self, x, y, myMark, othMark ):
    #相手のマークが続く回数をカウントする
    result = False
    findMyMark = False
    count = 0
    cx = x - 1
    while cx >= 0:
        if self.buttons[cx][y]["text"] == othMark:
            count = count + 1
        elif self.buttons[cx][y]["text"] == myMark:
            findMyMark = True
            break
        else:
            break
        cx = cx - 1

    #自分のマークを見つけた場合は、相手のマークを自分のマークに変える
    if findMyMark == True:
        cx = x - 1
        for ii in range(count):
            self.buttons[cx][y]["text"] = myMark
            cx = cx - 1
    #マークを変えたことを返す
    if (findMyMark == True) and (count != 0):
        result = True
    return result

            
def checkright( self, x, y, myMark, othMark ):
    #相手のマークが続く回数をカウントする
    result = False
    findMyMark = False
    count = 0
    cx = x + 1
    while cx <= 7:
        if self.buttons[cx][y]["text"] == othMark:
            count = count + 1
        elif self.buttons[cx][y]["text"] == myMark:
            findMyMark = True
            break
        else:
            break
        cx = cx + 1

    #自分のマークを見つけた場合は、相手のマークを自分のマークに変える
    if findMyMark == True:
        cx = x + 1
        for ii in range(count):
            self.buttons[cx][y]["text"] = myMark
            cx = cx + 1
    #マークを変えたことを返す
    if (findMyMark == True) and (count != 0):
        result = True
    return result


def checkdownright( self, x, y, myMark, othMark ):
   #相手のマークが続く回数をカウントする
    result = False
    findMyMark = False
    count = 0
    cx = x - 1
    cy = y - 1
    while cx >= 0 and cy >= 0:
        if self.buttons[cx][cy]["text"] == othMark:
            count = count + 1
        elif self.buttons[cx][cy]["text"] == myMark:
            findMyMark = True
            break
        else:
            break
        cx = cx - 1
        cy = cy - 1

    #自分のマークを見つけた場合は、相手のマークを自分のマークに変える
    if findMyMark == True:
        cx = x - 1
        cy = y - 1
        for ii in range(count):
            self.buttons[cx][cy]["text"] = myMark
            cx = cx - 1
            cy = cy - 1
    #マークを変えたことを返す
    if (findMyMark == True) and (count != 0):
        result = True
    return result

            
def checkupperright( self, x, y, myMark, othMark ):
   #相手のマークが続く回数をカウントする
    result = False
    findMyMark = False
    count = 0
    cx = x + 1
    cy = y - 1
    while cx <= 7 and cy >= 0:
        if self.buttons[cx][cy]["text"] == othMark:
            count = count + 1
        elif self.buttons[cx][cy]["text"] == myMark:
            findMyMark = True
            break
        else:
            break
        cx = cx + 1
        cy = cy - 1

    #自分のマークを見つけた場合は、相手のマークを自分のマークに変える
    if findMyMark == True:
        cx = x + 1
        cy = y - 1
        for ii in range(count):
            self.buttons[cx][cy]["text"] = myMark
            cx = cx + 1
            cy = cy - 1
    #マークを変えたことを返す
    if (findMyMark == True) and (count != 0):
        result = True
    return result

            
def checkdownleft( self, x, y, myMark, othMark ):
   #相手のマークが続く回数をカウントする
    result = False
    findMyMark = False
    count = 0
    cx = x - 1
    cy = y + 1
    while cx >= 0 and cy <= 7:
        if self.buttons[cx][cy]["text"] == othMark:
            count = count + 1
        elif self.buttons[cx][cy]["text"] == myMark:
            findMyMark = True
            break
        else:
            break
        cx = cx - 1
        cy = cy + 1

    #自分のマークを見つけた場合は、相手のマークを自分のマークに変える
    if findMyMark == True:
        cx = x - 1
        cy = y + 1
        for ii in range(count):
            self.buttons[cx][cy]["text"] = myMark
            cx = cx - 1
            cy = cy + 1
    #マークを変えたことを返す
    if (findMyMark == True) and (count != 0):
        result = True
    return result

            
def checkupperleft( self, x, y, myMark, othMark ):
   #相手のマークが続く回数をカウントする
    result = False
    findMyMark = False
    count = 0
    cx = x + 1
    cy = y + 1
    while cx <= 7 and cy <= 7:
        if self.buttons[cx][cy]["text"] == othMark:
            count = count + 1
        elif self.buttons[cx][cy]["text"] == myMark:
            findMyMark = True
            break
        else:
            break
        cx = cx + 1
        cy = cy + 1

    #自分のマークを見つけた場合は、相手のマークを自分のマークに変える
    if findMyMark == True:
        cx = x + 1
        cy = y + 1
        for ii in range(count):
            self.buttons[cx][cy]["text"] = myMark
            cx = cx + 1
            cy = cy + 1
    #マークを変えたことを返す
    if (findMyMark == True) and (count != 0):
        result = True
    return result

#コマ数カウント
def counttip(self):
    global whitecount, blackcount
    whitecount = 0
    blackcount = 0
    for x in range(8):
        for y in range(8):
            if self.buttons[x][y]["text"] =="○":
                whitecount = whitecount + 1
            elif self.buttons[x][y]["text"] == "●":
                blackcount = blackcount + 1

    print( 'white = ' ,whitecount)
    print( 'black = ', blackcount)

    self.blacknum["text"] = "黒" + str(blackcount) + "個"
    self.whitenum["text"] = "白" + str(whitecount) + "個"

#勝敗決定
def judge(self):
    allcount = whitecount + blackcount
    if allcount == 64:
        if whitecount < blackcount:
            self.label["text"] = "黒の勝ちです。"
            
        elif whitecount > blackcount:
            self.label["text"] = "白の勝ちです。"

        else:
            self.label["text"] = "引き分けです。"
            
    print("all = ",allcount)  


root = tk.Tk()
root.title("othero")
root.geometry("800x600")
app = Application(master=root)
app.mainloop()
root.mainloop
