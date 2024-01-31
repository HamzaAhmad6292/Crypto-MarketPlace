from flask import Flask, render_template, request, make_response,session,redirect,url_for, jsonify,abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import requests
import pyodbc
from getprice import get_price_in_usdt
import pandas as pd 
import requests,json
import qrcode
import io
import base64
import datetime
import json

import json
import ccxt
import plotly.graph_objs as go
from binance.client import Client
from datetime import datetime, timedelta



app = Flask(__name__)
app.secret_key = 'my_secret_ke'

server = '.'
database = 'proj'
driver = '{SQL Server}'


conn_str = f"""
    DRIVER={driver};
    SERVER={server};
    DATABASE={database};
    Trusted_Connection=yes;
"""

conn = pyodbc.connect(conn_str)




    
    
#  @app.route('/login',methods=["GET","POST"])

#  def converter():
#     session=db.session()

#     currency_from='USDT'
#     currency_to='BUSD'
#     ammount=5
#     response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={currency_from}&vs_currencies={currency_to}")
#     if response.status_code==200:
     
#      try:

#         conversion_rate = response.json()[currency_from][currency_to]
#         converted_ammount=ammount*conversion_rate
#         keyword='e'
#      except keyword as e:
#         return 'nigga error'

#         wallet=session.query(Wallet).filter_by(Wallet_Id='1',User_Id='1',Currency_code=currency_from).first()
#         if wallet is true :
#             wallet.Balance+=converted_ammount
#             wallet.Currency_code=currency_to
#             wallet.Last_update=datetime.utnow()
#             session.commit()
#         else:
#             return render_template('post.html')


@app.route("/")
def great():
    return render_template("index.html")




@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["GET","POST"])
def signupform():
   
         name = request.form.get('txt')
         email = request.form.get('email')
         password = request.form.get('pswd')
         action=request.form.get('action')
         cursor = conn.cursor()
         cursor.execute("SELECT * FROM Users WHERE name = ? AND email = ?", (name, email))
         rows = cursor.fetchall()
         if rows:
           
            error = "User already exists!"
            return "User Already Exist!"
         else:
            u_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            w_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')


            user_id = f"{name}-{u_timestamp}"
            wallet_id = f"{w_timestamp}"
            
            cursor.execute("insert into Wallet(Wallet_Id) values( '"+wallet_id+"');INSERT INTO Users (User_ID, Name, Email, Password,Wallet_Id) VALUES (?, ?, ?, ?,?)", (user_id, name, email, password,wallet_id))
            conn.commit()
           
            return render_template("signup.html")
         
       
    
@app.route("/login", methods=["GET","POST"])
def loginform():
    cursor=conn.cursor()
    email = request.form.get('log_email')
    password = request.form.get('log_pswd')
    cursor.execute("SELECT * FROM Users WHERE Password = ? AND Email = ?", (password, email))
    rows = cursor.fetchall()
    if rows:
        check_email=rows[0][2]
        check_pass=rows[0][3]
        user_id=rows[0][0]
        wallet_id=rows[0][4]
        session['User_Id']=user_id
        session['Wallet_Id']=wallet_id
        conn.commit()
        return redirect(url_for('dashboard'))
    else :
        conn.commit()
        return "Login failed"
    



@app.route('/dashboard')
def dashboard():
    
    cursor=conn.cursor()
    User_Id=session["User_Id"]
    cursor.execute("Select Wallet_Id from Users where User_Id='"+User_Id+"'")
    
    row1=cursor.fetchall()
    wallet_id=row1[0][0]
    
    dollar='usdt'
    cursor.execute("Select sum(Balance) from Wallet where Wallet_Id=? and Currency_code=?",(wallet_id,dollar))
    row2=cursor.fetchall()
    if row2:
     Balance_dollar=row2[0][0]
    else:
        Balance_dollar=0.0
    


    btc='btc'
    currency=[]
    total_usdt=0
    total_btc=0
    cursor.execute("Select Balance,Currency_code from Wallet where Wallet_Id=?",(wallet_id))
    row3=cursor.fetchall()
    if row3:
        i=0
        for i in range(len(row3)):
            if row3[i][1]=='usdt':
                x = int(row3[i][0])
                total_usdt=total_usdt+x
            else:
               get = str(row3[i][1])
               quantity=float(row3[i][0])
               get = get.upper()
               price=get_price_in_usdt(get,quantity)

               total_usdt=total_usdt+price
        
        one_btc=get_price_in_usdt('BTC',1)
        one_btc = float(one_btc)
        total_btc=total_usdt/one_btc



    else:
        total_btc=0.0
        total_usdt=0.0
    id=[]
    wallet_from=[]
    wallet_to=[]
    Price=[]
    Currency=[]
    Type=[]
    Quantity=[]

    cursor.execute("Select Transaction_Id,Wallet_Id_from,Wallet_Id_to,Price,Currency,Quantity,Type from transactions where Wallet_Id_to=?",(wallet_id))
    transactions=cursor.fetchall()
    for row in transactions:
        id.append(row.Transaction_Id)
        wallet_from.append(row.Wallet_Id_from)
        wallet_to.append(row.Wallet_Id_to)
        Price.append(row.Price)
        Currency.append(row.Currency)
        Type.append(row.Type)
        Quantity.append(row.Quantity)
    # items= id+ '  ' +wallet_from+'  ' +'  '+wallet_to+'  '+Price+'  '+Currency+'  '+Type+'  '+Quantity   
    items=id
    item2=wallet_to



    return render_template('dashboard.html',items=items,port_val=total_usdt,port_val_btc=total_btc)



@app.route('/buy')
def buy():
    return render_template('/buy.html')


@app.route('/Submit',methods=["GET","POST"])
def bought():
    cursor=conn.cursor()

  
    u_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    deposit_id = f"{u_timestamp}"
    
    User_Id=session['User_Id']
    Wallet_id_to=session['Wallet_Id']
    card_name=request.form.get('card-name')
    card_num=request.form.get('card-number')
    exp_date=request.form.get('expiry-date')
    cvv=request.form.get('cvv')
    amount=request.form.get('usdt-amount')
    Wallet_id_from='NULL Address'
    type='Bought'
    currency='usdt'

    datenow=datetime.datetime.now().date().strftime('%Y-%m-%d')
    cursor.execute("INSERT INTO Deposit (Deposit_Id, User_Id, Wallet_Id, Card_Name, Card_Num, Ammount, Currency, CVV, Date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (deposit_id, User_Id, Wallet_id_to, card_name, card_num, amount, 'usdt', cvv, datenow))
    
    cursor.execute('select * from Wallet where Wallet_Id=? and Currency_code=?',(Wallet_id_to,"usdt"))
    row=cursor.fetchall()
    
    
    if not row:
     cursor.execute("EXEC InsertWallet @WalletIdTo=?,@CurrencyCode=?,@Balance=?", Wallet_id_to, 'usdt', amount)
    else: 
     cursor.execute('EXEC UpdateWalletBalance @Amount = ?,@WalletIdTo = ?,@CurrencyCode=?',(amount,Wallet_id_to,currency))
    
    
    cursor.execute("EXEC InsertTransaction ?, ?, ?, ?, ?, ?, ?,?", deposit_id, Wallet_id_from, Wallet_id_to, amount, 'usdt',amount, datenow, type)
    
    conn.commit()


    return redirect(url_for('dashboard'))

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/deposit-withdrawal')
def deposit_withdrawal_addy():
    #hamza vro compute the crypto address here and store it in var "addy"
    addy='0x1213124151'

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data("address:" + addy)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to a base64-encoded string and embed it in the HTML
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    qr_src = f"data:image/png;base64,{img_str}"

    return render_template('deposit-withdrawal.html', address=addy, qr_src=qr_src)



@app.route('/withdraw', methods=['POST'])
def withdraw():
    coin_id = request.form['coin']
    amount = float(request.form['amount'])
    address = request.form['address']
    return 'Withdrawal successful'
    


@app.route('/markets',methods=['POST','GET'])
def market():
    response = requests.get("https://api.binance.com/api/v3/ticker/24hr")
    data = response.json()
    usdt_pairs = [d for d in data if d['symbol'].endswith('USDT')]
    top_200 = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)[:200]
    
    query = request.args.get('q')
    if query:
        top_200 = [coin for coin in top_200 if query.lower() in coin['symbol'].lower()]
        
    return render_template('markets.html', top_200=top_200, query=query)

#For Trading
@app.route('/trade/<pair>', methods=['GET', 'POST'])
def trade(pair):
    interval = request.args.get('interval', '1M') # replace with desired timeframe interval
    url = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval={interval}"
    response = requests.get(url)
    data = response.json()

    x_values = []
    open_values = []
    high_values = []
    low_values = []
    close_values = []

    for d in data:
        timestamp = int(d[0])/1000
        x_values.append(datetime.datetime.fromtimestamp(timestamp))
        open_values .append(float(d[1]))
        high_values .append(float(d[2]))
        low_values  .append(float(d[3]))
        close_values.append(float(d[4]))

    trace = go.Candlestick(x=x_values,
                           open=open_values,
                           high=high_values,
                           low=low_values,
                           close=close_values)

    data = [trace]
    layout = go.Layout(
        title=f"{pair} Candlestick Chart ({interval})",
        xaxis=dict(type='date', showgrid=False),  # Remove x-axis gridlines
        yaxis=dict(fixedrange=True, showgrid=False),  # Remove y-axis gridlines
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x',
        hoverdistance=-1,
        spikedistance=-1
    )


    fig = go.Figure(data=data, layout=layout)

    if request.method == 'POST':
        cursor=conn.cursor()

        User_Id=session['User_Id']
        
        order_type = request.form.get('order_type')
        quantity = float(request.form.get('quantity'))
        price = float(request.form.get('price'))
        currency = pair.replace('usdt', "")
        current_datetime = datetime.datetime.now()


        # to get wallet Id 
        cursor.execute("Select Wallet_Id from Users where User_Id='"+User_Id+"'")
        row1=cursor.fetchall()
        wallet_id=row1[0][0]
        order_id='order'+wallet_id


        if order_type == 'buy':
            cursor.execute("EXEC InsertOrder ?, ?, ?, ?, ?, ?, ?, ?, ?", order_id, User_Id, wallet_id, order_type, 'usdt', currency, price, quantity, 'pending')
            total = quantity * price
            # Implement buy order processing here...
            cursor.execute('Update Wallet set Balance=Balance+? where Wallet_ID=? and Currency_code=?',(quantity,wallet_id,currency))
            cursor.execute('Update Wallet set Balance=Balance-? where Wallet_ID=? and Currency_code=?',(quantity,wallet_id,'usdt'))


        elif order_type == 'sell':
            cursor.execute("EXEC InsertOrder ?, ?, ?, ?, ?, ?, ?, ?, ?", order_id, User_Id, wallet_id, order_type, currency, 'usdt', price, quantity, 'pending')
            cursor.execute('Update Wallet set Balance=Balance-? where Wallet_ID=? and Currency_code=?',(quantity,wallet_id,currency))
            cursor.execute('Update Wallet set Balance=Balance+? where Wallet_ID=? and Currency_code=?',(quantity,wallet_id,'usdt'))

            # Perform sell order logic
            total = quantity * price
            # Implement sell order processing here...








        url = "https://api.binance.com/api/v3/ticker/price?symbol="+currency
        response = requests.get(url)
        data = response.json()
        real_price = float(data['price'])
        
        if price == real_price or abs(price - real_price) / real_price <= 0.1:
            cursor.execute('update Orders set Status=? where Wallet_Id=? and Currency_to=?',('Done',wallet_id,currency))
            cursor.execute("EXEC InsertTransaction ?, ?, ?, ?, ?, ?, ?,?",order_id,'Coin_Fusion', wallet_id, price, currency, quantity,current_datetime, order_type)
            



    
        return render_template('trades.html', chart=fig.to_html(full_html=False), order_type=order_type, quantity=quantity, price=price, total=total)

    return render_template('trades.html', chart=fig.to_html(full_html=False))


 

@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    cursor=conn.cursor()
    User_Id=session["User_Id"]
    cursor.execute("Select Wallet_Id from Users where User_Id='"+User_Id+"'")
    row1=cursor.fetchall()
    wallet_id=row1[0][0]
    # Retrieve portfolio data from DB
    total_usdt=0
    cursor.execute("Select Balance,Currency_code from Wallet where Wallet_Id=?",(wallet_id))
    row3=cursor.fetchall()
    if row3:
        i=0
        for i in range(len(row3)):
            if row3[i][1]=='usdt':
                x = int(row3[i][0])
                total_usdt=total_usdt+x
            else:
               get = str(row3[i][1])
               quantity=float(row3[i][0])
               get = get.upper()
               price=get_price_in_usdt(get,quantity)

               total_usdt=total_usdt+price



    cursor.execute('Select distinct Currency_code,Balance from Wallet where Wallet_Id=?',(wallet_id))
    rows = cursor.fetchall()

    currency_codes = []
    balances = []
    for row in rows:
        currency_codes.append(row.Currency_code)
        balances.append(row.Balance)
    
    balances.append(12)
    balances.append(12000)
    
    session['Assets']=currency_codes
    session['Assets_Quantity']=balances
    return render_template('portfolio.html',total_portfolio=total_usdt,assets=currency_codes)




























if __name__ == '__main__':
    app.run(debug=True)




#Api for updating date and time
@app.route('/datetime')
def get_datetime():
    now = datetime.datetime.now()
    date = now.strftime("%d") 
    time = now.strftime("%H:%M")
    return {'date': date, 'time': time}




#Api for updating date and time
@app.route('/nft')
def nft():

    return render_template('nft.html')


#Api for updating date and time


@app.route('/pie-data')
def pie_data():
    asset=session["Assets"]
    balances=[]
    balances.append(12)
    balances.append(12000)
    
    return {'asset_name': asset, 'total_amount': balances}


@app.route('/port-history')
def port_history():
    month=['jan','feb','mar','apr','may','june','july','aug']
    port_worth=['26000','2000','2500','12000','2000','10000','10','999']
    return {'month_names': month, 'port_val': port_worth}



@app.route('/nft/marketplace')
def marketplace():
    return render_template('nft-marketplace.html')



# Sample NFT data
nfts = [
    {"id": 1, "image": "https://miro.medium.com/v2/resize:fit:670/0*iXFSD9fZ-AD73K3P.jpg", "price": 10},
    {"id": 2, "image": "https://miro.medium.com/v2/resize:fit:670/0*iXFSD9fZ-AD73K3P.jpg", "price": 20},
    {"id": 3, "image": "https://miro.medium.com/v2/resize:fit:670/0*iXFSD9fZ-AD73K3P.jpg", "price": 30}
]


@app.route('/nft-info')
def get_nft_info():
    return jsonify(nfts)

@app.route('/purchase')
def purchase_confirmation():
    # Perform purchase confirmation logic here
    # Calculate remaining balance, handle purchase confirmation, etc.
    remaining_balance = 80

    return render_template('purchase.html', balance=remaining_balance)



if __name__== '__main__':
    app.run(debug=True)
    
    





