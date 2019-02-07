#/bin/bash

echo " \n Check certificate preparation \n"

for pem in prep/*.pem; do
 printf '%s: %s\n' \
        "$(date -jf "%b %e %H:%M:%S %Y %Z" "$(openssl x509 -enddate -noout -in "$pem"|cut -d= -f 2)" +"%Y-%m-%d")" \
    "$pem";
done | sort
