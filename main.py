# import libraries here
from fastapi import FastAPI, Response
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "From Tangwen Zhu (tz2570): Hello World -- this will be NFL focused later."}

@app.get("/players/{player_id}")
async def player_hello_text(player_id: str):
    the_message = f"Hello player {player_id}, more details later"
    rsp = Response(content=the_message, media_type="text/plain")
    return rsp

if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000) # local machine
    uvicorn.run(app, host="0.0.0.0", port=8000)
