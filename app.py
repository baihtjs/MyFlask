import uuid

from flask import Flask, render_template, request, make_response, Response, redirect, url_for, abort
from flask_script import Manager

app = Flask(__name__)
#manager = Manager(app=app)


@app.route('/')
def hello_world():
    a=10
    b=1
    c=a/b
    #return c
    return 'Hello World!'
@app.route('/hello')
def hello():
    print(request.remote_addr)
    if request.remote_addr=='192.168.1.4':
        return redirect(url_for('ab'))
    else:
        return render_template('hello.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/params/<hehe>')
def params(hehe):
    print(hehe)

    return 'huoqucanshu'

@app.route('/get/<string:name>',methods=['GET','POST'])
def get(name):
    return 'get/name'
    return name
@app.route('/getint/<int:name>')
def getint(name):
    return 'get/name'
    return str('name')

@app.route('/getpath/<path:name>')
def getpath(name):
    return 'get/name'
    return str(name)

@app.route('/getuuid')
def get_uuid():
    return str(uuid.uuid4())

@app.route('/request/',methods=['GET','POST'])
def req():
    #print(type(request))
    #print(request.data)
    #print(request.args)
    print(request.args.get('name'))
    print(request.args.get('password'))
    print(request.args.getlist('password'))
    #print(request.form)
    #print(request.files)
    #print(request.cookies)
    #print(request.remote_addr)
    #print(request.url)
    #print(request.user_agent)
    return '请求'

@app.route('/response/')
def rep():
    #result = render_template('hello.html')
    #print(result)
    #print(type(result))
    #response=make_response('<h2>我是H2的response！</h2>')
    # response=make_response(render_template('hello.html'))
    response=Response(response='<h2>我是自己构造的response！</h2>', status=403)
    print(type(response))
    return response

@app.route('/redirect/')
def redir():
   response=redirect(url_for('hello'))
   print(response)
   print(type(response))
   return response

   # return redirect(url_for('hello'))

@app.route('/abort')
def ab():
    print(request.remote_addr)
    abort(404)


if __name__ == '__main__':
   app.run(debug=True, port=8000, host='0.0.0.0')

