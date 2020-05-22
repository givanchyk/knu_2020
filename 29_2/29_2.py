import sqlite3
import cgi
con = sqlite3.connect('DATABASE.db')
cur = con.cursor()
class Person:
    def __init__(self, name=None, age=None):
        self.name = name
        self.age = age

    def print(self):
        print(self.name, self.age, end=' ')
class Pass(Person):
    def __init__(self, age=None, name=None, dep=None, arr=None, dist=None):
        super().__init__(name, age)
        self.dep = dep
        self.arr = arr
        self.dist = dist
        self.h_p_km = 3
    def show(self):
        a = []
        for i in cur.execute('SELECT * FROM route'):
            a.append(' '.join(map(str, list(i[1:]))))
        return a

    def add_route(self):
        cur.execute("INSERT INTO route VALUES ({}, '{}', '{}', {});".format(0, self.dep, self.arr, self.dist))

    def add_pass(self):
        print(self.age)
        cur.execute("INSERT INTO person VALUES ({}, '{}', {}, '{}', '{}', {});".format(
            0, self.name, self.age, self.dep, self.arr, self.dist))

    def get_dist(self):
        for i in cur.execute("SELECT dist FROM route WHERE dep = '{}' and arr = '{}';".format(self.dep, self.arr)):
            self.dist = i[0]
            return i[0]

    def len_route(self):
        for i in cur.execute("SELECT dist FROM person WHERE name = '{}' and age = {};".format(self.name, self.age)):
            return i[0]
def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    status = '200 OK'
    headers = headers = [('Content-Type', 'text/html; charset=utf-8')]
    if path == '':
        s = '<br>'.join(Pass().show())
        start_response(status, headers)
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        name1 = form.getfirst("name1", "")
        age1 = form.getfirst("age1", "")
        if name1 and age1:
            s = Pass(age=int(age1), name=name1).len_route()*Pass().h_p_km
        with open('templates/MAIN.html', encoding='utf-8') as f:
            page = f.read().format(add=s)
    elif path == 'route':
        s = ''
        start_response(status, headers)
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        dep1 = form.getfirst("dep1", "")
        arr1 = form.getfirst("arr1", "")
        dist1 = form.getfirst("dist1", "")
        if dep1 and arr1 and dist1:
            try:
                Pass(dep=dep1, arr=arr1, dist=dist1).add_route()
                con.commit()
                s = 'Маршрут додано!'
            except:
                s = 'Такого пасажира ще немає в базі даних'
        with open('templates/ROUTE.html', encoding='utf-8') as f:
            page = f.read().format(add=s)
    elif path == 'pass':
        s = ''
        start_response(status, headers)
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        name1 = form.getfirst("name1", "")
        age1 = form.getfirst("age1", "")
        dep1 = form.getfirst("dep1", "")
        arr1 = form.getfirst("arr1", "")
        if name1 and age1 and dep1 and arr1:
            try:
                print(name1, age1)
                p = Pass(name=name1, age=int(age1), dep=dep1, arr=arr1)
                p.get_dist()
                p.add_pass()
                con.commit()
                s = 'Пасажира додано!'
            except:
                s = 'Такого маршруту ще не існує :('
        with open('templates/PASS.html', encoding='utf-8') as f:
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
