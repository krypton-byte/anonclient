import logging
import os
from anonchat.payload_pb2 import Action
import termios, sys
from typing import Optional
from .client import AnonChatAsync, logger
from .payload_pb2 import Message, Payload, TextMessage
import argparse
import asyncio
logger.setLevel(logging.INFO)
class Anu(AnonChatAsync):
    def __init__(self, url: str, token: str, name: str) -> None:
        super().__init__(url, token)
        self.paired = False
        fd = sys.stdin.fileno()
        self.r_i = None
        orig_termios = termios.tcgetattr(fd)
        new_termios = termios.tcgetattr(fd)
        new_termios[3] &= ~(termios.ICANON | termios.ECHO)
        
        # the following lines were added:
        new_termios[6][termios.VMIN] = 0 # minimal amount of characters to
        new_termios[6][termios.VTIME] = 1 # a max wait time of 1/10 second
        # set to new termios
        termios.tcsetattr(fd, termios.TCSADRAIN, new_termios)
        self.id_name = name
        self.queue = asyncio.Queue()
    async def on_message(self, message: Message, from_me: bool):
        await self.queue.put(('you'if from_me else 'msg', message.textMessage.text))
    async def terminput(self):
        """Get terminal input and send it to the queue."""
        sys.stdout.write('\rYou: ')
        sys.stdout.flush()
        while True:
            ch = sys.stdin.read(1) # read a single char (works because of the termios config)
            if ch == "\n":
                await self.queue.put(("finish", None)) # `None` here because we won't use the second argument
                await asyncio.sleep(0) # strange workaround so the queues actually work
                continue
            if ch:
                await self.queue.put(("input", ch))
            await asyncio.sleep(0) # strange workaround so the queues actually work
    async def render(self):
        msg = ''
        while True:
            evt, message = await self.queue.get()
            if evt == 'input':
                msg += message
            elif evt == 'finish':
                await self.send_payload(Message(textMessage=TextMessage(text=msg), id=self.id_name))
                msg = ''
            elif evt == 'msg':
                sys.stdout.write(f'\rAnonymous: {message}\n')
                sys.stdout.flush()
            elif evt == 'you':
                sys.stdout.write(f'\rYou: {message}\n')
            sys.stdout.write('\r' + ' '*os.get_terminal_size()[0])
            sys.stdout.write(f'\rYou: {msg}')
            sys.stdout.flush()
            self.queue.task_done()
    async def on_connected(self):
        await self.add_task(self.render())
        await self.send_payload(Action(name=Action.PAIR, id=self.id_name))
    async def on_paired(self, id: str):
        print(f'[+] {id} Paired')
        self.r_i = asyncio.ensure_future(self.terminput())
    async def on_close(self, id: str, ws: bool, from_me: bool):
        if self.r_i:
            self.r_i.cancel()
        print('Chat berhasil diputuskan' if from_me else 'Chat terputus')
        print('Melakukan pencarian ulang')
        await self.send_payload(Action(name=Action.PAIR, id=self.id_name))
    async def on_action(self, id: Optional[str], action_id: Action.Name):
        if Action.TIMEOUT == action_id:
            print('timeout to find partner\nretrying...')
            await self.send_payload(Action(name=Action.PAIR, id=self.id_name))
def anonchat():
    # termios stuff to: disable automatic echo so that, when a character is typed, it is not immediately printed on screen
    #                   read a single character from stdin without pressing <Enter> to finish
    fd = sys.stdin.fileno()
    orig_termios = termios.tcgetattr(fd)
    new_termios = termios.tcgetattr(fd)
    new_termios[3] &= ~(termios.ICANON | termios.ECHO)
    
    # the following lines were added:
    new_termios[6][termios.VMIN] = 0 # minimal amount of characters to
    new_termios[6][termios.VTIME] = 1 # a max wait time of 1/10 second
    # set to new termios
    termios.tcsetattr(fd, termios.TCSADRAIN, new_termios)
    async def terminput(queue: asyncio.Queue):
        """Get terminal input and send it to the queue."""
        while True:
            ch = sys.stdin.read(1) # read a single char (works because of the termios config)

            if ch == "\n":
                await queue.put(("finish", None)) # `None` here because we won't use the second argument
                await asyncio.sleep(0) # strange workaround so the queues actually work
                continue

            await queue.put(("input", ch))
            await asyncio.sleep(0) # strange workaround so the queues actually work
        
async def main(name: str):
    o = await Anu('wss://anonchat.krypton-byte.com/ws','159244216509b8948b5305cc9803249fad4fa2a47e3d7e326ac160fcf5bd372eb851dc30c5d21751', name)
    await o.ws.ping()
    await o.ws.wait_closed()

loop = asyncio.new_event_loop()
loop.run_until_complete(main('anonchat'))

# import websocket
# from .payload_pb2 import *
# ws = websocket.create_connection('ws://127.0.0.1:8000/ws')
# ws.send_binary(Payload(action=Action(name=Action.CONNECT, key='159244216509b8948b5305cc9803249fad4fa2a47e3d7e326ac160fcf5bd372eb851dc30c5d21751')).SerializeToString())
# print(Payload.FromString(ws.recv()))
# ws.send_binary(Payload(action=Action(name=Action.PAIR, id='joke')).SerializeToString())
# ws.send_binary(Payload(action=Action(name=Action.PAIR, id='joked')).SerializeToString())
# print(Payload.FromString(ws.recv()))
# print(Payload.FromString(ws.recv()))
# ws.send_binary(Payload(message=Message(textMessage=TextMessage(text='hi'), id='joke')).SerializeToString())
# print(Payload.FromString(ws.recv()))
