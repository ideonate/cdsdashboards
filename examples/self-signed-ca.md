# Self-Signed Cert Authority

Add myjupyterhub.net to /etc/hosts (on mac)

## Make Root CA

In ~/.ssh:

openssl req -x509 -new -nodes -key myCA.key -sha256 -days 1825 -out myCA.pem

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

openssl x509 -req -in myjupyterhub.net.csr -CA ~/.ssh/myCA.pem -CAkey ~/.ssh/myCA.key -CAcreateserial -out myjupyterhub.net.crt -days 1825 -sha256 -extfile myjupyterhub.net.ext 



