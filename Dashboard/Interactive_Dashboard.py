# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id = 'site-dropdown',
                                            options = [
                                                {'label': 'All Sites', 'value': 'All Sites'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                ],
                                            value='ALL',
                                            placeholder="Launch Sites",
                                            searchable=True    
                                      
                                            ),



                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                 dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                marks={0:'0 Kg', 1000:'1000 Kg', 2000:'2000 Kg', 3000:'3000 Kg', 4000:'4000 Kg',5000:'5000 Kg', 6000:'6000 Kg',7000:'7000 Kg',8000:'8000 Kg',9000:'9000 Kg',10000:'10000 Kg'},
                                                value = [0, 5000]                                             
                                                ),
                                html.Div(id='slider-output-container'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def pie(site_dropdown):
    if site_dropdown == 'All Sites':
        title_pie = f"Success Launches for site {site_dropdown}"       
        fig = px.pie(spacex_df, values='class', names='Launch Site', title=title_pie)
        return fig
    else:
        filtered_df= spacex_df[spacex_df['Launch Site'] == site_dropdown]
        filtered_LS = filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        title_pie = f"Success Launches for site {site_dropdown}"  
        fig = px.pie(filtered_LS, values='class count', names='class',title=title_pie)
        return fig
   
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
            )
def get_scatter_chart(site_dropdown, payload_slider):
    Booster_Version = []
    
    for index, row in spacex_df.iterrows():
        x = row['Booster Version'].split()[1]
        Booster_Version.append(x)
        
    spacex_df['Booster_Version'] = Booster_Version
    
    if site_dropdown == 'All Sites':
        fig1 = px.scatter(spacex_df[(spacex_df['Payload Mass (kg)'] > min(payload_slider)) & (spacex_df['Payload Mass (kg)'] < max(payload_slider))], 
                        x="Payload Mass (kg)", y="class", 
                        color='Booster_Version',
                        size="Payload Mass (kg)"
                        )
        return fig1
    else:
        fig1 = px.scatter(spacex_df[(spacex_df['Payload Mass (kg)'] > min(payload_slider)) & (spacex_df['Payload Mass (kg)'] < max(payload_slider)) & (spacex_df['Launch Site'] == site_dropdown)], 
                        x="Payload Mass (kg)", y="class", 
                        color='Booster_Version',
                        size="Payload Mass (kg)"
                        )
        return fig1  

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('payload-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


# Run the app
if __name__ == '__main__':
    app.run_server()
