import folium

# 定义主要途经点的近似经纬度
locations = {
    "基督城 (Christchurch)": [-43.532, 172.636],
    "凯库拉 (Kaikoura)": [-42.400, 173.680],
    "阿卡罗阿 (Akaroa)": [-43.803, 172.968],
    "蒂卡波 (Tekapo)": [-44.004, 170.477],
    "特威泽尔 (Twizel)": [-44.256, 170.100],
    "库克山 (Mt Cook)": [-43.733, 170.096],
    "瓦纳卡 (Wanaka)": [-44.694, 169.141],
    "克伦威尔 (Cromwell)": [-45.038, 169.198],
    "箭镇 (Arrowtown)": [-44.942, 168.829],
    "皇后镇 (Queenstown)": [-45.031, 168.662],
    "格林诺奇 (Glenorchy)": [-44.850, 168.383],
    "但尼丁 (Dunedin)": [-45.878, 170.502],
    "摩拉基/卡蒂奇 (Moeraki/Katiki)": [-45.361, 170.849],
    "奥马鲁 (Oamaru)": [-45.097, 170.969]
}

# 提取三个方案的路线轨迹
route1_nodes = ["基督城 (Christchurch)", "凯库拉 (Kaikoura)", "基督城 (Christchurch)", "蒂卡波 (Tekapo)", "库克山 (Mt Cook)", "瓦纳卡 (Wanaka)", "克伦威尔 (Cromwell)", "皇后镇 (Queenstown)", "格林诺奇 (Glenorchy)", "皇后镇 (Queenstown)", "但尼丁 (Dunedin)", "奥马鲁 (Oamaru)", "基督城 (Christchurch)"]
route2_nodes = ["基督城 (Christchurch)", "阿卡罗阿 (Akaroa)", "蒂卡波 (Tekapo)", "库克山 (Mt Cook)", "蒂卡波 (Tekapo)", "瓦纳卡 (Wanaka)", "箭镇 (Arrowtown)", "皇后镇 (Queenstown)", "克伦威尔 (Cromwell)", "但尼丁 (Dunedin)", "奥马鲁 (Oamaru)", "凯库拉 (Kaikoura)", "基督城 (Christchurch)"]
route3_nodes = ["基督城 (Christchurch)", "特威泽尔 (Twizel)", "库克山 (Mt Cook)", "特威泽尔 (Twizel)", "瓦纳卡 (Wanaka)", "箭镇 (Arrowtown)", "皇后镇 (Queenstown)", "摩拉基/卡蒂奇 (Moeraki/Katiki)", "奥马鲁 (Oamaru)", "基督城 (Christchurch)"]

# 初始化地图，中心点设在南岛中部
m = folium.Map(location=[-44.0, 170.5], zoom_start=7, tiles="CartoDB positron")

# 标注所有城市节点
for name, coords in locations.items():
    folium.CircleMarker(
        location=coords, radius=5, color="black", fill=True, fill_color="white", fill_opacity=1
    ).add_to(m)
    folium.Marker(
        location=coords, icon=folium.DivIcon(html=f'<div style="font-size: 10pt; font-weight: bold; width: 120px; color: black; text-shadow: 1px 1px 2px white;">{name}</div>')
    ).add_to(m)

# 绘制路线（设置不同颜色和偏移量避免重叠）
folium.PolyLine(locations=[locations[n] for n in route1_nodes], color="red", weight=4, opacity=0.7, tooltip="方案一：赏秋专线").add_to(m)
folium.PolyLine(locations=[locations[n] for n in route2_nodes], color="blue", weight=4, opacity=0.7, tooltip="方案二：经典小环线", dash_array="5, 5").add_to(m)
folium.PolyLine(locations=[locations[n] for n in route3_nodes], color="green", weight=5, opacity=0.9, tooltip="方案三：南岛秘境(推荐)").add_to(m)

# 保存为HTML，可以直接在浏览器打开并截图
m.save("nz_south_island_routes.html")
print("地图已生成：nz_south_island_routes.html，请在浏览器中打开查看。")