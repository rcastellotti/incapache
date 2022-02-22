import time
import requests
import json
import sys
import re
regex = r"\d+"
url = "http://localhost:"

port = sys.argv[1]
url += port


def print_headers(r):
    print("Response Headers: ")
    headers_json = json.dumps(dict(r.__dict__['headers']), indent=4)
    print(headers_json)


def print_request_headers(r):
    print("Request Headers: ")
    headers_request_json = json.dumps(dict(r.request.headers), indent=4)
    print(headers_request_json)


def index():
    r = requests.get(url + "/index.html")
    print("------------------------------")
    print(f"Performing {r.request.method} {r.request.path_url}")
    print_request_headers(r)
    print(f"Status code: {r.status_code}")
    print_headers(r)
    assert(r.status_code == 200)


def not_found():
    r = requests.get(url+"/aaa.html")
    print("------------------------------")
    print(f"Performing {r.request.method} {r.request.path_url}")
    print_request_headers(r)
    print(f"Status code: {r.status_code}")
    print_headers(r)
    assert(r.status_code == 404)


def mehtod_not_implemented():
    r = requests.post(url)
    print("------------------------------")
    print(f"Performing {r.request.method} {r.request.path_url}")
    print_request_headers(r)
    print(f"Status code: {r.status_code}")
    print_headers(r)
    assert(r.status_code == 501)


def index_304():
    gmt_time = time.strftime("%a, %d %b %Y %T GMT", time.gmtime())
    headers = {'If-Modified-Since': gmt_time}
    r = requests.get(url + "/index.html", headers=headers)
    print("------------------------------")
    print(f"Performing Conditional {r.request.method} {r.request.path_url}")
    print_request_headers(r)
    print(f"Status code: {r.status_code}")
    print_headers(r)
    
    assert(r.status_code == 304 and not r.content)


def index10():
    r = requests.get(url + "/index.html")
    print("------------------------------")
    print(f"Performing multiple {r.request.method} {r.request.path_url}")
    print_request_headers(r)
    print_headers(r)
    cookie_uid = re.search(regex, r.__dict__["headers"]["Set-Cookie"]).group(0)
    headers = {'Cookie': "id="+cookie_uid}
    for i in range(10):
        rn = requests.get(url + "/index.html", headers=headers)
        print(f"Performing {r.request.method} {r.request.path_url} #{i} Status code: {r.status_code}")

        assert(not "Set-Cookie" in dict(rn.__dict__))


def main():

    index()
    not_found()
    mehtod_not_implemented()
    index_304()
    index10()


if __name__ == "__main__":
    main()
