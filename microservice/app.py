"""Streamlit interface for Influence Functions Microservice"""
import sys
from pathlib import Path

# Ensure project root is on path so we can import top-level packages when
# Streamlit's working directory is `microservice/`.
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import streamlit as st
import requests
import json
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from visualization.plots import plot_influence_distribution as viz_plot_influence_distribution
from visualization.plots import plot_results_enhanced as viz_plot_results_enhanced
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Influence Functions Explorer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
POLL_INTERVAL = 2  # seconds

# ==================== Helper Functions ====================

def make_api_request(method: str, endpoint: str, data: Dict = None, timeout: int = 30) -> Optional[Dict]:
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        elif method == "DELETE":
            response = requests.delete(url, timeout=timeout)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to API at {API_BASE_URL}")
        return None
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        return None


def poll_experiment_status(experiment_id: str, max_wait: int = 3600) -> Optional[Dict]:
    """Poll experiment status until completion"""
    start_time = time.time()
    
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    while time.time() - start_time < max_wait:
        status_response = make_api_request("GET", f"/experiments/{experiment_id}/status")
        
        if status_response:
            with progress_placeholder.container():
                st.progress(min(status_response.get('progress', 0) / 100, 1.0))
            
            with status_placeholder.container():
                st.info(f"📊 {status_response.get('message', 'Processing...')}")
            
            if status_response.get('status') in ['completed', 'failed']:
                return status_response
        
        time.sleep(POLL_INTERVAL)
    
    st.error("⏱️ Experiment timeout")
    return None


def get_available_datasets() -> List[str]:
    """Get list of available datasets"""
    response = make_api_request("GET", "/info/datasets")
    if response:
        return response.get('datasets', [])
    return []


def get_available_models() -> List[str]:
    """Get list of available models"""
    response = make_api_request("GET", "/info/models")
    if response:
        return response.get('models', [])
    return ['random_forest']


def get_available_methods() -> List[str]:
    """Get list of available influence methods"""
    response = make_api_request("GET", "/info/influence-methods")
    if response:
        return response.get('methods', [])
    return []


def load_influence_weights(experiment_id: str, method: str) -> Optional[Dict]:
    """Load influence weights for specific method"""
    return make_api_request("GET", f"/experiments/{experiment_id}/influence-weights/{method}")


def load_graph_data(experiment_id: str) -> Optional[Dict]:
    """Load experiment graph data for plotting"""
    return make_api_request("GET", f"/experiments/{experiment_id}/graph-data")


def _local_plot_influence_distribution(weights: List[float], method: str) -> go.Figure:
    """Local Plotly fallback for influence weights distribution"""
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=weights,
        nbinsx=50,
        name='Influence Score Distribution',
        marker_color='rgba(55, 128, 191, 0.7)'
    ))

    fig.update_layout(
        title=f"Influence Scores Distribution - {method}",
        xaxis_title="Score Value",
        yaxis_title="Frequency",
        hovermode='x unified',
        template='plotly_white'
    )

    return fig


def plot_removal_comparison(results: Dict[str, Any], removal_percentages: List[int]) -> go.Figure:
    """Plot performance vs removal percentage"""
    fig = go.Figure()
    
    for method, values in results.items():
        if isinstance(values, dict) and 'final_mae' in values:
            continue
        if isinstance(values, (list, tuple)):
            fig.add_trace(go.Scatter(
                x=removal_percentages,
                y=values if isinstance(values, list) else [v.get('final_mae', 0) for v in values],
                mode='lines+markers',
                name=method,
                hovertemplate="<b>%{fullData.name}</b><br>Removal: %{x}%<br>MAE: %{y:.4f}<extra></extra>"
            ))
    
    fig.update_layout(
        title="Model Performance vs Data Removal",
        xaxis_title="Removal Percentage (%)",
        yaxis_title="Mean Absolute Error",
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


def plot_removal_impact(removal_data: Dict[str, List[Dict]]) -> go.Figure:
    """Plot removal impact for different methods"""
    fig = go.Figure()
    
    # Color palette for different methods
    colors = {
        'Influence': '#FF6B6B',
        'ArnoldiInfluence': '#4ECDC4',
        'CgInfluence': '#45B7D1',
        'LissaInfluence': '#FFA07A',
        'NystroemSketchInfluence': '#98D8C8',
        'PermutationImportance': '#F7DC6F',
        'Banzhaf': '#BB8FCE',
        'Shapley': '#F5B041',
        'BetaShapley': '#52BE80',
        'Random': '#808080'
    }
    
    for method, data_points in removal_data.items():
        if not data_points:
            continue
        
        # Sort by removal percentage
        sorted_data = sorted(data_points, key=lambda x: x.get('percent', 0))
        
        percentages = [d.get('percent', 0) for d in sorted_data]
        mae_values = [d.get('mae', 0) for d in sorted_data]
        
        fig.add_trace(go.Scatter(
            x=percentages,
            y=mae_values,
            mode='lines+markers',
            name=method,
            line=dict(color=colors.get(method, '#1f77b4')),
            marker=dict(size=8),
            hovertemplate="<b>%{fullData.name}</b><br>Removal: %{x}%<br>MAE: %{y:.4f}<extra></extra>"
        ))
    
    fig.update_layout(
        title="Model Performance Impact vs Data Removal Percentage",
        xaxis_title="Data Removal Percentage (%)",
        yaxis_title="Mean Absolute Error (MAE)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        font=dict(size=12)
    )
    
    return fig


# ==================== Page Layouts ====================

def page_home():
    """Home page"""
    st.title("🔬 Influence Functions Explorer")
    st.markdown("""
    Welcome to the Influence Functions Microservice! This application allows you to:
    
    - **Create Experiments**: Run influence function calculation experiments on predefined datasets
    - **Configure Parameters**: Customize all aspects of your experiments
    - **Analyze Results**: Visualize influence weights and model performance metrics
    - **Compare Methods**: Compare different influence calculation methods
    
    ### Quick Start
    1. Go to **New Experiment** tab to create an experiment
    2. Select a dataset and configure parameters
    3. Choose influence methods to compute
    4. Wait for the experiment to complete
    5. Explore results in the **Analysis** tab
    """)
    
    # Show available datasets
    st.subheader("📊 Available Datasets")
    datasets = get_available_datasets()
    cols = st.columns(len(datasets) if datasets else 1)
    for i, dataset in enumerate(datasets):
        with cols[i]:
            st.info(f"✓ {dataset.upper()}")


def page_new_experiment():
    """New experiment page"""
    st.title("🚀 Create New Experiment")
    
    # Get available options first
    available_methods = get_available_methods()
    datasets = get_available_datasets()
    models = get_available_models()
    
    # Initialize session state for checkbox selections
    all_methods = [
        'LOO', 'DataShapley', 'BetaShapley', 'Banzhaf', 'TMCShapley', 'KNNShapley', 'DataOOB', 'LeastCore',
        'Influence', 'ArnoldiInfluence', 'CgInfluence', 'LissaInfluence', 'NystroemSketchInfluence'
    ]
    
    for method in all_methods:
        if f"method_{method}" not in st.session_state:
            st.session_state[f"method_{method}"] = False
    
    # Preset button selections (OUTSIDE the form)
    st.subheader("Quick Select Methods")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📌 Select All", key="select_all"):
            for method in all_methods:
                st.session_state[f"method_{method}"] = True
            st.rerun()
    with col2:
        if st.button("❌ Clear All", key="clear_all"):
            for method in all_methods:
                st.session_state[f"method_{method}"] = False
            st.rerun()
    with col3:
        if st.button("🔧 Fast Methods", key="fast_methods"):
            for method in all_methods:
                st.session_state[f"method_{method}"] = method in ["BetaShapley", "Banzhaf"]
            st.rerun()
    
    # Main form
    with st.form("experiment_form"):
        # Dataset selection
        st.subheader("1️⃣ Dataset Selection")
        selected_dataset = st.selectbox(
            "Choose Dataset",
            datasets,
            help="Select a built-in dataset for the experiment"
        )
        
        # Model selection
        st.subheader("2️⃣ Model Configuration")
        col1, col2 = st.columns(2)
        with col1:
            model_type = st.selectbox(
                "Model Type",
                models,
                help="Choose the machine learning model"
            )
        with col2:
            use_distillation = st.checkbox(
                "Use Distillation",
                value=False,
                help="Apply teacher-student distillation during training"
            )
        
        if use_distillation:
            distillation_epochs = st.slider(
                "Distillation Epochs",
                min_value=50,
                max_value=500,
                value=200,
                step=50
            )
        else:
            distillation_epochs = 200
        
        # Data configuration
        st.subheader("3️⃣ Data Configuration")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sample_size = st.slider(
                "Sample Size (%)",
                min_value=1,
                max_value=100,
                value=100,
                step=1,
                help="Percentage of data to use from the original dataset"
            )
        
        with col2:
            test_size = st.slider(
                "Test Size",
                min_value=0.1,
                max_value=0.5,
                value=0.2,
                step=0.01,
                help="Fraction of data for testing"
            )
        
        with col3:
            val_size = st.slider(
                "Validation Size",
                min_value=0.05,
                max_value=0.3,
                value=0.1,
                step=0.01,
                help="Fraction of data for validation"
            )
        
        # Training configuration
        st.subheader("4️⃣ Training Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            n_epochs = st.slider(
                "Number of Epochs",
                min_value=10,
                max_value=1000,
                value=500,
                step=1
            )
        
        with col2:
            n_random_runs = st.slider(
                "Random Removal Runs",
                min_value=1,
                max_value=10,
                value=3,
                help="Number of random removal experiments for baseline"
            )
        
        # Removal configuration
        st.subheader("5️⃣ Data Removal Configuration")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            removal_strategy = st.selectbox(
                "Removal Strategy",
                ["remove_lowest_influence", "remove_highest_influence"],
                help="How to select samples for removal"
            )
        
        with col2:
            removal_range = st.slider(
                "Removal Percentage Range",
                min_value=1,
                max_value=99,
                value=(1, 99),
                step=1,
                help="Range of removal percentages to test"
            )
        
        with col3:
            num_removal_percentages = st.number_input(
                "Number of Removal Percentages",
                min_value=2,
                max_value=100,
                value=20,
                step=1,
                help="How many removal percentages to test in the range"
            )
        
        # Generate removal percentages (convert numpy int to Python int for JSON serialization)
        n_remove_percentages = [int(x) for x in np.linspace(removal_range[0], removal_range[1], num_removal_percentages, dtype=int)]
        st.info(f"Will test {len(n_remove_percentages)} removal percentages: {n_remove_percentages[:5]}... (showing first 5)")
        
        # Influence methods (inside form)
        st.subheader("6️⃣ Selected Influence Methods")
        
        col1, col2 = st.columns(2)
        
        # List 1: Shapley-based methods
        shapley_methods = [
            'LOO',
            'DataShapley',
            'BetaShapley',
            'Banzhaf',
            'TMCShapley',
            'KNNShapley',
            'DataOOB',
            'LeastCore'
        ]
        
        # List 2: Influence methods
        influence_methods = [
            'Influence',
            'ArnoldiInfluence',
            'CgInfluence',
            'LissaInfluence',
            'NystroemSketchInfluence'
        ]
        
        selected_methods = []
        
        with col1:
            st.write("**Shapley-Based Methods**")
            for method in shapley_methods:
                if st.checkbox(method, value=st.session_state.get(f"method_{method}", False), key=f"form_method_{method}"):
                    selected_methods.append(method)
        
        with col2:
            st.write("**Influence Methods**")
            for method in influence_methods:
                if st.checkbox(method, value=st.session_state.get(f"method_{method}", False), key=f"form_method_{method}"):
                    selected_methods.append(method)
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            col1, col2 = st.columns(2)
            with col1:
                random_state = st.number_input(
                    "Random State",
                    min_value=0,
                    max_value=10000,
                    value=39
                )
            with col2:
                debug_mode = st.checkbox("Debug Mode", value=False)
        
        # Submit buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button(
                "🚀 Start Experiment",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            validate_button = st.form_submit_button(
                "📋 Validate Config",
                use_container_width=True
            )
        
        if validate_button:
            # Save method selections to session state
            for method in all_methods:
                st.session_state[f"method_{method}"] = method in selected_methods
            st.success("✓ Configuration is valid!")
        
        if submit_button:
            # Save method selections to session state
            for method in all_methods:
                st.session_state[f"method_{method}"] = method in selected_methods
            
            # Prepare config
            config = {
                "dataset_name": selected_dataset,
                "model_type": model_type,
                "removal_strategy": removal_strategy,
                "n_remove_percentages": n_remove_percentages,
                "sample_size_percentage": sample_size,
                "test_size": test_size,
                "val_size": val_size,
                "n_epochs": n_epochs,
                "n_random_runs": n_random_runs,
                "selected_influence_methods": selected_methods,
                "use_distillation": use_distillation,
                "distillation_epochs": distillation_epochs,
                "random_state": random_state,
                "debug_mode": debug_mode
            }
            
            # Start experiment
            with st.spinner("🔄 Starting experiment..."):
                response = make_api_request(
                    "POST",
                    "/experiments/start",
                    {"config": config}
                )
            
            if response:
                experiment_id = response.get('experiment_id')
                st.session_state.current_experiment_id = experiment_id
                st.success(f"✓ Experiment started!\nID: {experiment_id}")
                
                # Poll status
                st.info("⏳ Waiting for experiment to complete...")
                status = poll_experiment_status(experiment_id)
                
                if status and status.get('status') == 'completed':
                    st.success("✓ Experiment completed!")
                    st.balloons()
                    
                    # Save to session for analysis
                    st.session_state.last_experiment_id = experiment_id
                    time.sleep(1)
                    st.rerun()


def page_analysis():
    """Analysis page"""
    st.title("📊 Experiment Analysis")
    
    # Get list of experiments
    response = make_api_request("GET", "/experiments")
    if not response or not response.get('experiments'):
        st.info("No experiments found. Create a new experiment first!")
        return
    
    experiments = response.get('experiments', [])
    
    # Experiment selector
    exp_options = [f"{e['experiment_id'][:8]}... ({e.get('dataset')}) - {e.get('created_at', '')[:10]}" 
                   for e in experiments]
    exp_ids = [e['experiment_id'] for e in experiments]
    
    selected_idx = st.selectbox("Select Experiment", range(len(exp_options)), 
                                format_func=lambda i: exp_options[i])
    selected_exp_id = exp_ids[selected_idx]
    
    # Load experiment results
    with st.spinner("📥 Loading experiment results..."):
        results_response = make_api_request("GET", f"/experiments/{selected_exp_id}/results")
    
    if not results_response:
        st.error("Failed to load experiment results")
        return
    
    # Display basic info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Dataset", results_response.get('config', {}).get('dataset_name', 'N/A'))
    with col2:
        st.metric("Model", results_response.get('config', {}).get('model_type', 'N/A'))
    with col3:
        st.metric("Samples", results_response.get('samples_count', 'N/A'))
    with col4:
        exec_time = results_response.get('execution_time', 0)
        st.metric("Execution Time", f"{exec_time:.1f}s")
    
    # Path to experiment plots (from main-style logger)
    experiment_dir = results_response.get('experiment_dir') or results_response.get('config', {}).get('experiment_dir')
    
    # Tabs for different analysis views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Influence Distribution",
        "🎯 Performance Metrics",
        "📉 Removal Impact",
        "🔍 Raw Scores"
    ])
    
    # Get available methods
    available_methods = results_response.get('influence_methods', [])
    
    with tab1:
        st.subheader("Influence Weights Distribution")
        
        if available_methods:
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_method = st.selectbox(
                    "Select Method",
                    available_methods,
                    key="dist_method"
                )
            
            with col1:
                with st.spinner(f"📥 Loading {selected_method} weights..."):
                    weights_response = load_influence_weights(selected_exp_id, selected_method)
                
                if weights_response:
                    weights = weights_response.get('weights', [])
                    stats = weights_response.get('statistics', {})
                    # If matplotlib PNG exists (saved by main logger), show it first
                    try:
                        if experiment_dir:
                            import os
                            img_path = os.path.join(experiment_dir, f"influence_distribution_influence_scores.png")
                            if os.path.exists(img_path):
                                st.image(img_path, use_column_width=True)
                    except Exception:
                        pass
                    
                    # Display statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Min", f"{stats.get('min', 0):.4f}")
                    with col2:
                        st.metric("Max", f"{stats.get('max', 0):.4f}")
                    with col3:
                        st.metric("Mean", f"{stats.get('mean', 0):.4f}")
                    with col4:
                        st.metric("Std Dev", f"{stats.get('std', 0):.4f}")
                    
                    # Prefer saved PNG (from main-style logger) or matplotlib visualization
                    try:
                        # Try to render using shared visualization functions (matplotlib)
                        scores_dict = {selected_method: np.array(weights)}
                        plt_obj = viz_plot_influence_distribution(scores_dict, plot_name_suffix=selected_method)
                        st.pyplot(plt_obj)
                    except Exception:
                        # Fallback to local interactive Plotly histogram
                        fig = _local_plot_influence_distribution(weights, selected_method)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Failed to load influence weights")
        else:
            st.warning("No influence methods computed for this experiment")
    
    with tab2:
        st.subheader("Performance Metrics")
        
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.info("Baseline Performance (No Data Removal)")
            st.json({
                "model": results_response.get('config', {}).get('model_type'),
                "samples": results_response.get('samples_count'),
            })
        
        with metric_col2:
            st.info("Removal Configuration")
            st.json({
                "strategy": results_response.get('config', {}).get('removal_strategy'),
                "percentages_tested": len(results_response.get('config', {}).get('n_remove_percentages', []))
            })
    
    with tab3:
        st.subheader("Model Performance vs Data Removal")
        st.info("Graphical comparison of model performance across different removal percentages")
        
        # Load graph data
        with st.spinner("📥 Loading experiment results..."):
            graph_data_response = load_graph_data(selected_exp_id)
        
        if graph_data_response and graph_data_response.get('removal_data'):
            removal_data = graph_data_response.get('removal_data', {})

            # Prefer to show the matplotlib results image saved by the main logger
            experiment_dir = results_response.get('experiment_dir') or results_response.get('config', {}).get('experiment_dir')
            shown = False

            if experiment_dir:
                try:
                    import os
                    import pickle

                    # First try PNG saved by logger
                    png_path = os.path.join(experiment_dir, "results_comparison.png")
                    if os.path.exists(png_path):
                        st.image(png_path, use_column_width=True)
                        shown = True
                    else:
                        # Try to load results.pkl and render with shared matplotlib function
                        pkl_path = os.path.join(experiment_dir, "results.pkl")
                        if os.path.exists(pkl_path):
                            with open(pkl_path, 'rb') as f:
                                data = pickle.load(f)
                            results_full = data.get('results', {})
                            n_remove_list = data.get('n_remove_list', [])
                            random_run_results = data.get('random_run_results', None)
                            try:
                                plt_obj = viz_plot_results_enhanced(
                                    results_full, 
                                    n_remove_list, 
                                    logger=None, 
                                    random_run_results=random_run_results
                                )
                                st.pyplot(plt_obj)
                                shown = True
                            except Exception as e:
                                st.error(f"Error rendering plot: {str(e)}")
                                shown = False
                except Exception:
                    shown = False

            if not shown:
                if available_methods:
                    # Allow user to select methods for comparison
                    methods_to_compare = st.multiselect(
                        "Methods to Compare",
                        list(removal_data.keys()),
                        default=list(removal_data.keys())[:min(3, len(removal_data))],
                        key="compare_methods"
                    )

                    if methods_to_compare:
                        # Filter removal data for selected methods
                        filtered_removal_data = {m: removal_data[m] for m in methods_to_compare if m in removal_data}

                        if filtered_removal_data:
                            fig = plot_removal_impact(filtered_removal_data)
                            st.plotly_chart(fig, use_container_width=True)

                            # Show detailed metrics
                            with st.expander("📊 Detailed Results"):
                                for method, data_points in filtered_removal_data.items():
                                    st.subheader(f"📈 {method}")

                                    df = pd.DataFrame(data_points)
                                    st.dataframe(df, use_container_width=True)
                        else:
                            st.warning("No data available for selected methods")
                else:
                    st.warning("No methods available for comparison")
        else:
            st.warning("No removal impact data available. Experiment may still be running or failed.")
    
    with tab4:
        st.subheader("Raw Influence Scores")

        if available_methods:
            selected_method = st.selectbox(
                "Select Method",
                available_methods,
                key="raw_method"
            )

            with st.spinner(f"📥 Loading scores..."):
                weights_response = load_influence_weights(selected_exp_id, selected_method)

            if weights_response:
                weights = np.array(weights_response.get('weights', []))

                # Create dataframe
                df = pd.DataFrame({
                    'Sample Index': range(len(weights)),
                    'Influence Score': weights,
                    'Rank': pd.Series(weights).rank(ascending=False).astype(int)
                })

                # Add ranking colors
                top_n = st.slider("Highlight Top N", min_value=1, max_value=20, value=10)

                st.dataframe(
                    df.sort_values('Influence Score', ascending=False).head(top_n),
                    use_container_width=True,
                    height=400
                )

                # Download option
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download Scores CSV",
                    csv,
                    f"influence_scores_{selected_exp_id[:8]}.csv",
                    "text/csv"
                )
            else:
                st.error("Failed to load influence weights")
        else:
            st.warning("No methods available for comparison")

def page_compare():
    """Comparison page"""
    st.title("🔄 Compare Experiments")
    
    st.info("Compare multiple experiments side-by-side to see the impact of different configurations")
    
    # Get experiments
    response = make_api_request("GET", "/experiments")
    if not response or not response.get('experiments'):
        st.warning("No experiments found")
        return
    
    experiments = response.get('experiments', [])
    exp_options = [f"{e['experiment_id'][:8]}... ({e.get('dataset')}) - {e.get('created_at', '')[:10]}" 
                   for e in experiments]
    exp_ids = [e['experiment_id'] for e in experiments]
    
    # Select experiments to compare
    selected_indices = st.multiselect(
        "Select Experiments to Compare",
        range(len(exp_options)),
        format_func=lambda i: exp_options[i],
        default=list(range(min(2, len(exp_options))))
    )
    
    if len(selected_indices) < 2:
        st.warning("Please select at least 2 experiments to compare")
        return
    
    selected_exp_ids = [exp_ids[i] for i in selected_indices]
    
    # Load results for comparison
    comparison_data = []
    
    for exp_id in selected_exp_ids:
        with st.spinner(f"Loading {exp_id[:8]}..."):
            results = make_api_request("GET", f"/experiments/{exp_id}/results")
            if results:
                comparison_data.append({
                    'exp_id': exp_id,
                    'dataset': results.get('config', {}).get('dataset_name'),
                    'model': results.get('config', {}).get('model_type'),
                    'samples': results.get('samples_count'),
                    'methods': len(results.get('influence_methods', []))
                })
    
    # Display comparison table
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Comparison visualizations
        st.subheader("Configuration Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            st.bar_chart(comparison_df.set_index('exp_id')[['samples']])
        
        with col2:
            st.bar_chart(comparison_df.set_index('exp_id')[['methods']])


def page_settings():
    """Settings page"""
    st.title("⚙️ Application Settings")
    
    with st.form("settings_form"):
        st.subheader("API Configuration")
        api_url = st.text_input(
            "API Base URL",
            value=API_BASE_URL,
            help="URL of the FastAPI backend"
        )
        
        poll_interval = st.slider(
            "Status Poll Interval (seconds)",
            min_value=1,
            max_value=10,
            value=2,
            help="How often to check experiment status"
        )
        
        st.subheader("Storage Settings")
        max_experiments = st.number_input(
            "Max Experiments to Keep",
            min_value=10,
            max_value=1000,
            value=100,
            help="Maximum number of experiments to store"
        )
        
        st.subheader("Display Settings")
        theme_options = ["light", "dark", "auto"]
        theme_index = theme_options.index("auto") if "auto" in theme_options else 0
        theme = st.selectbox(
            "Theme",
            theme_options,
            index=theme_index,
            help="Select display theme"
        )
        
        if st.form_submit_button("💾 Save Settings"):
            st.success("✓ Settings saved! (Note: API URL requires server restart)")


# ==================== Main App ====================

def main():
    """Main application"""
    
    # Initialize session state
    if 'selected_methods' not in st.session_state:
        st.session_state.selected_methods = []
    if 'current_experiment_id' not in st.session_state:
        st.session_state.current_experiment_id = None
    
    # Sidebar navigation
    st.sidebar.title("🔬 Influence Functions")
    
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "🚀 New Experiment", "📊 Analysis", "🔄 Compare", "⚙️ Settings"],
        key="main_nav"
    )
    
    st.sidebar.markdown("---")
    
    # API status
    health_response = make_api_request("GET", "/health")
    if health_response:
        st.sidebar.success("✓ API Connected")
    else:
        st.sidebar.error("✗ API Disconnected")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("v1.0.0 - Microservice Edition")
    
    # Route pages
    if page == "🏠 Home":
        page_home()
    elif page == "🚀 New Experiment":
        page_new_experiment()
    elif page == "📊 Analysis":
        page_analysis()
    elif page == "🔄 Compare":
        page_compare()
    elif page == "⚙️ Settings":
        page_settings()


if __name__ == "__main__":
    main()
