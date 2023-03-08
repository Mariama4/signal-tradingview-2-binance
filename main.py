from aiohttp import web
from binance_handler import *

routes = web.RouteTableDef()
app = web.Application()


@routes.post('/alert-hook')
async def alert(request):
    await sendNewOrder()
    return web.Response(text='')

if __name__ == "__main__":
    app.add_routes(routes)
    web.run_app(app, port='80')
