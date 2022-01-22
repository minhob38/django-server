# Django Server

기본적인 구조를 갖춘 django server입니다.

## 환경설정

### • 설치

**\- 저장소 받기**  
받고싶은 경로에 github repository를 clone합니다.

```sh
$ git clone https://github.com/minhob38/django-server.git [받을 경로]
```

**\- 가상환경 만들기**  
받은경로에서 아래 스크립트를 실행하여, python 가상환경을 만듭니다.

```sh
$ python -m venv .
```

🔎 가상환경은 `source bin/activate`으로 활성화하고, `deactive`로 비활성화합니다.

**\- package 설치하기**  
가상환경을 활성화한 뒤, 아래 스크립트를 실행하여 `requirements.txt`에 정의된 package들을 설치합니다.

```sh
$ pip install -r requirements.txt
```

**\- db 설정하기**  
아래 스크립트를 실행하여 `INSTALLED_APPS`에 정의된 app들의 database들을 설정합니다.

```sh
$ python manage.py migrate
```

### • 실행

**\- database 올리기**  
아래 스크립트로 database(postgresql)의 docker container를 올립니다.

```sh
$ python script.py docker:db-up
```

**\- server 실행하기**  
아래 스크립트로 django server를 실행시킵니다. (port번호를 지정하지않으면 port 8000에서 실행됩니다.)

```sh
$ python manage.py runserver [port 번호]
```

## API

본서버는 인증 API `api/auth`, 게시판 API `api/board`, 지도 API `api/map`으로 이루어져 있습니다.

### • auth api

인증 API(signup, signin, signout 등)이며 아래 stack으로 만들어져 있습니다.  
\- function based view  
\- function middleware

### • board api

게시판 API이며 아래 stack으로 만들어져 있습니다.  
\- class based view  
\- django rest framework

### • map api

지도 API이며 아래 stack으로 만들어져 있습니다.  
\- class based view  
\- django rest framework  
\- class middleware  
\- postgis (raw sql)

### 📔 API Document

api 요청/응답은 swagger를 기반으로 문서화되어 있습니다.

## Database

본서버는 database로 db.sqlite3, postgresql(+postgis)를 사용합니다.

<!-- ## CI / CD -->
