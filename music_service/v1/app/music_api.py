import os

from datetime import date
from typing import List
from databases import Database
import sqlalchemy 
from sqlalchemy.dialects.postgresql import ARRAY
from fastapi import FastAPI, status, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from typing import Optional

from schema import Music


DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

musics = sqlalchemy.Table(
    "musics",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", ARRAY(sqlalchemy.String)),
    sqlalchemy.Column("release_data", sqlalchemy.DATE),
    sqlalchemy.Column("keywords", ARRAY(sqlalchemy.String)),
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get(
    "/v1/musics/get_all_musics/",
    status_code=status.HTTP_200_OK,
)
async def get_all_musics():
    query = musics.select()
    musics_list = await database.fetch_all(query)

    if not musics_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No music",
        )

    return musics_list


@app.get(
    "/v1/musics/get_one_music/{music_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_one_music(music_id: int):
    query = musics.select().where(musics.c.id == music_id)

    one_music = await database.fetch_one(query)
    if not one_music:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No music with this id: `{music_id}` found",
        )

    return {"Status": "Success", "Music": one_music}


@app.post(
    "/v1/musics/create_music/",
    response_model=Music,
    status_code=status.HTTP_201_CREATED,
)
async def create_music(music: Music):
    query = musics.insert().values(title=music.title, 
                                   author=music.author, 
                                   release_data=music.release_data,
                                   keywords=music.keywords
    )
    last_record_id = await database.execute(query)

    return {**music.dict(), "id": last_record_id}


@app.put(
    "/v1/musics/update_music/{music_id}/",
    response_model=Music,
    status_code=status.HTTP_200_OK,
)
async def update_music(music_id: int, music: Music):
    query = musics.select().where(musics.c.id == music_id)
    one_music = await database.fetch_one(query)

    if not one_music:
           raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No music with this id: {music_id} found",
        )
    
    #verificar se o campo tem alteração
    query = (
        musics.update()
        .where(musics.c.id == music_id)
        .values(title=music.title)
    )

    await database.execute(query)
    
    return {**music.dict(), "title": music.title}

@app.delete("/v1/musics/delete_music/{music_id}/", status_code=status.HTTP_200_OK)
async def delete_music(music_id: int):
    query = musics.select().where(musics.c.id == music_id)
    one_music = await database.fetch_one(query)

    if not one_music:
           raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No music with this id: {music_id} found",
        )

    query = musics.delete().where(musics.c.id == music_id)
    await database.execute(query)

    return {"Status": "Success", "Message": "Music deleted successfully"}

@app.get(
    "/v1/musics/search/",
    status_code=status.HTTP_200_OK
)
async def search_music(keyword: Optional[str] = None) -> dict:
    query = musics.select().where(sqlalchemy.or_(
        musics.c.keywords.any(keyword),
        musics.c.title.like(f'%{keyword}%'),
        musics.c.author.any(keyword),
    ))
    musics_list = await database.fetch_all(query)

    return {"results": list(musics_list)}