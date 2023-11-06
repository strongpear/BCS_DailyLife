import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np


# Load data
df = pd.read_csv(open('dataFinished.csv', 'rb'))
df['Stress Rating'] = [str(i) for i in df['Stress Rating']]

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

    html.H3('Select the desired Subject, or All for all subjects.'),
    html.Span([html.P('Subject:', style={"margin-right":"10px"}),
                dcc.Dropdown(id='select_year',
                    options=[
                        {"label": "Subject " + str(i), "value": 'S' + str(i)} for i in np.sort([int(j[1:]) for j in df['Subject Number'].unique()])] + 
                        [{"label": "All", "value": "All"}],       # Change format from S1 to 1 (as an integer)
                        multi=False,
                        value="All",
                        style={'width': "200px", "margin-right": "10px"}
                ),
                html.P('Minimum Temperature (F)', style={"margin-right":"10px"}),
                dcc.Input(id='tempMin',
                        type='number',
                        value='',
                        style={'width': "75px", "margin-right":"10px"}
                        ),
                html.P('Maximum Temperature (F)', style={"margin-right": "10px"}),
                dcc.Input(id='tempMax',
                        type='number',
                        value='',
                        style={'width': "75px"}
                        )
            ], style=dict(display='flex')),
    html.Br(),
    dcc.Graph(id='map', figure={}),
])


# Callback
@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='select_year', component_property='value'),
     Input(component_id='tempMin', component_property='value'),
     Input(component_id='tempMax', component_property='value')]
)
def load_graph(subjectNumber, tempMin, tempMax):
    print(subjectNumber)
    dff = df.copy()
    if subjectNumber != "All":
        dff = dff[dff["Subject Number"] == subjectNumber]
    if tempMin != '':
        dff = dff[dff["Temperature (F)"] >= int(tempMin)]
    if tempMax != '':
        dff = dff[dff["Temperature (F)"] <= int(tempMax)]
    
    dff = dff.sort_values(by=['Stress Rating'])
    figure = px.scatter_mapbox(dff,
                        lat="X Coordinate",
                        lon="Y Coordinate",
                        hover_data=["Stress Rating", "Temperature (F)", "Element", "Subject Number"],
                        color='Stress Rating',
                        color_discrete_map={'1.0':'green', '2.0':'orange', '3.0':'yellow', '4.0':'purple', '5.0':'red', 'nan':'black'},
                        zoom=8,
                        height=800,
                        width=800,
                        )
    figure.update_layout(mapbox_style="open-street-map")
    figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return figure

# Run server
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)