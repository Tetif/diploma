from .tree_models import LightGBMModel, XGBoostModel, RandomForestModel, CatBoostModel
from .torch_models import PyTorchModelWrapper, DistilledModelWrapper
from config.settings import DEVICE


class ModelFactory:
    """Фабрика для создания моделей"""

    @staticmethod
    def create_model(model_params=None, **kwargs):
        """Создает модель на основе параметров"""
        # Поддержка как словаря model_params, так и отдельных параметров
        if model_params is None:
            model_params = kwargs
        elif isinstance(model_params, dict):
            # Объединяем model_params и kwargs, kwargs имеет приоритет
            params = model_params.copy()
            params.update(kwargs)
            model_params = params
        else:
            # Если передан не словарь, используем kwargs
            model_params = kwargs if kwargs else {'model_type': 'pytorch'}

        model_type = model_params.get('model_type', 'pytorch')
        input_size = model_params.get('input_size')
        device = model_params.get('device', DEVICE)
        model_architecture = model_params.get('model_architecture', 'simple')
        use_distillation = model_params.get('use_distillation', False)
        distillation_epochs = model_params.get('distillation_epochs', 50)
        task_type = model_params.get('task_type', 'regression')

        # Extracting model-specific parameters (those that are not generic params)
        # These will be passed to model constructors
        model_specific_params = ModelFactory._extract_model_params(model_params, model_type)
        tree_kwargs = {'task_type': task_type}

        if model_type == 'lightgbm':
            if use_distillation:
                base_model = LightGBMModel(params=model_specific_params, **tree_kwargs)
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(base_model, input_size, device, model_architecture, distillation_epochs)
            return LightGBMModel(params=model_specific_params, **tree_kwargs)
        elif model_type == 'xgboost':
            if use_distillation:
                base_model = XGBoostModel(params=model_specific_params, **tree_kwargs)
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(base_model, input_size, device, model_architecture, distillation_epochs)
            return XGBoostModel(params=model_specific_params, **tree_kwargs)
        elif model_type == 'random_forest':
            if use_distillation:
                base_model = RandomForestModel(params=model_specific_params, **tree_kwargs)
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(base_model, input_size, device, model_architecture, distillation_epochs)
            return RandomForestModel(params=model_specific_params, **tree_kwargs)
        elif model_type == 'catboost':
            if use_distillation:
                base_model = CatBoostModel(params=model_specific_params, **tree_kwargs)
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(base_model, input_size, device, model_architecture, distillation_epochs)
            return CatBoostModel(params=model_specific_params, **tree_kwargs)
        elif model_type == 'pytorch':
            if input_size is None:
                raise ValueError("Для PyTorch модели требуется input_size")
            return PyTorchModelWrapper(input_size, device=device, model_architecture=model_architecture, task_type=task_type)
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

    @staticmethod
    def _extract_model_params(model_params, model_type):
        """Extract model-specific params from the full parameter dict"""
        # These are generic parameter keys that should never be passed to model constructors
        generic_keys = {
            'model_type', 'input_size', 'device', 'model_architecture',
            'use_distillation', 'distillation_epochs', 'task_type',
            'removal_strategy', 'sample_size_percentage', 'temperature',
            'student_architecture'  # Added student_architecture
        }
        
        # For tree-based models, also exclude PyTorch-specific params
        if model_type in ['lightgbm', 'xgboost', 'catboost', 'random_forest']:
            tree_exclude = {
                'layers', 'dropout', 'batch_norm', 'learning_rate', 'd_model',
                'nhead', 'num_layers', 'dim_feedforward'
            }
            generic_keys.update(tree_exclude)
        
        # For PyTorch models, exclude tree-based params
        elif model_type == 'pytorch':
            torch_exclude = {
                'num_leaves', 'bagging_fraction', 'bagging_freq', 'min_data_in_leaf',
                'feature_fraction', 'max_depth', 'min_child_weight', 'subsample',
                'colsample_bytree', 'gamma', 'n_estimators', 'min_samples_split',
                'min_samples_leaf', 'iterations'
            }
            generic_keys.update(torch_exclude)
        
        # Create dict with all model params except generic/irrelevant ones
        specific_params = {k: v for k, v in model_params.items() 
                          if k not in generic_keys}
        return specific_params

    @staticmethod
    def get_available_models():
        """Возвращает список доступных моделей"""
        return ['lightgbm', 'xgboost', 'random_forest', 'catboost', 'pytorch']

    @staticmethod
    def get_model_config(model_type, dataset_name=None):
        """
        Возвращает конфигурацию для модели.
        Для конфига по датасету и типу модели используйте config.settings.get_model_config(dataset_name, model_type).
        """
        if dataset_name is not None:
            from config.settings import get_model_config as settings_get_model_config
            return settings_get_model_config(dataset_name, model_type)
        return {}