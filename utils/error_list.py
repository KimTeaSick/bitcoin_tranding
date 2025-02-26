def error_list(e_type):
  if e_type == 0:
    return {"status": 401, "data": "token invalid", "text":"유효하지 않은 토큰 입니다."}
  elif e_type == 1:
    return {"status": 402, "data": "paramater type different", "text": "잘못된 파라미터 입니다."}
  elif e_type == 2:
    return {"status": 403, "data": "Bad request", "text": "잘못된 요청입니다."}
