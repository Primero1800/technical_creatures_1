import httpx


def get(url=None, token=None):
    if not url:
        url = 'http://127.0.0.1:8000/user/token'
    with httpx.Client() as client:
        response = client.get(url=url, headers={'Authorization': 'bearer ' + token})
        print(response.request.headers)
        print(response.status_code)
        print(response.headers)
        print(response.text)


if __name__ == "__main__":
    while True:
        token=input("Input token: ")
        if token == 'q':
            break
        get(token=token)
