import pytest
import json
from fastapi.testclient import TestClient
from httpx import AsyncClient
from asgi_lifespan import LifespanManager

from app.ingest_files_api import app


@pytest.mark.asyncio
async def test_get_all_movies():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/v1/movies/get_all_movies/")

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_one_movie():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/v1/movies/get_one_movie/1/")

        assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_one_movie_error():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/v1/movies/get_one_movie/0/")

        assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_movie():
    new_movie =  {"title": "Star Wars: Episode IV - A New Hope",
                "genres": "Action|Adventure|Fantasy"
    }
    json_object = json.dumps(new_movie)

    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = client.post("/v1/movies/create_movie/", json = json_object)

    print(response)

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_movie():
    update_movie =  {"title": "Star Wars: Episode IV - A New Hope",
                "genres": "Action|Adventure|Fantasy"
    }

    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = client.put("/v1/movies/update_movie/1/", json = update_movie)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_movie():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = client.delete("/v1/movies/delete_movie/1/")

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_movie_error():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = client.delete("/v1/movies/delete_movie/0/")

    assert response.status_code == 404