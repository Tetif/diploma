"""
Example usage of the Influence Functions Microservice

This file contains practical examples of how to use the microservice
both through the API and Streamlit interface.
"""

# ==================== API Examples ====================

# Example 1: Start an experiment via Python requests
def example_start_experiment_api():
    """Example of starting an experiment via API"""
    import requests
    import json
    
    API_URL = "http://localhost:8000"
    
    # Configuration for the experiment
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
        "use_distillation": False,
        "random_state": 39,
        "debug_mode": False
    }
    
    # Start the experiment
    response = requests.post(
        f"{API_URL}/experiments/start",
        json={"config": config},
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        experiment_id = result['experiment_id']
        print(f"✓ Experiment started: {experiment_id}")
        return experiment_id
    else:
        print(f"✗ Error starting experiment: {response.text}")
        return None


# Example 2: Poll experiment status
def example_poll_status(experiment_id: str):
    """Example of polling experiment status"""
    import requests
    import time
    
    API_URL = "http://localhost:8000"
    
    while True:
        response = requests.get(
            f"{API_URL}/experiments/{experiment_id}/status",
            timeout=10
        )
        
        if response.status_code == 200:
            status = response.json()
            print(f"Status: {status['status']} ({status['progress']}%)")
            print(f"Message: {status['message']}")
            
            if status['status'] in ['completed', 'failed']:
                return status
        
        time.sleep(2)  # Poll every 2 seconds


# Example 3: Get experiment results
def example_get_results(experiment_id: str):
    """Example of getting experiment results"""
    import requests
    
    API_URL = "http://localhost:8000"
    
    response = requests.get(
        f"{API_URL}/experiments/{experiment_id}/results",
        timeout=10
    )
    
    if response.status_code == 200:
        results = response.json()
        print(f"Dataset: {results['config']['dataset_name']}")
        print(f"Model: {results['config']['model_type']}")
        print(f"Samples: {results['samples_count']}")
        print(f"Methods computed: {len(results['influence_methods'])}")
        print(f"Execution time: {results['execution_time']}s")
        return results
    else:
        print(f"✗ Error getting results: {response.text}")
        return None


# Example 4: Get influence weights
def example_get_influence_weights(experiment_id: str, method: str = "BetaShapley"):
    """Example of getting influence weights for a method"""
    import requests
    import numpy as np
    
    API_URL = "http://localhost:8000"
    
    response = requests.get(
        f"{API_URL}/experiments/{experiment_id}/influence-weights/{method}",
        timeout=10
    )
    
    if response.status_code == 200:
        weights_data = response.json()
        weights = np.array(weights_data['weights'])
        stats = weights_data['statistics']
        
        print(f"Method: {method}")
        print(f"Count: {weights_data['count']}")
        print(f"Statistics:")
        print(f"  Min: {stats['min']:.6f}")
        print(f"  Max: {stats['max']:.6f}")
        print(f"  Mean: {stats['mean']:.6f}")
        print(f"  Std: {stats['std']:.6f}")
        
        return weights
    else:
        print(f"✗ Error getting weights: {response.text}")
        return None


# Example 5: List all experiments
def example_list_experiments():
    """Example of listing saved experiments"""
    import requests
    
    API_URL = "http://localhost:8000"
    
    response = requests.get(
        f"{API_URL}/experiments",
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total experiments: {data['total']}")
        for exp in data['experiments']:
            print(f"  {exp['experiment_id'][:8]}... - {exp['dataset']} ({exp['created_at']})")
        return data['experiments']
    else:
        print(f"✗ Error listing experiments: {response.text}")
        return None


# Example 6: Compare multiple influence methods
def example_compare_methods(experiment_id: str):
    """Example of comparing multiple influence methods"""
    import requests
    import numpy as np
    
    API_URL = "http://localhost:8000"
    
    # Get available methods
    response = requests.get(f"{API_URL}/info/influence-methods", timeout=10)
    methods = response.json()['methods'][:3]  # Get first 3 methods
    
    print(f"Comparing methods for experiment {experiment_id[:8]}...")
    
    method_stats = {}
    for method in methods:
        weights_response = requests.get(
            f"{API_URL}/experiments/{experiment_id}/influence-weights/{method}",
            timeout=10
        )
        
        if weights_response.status_code == 200:
            data = weights_response.json()
            stats = data['statistics']
            method_stats[method] = stats
            
            print(f"\n{method}:")
            print(f"  Mean: {stats['mean']:.4f}")
            print(f"  Std:  {stats['std']:.4f}")
            print(f"  Min:  {stats['min']:.4f}")
            print(f"  Max:  {stats['max']:.4f}")
    
    return method_stats


# Example 7: Full workflow
def example_full_workflow():
    """Complete example: start, poll, get results"""
    import requests
    import numpy as np
    import time
    
    print("🚀 Starting complete workflow example...")
    print("=" * 60)
    
    # Step 1: Start experiment
    print("\n1️⃣  Starting experiment...")
    experiment_id = example_start_experiment_api()
    if not experiment_id:
        return
    
    # Step 2: Poll status
    print("\n2️⃣  Polling experiment status...")
    status = example_poll_status(experiment_id)
    
    if status['status'] != 'completed':
        print("✗ Experiment failed")
        return
    
    # Step 3: Get results
    print("\n3️⃣  Retrieving results...")
    results = example_get_results(experiment_id)
    
    # Step 4: Get influence weights
    print("\n4️⃣  Retrieving influence weights...")
    weights = example_get_influence_weights(experiment_id, "BetaShapley")
    
    # Step 5: Compare methods
    print("\n5️⃣  Comparing influence methods...")
    method_stats = example_compare_methods(experiment_id)
    
    print("\n" + "=" * 60)
    print("✓ Workflow completed successfully!")


# ==================== Streamlit Examples ====================

# The Streamlit interface is self-contained and provides:
# - GUI for starting experiments
# - Real-time status tracking
# - Interactive visualization of results
# - Influence weights browser
# - Experiment comparison tools

# To use: streamlit run microservice/app.py

# ==================== Command Line Usage ====================

# Start both API and UI:
# python microservice/run_services.py

# Start only API:
# python microservice/run_api.py

# Start only UI:
# python microservice/run_ui.py

# View API documentation:
# http://localhost:8000/docs

# Access Streamlit UI:
# http://localhost:8501

# ==================== Docker Usage ====================

# Build and run with Docker Compose:
# docker-compose up

# This will start:
# - API on http://localhost:8000
# - UI on http://localhost:8501

# ==================== Advanced Usage ====================

def example_batch_experiments():
    """Example of running multiple experiments in batch"""
    import requests
    import json
    
    API_URL = "http://localhost:8000"
    
    # Define multiple configurations
    configs = [
        {
            "dataset_name": "housing",
            "model_type": "random_forest",
            "sample_size_percentage": 100,
            "selected_influence_methods": ["BetaShapley"]
        },
        {
            "dataset_name": "adult",
            "model_type": "lightgbm",
            "sample_size_percentage": 100,
            "selected_influence_methods": ["Banzhaf"]
        },
        {
            "dataset_name": "wine",
            "model_type": "catboost",
            "sample_size_percentage": 100,
            "selected_influence_methods": ["Shapley"]
        }
    ]
    
    experiment_ids = []
    
    # Start all experiments
    for config in configs:
        response = requests.post(
            f"{API_URL}/experiments/start",
            json={"config": config},
            timeout=30
        )
        
        if response.status_code == 200:
            exp_id = response.json()['experiment_id']
            experiment_ids.append(exp_id)
            print(f"Started: {config['dataset_name']} with {config['model_type']}")
    
    print(f"\nStarted {len(experiment_ids)} experiments")
    return experiment_ids


def example_export_results(experiment_id: str, output_format: str = "csv"):
    """Example of exporting results to different formats"""
    import requests
    import pandas as pd
    import json
    
    API_URL = "http://localhost:8000"
    
    # Get influence weights
    response = requests.get(
        f"{API_URL}/experiments/{experiment_id}/influence-weights/BetaShapley",
        timeout=10
    )
    
    if response.status_code == 200:
        weights_data = response.json()
        weights = weights_data['weights']
        
        df = pd.DataFrame({
            'sample_index': range(len(weights)),
            'influence_score': weights
        })
        
        if output_format == "csv":
            filename = f"influence_weights_{experiment_id[:8]}.csv"
            df.to_csv(filename, index=False)
            print(f"✓ Exported to {filename}")
        elif output_format == "json":
            filename = f"influence_weights_{experiment_id[:8]}.json"
            with open(filename, 'w') as f:
                json.dump({
                    'experiment_id': experiment_id,
                    'weights': weights,
                    'count': len(weights)
                }, f, indent=2)
            print(f"✓ Exported to {filename}")


if __name__ == "__main__":
    # Run the full workflow example
    example_full_workflow()
    
    # Uncomment to run other examples:
    # example_list_experiments()
    # example_batch_experiments()
