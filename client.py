from socket import *

command = ''

# 접속 정보 설정
serverIP = '127.0.0.1' # 서버 IP를 127.0.0.1로 설정
serverPort = 8080 # 포트넘버 8080으로 설정


while command != 'quit' :
    command = input().split(' ')
    # 클라이언트 소켓 설정
    clientSocket = socket(AF_INET, SOCK_STREAM) # AF_INET : IPv4 인터넷 프로토콜, SOCK_STREAM : 소켓 타입을 TCP 프로토콜로 통신
    # clientSocket.close()
    clientSocket.connect((serverIP, serverPort)) # 서버 주소에 연결

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
