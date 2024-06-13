import streamlit as st
import pandas as pd
from PIL import Image
import requests
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.stats import f_oneway

def run():

    st.markdown("<h1 style='text-align: center; color: #FF6347;'>Pengaruh Jenis Bahan Bakar terhadap Emisi CO2</h1>", unsafe_allow_html=True)
    
    st.subheader('Analisis Perbandingan Bahan Bakar Regular Gasoline, Premium Gasoline, Diesel and Ethanol')
    st.write('by :  [Muhammad Daffa Miqoilla](https://www.linkedin.com/in/muhammad-daffa-miqoilla-2b17aa282/)')
    st.caption('E-mail : Miqoilla@gmail.com')
    # Read Data
    df = pd.read_csv('CO2_emissions_clean.csv')
    
    image = Image.open(requests.get('https://sparkoncept.com/wp-content/uploads/2022/03/17.-What-percentage-of-carbon-emissions-come-from-cars-1536x823.jpg', stream=True).raw)
    left_co, cent_co, last_co = st.columns([1, 4, 1])  # Adjust the ratio to make the central column wider
    with cent_co:
        st.image(image, use_column_width=True)  # Ensure the image uses the column width

 
    st.write('''
    Perubahan iklim global dan masalah lingkungan semakin menjadi perhatian utama di seluruh dunia. Salah satu kontributor utama terhadap perubahan iklim adalah emisi gas rumah kaca, termasuk emisi karbon dioksida (CO2) yang dihasilkan oleh sektor transportasi. Transportasi merupakan sektor dengan ketergantungan tertinggi pada bahan bakar fosil, yang menyebabkan emisi CO2 lebih tinggi dibandingkan sektor lainnya.

    Menurut laporan International Energy Agency (IEA) tahun 2021, sektor transportasi menyumbang sekitar 37% dari total emisi CO2. Studi terbaru dari IEA menunjukkan bahwa Kanada merupakan salah satu negara penyumbang emisi CO2 dari transportasi tertinggi, dengan total **206g/km** pada tahun 2021 ([National Observer](https://www.nationalobserver.com/2019/09/04/analysis/canadian-cars-are-worlds-dirtiest-ev-age-essential)). Peningkatan jumlah kendaraan bermotor menjadi tantangan besar bagi generasi saat ini, terutama di Kanada, untuk menurunkan tingkat emisi CO2.

    Selain itu, penting untuk memahami dampak jenis bahan bakar terhadap emisi CO2. Dalam industri otomotif, terdapat beberapa jenis bahan bakar umum, seperti bensin reguler, bensin premium, diesel, dan etanol. Setiap jenis bahan bakar memiliki karakteristik yang berbeda dan dapat mempengaruhi tingkat emisi CO2 yang dihasilkan oleh kendaraan. Analisis perbandingan antara jenis bahan bakar ini dapat memberikan wawasan yang berharga tentang dampak lingkungan yang dihasilkan oleh masing-masing jenis bahan bakar.
    ''')

    st.markdown("<br>", unsafe_allow_html=True)

    st.header('Dataset CO2 Emissions')
    st.dataframe(df)
    st.caption("Data Source: The data has been taken and compiled from the [Canada Goverment](https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64#wb-auto-6) official link ")
    st.markdown("<br>", unsafe_allow_html=True)


    total,year= st.columns(2)

    # Visualisasi brand
    table_brand1, table_brand2 = st.columns([1,1])
    st.markdown("<br>", unsafe_allow_html=True)

   
    with table_brand1: 
        st.subheader('Top 10 Brand Mobil yang paling banyak digunakan')
        make_count = df['Make'].value_counts().head(10)
        label_brand = make_count.index.tolist()
        values_brand = make_count.values.tolist()
        fig_make = px.pie(names=label_brand,
                          values= values_brand,
                          color_discrete_sequence=px.colors.sequential.RdBu,
                          title='Brand Mobil',)
        fig_make.update_traces(textposition='inside', texttemplate='%{label} (%{value} ')
    
        st.plotly_chart(fig_make)
        st.write('''Data menampilkan jumlah kendaraan berdasarkan Brand dan kuantitasnya. Dalam gambar diatas, terdapat beberapa merek kendaraan populer.
                    **Ford** menjadi Brand mobil kendaraan yang paling populer dengan jumlah pemakaian sebanyak 628 diikuti dengan **Chevrolet** 586, **BMW** 526, **Merchedes Benz** dan lain-lain''')
    

    with table_brand2: 
        st.subheader('Bahan bakar yang paling banyak digunakan')
        fuel_count = df['Fuel Type'].value_counts()
        label_fuel = fuel_count.index.tolist()
        values_fuel = fuel_count.values.tolist()
        fig_fuel = px.pie(names=label_fuel,
                          values= values_fuel,
                          color_discrete_sequence=px.colors.sequential.Redor,
                          title='Jenis Bahan Bakar',)
        fig_fuel.update_traces(textposition='inside', texttemplate='%{label} (%{value}) ')

        st.plotly_chart(fig_fuel)
        st.write('''Jika kita lihat dari jumlah pemakaian jenis bahan. Pemakaian jenis Gasoline sangat mendominasi seperti **Regular Gasoline** sebanyak 3632 dan **Premium Gasoline** 3197
        diikuti dengan **Ethanol** 368 pemakaian dan **Deisel** yang hanya 174 pemakaian''')


    st.markdown("<h2>Korelasi antara jenis bahan bakar, konsumsi, dan kapasitas mesin terhadap emisi CO2.</h2>", unsafe_allow_html=True)
    table_fuel1, table_fuel2 = st.columns([1,1])
    st.header('\n')

   

    with table_fuel1: 
        st.subheader('Top 5 brand yang menghasilkan Emisi CO2 paling banyak')
        top5_brand = df.groupby(df['Make'])[['CO2 Emissions(g/km)']].mean().sort_values(by='CO2 Emissions(g/km)', ascending=False).head(5)

        fig = px.bar(top5_brand, x=top5_brand.index, 
                    y='CO2 Emissions(g/km)', 
                    color='CO2 Emissions(g/km)', 
                    labels={'CO2 Emissions(g/km)': 'Emisi CO2'},
                    title='Rata-Rata Emisi CO2 per Brand',
                    color_continuous_scale='oranges')
    
        fig.update_traces(textposition='outside', texttemplate='%{y:.2f}')
    
        st.plotly_chart(fig)
        st.write('''Diatas merupakan gambar dari 5 brand yang paling banyak menghasilkan emisi karbon dioksida
                    **Bugatti** merupakan brand mobil yang paling banyak menyumbang emisi gas karbon dikosida dengan rataan sebesar **522g/km**
                    diikuti dengan **Lamborghini, SRT, Rolls-Royce dan Bentley**''')
    
    with table_fuel2: 
        st.subheader('Bahan bakar yang menghasilkan Emisi CO2 paling banyak')
        fuel = df.groupby(df['Fuel Type'])[['CO2 Emissions(g/km)']].mean().sort_values(by='CO2 Emissions(g/km)', ascending=False)

        fig = px.bar(fuel, x=fuel.index, 
                    y='CO2 Emissions(g/km)', 
                    color='CO2 Emissions(g/km)', 
                    labels={'CO2 Emissions(g/km)': 'Emisi CO2'}, 
                    title='Rata-Rata Emisi CO2 dari setiap Bahan Bakar',
                    color_continuous_scale='oranges')
    
        fig.update_traces(textposition='outside', texttemplate='%{y:.2f}')
    
        st.plotly_chart(fig)
        st.write('''Jika kita lihat dari jenis bahan bakar, mobil dengan bahan bakar **Ethanol** menjadi yang paling banyak menyumbang gas emisi karbon dioksida (CO2)
        dan yang bahan bakar yang paling sedikit adalah Regular Gasoline''')



 #--------------------------------------------------------
    left, central,right = st.columns([1,2,1])
    with central:

        fig1 = px.scatter(df, x='Fuel Consumption Comb (L/100 km)', y='CO2 Emissions(g/km)')
        fig2 = px.scatter(df, x='Fuel Consumption Comb (L/100 km)', y='Engine Size(L)', color='Cylinders', color_continuous_scale='reds')

        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(fig1['data'][0], row=1, col=1)
        fig.add_trace(fig2['data'][0], row=1, col=2)

        # Atur rentang sumbu x dan y
        fig.update_xaxes(range=[df['Fuel Consumption Comb (L/100 km)'].min(), df['Fuel Consumption Comb (L/100 km)'].max()], row=1, col=1)
        fig.update_yaxes(range=[df['CO2 Emissions(g/km)'].min(), df['CO2 Emissions(g/km)'].max()], row=1, col=1)
        fig.update_xaxes(range=[df['Fuel Consumption Comb (L/100 km)'].min(), df['Fuel Consumption Comb (L/100 km)'].max()], row=1, col=2)
        fig.update_yaxes(range=[df['Engine Size(L)'].min(), df['Engine Size(L)'].max()], row=1, col=2)
        st.subheader('Dampak konsumsi bahan bakar dan Kapasitas Mesin terhadap Emisi CO2')
        fig.update_layout(
            height=500,  # Atur tinggi gambar
            width=750,  # Atur lebar gambar
            xaxis=dict(title='Fuel Consumption Comb (L/100 km)'),  # Label sumbu x untuk gambar pertama
            yaxis=dict(title='CO2 Emissions(g/km)'),  # Label sumbu y untuk gambar pertama
            xaxis2=dict(title='Fuel Consumption Comb (L/100 km)'),  # Label sumbu x untuk gambar kedua
            yaxis2=dict(title='Engine Size(L)')  # Label sumbu y untuk gambar kedua
        )
        st.plotly_chart(fig)
        st.write('''Jika dilihat korelasi antara konsumsi bahan bakar dengan Emisi gas karbon dioksida maka korelasinya berbanding lurus, semakin besarnya konsumsi bahan bakar maka akan menghasilkan emisi karbon dioksida (CO2)
        yang lebih tinggi. Selain itu tingkat konsumsi bahan bakar juga dipengaruhi oleh besarnya kapasitas mesin mobil yang digunakan. maka dapat disimpulkan bahwa emisi gas karbon dioksida (CO2) sangat dipengaruhi oleh 
        besarnya kapasitas mesin mobil dan juga banyaknya konsumsi bahan bakar yang digunakan''')

    with st.expander('Apakah Jenis bahan bakar memiliki pengaruh yang Signifikan terhadap Emmisi gas CO2?'):
        st.subheader('Uji Hipotesis Testing (ANOVA)')
        st.write('''Untuk melihat apakah jenis bahan bakar berpengaruh terhadap emisi gas CO2 maka perlu dilakukan tes uji Hipotesis testing agar kita tahu
        apakah memiliki pengaruh yang signifikan atau tidak, pada pengujian kali ini methode yang dilakukan adalah ANOVA.
        Tes ANOVA menjadi metode yang paling cocok dalam konteks ini karena proyek ini karena ANOVA dapat melakukan uji untuk membandingkan 3 atau lebih variabel data''')
        st.write('Hipotesis Nol (H0): Tidak ada perbedaan signifikan dalam emisi CO2 antara jenis bahan bakar.')
        st.write('Hipotesis Alternatif (H1): Terdapat perbedaan signifikan dalam emisi CO2 antara jenis bahan bakar.')
        st.subheader('\n')

        bensin_regular = df[df['Fuel Type'] == 'Regular Gasoline']['CO2 Emissions(g/km)']
        bensin_premium = df[df['Fuel Type'] == 'Premium Gasoline']['CO2 Emissions(g/km)']
        diesel = df[df['Fuel Type'] == 'Diesel']['CO2 Emissions(g/km)']
        etanol = df[df['Fuel Type'] == 'Ethanol']['CO2 Emissions(g/km)']

        stat, p_value = f_oneway(bensin_regular, bensin_premium, diesel, etanol)

        # Menampilkan hasil
        st.write('Hasil Uji ANOVA:')
        from decimal import Decimal

        p_value_formatted = format(Decimal(p_value), '0.2e')
        st.write('P-value:', p_value_formatted)

        st.write(r'''Telah dilakukan Hipotesis Testing dengan menggunakan pengujian statistik ANOVA, untuk melihat apakah terdapat perbedaan yang signifikan Emisi karbon dioksida (CO2) yang dihasilkan pada setiap jenis bahan bakar (bensin\_regular, bensin\_premium, diesel dan etanol).
        Hasil dari uji ANOVA menunjukkan bahwa nilai p-value yang diperoleh sangat kecil ($1.112 \times 10^{-124}$). Karena nilai p-value lebih kecil dari tingkat signifikansi yang telah ditentukan (biasanya $\alpha = 0.05$),
        kita dapat menolak hipotesis nol (tidak ada perbedaan signifikan) sehingga dapat disimpulkan bahwa terdapat perbedaan signifikan dalam emisi CO2 antara jenis bahan bakar yang diuji dan Ethanol merupakan bahan bakar yang paling banyak menyumbang emisi gas karbon dioksida(CO2).''')




    one,two,three = st.columns([1,2,1])
    with two:
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<h1 style='text-align: center;'>Recommendation</h1>", unsafe_allow_html=True)
        st.write('''Demi menjawab tantangan untuk mengurangi tingkat emisi gas karbon dioksida (CO2) hal yang paling efektif adalah dengan cara mengganti kendaraan yang digunakan dari kendaraan konvensional menjadi kendaraan bermotor listrik, 
        namun tidak semua orang dapat membeli kendaraan bermotor listrik dikarenakan harganya yang cenderung lebih mahal dibandingkan kendaraan konvensional,
        sehingga berdasarkan data emisi karbon dioksida (CO2) di Negara Kanada, dapat disimpulkan bahwa penggunaan jenis bahan bakar memiliki dampak signifikan terhadap emisi CO2. Sebagai rekomendasi alternatif demi menurunkan tingkat emisi karbon dioksida yang dihasilkan, baiknya calon pengguna kendaraan lebih piintar untuk memilih jenis bahan bakar yang akan digunakan pada kendaraannya. karena mobil yang menggunakan bahan bakar
        **Regular Gasoline dan Diesel**  menghasilkan emisi karbon dioksida(CO2) lebih rendah 235.1 g/km dan 237.8 g/km dibandingkan dengan **Ethanol dan Premium Gasoline** yang menghasilkan emisi karbon dioksida (CO2) lebih tinggi sebesar 275.1 g/km dan 266.1 g/km. Berikut adalah beberapa alasan yang mendukung rekomendasi tersebut:''')
        st.write('1. Emisi CO2 yang Lebih Rendah: Mobil yang menggunakan regular gasoline dan diesel cenderung memiliki emisi CO2 yang lebih rendah dibandingkan dengan jenis bahan bakar lainnya. Hal ini berarti penggunaan jenis bahan bakar ini dapat membantu mengurangi jejak karbon dan dampak lingkungan yang dihasilkan.')
        st.write('2. Ketersediaan dan Infrastruktur: Regular gasoline dan diesel adalah jenis bahan bakar yang umum dan mudah ditemukan di stasiun pengisian bahan bakar. Infrastruktur yang mendukung penggunaan bahan bakar ini juga lebih luas dan tersedia secara luas di berbagai wilayah.')
        st.write('3. Efisiensi Konsumsi Bahan Bakar: Mobil yang menggunakan regular gasoline dan diesel umumnya memiliki efisiensi konsumsi bahan bakar yang baik. Hal ini dapat menghasilkan penggunaan bahan bakar yang lebih efisien dan mengurangi ketergantungan terhadap bahan bakar.')
        st.write('4. Pilihan Kendaraan yang Tersedia: Sebagian besar produsen mobil menawarkan berbagai pilihan kendaraan yang menggunakan regular gasoline dan diesel. Hal ini memberikan fleksibilitas bagi konsumen untuk memilih kendaraan yang sesuai dengan kebutuhan dan preferensi mereka.')
        
        fuel_types = ['All'] +['Regular Gasoline', 'Diesel','Premium Gasoline','Ethanol']

        # Kolom filter
        selected_fuel = st.selectbox('Jenis Bahan Bakar', fuel_types)

        if selected_fuel == 'All':
            filtered_data = df.groupby(df['Fuel Type'])[['CO2 Emissions(g/km)']].mean().sort_values(by='CO2 Emissions(g/km)', ascending=False)
        else:
            filtered_data = df[df['Fuel Type'] == selected_fuel]

        # Hitung rata-rata emisi CO2 berdasarkan jenis bahan bakar
        fuel = filtered_data.groupby('Fuel Type')['CO2 Emissions(g/km)'].mean().sort_values(ascending=False).head(5)

        # Buat bar chart
        fig = px.bar(fuel, x=fuel.index, y='CO2 Emissions(g/km)', 
                    color='CO2 Emissions(g/km)', 
                    labels={'CO2 Emissions(g/km)': 'Emisi CO2'},
                    title='Rata-Rata Emisi CO2 dari Setiap Bahan Bakar',
                    color_continuous_scale='oranges')

        fig.update_traces(textposition='outside', texttemplate='%{y:.2f}')

        # Tampilkan chart
        st.plotly_chart(fig)
                
        st.write('Sebelum melakukan pembelian mobil, juga penting untuk mempertimbangkan faktor lain seperti efisiensi bahan bakar secara keseluruhan, biaya perawatan, ketersediaan suku cadang, dan juga pertimbangan pribadi seperti preferensi lingkungan dan kenyamanan penggunaan.')


        data_lower = pd.DataFrame(df.groupby('Make')[['CO2 Emissions(g/km)']].mean().sort_values(by=('CO2 Emissions(g/km)')))
        st.write(data_lower)
        st.write('''Jika kita lihat berdasarkan Brand mobil, akan lebih baik pengguna mobil membeli mobil yang menghasilkan emisi CO2 yang rendah. dari data diatas dapat kita lihat bahwa Top 5 mobil dengan emisi CO2 terendah adalah
        **SMART, HONDA, FIAT, MAZDA, MINI**''')


if __name__ == '__main__':
    run()
