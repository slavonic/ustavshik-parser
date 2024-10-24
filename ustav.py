import urllib.request
import lxml.etree as et
import lxmlx.event as ev
from cslavonic.ucs_codec import register_UCS

register_UCS()

NS = 'http://www.ponomar.net/culiturgical'

def ns(tag):
    return '{' + NS + '}' + tag

def reencode(text):
    return text.encode('cp1251').decode('UCS')

def grab(url):
    if url.startswith('http://') or url.startswith('https://'):
        with urllib.request.urlopen(url) as f:
            html = f.read().decode('utf-8')
    else:
        with open(url) as f:
            html = f.read()

    xml = et.fromstring(html, parser=et.HTMLParser())
    body = xml.find('.//body')
    styles = list(body.findall('.//style'))
    scripts = list(body.findall('.//script'))
    for elt in styles + scripts:
        elt.getparent().remove(elt)

    yield {
        'type': ev.ENTER,
        'tag': ns('document'),
    }
    yield {
        'type': ev.TEXT,
        'text': '\n',
    }
    delayed_block = False
    delayed_inline = []
    def flush_block():
        if delayed_inline:
            yield { 'type': ev.ENTER, 'tag': ns('p')}
            yield from delayed_inline
            delayed_inline.clear()
            yield { 'type': ev.EXIT }
            yield { 'type': ev.TEXT, 'text': '\n\n' }

    for e,p in ev.with_peer(ev.scan(body)):
        if e['type'] == ev.ENTER:
            if e['tag'] in ('p', 'div', 'h1', 'h2', 'br'):
                delayed_block = True
            elif e['tag'] == 'span':
                if delayed_block:
                    delayed_block = False
                    yield from flush_block()
                delayed_inline.append({
                    'type': ev.ENTER,
                    'tag': ns('red'),
                })
        elif e['type'] == ev.EXIT:
            if p['tag'] in ('p', 'div', 'h1', 'h2', 'br'):
                delayed_block = True
            elif p['tag'] == 'span':
                delayed_inline.append({ 'type': ev.EXIT })
        elif e['type'] == ev.TEXT:
            if delayed_block:
                delayed_block = False
                yield from flush_block()
            delayed_inline.append({
                'type': ev.TEXT,
                'text': reencode(e['text']),
            })
    yield from flush_block()
    yield { 'type': ev.EXIT }

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Utility to parse and convert ustavshik.ru texts', prog='ustav')
    parser.add_argument('source', help='URL source (or local file name) to convert')
    parser.add_argument('target', help='file name to save the resulting XML')

    args = parser.parse_args()

    xml = ev.unscan(grab(args.source), nsmap={ None: NS })
    with open(args.target, 'wb') as f:
        f.write(et.tostring(xml, encoding='utf-8'))