import socket
import threading
from tkinter import *
from functools import partial

## Prepare the data
sizeOfLong = 64
portGate = 5051 ## Port không được nằm trong khoảng 0<= PORT <= 1024 vì đây là cổng cho các giao thức có sẵn trên máy
localIP = socket.gethostbyname(socket.gethostname())
## ở đây socket.gethostname() sẽ trả về têm của PC, còn socket.gethostbyname() sẽ trả về local IP của tên máy
# cân nhắc sử dụng cách này thay vì sử dụng một hằng số

## Data structures to make the program runs smoothly
## array để lưu index của các clients
def getIndexConnections(connection,address):
    for i in range(0,len(connectionArray)):
        if connectionArray[i] == (connection,address):
            return i


def deleteIndexConnections(connection,address):
    for i in range(0,len(connectionArray)):
        if connectionArray[i] == (connection,address):
            connectionArray.pop(i)
            break
connectionArray = [] ## Socket object


## construct object Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## lệnh cơ bản trong socket python
server.bind((localIP,portGate))

def handleInvidualThread(connection, address):
    indexConnection = getIndexConnections(connection,address) + 1
    print("Kết nối ", indexConnection ," đã được liên kết")
    while True:
        ## Một pakage gửi đi từ client sẽ mang hai thông tin:
        ## Số byte trong thông tin đó
        ## Thông tin đó
        ## Vì thế ta cần xác định được số byte được gửi đi trước
        messageSize = connection.recv(1024).decode("utf-8")
        if messageSize != '': ## Khi mà không nhận được message gì
            messageSize = int(messageSize)
            message = connection.recv(messageSize).decode("utf-8")
            print("Máy ", indexConnection ," muốn nói rằng: ",message)
            if message == "DISCONNECT":
                break
    deleteIndexConnections(connection,address) ## Làm xong thì xóa phần tử trong mảng này đi
    connection.close()
    print("Bye bye !")



def setExitTrue():
    for connection in  connectionArray:
        connection.close()
    server.close()
    tk.destroy()

def init():
    Server_text.configure(text = "Server đang chạy !")
    server.listen()
    try:
        while True:
            connection,address = server.accept() ## Nhận kết nối từ client và trả về connection
            connectionArray.append((connection,address))
            ## Ta có được connection kiểu trả về sẽ là một object kiểu Socket, vì thế khi truyền lên hàm handleInvidualThread
            ## thì sẽ là một biến mang kiểu đối tượng Socket
            thread = threading.Thread(target=handleInvidualThread, args=(connection,address)) ## Chia từng connection thành từng luồng khác nhau
            thread.start()
            print("SỐ CLIENT ĐANG HOẠT ĐỘNG: ",threading.active_count() -2)
    except setEXit == True:
            server.close()
            tk.destroy()


def initCommand():
    startServer = threading.Thread(target=init)
    startServer.start()

def hideLoginFrames(): ##Xóa các widgets Tkinter của phần login
    usernameLabel.pack_forget()
    usernameEntry.pack_forget()
    passwordLabel.pack_forget()
    passwordEntry.pack_forget()
    loginButton.pack_forget()
    Server_text.pack_forget()



def validateLogin(username,password):
    username_get = username.get()
    password_get = password.get()
    if username_get == "admin" and password_get == "123456": ## Ở đây sẽ là check liệu pass + username có nằm trong DB không
        hideLoginFrames()


## MAIN starts here ##
tk = Tk()
tk.geometry("400x500")
Server_text = Label(tk,text = "Đăng nhập vào server")
exitButton = Button(tk,text = "exit", padx = 100, pady = 50, command = setExitTrue)
initButton = Button(tk,text = "init", padx = 100, pady = 50, command = initCommand)
testButton = Button(tk,text = "forget",padx = 100, pady = 50, command = hideAllFrames)
Server_text.pack()
##exitButton.pack()
##initButton.pack()
##testButton.pack()

##userName label
usernameLabel = Label(tk,text ="Username: ")
username = StringVar()
usernameEntry = Entry(tk, textvariable = username)

 ##passWord Label
passwordLabel = Label(tk,text="Password")
password = StringVar()
passwordEntry = Entry(tk, textvariable=password, show='*')

##login button
validateLogin = partial(validateLogin,username,password)
loginButton = Button(tk,text="Login", padx = 50, pady = 50, command =validateLogin)
##Packlogin form
usernameLabel.pack()
usernameEntry.pack()
passwordLabel.pack()
passwordEntry.pack()
loginButton.pack()


tk.mainloop()
init()
