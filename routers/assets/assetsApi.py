from fastapi import APIRouter, Request
from lib.errorList import error_list
from .paramater import *
from .assetsFn import AssetsFn

assetsRouter = APIRouter(
  prefix="/assets",
  tags=["assets"]
)

assets = AssetsFn()

@assetsRouter.post("/asset_status")
async def asset_status_api(items: assets_status_items, request: Request):
  if request.state.valid_token != True:
      return error_list(0)
  try:
      data = await assets.rate_check(items, request.state.bit, request.state.idx)
      return {"status":200, "data":data }
  except Exception as e:
      print("getPossessoionCoinInfo Error ::: :::", e)
      return error_list(2)
  
