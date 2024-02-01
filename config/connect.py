from logging import root
from pymysql import cursors, connect
from fastapi import Depends, FastAPI, Request
from auth.auth import AuthHandler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
import os
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
conp = connect(host='10.233.121.1', user="root", passwd="RL@2024",
               database="mydb", port=3306)

if (conp.connect):
    print("Database Connected")
else:
    print("Database Not Connected")
cursor = conp.cursor(cursors.DictCursor)

SECRET_KEY = "cairocoders-ednalan"

auth_handler = AuthHandler()

app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url="/api/v1/docs", redoc_url="/api/v1/redoc", title="KobkoiApi", description="Just only want money", version="1.0.0")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)