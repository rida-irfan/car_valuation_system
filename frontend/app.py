import streamlit as st
import requests

st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="centered")

st.markdown("""
<style>
    body { background-color: #0d0d0d; color: #ffffff; }
    .title {
        font-size: 42px; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #6c5ce7, #00cec9);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .subtitle { font-size: 18px; text-align: center; color: #dfe6e9; margin-bottom: 20px; }
    .neon-box {
        background: rgba(20,20,20,0.8); padding: 20px; border-radius: 12px;
        border: 2px solid #6c5ce7; box-shadow: 0px 0px 15px #6c5ce7; margin-bottom: 20px;
    }
    .prediction-box {
        background: rgba(30,30,30,0.9); padding: 20px; border-radius: 12px;
        border: 2px solid #00cec9; text-align: center; font-size: 26px;
        box-shadow: 0px 0px 20px #00cec9; margin-top: 25px;
    }
    .stButton button {
        background: linear-gradient(90deg, #6c5ce7, #00cec9); color: white; border-radius: 10px;
        padding: 10px 20px; font-size: 18px; border: none; box-shadow: 0px 0px 10px #6c5ce7;
        transition: 0.3s;
    }
    .stButton button:hover { box-shadow: 0px 0px 20px #00cec9; transform: scale(1.02); }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🚗 Car Price Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your Car Price, predicted by AI</div>", unsafe_allow_html=True)

makes = ['Toyota', 'Suzuki', 'Daihatsu', 'Honda', 'Hyundai', 'Mitsubishi',
         'KIA', 'Changan', 'FAW', 'Mercedes', 'Chevrolet']
models_dict = {
    'Toyota': ['Corolla XLI', 'Corolla GLI', 'Altis Grande', 'Corolla Axio', 'Yaris', 'Prius'],
    'Suzuki': ['Swift', 'Wagon R', 'Baleno', 'Cultus VXR', 'Mehran VXR', 'Mehran VX', 'Cultus VXL'],
    'Daihatsu': ['Passo', 'Move', 'Cuore', 'Minica', 'Minicab Bravo', 'Ek Wagon'],
    'Honda': ['City IDSI', 'City Vario', 'Civic Prosmetic', 'City IVTEC', 'City Aspire', 'Civic Oriel', 'Civic EXi', 'Civic VTi', 'Civic VTi Oriel'],
    'Hyundai': ['Santro', 'Alsvin', 'Liana', 'Surf'],
    'Mitsubishi': ['Pajero Mini', 'Hijet'],
    'KIA': ['Sportage', 'V2'],
    'Changan': ['Joy', 'Classic'],
    'FAW': ['X-PV'],
    'Mercedes': ['E Class', 'C Class', 'Exclusive'],
    'Chevrolet': ['Spectra', 'ISIS']
}
fuels = ['Petrol', 'CNG', 'Hybrid', 'Diesel']
assembly = ['Imported', 'Local']
transmission = ['Automatic', 'Manual']
documents = ['Original', 'Duplicate']

st.markdown("<div class='neon-box'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

# Make and Model outside form so they update immediately when changed
with col1:
    Make = st.selectbox("Make", makes, key="make_select")
    Year = st.number_input("Year", min_value=1990, max_value=2024, value=2019, key="year_input")
    Fuel = st.selectbox("Fuel", fuels, key="fuel_select")
    Assembly = st.selectbox("Assembly", assembly, key="assembly_select")
    CarAge = st.number_input("Car Age", min_value=0, value=5, key="carage_input")
    
with col2:
    # Get models for selected Make - updates immediately when Make changes
    available_models = models_dict.get(Make, [])
    Model = st.selectbox("Model", available_models, key=f"model_select_{Make}")
    KMs = st.number_input("KM's driven", min_value=0, value=95000, key="kms_input")
    Transmission = st.selectbox("Transmission", transmission, key="transmission_select")
    CarDocuments = st.selectbox("Car documents", documents, key="documents_select")

st.markdown("</div>", unsafe_allow_html=True)

submit = st.button("Predict Price", type="primary", use_container_width=True)

if submit:
    data = {
        "Make": Make,
        "Model": Model,
        "Year": Year,
        "KM's driven": KMs,
        "Fuel": Fuel,
        "Car documents": CarDocuments,
        "Assembly": Assembly,
        "Transmission": Transmission,
        "Car Age": CarAge
    }
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=data, timeout=10)
        result = response.json()
        
        if 'error' in result:
            st.error(f"Backend Error: {result['error']}")
        elif 'prediction' in result:
            price = result['prediction'][0]
            st.markdown(f"<div class='prediction-box'>Estimated Price:<br><br><b>Rs {price:,}</b></div>", unsafe_allow_html=True)
        else:
            st.error(f"Unexpected response: {result}")
    except requests.exceptions.ConnectionError:
        st.error("Backend not responding! Make sure FastAPI is running on http://127.0.0.1:8000")
    except requests.exceptions.Timeout:
        st.error("Backend request timed out. Please try again.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
