# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # dcc.Dropdown(id='site-dropdown',...)
                                # The default select value is for ALL sites
                                html.Div(dcc.Dropdown(id="site-dropdown", 
                                                      options=[
                                                          {"label": "All Sites", "value": "ALL"},
                                                          {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                                                          {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
                                                          {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                                                          {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
                                                      ],
                                                      value="ALL",
                                                      placeholder="Select a Launch Site here")),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                html.Div(dcc.Graph(id="success-pie-chart")),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                html.Div(dcc.RangeSlider(id="payload-slider", min=0, max=10000, step=1000,
                                                         marks={0:"0", 1000: "100", 2000: "2000", 3000: "3000",4000: "4000",
                                                                5000: "5000", 6000: "6000", 7000: "7000", 8000: "8000", 9000: "9000",
                                                                10000: "10000"},
                                                         value=[min_payload, max_payload])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value")
)
def update_pie(input_site_dropdown):
    if input_site_dropdown == "ALL":
        df = spacex_df[spacex_df["class"] == 1]
        pie_chart = px.pie(df, values ="class", names="Launch Site")

    else:
        df = spacex_df[spacex_df["Launch Site"] == input_site_dropdown]
        label=["Success", "Failed"]
        counts = df["class"].value_counts()
        value = [counts.get(1,0), counts.get(0,0)]
        pie_chart = px.pie(df, values = value, names = label)

    return pie_chart

    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [Input(component_id="site-dropdown", component_property="value"), Input(component_id="payload-slider", component_property="value")]
)

def update_scatter(input_dropdown, input_slider):
    df_new = spacex_df[spacex_df["Payload Mass (kg)"] <= input_slider[1]]
    df = df_new[df_new["Payload Mass (kg)"] >= input_slider[0]]
    if input_dropdown == "ALL":
        scatter_chart = px.scatter(df, x="Payload Mass (kg)", y = "class", color="Launch Site", labels=("Payload", "Launch Outcome"))
    
    else:
        df = df[df["Launch Site"] == input_dropdown]
        scatter_chart = px.scatter(df, x="Payload Mass (kg)", y= "class")

    scatter_chart.update_layout(xaxis_title="Payload Mass (kg)", yaxis_title="Outcome")
    return scatter_chart
    
    
# Run the app
if __name__ == '__main__':
    app.run_server()
