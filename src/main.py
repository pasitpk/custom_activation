import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

import os
import uvicorn
from cryptography.fernet import Fernet
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv


load_dotenv()
decrypt_key = os.getenv("DECRYPT_KEY").encode()
encrypt_key = os.getenv("ENCRYPT_KEY").encode()

decryptor = Fernet(decrypt_key)
encryptor = Fernet(encrypt_key)

app = FastAPI()

@app.post("/activate/")
async def activate(request: Request):
    data = await request.json()
    encrypted_code_in = data['code'].encode()
    code = decryptor.decrypt(encrypted_code_in)
    encrypted_code_out = encryptor.encrypt(code).decode()
    return {'code': encrypted_code_out}

if __name__ == "__main__":
    
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    ssl_keyfile = os.getenv("SSL_KEYFILE")
    ssl_certfile = os.getenv("SSL_CERTFILE")
    ssl_keyfile_password = os.getenv("SSL_KEYFILE_PASSWORD")

    if host.startswith('http://'):
        host = host[7:]
    elif host.startswith('https://'):
        host = host[8:]
        
    uvicorn.run(app, 
                host=host, 
                port=int(port), 
                ssl_keyfile=ssl_keyfile if ssl_keyfile else None, 
                ssl_certfile=ssl_certfile if ssl_certfile else None,
                ssl_keyfile_password=ssl_keyfile_password if ssl_keyfile_password else None,
                )