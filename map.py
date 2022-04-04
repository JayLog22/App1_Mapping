import folium
import pandas

def get_elevation_color(elevation):
    if elevation < 1500:
        return 'green'
    elif 1500 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

data = pandas.read_csv("Volcanoes.txt")

latitudes = list(data["LAT"])
longitudes = list(data["LON"])
elevation = list(data["ELEV"])

starting_location = [39, -99]

html = """<h4>Volcano information:</h4>
Height: %s m
"""

map = folium.Map(location = starting_location, zoom_start = 6, tiles = "Stamen Terrain")
feature_group_volcanoes = folium.FeatureGroup("Volcanoes")

for lat, lon, elev in zip(latitudes, longitudes, elevation):
    iframe = folium.IFrame(html=html % str(elev), width=200, height=100)
    #elev_string = "Elevation: " + str(elev) + "m"
    feature_group_volcanoes.add_child(folium.CircleMarker(location = [lat, lon], radius = 8,popup = folium.Popup(iframe), fill_color=get_elevation_color(elev), color = 'grey', fill=True, fill_opacity=1))

feature_group_population = folium.FeatureGroup("Population")

feature_group_population.add_child(folium.GeoJson(data=open('world.json', 'r',encoding='utf-8-sig').read(),
                                        style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
                                        else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                        else 'red'}))


map.add_child(feature_group_volcanoes)
map.add_child(feature_group_population)
map.add_child(folium.LayerControl())
map.save("Map.html")