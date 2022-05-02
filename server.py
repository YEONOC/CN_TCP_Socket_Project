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
            
            if (path == 'index.html') :
                if (method == 'GET') :
                    return fillHeaderResp(header[1], body) 
                    # ex) request = GET 127.0.0.1/index.html => response = 200, ok
            
                else :
                    return fillHeaderResp(header[3]) 
                    # ex) request = HEAD 127.0.0.1/index.html => response = 400, bad request
            
            elif (path == 'update') :
                if (method == 'PUT') :
                    return respPut(body) 
                    # ex) request = PUT 127.0.0.1/update body => resPut(body) 함수를 실행해서 처리
            
                else :
                    return fillHeaderResp(header[3]) 
                    # ex) request = HEAD 127.0.0.1/update => response = 400, bad request
            
            elif (path == 'create') :
                if (method == 'POST') :
                    return respPost(body) 
                    # ex) request = POST 127.0.0.1/create body => resPost(body) 함수를 실행해서 처리
            
                else :
                    return fillHeaderResp(header[3]) 
                    # ex) request = HEAD 127.0.0.1/create => response = 400, bad request
            
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
        return fillHeaderResp(header[2], body=str(database))
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
        return fillHeaderResp(header[2], body=str(database))
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
serverSocket = socket(AF_INET, SOCK_STREAM) # AF_INET : IPv4 인터넷 프로토콜, SOCK_STREAM : 소켓 타입을 TCP 프로토콜로 통신
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

    connectionSocket.close() # 클라이언트 소켓 종료