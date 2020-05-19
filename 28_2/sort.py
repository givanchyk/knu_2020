import cgi
import json
import xml.etree.ElementTree as ET


def find(q1=None, q2=None, q3=None):
    tree = ET.parse('books.xml')
    root = tree.getroot()
    res = []
    if not q1 and not q2 and not q3:
        return res
    for book in root.findall('book'):
        author = book.find('author').text
        name = book.find('name').text
        year = book.find('year').text
        if q1:
            if author != q1:
                continue
        if q2:
            if name != q2:
                continue
        if q3:
            q3_s = q3.split('-')
            print(q3_s)
            if not int(q3_s[0]) <= int(year) <= int(q3_s[1]):
                continue
        res.append(' '.join([author, name, year]))
    return res


def add(author, name, year):
    tree = ET.parse('books.xml')
    root = tree.getroot()
    book = ET.SubElement(root, 'book')
    a = ET.SubElement(book, 'author')
    b = ET.SubElement(book, 'name')
    c = ET.SubElement(book, 'year')
    a.text = author
    b.text = name
    c.text = year
    elem_tree = ET.ElementTree(root)
    elem_tree.write('books.xml', encoding='utf-8')


def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    status = '200 OK'
    headers = headers = [('Content-Type', 'text/html; charset=utf-8')]
    if path == '':
        start_response(status, headers)
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        author = form.getfirst("author", "")
        name = form.getfirst("name", "")
        year = form.getfirst("year", "")
        s = '<br/>'.join(find(q1=author, q2=name, q3=year))
        with open('templates/findbook.html', encoding='utf-8') as f:
            page = f.read().format(books=s)
    elif path == "add":
        start_response(status, headers)
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        author = form.getfirst("author", "")
        name = form.getfirst("name", "")
        year = form.getfirst("year", "")
        if name and author and year:
            add(name, author, year)
            with open('templates/addbook.html', encoding='utf-8') as f:
                page = f.read().format(add="Book added")
        else:
            with open('templates/addbook.html', encoding='utf-8') as f:
                page = f.read().format(add="Not enough info")
    else:
        start_response('404 NOT FOUND', [('Content-Type', 'text/html; charset=utf-8'), ])
        with open('templates/error_404.html', encoding='utf-8') as f:
            page = f.read()

    return [bytes(page, encoding='utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(' Local WSGI web server ')
    make_server('', 8000, application).serve_forever()
