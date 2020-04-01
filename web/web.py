from flask import Flask, render_template, request

from dn42reg import lookup_asn, getwhois

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


@app.route('/lookup/<lookup_str>')
def page_lookup(lookup_str):
    if lookup_str.startswith('AS') and lookup_str[2:].isdigit():
        lookup_result = lookup_asn(lookup_str)
        if lookup_result == {}:
            return ""
        return render_template('lookup_asn.html', page='lookup', lookup=lookup_result)


@app.route('/about')
def page_about():
    return render_template('about.html', page='about')


@app.route('/js-licenses')
def page_js_licenses():
    return render_template('js-licenses.html', page='js-licenses')


if __name__ == '__main__':
    app.run(host='localhost', port=3000)
