import socket
import threading

sizeOfLong = 64
portGate = 5051 ## Port không được nằm trong khoảng 0<= PORT <= 1024 vì đây là cổng cho các giao thức có sẵn trên máy
localIP = socket.gethostbyname(socket.gethostname())
addr = (localIP,portGate)
print(addr)
## ở đây socket.gethostname() sẽ trả về têm của PC, còn socket.gethostbyname() sẽ trả về local IP của tên máy
# cân nhắc sử dụng cách này thay vì sử dụng một hằng số

## khởi  tạo object socket ở phía Client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)


def sendAMessage(message):
    ## Ta sẽ đi theo cấu trúc gửi tin bên client
    message = message.encode('utf-8')
    messageSize = len(message)
    messageSize_send = str(messageSize).encode('utf8')
    messageSize_send += b' ' * (1024 - len(messageSize_send))
    client.send(messageSize_send)
    client.send(message)


##message = ""
##while message != ""

sendAMessage("Hello, world!")
input()
