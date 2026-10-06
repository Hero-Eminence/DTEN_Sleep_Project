import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import os

# --- Load the cleaned dataset ---
# Since the CSV is in Task1_EDA, we go up one level (..) and into Task1_EDA
csv_path = os.path.join('..', 'Task1_EDA', 'sleep_cleaned.csv')

try:
    df = pd.read_csv(csv_path)
    print(f"Successfully loaded data from {csv_path}")
except FileNotFoundError:
    print(f"Error: Could not find the file at {csv_path}")
    print("Please ensure the file path is correct based on your folder structure.")
    exit()

# Map encoded sleep debt to readable labels for better visualization
debt_labels = {
    0: 'Optimal Recovery',
    1: 'Mild Deficit',
    2: 'Moderate Debt',
    3: 'Severe Sleep Debt'
}
df['sleep_debt_label'] = df['sleep_debt_encoded'].map(debt_labels)

# Define a consistent color map for sleep debt categories
color_map = {
    'Optimal Recovery': '#2ecc71',  # Green
    'Mild Deficit': '#f1c40f',      # Yellow
    'Moderate Debt': '#e67e22',     # Orange
    'Severe Sleep Debt': '#e74c3c'  # Red
}

# --- Initialize the Dash app ---
app = dash.Dash(__name__)
server = app.server
app.title = "Sleep Debt Insights Dashboard"

# --- Define the app layout ---
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'margin': '20px'}, children=[
    
    # Header
    html.H1("Sleep Debt & Lifestyle Insights Dashboard", 
            style={'textAlign': 'center', 'color': '#2c3e50'}),
    html.P("Explore how different factors influence sleep debt categories.", 
           style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': '30px'}),

    # Filters Section
    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '30px', 'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderRadius': '8px'}, children=[
        
        # Filter 1: Chronotype
        html.Div([
            html.Label("Filter by Chronotype:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='chronotype-filter',
                options=[{'label': c, 'value': c} for c in df['chronotype'].unique()],
                value=df['chronotype'].unique().tolist(),
                multi=True,
                style={'width': '250px'}
            )
        ]),
        
        # Filter 2: Occupation Type
        html.Div([
            html.Label("Filter by Occupation:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='occupation-filter',
                options=[{'label': o, 'value': o} for o in df['occupation_type'].unique()],
                value=df['occupation_type'].unique().tolist(),
                multi=True,
                style={'width': '250px'}
            )
        ])
    ]),

    # Visualizations Section
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'}, children=[
        
        # Chart 1: Distribution of Sleep Debt Categories (Pie Chart)
        html.Div([
            html.H3("Distribution of Sleep Debt Categories", style={'textAlign': 'center'}),
            dcc.Graph(id='pie-chart')
        ], style={'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)', 'padding': '15px', 'borderRadius': '8px'}),

        # Chart 2: Average Total Sleep Hours by Occupation (Bar Chart)
        html.Div([
            html.H3("Average Sleep Hours by Occupation", style={'textAlign': 'center'}),
            dcc.Graph(id='bar-chart')
        ], style={'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)', 'padding': '15px', 'borderRadius': '8px'}),

        # Chart 3: Bedtime Phone Usage vs Sleep Latency (Scatter Plot)
        html.Div([
            html.H3("Phone Usage vs. Sleep Latency", style={'textAlign': 'center'}),
            dcc.Graph(id='scatter-plot')
        ], style={'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)', 'padding': '15px', 'borderRadius': '8px', 'gridColumn': 'span 2'}),
    ])
])

# --- Define Callbacks for Interactivity ---
@app.callback(
    [Output('pie-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('scatter-plot', 'figure')],
    [Input('chronotype-filter', 'value'),
     Input('occupation-filter', 'value')]
)
def update_charts(selected_chronotypes, selected_occupations):
    # Filter the dataframe based on user selection
    if not selected_chronotypes:
        selected_chronotypes = df['chronotype'].unique()
    if not selected_occupations:
        selected_occupations = df['occupation_type'].unique()
        
    filtered_df = df[
        (df['chronotype'].isin(selected_chronotypes)) & 
        (df['occupation_type'].isin(selected_occupations))
    ]

    # --- Chart 1: Pie Chart ---
    pie_fig = px.pie(
        filtered_df, 
        names='sleep_debt_label', 
        title='Proportion of Users in Each Sleep Debt Category',
        color='sleep_debt_label',
        color_discrete_map=color_map,
        hole=0.4
    )
    pie_fig.update_traces(textposition='inside', textinfo='percent+label')

    # --- Chart 2: Bar Chart ---
    avg_sleep = filtered_df.groupby('occupation_type')['total_sleep_hours'].mean().reset_index()
    avg_sleep = avg_sleep.sort_values(by='total_sleep_hours', ascending=True)
    
    bar_fig = px.bar(
        avg_sleep,
        x='total_sleep_hours',
        y='occupation_type',
        orientation='h',
        title='Average Total Sleep Hours by Occupation Type',
        labels={'total_sleep_hours': 'Average Sleep Hours', 'occupation_type': 'Occupation'},
        color='total_sleep_hours',
        color_continuous_scale='Bluyl'
    )

    # --- Chart 3: Scatter Plot ---
    scatter_fig = px.scatter(
        filtered_df,
        x='bedtime_phone_minutes',
        y='sleep_latency_min',
        color='sleep_debt_label',
        color_discrete_map=color_map,
        title='Bedtime Phone Usage vs. Sleep Latency (Colored by Sleep Debt)',
        labels={'bedtime_phone_minutes': 'Bedtime Phone Usage (Minutes)', 
                'sleep_latency_min': 'Sleep Latency (Minutes)',
                'sleep_debt_label': 'Sleep Debt Category'},
        opacity=0.6,
        hover_data=['age', 'gender']
    )

    return pie_fig, bar_fig, scatter_fig

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=True)
