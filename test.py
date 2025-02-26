from platformPrivate import BitThumbPrivate, UpbitPrivate
import asyncio

upbit = UpbitPrivate('y3u6sBy5biSoqDTEHGHguVM6J2U0hEJenGZgJl83','dlNVYJqhbxTibIHlITR6ubAoA7RnVHxRrV7HqyY1')
bithumb = BitThumbPrivate('aeda5f9da2474b1a374db964c23c0f1c','e9f80d26e7a60ba7e076161325eb2704')

# print(bithumb.getMyCoinList())
# print(bithumb.getMyCoinList())

# upbit.nowRateFn()
asyncio.run(upbit.nowRateFn(4))