from flask import Flask, render_template, request

from dn42reg import lookup_asn, getwhois

from dn42graph import as_graph, path_graph

app = Flask(__name__)
app.config.from_pyfile('web_config.cfg')


def get_ip():
    try:
        ip = request.headers['x-real-ip']
    except KeyError:
        ip = None
    return ip


@app.context_processor
def add_ip():
    return dict(ip=get_ip())


@app.route('/')
@app.route('/network')
def page_network():
    return render_template('network.html', page='network')


@app.route('/whois')
def whois():
    search_key = next(iter(request.args))
    return getwhois(request.args.get(search_key), search_key)


@app.route("/lookup")
def page_lookup_search():
    return render_template('lookup_search.html', page='lookup')


@app.route("/roa")
def page_roa():
    return render_template('roa.html', page='roa')

@app.route("/as_graph/<asn>")
def as_graph_show(asn):
    if asn.isdigit():
        return as_graph(asn)
    elif asn.startswith('AS') and asn[2:].isdigit():
        return as_graph(asn[2:])
    else:
        return "404 Not Found"

@app.route('/lookup/<lookup_str>')
def page_lookup(lookup_str):
    if lookup_str.startswith('AS') and lookup_str[2:].isdigit():
        lookup_result = lookup_asn(lookup_str)
        if lookup_result == {}:
            return "404 Not Found"
        return render_template('lookup_asn.html', page='lookup', lookup=lookup_result)
    return "404 Not Found"

@app.route('/path_lookup')
def page_path_lookup():
    return render_template('path_lookup.html', page='path_lookup')

@app.route('/path_lookup/<from_asn>/<to_asn>')
def as_path_show(from_asn, to_asn):
    if from_asn.isdigit() and to_asn.isdigit():
        return path_graph(from_asn, to_asn)
    elif from_asn.startswith('AS') and to_asn.startswith('AS') and from_asn[2:].isdigit() and to_asn[2:].isdigit():
        return path_graph(from_asn[2:], to_asn[2:])
    else:
        return "404 Not Found"

@app.route('/isp')
def page_isp():
    return render_template('ISPs.html', page='isp')


@app.route('/about')
def page_about():
    return render_template('about.html', page='about')


@app.route('/js-licenses')
def page_js_licenses():
    return render_template('js-licenses.html', page='js-licenses')

@app.after_request
def add_header(res):
    res.headers['Cache-Control'] = "public, max-age=864000"
    return res

if __name__ == '__main__':
    app.run(host='localhost', port=3003)
