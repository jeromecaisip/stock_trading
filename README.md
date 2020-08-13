### Setup

1. Install `docker` and `docker-compose` and `make` utility.

2. On the root directory run `make dev-up`.

3. Generate mock data by running `make dev-generate-mock-data`
   username is `test@example.com` and password is `test`.
   
4. Run test `make dev-test`

### Usage
#### You can both use session for browseable API (for dev environment only) and [token authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication). 

Browseable API:

1. Go to `http://localhost:8000/api/v1/orders/`. Login with the credentials.

Token Authentiation:
2. See [DRF's documentation](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication). 


### ENDPOINTS
1. After getting authentication token get user's trader_id in `http://localhost:8000/api/users/me/`. 

2. Create and order: 

    POST `/api/v1/orders/`
    
    json {'transaction_type': <string:B|S> , 
    'stock':,<int:stock_id>, 
    'num_shares': <int>, 
    'traded_at': <int_with_two_decimal>,
    'trader': <user_trader_id> },

3. Total spent on buying: GET `/api/v1/orders/order_value?transaction_type=B`

4. Total spent on single stock: GET `/api/v1/orders/order_value?transaction_type=B&stock=<stock_id>`.


You can check out the unit tests in `api/v1/tests.py` for more details.
