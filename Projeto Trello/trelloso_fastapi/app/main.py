from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    router_auth,
    router_board, 
    router_tag,
    router_user,
    router_board,
    router_list,
    router_card,
    router_cardcomment,
    router_cardtag,
    router_cardmember
)
from app.engine import create_db_and_tables, get_settings
from app.import_data import  insert_test_data


origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "*"
]

api_router = APIRouter()
api_router.include_router(router_auth, prefix="/auth", tags=["auth"])
api_router.include_router(router_user, prefix="/users", tags=["users"])
api_router.include_router(router_tag, prefix="/tags", tags=["tags"])
api_router.include_router(router_board, prefix="/boards", tags=["boards"])
api_router.include_router(router_list, prefix="/lists", tags=["lists"])
api_router.include_router(router_card, prefix="/cards", tags=["cards"])
api_router.include_router(router_cardcomment, prefix="/card_comments", tags=["card_comments"])
api_router.include_router(router_cardmember, prefix="/card_members", tags=["card_members"])
api_router.include_router(router_cardtag, prefix="/card_tags", tags=["card_tags"])

app = FastAPI(title=get_settings().fastapi_title)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=get_settings().api_router_prefix)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    insert_test_data()

