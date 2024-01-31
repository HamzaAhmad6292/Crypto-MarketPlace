from flask import Flask,request,render_template, redirect, url_for, jsonify,abort
import requests,json
import qrcode
import io
import base64
import datetime
import json
import ccxt
import talib
import plotly.graph_objs as go
from binance.client import Client
from datetime import datetime, timedelta
import numpy as np




app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/buy')
def buy():
    return render_template('buy.html')

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
    interval = request.args.get('interval', '4h') # replace with desired timeframe interval
    url = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval={interval}"
    response = requests.get(url)
    data = response.json()

    x_values = []
    open_values = []
    high_values = []
    low_values = []
    close_values = []
    candle_text = []

    for d in data:
        timestamp = int(d[0])/1000
        x_values.append(datetime.fromtimestamp(timestamp))
        open_values.append(float(d[1]))
        high_values.append(float(d[2]))
        low_values.append(float(d[3]))
        close_values.append(float(d[4]))
        candle_text.append(f"Open: {d[1]}<br>High: {d[2]}<br>Low: {d[3]}<br>Close: {d[4]}")

    trace_candlestick = go.Candlestick(x=x_values,
                                       open=open_values,
                                       high=high_values,
                                       low=low_values,
                                       close=close_values,
                                       name='Candlestick',
                                       text=candle_text,
                                       hoverinfo='text')

    rsi_values = talib.RSI(np.array(close_values), timeperiod=14)

    trace_rsi = go.Scatter(x=x_values,
                       y=rsi_values,
                       name='RSI',
                       yaxis='y2')  # Set visibility to 'legendonly'



    # add trace_rsi in the data list to show the rsi line

    volume_values = [float(d[5]) for d in data]

    color_values = ['green' if close > open else 'red' for close, open in zip(close_values, open_values)]

    trace_volume = go.Bar(
    x=x_values,
    y=volume_values,
    name='Volume',
    yaxis='y3',
    marker=dict(color=color_values),
    opacity=1)

    data = [trace_candlestick, trace_volume]


    layout = go.Layout(
    title=f"{pair} Candlestick Chart ({interval})",
    xaxis=dict(
        type='date',
        showgrid=False,  # Remove x-axis gridlines
        zeroline=False,  # Remove the white line on the x-axis
    ),
    yaxis=dict(fixedrange=False, showgrid=False),  # Remove y-axis gridlines and enable range selection
    yaxis2=dict(fixedrange=True, showgrid=False, overlaying='y', side='right'),  # RSI axis
    xaxis2=dict(anchor='y2', showgrid=False),  # RSI x-axis
    yaxis3=dict(fixedrange=True, showgrid=False, overlaying='y', side='right'),  # Volume axis

    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    hovermode='x',
    hoverdistance=-1,
    spikedistance=-1,
    width=900,  # Adjust the width of the graph (in pixels)
    height=450,  # Adjust the height of the graph (in pixels)
    margin=dict(t=40, b=40, r=40, l=40),  # Adjust the margins
    showlegend=False,  # Hide the legend
    dragmode='pan',  # Enable chart dragging
    uirevision='true',  # Preserve zoom/pan state during updates
    shapes=[dict(type='rect', xref='paper', yref='paper', x0=0, y0=0, x1=1, y1=1, fillcolor='rgba(0,0,0,0)', layer='below', line=dict(color='rgba(0,0,0,0)'))],  # Transparent overlay to capture events outside the chart area
)

    fig = go.Figure(data=data, layout=layout)

    total = 0.0  # Assign a default value to total

    if request.method == 'POST':
        order_type = request.form.get('order_type')
        quantity = float(request.form.get('quantity'))
        price = float(request.form.get('price'))

        if order_type == 'buy':
            # Perform buy order logic
            total = quantity * price
            print(total)
            print(quantity)
            print(price)
            # Implement buy order processing here...

        elif order_type == 'sell':
            # Perform sell order logic
            total = quantity * price
            print(total)
            print(quantity)
            print(price)
            # Implement sell order processing here...

        return render_template('trades.html', chart=fig.to_html(full_html=False), order_type=order_type, quantity=quantity, price=price, total=total)

    # Default values for order_type when it's not a POST request
    order_type = None
    quantity = None
    price = None
    total = None

    return render_template('trades.html', chart=fig.to_html(full_html=False), order_type=order_type, quantity=quantity, price=price, total=total)

#Api for updating date and time
@app.route('/nft')
def nft():

    return render_template('nft.html')



if __name__ == '__main__':
    app.run(debug=True)




#Api for updating date and time
@app.route('/datetime')
def get_datetime():
    now = datetime.datetime.now()
    date = now.strftime("%d") 
    time = now.strftime("%H:%M")
    return {'date': date, 'time': time}



if 5000 == '__main__':
    app.run(debug=True,port=5000)