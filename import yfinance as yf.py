import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Lấy dữ liệu cổ phiếu Tesla
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")

# Lấy dữ liệu cổ phiếu Tesla
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")

# Reset lại index
tesla_data.reset_index(inplace=True)
tesla_data.head()

url_tesla = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data_tesla = requests.get(url_tesla).text

tesla_revenue = pd.read_html(html_data_tesla, match="Tesla Quarterly Revenue")[0]
tesla_revenue.columns = ["Date", "Revenue"]

# Làm sạch cột Revenue
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$', "", regex=True)
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

tesla_revenue.tail()

gme = yf.Ticker("GME")
gme_data = gme.history(period="max")

gme_data.reset_index(inplace=True)
gme_data.head()

url_gme = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_gme = requests.get(url_gme).text

gme_revenue = pd.read_html(html_data_gme, match="GameStop Quarterly Revenue")[0]
gme_revenue.columns = ["Date", "Revenue"]

# Làm sạch cột Revenue
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$', "", regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

gme_revenue.tail()

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        subplot_titles=("Historical Share Price", "Historical Revenue"), 
                        vertical_spacing = .3)
    
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-06-4']
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), 
                             y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), 
                             y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    
    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)
    fig.show()

# Gọi hàm vẽ biểu đồ cho Tesla
make_graph(tesla_data, tesla_revenue, 'Tesla Stock Data Dashboard')

# Gọi hàm vẽ biểu đồ cho GameStop
make_graph(gme_data, gme_revenue, 'GameStop Stock Data Dashboard')