# Foodgram — grocery assistant
------------


The service is created to host recipes for various dishes.
Here you can:
- Create or edit your recipes
- Explore other users recipes, add them to favorites or shopping cart
- Subscribe to users and be among the first to learn about new entries
- Download the list of ingredients needed to prepare the dishes in the basket

# Available endpoints 

------------


# Users
## Registration
```
POST http://<host>/api/users/

{
    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkin",
    "first_name": "Vasya",
    "last_name": "Pupkin",
    "password": "Qwgja2f12pz3"
}
```
## Password change
```
POST http://<host>/api/users/set_password/

{
    "new_password": "string",
    "current_password": "string"
}
```
## Get authorization token
```
POST http://<host>/api/auth/token/login/

{
    "password": "string",
    "email": "string"
}
```
## Delete authorization token
Authorization: Token TOKENVALUE
```
POST http://<host>/api/auth/token/logout/
```
## Get current user info
```
GET http://<host>/api/users/me/
```
## Get user info
```
GET http://<host>/api/users/{id}/
```
## Get users info
```
GET http://<host>/api/users/
```
## Get my subscriptions
Authorization: Token TOKENVALUE

Query params:
- page (integer) — number of page to show
- limit (integer) — limit of objects on page
- recipes_limit (integer) — limit of recipes nested in objects on page

```
GET http://<host>/api/users/subscriptions/
GET http://<host>/api/users/subscriptions/?page=3
GET http://<host>/api/users/subscriptions/?limit=2
GET http://<host>/api/users/subscriptions/?recipes_limit=3
```
## Subscribe to user
Authorization: Token TOKENVALUE

Query params:
- recipes_limit (integer) — limit of recipes nested in object on page

```
POST http://<host>/api/users/{id}/subscribe/
POST http://<host>/api/users/{id}/subscribe/?recipes_limit=5
```
## Unsubscribe from user
Authorization: Token TOKENVALUE

```
DELETE http://<host>/api/users/{id}/subscribe/
```
# Tags
## Get tags
```
GET http://<host>/api/tags/
```
## Get tag
```
GET http://<host>/api/tags/{id}/
```
# Ingredients
## Get ingredients
Query params:
- name (string) — search by partial occurrence at the beginning of the ingredient name.

```
GET http://<host>/api/ingredients/
GET http://<host>/api/ingredients/?name=лу
```
## Get ingredient
```
GET http://<host>/api/ingredients/{id}/
```
# Recipes
## Get recipes
Query params:
- page (integer) — number of page to show
- limit (integer) — limit of objects on page
- is_favorited (integer 0 or 1) — show only favorite recipes
- is_in_shopping_cart (integer 0 or 1) — show only recipes in shopping cart
- author (integer) — show only authors recipes
- tags (slug) — show recipes that have at least one of given tags

```
GET http://<host>/api/recipes/
GET http://<host>/api/recipes/?tags=breakfast&tags=dinner/
GET http://<host>/api/recipes/?author=3/
GET http://<host>/api/recipes/?page=3&limit=1&is_favorited=0/
```
## Get recipe
```
GET http://<host>/api/recipes/{id}/
```
## Create recipe
Authorization: Token TOKENVALUE
```
POST http://<host>/api/recipes/

{
    "ingredients": [
        {
            "id": 3,
            "amount": 300
        }
    ],
    "tags": [
        1,
        2
    ],
    "image": "base64 encoded image",
    "name": "string",
    "text": "string",
    "cooking_time": 1
}
```
## Update recipe
Authorization: Token TOKENVALUE

Allowed only for author.
```
PATCH http://<host>/api/recipes/{id}/

{
    "ingredients": [
        {
            "id": 3,
            "amount": 500
        }
    ],
    "tags": [
        1
    ],
}
```
## Delete recipe
Authorization: Token TOKENVALUE

Allowed only for author.
```
DELETE http://<host>/api/recipes/{id}/
```
# Favorites
## Add recipe to favorites
Authorization: Token TOKENVALUE
```
POST http://<host>/api/recipes/{id}/favorite/
```
## Delete recipe from favorites
Authorization: Token TOKENVALUE
```
DELETE http://<host>/api/recipes/{id}/favorite/
```
# Shopping cart
## Add to shopping cart
Authorization: Token TOKENVALUE
```
POST http://<host>/api/recipes/{id}/shopping_cart/
```
## Delete from shopping cart
Authorization: Token TOKENVALUE
```
DELETE http://<host>/api/recipes/{id}/shopping_cart/
```
## Download shopping list
Filename is shop_list.txt

Authorization: Token TOKENVALUE
```
GET http://<host>/api/recipes/download_shopping_cart/
```