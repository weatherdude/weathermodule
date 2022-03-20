from ipyleaflet import Map, basemaps, basemap_to_tiles, Heatmap, TileLayer
from ipywidgets import AppLayout
from ipywidgets import HTML, Layout, Dropdown, Output, Textarea, VBox, Label
import bqplot as bq
import numpy as np
from pandas import date_range
from datetime import datetime
import random


OWM_API_KEY = "4fe62e7b73e91da6cadffd2bf815fd91"

m = Map(center=(52, 10), zoom=5, basemap=basemaps.Hydda.Full)

maps = {'Hydda' : basemaps.Hydda.Full,
        'Esri' : basemaps.Esri.DeLorme}

header = HTML("<h1>Fictional World Weather</h1>", layout=Layout(height='auto'))
header.style.text_align='center'
basemap_selector = Dropdown( options = list(maps.keys()),
                            layout=Layout(width='auto'))

heatmap_selector = Dropdown(options=('Temperature', 'Precipitation'),
                            layout=Layout(width='auto'))

basemap_selector.value = 'Hydda'
m.layout.height='600px'

security_1 = np.cumsum(np.random.randn(150)) + 100.

dates = date_range(start='01-01-2007', periods=150)

dt_x = bq.DateScale()
sc_y = bq.LinearScale()

time_series = bq.Lines(x=dates, y=security_1, scales={'x': dt_x, 'y': sc_y})
ax_x = bq.Axis(scale=dt_x)
ax_y = bq.Axis(scale=sc_y, orientation='vertical')

fig = bq.Figure(marks=[time_series], axes=[ax_x, ax_y],
                fig_margin=dict(top=0, bottom=80, left=30, right=20))

m.layout.width='auto'
m.layout.height='auto'
fig.layout.width='auto'
fig.layout.height='auto'

out = HTML(
    value='',
    layout=Layout(width='auto', height='auto')
)

AppLayout(center=m,
          header=header,
          left_sidebar=VBox([Label("Basemap:"),
                             basemap_selector,
                             Label("Overlay:"),
                             heatmap_selector]),
          right_sidebar=fig,
          footer=out,
          pane_widths=['80px', 1, 1],
          pane_heights=['80px', 4, 1],
          height='600px',
          grid_gap="30px")

rows = []

X, Y = np.mgrid[-90:90:10j, -180:180:20j]

X = X.flatten()
Y = Y.flatten()

temps = np.random.randn(200, 150)*0.5

def add_log(msg):
    max_rows = 3
    rows.append(msg)
    if len(rows) > max_rows:
        rows.pop(0)
    return '<h4>Activity log</h4><ul>{}</ul>'.format('<li>'.join([''] + rows))


def generate_temp_series(x, y):
    if heatmap_selector.value == 'Precipitation':
        temp = np.cumsum(np.random.randn(150)) + 100.
    elif heatmap_selector.value == 'Temperature':
        dist = np.sqrt((X - x)**2 + (Y-y)**2) / 100
        dist = dist.max() - dist
        dist[dist > np.percentile(dist, 5)] = 0
        temp = np.cumsum(np.dot(dist, temps)+0.05) + 20 - np.abs(x) / 2
    time_series.y = temp

def handle_interaction(**kwargs):
    if kwargs['type'] == 'click':
        generate_temp_series(*kwargs['coordinates'])
        msg = '%s Selected coordinates: %s, Temp: %d C Precipitation: %d mm\n' % (
            datetime.now(), kwargs['coordinates'], random.randint(-20, 20), random.randint(0, 100))
        out.value = add_log(msg)

m.on_interaction(handle_interaction)

def on_map_selected(change):
    m.layers = [basemap_to_tiles(maps[basemap_selector.value]), weather_maps[heatmap_selector.value]]

basemap_selector.observe(on_map_selected, names='value')
heatmap_selector.observe(on_map_selected, names='value')

temp = TileLayer(min_zoom=1, max_zoom=18, url='https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid='+OWM_API_KEY, name='owm', attribute='me')
precipitation = TileLayer(min_zoom=1, max_zoom=18, url='https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid='+OWM_API_KEY, name='owm', attribute='me')

weather_maps = {'Temperature' : temp,
                'Precipitation' : precipitation}

m.add_layer(weather_maps[heatmap_selector.value])
