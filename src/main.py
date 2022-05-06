import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

import os
import uvicorn
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv


load_dotenv()
server_private_key = '-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQChfh2NEGnsxzdb\n0uvdinUf8FRXyJ/10r9B6zLFK9C8jcrwV/8xOg2bGobPguvS2/xWnVQ4JmWupTMZ\nr7KWKPT8zxpdkyOGcoytFswbA7p5leDYfoGaqgCwfVCAtKGrfycyztR892ubzS8f\nmwo4k4c7Dh5On0ozCA23Uk7Q1F74mAjis/l+8k1m6JZtEJATVnQMAwosei5xhR/N\n+SKTsT2PI7oGD6UFPo03LnqQjU6HImAU5ZxllTGBD16jiVTwFg61lOSEjoYzx+do\nY1zVlu34rfmWcboHw6MhUn4GC1BZttHKRtydHr7wlTGi+plQCfvCw44kVQf0Yion\ng3fIpQUbAgMBAAECggEAQRK4hacfh7GetPmA4XxxRbVpxxWonz2Uo9NKWfkV22Sn\nacGLqyJhaSZ/PA7dR9ItFBnBXf7a6kzXEnqh07AdR+GMFji8D+kIlpahGCGgem3S\ndGpFfzURogxc6//dRWWvPeHp7ZElY1qCqpGmxLVtwHYn8DZvh7CvFjesWqm4uyKk\nQIueRnixUhhaXa4fryaTNCwTdsVIFGLDz+u/Cryfy3DliwN1iQhw0BR563Wn0nnq\njyWBs5zFzttnKZLCuWzRdynEaRDOpm0bGxdNqusKKvunYBKNcomxkYjaln5Mu79n\nBWZ/mu2s4vOm/LsIaF1mQ+RhNpPCrYprwqVV6xhJAQKBgQDFFiccZUk/9TQ1lak4\n97FbuyIoa/iJ50VeEH4u9btYbZqbiGzURSO+W/wIS9B+T94QKJGtXg/5GYXFL/eS\n95ndJDbMn+t+KpEzpZcyfIJ2SCKhhWmkhfXFIoyG8+w5PoRLGMzdRV+J2JLfTXTk\nPk34+rnDXSD1lI+Azs6BgMpkawKBgQDRxC0FQIYn8KQ0RJeuTZr9iKU/aFKAiiTY\nIHD1GvBxHLh+dmn23NGUr98ixy8/qD5ekfqV1VvfB3BCT+Bue9zzaO52A5tvHEFP\n3yiF1o16MMJiHLko7F6KNR0r4+RGPPhVye33kt4653TFG5I4kKGULeqRDPPEzzdP\nzVW47sOOEQKBgQCxppBGlj36usn+6xKIWSyzpPDbQsfbdm4epfs31SS0RsewHr8K\nb/ASLNP3nm8nDFL8ebUmcr0vKoRcBCrDfRBiN7x1okkhhrkvtrmdNoJaoBcnRRy+\nwkmREt1c4A40Y1fYYVh4s4m0tVVel3EgM9EQ9t/va8jD1M+tqbyXG0JUVQKBgCXs\nGVeBur8tugHZBLL2RLbhJT65VXD3iIGqG8G0BRPt5Uy3i6CdeyYuRWC8McaIW/4s\n1eiQkfNYHOtgFWrj6aX3qmSbclY7/XK7HVBU4W7dscaa+r5zPQQvZf6xTGuGSj74\nKpU/b/2mKm4X9e9T9mIbivR+KvPBonZC4OR2BdSBAoGBAIkc338R3cdFzqt/US2o\n8dxgN7OQ0yZCD1z2tKlxeDVB2I5iQmRJ6Z/NEg992DeREoR7hAld/rPHt1DHYV7r\nhrFKLMWo2XaT3JDnCR1AC0vcLXb/pol9X6U7a5ql0JSoj7/EvygwOonb/fWp4vLL\ntR1C+CFXkHks34WMzCbXB1g9\n-----END PRIVATE KEY-----\n'
client_public_key = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwfjyGYMFOVOKqXHuxPCa\nwZjZXuydkf0JaqD3ekxMVmAmSP2Ufur65mu2EiigCApwpLtEBTxh0rQB9+7/H+xM\nnK0Oq78tttYrwta5qzkgZzU+eyYgbaNBuf0VzDbrp85PH3QNUjRx2jAQ2rSDkBCQ\nWSLRX5WHXIlsAW5u8h+n2clkpqArZxqNjkABC1lkazFNV2T8XjDBD4JvMqGQiSjl\n++rYxHid82k3r/dbLtQoNCa64CjXfRE97rMzgJyZV9tscXQJlAxyFRaIy+Hm/INJ\nAZhVsInrqYzh26/JIrzQA0/mj8rMU7pWnvjT2fJmSD2PUfqONCD0eRqBkJbBrqkH\n2wIDAQAB\n-----END PUBLIC KEY-----\n'


server_private_key = serialization.load_pem_private_key(server_private_key.encode(), password=None)
client_public_key = serialization.load_pem_public_key(client_public_key.encode())

app = FastAPI()

@app.post("/activate/")
async def activate(request: Request):
    encrypted_code_in = await request.body()
    code = decrypt(server_private_key, encrypted_code_in)
    encrypted_code_out = encrypt(client_public_key, code)
    return Response(content=encrypted_code_out)


def encrypt(public_key, message):
  ciphertext = public_key.encrypt(
      message,
      padding.OAEP(
          mgf=padding.MGF1(algorithm=hashes.SHA256()),
          algorithm=hashes.SHA256(),
          label=None
      )
  )
  return ciphertext


def decrypt(private_key, ciphertext):
  plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
  return plaintext


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