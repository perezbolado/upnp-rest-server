import json
import aiohttp_jinja2
from aiohttp import web

@aiohttp_jinja2.template('index.html')
async def index(request):
    locations = request.app['protocol'].get_locations()
    return {"locations": locations.values()}