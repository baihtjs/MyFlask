import os
import uuid

import paramiko
from flask import Flask, render_template, request, make_response, Response, redirect, url_for, abort, json, session, \
    flash, send_from_directory
from flask_script import Manager
from flask_wtf.csrf import validate_csrf
from jinja2.utils import generate_lorem_ipsum
from jinja2 import escape
from flask import Markup
from wtforms import ValidationError

from forms import LoginForm, UploadForm, MultiUploadForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
app.config['MAX_CONTENT_LENGTH']=2*1024*1024
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']
#app = Flask(__name__,static_url_path='',root_path='/static')
#manager = Manager(app=app)

@app.context_processor
def inject_foo():
    foo='I am a foo.'
    return dict(foo=foo) #全局变量可传入模版
@app.template_global()
def bar():
    return 'I am a Bar.'

@app.route('/')
def index():
    return render_template('index.html')

'''
def hello_world():
    a=10
    b=1
    c=a/b
    #return c
    return 'Hello World!'
'''
@app.route('/hello')
def hello():
    name = request.cookies.get('name')
    print(request.remote_addr)
    if request.remote_addr=='192.168.1.4':
        return redirect(url_for('ab'))
    elif name=='admin':
        return '<h1>%s您好！'%name
    elif name=='root':
        return '<h1>%s您好！'%name
    else:
        return render_template('hello.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/params/<hehe>')
def params(hehe):
    print(hehe)

    return 'huoqucanshu'

@app.route('/register/',methods=['GET','POST'])
def reg():
    return render_template('register.html')
    req_log_name=request.form.get('username')
    print(req_log_name)

@app.route('/login/',methods=['GET','POST'])
def login():
    req_log_name = request.form.get('username')
    req_log_pass = request.form.get('password')
    if req_log_name=='admin' and req_log_pass=='admin':
        session['logged_in'] = True
        response = Response(response='<h2>%s登陆成功！</h2>' %req_log_name, status=200)
        response.set_cookie('name', req_log_name)
        print(type(response))
        return response
    elif req_log_name=='root' and req_log_pass=='root':
        session['logged_in'] = True
        response = Response(response='<h2>%s登陆成功！</h2>' %req_log_name, status=200)
        response.set_cookie('name', req_log_name)
        print(type(response))
        return response
    else:
        return '登陆失败！'
    print(req_log_name)
    print(req_log_pass)
    #return render_template('login.html')

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello_world'))


@app.route('/home')
def home():
    return render_template('login.html')

@app.route('/get/<string:name>',methods=['GET','POST'])
def get(name):
    #return name
    return '<h1>Hello %s!</h1>' % name

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
    name=request.cookies.get('name')
    #print(request.form)
    #print(request.files)
    #print(request.cookies)
    #print(request.remote_addr)
    #print(request.url)
    #print(request.user_agent)
    return '请求！%s已登录' %name

@app.route('/response/')
def rep():
    #result = render_template('hello.html')
    #print(result)
    #print(type(result))
    #response=make_response('<h2>我是H2的response！</h2>')
    # response=make_response(render_template('hello.html'))
    response=Response(response='<h2>我是自己构造的response！</h2>', status=403)
    response.set_cookie('name','Jack')
    print(type(response))
    return response

@app.route('/redirect/')
def redir():
   response=redirect(url_for('hello'))
   print(response)
   print(type(response))
   return response

   # return redirect(url_for('hello'))

@app.route('/abort/')
def ab():
    print(request.remote_addr)
    abort(302)

@app.route('/baidu/')
def baidu():
    return '',302,{'location':'https://www.baidu.com'}

@app.route('/json/')
def myjson():
   # print(name)
   # result = json.jsonify({'name':'value'})
    #result =json.jsonify(name='chalie', age=18)
    #result = json.dumps({'name':'chalie','age':18})
    result='{"name":"Tom","age":20 }'
    response=Response(response=result,content_type='application/json')
    print(result)
    print(type(result))
    return response
@app.route('/script/')
def script():
    return render_template('script.html')

@app.route('/config/',methods=['POST'])
def config():
    req_souceip = request.form.get('sourceip')
    req_destip = request.form.get('destip')
    req_destport = request.form.get('destport')
    ssh = paramiko.SSHClient()
    know_host = paramiko.AutoAddPolicy()
    # 加载创建的白名单
    ssh.set_missing_host_key_policy(know_host)

    # 连接服务器
    ssh.connect(
        hostname="172.16.0.18",
        port=22,
        username="moniter",
        password="2*2=5No"
    )
    print('username')

    # 执行命令
    stdin, stdout, stderr = ssh.exec_command("route")

    print(stdout.read().decode())
    ssh.close()

    return '<p>源ip为%s</p>' %req_souceip
@app.route('/admin/')
def admin():
    if 'logged_in' not in session:
        return render_template('login.html')
    else:
        response = redirect(url_for('req'))
        return response

@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something</a>' % url_for('do_something')

@app.route('/bar')
def bar():
    return '<h1>Ba page</h1><a href="%s">Do something</a>' % url_for('do_something')

@app.route('/do_something')
def do_something():
    #return redirect(url_for('hello'))
    return redirect(request.referrer or url_for('hello'))

@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
    <h1>A very long post</h1>
    <div class="body">%s</div>
    <button id="load1">Load More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $(function() {
        $('#load1').click(function() {
            $.ajax({
                url: '/more',
                type: 'get',
                success: function(data){
                    $('.body').append(data);
                }
            })
        })
    })
    </script>''' % post_body
@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)
@app.route('/xss')
def xss():
    name = request.args.get('name')
    #response='<h1>Hello,%s!</h1>' % name
    response='<h1>Hello,%s!</h1>' % escape(name)
    return response
#http://127.0.0.1:5000/xss?name=<script>window.location.href="https://www.baidu.com";</script>
#http://127.0.0.1:5000/xss?name=<script>alert("Bingo!");</script>

@app.route('/watchlist')
def watchlist():
    user1 = {
            'username' : 'Charlie',
            'bio' : 'A boy who loves movies and music.',
    }
    movies1 = [
        {'name': 'My neighbor Totoro', 'year': '1988'},
        {'name': 'Three Color', 'year': '1998'},
        {'name': 'Froest GUMPS', 'year': '2098'},
        {'name': 'Black Swans', 'year': '1978'},
    ]
    return  render_template('watchlist.html', user2=user1, movies2=movies1)

@app.route('/banner')
def banner():
    return render_template('_banner.html')

@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')

@app.template_test()
def baz(n):
    if n == 'baz1':
        return True
    else:
        return False
@app.route('/flash')
def just_flash():
    flash('I am flash,who is looking for me?')
    return redirect(url_for('index'))
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'),404

@app.errorhandler(500)
def server_internal_err(e):
    return "500错误"
@app.route('/my_login')
def my_login():
    return render_template('my_login.html'),200

@app.route('/basic',methods=['GET', 'POST'])
def basic():
    form1=LoginForm()
    print(request.form.get('username'))
    if form1.validate_on_submit():
        username = form1.username.data
        flash('Welcome home,%s!'% username)
        return redirect(url_for('index'))
    return render_template('basic.html',form=form1)

@app.route('/bootstrap')
def bootstrap():
    form=LoginForm()
    return render_template('bootstrap.html',form=form)
@app.route('/upload',methods=['GET','POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f=form.photo.data
        filename=random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload Success!')
        session['filenames'] = [filename]
        print(session['filename'])
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)

def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename=uuid.uuid4().hex + ext
    return new_filename

@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')

@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)



def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/multi-upload',methods=['GET','POST'])
def multi_upload():
    form = MultiUploadForm()

    if request.method == 'POST':
        filenames = []

        # check csrf token
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error.')
            return redirect(url_for('multi_upload'))

        # check if the post request has the file part
        if 'photo' not in request.files:
            flash('This field is required.')
            return redirect(url_for('multi_upload'))

        for f in request.files.getlist('photo'):
            # if user does not select file, browser also
            # submit a empty part without filename
            # if f.filename == '':
            #     flash('No selected file.')
            #    return redirect(url_for('multi_upload'))
            # check the file extension
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(
                    app.config['UPLOAD_PATH'], filename
                ))
                filenames.append(filename)
            else:
                flash('Invalid file type.')
                return redirect(url_for('multi_upload'))
        flash('Upload success.')
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)


if __name__ == '__main__':
   app.run(debug=True, port=8000, host='0.0.0.0')

