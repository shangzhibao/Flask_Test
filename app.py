from flask import Flask,render_template,request,redirect,url_for,session
import os

app = Flask(__name__)
# 【重要】随便写一串随机字符串，用来加密cookie，自己保存好不要泄露
app.secret_key = "your-secret-random-string-123456abc"
# 全局访问密码，你改成自己想要的
WEB_PASSWORD = "123456"

# 在所有请求之前拦截，统一校验登录状态
@app.before_request
def check_login():
    # 登录页面本身不需要校验，防止死循环
    if request.path == "/login":
        return
    # 判断是否已经登录
    if not session.get("is_logged_in"):
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pwd = request.form.get("password", "")
        if pwd == WEB_PASSWORD:
            # 验证成功，标记登录，permanent=True 代表长期记住（默认31天）
            session["is_logged_in"] = True
            session.permanent = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", msg="密码错误，请重新输入！")
    return render_template("login.html", msg="")


@app.route('/')
def home():
    techs = ['HTML','CSS','Flask','Python']
    name = '30天Python编程'
    return render_template('home.html',techs = techs,name = name,title = '主页')

@app.route('/about')
def about():
    name = '30天Python编程'
    return render_template('about.html',name = name,title = '关于我们')

@app.route('/post')
def post():
    # name = '编程语言文章'
    num = request.args.get('num', type = int)
    return render_template('post.html',num = num,title = '影片播放')

@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    old_job = request.form['old_job']
    current_job = request.form['current_job']
    country = request.form['country']
    print(name, old_job, current_job, country)
    result_data = {
        'name':name,
        'old_job': old_job,
        'current_job': current_job,
        'country':country
    }
    return render_template('result.html', result_data = result_data, title= '结果')

@app.route('/bmi',methods = ['GET'])
def bmi_page():
    return render_template('bmi.html',title = 'BMI计算')

@app.route('/bmi_result',methods = ['POST'])
def bmi_result():
    height = float(request.form.get('height'))
    weight = float(request.form.get('weight'))
    bmi_value = round(weight / (height ** 2),2)
    if bmi_value < 18.5:
        msg = "偏瘦"
    elif 18.5 <= bmi_value < 24:
        msg = "正常"
    elif 24 <= bmi_value < 28:
        msg = "超重"
    else:
        msg = "肥胖"
    return render_template('bmi.html',title = 'BMI结果',bmi = bmi_value,info = msg)

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(debug= False,host= '0.0.0.0',port = port)
