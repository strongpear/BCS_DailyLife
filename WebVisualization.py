import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np


# Load data
df = pd.read_csv(open('dataFinished.csv', 'rb'))
df['Stress Rating'] = [str(i) for i in df['Stress Rating']]
stimuliCounts = pd.read_csv(open('stimuliCounts.csv', 'rb'))
stimDict = {row['Stimuli']: row['Count'] for index, row in stimuliCounts.iterrows()}
# Test Figure
# fig = px.scatter_mapbox(df,
#                         lat="X Coordinate",
#                         lon="Y Coordinate",
#                         hover_data=["Stress Rating", "Temperature (F)", "Element"],
#                         color='Stress Rating',
#                         zoom=8,
#                         height=800,
#                         width=800)
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# Initialize app
app = Dash(__name__)

server = app.server

# Html of App
app.layout = html.Div([
    html.H1('Stress in the Bryan-College Station Area', style={'text-align': 'center'}),

    html.H3('The following four options are filters that will alter all of the visualizations.'),
    html.Span([html.P('Subject:', style={"margin-right":"10px"}),
                dcc.Dropdown(id='select_participant',
                    options=[{"label": "All", "value": "All"}]+ 
                        [{"label": "Subject " + str(i), "value": 'S' + str(i)} for i in np.sort([int(j[1:]) for j in df['Subject Number'].unique()])],       # Change format from S1 to 1 (as an integer)
                        multi=False,
                        value="All",
                        style={'width': "200px", "margin-right": "10px"}
                ),
                html.P('Stimuli Element', style={"margin-right": "10px"}),
                dcc.Dropdown(id='select_stressor',
                    options= [{"label": "All", "value": "All"}] +
                        [{"label": str(key), "value": str(key)} for key in stimuliCounts['Stimuli'][:10]],       # Change format from S1 to 1 (as an integer)
                        multi=False,
                        value="All",
                        style={'width': "200px", "margin-right": "10px"}
                )
            ], style=dict(display='flex')),
    html.Span([html.P('Minimum Temperature (F)', style={"margin-right":"10px"}),
                dcc.Input(id='tempMin',
                        type='number',
                        value='',
                        style={'width': "75px", "margin-right":"10px", "height": "30px"}
                        ),
                html.P('Maximum Temperature (F)', style={"margin-right": "10px"}),
                dcc.Input(id='tempMax',
                        type='number',
                        value='',
                        style={'width': "75px", "margin-right": "10px", "height": "30px"},
                        ),
            ], style=dict(display='flex')),
    html.H4(html.Div(id='total')),
    html.Br(),
    dcc.Graph(id='map', figure={}),
    dcc.Graph(id='scatterplot', figure={}),
    dcc.Graph(id='hist', figure={}),
    dcc.Graph(id='ratings', figure={})
])


# Callback
@app.callback(
    [Output(component_id='map', component_property='figure'),
     Output(component_id='scatterplot', component_property='figure'),
     Output(component_id='hist', component_property='figure'),
     Output(component_id='ratings', component_property='figure'),
     Output(component_id='total', component_property='children')],
    [Input(component_id='select_participant', component_property='value'),
     Input(component_id='tempMin', component_property='value'),
     Input(component_id='tempMax', component_property='value'),
     Input(component_id='select_stressor', component_property='value')]
)
def load_graph(subjectNumber, tempMin, tempMax, stressor):
    dff = df.copy()
    if subjectNumber != "All":
        dff = dff[dff["Subject Number"] == subjectNumber]
    if tempMin != '':
        dff = dff[dff["Temperature (F)"] >= int(tempMin)]
    if tempMax != '':
        dff = dff[dff["Temperature (F)"] <= int(tempMax)]
    if stressor != "All":
        dff = dff[dff["Element"].str.contains(stressor)]
    
    dff = dff.sort_values(by=['Stress Rating'])
    figure = px.scatter_mapbox(dff,
                        lat="X Coordinate",
                        lon="Y Coordinate",
                        hover_data=["Stress Rating", "Temperature (F)", "Element", "Subject Number"],
                        color='Stress Rating',
                        color_discrete_map={'1.0':'green', '2.0':'orange', '3.0':'yellow', '4.0':'purple', '5.0':'red', 'nan':'black'},
                        zoom=8,
                        height=500,
                        width=1100)
    figure.update_layout(mapbox_style="open-street-map")
    figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    figure.update_layout(mapbox=dict(center=dict(lat=30.625087, lon=-96.338299), zoom=12))
    figure.update_layout(title="Dot Plot of Stress Reports in the B/CS Area")
    scatter = px.scatter(dff, x="Temperature (F)", y="Stress Rating", title="Temperature vs Stress Rating")

    hist = px.histogram(dff, x="Temperature (F)", text_auto=True, nbins=20, title="Temperature Frequency")

    bar = px.histogram(dff, x="Stress Rating", text_auto='.2s', title="Stress Rating Frequency")

    count = "Count of Stress Reports Displayed: " + str(len(dff))
    return figure, scatter, hist, bar, count

# Run server
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)