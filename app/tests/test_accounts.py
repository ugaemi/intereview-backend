# import pytest
# from httpx import AsyncClient
#
#
# @pytest.mark.asyncio
# async def test_create_new_user():
#     async with AsyncClient(base_url="http://localhost:8000") as ac:
#         response = await ac.post(
#             "/api/v1/accounts/",
#             json={
#                 "username": "tester@naver.com",
#                 "name": "테스터",
#                 "password": "test1234!",
#                 "phone": "+821012345678",
#             },
#         )
#         assert response.status_code == 200
