# Web page generator for NIFTY 50 predictions
import json
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import logging

class WebDashboardGenerator:
    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def generate_dashboard(self, predictions, historical_data, model_metrics):
        '''
        Generate complete HTML dashboard with predictions and charts
        '''
        try:
            # Create charts
            price_chart = self.create_price_chart(historical_data, predictions)
            metrics_chart = self.create_metrics_chart(model_metrics)
            comparison_chart = self.create_prediction_comparison(predictions)

            # Prepare data for template
            dashboard_data = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S IST'),
                'current_price': historical_data['Close'].iloc[-1],
                'predictions': predictions,
                'recommendation': self.get_recommendation(predictions, historical_data['Close'].iloc[-1]),
                'price_chart': price_chart,
                'metrics_chart': metrics_chart,
                'comparison_chart': comparison_chart,
                'model_performance': model_metrics,
                'market_status': self.get_market_status()
            }

            # Generate HTML
            html_content = self.render_template('dashboard.html', dashboard_data)

            # Save to docs folder for GitHub Pages
            os.makedirs('docs', exist_ok=True)
            with open('docs/index.html', 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Also save data as JSON for API access
            with open('docs/data.json', 'w', encoding='utf-8') as f:
                json.dump(dashboard_data, f, indent=2, default=str)

            self.logger.info("Dashboard generated successfully at docs/index.html")
            return True

        except Exception as e:
            self.logger.error(f"Error generating dashboard: {str(e)}")
            raise

    def create_price_chart(self, historical_data, predictions):
        '''Create interactive price chart with predictions'''
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('NIFTY 50 Price Trend', 'Volume'),
            specs=[[{"secondary_y": False}], [{"secondary_y": False}]],
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )

        # Historical prices
        fig.add_trace(
            go.Scatter(
                x=historical_data.index,
                y=historical_data['Close'],
                mode='lines',
                name='Historical Price',
                line=dict(color='#1f77b4', width=2)
            ),
            row=1, col=1
        )

        # Prediction points
        next_date = pd.date_range(start=historical_data.index[-1], periods=2, freq='D')[1]

        colors = ['#ff7f0e', '#2ca02c', '#d62728']  # RNN, LSTM, CNN
        for i, (model, pred) in enumerate(predictions.items()):
            fig.add_trace(
                go.Scatter(
                    x=[historical_data.index[-1], next_date],
                    y=[historical_data['Close'].iloc[-1], pred],
                    mode='lines+markers',
                    name=f'{model} Prediction',
                    line=dict(color=colors[i], width=3, dash='dash'),
                    marker=dict(size=8)
                ),
                row=1, col=1
            )

        # Volume
        fig.add_trace(
            go.Bar(
                x=historical_data.index[-30:],  # Last 30 days
                y=historical_data['Volume'].iloc[-30:],
                name='Volume',
                marker_color='rgba(158,202,225,0.6)',
                showlegend=False
            ),
            row=2, col=1
        )

        fig.update_layout(
            title='NIFTY 50 Stock Prediction Dashboard',
            xaxis_title='Date',
            yaxis_title='Price (₹)',
            template='plotly_white',
            height=600,
            showlegend=True,
            legend=dict(x=0.01, y=0.99)
        )

        fig.update_yaxes(title_text="Price (₹)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        return pyo.plot(fig, output_type='div', include_plotlyjs=False)

    def create_metrics_chart(self, model_metrics):
        '''Create model performance comparison chart'''
        models = list(model_metrics.keys())
        metrics = ['RMSE', 'MAE', 'R2']

        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=metrics,
            specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]]
        )

        colors = ['#ff7f0e', '#2ca02c', '#d62728']

        for i, metric in enumerate(metrics):
            values = [model_metrics[model].get(metric, 0) for model in models]

            fig.add_trace(
                go.Bar(
                    x=models,
                    y=values,
                    name=metric,
                    marker_color=colors[i],
                    showlegend=False
                ),
                row=1, col=i+1
            )

        fig.update_layout(
            title='Model Performance Comparison',
            height=400,
            template='plotly_white'
        )

        return pyo.plot(fig, output_type='div', include_plotlyjs=False)

    def create_prediction_comparison(self, predictions):
        '''Create prediction comparison chart'''
        models = list(predictions.keys())
        values = list(predictions.values())

        fig = go.Figure(data=[
            go.Bar(
                x=models,
                y=values,
                marker_color=['#ff7f0e', '#2ca02c', '#d62728'],
                text=[f'₹{v:.2f}' for v in values],
                textposition='auto',
            )
        ])

        fig.update_layout(
            title='Next Day Price Predictions by Model',
            xaxis_title='Model',
            yaxis_title='Predicted Price (₹)',
            template='plotly_white',
            height=300
        )

        return pyo.plot(fig, output_type='div', include_plotlyjs=False)

    def get_recommendation(self, predictions, current_price):
        '''Generate investment recommendation'''
        avg_prediction = sum(predictions.values()) / len(predictions)
        change_pct = ((avg_prediction - current_price) / current_price) * 100

        if change_pct > 2:
            return {
                'action': 'BUY',
                'confidence': 'High',
                'reason': f'Strong upward trend predicted (+{change_pct:.2f}%)',
                'color': '#28a745'
            }
        elif change_pct > 0.5:
            return {
                'action': 'HOLD',
                'confidence': 'Medium',
                'reason': f'Moderate upward trend predicted (+{change_pct:.2f}%)',
                'color': '#ffc107'
            }
        elif change_pct > -0.5:
            return {
                'action': 'HOLD',
                'confidence': 'Medium',
                'reason': f'Stable trend predicted ({change_pct:+.2f}%)',
                'color': '#6c757d'
            }
        elif change_pct > -2:
            return {
                'action': 'CAUTION',
                'confidence': 'Medium',
                'reason': f'Moderate downward trend predicted ({change_pct:.2f}%)',
                'color': '#fd7e14'
            }
        else:
            return {
                'action': 'SELL',
                'confidence': 'High',
                'reason': f'Strong downward trend predicted ({change_pct:.2f}%)',
                'color': '#dc3545'
            }

    def get_market_status(self):
        '''Get current market status'''
        now = datetime.now()
        # Indian market hours: 9:15 AM to 3:30 PM IST
        market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)

        if market_open <= now <= market_close and now.weekday() < 5:
            return {'status': 'OPEN', 'color': '#28a745'}
        else:
            return {'status': 'CLOSED', 'color': '#dc3545'}

    def render_template(self, template_name, data):
        '''Render HTML template with data'''
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template(template_name)
        return template.render(**data)

if __name__ == "__main__":
    # Test web generation
    generator = WebDashboardGenerator()

    # Sample data for testing
    sample_predictions = {
        'RNN': 18650.25,
        'LSTM': 18720.75,
        'CNN': 18590.30
    }

    sample_metrics = {
        'RNN': {'RMSE': 0.059, 'MAE': 0.042, 'R2': 0.810},
        'LSTM': {'RMSE': 0.002, 'MAE': 0.032, 'R2': 0.537},
        'CNN': {'RMSE': 0.134, 'MAE': 0.016, 'R2': 0.765}
    }

    print("Web generator initialized successfully!")
