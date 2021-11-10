import socket
import threading

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
    connection.close()
    print("Bye bye !")

def init():
    server.listen()
    while True:
        connection,address = server.accept() ## Nhận kết nối từ client và trả về connection
        connectionArray.append((connection,address))
        ## Ta có được connection kiểu trả về sẽ là một object kiểu Socket, vì thế khi truyền lên hàm handleInvidualThread
        ## thì sẽ là một biến mang kiểu đối tượng Socket
        thread = threading.Thread(target=handleInvidualThread, args=(connection,address)) ## Chia từng connection thành từng luồng khác nhau
        thread.start()
        print("SỐ CLIENT ĐANG HOẠT ĐỘNG: ",threading.active_count() -1)


print("Khởi động server")
init()
