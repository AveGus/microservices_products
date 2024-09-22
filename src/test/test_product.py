import json
from test.conftest import client


def client_json_load(name):
    result = json.loads(name.content.decode("utf-8"))
    return result


async def test_add_product(product_type):
    response = client.post("api/products", json={
        "name": "burger",
        "product_type_id": 1
    })
    result = client_json_load(response)
    assert response.status_code == 200
    assert result["product_type"]["name"] == product_type.name
    assert result["product_type_id"] == product_type.id


async def test_get_product(product):
    all_products = client.get("api/products")
    result = client_json_load(all_products)
    assert len(result) == 1
    assert result[0]["id"] == product.id


def test_get_product_by_id(product):
    all_product_by_id = client.get("api/products/1")
    result = client_json_load(all_product_by_id)
    assert result[0]["id"] == product.id
    assert result[0]["name"] == product.name


def test_get_product_by_typeID(product):
    product_by_typeID = client.get("api/products/type/1")
    result = client_json_load(product_by_typeID)
    assert len(result) == 1
    assert result[0]["product_type_id"] == product.product_type.id
    assert result[0]["product_type"]["name"] == product.product_type.name
