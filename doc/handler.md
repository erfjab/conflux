# Extract JWT Secret Key from Marzban Database

First, extract the `JWT Secret Key` from both the new and old Marzban databases. This key is used to generate JWT tokens.

# Create conflux.py File in Marzban Directory

Create the `conflux.py` file in the Marzban directory:

```bash
nano /opt/marzban/conflux.py
```

Then, paste the following code into the file and replace `tokens` with the extracted `JWT Secret Key` values:

```python
def get_subscription_payload(token: str) -> Union[dict, None]:
    try:
        if len(token) < 15:
            return None

        # Check if it's a JWT token
        if token.startswith("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."):
            for SECRET_KEY in SECRET_KEYS:
                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                    if payload.get("access") == "subscription":
                        return {
                            "username": payload["sub"],
                            "created_at": datetime.utcfromtimestamp(payload["iat"]),
                        }
                except jwt.exceptions.PyJWTError:
                    continue
            return None
        else:
            if len(token) < 10:
                return None
            u_token = token[:-10]
            u_signature = token[-10:]
            try:
                u_token_dec = b64decode(
                    u_token.encode("utf-8") + b"=" * (-len(u_token) % 4),
                    altchars=b"-_",
                    validate=True,
                ).decode("utf-8")
                u_username, u_created_at_str = u_token_dec.split(",", 1)
                u_created_at = int(u_created_at_str)
            except:
                return None

            for SECRET_KEY in SECRET_KEYS:
                u_token_resign = b64encode(
                    sha256((u_token + SECRET_KEY).encode("utf-8")).digest(),
                    altchars=b"-_",
                ).decode("utf-8")[:10]
                if u_signature == u_token_resign:
                    return {
                        "username": u_username,
                        "created_at": datetime.utcfromtimestamp(u_created_at),
                    }
            return None
    except:
        return None
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
SECRET_KEYS = ["secretone", "secrettow", "secretthree"]
```

This allows Conflux to handle tokens from multiple Marzban instances seamlessly. Just replace `"secretthree"` with the actual JWT Secret Key of the additional Marzban instance.