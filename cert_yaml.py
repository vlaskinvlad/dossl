import collections
import logging
import re
import ssl
import sys
from datetime import datetime, timezone, time
from os import listdir
from os.path import join
from typing import Tuple

import jinja2

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

LOGGER = logging.getLogger(__name__)


def pem_to_name(n: str) -> str:
    a = n.split('.pem')[0]
    return "%s_cert" % re.sub("[\.-]", "_", a)


def key_to_name(n: str) -> str:
    a = n.split('.key')[0]
    return "%s_key" % re.sub("[\.-]", "_", a)


def parse_to_tuple(s: str) -> Tuple:
    p = re.compile("^(?P<domain>[-\.\w]+?)\-?(?P<id>\d*?)\.(?P<tp>pem|key)$")
    m = p.match(s)
    if m:
        d = m.groupdict()
        id = int(d['id']) if d.get('id') else -1
        return d['tp'], d['domain'], id
    else:
        return None


def main():
    path = "prep"
    res_pem = {}
    res_key = {}

    res = dict()
    tmp_keys = dict()
    index = dict()

    for f in listdir(path):
        fpath = join(path, f)
        val = open(fpath, 'r').read()
        LOGGER.debug(join(path, f))
        t = parse_to_tuple(f)
        if t:
            tp, domain, id = t
            key = domain
            if tp == 'pem':
                try:
                    cert_dict = ssl._ssl._test_decode_cert(fpath)
                    dt = datetime.strptime(cert_dict['notAfter'], "%b %d %H:%M:%S %Y GMT")
                    ts = int(dt.replace(tzinfo=timezone.utc).timestamp())
                    if domain not in index:
                        res[domain] = val
                        index[domain] = (ts, id)
                    elif (ts, 0) > index[domain]:
                        res[domain] = val
                        index[domain] = (ts, id)
                except Exception as e:
                    LOGGER.error("EXCEPTION: %s %s" % (f, e))
            elif tp == 'key':
                tmp_keys[(domain, id)] = val

    def trim_name(a):
        return re.sub("[\.-]", "_", a)

    for domain, v in res.items():
        pem_val = v
        id = index[domain]
        ts = id[0]
        dt = datetime.fromtimestamp(ts)
        # LOGGER.info("Domain: %s until: %s" % (domain, dt))
        if dt < datetime.today():
            LOGGER.error("Expired ceritificate: %s" % domain)
        key_key = (domain, id[1])
        key_val = tmp_keys[key_key]
        res_pem["%s_cert" % trim_name(domain)] = pem_val
        res_key["%s_key" % trim_name(domain)] = key_val

    with open("./templates/ansible_cert.yaml", 'r') as f:
        template = jinja2.Template(f.read())

    with open("ansible_cert.yaml", "w") as f:
        f.write(template.render(pems=res_pem, keys=res_key))


if __name__ == '__main__':
    main()
