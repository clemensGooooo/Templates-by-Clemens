# SSL-HTTPS
How you can create a https Nginx....

## Open SSL


Usually, OpenSSL is installed but if it isn't you have to install it.
<br>
You can check if it's installed with `openssl` in the command line.

## Create CA (Certificate Authority)

You have to create this with some commands...
<br>
```
openssl genrsa -aes256 -out ca-key.pem 4096
```

You have to write your password down becaus you need it later...

```
openssl req -new -x509 -sha256 -days 365 -key ca-key.pem -out ca.pem
```
Now you can create a certificate...

## Generate your certificate

Here we create your certificate...
```
openssl genrsa -out cert-key.pem 4096
```

Request for a certificate signing

```
openssl req -new -sha256 -subj "/CN=yourcn" -key cert-key.pem -out cert.csr
```
Here you create a file for your server preferences..
```
echo "subjectAltName=DNS:your-dns.record,IP:257.10.10.1" >> extfile.cnf
```
Last step is to create the real certificate

```
openssl x509 -req -sha256 -days 365 -in cert.csr -CA ca.pem -CAkey ca-key.pem -out cert.pem -extfile extfile.cnf -CAcreateserial
```

## How to insert the certificate on server

To upload the certificates on our server (if your machie where you created it is't the server) we nned a service like `rsync`.

---

Now I uploaded the certificate in `/etc/ssl`, in this folder are two subfolders `private` and `certs`...

Upload the `cert-key.pem` into the folder `private`...

```
rsync cert-key.pem user@[ip-addresse]:/etc/ssl/private/
```

and the second file...

To connect the files to one.

```
cat cert.pem ca.pem >> full.pem 
```

To upload...

```
rsync full.pem user@[ip-addresse]:/etc/ssl/certs/
```
### Edit the config file of nginx

Add the following lines into your nginx config file `/etc/nginx/nginx.conf`

```
listen 443;
server_name domainname.com;
ssl on;
ssl_certificate /etc/ssl/certs/certs/full.pem;
ssl_certificate_key /etc/ssl/private/cert-key.pem;
ssl_prefer_server_ciphers on;
```
