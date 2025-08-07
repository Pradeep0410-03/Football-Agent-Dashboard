# app.py - FINAL Polished Version with ALL Features
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import re
import sqlite3

# --- 1. Load Data from SQLite Database ---
try:
    conn = sqlite3.connect('transfers.db')
    df = pd.read_sql_query("SELECT * FROM transfers", conn)
    conn.close()
    print("✅ Data loaded successfully from the database!")
except Exception as e:
    print(f"❌ ERROR: Could not read from the database. Error: {e}")
    exit()

# --- 2. Data Cleaning and Preparation ---
def clean_fee(fee):
    if not isinstance(fee, str): return 0.0
    fee_lower = fee.lower().replace('€', '')
    numeric_part = re.search(r'(\d+\.?\d*)', fee_lower)
    if not numeric_part: return 0.0
    value = float(numeric_part.group(1))
    if 'm' in fee_lower: return value
    elif 'k' in fee_lower: return value / 1000
    return value / 1_000_000

df['fee_numeric_m'] = df['fee'].apply(clean_fee)

# --- 3. Prepare Data for Dashboard Components ---

# Key Numbers data
arrivals = df[df['type'] == 'Arrival']
departures = df[df['type'] == 'Departure']
total_spending = arrivals['fee_numeric_m'].sum()
total_income = departures['fee_numeric_m'].sum()
net_spend = total_income - total_spending

# Top 5 Transfers Table data
top_5_transfers = arrivals.sort_values(by='fee_numeric_m', ascending=False).head(5)
top_5_table = dbc.Table.from_dataframe(
    top_5_transfers[['player', 'from_club', 'fee']], 
    striped=True, bordered=True, hover=True, color="dark"
)

# Pie Chart data
type_counts = df['type'].value_counts().reset_index()
type_counts.columns = ['type', 'count']
fig_pie = px.pie(type_counts, names='type', values='count', 
                 title='Arrivals vs. Departures', hole=0.4,
                 color_discrete_sequence=['#7DFB7D', '#F66D3A'])
fig_pie.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

# Top 10 Agents Chart Data (with polishing/filtering)
AGENTS_TO_IGNORE = ['Not Found', 'Relatives', 'Without Club', 'Request Error', 'No URL']
agent_df = df[~df['agent_name'].str.contains('Scrape Failed', na=False)]
agent_df = agent_df[~agent_df['agent_name'].isin(AGENTS_TO_IGNORE)]
agent_deals = agent_df.groupby('agent_name')['fee_numeric_m'].sum().reset_index()
top_10_agents = agent_deals.sort_values(by='fee_numeric_m', ascending=False).head(10)

fig_agent_bar = px.bar(top_10_agents, x='agent_name', y='fee_numeric_m', 
                 title='Top 10 Agents by Total Deal Value (€M)', labels={'agent_name': 'Agent', 'fee_numeric_m': 'Total Value in Million €'},
                 color='agent_name', template='plotly_dark', text_auto='.2s')
fig_agent_bar.update_layout(plot_bgcolor='#1E1E1E', paper_bgcolor='#1E1E1E')


# Network Graph Data
G = nx.Graph()
for _, row in df.head(30).iterrows():
    G.add_node(row['player'], type='Player', color='skyblue')
    G.add_node(row['from_club'], type='Club', color='#F66D3A')
    G.add_node(row['to_club'], type='Club', color='#7DFB7D')
    G.add_edge(row['from_club'], row['player'])
    G.add_edge(row['player'], row['to_club'])

pos = nx.spring_layout(G, k=0.9, iterations=50)
edge_trace = go.Scatter(x=[], y=[], line=dict(width=0.7, color='#505050'), hoverinfo='none', mode='lines')
for edge in G.edges():
    edge_trace['x'] += tuple([pos[edge[0]][0], pos[edge[1]][0], None])
    edge_trace['y'] += tuple([pos[edge[0]][1], pos[edge[1]][1], None])
node_trace = go.Scatter(x=[], y=[], mode='markers', text=[], hoverinfo='text',
                        marker=dict(showscale=False, color=[], size=15, line_width=2))
for node in G.nodes():
    node_trace['x'] += tuple([pos[node][0]])
    node_trace['y'] += tuple([pos[node][1]])
    node_trace['marker']['color'] += tuple([G.nodes[node]['color']])
    node_trace['text'] += tuple([f"{G.nodes[node]['type']}: {node}"])

fig_network = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
    title=dict(text='Transfer Network (Sample of 30 Players)', font=dict(size=20)),
    showlegend=False, hovermode='closest', margin=dict(b=20,l=5,r=5,t=40),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor='#111111', paper_bgcolor='#111111', font_color='white'))

# --- 4. Initialize and Layout the App ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

def create_info_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H4(title, className="card-title text-center"),
            html.H2(f"€{value:.2f}M", className=f"card-text text-center text-{color}")
        ]),
    )

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Football Agent Influence Dashboard", className="text-center text-success p-4"))),
    
    dbc.Row([
        dbc.Col(create_info_card("Total Spending", total_spending, "danger"), width=4),
        dbc.Col(create_info_card("Total Income", total_income, "success"), width=4),
        dbc.Col(create_info_card("Net Spend", net_spend, "info"), width=4),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.H4("Top 10 Agents", className="text-center"),
            dcc.Graph(figure=fig_agent_bar),
            html.H4("Activity Type", className="text-center mt-4"),
            dcc.Graph(figure=fig_pie),
        ], width=12, lg=5),
        dbc.Col([
            html.H4("Top 5 Biggest Transfers", className="text-center"),
            top_5_table,
            html.H4("Transfer Network", className="text-center mt-4"),
            dcc.Graph(figure=fig_network, style={'height': '60vh'})
        ], width=12, lg=7),
    ], className="mt-4"),

    dbc.Row(dbc.Col(html.H3("All Scraped Transfer Records", className="text-center text-info mt-5 p-2"))),

    dbc.Row(dbc.Col(
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i.replace("_", " ").title(), 'id': i} for i in df.columns],
            page_size=10,
            style_as_list_view=True,
            style_header={'backgroundColor': '#1f2630', 'fontWeight': 'bold'},
            style_cell={'padding': '10px', 'backgroundColor': '#303640', 'color': 'white'},
            sort_action="native",
            filter_action="native",
        ), width=12
    ))
], fluid=True)

# --- 5. Run the App ---
if __name__ == '__main__':
    app.run(debug=True)