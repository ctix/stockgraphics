#from peewee import SqliteDatabase, Model, \
#        IntegerField, CharField, TextField, DateTimeField
from peewee import *  ## fn.COUNT need it ???
from datetime import datetime
import time
from pathlib import Path
from dataStruct  import Mins,Equities
from accounts import User
from sanic import Sanic
from sanic_jwt import exceptions,initialize
from sanic.response import html,json,text, redirect
from sanic_jwt.decorators import protected


import hashlib, uuid

def _salt():
    return uuid.uuid4().bytes

def computed_password(salt, in_passwd):
    return hashlib.sha512(in_passwd + salt).digest()


def get_hq_dt(type):
    """get the current time ,return 3 types of datetime"""
    dt = time.localtime()
    hr, min = 9, 30
    if type == 'start':
        return datetime(dt.tm_year, dt.tm_mon, dt.tm_mday, hr, min, 0, 0)
    elif type == 'now':
        return datetime(dt.tm_year, dt.tm_mon, dt.tm_mday,
                        dt.tm_hour, dt.tm_min, dt.tm_sec, 0)
    # only get datum of the specified stock @1minute ago
    elif type == '1m_ago':
        return datetime(dt.tm_year, dt.tm_mon, dt.tm_mday,
                        dt.tm_hour, dt.tm_min-1, dt.tm_sec, 0)

def check_stored_auth(username, password):
    """ find in sqlite user table for username user_id , hash 
    password , and validating """

    try:   #if user doest exist ,then raise exceptions
        user = User.get(User.username == username)
    except:
        # raise exceptions.AuthenticationFailed("User not found.")
        return False

    bytes_password = password.encode()    # encode to bytes array
    hash_passwd = computed_password(user.salt,bytes_password)
    #if password != user.password:
    if hash_passwd != user.password:
        # raise exceptions.AuthenticationFailed("Password is incorrect.")
        return False
    else:
        return user



async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    auth_user = check_stored_auth(username,password)
    if not auth_user:
        raise exceptions.AuthenticationFailed("Error on User/password.")
    else:
        return  {"user_id": auth_user.id, "username": auth_user.username}



app = Sanic()
initialize(app, authenticate=authenticate)



LOGIN_FORM = '''
<h2>Please sign in, you can try:</h2>
<dl>
<dt>Username</dt> <dd>demo</dd>
<dt>Password</dt> <dd>1234</dd>
</dl>
<p>{}</p>
<form action="" method="POST">
  <input class="username" id="name" name="username"
    placeholder="username" type="text" value=""><br>
  <input class="password" id="password" name="password"
    placeholder="password" type="password" value=""><br>
  <input id="submit" name="submit" type="submit" value="Sign In">
</form>
'''

@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    message = 'The Initial Login Page'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # for demonstration purpose only, you should use more robust method
        auth_user = check_stored_auth(username,password)
        if not auth_user:
            message = 'invalid username or password'
            return html(LOGIN_FORM.format(message))
        else:
            #return redirect('/about')
            return redirect('/auth')
    else:
        return html(LOGIN_FORM.format(message))


@app.route("/protected")
@protected()
async def protected_route(request):
        return json({"protected": True})

# testing the protected content,ensure accessibility after 
# authentication
@app.route("/about")
@protected()
async def df_handler(request):
    # return json("HoW R U ,Now {}, \n start date,time ==> {}".format(now_dt, hq_st_dt))
    #return json(""" <html> <title>Available exposed Restful API</title>
    return html(""" <html> <title>Available exposed Restful API</title>
            <P> <h1>Available exposed Restful API
        <p>
		<HR align=left width=300 color=#987cb9 SIZE=3>
        <p>
            <p> <h2> http://ip_address/      ==> this help
            <p> http://ip_address/hq/stockcode  ==> dataset 1 minuts ago
            <p> http://ip_address/today/stockcode
                        ==>dataset of the stock from today market open
            <p> http://ip_address/date/stockcode+date  ==> the history date data
            <p> http://ip_address/stock_list  ==> recorded stock list 
            </html>""")


# the Rest api get the datum 1 minute ago
@app.route("/hq/<name:[A-z0-9]+>")
async def stock_hq_handler(request, name):
    hq_1min = get_hq_dt("1m_ago")
    result_lst = []
    minhq = Mins.select().where((Mins.stock == name)
                                & (Mins.dt > hq_1min))  # .limit
    for it in minhq:
        dt_str = (it.dt).strftime("%Y-%m-%d %H:%M:%S")
        result_lst.append([it.detail, dt_str])

    return json(result_lst)


@app.route("/today/<name:[A-z0-9]+>")
async def stock_hq_handler(request, name):
    # hq_today = get_hq_dt("now")
    hq_st_dt = get_hq_dt("start")
    result_lst = []
    minhq = Mins.select().where((Mins.stock == name)
                                & (Mins.dt > hq_st_dt))  # .limit
    for it in minhq:
        dt_ = it.dt
        dt_str = (dt_).strftime("%Y-%m-%d %H:%M:%S")
        result_lst.append([it.detail, dt_str])

    return json(result_lst)


@app.route("/date/<namedate:[A-z0-9]+>")
async def stock_his_handler(request, namedate):
    """handler query datum for the specified stock
    @ the history date"""
    result_lst = []
    name, yr, mn, dy = namedate[:8], namedate[8:12], namedate[12:14], namedate[14:]
    sdate = yr+"-"+mn+"-"+dy
    items = Mins.select().where((Mins.stock == name)
                                & (Mins.dt.contains(sdate)))
    for it in items:
        dt_ = it.dt
        dt_str = (dt_).strftime("%Y-%m-%d %H:%M:%S")
        result_lst.append([it.detail, dt_str])

    return json(result_lst)

# add the api for query the stock list
@app.route("/stock_list")
async def stock_list_handler(request):
    result_lst = []
    stklst = (Mins
		.select(Mins.stock,fn.COUNT(Mins.id).alias("total"))
		.group_by(Mins.stock)
		.distinct()
		)

    for stk in stklst:
        result_lst.append((stk.stock, stk.total))

    return json(result_lst)

# add the api for query the sino-us stock list
@app.route("/stock_list/us")
async def stock_list_handler(request):
    result_lst = []
    stklst = Equities.select()
    for stk in stklst:
        result_lst.append((stk.cname, stk.code,stk.category))

    return text(result_lst)

#output the prediction of the specified security 
@app.route("/predict/<name:[A-z0-9]+>")
async def predict__handler(request, name):
    result_lst = []
    stklst = Equities.select()
    for stk in stklst:
        result_lst.append((stk.cname, stk.code,stk.category))

    return json(result_lst)

#get retrieving securities from finance yahoo 
@app.route("/retrieve/<name:[A-z0-9]+>")
async def retrieve_handler(request,name):
    result_lst = []
    stklst = Equities.select()
    for stk in stklst:
        result_lst.append((stk.cname, stk.code,stk.category))


# Find out the wether or not the specfic model exists
@app.route("/modelexistenct/<name:[A-z0-9]+>")
async def find_model_handler(request,name):
    model_path = "/home/ctix/Dev/models/"
    modfile = Path(model_path+name)
    return  json( modfile.exists())

## TODO: add routes like "/ml/models/sid"
## machine learning applying various algorithms on security id
## May it be with parameters like predicting after number of days
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
