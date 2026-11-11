def test_quote_create_and_retrieve(client):
    response=client.post('/procurement/quotes',json={
        'sku':'CHAIN-01','quantity':2,'zone':'local','promotion_code':'DEPOT10'})
    assert response.status_code==201
    obj=response.json()
    assert obj['subtotal_cents']==2598
    assert obj['total_cents']==2598-259+150
    assert client.get('/procurement/quotes/'+obj['quote_id']).json()==obj

def test_quote_unknown_product(client):
    assert client.post('/procurement/quotes',json={
        'sku':'NONE','quantity':1,'zone':'local'}).status_code==404

def test_quote_quantity(client):
    assert client.post('/procurement/quotes',json={
        'sku':'CHAIN-01','quantity':0,'zone':'local'}).status_code==422

def test_quote_unknown_id(client):
    assert client.get('/procurement/quotes/invalid').status_code==404
