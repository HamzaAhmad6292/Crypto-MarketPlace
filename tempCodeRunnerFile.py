@app.route('/trade/<pair>')
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
        x_values.append(datetime.fromtimestamp(timestamp))
        open_values.append(float(d[1]))
        high_values.append(float(d[2]))
        low_values.append(float(d[3]))
        close_values.append(float(d[4]))

    trace = go.Candlestick(x=x_values,
                           open=open_values,
                           high=high_values,
                           low=low_values,
                           close=close_values,
                           xaxis='x1',
                           yaxis='y1')

    data = [trace]
    layout = go.Layout(title=f"{pair} Candlestick Chart ({interval})",
                       xaxis=dict(domain=[0, 1], fixedrange=False, type='date'),
                       yaxis=dict(domain=[0.2, 1], autorange=True, fixedrange=False),
                       xaxis_showgrid=False,  # Remove x-axis gridlines
                       yaxis_showgrid=False,  # Remove y-axis gridlines
                       plot_bgcolor='rgba(0,0,0,0)',
                       paper_bgcolor='rgba(0,0,0,0)',
                       hovermode='x',
                       hoverdistance=-1,
                       spikedistance=-1)

    fig = go.Figure(data=data, layout=layout)
    if request.method == 'POST':
        # Handle the submitted order form
        order_type = request.form.get('order_type')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        # Process the order here...

    return render_template('trades.html', chart=fig.to_html(full_html=False))

