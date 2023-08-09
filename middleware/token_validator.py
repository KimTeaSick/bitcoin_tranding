from routers.user.userApi import user

async def token_validator(request):
  headers = request.headers
  path = request.url.path
  if path == "/user/login": 
    return 1
  if "authorization" in headers.keys():
    bithumb = user.connect_bithumb_privit(headers.get("authorization").replace("Bearer ", ""))
    return bithumb
    # print("bithumb :::::   :::::", bithumb)
  else:
    return 1
