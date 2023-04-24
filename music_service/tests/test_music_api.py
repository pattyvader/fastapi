import json

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from asgi_lifespan import LifespanManager

from app.music_api import app


@pytest.mark.asyncio
async def test_get_all_musics():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/v1/musics/get_all_musics/")

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_one_music():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/v1/musics/get_one_music/1/")

        assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_one_music_error():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/v1/musics/get_one_music/0/")

        assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_music():
    new_music =  {"title": "Teste",
                  "author": "teste"
    }
    json_object = json.dumps(new_music)

    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = client.post("/v1/musics/create_music/", json = json_object)

    print(response)

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_music():
    update_music =  {"title": "Teste",
                     "author": "teste"
    }

    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = client.put("/v1/musics/update_music/1/", json = update_music)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_music():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = client.delete("/v1/musics/delete_music/1/")

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_music_error():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = client.delete("/v1/musics/delete_music/0/")

    assert response.status_code == 404