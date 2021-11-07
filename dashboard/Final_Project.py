# Nama Muhammad Nabil Fadhlurrahman
# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
import squarify
import seaborn as sns
import streamlit as st
import warnings 
warnings.filterwarnings('ignore')
sns.set(rc={'figure.figsize':(8,8)})
plt.style.use('dark_background')

current_palette_7 = sns.color_palette("hls", 7)
sns.set_palette(current_palette_7)

# {Start Config}
st.set_page_config(page_title='My Dashboard',layout='wide')
st.title("Perilaku Konsumen pada Supermarket Dayang Sumbi")
data = pd.read_csv('supermarket_sales - Sheet1.csv',parse_dates=True)
data.index = data.Date
data.head()
tsa = data.copy()
# {End Config}
# {Descriptive Statistics}
col1,col2,col3 = st.columns(3)
col1.metric('Total Konsumen : ', len(data['Invoice ID']))
col2.metric('Total Pendapatan : ', int(sum(data['gross income'])))
col3.metric('Kepuasan Pelanggan : ', (data['Rating'].mean()))
# {Start Sidebar}
st.sidebar.header("Supermarket Dayang Sumbi")
st.sidebar.subheader("Settings")
st.sidebar.text('Analisis Deret Waktu:')
ets = st.sidebar.radio('> ETS Decomposition', ['False','True'])
st.sidebar.text('Segmentasi Konsumen:')
active = st.sidebar.checkbox('Munculkan Filter Segmentasi Konsumen')
if active:
  selection_filter = st.sidebar.radio('> Pilih Filter',['Payment','Gender','Product line','City'])
  selection_class = st.sidebar.selectbox('> Pilih Class', data[selection_filter].unique())
  modified_ = data[data[selection_filter]==str(selection_class)]
  data = modified_
st.sidebar.text('Analisis Pendapatan:')
a = st.sidebar.checkbox('> Munculkan Analisis Pendapatan')
if a:
  filter_ = st.sidebar.radio('> Pilih Filter',['Total','cogs','gross income'])
  

# {End Sidebar}

# {Start Line 1}
# Time Series Analysis
from statsmodels.tsa.filters.hp_filter import hpfilter  #The Hodrick-Prescott (HP) filter refers to a data-smoothing technique

# Config Line 1
st.header("Analisis Deret Waktu")
baris1_col1,baris1_col2 = st.columns((2,2))
# {Start Columns 1}
### Time Series Analysis for Number of Transaction
tsa_ID = tsa['Invoice ID'].copy()
tsa_ID = tsa_ID.groupby('Date').count()
tsa_ID = pd.DataFrame(tsa_ID)
id_cycle, id_trend = hpfilter(tsa_ID)
tsa_ID['Trend ID'] = id_trend
fig1,ax1 = plt.subplots()
tsa_ID['Invoice ID'].plot(kind='line')
tsa_ID['Trend ID'].plot(style='--')
ax1.set_xlabel('Data Deret Waktu') #Set keterangan sumbu x
ax1.set_ylabel('Banyaknya Transaksi')
baris1_col1.subheader('Pergerakan Transaksi Kosumen')
ax1.legend()
baris1_col1.pyplot(fig1)
# {End Columns 1}

# {Start Columns 2}
### Time Series Analysis for Number of Quantity
fig2,ax2 = plt.subplots()
tsa_Quantity = tsa['Quantity'].copy()
tsa_Quantity = tsa_Quantity.groupby('Date').sum()
tsa_Quantity = pd.DataFrame(tsa_Quantity)
tsa_Quantity['Quantity'].plot(kind='line')
quantity_cycle, quantity_trend = hpfilter(tsa_Quantity)
tsa_Quantity['Trend Quantity'] = quantity_trend
tsa_Quantity['Trend Quantity'].plot(style='--')
ax2.set_xlabel('Data Deret Waktu') #Set keterangan sumbu x
ax2.set_ylabel('Banyaknya Barang')
baris1_col2.subheader('Pergerakan Kuantitas Barang')
ax2.legend()
baris1_col2.pyplot(fig2)
# {End Line 1}
# {Shadow Line }
if ets =='True':
  shadow1,shadow2 = st.columns((2,2))
  # Shadow 1
  shadow1.subheader('ETS dari Banyak Transaksi')
  shadow1.image('./id_ets.png')
  shadow2.subheader('ETS dari Kuantiti Barang')
  shadow2.image('./quantity_ets.png')
# {Shadow Line End}
# {Start Line 2}
# Config Line 2
  
st.header("Segmentasi Konsumen")
if active:
  col1,col2 = st.columns(2)
  col1.metric('Filter: ', selection_filter)
  col2.metric('Class: ', selection_class)
  
baris2_col1,baris2_col2 = st.columns((2,2))
# {Start Columns 1}
### Time Series Analysis for Number of Quantity
fig3,ax3 = plt.subplots()

data_ = [i for i in data.Payment.value_counts()]
labels = [i for i in data.Payment.unique()]
#create pie chart
plt.pie(data_, labels = labels, autopct='%.00f%%')
baris2_col1.subheader('Proporsi Payment Konsumen')
ax3.legend()
baris2_col1.pyplot(fig3)
# {End Columns 1}
# {Start Columns 2}
### Gender Pie
fig4,ax4 = plt.subplots()
data_ = [i for i in data.Gender.value_counts()]
labels = [i for i in data.Gender.unique()]
#create pie chart
plt.pie(data_, labels = labels, autopct='%.00f%%')
baris2_col2.subheader('Prosentase Gender Konsumen')
my_circle=plt.Circle( (0,0), 0.7, color='Black')
p=plt.gcf()
p.gca().add_artist(my_circle)
ax4.legend()
baris2_col2.pyplot(fig4)
# {End Columns 2}
# {End Line 2}
# {Start Line 3}
# Config Line 3
baris3_col1,baris3_col2 = st.columns((2,2))
# {Start Columns 1}
fig5,ax5 = plt.subplots()
df = pd.DataFrame({'kind':[i for i in data['Product line'].value_counts()], 'group':[i for i in data['Product line'].unique()] })
# plot 
squarify.plot(sizes=df['kind'], label=df['group'], alpha=.8 )
plt.axis('off')
baris3_col1.subheader('Peta Pohon Jenis Produk')
baris3_col1.pyplot(fig5)
# {End Columns 1}
# {Start Columns 2}
fig6,ax6 = plt.subplots()
df = pd.DataFrame({'kind':[i for i in data['City'].value_counts()], 'group':[i for i in data['City'].unique()] })
# plot 
squarify.plot(sizes=df['kind'], label=df['group'], alpha=.8 )
plt.axis('off')
baris3_col2.subheader('Peta Pohon Kota Konsumen')
baris3_col2.pyplot(fig6)
# {End Columns 2}
# {End Line 3}

# {Start Line 4}
if a:
  st.header('Analisis Pendapatan')
  # Config Line 3
  baris4_col1,baris4_col2 = st.columns(2)
  revenue = tsa.copy()
  # {Start Columns 1}
  # plot1
  fig7,ax7 = plt.subplots()
  baris4_col1.subheader('Analisis Rerata '+filter_+' Terhadap Product Line')
  revenue = data.groupby('Product line').mean().round(2).reset_index()
  ax = sns.barplot(data=revenue,x='Product line',y=filter_)
  plt.xticks(rotation = 20)
  for p in ax.patches:
      ax.annotate(f'\n{p.get_height()}', (p.get_x()+0.3, p.get_height()), ha='center', va='bottom', color='white', size=15)
  baris4_col1.pyplot(fig7)
  # {End Columns 1}
  # {Start Columns 2}
  fig8,ax8 = plt.subplots()
  baris4_col2.subheader('Analisis Rerata '+filter_ +' Terhadap City')
  revenue = data.groupby('City').mean().round(2).reset_index()
  ax = sns.barplot(data=revenue,x='City',y=filter_)
  plt.xticks(rotation = 45)
  for p in ax.patches:
      ax.annotate(f'\n{p.get_height()}', (p.get_x()+0.3, p.get_height()), ha='center', va='bottom', color='white', size=15)
  baris4_col2.pyplot(fig8)
  # {End Line 4}
