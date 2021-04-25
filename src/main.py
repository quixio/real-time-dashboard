# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:80/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import requests
import io
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import signalrcore
from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
from signalrcore.hub_connection_builder import HubConnectionBuilder
from dash.dependencies import Input, Output, State
import plotly

streamId = ""
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qVTBRVE01TmtJNVJqSTNOVEpFUlVSRFF6WXdRVFF4TjBSRk56SkNNekpFUWpBNFFqazBSUSJ9.eyJodHRwczovL3F1aXguYWkvb3JnX2lkIjoicXVpeCIsImh0dHBzOi8vcXVpeC5haS9vd25lcl9pZCI6ImF1dGgwfGI3YjI1ZGJkLWRjN2QtNGFkZC05MmQ4LTM4OTI0Mjc3NTJiNyIsImh0dHBzOi8vcXVpeC5haS90b2tlbl9pZCI6ImY2ZmY5NzY2LTE0ODctNDU1OC04ZWU4LWQ3NDFlYmRhMzFmMCIsImh0dHBzOi8vcXVpeC5haS9leHAiOiIxNjE5NzEyMDAwIiwiaHR0cHM6Ly9xdWl4LmFpL3JvbGVzIjoiYWRtaW4iLCJpc3MiOiJodHRwczovL2xvZ2ljYWwtcGxhdGZvcm0uZXUuYXV0aDAuY29tLyIsInN1YiI6InFyY2F2RmJMNkw4bXJ0b1JjMFZucXFhR2lxWXM5VENLQGNsaWVudHMiLCJhdWQiOiJxdWl4IiwiaWF0IjoxNjE5MzA4MjM0LCJleHAiOjE2MjE5MDAyMzQsImF6cCI6InFyY2F2RmJMNkw4bXJ0b1JjMFZucXFhR2lxWXM5VENLIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOltdfQ.GgBQPuOJOB9HO4syqIkCUudCPkAUHWjJfB-PEvaga8YiZevBQf3N1-YlnFy-rPvQ6ANIxbMWI8k2qCoPOb9hbxKWSe9CenxBiQJJV338bmWW2AEfhuQPCvoT8J8yHfTatoTX_Y-jkJ0jVPKaHyNrgYUQyxYnWxI9EftFRHZiGknt4WJes51rfThuJVHnwf09lHWGoQkY37Fb_tqBVUubnq8lavIMSRMrJN-buI7wwfv_Yz5E-iM4UoLJsPYhkdgkvmv_uYpwfddYogvt0vk4F02Mq5LLI3o6f1kQwts9rADxMhe2ryAbhK03Eb9yY5kX8pRntQPWPE7qtgPQbHymWA"
server_url = "wss://reader-quix-gamedemo.platform.quix.ai/hub"

hub_connection = HubConnectionBuilder()\
    .with_url(server_url, options={"access_token_factory": lambda : token,  })\
    .build()

hub_connection.on_open(print("Connection opened."))
hub_connection.on_close(lambda: on_close_handler())

def on_close_handler():
    print("Connection closed.")
    if streamId:
        print("Reconnecting...")
        hub_connection.start()
        print("Connection restarted.")
        print("Subscribing to stream: {}".format(streamId))
        hub_connection.send("SubscribeToParameter", ["codemasters", value, "Speed"])
        print("Subscribed to stream: {}".format(streamId))


speed = []
timestamps = []
def on_data(payload):
    for data in payload:
        for row in range(len(data['numericValues']['Speed'])):
            timestamps.append(str(datetime.datetime.fromtimestamp(data['timestamps'][row] / 1000000000)))
            speed.append(data['numericValues']['Speed'][row])

hub_connection.on("ParameterDataReceived", on_data)
hub_connection.start()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# We add secondary y axe to accommodate second parameter.
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add series into plot for speed.
fig.add_trace(
    go.Scatter(x=[], y=[], name="Speed", ),
    secondary_y=False,
)

fig.update_yaxes(range=[0,400])


@app.callback(Output('example-graph', 'extendData'), [Input('interval', 'n_intervals')])
def update_data(n_intervals):
    global speed
    global timestamps

    res = dict(x=[timestamps], y=[speed])

    speed = []
    timestamps = []
    return res


app.layout = html.Div(children=[
    html.H1(children='Hello from Quix'),
    dcc.Input(
            id="input",
            type="text"
    ),
    html.Div(children='''
        Example dashboard with Dash and Quix.
    '''),

    dcc.Graph(
        animate = True,
        id='example-graph',
        figure=fig
    ),
    dcc.Interval(id="interval", interval=1000),

    html.Div(id="out-all-types")
])

@app.callback(
    Output("out-all-types", "children"),
    [Input("input", "value")]
)
def cb_render(value):
    global streamId
    streamId = value
    hub_connection.send("SubscribeToParameter", ["codemasters", value, "Speed"])


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=80)
