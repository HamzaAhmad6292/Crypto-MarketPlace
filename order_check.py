from flask import Flask, render_template, request, make_response,session,redirect,url_for
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
import ccxt
import plotly.graph_objs as go
from binance.client import Client
from datetime import datetime, timedelta
from App import conn


def check_order():
    cursor=conn.cursor()
    User_Id=session["User_Id"]
    cursor.execute("Select Wallet_Id from Users where User_Id='"+User_Id+"'")
    row1=cursor.fetchall()
    wallet_id=row1[0][0]

    cursor.execute("Select ,(wallet_id))
    row3=cursor.fetchall()
    if row3:
        i=0
        for i in range(len(row3)):

    
