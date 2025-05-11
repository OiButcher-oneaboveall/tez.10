
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

# Arayüz ayarları
st.set_page_config(layout="wide", page_title="Rota Optimizasyonu", page_icon="🚛")
with open("style.css") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

tabs = st.tabs([
    "🚀 Yeni Optimizasyon", "⚙️ Parametreler", "📈 Sonuçlar", "🗺️ Harita",
    "⛽ Bekleme Animasyonu", "🌱 Emisyon ve Enerji", "🕒 Gantt Şeması",
    "📊 Parametre Analizi", "📂 Senaryo Karşılaştırma"
])

with tabs[0]:
    st.header("🚛 Yeni Senaryo Bilgileri")
    senaryo_adi = st.text_input("Senaryo Adı", value="Senaryo 1")
    kullanici = st.text_input("Kullanıcı Adı", value="Misafir")
    st.success(f"👤 {kullanici} tarafından oluşturuluyor: **{senaryo_adi}**")

with tabs[1]:
    st.header("⚙️ Genetik Algoritma Parametreleri")
    pop_size = st.slider("Popülasyon Büyüklüğü", 50, 500, 200)
    generations = st.slider("Nesil Sayısı", 100, 2000, 1000)
    max_risk = st.slider("Maksimum Toplam Risk", 0.5, 3.0, 1.5, step=0.1)
    
with st.form("hesapla_form"):
    submitted = st.form_submit_button("🚀 Optimizasyonu Başlat")
    if submitted:
        with st.spinner("⛽ İkmal aracı yolda, rota optimize ediliyor..."):
            route, dist, time, risk, log = run_ga(pop_size, generations, max_risk)
            if route:
                st.session_state["route"] = route
                st.session_state["dist"] = dist
                st.session_state["time"] = time
                st.session_state["risk"] = risk
                st.session_state["log"] = log
                st.success("✅ Rota başarıyla oluşturuldu!")
            else:
                st.error("❌ Rota bulunamadı.")


if hesapla:
    route, dist, time, risk, log = run_ga(pop_size, generations, max_risk)
    if route:
        st.session_state["route"] = route
        st.session_state["dist"] = dist
        st.session_state["time"] = time
        st.session_state["risk"] = risk
        st.session_state["log"] = log
        st.success("✅ Rota başarıyla oluşturuldu!")
    else:
        st.error("❌ Rota bulunamadı.")

with tabs[2]:
    st.header("📈 Sonuçlar")
    if "route" in st.session_state:
        city_names = [cities[i] for i in st.session_state["route"]]
        st.write("**Rota:**", " → ".join(city_names))
        st.write("📏 Mesafe:", round(st.session_state["dist"], 2), "km")
        st.write("⏱ Süre:", round(st.session_state["time"], 1), "dk")
        st.write("☢️ Risk:", round(st.session_state["risk"], 3))
        if st.button("💾 Senaryoyu Kaydet"):
            scenario = {
                "name": senaryo_adi,
                "route": st.session_state["route"],
                "dist": st.session_state["dist"],
                "time": st.session_state["time"],
                "risk": st.session_state["risk"]
            }
            with open(f"{SCENARIO_DIR}/{senaryo_adi}.json", "w") as f:
                json.dump(scenario, f)
            st.success(f"✅ {senaryo_adi} kaydedildi.")
    else:
        st.info("Henüz bir senaryo hesaplanmadı.")

with tabs[3]:
    st.header("🗺️ Harita")
    if "route" in st.session_state:
        route_names = [cities[i] for i in st.session_state["route"]]
        folium_map = plot_folium_route(route_names)
        if folium_map:
            st_folium(folium_map, use_container_width=True)
    else:
        st.warning("Rota bulunamadı.")

with tabs[4]:
    st.header("⛽ Bekleme Animasyonu")
    st.markdown("🚧 Bu bölüm isteğe bağlı olarak entegre edilecek...")

with tabs[5]:
    st.header("🌱 Emisyon ve Enerji")
    if "dist" in st.session_state:
        co2 = round(st.session_state["dist"] * 0.2, 2)
        energy = round(st.session_state["dist"] * 0.25, 2)
        st.metric("🌍 CO₂ Emisyonu", f"{co2} kg")
        st.metric("⚡ Enerji Tüketimi", f"{energy} kWh")
    else:
        st.info("Henüz rota oluşturulmadı.")

with tabs[6]:
    st.header("🕒 Gantt Şeması")
    if "log" in st.session_state:
        fig = plot_gantt(st.session_state["log"])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Zaman çizelgesi yok.")

with tabs[7]:
    st.header("📊 Parametre Analizi")
    st.markdown("📈 Bu bölümde gelecekteki varyasyon analizleri yer alacak...")

with tabs[8]:
    st.header("📂 Senaryo Karşılaştırma")
    files = [f for f in os.listdir(SCENARIO_DIR) if f.endswith(".json")]
    selected = st.multiselect("📁 Karşılaştırmak için senaryoları seçin:", files, default=files[:2] if len(files) >= 2 else files)
    if selected:
        loaded = []
        for fname in selected:
            with open(os.path.join(SCENARIO_DIR, fname)) as f:
                data = json.load(f)
                data["name"] = fname.replace(".json", "")
                loaded.append(data)
        st.subheader("📊 Risk / Mesafe / Süre")
        st.plotly_chart(plot_scenario_comparison(loaded), use_container_width=True)
        st.subheader("🌱 Emisyon & Enerji")
        st.plotly_chart(plot_emission_energy_comparison(loaded), use_container_width=True)
    else:
        st.info("En az 1 senaryo seçin.")
