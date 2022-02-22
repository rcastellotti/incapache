Roberto Castellotti s4801634
Fabio Fontana s4891185
Federico Fontana s4835118

# Relazione Incapache 4.0/1

Durante l'implementazione di Incapache abbiamo testato i metodi richiesti usando lo script `test.py` e [python-requests](https://requests.readthedocs.io/en/master/), riportiamo i test:

## Richiesta GET /index.html

```
Performing GET /index.html
Request Headers:
{
    "User-Agent": "python-requests/2.23.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "keep-alive"
}
Status code: 200
Response Headers:
{
    "Date": "Tue, 15 Dec 2020 09:11:02 GMT",
    "Set-Cookie": "id=0; Expires=Tue, 15 Dec 2021 09:11:02 GMT;",
    "Server": "incApache for SET.",
    "Connection": "close",
    "Content-Length": "936 ",
    "Content-Type": "text/html; charset=us-ascii",
    "Last-Modified": "Tue, 15 Dec 2020 08:36:38 GMT"
}
```

Questa richiesta setta il cookie per il tracking del numero di richieste effetuate dal client in considerazione.

## Richiesta GET

```
Performing GET /aaa.html
Request Headers:
{
    "User-Agent": "python-requests/2.23.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "keep-alive"
}
Status code: 404
Response Headers:
{
    "Date": "Tue, 15 Dec 2020 09:11:02 GMT",
    "Set-Cookie": "id=1; Expires=Tue, 15 Dec 2021 09:11:02 GMT;",
    "Server": "incApache for SET.",
    "Connection": "close",
    "Content-Length": "250 ",
    "Content-Type": "text/html; charset=us-ascii",
    "Last-Modified": "Tue, 15 Dec 2020 08:36:38 GMT"
}
```

Questa richiesta ottiene risposta con status code `404` poiché non esiste la pagina `aaa.html`

## Richiesta POST

```
Performing POST /
Request Headers:
{
    "User-Agent": "python-requests/2.23.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Content-Length": "0"
}
Status code: 501
Response Headers:
{
    "Allow": "HEAD,GET",
    "Date": "Tue, 15 Dec 2020 09:11:02 GMT",
    "Set-Cookie": "id=2; Expires=Tue, 15 Dec 2021 09:11:02 GMT;",
    "Server": "incApache for SET.",
    "Connection": "close",
    "Content-Length": "311 ",
    "Content-Type": "text/html; charset=us-ascii",
    "Last-Modified": "Tue, 15 Dec 2020 08:36:38 GMT"
}
```

Incapache non supporta richieste di tipo POST, lo status-code di risposta è pertanto `501 Not Implemented`

## Richiesta conditional GET

```
Performing Conditional GET /index.html
Request Headers:
{
    "User-Agent": "python-requests/2.23.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "If-Modified-Since": "Tue, 15 Dec 2020 09:11:02 GMT"
}
Status code: 304
Response Headers:
{
    "Date": "Tue, 15 Dec 2020 09:11:02 GMT",
    "Set-Cookie": "id=3; Expires=Tue, 15 Dec 2021 09:11:02 GMT;",
    "Server": "incApache for SET.",
    "Connection": "close"
}
```

Questa richiesta ottiene risposta `304 Not Modified` (nella richiesta abbiamo l'header `If-Modified-Since` che corrisponde alla `Date` settata nella prima richiesta a `/index.html`)

## Richieste GET multiple

```
Performing multiple GET /index.html
Request Headers:
{
    "User-Agent": "python-requests/2.23.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "keep-alive"
}
Response Headers:
{
    "Date": "Tue, 15 Dec 2020 09:11:02 GMT",
    "Set-Cookie": "id=4; Expires=Tue, 15 Dec 2021 09:11:02 GMT;",
    "Server": "incApache for SET.",
    "Connection": "close",
    "Content-Length": "936 ",
    "Content-Type": "text/html; charset=us-ascii",
    "Last-Modified": "Tue, 15 Dec 2020 08:36:38 GMT"
}
Performing GET /index.html #0 with cookie id=4 Status code: 200
Performing GET /index.html #1 with cookie id=4 Status code: 200
Performing GET /index.html #2 with cookie id=4 Status code: 200
Performing GET /index.html #3 with cookie id=4 Status code: 200
Performing GET /index.html #4 with cookie id=4 Status code: 200
Performing GET /index.html #5 with cookie id=4 Status code: 200
Performing GET /index.html #6 with cookie id=4 Status code: 200
Performing GET /index.html #7 with cookie id=4 Status code: 200
Performing GET /index.html #8 with cookie id=4 Status code: 200
Performing GET /index.html #9 with cookie id=4 Status code: 200
```

Multiple richieste dello stesso client incrementano il counter delle richieste provenienti dallo stesso client (identificato con il cookie).

Il fatto che richieste mulitple (fatte con Python e Jmeter)  abbiano tuttte status-code `200` e aggiornino correttamente il counter delle visite ci assicura l'assenza di **race condition** e **deadlock**.

Riportiamo inoltre i risultati dei test svolti con Jmeter: `inc1.0_100_results.csv` e `inc1.0_1000_results.csv`.
