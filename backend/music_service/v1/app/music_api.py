from datetime import date
from typing import List
from databases import Database
import sqlalchemy
from sqlalchemy.dialects.postgresql import ARRAY
from fastapi import FastAPI, status, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from typing import Optional
from pydantic import BaseModel


DATABASE_URL = "postgresql://admin:admin@postgres/music_db"
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

class MyBaseModel(BaseModel):
    class Config:
        orm_mode = True

class Music(MyBaseModel):
    title: str
    author: list
    release_data: date
    keywords: list

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get(
    "/v1/musics/get_all_musics/",
    response_model=List[Music],
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

    return {"Status": "Success", "Musics": musics_list}


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
    query = filter(musics.c.title.like(keyword) | musics.c.keywords.like(f'%{keyword}%'))
    musics_list = await database.fetch_all(query)
    musics.query.filter

    return {"results": list(musics_list)}

'''@app.get(
    "/v1/musics/search/",
    status_code=status.HTTP_200_OK
)
def search(
    keyword: Optional[str] = None, max_results: Optional[int] = 10 
) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": musics[:max_results]}  # 6

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), List[Music])  # 7
    return {"results": list(results)}'''