# Django Server
기본적인 구조를 갖춘 django server입니다.

## API
본서버는 인증 API `api/auth`와 지도 API `api/map`으로 이루어져 있습니다.

### • auth api
인증 API(signup, signin, signout 등)이며 아래 stack으로 만들어져 있습니다.  
\- function based view  
\- function middleware  

### • board api
게시판 API이며 아래 stack으로 만들어져 있습니다.  
\- class based view
\- django rest framework
\- class middleware  

### • map api
지도 API이며 아래 stack으로 만들어져 있습니다.  
\- class based view
\- django rest framework
\- postgis (raw sql)

### 📔 API Document
api 요청/응답은 swagger를 기반으로 문서화되어 있습니다.

## Database
본서버는 database로 db.sqlite3, postgresql(+postgis)를 사용합니다.

## To Do
- social signup / login
- admin (settings.py)
- map (class view, postgresql gis, jwt, template)
- refresh token (redis)
- test code
- lint
- docker
- class middleware (map, response formatting)
- 1) 모든 sgg 행조회 (serializer, apivew), 2)해당동 행조회 3)해당 경계 동들 조회 4)면적순조회 5)해당점을 포함하는 동조회
- orm이 아닌 raw sql을 사용하면, serializer는 안쓰는게 좋을듯
- serverless (gcp, aws)
- 보안
- socket 서버
- 파일
- multi login