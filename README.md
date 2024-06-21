# credentialDatabaseTokenAuth

---

Simple fastapi based python server for generating jwt auth tokens using username and passwords. Backed by a sqlite database with a relational set of 3 databases to track user information, permissions, and permission meaning. Run through openssl self certified certificates to enable https for local run.

### Usage (Non-Docker):

1. `conda create -n myenv python=3.9`
2. `conda activate myenv`
3. `pip install -r requirements.txt`
4. `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`
5. `python initial_db_creation.py`
6. `python main.py`
