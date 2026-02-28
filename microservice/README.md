# 🔬 Influence Functions Microservice

A FastAPI + Streamlit microservice for running influence function experiments with flexible configuration and interactive analysis.

## Features

✨ **Key Features:**
- 🎯 Support for 4 built-in datasets (Adult, Housing, Wine, Zillow)
- 🤖 Multiple model types (Random Forest, LightGBM, XGBoost, CatBoost, PyTorch)
- 📊 Comprehensive influence computation methods
- ⚙️ Full parameter configuration and customization
- 💾 Persistent storage of influence weights and results
- 📈 Interactive visualization and analysis
- 🔄 Experiment comparison and history
- 🚀 Asynchronous experiment processing

## Architecture

```
microservice/
├── api/
│   ├── __init__.py          # FastAPI application
│   └── models.py            # Pydantic models for API
├── services/
│   ├── __init__.py
│   └── experiment_service.py # Core experiment logic
├── storage/
│   ├── __init__.py
│   └── influence_storage.py  # Storage management
├── app.py                   # Streamlit UI
├── run_services.py          # Start both API and UI
├── run_api.py              # Start only API
├── run_ui.py               # Start only UI
└── README.md
```

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL (optional, for production)

### Setup

1. Install dependencies:
```bash
pip install -r requirements_microservice.txt
```

2. Configure environment (optional):
```bash
export API_BASE_URL="http://localhost:8000"
export API_PORT=8000
export STREAMLIT_PORT=8501
```

## Running the Microservice

### Option 1: Start Both Services (Recommended)

```bash
python microservice/run_services.py
```

This will start:
- **FastAPI** on `http://localhost:8000`
- **Streamlit** on `http://localhost:8501`

### Option 2: Start API Only

```bash
python microservice/run_api.py
```

API Documentation will be available at `http://localhost:8000/docs`

### Option 3: Start UI Only

Requires API already running on localhost:8000

```bash
python microservice/run_ui.py
```

## API Endpoints

### Health & Info
- `GET /health` - Health check
- `GET /info/datasets` - List available datasets
- `GET /info/models` - List available models
- `GET /info/influence-methods` - List available influence methods

### Experiments
- `POST /experiments/start` - Start new experiment
- `GET /experiments/{id}/status` - Get experiment status
- `GET /experiments/{id}/results` - Get experiment results
- `GET /experiments/{id}/influence-weights/{method}` - Get influence weights
- `GET /experiments` - List all experiments
- `DELETE /experiments/{id}` - Delete experiment

### Data
- `POST /datasets/upload` - Upload custom dataset (STUB)

## Streamlit Interface

### Pages

1. **Home** - Overview and quick start
2. **New Experiment** - Create and configure experiments
3. **Analysis** - Visualize results and influence weights
4. **Compare** - Side-by-side experiment comparison
5. **Settings** - Configure application preferences

### Workflow

1. Navigate to "New Experiment"
2. Select dataset and model
3. Configure data split, training parameters
4. Choose removal strategy and percentages
5. Select influence computation methods
6. Click "Start Experiment"
7. Wait for completion
8. Analyze results in the "Analysis" tab

## Configuration Options

### Model Parameters
- **Model Type**: `random_forest`, `lightgbm`, `xgboost`, `catboost`, `pytorch`
- **Epochs**: Number of training epochs (10-1000)
- **Cross-Validation**: K-fold CV folds (1-10)

### Data Configuration
- **Sample Size**: Percentage of data to use (1-100%)
- **Test Size**: Fraction for test set (0.1-0.5)
- **Validation Size**: Fraction for validation (0.05-0.3)

### Removal Strategy
- **Strategy**: `remove_lowest_influence` or `remove_highest_influence`
- **Percentages**: Range of removal percentages to test (1-99%)
- **Random Runs**: Number of random removal baseline runs (1-10)

### Influence Methods
- BetaShapley
- Shapley
- Influence
- ArnoldiInfluence
- CgInfluence
- LissaInfluence
- NystroemSketchInfluence
- PermutationImportance
- Banzhaf

## Influence Weights Storage

All computed influence weights are automatically saved in `microservice_storage/experiments/{experiment_id}/`:

```
experiment_id/
├── config.json          # Experiment configuration
├── results.json         # Model performance metrics
├── influence_weights.pkl # Computed weights (binary)
├── scores_raw.pkl       # Raw scores for all methods
└── metadata.json        # Metadata and timestamps
```

### Accessing Stored Weights

```python
from microservice.storage.influence_storage import InfluenceWeightsStorage

storage = InfluenceWeightsStorage()
experiment = storage.load_experiment(experiment_id)
weights = experiment['influence_weights']['BetaShapley']
```

## Example Usage

### Via Streamlit UI (Easiest)

1. Start services: `python microservice/run_services.py`
2. Open browser to `http://localhost:8501`
3. Navigate to "New Experiment"
4. Fill in configuration and click "Start Experiment"
5. Wait for completion and explore results

### Via API (Python)

```python
import requests
import json
import time

API_URL = "http://localhost:8000"

# 1. Start experiment
config = {
    "dataset_name": "housing",
    "model_type": "random_forest",
    "removal_strategy": "remove_lowest_influence",
    "n_remove_percentages": [10, 20, 30, 40, 50],
    "sample_size_percentage": 100,
    "test_size": 0.2,
    "val_size": 0.1,
    "n_epochs": 500,
    "n_random_runs": 3,
    "cv_folds": 1,
    "selected_influence_methods": ["BetaShapley", "Banzhaf"],
    "use_distillation": False
}

response = requests.post(
    f"{API_URL}/experiments/start",
    json={"config": config}
)
experiment_id = response.json()['experiment_id']
print(f"Started experiment: {experiment_id}")

# 2. Poll status
while True:
    status = requests.get(f"{API_URL}/experiments/{experiment_id}/status").json()
    print(f"Status: {status['status']} - {status['progress']}%")
    if status['status'] in ['completed', 'failed']:
        break
    time.sleep(2)

# 3. Get results
results = requests.get(f"{API_URL}/experiments/{experiment_id}/results").json()
print(f"Execution time: {results['execution_time']}s")

# 4. Get influence weights
weights = requests.get(
    f"{API_URL}/experiments/{experiment_id}/influence-weights/BetaShapley"
).json()
print(f"Got {weights['count']} influence scores")
print(f"Mean: {weights['statistics']['mean']:.4f}")
```

### Via cURL

```bash
# Start experiment
curl -X POST "http://localhost:8000/experiments/start" \
  -H "Content-Type: application/json" \
  -d '{
    "config": {
      "dataset_name": "adult",
      "model_type": "random_forest",
      "selected_influence_methods": ["BetaShapley"]
    }
  }'

# Check status
curl "http://localhost:8000/experiments/{experiment_id}/status"

# Get results
curl "http://localhost:8000/experiments/{experiment_id}/results"

# Get API documentation
curl "http://localhost:8000/docs"
```

## Performance Considerations

- **Small datasets** (< 1000 samples): Most methods complete in seconds
- **Medium datasets** (1000-10000): Usually 1-5 minutes
- **Large datasets** (> 10000): 5-30 minutes depending on method
- **GPU acceleration**: PyTorch models benefit from CUDA

## Troubleshooting

### API Connection Error
- Ensure API is running on localhost:8000
- Check firewall settings
- Verify no port conflicts

### Long Experiment Time
- Reduce `n_remove_percentages` range
- Decrease `cv_folds`
- Use faster methods (e.g., BetaShapley instead of Shapley)
- Reduce sample size

### Out of Memory
- Reduce `sample_size_percentage`
- Reduce batch size in experiment config
- Run on machine with more RAM

### GPU Not Detected
- Install CUDA toolkit
- Check PyTorch installation: `python -c "import torch; print(torch.cuda.is_available())"`

## Future Enhancements

📋 Planned features:
- [ ] Custom dataset upload support
- [ ] Database backend for experiment storage
- [ ] Advanced statistical analysis
- [ ] Experiment scheduling
- [ ] Multi-GPU support
- [ ] Export to various formats (Excel, PDF, etc.)
- [ ] Real-time collaboration
- [ ] REST API versioning

## Contributing

To contribute improvements:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

[Your License Here]

## Support

For issues or questions, please open an issue on GitHub or contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-17
