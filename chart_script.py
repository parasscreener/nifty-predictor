import plotly.graph_objects as go
import pandas as pd

# Create the data for the flowchart components
components_data = [
    {
        "component": "Data Sources",
        "type": "data", 
        "items": ["Yahoo Finance API", "yfinance Library", "Real-time NIFTY 50", "OHLCV Data", "Market Status"],
        "color": "#3498db",
        "icon": "📊",
        "x": 1, "y": 6
    },
    {
        "component": "GitHub Repository",
        "type": "storage",
        "items": ["Source Code", "ML Models", "Templates", "Workflows", "Configuration"], 
        "color": "#2c3e50",
        "icon": "📁",
        "x": 1, "y": 4
    },
    {
        "component": "GitHub Actions Pipeline",
        "type": "automation",
        "items": ["Daily Trigger (9:30 AM IST)", "Data Collection", "Model Predictions", "Chart Generation", "Page Deployment"],
        "color": "#f39c12", 
        "icon": "⚙️",
        "x": 3, "y": 5
    },
    {
        "component": "ML Processing",
        "type": "processing",
        "items": ["RNN Predictions", "LSTM Predictions", "CNN Predictions", "Performance Metrics", "Recommendations"],
        "color": "#27ae60",
        "icon": "🤖", 
        "x": 5, "y": 6
    },
    {
        "component": "Web Generation", 
        "type": "web",
        "items": ["Plotly Charts", "HTML Templates", "JSON APIs", "Responsive Design", "Interactive UI"],
        "color": "#e74c3c",
        "icon": "🎨",
        "x": 5, "y": 4
    },
    {
        "component": "GitHub Pages",
        "type": "hosting", 
        "items": ["Static Website", "CDN Delivery", "HTTPS Security", "Custom Domain", "Global Access"],
        "color": "#9b59b6",
        "icon": "🌐",
        "x": 7, "y": 5
    },
    {
        "component": "User Access",
        "type": "users",
        "items": ["Web Dashboard", "Mobile View", "JSON Data API", "Real-time Updates", "Investment Insights"], 
        "color": "#1abc9c",
        "icon": "👥",
        "x": 9, "y": 5
    }
]

# Create DataFrame
df = pd.DataFrame(components_data)

# Create hover text with items
df['hover_text'] = df.apply(lambda row: f"{row['icon']} {row['component']}<br>" + 
                           "<br>".join(row['items'][:3]) + 
                           (f"<br>+{len(row['items'])-3} more" if len(row['items']) > 3 else ""), axis=1)

# Create the scatter plot
fig = go.Figure()

# Add scatter points for each component
for i, row in df.iterrows():
    fig.add_trace(go.Scatter(
        x=[row['x']],
        y=[row['y']], 
        mode='markers+text',
        marker=dict(
            size=80,
            color=row['color'],
            line=dict(width=3, color='white')
        ),
        text=f"{row['icon']}<br>{row['component'][:10]}",
        textposition="middle center",
        textfont=dict(size=9, color='white', family='Arial Black'),
        hovertext=row['hover_text'],
        hoverinfo='text',
        name=row['type'].title(),
        legendgroup=row['type'],
        showlegend=True if row['type'] not in [t['type'] for t in components_data[:i]] else False
    ))

# Add flow arrows using annotations
arrows = [
    # Data Sources -> GitHub Actions
    {'x': 1.5, 'y': 5.8, 'ax': 2.5, 'ay': 5.2, 'text': ''},
    # GitHub Repo -> GitHub Actions 
    {'x': 2.5, 'y': 4.8, 'ax': 1.5, 'ay': 4.2, 'text': ''},
    # GitHub Actions -> ML Processing
    {'x': 4.5, 'y': 5.8, 'ax': 3.5, 'ay': 5.2, 'text': ''},
    # GitHub Actions -> Web Generation
    {'x': 4.5, 'y': 4.2, 'ax': 3.5, 'ay': 4.8, 'text': ''},
    # ML Processing -> GitHub Pages
    {'x': 6.5, 'y': 5.8, 'ax': 5.5, 'ay': 5.2, 'text': ''},
    # Web Generation -> GitHub Pages
    {'x': 6.5, 'y': 4.2, 'ax': 5.5, 'ay': 4.8, 'text': ''},
    # GitHub Pages -> User Access
    {'x': 8.5, 'y': 5, 'ax': 7.5, 'ay': 5, 'text': ''}
]

# Add arrows as annotations
for arrow in arrows:
    fig.add_annotation(
        x=arrow['x'], y=arrow['y'],
        ax=arrow['ax'], ay=arrow['ay'],
        xref='x', yref='y',
        axref='x', ayref='y',
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#34495e",
        showarrow=True,
        text=arrow['text']
    )

# Update layout
fig.update_layout(
    title="NIFTY 50 Prediction Dashboard",
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 10]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[3, 7]),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(
        orientation='h',
        yanchor='bottom', 
        y=1.05,
        xanchor='center',
        x=0.5
    ),
    hovermode='closest'
)

# Update traces to disable clipping
fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image("nifty_architecture_flowchart.png")
fig.show()