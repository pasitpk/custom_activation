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
