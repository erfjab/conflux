# Extract JWT Secret Key from Marzban Database

First, extract the `JWT Secret Key` from both the new and old Marzban databases. This key is used to generate JWT tokens.

# Create conflux.py File in Marzban Directory

Create the `conflux.py` file in the Marzban directory:

```bash
nano /opt/marzban/conflux.py
```

Then, paste the following code into the file and replace `tokens` with the extracted `JWT Secret Key` values:

```python
import time
import jwt
from base64 import b64decode, b64encode
from datetime import datetime, timedelta
from functools import lru_cache
from hashlib import sha256
from math import ceil
from typing import Union


from config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES

SECRET_KEYS = ["secretone", "secrettwo"]

@lru_cache(maxsize=None)
def get_secret_key():
    from app.db import GetDB, get_jwt_secret_key

    with GetDB() as db:
        return get_jwt_secret_key(db)


def create_admin_token(username: str, is_sudo=False) -> str:
    data = {
        "sub": username,
        "access": "sudo" if is_sudo else "admin",
        "iat": datetime.utcnow(),
    }
    if JWT_ACCESS_TOKEN_EXPIRE_MINUTES > 0:
        expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        data["exp"] = expire
    encoded_jwt = jwt.encode(data, get_secret_key(), algorithm="HS256")
    return encoded_jwt


def get_admin_payload(token: str) -> Union[dict, None]:
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=["HS256"])
        username: str = payload.get("sub")
        access: str = payload.get("access")
        if not username or access not in ("admin", "sudo"):
            return
        try:
            created_at = datetime.utcfromtimestamp(payload["iat"])
        except KeyError:
            created_at = None

        return {
            "username": username,
            "is_sudo": access == "sudo",
            "created_at": created_at,
        }
    except jwt.exceptions.PyJWTError:
        return


def create_subscription_token(username: str) -> str:
    data = username + "," + str(ceil(time.time()))
    data_b64_str = (
        b64encode(data.encode("utf-8"), altchars=b"-_").decode("utf-8").rstrip("=")
    )
    data_b64_sign = b64encode(
        sha256((data_b64_str + get_secret_key()).encode("utf-8")).digest(),
        altchars=b"-_",
    ).decode("utf-8")[:10]
    data_final = data_b64_str + data_b64_sign
    return data_final


def get_subscription_payload(token: str) -> Union[dict, None]:
    for secret in SECRET_KEYS:
        try:
            if len(token) < 15:
                continue

            if token.startswith("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."):
                payload = jwt.decode(token, secret, algorithms=["HS256"])
                if payload.get("access") == "subscription":
                    return {"username": payload['sub'], "created_at": datetime.utcfromtimestamp(payload['iat'])}
                else:
                    continue
            else:
                u_token = token[:-10]
                u_signature = token[-10:]
                try:
                    u_token_dec = b64decode(
                        (u_token.encode('utf-8') + b'=' * (-len(u_token.encode('utf-8')) % 4)),
                        altchars=b'-_', validate=True)
                    u_token_dec_str = u_token_dec.decode('utf-8')
                except:
                    continue
                u_token_resign = b64encode(sha256((u_token+secret).encode('utf-8')
                                                ).digest(), altchars=b'-_').decode('utf-8')[:10]
                if u_signature == u_token_resign:
                    u_username = u_token_dec_str.split(',')[0]
                    u_created_at = int(u_token_dec_str.split(',')[1])
                    return {"username": u_username, "created_at": datetime.utcfromtimestamp(u_created_at)}
                else:
                    continue
        except jwt.exceptions.PyJWTError:
            continue
    return
```

# Add Volume to docker-compose.yml

Edit the `docker-compose.yml` file for Marzban:

```bash
nano /opt/marzban/docker-compose.yml
```

Add the following line under the `volumes` section:

```yaml
volumes:
    - /opt/marzban/conflux.py:/code/app/utils/jwt.py
```

Then restart the Marzban service:

```bash
marzban restart
```

if you have any problem: [@ErfJabGroup](https://t.me/erfjabgroup)

---

If you want to integrate another Marzban instance into Conflux, simply add its **JWT Secret Key** to the `SECRET_KEYS` list. For example:

```python
SECRET_KEYS = ["secretone", "secrettwo", "secretthree"]
```

This allows Conflux to handle tokens from multiple Marzban instances seamlessly. Just replace `"secretthree"` with the actual JWT Secret Key of the additional Marzban instance.
