from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
# Import mo rin dito yung gamit mong MySQL connector (hal. flask_mysqldb o pymysql)

app = Flask(__name__)
app.secret_key = 'lagyan_mo_ng_secret_key_dito'

oauth = OAuth(app)

# ==========================================
# 1. ILAGAY DITO ANG KEYS MO
# ==========================================
facebook = oauth.register(
    name='facebook',
    client_id='2093978184656683',          # <-- I-paste ang App ID dito
    client_secret='723f57831a12e6e151714d16c1c9790d',  # <-- I-paste ang App Secret dito
    access_token_url='https://graph.facebook.com/v18.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v18.0/dialog/oauth',
    api_base_url='https://graph.facebook.com/v18.0/',
    client_kwargs={'scope': 'email public_profile'}
)

# ==========================================
# 2. LOGIN ROUTE
# ==========================================
@app.route('/login/facebook')
def login_facebook():
    # Ginamit ko na yung Tailscale URL mo para iwas error sa redirect
    redirect_uri = 'https://127.0.0.1:5000/auth/facebook/callback'
    return facebook.authorize_redirect(redirect_uri)

# ==========================================
# 3. CALLBACK & MYSQL ROUTE
# ==========================================
@app.route('/auth/facebook/callback')
def facebook_callback():
    # Kukunin nito yung data mula kay FB
    token = facebook.authorize_access_token()
    resp = facebook.get('me?fields=id,name,email')
    user_info = resp.json()
    
    email = user_info.get('email')
    name = user_info.get('name')
    
    # Para ma-test mo muna na gumagana bago mo buhayin yung database code:
    # return f"Success pre! Pangalan: {name} | Email: {email}"

    # ---------------------------------------------------------
    # KAPAG READY NA ANG DATABASE MO, TANGGALIN ANG COMMENT (#) SA BABA:
    # ---------------------------------------------------------
    
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM users WHERE email = %s", [email])
    # account = cur.fetchone()
    
    # if account:
    #     # May record na, i-login agad
    #     session['logged_in'] = True
    #     session['email'] = email
    #     return redirect('/dashboard')
    # else:
    #     # First time mag-login via FB, i-save sa DB
    #     cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    #     mysql.connection.commit()
    #     
    #     session['logged_in'] = True
    #     session['email'] = email
    #     return redirect('/dashboard')

if __name__ == '__main__':
    # I-run mo ito tapos buksan mo yung Tailscale link mo
    app.run(debug=True, port=5000)