from telethon import TelegramClient, events, sync
from json import loads
from re import findall,search
from os.path import dirname, abspath
PATH = dirname(abspath(__file__))

with open(PATH+'/config.py', 'r', encoding='utf-8') as r:
    config = loads(r.read())

chat_id = config['bot_token'].split(':')[0]

appid = config['appid']
apihash = config['apihash']

client = TelegramClient('anon',api_id=appid,api_hash=apihash)

flag = ['-','\\','|','/']
i = 0

@client.on(events.NewMessage)
async def main(event):
    global i
    
    #print('\r'+flag[i],flush=True,end='')
    message = event.message.message
    if i == 3:
        i = 0
    else:
        i += 1
     
    # listen channel message and forward to a new chat
    
    # listen user message and forward to a new chat
    if hasattr(event.from_id, 'user_id') and str(event.from_id.user_id) in [str(chat_id)]:
        print('this message from a user',event.text)
     
        if 'forward_message_to:' in message:
    
            reg_text = search(r'forward_message_to:#(.*?)#',message).group()
            to_user = findall(r'forward_message_to:#(.*?)#',message)[0]
            print(f'forward_message_to:{to_user}')
            await client.send_message(to_user,message.replace(reg_text,''))
        print()
        return
    
        
with client:
    from setproctitle import setproctitle
    setproctitle('telegram listen for forward')
    print('start listen')
    client.run_until_disconnected()
 
