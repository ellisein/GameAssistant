# GameAssistant

게임 API 등을 이용하여 게임 플레이에 도움을 줄 수 있도록 개발한 Django 기반 웹 서버입니다.

## 개발 환경

- Windows 10
- Python 3.7.3

### 파이썬 라이브러리

- Django 3.2.11
- asyncio 3.4.3
- aiohttp 3.6.2
- Pillow 9.0.0
- MinePI 0.4.2

## 실행 방법

1. Python을 설치합니다.
2. 다음 명령어를 사용하여 파이썬 라이브러리들을 설치합니다.

```
pip install -u django asyncio aiohttp Pillow MinePI
```

3. 월드 오브 워크래프트 API 기능 사용을 위해 [블리자드 API 홈페이지](https://develop.battle.net/access/clients)에서 사이트 내 문서에 따라 API 키를 획득합니다. 발급받은 API 키를 환경변수로 설정합니다.

```
setx BLIZZARD_API_CLIENT_ID "발급받은 CLIENT ID"
setx BLIZZARD_API_CLIENT_SECRET "발급받은 CLIENT SECRET"
```

4. 프로젝트 디렉터리에서 다음 명령어를 사용하여 정의된 Django 모델을 DB에 적용합니다.

```
python manage.py makemigrations games
python manage.py migrate
```

5. 다음 명령어로 코드를 실행합니다.

```
python manage.py runserver 0.0.0.0:80
```

## 미리보기

### 월드 오브 워크래프트 > 캐릭터 검색
![wow_character](/previews/wow_character.jpg)

### 월드 오브 워크래프트 > 신화 쐐기돌
![wow_mythic_keystone](/previews/wow_mythic_keystone.jpg)

### ANNO 1800 > 생산시설 계산기
![anno_calculator](/previews/anno_calculator.jpg)

### 마인크래프트 > 유저 스킨 검색
![minecraft_user](/previews/minecraft_user.jpg)
