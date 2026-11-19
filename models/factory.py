from .tree_models import LightGBMModel, XGBoostModel, RandomForestModel, CatBoostModel
from .torch_models import (
    PyTorchModelWrapper,
    DistilledModelWrapper,
    DEFAULT_CNN_SMALL_PARAMS,
)
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
        student_architecture = model_params.get('student_architecture', model_architecture)
        use_distillation = model_params.get('use_distillation', False)
        distillation_epochs = model_params.get('distillation_epochs', 50)
        temperature = model_params.get('temperature', 2.0)
        task_type = model_params.get('task_type', 'regression')

        # Extracting model-specific parameters (those that are not generic params)
        # These will be passed to model constructors
        model_specific_params = ModelFactory._extract_model_params(model_params, model_type)
        tree_kwargs = {'task_type': task_type}

        num_classes = model_params.get('num_class', 1)

        if model_type == 'lightgbm':
            if use_distillation:
                base_model = LightGBMModel(params=model_specific_params, **tree_kwargs)
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(
                    base_model,
                    input_size,
                    device,
                    student_architecture,
                    distillation_epochs,
                    temperature=temperature,
                    num_classes=num_classes,
                    task_type=task_type,
                    batch_size=model_params.get('batch_size'),
                )
            return LightGBMModel(params=model_specific_params, **tree_kwargs)
        elif model_type == 'xgboost':
            if use_distillation:
                base_model = XGBoostModel(params=model_specific_params, **tree_kwargs)
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(
                    base_model,
                    input_size,
                    device,
                    student_architecture,
                    distillation_epochs,
                    temperature=temperature,
                    num_classes=num_classes,
                    task_type=task_type,
                    batch_size=model_params.get('batch_size'),
                )
            return XGBoostModel(params=model_specific_params, **tree_kwargs)
        elif model_type == 'random_forest':
            if use_distillation:
                base_model = RandomForestModel(params=model_specific_params, **tree_kwargs)
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(
                    base_model,
                    input_size,
                    device,
                    student_architecture,
                    distillation_epochs,
                    temperature=temperature,
                    num_classes=num_classes,
                    task_type=task_type,
                    batch_size=model_params.get('batch_size'),
                )
            return RandomForestModel(params=model_specific_params, **tree_kwargs)
        elif model_type == 'catboost':
            if use_distillation:
                base_model = CatBoostModel(params=model_specific_params, **tree_kwargs)
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(
                    base_model,
                    input_size,
                    device,
                    student_architecture,
                    distillation_epochs,
                    temperature=temperature,
                    num_classes=num_classes,
                    task_type=task_type,
                    batch_size=model_params.get('batch_size'),
                )
            return CatBoostModel(params=model_specific_params, **tree_kwargs)
        elif model_type == 'pytorch':
            if input_size is None:
                raise ValueError("Для PyTorch модели требуется input_size")
            if model_architecture == 'cnn_small' and input_size not in (3072, 784):
                raise ValueError(
                    "Архитектура cnn_small поддерживает только вход размера 3072 (CIFAR-10) "
                    f"или 784 (MNIST), получено input_size={input_size}"
                )
            arch_config = model_params.get(model_architecture)
            if model_architecture == 'cnn_small':
                if isinstance(arch_config, dict):
                    torch_kwargs = dict(arch_config)
                else:
                    torch_kwargs = dict(DEFAULT_CNN_SMALL_PARAMS)
            elif isinstance(arch_config, dict):
                torch_kwargs = dict(arch_config)
            else:
                torch_kwargs = {}
            if task_type == 'multiclass_classification':
                nc = model_params.get('num_class')
                if nc is not None:
                    torch_kwargs['num_classes'] = int(nc)
            if task_type == 'binary_classification' and model_params.get('pos_weight') is not None:
                torch_kwargs['pos_weight'] = model_params['pos_weight']
            # [AUDIT-FIX B1] Сколько full-batch эпох делает fit(X, y) «с нуля» (так обучают
            # модель pyDVL-методы на подмножествах) и seed переинициализации — для воспроизводимости.
            from config.settings import EXPERIMENT_CONFIG, RANDOM_STATE
            torch_kwargs.setdefault(
                'default_epochs',
                int(model_params.get('valuation_epochs') or EXPERIMENT_CONFIG.get('valuation_epochs', 200)),
            )
            torch_kwargs.setdefault('refit_seed', RANDOM_STATE)
            if model_params.get('batch_size'):      # [AUDIT-FIX B11] mini-batch epochs (None = legacy)
                torch_kwargs.setdefault('batch_size', int(model_params['batch_size']))
            return PyTorchModelWrapper(
                input_size,
                device=device,
                model_architecture=model_architecture,
                task_type=task_type,
                **torch_kwargs
            )
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
            'student_architecture', 'available_metrics', 'num_class',
            # передаются в DistilledModelWrapper.fit(), не в конструкторы деревьев
            'distillation_patience', 'distillation_min_delta',
            # [AUDIT-FIX D3] torch-only / experiment keys: CatBoost and sklearn RandomForest reject unknown
            # constructor kwargs (TypeError), LightGBM / XGBoost only warn
            'valuation_epochs', 'pos_weight', 'num_classes', 'batch_size',
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
        nc = model_params.get('num_class')
        # LightGBM / XGBoost multiclass берут num_class из params (см. датасет-конфиги).
        if nc is not None and model_type in ('lightgbm', 'xgboost'):
            try:
                specific_params['num_class'] = int(nc)
            except (TypeError, ValueError):
                pass
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
