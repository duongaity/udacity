# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Documenting Endpoints

### Endpoints

**GET /categories**

General:

-   Returns a list of drinks and it should contain drink.short() data, success value

-   Sample: `curl http://127.0.0.1:5000/drinks`

-   Result :

```
{
  "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
   "success": true
}
```

**GET /drinks-detail**

General:

-   Returns a list of drinks and drink.long() data, success value.

Sample `curl http://127.0.0.1:5000/drinks-detail`

```
{
  "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "water"
        }
    ],
    "success": true
}
```

**POST /drinks**

General:

-   Creates a new drink using the title, recipe. Returns status code 200, success value

-   Sample: `curl http://127.0.0.1:5000/drinks -X POST -H "Content-Type: application/json" -d '"recipe": [
    {
        "color": "blue",
        "parts": 1
    },
    {
        "color": "red",
        "parts": 2
    }
],
"title": "milk"`

-   Result

```
{
   "drinks":[
      "recipe": [
        {
            "color": "blue",
            "parts": 1
        },
        {
            "color": "red",
            "parts": 2
        }
      ],
      "title": "milk"
   ]
  "success": True,
}
```

**POST /drinks/{id}**

General:

-   Update a new drink using the title, recipe. Returns status code 200, success value

-   Sample: `curl http://127.0.0.1:5000/drinks/1 -X PATCH -H "Content-Type: application/json" -d '"recipe": [
    {
        "color": "blue",
        "parts": 1
    },
    {
        "color": "red",
        "parts": 2
    }
],
"title": "milk"`

-   Result

```
{
   "drinks":[
      "recipe": [
        {
            "color": "blue",
            "parts": 1
        },
        {
            "color": "red",
            "parts": 2
        }
      ],
      "title": "milk"
   ]
  "success": True,
}
```

**DELETE /drinks/{id}**

General:

-   Update a new drink using the title, recipe. Returns status code 200, success value

-   Sample `curl -X DELETE http://127.0.0.1:5000/drinks/1`
-   Result

```
{
   "delete": 1,
   "success": True,
}
```
