## DOSSL Simple docker wrapper for CertBot to get Letsencrypt certs

DOSSL helps you to get SSL certificates via DNS validation for you domain.

The certificates are stored in Docker volume `letsencrypt` (create on `make build` if necessary)

Make file commands can help you to start the process and copy the certs from the volume. 

TBD: 
* [ ] Export volume in encrypted form for certs backup
* [ ] Make volume temporary, have encrypted form of certs storage

## How to use 

1. `make build` get the image and make docker volume called `letsencrypt`
    
    - OR `docker pull vlaskinvlad/dossl:latest` - pull the image
    
      `docker volume create --name letsencrypt` - create the volume
   
   
2. `make cert` generate SSL certs via [CertBot](https://certbot.eff.org) & [Letsencrypt](https://letsencrypt.org)

    It will ask you about the fdqn and start CertBot chat.
   
    At some point you will have to create DNS TXT record, please be prepared for that.
    
    
3. `make cert_copy` copies the certs from the container `letsencrypt` to local folder `./certs`

   Expected directory structure would be:
   
   ```
   ./certs
         ./your_domain
             cert.pem
             chain.pem
             fullchain.pem
             privkey.pem             
   ```
