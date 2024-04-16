from app import app
# from OpenSSL import SSL
 
app.secret_key = '6dbf23122cb5046cc5c0c1b245c75f8e43c59ca8ffeac292715e5078e631d0c9'
app.config['SESSION_TYPE'] = 'filesystem'

app.run(debug=True,host="0.0.0.0", port=5000, ssl_context=('./certificate/cert.pem', './certificate/key.pem'))
