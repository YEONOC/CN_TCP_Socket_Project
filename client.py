from socket import *

command = ''

# 접속 정보 설정
serverIP = '127.0.0.1' # 서버 IP를 127.0.0.1로 설정
serverPort = 8080 # 포트넘버 8080으로 설정

commandList = [
    "HEAD 127.0.0.1/",                          # HEAD 메소드 요청 => 100 continue
    "GET 127.0.0.1/index.css",                  # 잘못된 path를 입력한 GET 요청 => 400 bad request
    "POST 127.0.0.1/create name:choiboseok",    # name : choiboseok 이란 정보를 db.json 파일에 저장해주는 POST 메소드 요청 => 201 created
    "GET 127.0.0.1/db.json",                    # GET 메소드 요청 => 200 ok
    "GET 127.0.0.1/create",                     # 잘못된 method를 입력한 create_path 요청 => 400 bad request
    "PUT 127.0.0.1/update name:choi",           # name : choi로 갱신하는 PUT 메소드 요청 => 200 ok
    "GET 127.0.0.1/update",                     # 잘못된 method를 입력한 create_path 요청 => 400 bad request
    "HEAD 128.0.0.2/",                          # 잘못된 IP에 연결하는 요청 => 400 bad request
    "POST 127.0.0.1/coding",                    # 잘못된 path를 입력한 POST 요청 => 404 not found
    "GET 127.0.0.1/db.json"                     # db.json 파일에 있는 내용을 요청 => 200 ok
]


for i in range(10) : # case 10개
    # 클라이언트 소켓 설정
    with socket(AF_INET, SOCK_STREAM) as clientSocket : # AF_INET : IPv4 인터넷 프로토콜, SOCK_STREAM : 소켓 타입을 TCP 프로토콜로 통신
        clientSocket.connect((serverIP, serverPort)) # 서버 주소에 연결
        command = commandList[i].split(' ')
        method = command[0]
        url = command[1]

        # request body가 담긴 요청인지 아닌지 분류
        if (len(command) == 3) :
            body = command[2]
        else :
            body = '' # body가 없는 요청인 경우
    
        request = f"{method} / HTTP/1.1\r\nHost: {url}\r\nContent-Type: text/html\r\nConnection: keep-alive\r\nContent-Length: {len(body)}\r\n\n{body}"
    
        clientSocket.send(request.encode()) # 서버에 메세지 전송
        msg = clientSocket.recv(1024).decode("utf-8") # 서버로 부터 온 메세지

        print("응답 요청 결과 : \n{}".format(msg))
        print("-----------------------------------")

        clientSocket.close()