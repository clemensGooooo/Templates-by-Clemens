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
