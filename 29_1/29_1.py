import cgi
import sqlite3
con = sqlite3.connect('DATABASE.db')
cur = con.cursor()
def add_person(id, name, contact):
    cur.execute("INSERT INTO person VALUES ({}, '{}', '{}');".format(id, name, contact))
def add_item(id, item_name, contact):
    cur.execute("INSERT INTO item VALUES ({}, '{}', '{}');".format(id, item_name, contact))
def check(item_name, name):
    for _ in cur.execute("SELECT 1 FROM item WHERE item_name = '{}' AND name = '{}';".format(item_name, name)):
        return 1
    return 0
def find_person(item_name):
    res = []
    for i in cur.execute("SELECT * FROM item WHERE item_name = '{}';".format(item_name)):
        res.append(i[2])
    return res
def find_item(name):
    res = []
    for i in cur.execute("SELECT * FROM item WHERE name = '{}';".format(name)):
        res.append(i[1])
    return res
def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    status = '200 OK'
    headers = headers = [('Content-Type', 'text/html; charset=utf-8')]
    if path == '':
        s = ''
        start_response(status, headers)
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        name1 = form.getfirst("name1", "")
        contacts1 = form.getfirst("contacts1", "")
        item_name2 = form.getfirst("item_name2", "")
        name2 = form.getfirst("name2", "")
        item_name3 = form.getfirst("item_name3", "")
        name3 = form.getfirst("name3", "")
        item_name4 = form.getfirst("item_name4", "")
        name5 = form.getfirst("name5", "")
        if name1 and contacts1:
            print(name1, contacts1)
            add_person(0, name1, contacts1)
            s = 'Постачальника додано до бази даних'
        elif item_name2 and name2:
            add_item(0, item_name2, name2)
            s = 'Товар додано до бази даних'
        elif item_name3 and name3:
            s = 'Постачає' if check(item_name3, name3) else 'Не постачає'
        elif item_name4:
            s = '<br>'.join(find_person(item_name4))
        elif name5:
            s = '<br>'.join(find_item(name5))
        with open('templates/TEMPLATE.html', encoding='utf-8') as f:
            page = f.read().format(add=s)
    else:
        start_response('404 NOT FOUND', [('Content-Type', 'text/html; charset=utf-8'), ])
        with open('templates/error_404.html', encoding='utf-8') as f:
            page = f.read()

    return [bytes(page, encoding='utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(' Local WSGI web server ')
    make_server('', 8000, application).serve_forever()

con.commit()
con.close()