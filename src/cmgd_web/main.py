import logging
import typing
import json
from importlib.metadata import entry_points

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .config import LOGLEVEL
from .models import metadata

logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)

def load_modules(app=None):
    """Pull in modules from entry_points

    Modules are defined in pyproject.toml. Each
    module is first loaded (imported). If there is
    an init_app() function in the loaded module,
    it is run next. The init_app() is used to add
    a router to the app, for example.
    """
    for ep in entry_points()["cmgd_web.modules"]:
        print(ep)
        logger.info("Loading module: %s", ep.name)
        mod = ep.load()
        if app:
            init_app = getattr(mod, "init_app", None)
            if init_app:
                # typically, init_app looks like:
                #
                # def init_app(app):
                #    app.include_router(router, prefix='/samples')
                init_app(app)

class JSONResponder(JSONResponse):

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(content,allow_nan=True).encode('UTF-8')

def get_app():
    app = FastAPI(title="Curated Metagenomics Web Portal and API",
                  default_response_class = JSONResponder)
    load_modules(app)
    return app
