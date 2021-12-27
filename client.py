import socket
import threading
from tkinter import *
from tkinter import ttk
from functools import partial
import json
import sys

def sendAMessage(message):
    global client
    ## Ta sẽ đi theo cấu trúc gửi tin bên client
    message = message.encode('utf-8')
    messageSize = len(message)
    messageSize_send = str(messageSize).encode('utf8')
    messageSize_send += b' ' * (1024 - len(messageSize_send))
    client.send(messageSize_send)
    client.send(message)


sizeOfLong = 64
portGate = 5051 ## Port không được nằm trong khoảng 0<= PORT <= 1024 vì đây là cổng cho các giao thức có sẵn trên máy


global isInputIP_Failed ## Biến này để check rằng đã bao giờ nhập IP sai chưa ?
isInputIP_Failed = False

def receiveMessage(connection):
    messageSize = connection.recv(1024).decode("utf-8")
    message = ""
    if messageSize != '':
        messageSize = int(messageSize)
        message = connection.recv(messageSize).decode("utf-8")
    return message


currency = [] ##option chosing Array
currency_sell = []
currency_buy = []
isExchange = False


def appearComboBox():
    ##create combo boxư
    global comboBox
    comboBox = ttk.Combobox(tk,value = currency)
    comboBox.current(0)
    comboBox.place(x =275.0 , y =445.0 )

def getTheEquivalentSell(currency_string):
    for i in range(0,len(currency)):
        if currency[i] == currency_string:
            return currency_sell[i]/1000

def getTheEquivalentBuy(currency_string):
    for i in range(0,len(currency)):
        if currency[i] == currency_string:
            return currency_buy[i]/1000

global messageLabel1,messageLabel2
global messageLabel1_stringVar,messageLabel2_stringVar

def exchange():
    global comboBox
    global isExchange
    global messageLabel1,messageLabel2
    global messageLabel1_stringVar,messageLabel2_stringVar
    currency_type = comboBox.get()
    sell = getTheEquivalentSell(currency_type)
    buy = getTheEquivalentBuy(currency_type)
    originalMoney = int(currencyEnter.get())
    exchangeMoney_sell = sell*originalMoney
    exchangeMoney_buy = buy*originalMoney
    message_1 = "Số tiền quy đổi sang "+currency_type+ " nếu mua: "+ str(exchangeMoney_buy) +" nghìn đồng"
    message_2 = "Số tiền quy đổi sang "+currency_type+ " nếu bán: "+ str(exchangeMoney_sell)+" nghìn đồng"


    if isExchange == False:
        messageLabel2_stringVar = StringVar()
        messageLabel1_stringVar = StringVar()
        messageLabel1_stringVar.set(message_1)
        messageLabel2_stringVar.set(message_2)
        messageLabel1 = Label(tk,textvariable = messageLabel1_stringVar)
        messageLabel2 = Label(tk,textvariable = messageLabel2_stringVar)
        messageLabel1.place(x= 275.0, y = 540.0)
        messageLabel2.place(x= 275.0, y = 565.0)
        isExchange = True
    else:
        messageLabel1_stringVar.set(message_1)
        messageLabel2_stringVar.set(message_2)


isTreeAppear = False




def appearExchange():
    chooseCurrency_label = Label(tk,text ="Chọn loại tiền tệ muốn quy đổi")
    chooseCurrency_label.place(x= 275.0, y = 420.0)
    appearComboBox()
    chooseQuantity_label = Label(tk,text ="Nhập số lượng bạn muốn quy đổi ( theo đơn vị nghìn VNĐ)")
    chooseQuantity_entry = Entry(tk,textvariable = currencyEnter)
    chooseQuantity_label.place(x= 175.0, y = 470.0)
    chooseQuantity_entry.place(x= 275.0, y = 500.0)
    exchangeCurrency_button = Button(tk,text = "QUY ĐỔI",command = exchange)
    exchangeCurrency_button.place(x= 300.0, y = 515.0)

def appearMyTree(result):
    global isTreeAppear,myTree
    myTree = ttk.Treeview(tk)
    countResult = 1
    myTree['columns'] = ("Buy Cash","Buy Transfer","Currency","Sell")
    myTree.column("#0", width = 120, minwidth = 30)
    myTree.column("Buy Cash", anchor = CENTER, width = 120)
    myTree.column("Buy Transfer", anchor = CENTER, width = 120)
    myTree.column("Currency", anchor = CENTER, width = 120)
    myTree.column("Sell", anchor = CENTER, width = 120)

    ##Create Headings
    myTree.heading("#0", text = "Index", anchor = CENTER)
    myTree.heading("Buy Cash", text = "Buy Cash", anchor = CENTER)
    myTree.heading("Buy Transfer", text = "Buy Transfer", anchor = CENTER)
    myTree.heading("Currency", text = "Currency", anchor = CENTER)
    myTree.heading("Sell", text = "Sell", anchor = CENTER)
    isTreeAppear = True
    for i in result:
        myTree.insert(parent = '', index = 'end', iid=None, text = str(countResult), values = (i['buy_cash'],i['buy_transfer'],i['currency'],i['sell']))
        currency.append(i['currency'])
        currency_buy.append(i['buy_cash'])
        currency_sell.append(i['sell'])
        countResult += 1
    myTree.place(x = 50.0, y = 180.0 )

def updateTree(myTree,result):
    myTree.place_forget()
    myTree.destroy()
    appearMyTree(result)


def getData():
    sendAMessage("DATA_REQUEST")
    data = receiveMessage(client) ## Lấy dữ liệu ở dạng chuỗi
    data_json = json.loads(data) ## ta chuyển chuỗi sang object json
    result = data_json['results']
    ##Tkinter Treeview
    global isTreeAppear,myTree
    if isTreeAppear == False:
        appearMyTree(result)
    else:
        updateTree(myTree,result)

    appearExchange()



def Exit():
    try:
        sendAMessage("EXIT")
    except:
        pass ## Nếu như không thể sendMessage thì bỏ qua luôn ( tức là trường hợp server đã tắt)
    global client
    client.close()
    tk.destroy()
    sys.exit()

def userGUI():
    ##Gắn Button "Lấy dữ liệu"
    buttonGetData_image = PhotoImage(file = "assest/Client/user/button_1.png")
    buttonGetData = Button(tk,image = buttonGetData_image, borderwidth = 0,
                                highlightthickness =0, relief = "flat", command = getData)
    buttonGetData.image = buttonGetData_image
    buttonGetData.place(x=54.0,y=89.0,width=191.0,height=72.0)

    buttonExit_image = PhotoImage(file = "assest/Client/user/button_2.png")
    buttonExit = Button(tk,image = buttonExit_image, borderwidth = 0,
                                highlightthickness =0, relief = "flat",command = Exit)
    buttonExit.image = buttonExit_image
    buttonExit.place(x=433.0,y=89.0,width=191.0,height=72.0)




def hideLoginFrames():
    global usernameEntry_image_label,usernameEntry,passwordEntry_image_label,passwordEntry,loginButton
    global isLoginError
    usernameEntry_image_label.place_forget()
    usernameEntry.place_forget()
    passwordEntry_image_label.place_forget()
    passwordEntry.place_forget()
    loginButton.place_forget()
    if isLoginError:
        loginError_label.place_forget()
    userBackground = PhotoImage(file = "assest/Client/user/image_1.png")
    Client_text_label.configure(image = userBackground)
    Client_text_label.photo_ref = userBackground

isLoginError = False
def verifyLogin(username,password):
    ##Send message to server that we will verify Login
    ##LOGIN_REQUEST => MESSAGE
    global isLoginError
    global loginError_label
    username = str(username.get())
    password = str(password.get())
    sendAMessage("LOGIN_REQUEST")
    sendAMessage(username)
    sendAMessage(password)
    message = receiveMessage(client)
    if message == "VALID":
        hideLoginFrames()
        userGUI()
    elif message == "INVALID":
        if  isLoginError == False:
            isLoginError = True
            loginError_label = Label(tk,bg = "#81BFD3",text = "Tài khoản không tồn tại, xin đăng nhập lại")
            loginError_label.place(x= 230.0, y = 475.0)
        else:
            pass


def hideInputIP_Frames():
    global isInputIP_Failed
    global inputIP_failed
    inputIP_entry.place_forget()
    inputIP_button.place_forget()
    inputIP_entry_label.place_forget()
    if isInputIP_Failed:
        inputIP_failed.destroy()
    registerBackground = PhotoImage(file = "assest/Client/register/registerbackground.png")
    Client_text_label.configure(image = registerBackground)
    Client_text_label.photo_ref = registerBackground


def loginForm():
    global usernameEntry_image_label,usernameEntry,passwordEntry_image_label,passwordEntry,loginButton

    ##Load ảnh cho Entry username
    username = StringVar()
    usernameEntry_image = PhotoImage(file = "assest/Client/entry_1.png")
    usernameEntry_image_label = Label(tk,image = usernameEntry_image)
    usernameEntry_image_label.image = usernameEntry_image ## Keep Reference
    usernameEntry = Entry(tk,bd =0, bg="#81BFD3", highlightthickness = 0  ,textvariable = username)
    usernameEntry_image_label.place(x= 300.0,y=260)
    usernameEntry.place(x=311.99999999999994,y=262.0,width=326.0,height=45.0)

    ##load ảnh cho Entry Password
    password = StringVar()
    passwordEntry_image = PhotoImage(file = "assest/Client/register/entry_2.png")
    passwordEntry_image_label = Label(tk,image = passwordEntry_image)
    passwordEntry_image_label.image = passwordEntry_image
    passwordEntry_image_label.place(x=300.0,y=328.5)
    passwordEntry = Entry(tk,bd =0, bg="#81BFD3", highlightthickness = 0 ,textvariable=password, show='*')
    passwordEntry.place(x=312.0,y=330.0,width=326.0,height=45.0)

    ##load ảnh cho Button đăng nhập
    loginButton_image = PhotoImage(file = "assest/Client/register/register_button.png")
    loginButton = Button(tk,image = loginButton_image, borderwidth=0, highlightthickness=0,
                                            command = partial(verifyLogin,username,password))
    loginButton.image = loginButton_image
    loginButton.place(x=204.0,y=421.0,width=295.0,height=50.0)

def connectSocket(localIP,portGate):
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(1)
    addr = (localIP,portGate)
    client.connect(addr)
    print("Connected")


def verifyIP(inputIP):
    global isInputIP_Failed
    global inputIP_failed
    try:
        connectSocket(inputIP.get(),5051) ## Chỗ này nếu không kết nối được sẽ quăng xuống except
        hideInputIP_Frames()
        loginForm()
    except:
        if isInputIP_Failed == False:
            isInputIP_Failed = True
            inputIP_failed = Label(tk,bg = "#FFFFFF",text = "IP không hợp lệ")
            inputIP_failed.place(x=315,y=420.0)
        else:
            pass


## MAIN starts here
check = localIP = socket.gethostbyname(socket.gethostname())
tk = Tk()
tk.configure(bg = "#FFFFFF")
tk.geometry("705x600")
tk.resizable(False,False)
tk.title("Client")

##Load background
backgroundImage = PhotoImage(file = "assest/Client/image_1.png")
Client_text_label = Label(tk,image = backgroundImage)
Client_text_label.place(x =0, y= 0)

##Load Entry Nhập IP
inputIP = StringVar()
inputIP_entry_image = PhotoImage(file = "assest/Client/entry_1.png")
inputIP_entry_label = Label(tk,image = inputIP_entry_image)
inputIP_entry_label.place(x= 307, y= 257)
inputIP_entry = Entry(tk,bd =0,bg="#81BFD3", highlightthickness=0, textvariable = inputIP)
inputIP_entry.place(x=311.99999999999994,y=262.0,width=326.0,height=40.0)


##Load Button "Kết Nối
verifyIP = partial(verifyIP,inputIP) ## Đóng gói lại một hàm thành một object
inputIP_button_image = PhotoImage(file = "assest/Client/button_1.png")
inputIP_button = Button(tk,image = inputIP_button_image,borderwidth=0,
                          highlightthickness=0,command = verifyIP)

inputIP_button.place(x=204.99999999999994,y=368.0,width=295.0,height=50.0)



currencyEnter = StringVar()

tk.mainloop()
