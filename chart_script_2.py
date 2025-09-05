import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Parse the data
data = [
  {
    "deployment_type": "Email-Based System",
    "steps": [
      {
        "step": "Data Collection",
        "duration": "2 min",
        "complexity": "Medium",
        "description": "Fetch NIFTY 50 data from Yahoo Finance"
      },
      {
        "step": "ML Predictions", 
        "duration": "1 min",
        "complexity": "Medium",
        "description": "Generate RNN, LSTM, CNN predictions"
      },
      {
        "step": "Email Gen",
        "duration": "30 sec",
        "complexity": "Medium", 
        "description": "Create HTML email template"
      },
      {
        "step": "SMTP Auth",
        "duration": "10 sec",
        "complexity": "High",
        "description": "Gmail app password authentication"
      },
      {
        "step": "Send Email",
        "duration": "5 sec",
        "complexity": "Low",
        "description": "Send via Gmail SMTP"
      }
    ],
    "total_time": "3.75 min",
    "user_access": "Email Inbox Only",
    "mobile_friendly": "Limited",
    "real_time": "No",
    "setup_complexity": "High (Gmail config)",
    "maintenance": "Medium (SMTP issues)",
    "api_access": "None"
  },
  {
    "deployment_type": "Web-Based System",
    "steps": [
      {
        "step": "Data Collection",
        "duration": "2 min", 
        "complexity": "Medium",
        "description": "Fetch NIFTY 50 data from Yahoo Finance"
      },
      {
        "step": "ML Predictions",
        "duration": "1 min",
        "complexity": "Medium",
        "description": "Generate RNN, LSTM, CNN predictions"
      },
      {
        "step": "Chart Gen",
        "duration": "30 sec",
        "complexity": "Medium",
        "description": "Create interactive Plotly visualizations"
      },
      {
        "step": "HTML Render", 
        "duration": "15 sec",
        "complexity": "Low",
        "description": "Generate responsive dashboard"
      },
      {
        "step": "Pages Deploy",
        "duration": "30 sec",
        "complexity": "Low", 
        "description": "Auto-deploy to GitHub Pages"
      }
    ],
    "total_time": "4.25 min",
    "user_access": "Any Browser/Device",
    "mobile_friendly": "Fully Responsive",
    "real_time": "Yes (auto-refresh)",
    "setup_complexity": "Low (GitHub only)",
    "maintenance": "Very Low (automatic)",
    "api_access": "JSON endpoints available"
  }
]

# Function to convert duration to seconds
def duration_to_seconds(duration_str):
    if 'min' in duration_str:
        return float(duration_str.replace(' min', '')) * 60
    elif 'sec' in duration_str:
        return float(duration_str.replace(' sec', ''))
    return 0

# Prepare data for timeline visualization
timeline_data = []
system_colors = ['#DB4545', '#1FB8CD']  # Red for email, cyan for web
complexity_colors = {'High': '#964325', 'Medium': '#D2BA4C', 'Low': '#2E8B57'}

for i, system in enumerate(data):
    cumulative_time = 0
    system_name = system["deployment_type"]
    
    for j, step in enumerate(system["steps"]):
        duration_sec = duration_to_seconds(step["duration"])
        
        timeline_data.append({
            'system': system_name,
            'step': step["step"],
            'start_time': cumulative_time,
            'duration': duration_sec,
            'end_time': cumulative_time + duration_sec,
            'complexity': step["complexity"],
            'description': step["description"][:35],
            'system_color': system_colors[i],
            'complexity_color': complexity_colors[step["complexity"]],
            'y_pos': i,
            'duration_display': step["duration"],
            'total_time': system["total_time"]
        })
        
        cumulative_time += duration_sec

# Create the figure
fig = go.Figure()

# Add timeline bars for each step
for row in timeline_data:
    # Only show step name if bar is wide enough, otherwise show duration only
    if row['duration'] >= 20:  # 20 seconds or more
        text_content = f"{row['step']}<br>{row['duration_display']}"
    else:
        text_content = row['duration_display']
    
    fig.add_trace(go.Bar(
        x=[row['duration']],
        y=[row['system']],
        orientation='h',
        base=[row['start_time']],
        name=row['step'],
        marker_color=row['complexity_color'],
        marker_line=dict(color=row['system_color'], width=4),
        opacity=0.9,
        text=text_content,
        textposition='inside',
        textfont=dict(size=11, color='white', family='Arial Black'),
        hovertemplate=(
            f"<b>{row['step']}</b><br>" +
            f"Duration: {row['duration_display']}<br>" +
            f"Complexity: {row['complexity']}<br>" +
            f"{row['description']}" +
            "<extra></extra>"
        ),
        showlegend=False
    ))

# Update layout
fig.update_layout(
    title="NIFTY 50 Deploy Timeline Comparison",
    xaxis_title="Time (min)",
    yaxis_title="",
    barmode='overlay'
)

# Update x-axis to show proper minutes scale
max_time = max([row['end_time'] for row in timeline_data])
fig.update_xaxes(
    range=[0, max_time + 30],
    tickmode='linear',
    dtick=30,
    tickvals=[0, 30, 60, 90, 120, 150, 180, 210, 240, 270],
    ticktext=['0', '0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5'],
    title="Time (min)"
)

# Update traces
fig.update_traces(cliponaxis=False)

# Add total time labels at the end of each timeline
email_total = 225  # 3.75 minutes in seconds
web_total = 255   # 4.25 minutes in seconds

fig.add_annotation(
    x=email_total + 15, y=0,
    text="Total: 3.75m",
    showarrow=False,
    font=dict(size=12, color="#DB4545", family='Arial Black'),
    bgcolor="rgba(255,255,255,0.9)",
    bordercolor="#DB4545",
    borderwidth=2
)

fig.add_annotation(
    x=web_total + 15, y=1,
    text="Total: 4.25m",
    showarrow=False,
    font=dict(size=12, color="#1FB8CD", family='Arial Black'),
    bgcolor="rgba(255,255,255,0.9)",
    bordercolor="#1FB8CD",
    borderwidth=2
)

# Add system advantages/limitations closer to timelines
fig.add_annotation(
    x=140, y=0.3,
    text="❌ SMTP Setup ❌ Email Only ❌ No Real-time",
    showarrow=False,
    font=dict(size=11, color="#DB4545"),
    bgcolor="rgba(219,69,69,0.1)",
    bordercolor="#DB4545",
    borderwidth=1
)

fig.add_annotation(
    x=140, y=0.7,
    text="✅ Mobile Ready ✅ API Access ✅ Auto Updates",
    showarrow=False,
    font=dict(size=11, color="#1FB8CD"),
    bgcolor="rgba(31,184,205,0.1)",
    bordercolor="#1FB8CD",
    borderwidth=1
)

# Add complexity legend at the bottom
fig.add_annotation(
    x=135, y=-0.7,
    text="Complexity Legend:",
    showarrow=False,
    font=dict(size=12, color="black", family='Arial Black'),
)

# Add colored boxes for complexity legend
fig.add_shape(type="rect", x0=180, y0=-0.75, x1=190, y1=-0.65, 
              fillcolor="#964325", line=dict(width=1, color="white"))
fig.add_annotation(x=195, y=-0.7, text="High", showarrow=False, 
                  font=dict(size=11, color="#964325"))

fig.add_shape(type="rect", x0=210, y0=-0.75, x1=220, y1=-0.65, 
              fillcolor="#D2BA4C", line=dict(width=1, color="white"))
fig.add_annotation(x=225, y=-0.7, text="Medium", showarrow=False, 
                  font=dict(size=11, color="#D2BA4C"))

fig.add_shape(type="rect", x0=250, y0=-0.75, x1=260, y1=-0.65, 
              fillcolor="#2E8B57", line=dict(width=1, color="white"))
fig.add_annotation(x=265, y=-0.7, text="Low", showarrow=False, 
                  font=dict(size=11, color="#2E8B57"))

# Update y-axis range to accommodate legend
fig.update_yaxes(range=[-0.9, 1.5])

# Save the chart
fig.write_image("deployment_timeline_comparison.png", width=1200, height=600, scale=2)