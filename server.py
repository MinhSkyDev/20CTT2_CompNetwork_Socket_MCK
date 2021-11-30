import socket
import threading
from tkinter import *
from functools import partial
import sys
import requests
from GetApi import getAPI


## Prepare the data
sizeOfLong = 64
portGate = 5051 ## Port không được nằm trong khoảng 0<= PORT <= 1024 vì đây là cổng cho các giao thức có sẵn trên máy
localIP = socket.gethostbyname(socket.gethostname())
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


def checkUserExist(user):
    if user[0] == "ABC" and user[1] == "XYZ":
        return True
    else:
        return False

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
                checkUserInDatabase = checkUserExist(user)
                if checkUserInDatabase:
                    sendAMessage("VALID",connection)
                else:
                    sendAMessage("INVALID",connection)
            elif message == "DATA_REQUEST":
                data_receive = getAPI()
                sendAMessage(data_receive,connection)





    deleteIndexConnections(connection,address) ## Làm xong thì xóa phần tử trong mảng này đi
    connection.close()
    print("Bye bye !")




def ExitServer():
    server.close()
    tk.destroy()
    setExit = True

def init():
    Server_text.configure(text = "Server đang chạy !")
    server.listen()
    global setExit
    try:
        while True:
            connection,address = server.accept() ## Nhận kết nối từ client và trả về connection
            connectionArray.append((connection,address))
            ## Ta có được connection kiểu trả về sẽ là một object kiểu Socket, vì thế khi truyền lên hàm handleInvidualThread
            ## thì sẽ là một biến mang kiểu đối tượng Socket
            thread = threading.Thread(target=handleInvidualThread, args=(connection,address)) ## Chia từng connection thành từng luồng khác nhau
            thread.start()
            global logRecords_string ## chỗ này phải gọi biến global này ra để có thể cập nhật được log
            logRecords_string += "\n Máy " + str(getIndexConnections(connection,address) +1) +" đã kết nối"
            log_records.config(text = logRecords_string)
    except:
            return


def initThreading():
    startServer = threading.Thread(target=init)
    startServer.start()

def hideLoginFrames(): ##Xóa các widgets Tkinter của phần login
    global isLoginError
    usernameLabel.pack_forget()
    usernameEntry.pack_forget()
    passwordLabel.pack_forget()
    passwordEntry.pack_forget()
    loginButton.pack_forget()
    Server_text.pack_forget()
    if isLoginError == True:
        loginError.pack_forget()

def usersAction():
    Active_users_text = Label(tk, text='ACTIVE USER', bg='#FFEFDB', font=('helvetica', 30, 'normal'))
    global log_records
    log_records = Label(tk,text =logRecords_string, bg='#FFEFDB', pady = 20) ## Đây là object để hiện lên các dòng lịch sử đăng nhập các kiểu của các clients
    exitButton = Button(tk,text = "exit", padx = 100, pady = 50, command = ExitServer)
    Active_users_text.pack()
    log_records.pack()
    exitButton.pack()
    initThreading()


def validateLogin(username,password):
    global isLoginError
    username_get = username.get()
    password_get = password.get()
    if username_get == "admin" and password_get == "123456": ## Ở đây sẽ là check liệu pass + username có nằm trong DB không
        hideLoginFrames()
        usersAction()
    else:
        if isLoginError:
            pass ## Do nothing
        else:
            loginError.pack()
            isLoginError = True



## MAIN starts here ##
tk = Tk()
tk.geometry("705x480")
tk.configure(background='#FFEFDB')
Server_text = Label(tk, text='ĐĂNG NHẬP VÀO SERVER', bg='#FFEFDB', font=('helvetica', 30, 'normal'))
##exitButton = Button(tk,text = "exit", padx = 100, pady = 50, command = setExitTrue)
##initButton = Button(tk,text = "init", padx = 100, pady = 50, command = initCommand)
##testButton = Button(tk,text = "forget",padx = 100, pady = 50, command = hideAllFrames)
Server_text.pack(pady = 50)
##exitButton.pack()
##initButton.pack()
##testButton.pack()

##userName label
usernameLabel = Label(tk,text ="Username: ", bg = "#FFEFDB")
username = StringVar()
usernameEntry = Entry(tk, textvariable = username)

 ##passWord Label
passwordLabel = Label(tk,text="Password", bg = "#FFEFDB")
password = StringVar()
passwordEntry = Entry(tk, textvariable=password, show='*')
##login button
## Trả về một object đã được nén lại từ một function với các parameters tương ứng
validateLogin = partial(validateLogin,username,password)
loginButton = Button(tk,text="Login", padx = 20, pady = 20, command =validateLogin)
loginError = Label(tk,text = "Đăng nhập thất bại, xin mời đăng nhập lại")
##Packlogin form
usernameLabel.pack()
usernameEntry.pack()
passwordLabel.pack()
passwordEntry.pack()
loginButton.pack(pady = 20)

tk.mainloop()
