import logging
import re
import sys
from os import listdir
from os.path import join

import jinja2

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

LOGGER = logging.getLogger(__name__)


def pem_to_name(n: str) -> str:
    a = n.split('.pem')[0]
    return "%s_cert" % re.sub("\.", "_", a)


def key_to_name(n: str) -> str:
    a = n.split('.key')[0]
    return "%s_key" % re.sub("\.", "_", a)


def main():
    path = "prep"
    res_pem = {}
    res_key = {}

    for f in listdir(path):
        fpath = join(path, f)
        val = open(fpath, 'r').read()
        LOGGER.debug(join(path, f))

        if f.endswith(".pem"):
            key = pem_to_name(f)
            res_pem[key] = val
            LOGGER.debug("PEM: %s processed" % key)

        elif f.endswith(".key"):
            key = key_to_name(f)
            res_key[key] = val
            LOGGER.debug("KEY: %s processed" % key)

    with open("./templates/ansible_cert.yaml", 'r') as f:
        template = jinja2.Template(f.read())

    with open("ansible_cert.yaml", "w") as f:
        f.write(template.render(pems=res_pem, keys=res_key))

if __name__ == '__main__':
    main()
