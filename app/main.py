import os.path

from flask import Flask, render_template
import pandas as pd
import folium

app = Flask(__name__)

url = 'https://raw.githubusercontent.com/debora28/pi-2020.2/main/2014-1-10mil.csv'


def main():
    data = pd.read_csv(url)

    x = data['LATITUDE'].mode()
    data['LATITUDE'].fillna('-23.71286115', inplace=True)

    data['LONGITUDE'].fillna('-46.78186771', inplace=True)

    anti_lat = data['LATITUDE']
    anti_lon = data['LONGITUDE']

    def new_array(collunm_cvs):
        def replace_location(string):
            string = (string.replace('.', ''))
            string = '{0}{1}{2}'.format(string[0:3], '.', string[3:])
            return string

        newArray = []
        for x in collunm_cvs:
            newArray.append(replace_location(x))

        DF = pd.DataFrame(newArray)
        DF.to_csv("data1.csv")
        return (DF)

    nova_lat = new_array(anti_lat)
    nova_lon = new_array(anti_lon)

    data['nova_latitude'] = ""
    data['nova_longitude'] = ""

    data['nova_latitude'] = data['nova_latitude'] + nova_lat
    data['nova_longitude'] = data['nova_longitude'] + nova_lon

    from folium import plugins
    coordenadas = []
    lat = data['nova_latitude'][:10000].values
    long = data['nova_longitude'][:10000].values

    mapa = folium.Map(location=[-23.542183, -46.640599], tiles='Stamen Toner', zoom_start=12)

    for la, lo in zip(lat, long):
        coordenadas.append([la, lo])

    mapa.add_child(plugins.HeatMap(coordenadas))
    mapa
    save_path = 'app/templates'
    file_name = 'image.html'
    complete_name = os.path.join(save_path, file_name)
    mapa.save(complete_name)


@app.route("/")
def hello():
    return url

@app.route("/update")
def update():
    main()
    return "<h1>Update Success </h1>"

@app.route("/mapa")
def mapa():
    return render_template('image.html')
