.DEFAULT_GOAL=build

CERT_VOLUME=letsencrypt
NAME=dossl
GIT_VERSION := $(shell git describe --abbrev=7 --dirty --always --tags)
TAG = $(GIT_VERSION)
PWD := $(shell pwd)


chains:
	./prepcert.sh

volumes:
	@docker volume inspect $(CERT_VOLUME) >/dev/null 2>&1 || docker volume create --name $(CERT_VOLUME)

build: volumes
	@docker build -t $(NAME):$(TAG) .
	
cert:   volumes
	@while [ -z "$$DOMAIN_NAME" ]; do \
		read -r -p "Enter domain name (valid fqdn):" DOMAIN_NAME; \
        done ; \
	docker run -v $(CERT_VOLUME):/etc/letsencrypt -it $(NAME):$(TAG) -d $$DOMAIN_NAME --manual --preferred-challenges dns certonly

cert_copy:
	$(eval $@_TMP := "tmp-image")
	@docker rm -f $($@_TMP) || echo "Prev. image: $($@_TMP) is not there, good."  
	@docker run -v $(CERT_VOLUME):/etc/letsencrypt --name $($@_TMP) -d alpine:3.1 sleep 30 
	@docker cp $($@_TMP):/etc/letsencrypt $(PWD)/certs || echo "Seems there is nothing to copy, sorry..."
	@docker rm -f $($@_TMP)
	echo "Bye!"

call:
	make cert_copy
	make chains

.PHONY: volumes chains
