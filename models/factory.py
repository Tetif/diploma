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

        if model_type == 'lightgbm':
            if use_distillation:
                base_model = LightGBMModel()
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(base_model, input_size, device, model_architecture, distillation_epochs)
            return LightGBMModel()
        elif model_type == 'xgboost':
            if use_distillation:
                base_model = XGBoostModel()
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(base_model, input_size, device, model_architecture, distillation_epochs)
            return XGBoostModel()
        elif model_type == 'random_forest':
            if use_distillation:
                base_model = RandomForestModel()
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(base_model, input_size, device, model_architecture, distillation_epochs)
            return RandomForestModel()
        elif model_type == 'catboost':
            if use_distillation:
                base_model = CatBoostModel()
                if input_size is None:
                    raise ValueError("Для дистиллированной модели требуется input_size")
                return DistilledModelWrapper(base_model, input_size, device, model_architecture, distillation_epochs)
            return CatBoostModel()
        elif model_type == 'pytorch':
            if input_size is None:
                raise ValueError("Для PyTorch модели требуется input_size")
            return PyTorchModelWrapper(input_size, device=device, model_architecture=model_architecture)
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

    @staticmethod
    def get_available_models():
        """Возвращает список доступных моделей"""
        return ['lightgbm', 'xgboost', 'random_forest', 'catboost', 'pytorch']