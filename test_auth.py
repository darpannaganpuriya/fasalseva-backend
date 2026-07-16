import json, urllib.request, time

email = f"testuser{int(time.time())}@example.com"
body = json.dumps({"name":"Test User","email":email,"password":"Password123","phone":"9999999999","role":"farmer"}).encode()
req = urllib.request.Request('http://127.0.0.1:8000/api/auth/signup', data=body, headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print('SIGNUP STATUS', resp.status)
        print(resp.read().decode())
except urllib.error.HTTPError as e:
    print('SIGNUP HTTP ERROR', e.code)
    try:
        print(e.read().decode())
    except Exception:
        pass
except Exception as e:
    print('SIGNUP ERROR', repr(e))

# Now try login
body2 = json.dumps({"email": email, "password": "Password123"}).encode()
req2 = urllib.request.Request('http://127.0.0.1:8000/api/auth/login', data=body2, headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req2, timeout=10) as resp:
        print('LOGIN STATUS', resp.status)
        print(resp.read().decode())
except urllib.error.HTTPError as e:
    print('LOGIN HTTP ERROR', e.code)
    try:
        print(e.read().decode())
    except Exception:
        pass
except Exception as e:
    print('LOGIN ERROR', repr(e))
3