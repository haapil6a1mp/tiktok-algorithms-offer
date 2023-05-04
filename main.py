
#!encoding=utf8
import ast
import base64
import json
from typing import Optional

import requests
from fastapi import FastAPI, Form, Response
from pydantic import BaseModel

from lib.Captcha import PuzzleSolver
from lib.TTEncrypt import TT
from lib.XGorgon import XGorgon
from lib.Xlog import XLOG


class XGorgonDict(BaseModel):
    params: str
    headers: dict


class PostBase64Dict(BaseModel):
    base64: str


app = FastAPI()


@app.post("/captcha")
def captcha(puzzle: str = Form(...), piece: str = Form(...)):
    try:
        base64puzzle = base64.b64encode(
            requests.get(puzzle).content)
        base64piece = base64.b64encode(
            requests.get(piece).content)
        solver = PuzzleSolver(base64puzzle=base64puzzle,
                              base64piece=base64piece)
        return {"x": solver.get_position()}
    except Exception as e:
        print(e)
        return None


@app.post('/x-gorgon')
def x_gorgon(req: XGorgonDict):
    try:
        xg = XGorgon()
        return xg.calculate(req.params, req.headers)
    except Exception as e:
        print(e)
        return None


@app.post('/tt_encrypt')
def tt_encrypt(req: PostBase64Dict):
    try:
        lib = TT()
        body = str(base64.b64decode(req.base64))
        data = lib.encrypt(body)
        return {"base64": base64.b64encode(data)}
    except Exception as e:
        print(e)
        return None


@app.post('/tt_decrypt')
def tt_encrypt(req: PostBase64Dict):
    try:
        ttencrypt = TT()
        body = base64.b64decode(req.base64)
        data = ttencrypt.decrypt(body)
        return Response(data, headers={"Content-Type": 'application/json'})
    except Exception as e:
        return None


@app.post('/xlog_encrypt')
def tt_encrypt(req: PostBase64Dict):
    try:
        lib = XLOG()
        body = str(base64.b64decode(req.base64))
        data = lib.encrypt(body)
        return {"base64": base64.b64encode(data)}
    except Exception as e:
        print(e)
        return None


@app.post('/xlog_decrypt')
def tt_encrypt(req: PostBase64Dict):
    try:
        lib = XLOG()
        body = base64.b64decode(req.base64)
        data = lib.decrypt(body)
        return Response(data, headers={"Content-Type": 'application/json'})
    except Exception as e:
        print(e)
        return None


# Start ASGI Server
# uvicorn main:app --reload --host 0.0.0.0 --port 8100
