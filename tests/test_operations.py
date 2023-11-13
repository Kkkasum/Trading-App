from datetime import datetime

from httpx import AsyncClient


async def test_add_operation(ac: AsyncClient):
    response = await ac.post('/operations', json={
        "id": 1,
        "quantity": "25.5",
        "figi": "figi_CODE",
        "instrument_type": "bond",
        "date": datetime.utcnow(),
        "type": "Выплата купонов",
    })

    assert response.status_code == 200, "Операция не добавилась"


async def test_get_operation(ac: AsyncClient):
    response = await ac.get('/operations', params={
        "operation_type": "Выплата купонов",
    })

    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert len(response.json()['data']) == 1
