# Setup Instructions for Web Dashboard

## 🌐 Live Dashboard URL
Your dashboard will be available at: `https://[username].github.io/[repository-name]`

## 🚀 Quick Setup

### 1. Repository Configuration
1. Fork or create this repository
2. Go to **Settings** → **Pages**  
3. Under **Source**, select **GitHub Actions**
4. The dashboard will auto-deploy on every push to main branch

### 2. Automatic Updates
- **Daily Updates**: Runs automatically Monday-Friday at 9:30 AM IST
- **Manual Trigger**: Go to Actions tab → "Deploy NIFTY 50 Dashboard" → "Run workflow"
- **Model Training**: Monthly automatic retraining (first Sunday of each month)

### 3. Customization
Edit these files to customize:
- `templates/dashboard.html`: Web interface design
- `src/web_generator.py`: Chart generation and data processing
- `.github/workflows/deploy_dashboard.yml`: Deployment schedule

## 📊 Features

### Real-Time Dashboard
- **Live NIFTY 50 Price**: Current market price and status
- **AI Predictions**: Next-day predictions from RNN, LSTM, CNN models
- **Investment Recommendation**: Automated BUY/HOLD/SELL suggestions
- **Interactive Charts**: Price trends, volume, model comparisons
- **Performance Metrics**: Model accuracy from research paper

### API Access
- **JSON Data**: Access raw data at `/data.json`
- **Prediction History**: Historical predictions at `/prediction_history.json`
- **Mobile Responsive**: Works on all devices

## 🔧 Technical Details

### Data Sources
- **Primary**: Yahoo Finance (yfinance) for real-time NIFTY 50 data
- **Backup**: NSE API integration available
- **Update Frequency**: Daily during market hours

### Model Implementation
Based on research paper: "Stock Market Prediction of NIFTY 50 Index Applying Machine Learning Techniques"
- **RNN**: 2 layers, ReLU activation, 0.2 dropout
- **LSTM**: 2 layers, ReLU activation, best performer (RMSE: 0.002)
- **CNN**: 3 conv layers, Sigmoid activation, max pooling

### Deployment Pipeline
```
Data Collection → Model Prediction → Chart Generation → HTML Rendering → GitHub Pages
```

## 📱 Mobile Features
- Responsive design for all screen sizes
- Auto-refresh during market hours
- Touch-friendly interactive charts
- Offline-capable static site

## 🛠️ Troubleshooting

### Dashboard Not Updating
1. Check **Actions** tab for workflow status
2. Ensure GitHub Pages is enabled in repository settings
3. Verify workflow permissions in Settings → Actions → General

### Prediction Errors
1. Check workflow logs in Actions tab
2. Verify data source availability (yfinance API)
3. Review error logs in workflow artifacts

### Custom Domain (Optional)
1. Add `CNAME` file to `docs/` directory with your domain
2. Configure DNS settings at your domain provider
3. Enable HTTPS in repository settings

## 📈 Usage Tips

### Best Viewing Times
- **Market Hours**: 9:15 AM - 3:30 PM IST for live updates
- **After Hours**: View predictions for next trading day
- **Weekends**: Review weekly performance and trends

### Investment Guidance
- **BUY Signal**: Strong upward trend predicted (>2% increase)
- **HOLD Signal**: Stable or moderate trend (-0.5% to +2%)
- **SELL Signal**: Strong downward trend predicted (<-2%)

⚠️ **Disclaimer**: This is for educational purposes only. Always consult financial advisors before making investment decisions.
