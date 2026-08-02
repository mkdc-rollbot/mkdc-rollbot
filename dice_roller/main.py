import asyncio

from fastapi import FastAPI
from parser import parse_roll
from roller import roll_die

app = FastAPI()

@app.post("/roll/{roll_str}")
async def roll(roll_str: str):
    roll_command = await parse_roll(roll_str)
    roll_results = await roll_die(roll_command)
    return {'data': roll_results}
