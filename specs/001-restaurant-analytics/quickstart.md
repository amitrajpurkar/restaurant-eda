# Quick Start Guide: Restaurant Analytics Web Application

**Purpose**: Get the restaurant analytics application running locally in minutes
**Created**: 2025-11-12
**Feature**: Restaurant Analytics Web Application

## Prerequisites

### System Requirements

- **Python**: 3.11 or higher
- **Memory**: 512MB minimum (for processing 50K+ records)
- **Storage**: 100MB free space
- **OS**: Windows, macOS, or Linux

### Required Files

- `zomato.csv` - Restaurant dataset (placed in the repository root `data/` directory)

## Installation Steps

### 1. Clone Repository and Setup Environment

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd restaurant-eda

# Switch to the feature branch
git checkout 001-restaurant-analytics

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -c "import flask, pandas, matplotlib, seaborn; print('Dependencies installed successfully')"
```

### 3. Prepare Data

```bash
# Verify data file exists (repo root)
ls -la ../data/zomato.csv
```

### 4. Run the Application

```bash
# Start the Flask application
python src/app.py

# You should see output similar to:
# * Serving Flask app 'app'
# * Running on http://127.0.0.1:5000
# * Loading restaurant data... 51717 records loaded
# * Analytics processed in 0.045 seconds
```

### 5. Access the Application

Open your web browser and navigate to:
- **Main Dashboard**: http://127.0.0.1:5000
- **API Documentation**: http://127.0.0.1:5000/api/docs
- **Health Check**: http://127.0.0.1:5000/api/health

## Application Features

### Main Dashboard Sections

1. **Restaurant Types Summary**
   - Card display showing restaurant type distribution
   - Hover for average rating and cost information
   - Pie chart visualization

2. **Top Restaurants Ranking**
   - Top 10 restaurants by votes and ratings
   - Click cards for detailed information
   - Bar chart visualization

3. **Foodie Areas Analysis**
   - Bangalore areas ranked by restaurant density
   - Area-specific cuisine and restaurant type breakdowns
   - Location-based insights

### API Endpoints

- `GET /api/health` - Application health status
- `GET /api/restaurant-types` - Restaurant type analytics
- `GET /api/top-restaurants` - Top restaurants ranking
- `GET /api/foodie-areas` - Foodie areas analysis
- `GET /api/charts/{type}` - Chart generation

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
pytest tests/contract/      # Contract tests only
```

### Code Quality Checks

```bash
# Type checking
mypy src/

# Linting
ruff check src/

# Code formatting
black src/
```

### Development Server Options

```bash
# Development mode with debug
export FLASK_ENV=development
python src/app.py

# Auto-reload on file changes
flask --app src.app run --debug
```

## Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'flask'"
```bash
# Solution: Activate virtual environment and install dependencies
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
```

**Issue**: "FileNotFoundError: zomato.csv"
```bash
# Solution: Ensure data file is in correct location (repo root)
ls data/zomato.csv
```

**Issue**: "Memory error when loading data"
```bash
# Solution: Check available memory and data file size
python -c "import pandas as pd; df = pd.read_csv('data/zomato.csv'); print(f'Shape: {df.shape}, Memory: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB')"
```

**Issue**: "Port 5000 already in use"
```bash
# Solution: Use different port
export FLASK_PORT=5001
python src/app.py
# Or kill existing process
lsof -ti:5000 | xargs kill
```

### Performance Issues

**Slow initial load**:
- Check CSV file size (should be <50MB)
- Verify sufficient RAM (>512MB available)
- Consider data sampling for testing

**Slow API responses**:
- Check data processing logs
- Verify pandas operations are vectorized
- Monitor memory usage

### Data Issues

**Missing or corrupted data**:
```bash
# Validate CSV structure
python -c "
import pandas as pd
df = pd.read_csv('data/zomato.csv')
print(f'Columns: {list(df.columns)}')
print(f'Shape: {df.shape}')
print(f'Missing values: {df.isnull().sum().sum()}')
"
```

**Incorrect analytics results**:
- Check data cleaning logic in `src/services/data_loader.py`
- Verify aggregation calculations in `src/services/analytics.py`
- Review test cases for expected behavior

## Configuration

### Environment Variables

Create `.env` file in backend directory:

```bash
# Flask configuration
FLASK_ENV=development
FLASK_PORT=5000
FLASK_DEBUG=true

# Data configuration
DATA_FILE_PATH=data/zomato.csv
CHART_CACHE_ENABLED=true
CHART_CACHE_TTL=300

# Performance configuration
MAX_WORKERS=4
MEMORY_LIMIT_MB=512
```

### Customization Options

**Chart Appearance**:
Edit `src/utils/charts.py` to modify colors, fonts, and styles

**Data Processing**:
Edit `src/services/analytics.py` to change ranking algorithms or add new metrics

**UI Customization**:
Edit `frontend/static/css/main.css` and `frontend/templates/` files

## Production Deployment

### Basic Production Setup

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 src.app:app

# Or with systemd service
sudo systemctl start restaurant-analytics
```

### Docker Deployment

```bash
# Build Docker image
docker build -t restaurant-analytics .

# Run container
docker run -p 5000:5000 -v $(pwd)/data:/app/data restaurant-analytics
```

## Next Steps

1. **Explore the Data**: Browse the dashboard and analyze restaurant patterns
2. **Customize Visualizations**: Modify chart styles and add new analytics
3. **Extend Features**: Add new API endpoints or frontend components
4. **Deploy**: Set up production hosting for wider access

## Support

For issues or questions:
1. Check this troubleshooting section
2. Review the test cases for expected behavior
3. Examine the API documentation at `/api/docs`
4. Check application logs for detailed error information

Happy analyzing! 🍽️📊
