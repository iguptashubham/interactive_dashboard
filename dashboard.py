#importing Modules

import streamlit as st #dashboard
import pandas as pd #data manipulation
import datetime
from PIL import Image as img #for image
import plotly.express as px #data visualization
import plotly.graph_objects as go #data visualization

#Read the excel data

df = pd.read_excel('Adidas.xlsx')

#page configuration

st.set_page_config(page_title='Adidas Sales Dashboard', page_icon='logo1.png',layout='wide')

#mardown

st.markdown('<style>div.block-container{padding-top:1rem;</style>', unsafe_allow_html=True)

image = img.open('logo1.png') #open the image

#columns 1,2
col1, col2 = st.columns([0.1,0.9])

#with column 1
with col1:
  st.image(image, width=90)
  
#with column 2
html_title = """
  <style>
  .title-text{
  font-weight:bold;
  padding:5px;
  border-radius:6px;
  }
  </style>
  <center><h1 class='title-text'>Adidas Sales Dashboard</h1></center>
  """
 
with col2:
  st.markdown(html_title, unsafe_allow_html=True)
  
#columns 3,4,5
col3, col4, col5 = st.columns([0.1,0.45,0.45])

#with column 3
with col3:
  box_date = str(datetime.datetime.now().strftime('%d %B %Y'))
  st.write(f'last Updated by: \n {box_date}')
  
#with column 4
with col4:
  fig = px.bar(df, x ='Retailer', y ='TotalSales', labels={'TotalSales':'TotalSales {$}'}, title = 'Total Sales by Retailer', hover_data=['TotalSales'], template='gridon', height=500)
  
  st.plotly_chart(fig, use_container_width=True)

_, view1, down1, view2, down2 = st.columns([0.15,0.20,0.20,0.20,0.20])

with view1:
  #dropdown expander with data
  expander = st.expander('Retailer Wise Sales')
  data = df[['Retailer','TotalSales']].groupby('Retailer')['TotalSales'].sum()
  expander.write(data)

with down1:
  st.download_button('Get Data', data = data.to_csv().encode('utf-8'),file_name='Retailersales.csv',mime = 'text/csv')
  
df['month_year'] = df['InvoiceDate'].dt.strftime("%b'%y")
data2 = df.groupby('month_year')['TotalSales'].sum().reset_index()
  
#with column 5
with col5:
  fig1 = px.line(data2, x='month_year', y='TotalSales', labels={'TotalSales':'TotalSales {$}'},title='Total Sales by Year',hover_data=['TotalSales'], template='plotly_white', height=500)
  
  st.plotly_chart(fig1, use_container_width=True)
  
with view2:
  expander = st.expander('Total Sales by Year')
  data2 = df[['month_year','TotalSales']].groupby('month_year')['TotalSales'].sum()
  expander.write(data2)
  
with down2:
  st.download_button('Get Data', data = data2.to_csv().encode('utf-8'),file_name='Total Sales by Year',mime='txt/csv')
  
st.divider()

result1 = df.groupby('State')[['TotalSales','UnitsSold']].sum().reset_index()

#addd the units sold as a line chart on secondary y axis  

fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1['State'], y = result1['TotalSales'], name="Total Sales"))
fig3.add_trace(go.Scatter(x=result1['State'],y=result1['UnitsSold'], mode = 'lines', name = 'units sold', yaxis = 'y2'))

fig3.update_layout(
  title = 'Total Sales and units sold by state',
  xaxis = dict(title='State'),
  yaxis=dict(title='Total Sales', showgrid = False),
  yaxis2 = dict(title='Units Sold', overlaying = 'y', side = 'right'),
  template = 'plotly_white',
  legend = dict(x=1,y=1)
  )
# add the units sold as a line chart on a secondary y-axis


_, col6 = st.columns([0.1,1])
with col6:
    st.plotly_chart(fig3,use_container_width=True)
    
_, view3, down3 = st.columns([0.5,0.45,0.45])

with view3:
  expander = st.expander('Sales by units sold')
  expander.write(result1)
  
with down3:
  st.download_button('get_data', data = result1.to_csv().encode('utf-8'), file_name='Sales by units Sold', mime='text/csv')
  
st.divider()

#treemap charts

_, col7 = st.columns([0.1,1])

treemap1 = df[['Region','City','TotalSales']].groupby(['Region','City'])['TotalSales'].sum().reset_index()

def format_sales(value):
  if value >=0:
    return '{:.2f} lakh'.format(value / 1_000_00)
  
treemap1['Total sales(format)'] = treemap1['TotalSales'].apply(format_sales)

fig4 = px.treemap(treemap1, path=['Region','City'], values='TotalSales',hover_name='Total sales(format)', hover_data=['Total sales(format)'], color = 'City', height=700, width=600)

fig4.update_traces(textinfo='label+value')

with col7:
  st.subheader(":point_right: Total Sales by Region and city in Treemap")
  st.plotly_chart(fig4, use_container_width=True)
  
_, view4, down4 = st.columns([0.5,0.45,0.45])

with view4:
  result2 = df[['Region','City','TotalSales']].groupby(['Region','City'])['TotalSales'].sum()
  expander = st.expander('Total sales by region and city')
  expander.write(result2)
  
with down4:
  st.download_button('Get Data', data = result2.to_csv().encode('utf-8'), file_name='Total Sales by Region and City', mime='Text/csv')
  
st.divider()

_, view5, down5 = st.columns([0.1,1,0.25])

with view5:
  expander = st.expander('View rales Data')
  expander.write(df)
  
with down5:
  st.download_button('Raw Data', data = df.to_csv().encode('utf-8'), file_name='raw_data', mime = 'text/csv')
  
st.divider()