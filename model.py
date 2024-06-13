import streamlit as st
import pandas as pd
import joblib
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Load animasi Lottie
lottie_animation = load_lottieurl("https://lottie.host/3384a5ff-1942-4ec7-8cfa-9e4270d819ac/YCD0F1erqt.json")

# Load model pipeline
with open('pipeline_model_randomforest.pkl', 'rb') as file:
    pipeline_model_randomforest = joblib.load(file)

def run():
    st.markdown("<h1 style='text-align: center; color:green;'>Eco Emission Predictor!</h1>", unsafe_allow_html=True)
   
    # Tampilkan animasi Lottie
    if lottie_animation:
        st_lottie(lottie_animation, height=480, key="chatbot")

    st.subheader('Track Your Carbon Footprint')

    # Buat form untuk input parameter
    with st.form(key='form_parameters'):
        make = st.selectbox('Brand', ('ACURA', 'ALFA ROMEO', 'ASTON MARTIN', 'AUDI', 'BENTLEY', 'BMW',
                                      'BUICK', 'CADILLAC', 'CHEVROLET', 'CHRYSLER', 'DODGE', 'FIAT',
                                      'FORD', 'GMC', 'HONDA', 'HYUNDAI', 'INFINITI', 'JAGUAR', 'JEEP',
                                      'KIA', 'LAMBORGHINI', 'LAND ROVER', 'LEXUS', 'LINCOLN', 'MASERATI',
                                      'MAZDA', 'MERCEDES-BENZ', 'MINI', 'MITSUBISHI', 'NISSAN',
                                      'PORSCHE', 'RAM', 'ROLLS-ROYCE', 'SCION', 'SMART', 'SRT', 'SUBARU',
                                      'TOYOTA', 'VOLKSWAGEN', 'VOLVO', 'GENESIS', 'BUGATTI'), index=1)
        
        vehicle_class = st.selectbox('Vehicle Class', ('COMPACT', 'SUV - SMALL', 'MID-SIZE', 'TWO-SEATER', 'MINICOMPACT',
                                                      'SUBCOMPACT', 'FULL-SIZE', 'STATION WAGON - SMALL',
                                                      'SUV - STANDARD', 'VAN - CARGO', 'VAN - PASSENGER',
                                                      'PICKUP TRUCK - STANDARD', 'MINIVAN', 'SPECIAL PURPOSE VEHICLE',
                                                      'STATION WAGON - MID-SIZE', 'PICKUP TRUCK - SMALL'), index=1)
        
        transmission = st.radio('Transmission', ['Automatic', 'Manual'])
        fuel_type = st.selectbox('Fuel Type', ('Premium Gasoline', 'Regular Gasoline', 'Ethanol', 'Diesel'), index=1)
        engine_size = st.slider('Engine Size', min_value=1.0, max_value=8.4, value=1.0, step=0.1)
        cylinders = st.number_input('Cylinders', min_value=1, max_value=16, value=1, step=1)
        fuel_consumption_liters = st.number_input('Fuel Consumption (L/100 km)', min_value=1.0, max_value=26.0, value=1.0, step=0.5)
        fuel_consumption_mpg = st.number_input('Fuel Consumption (mpg)', min_value=11, max_value=70, value=11, step=1)

        st.markdown('---')

        submitted = st.form_submit_button('Predict')

    # Prediksi berdasarkan input parameter
    data_inf = {
        'Make': make,
        'Vehicle Class': vehicle_class,
        'Transmission': transmission,
        'Fuel Type': fuel_type,
        'Engine Size(L)': engine_size,
        'Cylinders': cylinders,
        'Fuel Consumption Comb (L/100 km)': fuel_consumption_liters,
        'Fuel Consumption Comb (mpg)': fuel_consumption_mpg
    }

    data_inf = pd.DataFrame([data_inf])

    if submitted:       
        y_pred = pipeline_model_randomforest.predict(data_inf)
        st.write('The result is :')
        st.write(f'<p style="font-size:40px;">CO2 Emissions : {str(int(y_pred))} g/km</p>', unsafe_allow_html=True)

if __name__ == '__main__':
    run()
