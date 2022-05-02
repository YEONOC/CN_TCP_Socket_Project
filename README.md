# CN_TCP_Socket_Project
TCP 기반 소켓 프로그래밍 작성

- 동작 환경
   * python 3.9
   * server.py와 client.py로 분리하여 진행
   * port number는 8080으로 하여 localhost로 실행

- 소스 코드
   1. server.py
```python
from socket import * # socket 통신 모듈 가져오기
import time        # 실시간 전송 시간을 파악하기 위해 time 모듈 가져오기
import json        # json파일 생성, 수정을 위해 json 모듈 가져오기

# 통신정보 설정
IP = '127.0.0.1' # IP는 client에서 지정한 127.0.0.1로 디폴트
PORT = 8080 # 포트번호를 8080 지정

# 100 = continue / 200 = ok / 201 = created / 400 = bad request / 404 = not found
header = [[100, 'CONTINUE'], [200, 'OK'], [201, 'CREATED'], [400, 'BAD REQUEST'], [404, 'NOT FOUND']]

# client로부터 요청받은 메세지의 method와 url, body를 분석해서 각각의 요청에 대한 처리
def check(method, url, body) :
    if ('/' in url) :
        host, path = url.split('/') 
        # ex) 127.0.0.1/index.html => host = 127.0.0.1, path = index.html
        
        if (host == IP) :
            if (method == 'HEAD') :
                return fillHeaderResp(header[0])  
                # ex) request = HEAD 127.0.0.1/ => response = 100, continue
            
            if (method == 'GET') :
                if (path == 'db.json') :
                    with open('./db.json', 'r') as f:
                        json_data = json.load(f)
                    database=json.dumps(json_data, indent="\t")
                    return fillHeaderResp(header[1], body = database) 
                    # ex) request = GET 127.0.0.1/db.json => response = 200, ok
            
                else :
                    return fillHeaderResp(header[3]) 
                    # ex) request = GET 127.0.0.1/index.css => response = 400, bad request
            
            elif (path == 'update') :
                if (method == 'PUT') :
                    return respPut(body) 
                    # ex) request = PUT 127.0.0.1/update body => resPut(body) 함수를 실행해서 처리
            
                else :
                    return fillHeaderResp(header[3]) 
                    # ex) request = GET 127.0.0.1/update => response = 400, bad request
            
            elif (path == 'create') :
                if (method == 'POST') :
                    return respPost(body) 
                    # ex) request = POST 127.0.0.1/create body => resPost(body) 함수를 실행해서 처리
            
                else :
                    return fillHeaderResp(header[3]) 
                    # ex) request = GET 127.0.0.1/create => response = 400, bad request
            
            else :
                return fillHeaderResp(header[4]) 
                # ex) request = POST 127.0.0.1/coding => response = 404, not found
        
        else :
            return fillHeaderResp(header[3], body="refused connection") 
            # ex) request = 128.0.0.1/index.html => 400, bad request
    
    else : 
        return fillHeaderResp(header[4]) 
        # ex) request = 127.0.0.1 => response = 404, not found

# put method가 들어왔을 때 처리
def respPut(body) :
    body = body.split(':')
    # ex) body = name:choiboseok => body["name", "choiboseok"]
    if (len(body) == 2) :
        with open('./db.json', 'r') as f: # db.json 파일 내용 불러오기
            json_data = json.load(f)
        json_data[body[0]] = body[1]
        with open('./db.json', 'w', encoding='utf-8') as make_file: # db.json 파일에 수정사항 쓰기
            json.dump(json_data, make_file, indent="\t")
        with open('./db.json', 'r') as f: # db.json 파일 내용 불러오기
            json_data = json.load(f)
        database = json.dumps(json_data, indent="\t")
        return fillHeaderResp(header[1], body=database)
    else :
        return fillHeaderResp(header[3])
        
# post method가 들어왔을 때 처리
def respPost(body) :
    body = body.split(':')
    if (len(body) == 2) :
        db = dict()
        key = body[0]
        value = body[1]
        db[key] = value
        with open('./db.json','w', encoding='utf-8') as make_file : # db.json 파일에 수정사항 쓰기
            json.dump(db, make_file, indent='\t')
    
        with open('./db.json', 'r') as f: # db.json 파일 내용 불러오기
            json_data = json.load(f)
        database = json.dumps(json_data, indent="\t")
        return fillHeaderResp(header[2], body=database)
    else :
        return fillHeaderResp(header[3])

# server에서 client로 요청에 대한 응답을 줄 때, header를 달고 응답 메세지를 생성
def fillHeaderResp(header, body='') :
    date = time.strftime('%a, %b %d %Y %H:%M:%S GMT', time.localtime(time.time()))
    return f"HTTP/1.1 {header[0]} {header[1]}\r\nContent-Type: text/html\r\nConnection: keep-alive\r\nContent-Length: {len(body)}\r\nDate: {date}\r\n\n{body}"

# 들어온 메세지에서 client가 요청한 http method가 무엇인지 찾음
def findMethod(arr) :
    arr = arr.split(' ')
    return arr[0]

#서버 소켓 설정
with socket(AF_INET, SOCK_STREAM) as serverSocket : # AF_INET : IPv4 인터넷 프로토콜, SOCK_STREAM : 소켓 타입을 TCP 프로토콜로 통신
    serverSocket.bind((IP,PORT)) # 주소 바인딩
    serverSocket.listen(1) # 클라이언트의 요청을 받을 준비
    print("server connected, localhost:8080")

    # 무한루프 진입
    while True :
        connectionSocket, addr = serverSocket.accept() # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 변환

        msg = connectionSocket.recv(1024).decode('utf-8') # 클라이언트가 보낸 메세지 변환
    
        # 클라이언트의 request 확인
        msgarr = msg.split('\n')
        method = findMethod(msgarr[0])
        url = msgarr[1][6:-1]
        body = msgarr[-1]
        resp = check(method, url, body)
    
        print("[{}] message : \n{}".format(addr, msg)) # 클라이언트가 보낸 메세지 출력

        connectionSocket.send(resp.encode('utf-8')) # 클라이언트에게 응답
```
   2. client.py
```python
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
```

- 결과
   * 실행 case 10 가지 (차례대로)
      -     "HEAD 127.0.0.1/",                          # HEAD 메소드 요청 => 100 continue
      -     "GET 127.0.0.1/index.css",                  # 잘못된 path를 입력한 GET 요청 => 400 bad request
      -     "POST 127.0.0.1/create name:choiboseok",    # name : choiboseok 이란 정보를 db.json 파일에 저장해주는 POST 메소드 요청 => 201 created
      -     "GET 127.0.0.1/db.json",                    # GET 메소드 요청 => 200 ok
      -     "GET 127.0.0.1/create",                     # 잘못된 method를 입력한 create_path 요청 => 400 bad request
      -     "PUT 127.0.0.1/update name:choi",           # name : choi로 갱신하는 PUT 메소드 요청 => 200 ok
      -     "GET 127.0.0.1/update",                     # 잘못된 method를 입력한 create_path 요청 => 400 bad request
      -     "HEAD 128.0.0.2/",                          # 잘못된 IP에 연결하는 요청 => 400 bad request
      -     "POST 127.0.0.1/coding",                    # 잘못된 path를 입력한 POST 요청 => 404 not found
      -     "GET 127.0.0.1/db.json"                     # db.json 파일에 있는 내용을 요청 => 200 ok
   * server.py 실행 결과
      ![3849E57F-B164-49B1-91AB-C88976C11BF4](https://user-images.githubusercontent.com/39399715/166238644-c522ceca-54b6-4960-ab16-c352dfa549ab.png)
      ![1EB97501-57BF-4614-B711-726F4A459AC0](https://user-images.githubusercontent.com/39399715/166238793-d9918382-9bd2-45b7-9664-c24452350f75.png)
   
   * client.py 실행 결과
      ![47E4EEC7-5BC3-4C0A-965F-3204A96E84E8](https://user-images.githubusercontent.com/39399715/166239310-644cbc16-8b80-4d62-a19e-7f8ab6da3e19.png)
      ![D92FEAB2-3DF5-496A-AAE6-4D3549E7B820](https://user-images.githubusercontent.com/39399715/166239341-b3dc1d1f-b20c-4c1c-a29e-26152be49383.png)
   * wireshark 캡쳐
      ![5717AE21-6568-43D8-8947-5673BCB86EE5](https://user-images.githubusercontent.com/39399715/166239662-45f641de-f32c-4bf6-bc05-27e9d5bee56c.png)
   * db.json 파일
      ![A8D4E730-253D-4A5B-BCEA-1E832960CFB4](https://user-images.githubusercontent.com/39399715/166239948-19665757-d65e-4fda-a101-8f7c9432f9eb.png)
