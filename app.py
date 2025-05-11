
import streamlit as st
import os, json
from optimizer import run_ga
from visualizer import (
    plot_gantt, plot_folium_route,
    plot_scenario_comparison, plot_emission_energy_comparison
)
from streamlit_folium import st_folium

cities = ["Rafineri", "Gürpınar", "Yenikapı", "Selimiye", "İçerenköy", "Tophane", "Alibeyköy", "İstinye"]
SCENARIO_DIR = "scenarios"
os.makedirs(SCENARIO_DIR, exist_ok=True)

st.set_page_config(layout="wide", page_title="Çok Amaçlı Rota Optimizasyonu", page_icon="📌")
with open("style.css") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

tabs = st.tabs([
    "🚀 Yeni Optimizasyon", "⚙️ Parametreler", "📈 Sonuçlar", "🗺️ Harita",
    "🌱 Emisyon ve Enerji", "🕒 Gantt Şeması", "📂 Senaryo Karşılaştırma"
])

with tabs[0]:
    st.header("🚀 Senaryo Bilgisi")
    senaryo_adi = st.text_input("Senaryo Adı", value="Senaryo_1")
    kullanici = st.text_input("Kullanıcı", value="Kullanıcı")

with tabs[1]:
    st.header("⚙️ GA Parametreleri")
    pop_size = st.slider("Popülasyon", 50, 500, 200)
    generations = st.slider("Nesil", 100, 2000, 1000)
    max_risk = st.slider("Maksimum Risk", 0.5, 3.0, 1.5, step=0.1)

    hedef = st.radio("🔧 Optimizasyon Hedefi", [
        "Minimum Mesafe", "Minimum Süre", "Minimum Risk", "Maksimum Ortalama Hız"
    ])
    
    with st.form("optimizasyon_formu"):
        submitted = st.form_submit_button("🚀 Optimizasyonu Başlat")

if submitted:
    with st.spinner("Rota optimize ediliyor..."):
        route, dist, time, risk, log = run_ga(pop_size, generations, max_risk, hedef)
        st.write("🔍 **Çıktılar**")
        st.write("➡️ Rota:", route)
        st.write("📏 Mesafe:", dist)
        st.write("⏱ Süre:", time)
        st.write("☢️ Risk:", risk)
        if time > 0:
            avg_speed = round(dist / (time / 60), 2)
            st.write("🚀 Ortalama Hız:", avg_speed, "km/h")
        else:
            avg_speed = 0
        if not route:
            st.warning("Rota bulunamadı. max_risk'i artırın.")
        else:
            st.session_state["result"] = {
                "route": route, "dist": dist, "time": time,
                "risk": risk, "log": log, "avg_speed": avg_speed,
                "name": senaryo_adi
            }
            st.success("Rota başarıyla oluşturuldu.")

with tabs[2]:
    if "result" in st.session_state:
        r = st.session_state["result"]
        st.write("📌 Senaryo:", r["name"])
        st.write("📏 Mesafe:", r["dist"], "km")
        st.write("⏱ Süre:", r["time"], "dk")
        st.write("☢️ Risk:", r["risk"])
        st.write("🚀 Ortalama Hız:", r["avg_speed"], "km/h")
        if st.button("💾 Senaryoyu Kaydet"):
            with open(os.path.join(SCENARIO_DIR, r["name"] + ".json"), "w") as f:
                json.dump(r, f)
            st.success("Kaydedildi.")
    else:
        st.info("Henüz senaryo oluşturulmadı.")

with tabs[3]:
    if "result" in st.session_state:
        route_names = [cities[i] for i in st.session_state["result"]["route"]]
        harita = plot_folium_route(route_names)
        st_folium(harita, use_container_width=True)

with tabs[4]:
    if "result" in st.session_state:
        dist = st.session_state["result"]["dist"]
        co2 = round(dist * 0.2, 2)
        kwh = round(dist * 0.25, 2)
        st.metric("🌍 CO₂", f"{co2} kg")
        st.metric("⚡ Enerji", f"{kwh} kWh")

with tabs[5]:
    if "result" in st.session_state:
        fig = plot_gantt(st.session_state["result"]["log"])
        st.plotly_chart(fig, use_container_width=True)

with tabs[6]:
    files = [f for f in os.listdir(SCENARIO_DIR) if f.endswith(".json")]
    selected = st.multiselect("📂 Senaryoları Seç", files, default=files[:2] if len(files)>=2 else files)
    if selected:
        loaded = []
        for f_name in selected:
            with open(os.path.join(SCENARIO_DIR, f_name)) as f:
                d = json.load(f)
                d["name"] = f_name.replace(".json", "")
                loaded.append(d)
        st.plotly_chart(plot_scenario_comparison(loaded), use_container_width=True)
        st.plotly_chart(plot_emission_energy_comparison(loaded), use_container_width=True)
