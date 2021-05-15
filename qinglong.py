from requests import get,post,Response
from urllib.parse import   urlencode
from time import time
from json import dumps,loads



 
 

class qinglong:

    def __init__(self,host,username,password) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.authorization = None

    def _post(self,route,data,query_params:dict='') -> Response:
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42'
        }
        params = {
            't':str(int(time()*1000))
        }
        if self.authorization:
            headers['Authorization'] = f'Bearer {self.authorization}'
        url = self.host+'/api'+route
        
        if query_params:
            params.update(query_params)
        params = urlencode(params)
        url = url+f'?{params}'
        
        result = post(url,headers=headers,data=dumps(data),timeout=20)
        print(f'请求url：{url}, status_code: {result.status_code}')
        return result

    def _get(self, route , query_params: dict = '') -> Response:
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42'
        }
        params = {
            't': str(int(time()*1000))
        }
        if self.authorization:
            headers['Authorization'] = f'Bearer {self.authorization}'
        url = self.host+'/api'+route

        if query_params:
            params.update(query_params)
        params = urlencode(params)
        url = url+f'?{params}'

        result = get(url, headers=headers,timeout=20)
        print(f'请求url：{url}, status_code: {result.status_code}')
        return result

    def login(self):
        route = '/login'
        data = {
            'username': self.username,
            'password': self.password
        }
        query_params = urlencode({'t': str(int(time()*1000))})
        url = self.host+'/api'+route+f'?{query_params}'
        result = self._post( data=data,route=route)
        if result.status_code == 200:
            print(result.text)
            self.authorization = result.json()['token']

    def get_token(self):
        if not self.authorization:
            self.login()
        return self.authorization

    
    def _get_logs_list(self) -> Response:
        route = '/logs'
        result = self._get(route=route)
        return result

    def get_log_file(self,typ,file):
        route = f'/logs/{typ}/{file}'
        result = self._get(route=route)
        return result


