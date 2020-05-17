# Self-Signed Cert Authority

Add myjupyterhub.net to /etc/hosts (on mac)

## Make Root CA

In ~/.ssh:

openssl genrsa -des3 -out myCA.key 2048

openssl req -x509 -new -nodes -key myCA.key -sha256 -days 365 -out myCA.pem

(Certs must now be ~12 months validity)

Add to Keychain:
https://deliciousbrains.com/ssl-certificate-authority-for-local-https-development/

## Generate certs for new dev site:

openssl genrsa -out myjupyterhub.net.key 2048
openssl req -new -key myjupyterhub.net.key -out myjupyterhub.net.csr

vi myjupyterhub.net.ext
```
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
 
[alt_names]
DNS.1 = myjupyterhub.net
```

openssl x509 -req -in myjupyterhub.net.csr -CA ~/.ssh/myCA.pem -CAkey ~/.ssh/myCA.key -CAcreateserial -out myjupyterhub.net.crt -days 365 -sha256 -extfile myjupyterhub.net.ext 



