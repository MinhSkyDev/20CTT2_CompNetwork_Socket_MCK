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


def getData():
    sendAMessage("DATA_REQUEST")
    data = receiveMessage(client) ## Lấy dữ liệu ở dạng chuỗi
    data_json = json.loads(data) ## ta chuyển chuỗi sang object json
    result = data_json['results']
    countResult = 1
    ##Tkinter Treeview
    myTree = ttk.Treeview(tk)
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
    for i in result:
        myTree.insert(parent = '', index = 'end', iid=None, text = str(countResult), values = (i['buy_cash'],i['buy_transfer'],i['currency'],i['sell']))
        countResult += 1

    myTree.pack(pady = 20)

def Exit():
    sendAMessage("EXIT")
    global client
    client.close()
    tk.destroy()
    sys.exit()

def userGUI():
    userGUI_welcome_label = Label(tk,text = "CHÀO MỪNG")
    getData_button = Button(tk,text = "Lấy dữ liệu", command = getData)
    exit_button = Button(tk,text = "Thoát", command = Exit)
    userGUI_welcome_label.pack()
    getData_button.pack()
    exit_button.pack()


def hideLoginFrames():
    global isLoginError ## Nhớ kiểm tra kỹ lại khúc này
    global loginText_label
    global usernameLabel
    global usernameEntry
    global passwordEntry
    global passwordLabel
    global loginButton
    global loginError_label
    loginText_label.pack_forget()
    usernameLabel.pack_forget()
    usernameEntry.pack_forget()
    passwordLabel.pack_forget()
    passwordEntry.pack_forget()
    loginButton.pack_forget()
    if isLoginError:
        loginError_label.pack_forget()

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
            loginError_label = Label(tk,text = "Tài khoản không tồn tại, xin đăng nhập lại")
            loginError_label.pack()
        else:
            pass


def hideInputIP_Frames():
    global isInputIP_Failed
    global inputIP_failed
    Client_text_label.pack_forget()
    inputIP_entry.pack_forget()
    inputIP_button.pack_forget()
    if isInputIP_Failed:
        inputIP_failed.pack_forget()


def loginForm():
    global loginText_label
    global usernameLabel
    global usernameEntry
    global passwordEntry
    global passwordLabel
    global loginButton
    loginText_label = Label(tk,text = "Đăng nhập")
    loginText_label.pack()
    ##userName label
    usernameLabel = Label(tk,text ="Username: ")
    username = StringVar()
    usernameEntry = Entry(tk, textvariable = username)

     ##passWord Label
    passwordLabel = Label(tk,text="Password")
    password = StringVar()
    passwordEntry = Entry(tk, textvariable=password, show='*')
    loginButton = Button(tk,text = "Login", command = partial(verifyLogin,username,password))
    usernameLabel.pack()
    usernameEntry.pack()
    passwordLabel.pack()
    passwordEntry.pack()
    loginButton.pack()


def connectSocket(localIP,portGate):
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            inputIP_failed = Label(tk,text = "IP không hợp lệ")
            inputIP_failed.pack()
        else:
            pass


## MAIN starts here
check = localIP = socket.gethostbyname(socket.gethostname())
tk = Tk()
tk.geometry("705x480")
Client_text_label = Label(tk,text = "Nhập IP của server: ")
inputIP = StringVar()
inputIP_entry = Entry(tk, textvariable = inputIP)
verifyIP = partial(verifyIP,inputIP)
inputIP_button = Button(tk,text = "Xác nhận",command = verifyIP)
Client_text_label.pack()
inputIP_entry.pack()
inputIP_button.pack()

tk.mainloop()
