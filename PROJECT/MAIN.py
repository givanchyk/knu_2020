import sqlite3
import cgi
import xml.etree.ElementTree as ET
con = sqlite3.connect('DATABASE.db')
cur = con.cursor()


def g(x):
    if x:
        return x
    return 'NULL'


def show_employee():
    a = cur.execute("SELECT * FROM employee")
    return '<br>'.join([' '.join(map(str, i)) for i in a])


def is_employee(*args):
    sql = "SELECT 1 FROM employee WHERE name = ?"
    for _ in cur.execute(sql, tuple(map(g, args))):
        return 1
    return 0


def add_employee(*args):
    sql = "INSERT INTO employee VALUES (?, ?, ?, ?, ?);"
    cur.execute(sql, tuple(map(g, args)))


def edit_employee(*args):
    sql = """UPDATE employee 
    SET name = ?, year = ?, address = ?, unit = ?, position = ?
    WHERE name = ?;"""
    cur.execute(sql, tuple(map(g, args)))


def delete_employee(*args):
    sql = """DELETE FROM employee WHERE name = ?"""
    cur.execute(sql, tuple(map(g, args)))


def show_unit():
    a = cur.execute("SELECT * FROM unit")
    return '<br>'.join([' '.join(map(str, i)) for i in a])


def add_unit(*args):
    sql = "INSERT INTO unit VALUES (?, ?);"
    cur.execute(sql, tuple(map(g, args)))


def edit_unit(*args):
    sql = """UPDATE unit 
        SET name = ?, count = ?
        WHERE name = ?;"""
    sql2 = """UPDATE employee 
        SET unit = ?
        WHERE unit = ?;"""
    cur.execute(sql, tuple(map(g, args)))
    cur.execute(sql2, tuple(map(g, (args[0], args[2]))))


def delete_unit(*args):
    sql = """DELETE FROM unit WHERE name = ?"""
    sql2 = """DELETE FROM employee WHERE unit = ?"""
    cur.execute(sql, tuple(map(g, args)))
    cur.execute(sql2, tuple(map(g, args)))


def is_unit(*args):
    sql = "SELECT 1 FROM unit WHERE name = ?"
    for _ in cur.execute(sql, tuple(map(g, args))):
        return 1
    return 0


def show_position():
    a = cur.execute("SELECT * FROM position")
    return '<br>'.join([' '.join(map(str, i)) for i in a])


def add_position(*args):
    sql = "INSERT INTO position VALUES (?);"
    cur.execute(sql, tuple(map(g, args)))


def edit_position(*args):
    sql = """UPDATE position 
        SET name = ?
        WHERE name = ?;"""
    sql2 = """UPDATE employee  
        SET position = ?
        WHERE position = ?;"""
    cur.execute(sql, tuple(map(g, args)))
    cur.execute(sql2, tuple(map(g, args)))


def delete_position(*args):
    sql = """DELETE FROM position WHERE name = ?"""
    sql2 = """DELETE FROM employee WHERE position = ?"""
    cur.execute(sql, tuple(map(g, args)))
    cur.execute(sql2, tuple(map(g, args)))


def is_position(*args):
    sql = "SELECT 1 FROM position WHERE name = ?"
    for _ in cur.execute(sql, tuple(map(g, args))):
        return 1
    return 0


def add_order(*args):
    sql = "INSERT INTO order1 VALUES (?);"
    cur.execute(sql, tuple(map(g, args)))


def add_order_2(*args):
    tree = ET.parse('books.xml')
    root = tree.getroot()
    employee = ET.SubElement(root, 'employee')
    if args[0] == 'Employ':
        a = ET.SubElement(employee, 'action')
        b = ET.SubElement(employee, 'name')
        c = ET.SubElement(employee, 'age')
        d = ET.SubElement(employee, 'address')
        e = ET.SubElement(employee, 'unit')
        f = ET.SubElement(employee, 'position')
        a.text, b.text, c.text, d.text, e.text, f.text = args
    elif args[0] == 'Transfer':
        a = ET.SubElement(employee, 'action')
        b = ET.SubElement(employee, 'name')
        c = ET.SubElement(employee, 'unit')
        d = ET.SubElement(employee, 'position')
        a.text, b.text, c.text, d.text = args
    elif args[0] == 'Dismiss':
        a = ET.SubElement(employee, 'action')
        b = ET.SubElement(employee, 'name')
        a.text, b.text = args

    elem_tree = ET.ElementTree(root)
    elem_tree.write('books.xml', encoding='utf-8')


def show_order():
    a = cur.execute("SELECT * FROM order1")
    return '<br>'.join([' '.join(map(str, i)) for i in a])


def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    if path == '':
        s = show_employee()
        start_response(status, headers)
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        name1 = form.getfirst("name1", "")
        age1 = form.getfirst("age1", "")
        address1 = form.getfirst("address1", "")
        unit1 = form.getfirst("unit1", "")
        position1 = form.getfirst("position1", "")
        name2 = form.getfirst("name2", "")
        name3 = form.getfirst("name3", "")
        age2 = form.getfirst("age2", "")
        address2 = form.getfirst("address2", "")
        unit2 = form.getfirst("unit2", "")
        position2 = form.getfirst("position2", "")
        name4 = form.getfirst("name4", "")
        if name1:
            if is_employee(name1):
                s = 'Робітник вже є в базі даних'
            else:
                if is_unit(unit1) and is_position(position1):
                    add_employee(name1, age1, address1, unit1, position1)
                    s = 'Робітника додано'
                else:
                    s = 'Даних посади або підрозділа не існує'
        elif name2:
            if is_employee(name2):
                edit_employee(name3, age2, address2, unit2, position2, name2)
                s = 'Інформацію про робітника змінено'
            else:
                s = 'Робітника немає в базі даних'
        elif name4:
            if is_employee(name4):
                delete_employee(name4)
                s = 'Дані про робітника видалено'
            else:
                s = 'Робітника немає в базі даних'
        with open('templates/MAIN.html', encoding='utf-8') as f:
            page = f.read().format(add=s)
    elif path == 'unit':
        s = show_unit()
        start_response(status, headers)
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        name1 = form.getfirst("name1", "")
        count1 = form.getfirst("count1", "")
        name2 = form.getfirst("name2", "")
        name3 = form.getfirst("name3", "")
        count2 = form.getfirst("count2", "")
        name4 = form.getfirst("name4", "")
        if name1:
            if is_unit(name1):
                s = 'Підрозділ вже є в базі даних'
            else:
                add_unit(name1, count1)
                s = 'Підрозділ додано'
        elif name2:
            if is_unit(name2):
                edit_unit(name3, count2, name2)
                s = 'Інформацію про підрозділ змінено'
            else:
                s = 'Підрозділа немає в базі даних'
        elif name4:
            if is_unit(name4):
                delete_unit(name4)
                s = 'Дані про підрозділ видалено'
            else:
                s = 'Підрозділа немає в базі даних'
        with open('templates/UNIT.html', encoding='utf-8') as f:
            page = f.read().format(add=s)
    elif path == 'position':
        s = show_position()
        start_response(status, headers)
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        name1 = form.getfirst("name1", "")
        name2 = form.getfirst("name2", "")
        name3 = form.getfirst("name3", "")
        name4 = form.getfirst("name4", "")
        if name1:
            if is_position(name1):
                s = 'Посада вже є в базі даних'
            else:
                add_position(name1)
                s = 'Посаду додано'
        elif name2:
            if is_position(name2):
                edit_position(name3, name2)
                s = 'Інформацію про посаду змінено'
            else:
                s = 'Посади немає в базі даних'
        elif name4:
            if is_position(name4):
                delete_position(name4)
                s = 'Дані про посаду видалено'
            else:
                s = 'Посади немає в базі даних'
        with open('templates/POSITION.html', encoding='utf-8') as f:
            page = f.read().format(add=s)
    elif path == 'order':
        s = show_order()
        start_response(status, headers)
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        name1 = form.getfirst("name1", "")
        age1 = form.getfirst("age1", "")
        address1 = form.getfirst("address1", "")
        unit1 = form.getfirst("unit1", "")
        position1 = form.getfirst("position1", "")
        name2 = form.getfirst("name2", "")
        unit2 = form.getfirst("unit2", "")
        position2 = form.getfirst("position2", "")
        name3 = form.getfirst("name3", "")
        if name1:
            action = 'Employ'
            args = (action, name1, age1, address1, unit1, position1)
            s = 'Наказ додано до бази даних та XML'
            try:
                add_order(' '.join(args))
                add_order_2(*args)
            except:
                s = 'Даний наказ вже існує'
        elif name2:
            if is_employee(name2):
                action = 'Transfer'
                args = (action, name2, unit2, position2)
                s = 'Наказ додано до бази даних та XML'
                try:
                    add_order(' '.join(args))
                    add_order_2(*args)
                except:
                    s = 'Даний наказ вже існує'
            else:
                s = 'Робітника немає в базі даних'
        elif name3:
            if is_employee(name3):
                action = 'Dismiss'
                args = (action, name3)
                s = 'Наказ додано до бази даних та XML'
                try:
                    add_order(' '.join(args))
                    add_order_2(*args)
                except:
                    s = 'Даний наказ вже існує'
            else:
                s = 'Робітника немає в базі даних'
        with open('templates/ORDER.html', encoding='utf-8') as f:
            page = f.read().format(add=s)
    else:
        start_response('404 NOT FOUND', [('Content-Type', 'text/html; charset=utf-8'), ])
        with open('templates/error_404.html', encoding='utf-8') as f:
            page = f.read()
    con.commit()
    return [bytes(page, encoding='utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(' Local WSGI web server ')
    make_server('', 8000, application).serve_forever()

con.commit()
con.close()
