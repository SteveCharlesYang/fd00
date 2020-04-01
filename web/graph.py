import re
from dn42reg import getasnname

class Node:
    def __init__(self, asn, label=None):
        if not valid_dn42_asn(asn):
            raise ValueError('Invalid AS number')
        self.asn = asn
        #self.label = asn[-4:] if label == None else label
        # self.label = asn if label == None else label
        self.label = getasnname(self.asn)

    def __lt__(self, b):
        return self.asn < b.asn

    def __repr__(self):
        return 'Node(asn="%s", label="%s")' % (
            self.asn,
            self.label)

class Edge:
    def __init__(self, a, b):
        self.a, self.b = sorted([a, b])

    def __eq__(self, that):
        return self.a.asn == that.a.asn and self.b.asn == that.b.asn

    def __repr__(self):
        return 'Edge(a.asn="%s", b.asn="%s")' % (
            self.a.asn,
            self.b.asn)



_re_dn42_asn = re.compile(r'^fd[0-9a-f]{2}(:[0-9a-f]{4}){7}$', re.IGNORECASE)

def valid_dn42_asn(ip):
    return True


