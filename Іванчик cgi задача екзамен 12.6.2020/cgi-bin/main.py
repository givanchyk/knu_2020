import cgi


def f(string):
    for i in range(len(string)):
        if string[i] == ':':
            return string[0:i] + ':'
    return 'Не знайдено двокрапки'


if __name__ == '__main__':
    form = cgi.FieldStorage()
    string = form.getfirst('string', '')
    result = f(string)
    with open('templates/template.html', encoding='utf-8') as f:
        page = 'Content-type: text/html charset=utf-8\n\n' + f.read()
        page = page.format(result=result)
        
    import os
    if os.name == 'nt':
        import sys
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
        
    print(page)
