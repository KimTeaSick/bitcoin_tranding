import asyncio
# 웹 소켓 모듈을 선언한다.
import websockets
import json

async def connect():
  # 웹 소켓에 접속을 합니다.
  async with websockets.connect("wss://pubwss.bithumb.com/pub/ws") as websocket:
    # 10번을 반복하면서 웹 소켓 서버로 메시지를 전송합니다.
    for i in range(1,10,1):
      
      await websocket.send("hello socket!!");
      # 웹 소켓 서버로 부터 메시지가 오면 콘솔에 출력합니다.
      data = await websocket.recv();
      print(data);
# 비동기로 서버에 접속한다.
asyncio.get_event_loop().run_until_complete(connect())