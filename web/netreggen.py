from os import listdir
from os.path import isfile, join
from flask import Config
import json

config = Config('./')
config.from_pyfile('web_config.cfg')


def geninetnum(numtype="route"):
    inetnum_data = dict()
    if numtype == "route":
        inetpath = config["WHOIS_REG_DIR"] + "/data/inetnum/"
    else:
        inetpath = config["WHOIS_REG_DIR"] + "/data/inet6num/"
    rtpath = config["WHOIS_REG_DIR"] + "/data/" + numtype
    inetfiles = [f for f in listdir(rtpath) if isfile(join(rtpath, f))]
    for filename in inetfiles:
        f = open(rtpath + '/' + filename)
        origins = []
        for ln in f:
            if ln.startswith(numtype+":"):
                rt = ln[len(numtype+":"):]
                rt = rt.strip()
                rt = {"inum": rt}
                try:
                    f = open(inetpath + filename)
                    for ln in f:
                        if ln.startswith("netname:"):
                            netname = ln[len("netname:"):]
                            netname = netname.strip()
                            rt["netname"] = netname
                except IOError:
                    pass
            if ln.startswith("origin:"):
                ori = ln[len("origin:"):]
                ori = ori.strip()
                origins.append(ori)
        for origin in origins:
            if not origin in inetnum_data:
                inetnum_data[origin] = [rt]
            else:
                inetnum_data[origin].append(rt)
    return inetnum_data


if __name__ == "__main__":
    idata = geninetnum()
    i6data = geninetnum("route6")

    with open('network-registry/inetnum-as.json', 'w') as fp:
        json.dump({
            "inet": idata,
            "inet6": i6data
        }, fp)
