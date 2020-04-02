import json
from flask import Config

config = Config("./")
config.from_pyfile('web_config.cfg')

inetdb_file = open('network-registry/inetnum-as.json')
inetdb = json.load(inetdb_file)

def getkey(ln):
    spl = ln.split(":", 1)
    return {
        "key": spl[0],
        "val": spl[1].lstrip()
    }


def getasnname(asn):
    asname = "Null"
    if asn is None:
        return asname
    try:
        f = open(config["WHOIS_REG_DIR"] + "/data/aut-num/AS" + asn)
        for ln in f:
            if ln.startswith("as-name:"):
                asname = ln[len("as-name:"):]
                asname = asname.lstrip()
    except IOError:
        pass
    return asname


def getwhois(search_str, search_type):
    whois = dict()
    if search_str is None:
        return whois
    try:
        f = open(regconfig["WHOIS_REG_DIR"] + "/data/" +
                 search_type+"/" + search_str)
        for ln in f:
            k = getkey(ln)
            if(k["key"] in whois):
                if(isinstance(whois[k["key"]], list)):
                    whois[k["key"]].append(k["val"])
                else:
                    whois[k["key"]] = [whois[k["key"]], k["val"]]
            else:
                whois[k["key"]] = k["val"]
    except IOError:
        pass
    if(search_str in inetdb["inet"]):
        whois["inetnum"] = inetdb["inet"][search_str]
    if(search_str in inetdb["inet6"]):
        whois["inet6num"] = inetdb["inet6"][search_str]
    return whois


def lookup_asn(asn):
    return getwhois(asn, search_type="aut-num")
