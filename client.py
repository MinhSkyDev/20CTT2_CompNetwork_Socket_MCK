import socket
import threading
from tkinter import *
from functools import partial

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
##addr = (localIP,portGate)
##print(addr)
## ở đây socket.gethostname() sẽ trả về têm của PC, còn socket.gethostbyname() sẽ trả về local IP của tên máy
# cân nhắc sử dụng cách này thay vì sử dụng một hằng số



global isInputIP_Failed ## Biến này để check rằng đã bao giờ nhập IP sai chưa ?
isInputIP_Failed = False

def verifyLogin(username,password):
    ##Send message to server that we will verify Login
    ##LOGIN_REQUEST => MESSAGE
    username = str(username.get())
    password = str(password.get())
    sendAMessage("LOGIN_REQUEST")
    sendAMessage(username)
    sendAMessage(password)

def hideInputIP_Frames():
    global isInputIP_Failed
    Client_text_label.pack_forget()
    inputIP_entry.pack_forget()
    inputIP_button.pack_forget()
    if isInputIP_Failed:
        inputIP_failed.pack_forget()


def loginForm():
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
    localIP = socket.gethostbyname(socket.gethostname()) ## Chưa biết được rằng trả về có phải là một string không
    print(localIP,inputIP)
    if localIP == inputIP.get():
        hideInputIP_Frames()
        connectSocket(localIP,5051)
        loginForm()
    else:
        if isInputIP_Failed == False:
            isInputIP_Failed = True
            inputIP_failed = Label(tk,text = "IP không hợp lệ")
            inputIP_failed.pack()
        else:
            pass


## MAIN starts here
check = localIP = socket.gethostbyname(socket.gethostname())
print(check)
tk = Tk()
tk.geometry("400x500")
Client_text_label = Label(tk,text = "Nhập IP của server: ")
inputIP = StringVar()
inputIP_entry = Entry(tk, textvariable = inputIP)
verifyIP = partial(verifyIP,inputIP)
inputIP_button = Button(tk,text = "Xác nhận",command = verifyIP)
Client_text_label.pack()
inputIP_entry.pack()
inputIP_button.pack()

tk.mainloop()
