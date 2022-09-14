from __future__ import annotations
from typing import Awaitable, Optional, Union
from websockets.legacy.client import Connect
from websockets.legacy.client import WebSocketClientProtocol
from .payload_pb2 import Alert, Message, Action, Payload
import logging
import asyncio
logging.basicConfig(format='%(asctime)s <-> %(message)s', level=logging.INFO)
logger = logging.getLogger('anonchat')
class BadCredentials(Exception):
    pass

class InvalidProtoObject(Exception):
    pass

class AnonChatAsync:
    ws: WebSocketClientProtocol
    def __await__(self):
        return self.__init_async__().__await__()
    def __init__(self, url: str,token: str) -> None:
        self.token = token
        self.url = url
        self.futures = []
    async def __init_async__(self):
        self.ws = await Connect(self.url).__aenter__()
        await self.add_task(self.run())
        return self
    async def __aexit__(self, *args, **kwargs) -> None:
        await self.ws.close()
    async def send_payload(self, payload: Union[Message, Alert, Action]):
        key: str = ''
        if isinstance(payload, Message):
            key = 'message'
        elif isinstance(payload, Alert):
            key = 'alert'
        elif isinstance(payload, Action):
            key = 'action'
        if key:
            logger.debug('send %s payload' % key.title())
            await self.ws.send(Payload(**{key: payload}).SerializeToString())
        else:
            raise InvalidProtoObject()
            
    async def on_connected(self):
        self.connected = True
        logger.debug('CONNECTED')
        pass
    async def on_message(self, message: Message, from_me: bool):
        logger.debug('MESSAGE from id ', message.id)
        pass
    async def on_paired(self, id: str):
        logger.debug(f'{id} PAIRED')
        pass
    async def on_close(self, id: str, ws_partner_closed: bool, from_me: bool):
        logger.debug('ID ', id, 'CLOSED ws_partner: ', 'DISCONNECT' if ws_partner_closed else 'CONNECTED', ' from_me: ', from_me)
        pass
    async def on_action(self, id: Optional[str], action_id: Action.Name):
        logger.debug('ACTION ', Action.Name.Name(action_id))
        pass
    async def add_task(self, task: Awaitable):
        self.futures.append(asyncio.ensure_future(task))
        for i in self.futures:
            if i.done():
                self.futures.remove(i)
    async def run(self):
        await self.ws.send(Payload(action=Action(name=Action.CONNECT, key=self.token)).SerializeToString())
        while True:
            resp = await self.ws.recv()
            if isinstance(resp, bytes):
                payload = Payload.FromString(resp)
                logger.debug('receive '+payload.__str__())
                if payload.message != Message():
                    await self.add_task(self.on_message(payload.message, payload.message.from_me))
                elif payload.action != Action():
                    if payload.action.name == Action.PAIRED:
                        await self.add_task(self.on_paired(payload.action.id))
                    elif payload.action.name in [Action.WS_DISCONNECT, Action.CLOSED]:
                        await self.add_task(self.on_close(payload.action.id, payload.action.name == Action.WS_DISCONNECT, payload.action.from_me))
                    else:
                        await self.add_task(self.on_action(payload.action.id if payload.action.id else None, payload.action.name))
                elif payload.alert != Alert():
                    if payload.alert.type == Alert.CONNECTED:
                        await self.add_task(self.on_connected())
                    elif payload.alert.type == Alert.BAD_CREDENTIALS:
                        raise BadCredentials()


            
