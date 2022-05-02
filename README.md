# CN_TCP_Socket_Project
TCP 기반 소켓 프로그래밍 작성

- 소켓 통신을 활용하여 Server, Client 프로그램 작성
  * 프로그래밍 언어는 C, Java, Python 으로 구현
- TCP 기반 소켓프로그래밍 작성후 
   Client에서는 HTTP 프로토콜의 GET/HEAD/POST/PUT Request를 요청하고
   Server에서는 Client의 Request에따라 응답 메시지를 구성하여 Response하도록 구현
   (TCP 기반 Client, Server 구현한 프로그램 파일을 제출)
   * 예) Method-응답 xxx의 case 5개 이상 수행.
      GET-응답 4xx, GET-응답 2xxx, HEAD-응답 1xx, POST-응답 2xxx, POST-응답 1xx 등
   * 소켓 통신은 PC가 2대 이상이면 Client, Server 실행은 분리하여 진행을 권장
      2대 이상 환경이 안되는 경우는 localhost로 진행도 가능
   * HTTP 명령어 수행 결과를 WireShark로 캡쳐하여 제출하는 경우는 가산점 부여
* 제출: 소스파일과 Readme 파일(ppt, doc 등)을 작성하여 제출
            Readme 파일은 소스 파일, 동작 환경, HTTP 명령어 결과에 대한 설명을 포함
            HTTP 명령어 수행시 Client, Server에서 출력하는 내용을 화면 캡쳐하여 작성
* 제출일정 : 5월3일(화)