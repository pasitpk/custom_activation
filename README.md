# custom_activation

## example of activation
<a href="https://colab.research.google.com/drive/1qI7oDPFtEwO4i6zlJRC8HhGvfQA_EEad?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
```python
import os
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

activation_server_url = 'https://test.pasitpk.app/activation2/activate/'  # https://github.com/pasitpk/custom_activation
client_private_key = '-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQDB+PIZgwU5U4qp\nce7E8JrBmNle7J2R/QlqoPd6TExWYCZI/ZR+6vrma7YSKKAICnCku0QFPGHStAH3\n7v8f7EycrQ6rvy221ivC1rmrOSBnNT57JiBto0G5/RXMNuunzk8fdA1SNHHaMBDa\ntIOQEJBZItFflYdciWwBbm7yH6fZyWSmoCtnGo2OQAELWWRrMU1XZPxeMMEPgm8y\noZCJKOX76tjEeJ3zaTev91su1Cg0JrrgKNd9ET3uszOAnJlX22xxdAmUDHIVFojL\n4eb8g0kBmFWwieupjOHbr8kivNADT+aPysxTulae+NPZ8mZIPY9R+o40IPR5GoGQ\nlsGuqQfbAgMBAAECgf88IL5c+TDEhxgkfgKDqjnxMd+uzbv9IzJsy65jf8Rfh6hx\nOp3CXIHrKc0D7rVTyMLa/8A5u6hHGewVNkxphxSwynw59DObsVIvi8AGvEYBNxvf\n72elyAVJ5OdHvUrOZRg4FOLLrLsqbz8+AmtCmrWM4xGdrItvHUlf4zTD2VN4LskF\nNWzDaPjeYQVwAx2vxd3oWvoXRjlMrkyrPKdnRkuWJkINRYG325B34WNx+c9X2n5s\nu/w7jBRWZKrOtxIY5rkTG12qOoaXC9+7FUA4IVp8LCFrECBmxtvCTPVoA6GVQ7tK\ng156H81zt/yBHb2p6RmPEmuPBG3h/Dcr2D+MAJECgYEA3xU2u7dK19L+uCLWTHew\nittgnlrtpN12/vuoNmC1vn3khAUMvF98iQCqjRdS9tMQSsW+6BmGKR6xeor7WUUx\nqUWhmff2wEMW+mLWbAKVrVYdRb1RcVkNI95gYv4IJLmNlrU5YL2KmwxuL/aeSy2G\nb71qwef1Md1NPA1wNdFZTo0CgYEA3pgbllHzLdjzfOQOaHpB2YHroiQrfDBN7I/S\nlMvUSaFk3Kd32kofhsDpkkXgjyMOmq+O3/uiFkAlwPrgXe+iAtBq2bxrB6eP0Pdv\nGFpnGpxKn2/Y4ykBX0w2I0KAEDoiRYiYxbE8aGQ60kuaSR4yODz9t1s54Zdvbhpv\ngIfX6gcCgYAzdQQ8BoqIAA5rUPXXi6A4V2QRAu5gIgmJxWjGqkYh244zeaq3ZNso\nCvRMOT4U2xid9sETbpfIsmDD4H0b2V8cKYieKFlNfew180h8f5gg9IUqCgJYP+9M\n/8WB8BDWz8o+Ii1LCE2JeDOOcreOpcCl065lbejcCK0BFiR09YZBHQKBgQDETxWV\nXrS+rGUgsehbD+dfMgtjtc57+gXfKYAoJhMU1LelOjSjWVewehYEIIhI9Dv/A/FX\nbA6o3O3u4dJaRep13OU/HcKuv4JAYtehfKkNeOT+858tx44kQ4xDUHSs2vg6pptF\nTmfeEPcnW/G3pl/X5UJFILlNUUa+raXEjwlGpQKBgGitsyXHBegew1h4YKlRW024\nAOFFb5Cx6kvuAsdhtKnd7QiLppskt4+rVXU7PeZibUzLqt/s19nSOleWePC5mqBA\nEfPr26uGjkAnODTFJpgQE1HADqRGNvAR/btzl8G2GOmSIfCPK4gPpOG3+m/UjoXU\nVmY4+evndRJeFBV127A4\n-----END PRIVATE KEY-----\n'
server_public_key = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoX4djRBp7Mc3W9Lr3Yp1\nH/BUV8if9dK/QesyxSvQvI3K8Ff/MToNmxqGz4Lr0tv8Vp1UOCZlrqUzGa+ylij0\n/M8aXZMjhnKMrRbMGwO6eZXg2H6BmqoAsH1QgLShq38nMs7UfPdrm80vH5sKOJOH\nOw4eTp9KMwgNt1JO0NRe+JgI4rP5fvJNZuiWbRCQE1Z0DAMKLHoucYUfzfkik7E9\njyO6Bg+lBT6NNy56kI1OhyJgFOWcZZUxgQ9eo4lU8BYOtZTkhI6GM8fnaGNc1Zbt\n+K35lnG6B8OjIVJ+BgtQWbbRykbcnR6+8JUxovqZUAn7wsOOJFUH9GIqJ4N3yKUF\nGwIDAQAB\n-----END PUBLIC KEY-----\n'

client_private_key = serialization.load_pem_private_key(client_private_key.encode(), password=None)
server_public_key = serialization.load_pem_public_key(server_public_key.encode())

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
  
def activate():
    code = Fernet.generate_key()  # byte string
    encrypted_code = encrypt(server_public_key, code)
    res = requests.post(activation_server_url, data=encrypted_code)
    if res.status_code == 200:
        encrypted_code = res.content  # convert to byte for decryption
        decrypted_code = decrypt(client_private_key, encrypted_code)
        if decrypted_code == code:
            return True
    return False
 
if activate():
  print('Successfully activated')
  """
  For model encryption and decryption, please refer to 'https://colab.research.google.com/drive/17gU3n5yKciO5tVcESZCU3bHOtAlHXqV-?usp=sharing'
  """
  # model = onnxruntime.InferenceSession(decrypt_file(encrypted_model_file, model_decrypt_key))
else:
  print('Activation failed')

```

## model encryption & decryption
For model encryption and decryption, please refer to <a href="https://colab.research.google.com/drive/17gU3n5yKciO5tVcESZCU3bHOtAlHXqV-?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
