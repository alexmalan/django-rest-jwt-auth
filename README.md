Django REST API JWT Auth
========================

### Description
-   Product management API with JWT authentication;
-   Django generic permission system integrated;
-   Custom exception handlers;
-   Best practices for configuration split and project structure;

### Workflow
1.  A user is REGISTERed in the database.
2.  In order to LOGIN, we pass username and password in the request payload.
3.  The request will retrieve an ACCESS token and a REFRESH token.
4.  The ACCESS token will be passed in all the other request headers as value for 'Authorization' key. It has to start with 'Bearer' followed by a space and then the key. This way someone can access resources that require authentication.
5.  Once a certain time interval passes, the ACCESS token will be invalid.
6.  In order to get a new ACCESS token we will send a request that takes the REFRESH token previously generated as payload.
7.  The result of the call will be a new access token with the same time interval validity.
8.  When a user performs a log out, we blacklist both ACCESS and REFRESH tokens in order for them to not be used further.

*  Note: If the REFRESH token is lost then the user will require to do a new LOGIN request after the ACCESS token expires. 

## Code quality

### Static analysis
- Static code analysis used: https://deepsource.io/

### Pylint
- Pylint used to maintain code quality;
- Current status: `Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)`

## Requirements

-   It is assumed that you have Python. If not, then download the latest versions from:
    * [Python](https://www.python.org/downloads/)
    * [PostgreSQL](https://www.postgresql.org/download/)
    
## Installation

1. **Clone git repository**:
    ```bash
    git clone https://github.com/alexmalan/django-rest-basic-auth.git
    ```

2. **Create virtual environment**
    ```bash
    python -m venv $(pwd)/venv
    source venv/bin/activate
    ```   

3. **Install requirements**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Add environment variables**
    - Create a file named `.env` in project root directory
    - Add and fill next environment variables with your local database config:
        ```.env
        SECRET_KEY=
        DATABASE_NAME=
        DATABASE_USER=
        DATABASE_PASSWORD=
        DATABASE_HOST=
        DATABASE_PORT=
        ```

5. **Make migrations**:
    ```bash
    python manage.py makemigrations
    ```

6. **Migrate**:
    ```bash
    python manage.py migrate
    ```

## Run

-   Run APP using command:
    ```bash
    python manage.py runserver <optional_port_id>
    ```
- Localhost resources:
    localhost:<port_id>/admin/ - admin login page
    localhost:<port_id>/api/   - endpoints
    
## Postman Configuration

### Library Import
* Find the product_management.postman_collection.json in the root directory
- Open Postman
   - File
      - Import
         - Upload files
            - Open

### Environment
* Environments
   - Add
      - Variable: csrftoken
      - Variable: access
      - Variable: refresh
      - Type - all: default
   - Save

- In order to set the CSRF token and retrieve the JWT ACCESS and REFRESH tokens in the environment you have to send a
   * REGISTER request - register a user
   * LOGIN request - login a user


## Files
* `core` - Django settings files
* `common/` - Django common functionality
* `apps/` - Back-end code
* `venv/` - Virtual environment files used to generate requirements;

    
## Test
Run command:
* python manage.py test -k --verbosity 2
* python manage.py test {app_name} -k --verbosity 2
    * [Important] 
        * To use same database for test and development `-k ( -keepdb )`
            - otherwise, django will try to create a separate new db '{db_name}_test'
        * Optional `--verbosity 2`
            - displays the result foreach test
        * If tests are not working make sure all migrations are done : 
            `python manage.py migrate`
