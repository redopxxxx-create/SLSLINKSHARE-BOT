from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    # Yeh response web browser pe dikhega jab koi aapka app URL open karega
    return web.json_response("SLS Bots - Advanced Links Sharing System")

# +++ Modified By @itsryosudhish [SLS Bots] +++
# This file is essential for the web-server to keep the bot alive.
