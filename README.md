# PyP
광명북고등학교 파이프(PyP)동아리

> ### 소스코드 업로드 시 유의점
> 1. 두 명의 학번으로 디렉토리를 생성합니다. (예시: /20103_20107)
> 2. 디렉토리 안에 소스코드를 업로드합니다.
> 3. **(중요) API KEY는 절대 유출하지 마세요.** (아래를 참고해서 코드 수정)
> ```python
> import requests
> import time
> import json
>
> with open('data.json', 'r') as f:
>    data = json.load(f)
>
> RIOT_API_KEY = 'API_KEY' # 이렇게 하라고
> Headers = {
>    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
>                  "Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
>    "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
>    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
>    "Origin": "https://developer.riotgames.com",
>    "X-Riot-Token": RIOT_API_KEY
> } ...
> ```
