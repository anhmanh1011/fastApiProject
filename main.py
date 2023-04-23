import asyncio
import re
import time
import traceback

import uvicorn
from fastapi import BackgroundTasks, FastAPI
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.types import InputPeerSelf

app = FastAPI()

client: TelegramClient
lst_channel = 'scanmmovn;congdongfbtool;fbmarketisocial;SHOP2FA;trieuvia;FSpammer;okscanw;GroupiSocial;tricksandtipsbuysell;chonguyenlieuisocial;CongDongIsocialTuDo;AdbreakUnderground;iforumfacebookblack;VOIADSviaBMXMDN;clonermmo;FacebookVietNam;congdongfacebookvietnam;bmgiare;bangkinggruop;adstichxank;CheckScammer;congdongscanviavietnam;HGN_B4NKLOG;kenhscan'


# api_id = 28921419
# api_hash = '8aca63a102fec741ebf418074c070499'


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/start")
async def say_hello(api_id: int, api_hash: str, phone: str):
    # asyncio.get_event_loop().run_until_complete(login(api_id, api_hash, phone))
    await login(api_id, api_hash, phone)
    return {"message": f"sent code to telegram {phone}"}


async def forward_message_toChat(client: TelegramClient, str_arr_channel: str):
    while True:
        try:
            self_peer = InputPeerSelf()
            messages = await client.get_messages(self_peer, limit=1)
            latest_message = messages[0]
            arr: [] = str_arr_channel.split(';')

            for i in range(len(arr) - 1, -1, -1):
                #     reversed_arr.append(arr[i])
                # for channel_str in arr:
                username = str(arr[i])
                try:
                    await client(JoinChannelRequest(username))
                    # dialogs = client.get_dialogs(limit=1)
                    print(" wirte to channel name" + username)
                    await client(ForwardMessagesRequest(
                        from_peer=await client.get_input_entity(self_peer),
                        id=[latest_message.id],
                        to_peer=await client.get_input_entity(username)
                    ))
                    print(" wirte to channel name" + username + ' Successfully')
                    time.sleep(10)
                except Exception as e:
                    print(f'write to channel {username} error {e}')
                    error: str = str(e)
                    if error.__contains__('wait'):
                        wait_time = re.findall("[0-9]{3}", str(e))[0]
                        print(f'waiting ... {wait_time}')
                        time.sleep(int(wait_time))
                    else:
                        continue
        except Exception as ex:
            print(ex)
            print(ex)
            traceback.print_exc()
        finally:
            time.sleep(600)


@app.get("/appr")
async def say_hello(code: str, background_tasks: BackgroundTasks):
    global client
    await client.sign_in(code=code)
    user = await client.get_input_entity('me')
    await client.send_message('me', 'loggin success!')
    print(user.stringify())
    # background_tasks.add_task(forward_message_toChat, client, lst_channel)
    # new_thread = Thread(target=forward_message_toChat, args=(client, lst_channel))
    # new_thread.start()
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        print('Async event loop already running. Adding coroutine to the event loop.')
        tsk = loop.create_task(forward_message_toChat(client, lst_channel))
        # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
        # Optionally, a callback function can be executed when the coroutine completes
        tsk.add_done_callback(
            lambda t: print(f'Task done with result={t.result()}  << return val of main()'))
    else:
        print('Starting new event loop')
        result = asyncio.run(forward_message_toChat(client, lst_channel))
    # forward_message_toChat(client, lst_channel)
    return {"message": f"loggin success {user.stringify()}"}


async def login(api_id, api_hash, phone):
    global client
    client = TelegramClient(
        api_hash, api_id, api_hash)
    await client.connect()
    await client.sign_in(phone=phone)


# if __name__ == '__main__':
#     uvicorn.run(app, port=8000)
