from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 
import uvicorn


def initialize_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount("/static", StaticFiles(directory="./image"), name="static")
    from controller.mgmt import router as mgmt_router
    app.include_router(mgmt_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}
    
    return app

app = initialize_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
