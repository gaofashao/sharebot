from requests.api import patch
from qinglong import qinglong
from json import loads,dumps
from re import findall
from requests import get
from urllib.parse import urlencode
from time import sleep
from os.path import dirname,abspath
PATH = dirname(abspath(__file__))

with open(PATH+'/config.py','r',encoding='utf-8') as r:
    config = loads(r.read())

username = config['username']
password = config['password']
host = config['host']
codes = config['codes']
default_user = config.get('default_user',None)
bot_token = config['bot_token']
chat_id = config['chat_id']

ql = qinglong(host=host, username=username, password=password)
ql.login()
result = ql._get_logs_list().json()
 
for r in result['dirs']:
    if r['name'] == 'chinnkarahoi_jd_get_share_code':
        print(max(r['files']))
        file = max(r['files'])
        result = ql.get_log_file('chinnkarahoi_jd_get_share_code', file)
        with open(f'/root/item/jd_beans/{file}', 'w', encoding='utf-8') as w:
            w.write(result.json()['data'])
        log = result.json()['data']
  
for code_bot, code_log in codes.items():
    _codes = []
    for i in default_user or range(1,5+1):
        
        code = findall(f"【京东账号{i}.*{code_log}】(.*)",log)
        print('code:', code, f"【京东账号{i}.*{code_log}】(.*)")
        #code = findall(f"{code_log}{i}='(.*?)'",log)
        if len(code) != 1: continue
        code = code[0]
        if code:
            _codes.append(code)
    code = '&'.join(_codes)
    text = f'/submit_activity_codes {code_bot} {code}'
    query_params = {
        'chat_id':chat_id,
        'text': f'forward_message_to:#TuringLabbot#{text}'
    }
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?{urlencode(query_params)}'
    result = get(url)
    #sleep(1)
    print(result.text)
