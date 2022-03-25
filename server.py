from socket import *

# 통신정보 설정
serverIP = '' # IP는 client에서 지정한 127.0.0.1로 디폴트
serverPort = 8080 # 포트번호를 8080 지정

#서버 소켓 설정
serverSocket = socket(AF_INET, SOCK_STREAM) # AF_INET : IPv4 인터넷 프로토콜, SOCK_STREAM : 소켓 타입을 TCP 프로토콜로 통신
serverSocket.bind((serverIP,serverPort)) # 주소 바인딩
serverSocket.listen(1) # 클라이언트의 요청을 받을 준비
print("The server is ready to receive - 8080 PORT")

# 무한루프 진입
while True :
    connectionSocket, addr = serverSocket.accept() # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 변환
    msg = connectionSocket.recv(1024) # 클라이언트가 보낸 메세지 변환
    print("[{}] message : {}".format(addr, msg)) # 클라이언트가 보낸 메세지 출력
    
    connectionSocket.sendall("welcome!".encode()) # 클라이언트에게 응답

    connectionSocket.close() # 클라이언트 소켓 종료