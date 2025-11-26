import requests
import redis
import json

redis_client = redis.Redis()
TTL = 60


API_KEY = '5a7b2aabf55b8fd8c04d560f588c9cdc'
CACHE_KEY = 'currency'

def get_rates():
    cached = redis_client.get(CACHE_KEY)

    if cached:
        return json.loads(cached)

    response = requests.get(f'https://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&format=1')
    data = response.json()
    redis_client.setex(CACHE_KEY, TTL, json.dumps(data))

    return data

def get_eur_rate():
    data = get_rates()

    eur_rate = data['rates']['RUB']

    return round(eur_rate, 2)

def get_usd_rate():
    data = get_rates()

    rub_rate = data['rates']['RUB']
    usd_rate = data['rates']['USD']

    rate = rub_rate / usd_rate

    return round(rate, 2)



