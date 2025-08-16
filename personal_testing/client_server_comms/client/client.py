import requests


def main():
    response = requests.get("http://127.0.0.1:5000")
    print(response.text)


if __name__ == "__main__":
    main()
