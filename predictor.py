# Updated prediction engine for web deployment
import pandas as pd
import numpy as np
from src.data_collector import NIFTYDataCollector
from src.models import NIFTYModels
from src.web_generator import WebDashboardGenerator
import joblib
from datetime import datetime
import logging
import json

class NIFTYWebPredictor:
    def __init__(self):
        self.data_collector = NIFTYDataCollector()
        self.models = NIFTYModels()
        self.web_generator = WebDashboardGenerator()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/prediction.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def run_daily_prediction(self):
        '''
        Main function to run daily predictions and update website
        Called by GitHub Actions
        '''
        try:
            self.logger.info("Starting daily NIFTY 50 prediction for web dashboard...")

            # Fetch latest data
            data = self.data_collector.fetch_nifty_data()
            processed_data, scaler = self.data_collector.preprocess_data(data)

            # Load or create sample models (for demo)
            predictions = self.make_sample_predictions(data)

            # Get model performance metrics
            model_metrics = self.get_model_metrics()

            # Generate web dashboard
            success = self.web_generator.generate_dashboard(
                predictions, 
                data, 
                model_metrics
            )

            if success:
                self.logger.info("Web dashboard updated successfully")
                self.save_prediction_log(predictions, data)
            else:
                raise Exception("Failed to generate web dashboard")

        except Exception as e:
            self.logger.error(f"Error in daily prediction: {str(e)}")
            self.generate_error_page(str(e))
            raise

    def make_sample_predictions(self, data):
        '''
        Make sample predictions (replace with actual trained models)
        '''
        current_price = data['Close'].iloc[-1]

        # Generate realistic predictions based on recent trend
        recent_change = (current_price - data['Close'].iloc[-5]) / data['Close'].iloc[-5]

        predictions = {
            'RNN': current_price * (1 + recent_change * 0.8 + np.random.normal(0, 0.005)),
            'LSTM': current_price * (1 + recent_change * 1.2 + np.random.normal(0, 0.003)),
            'CNN': current_price * (1 + recent_change * 0.6 + np.random.normal(0, 0.007))
        }

        return predictions

    def get_model_metrics(self):
        '''
        Get model performance metrics (from research paper)
        '''
        return {
            'RNN': {
                'RMSE': 0.059,
                'MAE': 0.042,
                'R2': 0.810,
                'MSE': 0.00347
            },
            'LSTM': {
                'RMSE': 0.002,
                'MAE': 0.032,
                'R2': 0.537,
                'MSE': 0.002
            },
            'CNN': {
                'RMSE': 0.134,
                'MAE': 0.016,
                'R2': 0.765,
                'MSE': 0.018
            }
        }

    def save_prediction_log(self, predictions, data):
        '''Save prediction history'''
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'current_price': float(data['Close'].iloc[-1]),
            'predictions': {k: float(v) for k, v in predictions.items()},
            'volume': float(data['Volume'].iloc[-1])
        }

        # Append to history file
        history_file = 'docs/prediction_history.json'
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        history.append(log_entry)

        # Keep only last 100 entries
        history = history[-100:]

        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def generate_error_page(self, error_message):
        '''Generate error page when predictions fail'''
        error_html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>NIFTY 50 Prediction - Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .error {{ color: #dc3545; text-align: center; }}
                .refresh {{ margin-top: 20px; text-align: center; }}
                .btn {{ background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="error">
                    <h1>⚠️ Service Temporarily Unavailable</h1>
                    <p>The NIFTY 50 prediction service is currently experiencing issues:</p>
                    <p><em>{error_message}</em></p>
                    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}</p>
                </div>
                <div class="refresh">
                    <a href="javascript:location.reload()" class="btn">Refresh Page</a>
                </div>
            </div>
        </body>
        </html>
        '''

        os.makedirs('docs', exist_ok=True)
        with open('docs/index.html', 'w', encoding='utf-8') as f:
            f.write(error_html)

if __name__ == "__main__":
    predictor = NIFTYWebPredictor()
    predictor.run_daily_prediction()
