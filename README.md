# custom_activation

## example of activation
<a href="https://colab.research.google.com/drive/1KLov5Zy8gaJDBCbfhxqRCEAHRq0OLcGl?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
```python
import requests
from cryptography.fernet import Fernet

activation_url = 'https://test.pasitpk.app/activation/activate/'  # https://github.com/pasitpk/custom_activation
encrypt_key = 'JmixbxpEWqqKKpA_xAdmhYFH1c7s_ZkMjK89JKO1mmY='  # generated using "Fernet.generate_key().decode()", must be the same as "decrypt_key" used in the activation server
decrypt_key = 'KxMEvdmQQ7bJhH2YaNHm2Cjkbi65eDjvmJ9trTJhcaM='  # generated using "Fernet.generate_key().decode()", must be the same as "encrypt_key" used in the activation server

encryptor = Fernet(encrypt_key.encode())
decryptor = Fernet(decrypt_key.encode())

def activate():
  code = Fernet.generate_key()  # byte string
  encrypted_code = encryptor.encrypt(code).decode()  # convert to string before sending
  res = requests.post(activation_url, json={'code': encrypted_code})
  if res.status_code == 200:
    encrypted_code = res.json()['code'].encode()  # convert to byte for decryption
    decrypted_code = decryptor.decrypt(encrypted_code)
    if decrypted_code == code:
      return True
  return False
  
if activate():
  print('Successfully activate')
else:
  print('Activation failed')

```
## example of .env
```env
HOST=0.0.0.0
PORT=9898
SSL_KEYFILE=
SSL_CERTFILE=
SSL_KEYFILE_PASSWORD=
WORKERS=1
DECRYPT_KEY="JmixbxpEWqqKKpA_xAdmhYFH1c7s_ZkMjK89JKO1mmY="
ENCRYPT_KEY="KxMEvdmQQ7bJhH2YaNHm2Cjkbi65eDjvmJ9trTJhcaM="
```
