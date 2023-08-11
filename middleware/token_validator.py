from routers.user.userApi import user

async def token_validator(request):
  headers = request.headers
  path = request.url.path
  pass_path = ["/user/login", "/user/register"] 
  if path in pass_path: 
    return 1
  if "authorization" in headers.keys():
    bithumb = user.connect_bithumb_privit(headers.get("authorization").replace("Bearer ", ""))
    idx = bithumb[1]
    bithumb = bithumb[0]
    return (bithumb , idx)
  else:
    return 1
