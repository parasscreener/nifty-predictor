import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create mock historical data for NIFTY 50
dates = pd.date_range(start='2023-12-01', end='2024-01-15', freq='D')
np.random.seed(42)

# Generate realistic stock price movement
base_price = 21000
returns = np.random.normal(0.001, 0.02, len(dates))
prices = [base_price]

for ret in returns[1:]:
    prices.append(prices[-1] * (1 + ret))

historical_data = pd.DataFrame({
    'Date': dates,
    'Price': prices
})

# Current price and predictions
current_price = 21450.75
predictions = {
    'RNN': 21520,
    'LSTM': 21580, 
    'CNN': 21490
}

# Create future dates for predictions
future_dates = pd.date_range(start='2024-01-16', periods=15, freq='D')

# Create the main figure
fig = go.Figure()

# Add historical price line
fig.add_trace(go.Scatter(
    x=historical_data['Date'],
    y=historical_data['Price'],
    mode='lines',
    name='Historical',
    line=dict(color='#1FB8CD', width=3),
    hovertemplate='Date: %{x}<br>Price: ₹%{y:,.0f}<extra></extra>'
))

# Add current price point
fig.add_trace(go.Scatter(
    x=[historical_data['Date'].iloc[-1]],
    y=[current_price],
    mode='markers',
    name='Current',
    marker=dict(size=15, color='#DB4545', symbol='diamond'),
    hovertemplate='Current: ₹%{y:,.0f}<extra></extra>'
))

# Add prediction lines with extended forecast
colors = ['#2E8B57', '#5D878F', '#D2BA4C']
dash_styles = ['dash', 'dot', 'dashdot']

for i, (model, pred_price) in enumerate(predictions.items()):
    pred_x = [historical_data['Date'].iloc[-1]] + list(future_dates)
    pred_y = [current_price] + [pred_price] * len(future_dates)
    
    fig.add_trace(go.Scatter(
        x=pred_x,
        y=pred_y,
        mode='lines+markers',
        name=f'{model}: ₹{pred_price:,.0f}',
        line=dict(color=colors[i], width=3, dash=dash_styles[i]),
        marker=dict(size=4, color=colors[i]),
        hovertemplate=f'{model}: ₹%{{y:,.0f}}<extra></extra>'
    ))

# Get chart boundaries for positioning dashboard elements
y_min = min(historical_data['Price']) - 500
y_max = max(historical_data['Price']) + 1000
x_min = historical_data['Date'].iloc[0]
x_max = future_dates[-1]

# Add dashboard-style annotations and text boxes
# Header simulation
fig.add_annotation(
    x=x_min + (x_max - x_min) * 0.5,
    y=y_max + 800,
    text="<b>NIFTY 50 AI Dashboard</b><br>Status: OPEN | Updated: 2024-01-15 09:45",
    showarrow=False,
    font=dict(size=16, color='#1FB8CD'),
    bgcolor='rgba(31, 184, 205, 0.1)',
    bordercolor='#1FB8CD',
    borderwidth=1,
    xanchor='center'
)

# Current price display
fig.add_annotation(
    x=x_min + (x_max - x_min) * 0.15,
    y=y_max + 400,
    text=f"<b>Current Price</b><br><span style='font-size:20px'>₹{current_price:,.0f}</span>",
    showarrow=False,
    font=dict(size=14, color='#DB4545'),
    bgcolor='rgba(219, 69, 69, 0.1)',
    bordercolor='#DB4545',
    borderwidth=1,
    xanchor='center'
)

# AI Predictions card
prediction_text = "<b>AI Predictions</b><br>" + "<br>".join([f"{k}: ₹{v:,.0f}" for k, v in predictions.items()])
fig.add_annotation(
    x=x_min + (x_max - x_min) * 0.85,
    y=y_max + 400,
    text=prediction_text,
    showarrow=False,
    font=dict(size=12, color='#2E8B57'),
    bgcolor='rgba(46, 139, 87, 0.1)',
    bordercolor='#2E8B57',
    borderwidth=1,
    xanchor='center'
)

# Recommendation card
fig.add_annotation(
    x=x_min + (x_max - x_min) * 0.15,
    y=y_max - 200,
    text="<b>Recommendation</b><br>Action: HOLD<br>Trend: +0.61%<br>Confidence: Medium",
    showarrow=False,
    font=dict(size=11, color='#D2BA4C'),
    bgcolor='rgba(210, 186, 76, 0.1)',
    bordercolor='#D2BA4C',
    borderwidth=1,
    xanchor='center'
)

# Performance metrics
metrics_text = "<b>Model Performance</b><br>RNN: RMSE 0.059<br>LSTM: RMSE 0.002<br>CNN: RMSE 0.134"
fig.add_annotation(
    x=x_min + (x_max - x_min) * 0.85,
    y=y_max - 200,
    text=metrics_text,
    showarrow=False,
    font=dict(size=11, color='#5D878F'),
    bgcolor='rgba(93, 135, 143, 0.1)',
    bordercolor='#5D878F',
    borderwidth=1,
    xanchor='center'
)

# Footer disclaimer
fig.add_annotation(
    x=x_min + (x_max - x_min) * 0.5,
    y=y_min - 300,
    text="Educational Purpose Only | API Access Available | Auto-refresh Every 5min",
    showarrow=False,
    font=dict(size=10, color='#13343B'),
    bgcolor='rgba(19, 52, 59, 0.1)',
    bordercolor='#13343B',
    borderwidth=1,
    xanchor='center'
)

# Current price callout on chart
fig.add_annotation(
    x=historical_data['Date'].iloc[-1],
    y=current_price,
    text=f"₹{current_price:,.0f}",
    showarrow=True,
    arrowhead=2,
    arrowcolor='#DB4545',
    bgcolor='#DB4545',
    bordercolor='white',
    font=dict(color='white', size=12),
    ax=30,
    ay=-30
)

# Update layout with dashboard styling
fig.update_layout(
    title='Interactive Price Chart with Predictions',
    xaxis_title='Date',
    yaxis_title='Price (₹)',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
    hovermode='x unified',
    plot_bgcolor='rgba(248, 249, 250, 0.8)',
    paper_bgcolor='white'
)

# Update traces
fig.update_traces(cliponaxis=False)

# Update axes with better formatting
fig.update_yaxes(tickformat='.0f', gridcolor='rgba(0,0,0,0.1)')
fig.update_xaxes(tickangle=45, gridcolor='rgba(0,0,0,0.1)')

# Save the chart
fig.write_image('nifty50_dashboard.png')
print("Complete dashboard-style chart saved successfully")