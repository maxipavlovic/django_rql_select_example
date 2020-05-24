## Setup
To test [Django-RQL](https://github.com/cloudblue/django-rql/) Select Operations, please, activate virtual environment and do the following:
```commandline
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data.json
python manage.py runserver
```

You can play with models in Django Admin, if you want:
```commandline
python manage.py createsuperuser
```

## Demo
To test how select works you can use curl or any of your favourite browsers.
Let's look at products collection.
```commandline
curl -s "127.0.0.1:8000/api/products/" | jq '. | length'
```
We will see that there are `3` items in collection. Let's add a filter and get all products, that start with "Connect".
```commandline
curl -s "127.0.0.1:8000/api/products/?like(name,Connect*)" | jq '.'
```
You will see the following result:
```json
[
  {
    "id": 1,
    "name": "Connect",
    "category": {
      "id": 1,
      "name": "Cloud Applications"
    }
  },
  {
    "id": 2,
    "name": "Connect Zapier Extension",
    "category": {
      "id": 1,
      "name": "Cloud Applications"
    }
  }
]
```
We have got `2` products, which is correct, but where the hell is company? Response really seems a little strange at first as in serializer we have the following fields `fields = ('id', 'name', 'category', 'company')`.
Don't worry, `company` is not missing. In declarative filtering configuration we have the following settings:
```python
{
    'namespace': 'company',
    'filters': ('id', 'name'),
    'hidden': True,  # This means that by default company will not be shown
    'qs': SelectRelated('company'),
}
```
Then, everything seems correct, but lets look what SQL is executed behind the scenes. To get SQL we could do the following query:
```commandline
curl -s "127.0.0.1:8000/api/products/?like(name,Connect*)&profile_sql=true"
```
Here is the result:
```sql
SELECT "example_product"."id", "example_product"."name", "example_product"."category_id", "example_product"."company_id", "example_category"."id", "example_category"."name" 
FROM "example_product"
 LEFT OUTER JOIN "example_category" ON ("example_product"."category_id" = "example_category"."id") 
WHERE "example_product"."name" LIKE 'Connect%' ESCAPE '\'
```
Awesome! RQL optimized our SQL query also, as there is no unneeded `INNER JOIN` for the company of the product.
Lets include `company` and see how library behaves.
```commandline
curl -s "127.0.0.1:8000/api/products/?like(name,Connect*)&select(company)" | jq '.'
```
Here is the expected result:
```json
[
  {
    "id": 1,
    "name": "Connect",
    "category": {
      "id": 1,
      "name": "Cloud Applications"
    },
    "company": {
      "id": 1,
      "name": "CloudBlue Connect"
    }
  },
  {
    "id": 2,
    "name": "Connect Zapier Extension",
    "category": {
      "id": 1,
      "name": "Cloud Applications"
    },
    "company": {
      "id": 1,
      "name": "CloudBlue Connect"
    }
  }
]
```
And the SQL behind it:
```sql
SELECT "example_product"."id", "example_product"."name", "example_product"."category_id", "example_product"."company_id", "example_category"."id", "example_category"."name", "example_company"."id", "example_company"."name" 
FROM "example_product" 
LEFT OUTER JOIN "example_category" ON ("example_product"."category_id" = "example_category"."id") 
INNER JOIN "example_company" ON ("example_product"."company_id" = "example_company"."id") 
WHERE "example_product"."name" LIKE 'Connect%' ESCAPE '\'
```
Seems everything is fine. Let's check if RQL also supports excluding of fields.

We will drop all filters and exclude `category` and `name` to get only the list of Product IDs.
```commandline
curl -s "127.0.0.1:8000/api/products/?select(-category,-name)" | jq '.'
```
Here is the expected result:
```commandline
[
  {
    "id": 1
  },
  {
    "id": 2
  },
  {
    "id": 3
  }
]
```
And the SQL behind it:
```sql
SELECT "example_product"."id", "example_product"."name", "example_product"."category_id", "example_product"."company_id" 
FROM "example_product"(
```
Perfect! That's what [Django-RQL](https://github.com/cloudblue/django-rql/) calls "Power of Select".

Of course, this demonstration is pretty simple and [Django-RQL](https://github.com/cloudblue/django-rql/) 
supports much more: for example, Annotations and Prefetch Related, nested optimizations, selects of exact nested fields, etc.

If you have any questions, feel free to contact me here or in:
* Telegram - [@mxmkol](https://t.me/mxmkol)
* LinkedIn - [@mxms](https://www.linkedin.com/in/mxms/)