"""
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""
# Enable Monocle Tracing
from monocle_apptrace import setup_monocle_telemetry
setup_monocle_telemetry(workflow_name = 'employee-teams-basic-bot', monocle_exporters_list = 'okahu')

from http import HTTPStatus

from aiohttp import web
from botbuilder.core.integration import aiohttp_error_middleware

from bot import bot_app

routes = web.RouteTableDef()

@routes.post("/api/messages")
async def on_messages(req: web.Request) -> web.Response:
    res = await bot_app.process(req)

    if res is not None:
        return res

    return web.Response(status=HTTPStatus.OK)

app = web.Application(middlewares=[aiohttp_error_middleware])
app.add_routes(routes)

from config import Config

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=Config.PORT)