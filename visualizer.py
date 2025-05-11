
import plotly.figure_factory as ff
import plotly.graph_objects as go
import folium

def plot_gantt(log):
    tasks = []
    for i, entry in enumerate(log):
        start = entry["arrival"]
        end = entry["departure"]
        tasks.append(dict(Task=f"{entry['from']}→{entry['to']}", Start=start, Finish=end))
    fig = ff.create_gantt(tasks, index_col='Task', show_colorbar=True, group_tasks=True)
    return fig

def plot_folium_route(city_names):
    m = folium.Map(location=[41.015137, 28.979530], zoom_start=11)
    folium.Marker(location=[41.015137, 28.979530], tooltip="Rafineri", icon=folium.Icon(color="green")).add_to(m)
    for i, name in enumerate(city_names):
        folium.CircleMarker(location=[41 + i*0.01, 28.98 + i*0.01], radius=5, popup=name, color="blue").add_to(m)
    folium.PolyLine([(41 + i*0.01, 28.98 + i*0.01) for i in range(len(city_names))], color="red").add_to(m)
    return m

def plot_scenario_comparison(data):
    fig = go.Figure()
    names = [d['name'] for d in data]
    fig.add_trace(go.Bar(name="Mesafe", x=names, y=[d['dist'] for d in data]))
    fig.add_trace(go.Bar(name="Süre", x=names, y=[d['time'] for d in data]))
    fig.add_trace(go.Bar(name="Risk", x=names, y=[d['risk'] for d in data]))
    fig.add_trace(go.Bar(name="Hız", x=names, y=[d.get('avg_speed', 0) for d in data]))
    fig.update_layout(barmode='group')
    return fig

def plot_emission_energy_comparison(data):
    fig = go.Figure()
    names = [d['name'] for d in data]
    emissions = [round(d['dist'] * 0.2, 2) for d in data]
    energy = [round(d['dist'] * 0.25, 2) for d in data]
    fig.add_trace(go.Bar(name="CO₂ (kg)", x=names, y=emissions))
    fig.add_trace(go.Bar(name="Enerji (kWh)", x=names, y=energy))
    fig.update_layout(barmode='group')
    return fig
