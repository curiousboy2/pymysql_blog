import pymysql
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
#from flask.ext.script import Manager

# create our little application :)
app = Flask(__name__)
#设置默认的环境变量
app.config.update(dict(LOGIN_NAME='admin',LOGIN_PASSWD='default',SECRET_KEY='hello world'))
def get_cursor():
    #连接mysql数据库
    cur=pymysql.connect(db='hello',user='root',port=3306,host='localhost',passwd='huanghu')
    return cur

@app.route('/')
def show_entries():
    with get_cursor() as cur:
        cur.execute('select title, content from entries order by id desc limit 3')
        entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add',methods=['POST'])
def add_entry():
    title=request.form['title']
    content=request.form['content']
    with get_cursor() as cur:
        cur.execute('insert into entries(title,content) values(%s,%s)',[title,content])
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['LOGIN_NAME']:#app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['LOGIN_PASSWD']:#app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('show_entries'))

if __name__=='__main__':
    app.run(debug=True)
