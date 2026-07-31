from system_base import RolePlayingSystem
from fastapi import FastAPI

def create_app(engine: RolePlayingSystem):

    app = FastAPI()

    @app.post("/roll")
    def roll(request):
        return engine.roll(request)

    @app.get("/metadata")
    def metadata():
        return engine.metadata()

    return app
