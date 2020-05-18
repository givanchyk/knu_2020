import cgi
import json


def application(environ, start_response):
    if environ.get('PATH_INFO', '').lstrip('/') == '':
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        result1 = ''
        result2 = ''
        seq_str = form.getfirst('sequence', '')
        if seq_str:
            for i in range(len(seq_str)):
                if seq_str[i] in [str(num) for num in range(10)]:
                    result1 += seq_str[i]
                else:
                    result2 += seq_str[i]
        with open('data.json', 'w') as f:
            json.dump([result1, result2], f)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'), ])
        with open('templates/template.html', encoding='utf-8') as f:
            page = f.read().format(result1=result1, result2=result2)
    else:
        start_response('404 NOT FOUND', [('Content-Type', 'text/html; charset=utf-8'), ])
        with open('templates/error_404.html', encoding='utf-8') as f:
            page = f.read()

    return [bytes(page, encoding='utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(' Local WSGI web server ')
    make_server('', 8000, application).serve_forever()
