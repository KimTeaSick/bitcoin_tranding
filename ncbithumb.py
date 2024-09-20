from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Request
from starlette.requests import Request

from routers.dashborad import dash_api
from routers.coin_list import coin_api
from routers.trade_his import trade_his_api
from routers.search import search_api
from routers.trade import trade_api
from routers.test import test_api
from routers.user import user_api
from routers.assets import assets_api
from routers.member import member_api

from middleware.token_validator import token_validator

import uvicorn

app = FastAPI()

origins = ["http://localhost:3000", ]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.middleware("http")
async def middleware(request: Request, call_next):
    global bit
    path = request.url.path
    pass_path = ["/user/login", "/user/register", "/test/test", "/test/signTrade"] 
    if path in pass_path:
        response = await call_next(request)
        return response
    authorization_header = request.headers.get("Authorization")
    if authorization_header != 'Bearer null' and authorization_header != None:
        bit = await token_validator(request)
        if bit != 401:
            idx = bit[1]
            bit = bit[0]
            request.state.bit = bit
            request.state.idx = idx
            request.state.valid_token = True
        else:
            request.state.valid_token = False
    else:
        request.state.valid_token = False

    response = await call_next(request)
    return response

app.include_router(user_api.router)
app.include_router(dash_api.router)
app.include_router(coin_api.router)
app.include_router(trade_his_api.router)
app.include_router(search_api.router)
app.include_router(trade_api.router)
app.include_router(assets_api.router)
app.include_router(test_api.router)
app.include_router(member_api.router)

if __name__ == "__main__":
    config = uvicorn.Config("ncbithumb:app", port=8888, log_level="info", host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()
