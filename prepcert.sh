#/bin/bash

rm -rf prep
mkdir prep

for d in certs/letsencrypt/live/*
do
    n=${d##*/}
    cat "$d/fullchain.pem" >  "prep/$n.pem"
    #cat "$d/chain.pem" >>  "prep/$n.pem"
    cat "$d/privkey.pem" >>  "prep/$n.key"
    echo "done $n"
done

echo " \n Check certificate preparation \n"

for pem in prep/*.pem; do
 printf '%s: %s\n' \
        "$(date -jf "%b %e %H:%M:%S %Y %Z" "$(openssl x509 -enddate -noout -in "$pem"|cut -d= -f 2)" +"%Y-%m-%d")" \
    "$pem";
done | sort
