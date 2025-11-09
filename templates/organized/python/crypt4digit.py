import secrets
pin = ''.join(str(secrets.randbelow(10)) for _ in range(4))
print(pin)
