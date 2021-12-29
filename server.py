import socket
import threading
from tkinter import *
from functools import partial
import sys
import requests
from GetApi import getAPI
from DB import isValidServer,isValidClient
import time


## Prepare the data
sizeOfLong = 64
portGate = 5051 ## Port không được nằm trong khoảng 0<= PORT <= 1024 vì đây là cổng cho các giao thức có sẵn trên máy
localIP = socket.gethostbyname(socket.gethostname())
data_receive = ""
checkUpdateAPI = False ##Sẽ truyển về true khi dừng chương trình
## ở đây socket.gethostname() sẽ trả về têm của PC, còn socket.gethostbyname() sẽ trả về local IP của tên máy
# cân nhắc sử dụng cách này thay vì sử dụng một hằng số


logRecords_string = "" ## Chuỗi dùng để lưu các records của các users
isLoginError = False
global setExit
setExit = False

## construct object Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## lệnh cơ bản trong socket python
server.bind((localIP,portGate))

## Data structures to make the program runs smoothly
## array để lưu index của các clients
connectionArray = [] ## Socket object
def getIndexConnections(connection,address):
    for i in range(0,len(connectionArray)):
        if connectionArray[i] == (connection,address):
            return i

def deleteIndexConnections(connection,address):
    for i in range(0,len(connectionArray)):
        if connectionArray[i] == (connection,address):
            connectionArray.pop(i)
            break


def sendAMessage(message,connection): ## Ở đây ta phải dùng connection thay vì server vì dùng chính thread connection đó để send luôn tương tự bên client, ta có client == connection ở trường hợp này
    message = message.encode('utf-8')
    messageSize = len(message)
    messageSize_send = str(messageSize).encode('utf8')
    messageSize_send += b' ' * (1024 - len(messageSize_send))
    connection.send(messageSize_send)
    connection.send(message)

def receiveUsernameAndPassword(connection,address):
    usernameSize = connection.recv(1024).decode("utf-8")
    username = ""
    if usernameSize != '':
        usernameSize = int(usernameSize)
        username = connection.recv(usernameSize).decode("utf-8")
    passwordSize = connection.recv(1024).decode("utf-8")
    password = ""
    if passwordSize != '':
        passwordSize = int(passwordSize)
        password = connection.recv(passwordSize).decode("utf-8")
    user = (username,password)
    return user




def handleInvidualThread(connection, address): ## Hàm để xử lý từng luồng khác nhau của các client, nói chung việc gửi nhận dữ liệu sẽ thực hiện ở đây
    indexConnection = getIndexConnections(connection,address) + 1
    while True:
        ## Một pakage gửi đi từ client sẽ mang hai thông tin:
        ## Số byte trong thông tin đó
        ## Thông tin đó
        ## Vì thế ta cần xác định được số byte được gửi đi trước
        messageSize = connection.recv(1024).decode("utf-8")
        if messageSize != '': ## Khi mà không nhận được message gì
            messageSize = int(messageSize)
            message = connection.recv(messageSize).decode("utf-8")
            if message == "LOGIN_REQUEST":
                user = receiveUsernameAndPassword(connection,address)
                checkUserInDatabase = isValidClient(user[0],user[1])
                if checkUserInDatabase:
                    sendAMessage("VALID",connection)
                else:
                    sendAMessage("INVALID",connection)
            elif message == "DATA_REQUEST":
                global data_receive
                sendAMessage(data_receive,connection)
            elif message == "EXIT":
                deleteIndexConnections(connection,address) ## Làm xong thì xóa phần tử trong mảng này đi
                connection.close()
                break





def ExitServer():
    server.close()
    tk.destroy()
    sys.exit()


def init():
    server.listen()
    global setExit
    try:
        while True:
            connection,address = server.accept() ## Nhận kết nối từ client và trả về connection
            connectionArray.append((connection,address))
            ## Ta có được connection kiểu trả về sẽ là một object kiểu Socket, vì thế khi truyền lên hàm handleInvidualThread
            ## thì sẽ là một biến mang kiểu đối tượng Socket
            thread = threading.Thread(target=handleInvidualThread, args=(connection,address)) ## Chia từng connection thành từng luồng khác nhau
            thread.daemon = True
            thread.start()
            global logRecords_string ## chỗ này phải gọi biến global này ra để có thể cập nhật được log
            logRecords_string += "\n Máy " + str(getIndexConnections(connection,address) +1) +" đã kết nối"
            log_records.config(text = logRecords_string)
    except:
            return

def updateAPI(): ##Update dữ liệu sao 30p = 60*30 giây
    global data_receive
    while True:
        data_receive = getAPI()
        time.sleep(60*30)

def initThreading():
    startServer = threading.Thread(target=init)
    updateAPI_threading = threading.Thread(target=updateAPI)
    startServer.daemon = True
    updateAPI_threading.daemon = True
    ## Chia luồng để tránh bị freeze
    startServer.start()
    updateAPI_threading.start()

def hideLoginFrames(): ##Xóa các widgets Tkinter của phần login
    global isLoginError
    usernameEntry.place_forget()
    passwordEntry.place_forget()
    loginButton.place_forget()
    userActive_image = PhotoImage(file = "assest/Server/active_users.png")
    Server_text.config(image = userActive_image)
    Server_text.photo_ref = userActive_image
    if isLoginError == True:
        loginError.place_forget()

def usersAction():
    global log_records
    log_records = Label(tk,text =logRecords_string, bg='#FFFFFF', pady = 20) ## Đây là object để hiện lên các dòng lịch sử đăng nhập các kiểu của các clients
    exitButton = Button(tk,text = "exit", highlightthickness=0 ,
                    padx = 30, pady = 20, command = ExitServer)
    log_records.place(x= 300 , y= 150)
    exitButton.place(x= 315, y = 390)
    initThreading()


def validateLogin(username,password):
    global isLoginError
    username_get = username.get()
    password_get = password.get()
    if isValidServer(username_get,password_get): ## Ở đây sẽ là check liệu pass + username có nằm trong DB không
        hideLoginFrames()
        usersAction()
    else:
        if isLoginError:
            pass ## Do nothing
        else:
            loginError.place(x=245.0,y=390.0)
            isLoginError = True



## MAIN starts here ##
tk = Tk()
tk.geometry("705x480")
tk.configure(background='#FFFFFF')
tk.title("Server")
tk.resizable(False,False)


loginBackground_image = PhotoImage( file="assest/Server/image_1.png" )

Server_text = Label(tk, image = loginBackground_image)
Server_text.place(x=0,y=0)


##userName entry
username = StringVar()
usernameEntry = Entry(tk, textvariable = username)

 ##passWord Label
password = StringVar()
passwordEntry = Entry(tk, textvariable = password,  show = '*')
##login button
## Trả về một object đã được nén lại từ một function với các parameters tương ứng
validateLogin = partial(validateLogin,username,password)
loginButton_image = PhotoImage(file = "assest/Server/button_1.png")
loginButton = Button(tk,borderwidth=0,highlightthickness=0,image = loginButton_image, command =validateLogin)
loginError = Label(tk,text = "Đăng nhập thất bại, xin mời đăng nhập lại")
##Packlogin form
passwordEntry.place(x=301.0,y=275.0,width=286.0,height=32.0)
usernameEntry.place(x=301.0,y=221.0,width=286.0,height=32.0)
loginButton.place(x=245.0,y=341.0,width=212.0,height=36.0)

tk.mainloop()
