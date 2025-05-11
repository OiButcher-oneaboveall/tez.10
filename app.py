
import streamlit as st
from optimizer import run_ga
import os

cities = ["Rafineri", "Gürpınar", "Yenikapı", "Selimiye", "İçerenköy", "Tophane", "Alibeyköy", "İstinye"]

st.set_page_config(layout="wide")
st.title("🚛 GA Optimizasyon Testi (DEBUG)")

os.makedirs("scenarios", exist_ok=True)

pop_size = st.slider("Popülasyon Büyüklüğü", 50, 500, 200)
generations = st.slider("Nesil Sayısı", 100, 2000, 1000)
max_risk = st.slider("Maksimum Risk", 0.5, 3.0, 1.5, 0.1)

if st.button("🚀 Hesapla (Test)"):
    with st.spinner("⛽ Optimizasyon çalışıyor..."):
        route, dist, time, risk, log = run_ga(pop_size, generations, max_risk)
        st.write("🔍 GA Çıktısı:")
        st.write("route:", route)
        st.write("dist:", dist)
        st.write("time:", time)
        st.write("risk:", risk)
        st.write("log:", log)
        if not route:
            st.warning("❗ Rota üretilemedi. Parametreleri gözden geçirin veya max_risk değerini artırın.")
