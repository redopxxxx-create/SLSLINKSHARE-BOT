# +++ Modified By @itsryosudhish [SLS Bots] +++
# Original Logic by Codeflix Bots

from aiohttp import web
from .route import routes

async def web_server():
    # web_app initialize ho raha hai routes ke saath
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

# Note: Yeh file 'plugins' folder ke andar hona zaruri hai 
# taaki bot start hote waqt routes ko recognize kar sake.
