Nella terza e ultima esercitazione realizziamo un web server che vuole imitare il [web server Apache](http://www.apache.org/) ma
riesce a fare molto meno. Per questo motivo lo chiameremo **incApache(incApache i**s **n**ot **c**omparable to **Apache**, pronunciato
all'americana come "incapaci") e il suo logo è l'indiano UncaDunca:

![uncadunca](uncadunca.jpg)

incApache riconosce solo i **metodi HEAD e GET,** non è in grado di comprendere il metodo POST.

# Il metodo HEAD

Il **metodo HEAD** viene usato principalmente per scopi di debug. Di fatto viene restituita una risposta del tutto analoga a quella che si avrebbe con il metodo GET ma non si restituisce la risorsa richiesta,
bensì solo la parte di header. Esempi di risposte ottenute interrogando alcuni server web con il metodo HEAD sono quelli seguenti, nei quali per semplicità sono stati cancellati alcuni header che non considereremo.

## HEAD: esempio 1

Richiesta della homepage sul server web che gira su localhost ed è in ascolto sulla porta 80

```bash
>telnet localhost 80
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
HEAD / HTTP/1.0
```

```
HTTP/1.0 200 OK                                \* Request line (la richiesta HTTP è andata a buon fine) */
Date: Mon, 26 Nov 2014 19:50:39 GMT            \* Data della risposta in formato standard GMT */
Server: Apache/2.2.17 (Ubuntu)                 \* Tipo di server */
Last-Modified: Thu, 29 Sep 2014 09:43:08 GMT   \* Data di modifica del file richiesto in formato standard */
Content-Length: 177                            \* Lunghezza del file (in byte) */
Connection: close                              \* Il server chiude la connessione dopo aver servito il client */
Content-Type: text/html                        \* MIME tipe del file richiesto */
                                               \* **Nota:** ogni header termina con una riga vuota (\\r\\n) */
```

## HEAD: esempio 2

Richiesta della pagina `aaa.html` sul server web www.disi.unige.it in ascolto sulla porta 80. La pagina `aaa.html` non esiste sul server.

```bash
> telnet www.disi.unige.it 80
Trying 130.251.61.13
Connected to c3po.disi.unige.it.
Escape character is '^]'.
HEAD /aaa.html HTTP/1.0
```

```
HTTP/1.0 404 Not Found
Date: Mon, 26 Nov 2014 20:09:49 GMT
Server: Apache
Connection: close
Content-Type: text/html; charset=iso-8859-1
```

## HEAD: esempio 3

Richiesta della home page sul server web `www.google.it` in ascolto sulla porta 80. Il metodo HEAD non viene scritto correttamente.

```
> telnet www.google.it 80
Trying 173.194.35.24
Connected to www.google.it.
Escape character is '^]'.
HEAAD / HTTP/1.0
```

```
HTTP/1.0 405 Method Not Allowed
Content-Type: text/html; charset=UTF-8
Content-Length: 960
Date: Mon, 26 Nov 2014 20:14:02 GMT
Server: GFE/2.0
```

# Il metodo GET

Il **metodo GET** viene usato ogni volta che si vuole richiedere un file.
Supponiamo che un client voglia richiedere un' immagine, per esempio il logo di incApache. Una tipica richiesta inviata da un browser Firefox è simile alla seguente.

```
GET /images/uncadunca.jpg HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (Ubuntu; X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0
Accept: image/png,image/\*;q=0.8,\*/\*;q=0.5
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip, deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,\*;q=0.7
If-Modified-Since: Mon, 26 Nov 2014 11:27:51 GMT
```

Nella Request line compare il metodo **GET** e il nome di un file JPG (`/images/uncadunca.jpg`). Tutti gli
altri header della richiesta sono opzionali e possono essere utili per "servire" al meglio il client.

**Nota:** a partire dalla versione 1.1 del protocollo anche l' header `Host:` è diventato obbligatorio perché è possibile definire i [virtual host](http://httpd.apache.org/docs/2.0/vhosts/) (che incApache non supporta).

Come nel caso del metodo HEAD si possono verificare varie situazioni.

1.  Il file **non esiste** all' interno della directory pubblica cui il web server può accedere. Si avrà una risposta del tipo seguente, nella quale viene restituito un file HTML che segnala l'errore. Il file HTML occupa 298 byte.

    ```
    HTTP/1.1 404 Not Found
    Date: Mon, 03 Dec 2014 18:07:30 GMT
    Server: Apache/2.2.17 (Ubuntu)
    Vary: Accept-Encoding
    Connection: close
    Content-Length: 298
    Content-Type: text/html; charset=iso-8859-1

    Not Found

    The requested URL /mywww/images/uncadunc.jpg was not found on this server.

    Apache/2.2.17 (Ubuntu) Server at localhost Port 80
    ```

2.  Il file **esiste** all' interno della directory pubblica cui il web server può accedere e:

    - La copia che si trova sul server è più recente di quella già disponibile sul client. Questa informazione si ottiene andando a confrontare la data della risorsa sul server con la data che il client presenta nell' header `If-Modified-Since`: (in
      questo caso il 26/11/2014). Se la risorsa sul server è stata modificata, si otterrà una risposta simile a quella seguente cui farà seguito la risorsa stessa:

      ```
      HTTP/1.1 200 OK
      Date: Mon, 03 Dec 2014 17:51:13 GMT
      Server: Apache/2.2.17 (Ubuntu)
      Last-Modified: Sun, 02 Dec 2014 10:27:51 GMT
      Accept-Ranges: bytes
      Content-Length: 12385
      Content-Type: image/jpeg
      ```

      **Nota:** tra l' header e la risorsa restituita ad un client ci deve essere sempre una (e solo una) linea vuota (codificata con \\r\\n).

    - La copia che si trova sul server non è più recente di quella già disponibile sul client. Si otterrà la risposta seguente (`conditional GET`) e il browser visualizzerà la risorsa già presente nella sua cache.
      ```
      HTTP/1.1 304 Not Modified
      Date: Mon, 03 Dec 2014 17:53:05 GMT
      Server: Apache/2.2.17 (Ubuntu)
      ```

# Se le cose non vanno a buon fine?

Non sempre le richieste fatte ai web server possono essere soddisfatte, e incApache è particolarmente soggetto a queste evenienze, visto che implementa solo due dei metodi previsti dal protocollo!

Forse l'errore più comune si verifica quando si cerca un file che non esiste (perché si sbaglia a digitarne il nome). In questo caso lo standard HTTP prevede di restituire una risposta di tipo **404 Not Found** come abbiamo appena discusso.

Se, invece, la richiesta contiene un metodo non supportato o non rispetta lo standard del protocollo si potrebbero ottenere risposte come quelle seguenti.

```
HTTP/1.1 501 Method Not Implemented
Date: Mon, 03 Dec 2014 18:19:41 GMT
Server: Apache/2.2.17 (Ubuntu)
Allow: GET, HEAD,POST
Vary: Accept-Encoding
Content-Length: 306
Connection: close
Content-Type: text/html; charset=iso-8859-1

Method Not Implemented

GETT to /mywww/images/uncadunc.jpg not supported.

------------------------------------------------------------------------

Apache/2.2.17 (Ubuntu) Server at localhost Port 80
```

```
HTTP/1.1 400 Bad Request
Date: Mon, 03 Dec 2014 18:23:43 GMT
Server: Apache/2.2.17 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 301
Connection: close
Content-Type: text/html; charset=iso-8859-1

Bad Request

Your browser sent a request that this server could not understand.

------------------------------------------------------------------------

Apache/2.2.17 (Ubuntu) Server at 127.0.1.1 Port 80
```

# I Cookies

In questo laboratorio viene usato il meccanismo dei Cookie per tener traccia delle azioni compiute dai vari client, in particolare per contare il numero di richieste HTTP inviate da ciascun client.

Questo avviene assegnando ad ogni client un identificatore univoco, al quale viene associato un contatore del numero di richieste ricevute. Data l\'implementazione multithread del servizio, occorre prevenire corse critiche nell\'accesso alla struttura dati che mantinene il contatore del numero di Cookies assegnati. La prima volta che un client si connette non ha Cookies da includere nella richiesta, e il server genera un nuovo Cookie da includere nell' header della risposta, azzerando il contatore del numero di accessi per il nuovo client; le volte successive che il client si connette include il suo Cookie nell\'header della richiesta, permettendo cosi' al server di riconoscere il client e di incrementare il relativo contatore del numero di richieste. Occorre generare un Cookie con associata una data di scadenza abbastanza lontana nel tempo da permettere il conteggio delle richieste per almeno un anno.

Per tutte le altre parti del protocollo si rimanda agli RFC, a Google e alla documentazione ufficiale. Un sito vecchio ma semplice è [HTTP Made Really Easy](http://www.jmarshall.com/easy/http/); in rete esistono davvero moltissime informazioni su questo argomento.

# System call e funzioni C

Molte delle system call e delle funzioni C da usare le abbiamo già viste nelle prime due esercitazioni, alcune sono nuove.

## Socket

Per queste system call vi rimandiamo alle esercitazioni precedenti.

## File system

L'accesso alle informazioni sui file memorizzati al di sotto della **Document Root** serve per verificare se i file richiesti esistono e se sono leggibili dal web server. Per fare questo potete riusare le primitive già usate nelle esercitazioni precedenti cui si
aggiungono questa volta alcune funzioni che permettono di **aggiungere sicurezza ad incApache**. In particolare, vogliamo evitare che incApache possa servire risorse che non sono al di sotto della Document Root. Per fare questo, il web server deve invocare la
system call `chroot()` che, di fatto, non permette al processo di uscire dalla directory impostata come nuova root directory del file system.

> "A chroot jail is a way to isolate a process from the rest of the system. It should only be used for processes that don\'t run as root, as root users can break out of the jail very easily.\* \*The idea is that you create a directory tree where you copy or link in
> all the system files needed for a process to run. You then use the chroot system call to change the root directory to be at the base of this new tree and start the process running in that chroot\'d environment. Since it can\'t actually reference paths outside the
> modified root, it can\'t maliciously read or write to those locations."

Il valore della nuova directory che diventa la root del file system accessibile da incApache deve coincidere con il valore della Document Root. Tra le system call da invocare per realizzare questa parte ricordiamo:

1.  [`getcwd()`](http://pubs.opengroup.org/onlinepubs/9699919799/functions/getcwd.html)
2.  [`chdir()`](http://pubs.opengroup.org/onlinepubs/9699919799/functions/chdir.html)
3.  [`chroot()`](http://pubs.opengroup.org/onlinepubs/7908799/xsh/chroot.html)
4.  [`setuid()`](http://pubs.opengroup.org/onlinepubs/9699919799/functions/setuid.html)

**Attenzione:** la system call `chroot()` può essere eseguita solo da processi con UID = 0. Successivamente però il processo deve cambiare il proprio UID affinché l'esecuzione di `chroot()` abbia l' effetto voluto. Per ottenere questo risultato, l\'eseguibile incapache viene salvato su un file di proprietà di root con il bit "`s`" attivo per l' utente; in questo modo il processo assume UID = 0 nel momento in cui termina la chiamata di sistema `execve()`. Dopo l' esecuzione di `chroot()` il processo rilascia volontariamente i privilegi di root cambiando il suo UID in modo da ripristinare il corretto UID dell' utente.

# Gestione dei MIME Type

Tutte le volte che un server restituisce una risorsa deve anche specificarne il MIME Type. Nel momento in cui il web server ha lanciato il comando chroot non è più in grado di lanciare l' esecuzione del comando `file -i` per ottenere il MIME Type delle risorse perché non "vede" la directory che contiene l' eseguibile file. Per questo motivo, **incapache** lancia il comando `file` prima di entrare nella "chroot jail" e fa in modo che rimanga in ascolto tramite delle pipe. In questo modo il processo nella "chroot jail" può comunicare con `file` per ottenere i MIME type.

# Gestione delle date

Dalla documentazione ufficiale:

"HTTP applications have historically allowed three different formats for the representation of date/time stamps:

- **Sun, 06 Nov 1994 08:49:37 GMT** RFC 822, updated by RFC 1123, **formato consigliato**
- Sunday, 06-Nov-94 08:49:37 GMT RFC 850, obsoleted by RFC 1036
- Sun Nov 6 08:49:37 1994 ANSI C' s `asctime()` format

La gestione delle date per le richieste e le risposte HTTP richiede di **convertire Unix timestamp in uno dei formati accettati dallo standard**.
In particolare, vi suggeriamo di usare le seguenti funzioni (o loro varianti! Leggete bene commenti e manuali...):

- [`time()`](http://pubs.opengroup.org/onlinepubs/9699919799/functions/time.html) return the value of time in seconds since the [Epoch](http://en.wikipedia.org/wiki/Epoch_time)
- [`gmttime()`](http://pubs.opengroup.org/onlinepubs/9699919799/functions/gmtime.html) convert a time value to a [broken-down UTC time](http://www.gnu.org/software/libc/manual/html_nodeBroken_002ddown-Time.html) e la sua "inversa" [`timegm()`](http://linux.die.net/man/3/timegm)
- [`strftime()`](http://pubs.opengroup.org/onlinepubs/9699919799/functions/strftime.html) write a date according to a given format
- [`strptime()`](http://pubs.opengroup.org/onlinepubs/9699919799/functions/strptime.html) given a date return a broken-down time

Con queste funzioni si può scrivere l' header "`Date: ..."` di una risposta HTTP e gestire il Conditional GET riconoscendo l' header "`If-Modified-Since: ...`" di una richiesta HTTP.

# Connessioni multiple e Pthread

incApache usa **thread multipli** per gestire più connessioni contemporanee da parte di client (browser) diversi. Per il momento il vantaggio dell\'uso dei `pthread` invece di processi multipli creati con `fork()` è solo una (modesta) riduzione della quantità di risorse utilizzate a livello di sistema. Tuttavia l' uso dei thread ci consentirà successivamente di implementare le estensioni richieste per la versione 4.1 del server.

Nella versione 2.0 il processo che gestisce le richieste e risposte HTTP lancia un numero predeterminato di thread indipendenti nella fase di inizializzazione, e questi thread rimangono attivi fino alla terminazione del processo stesso (che può essere ottenuta solo da
shell, mandando un SIGKILL). Ogni thread accetta una richiesta di connessione, interpreta la richiesta HTTP, manda la corrispondente risposta HTTP, chiude la connessione e torna ad accettare una nuova connessione. Poiché però tutti i thread accettano connessioni dallo
stesso socket in modalità `listen()`, occorre prevenire corse critiche mediante l 'uso delle primitive: `pthread_mutex_lock()` e `pthread_mutex_unlock()`.

**ATTENZIONE:** l' attivazione di piu' thread contemporanei puo' generare corse critiche in alcune funzioni di libreria e/o system call. **_Accertarsi sempre_** (leggendo il man) che le funzioni usate siano "thread-safe/rientranti"!

# File di supporto

L\'archivio di questa settimana, [**incapache-students.tgz**](https://2020.aulaweb.unige.it/pluginfile.php/1067868/mod_page/content/6/incapache-students.tgz), contiene tutti i file che andranno consegnati per la terza e ultima esercitazione. La directory `www-root` contiene le pagine HTML di prova, utili per controllare il corretto funzionamento del server web. Si tratta di poche pagine HTML che includono al loro interno alcune immagini e condividono un file di stile. La pagina principale si chiama `index.html`. Esiste, fra queste pagine, anche un semplice form web che permette di testare il (mancato) funzionamento del metodo POST e un link errato che permette di testare la risposta 404 Not Found.

**ATTENZIONE:** Nell' archivio trovate gli eseguibili compilati - e funzionanti - per il laboratorio (sia per la versione 4.0, sia per la 4.1). Quando scompattate l 'archivio si perdono delle proprietà del file eseguibile che sono fondamentali per il buon funzionamento delprogramma. In particolare, dovete modificare il proprietario e settare il bit `"s"`. Il risultato finale dovrebbe essere simile a questo:

``` bash
-rwsr-sr-x 1 root root 20218 nov 24 11:49 incapache4.0debug-ubuntu64
-rwsr-sr-x 1 root root 23570 nov 24 11:49 incapache4.1debug-ubuntu64
```

La directory `src` contiene i file sorgente, così organizzati:

1.  `README`: file di istruzioni.
2.  `Makefile`: il makefile ;)
3.  `main.c`: riceve in input la directory da usare come document-root
    e, opzionalmente, il numero di porta sulla quale mettersi in
    ascolto. Usa la syscall chroot() per isolarsi dal resto del sistema,
    crea i socket per la comunicazione con i client e si pone in attesa
    di richieste, che gestisce mediante thread.
4.  `http.c**: gestisce le richieste HTTP (funzione `http_manage_request()`) e invia le risposte HTTP (funzione `send_response()`) preparando gli header opportuni e inviando le
    risorse specificate nelle richieste.
5.  **aux.c**: contiene le funzioni ausiliarie.
6.  **incApache.h**: contiene le definizione di costanti, le strutture
    dati e prototipi delle funzioni.
7.  **threads.c:** serve per una gestione multithread e comprende una
    parte facoltativa dell'esercitazione che verrà descritta in
    seguito.
8.  Nei file sorgenti le stringhe `TO BE DONE 4.0 START` e `TO BE DONE 4.0 END`
    indicano le parti obbligatorie per tutti.

# Debug

Il debug di incApache all' inizio non sarà semplicissimo. Una volta implementato il metodo GET potete cominciare a interrogare incApache mediante un browser. Per fare questo
dovete scrivere nella barra delle URL: `localhost:NUMPORT/<nomefilecercato>` dove NUMPORT è il numero di porta sulla quale avete messo in ascolto il server; se non specificate nessuna porta il valore di default è 8000. Potete anche usare il comando telnet `telnet locahost NUMPORT` e usare [Wireshark](https://www.wireshark.org/) per vedere quali dati transitano durante la comunicazione.

# Parte facoltativa

## HTTP/1.1 con pipeline

Eccoci arrivati alla parte opzionale di incApache: si consiglia di procedere con questa parte solo dopo aver ottenuto il perfetto funzionamento della versione 3.0, anche in caso di apertura di connessioni multiple.

Nella rete odierna un servizio online in grado di gestire una richiesta alla volta non avrebbe alcun senso, si tratterebbe di un servizio destinato a fallimento certo. Per questo motivo già incApache 3.0 adotta la tecnica dei thread multipli, ciascuno dedicato a rispondere a una connessione diversa. Nella versione 3.1 incApache, oltre a usare i thread per gestire connessioni multiple (cioè richieste in arrivo da più client), prova anche a sfruttare i thread per aumentare la propria velocità di risposta nel caso in cui il client gestisca le connessioni in una modalità detta di pipeline.

HTTP/1.1 allows multiple HTTP requests to be written out to a socket together without waiting for the corresponding responses. The requestor then waits for the responses to arrive in the order in which they were requested. The act of pipelining the requests can result in a dramatic improvement in page loading times, especially over high latency connections.

La figura seguente (presa da Wikipedia) descrive le connessioni in pipeline.

![pipeline](pipeline.png)

Le richieste in pipeline (così come l'apertura di connessioni multiple) sono una funzionalità implementata dal browser/client e completamente trasparente dal punto di vista del server, nel senso che un normale server come la versione 3.0 di incApache le potrebbe gestire. Tuttavia, anche il server può sfruttare le richieste in pipeline per aumentare la propria velocità di risposta, usando i thread in un modo più sofisticato: il web server può generare un nuovo thread per ogni richiesta di una nuova risorsa, e preparare simultaneamente le risposte; siccome però le risorse dovranno essere restituite al client nello stesso ordine in cui le richieste sono state ricevute dal server (FIFO), ci vorrà una fase di coordinamento tra i vari thread di risposta.

Questa fase di coordinamento si ottiene implementando una sorta di "sala di attesa dal medico" nella quale ogni paziente quando entra chiede chi è stato l'ultimo ad arrivare, ne tiene traccia ed entra nello studio del medico solo quando chi lo precede ne esce. In questo modo, ognuno ha una visione parziale della coda (si preoccupa di una sola persona) ma questa visione parziale gli permette una corretta implementazione di una coda FIFO.

Allo stesso modo, ogni nuovo thread dovrà memorizzate l'identificatore del thread che gestisce la richiesta precedente e attendere la sua terminazione usando la system call `pthread_join()`. Il primo thread, ovviamente, non dovrà aspettare nessuno e l'ultimo thread dovrà essere atteso dal thread principale che gestisce le richieste su quella connessione prima di chiudere la connessione stessa e tornare ad attendere per nuove richieste di connessione.

## Task per incApache 4.1

All'interno dei file di supporto gia` usati per la versione 3.0 completate le parti identificate da **TO BE DONE 4.1 START** e **TO BE DONE 4.1 END** e poi definite la costante IncApache3.1 nel Makefile.

Organizzate una buona strategia per il debugging della versione multithread. Per verificare il corretto funzionamento della versione 3.1 non basta mandare richieste multiple via telnet una dopo l'altra, altrimenti il server avrebbe il tempo di servire la richiesta precedente prima dell'arrivo della successiva. Tipicamente un browser aggiornato è in grado di inviare richieste in pipeline quando la pagina da visualizzare contiene molte immagini diverse. In alternativa si possono preparare degli script per generare sequenze di più richieste consecutive sulla stessa connessione, aprendo connessioni multiple, ciascuna delle quali in modalità pipeline.
Infine, è anche possibile usare strumenti (per es.[jmeter](https://jmeter.apache.org/)) pensati proprio per creare un carico "pesante" e valutare le prestazioni di un server.
