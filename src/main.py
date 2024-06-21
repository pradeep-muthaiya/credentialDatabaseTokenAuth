import sqlite3
import ssl
from fastapi import FastAPI, HTTPException
import uvicorn
from dtos.InputOutputs import UserNamePassword
import jwt
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/")
def health_check():
    return "healthy"

@app.post("/get_token")
def get_token(data: UserNamePassword):
    connection = sqlite3.connect("../src/creds.db")
    cursor = connection.cursor()
    username, password =data.username, data.password
    cursor.execute(f"SELECT * FROM credentials WHERE username='{username}' AND password='{password}'")
    user_record = cursor.fetchall()
    if len(user_record) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        user_id = user_record[0][0]
        cursor.execute(f"SELECT * FROM permissions WHERE userid='{user_id}'")
        user_id = user_record[0][0]
        cursor.execute(f"SELECT pl.rolename FROM permissions p LEFT JOIN permission_labels pl ON p.permissionid=pl.permissionid WHERE p.userid={user_id}")
        permission_records = cursor.fetchall()
        user_permissions = [permission[0] for permission in permission_records]
        record_creation = datetime.now()
        data = {
            "user_id": user_record[0][0],
            "user_firstName": user_record[0][1],
            "user_lastName": user_record[0][2],
            "user_permissions": user_permissions,
            "created_at": record_creation.strftime("%m/%d/%Y, %H:%M:%S"),
            "expires_at": (record_creation + timedelta(days=1)).strftime("%m/%d/%Y, %H:%M:%S")
        }
        token = jwt.encode(data, "simple_token", algorithm="HS256")
        cursor.close()
        connection.close()
        return {
            "token": token,
            "created_at": record_creation.strftime("%m/%d/%Y, %H:%M:%S"),
            "expires_at": (record_creation + timedelta(days=1)).strftime("%m/%d/%Y, %H:%M:%S")
        }

if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain('cert.pem', keyfile='key.pem')
    uvicorn.run("main:app", host="127.0.0.1", port=8000, ssl_keyfile='./key.pem', ssl_certfile="./cert.pem")