def error_list(e_type):
  if e_type == 0:
    return {"status": 401, "data": "token invalid"}
  if e_type == 1:
    return {"status": 402, "data": "paramater type different"}
  if e_type == 2:
    return {"status": 403, "data": "Bad request"}
