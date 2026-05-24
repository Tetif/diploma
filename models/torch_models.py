import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from .base import BaseModel
from config.settings import DEVICE

# Default PyTorch model configurations
DEFAULT_PYTORCH_PARAMS = {
    'simple': {
        'layers': [32, 16, 8],
        'dropout': 0.2,
        'learning_rate': 0.001
    },
    'improved': {
        'layers': [64, 32, 16, 8],
        'batch_norm': True,
        'dropout': [0.2, 0.15, 0.1],
        'learning_rate': 0.001
    },
    'ft_transformer': {
        'd_model': 16,
        'nhead': 4,
        'num_layers': 2,
        'dim_feedforward': 64,
        'dropout': 0.1,
        'learning_rate': 0.001
    },
    'ft_transformer_simple': {
        'd_model': 8,
        'nhead': 2,
        'num_layers': 1,
        'dim_feedforward': 32,
        'dropout': 0.1,
        'learning_rate': 0.001
    },
    'cnn_small': {
        'dropout': 0.25,
        'base_channels': 32,
        'learning_rate': 0.001,
    },
}

# Used by ModelFactory when a dataset config has no nested cnn_small block.
DEFAULT_CNN_SMALL_PARAMS = DEFAULT_PYTORCH_PARAMS['cnn_small'].copy()


class SimpleNN(nn.Module):
    def __init__(self, input_size, layers=None, dropout=0.2, output_size=1):
        super(SimpleNN, self).__init__()
        if layers is None:
            layers = DEFAULT_PYTORCH_PARAMS['simple']['layers']

        modules = []
        prev_size = input_size

        for i, layer_size in enumerate(layers):
            modules.append(nn.Linear(prev_size, layer_size))
            modules.append(nn.ReLU())
            if dropout > 0:
                modules.append(nn.Dropout(dropout))
            prev_size = layer_size

        modules.append(nn.Linear(prev_size, output_size))

        self.network = nn.Sequential(*modules)

    def forward(self, x):
        return self.network(x)


class ImprovedNN(nn.Module):
    def __init__(self, input_size, layers=None, dropout=None, batch_norm=True, output_size=1):
        super(ImprovedNN, self).__init__()
        if layers is None:
            layers = DEFAULT_PYTORCH_PARAMS['improved']['layers']
        if dropout is None:
            dropout = DEFAULT_PYTORCH_PARAMS['improved']['dropout']

        modules = []
        prev_size = input_size

        for i, layer_size in enumerate(layers):
            modules.append(nn.Linear(prev_size, layer_size))

            if batch_norm:
                modules.append(nn.BatchNorm1d(layer_size))

            modules.append(nn.ReLU())

            if dropout and i < len(dropout):
                modules.append(nn.Dropout(dropout[i]))

            prev_size = layer_size

        modules.append(nn.Linear(prev_size, output_size))

        self.network = nn.Sequential(*modules)

    def forward(self, x):
        return self.network(x)


class SmallImageCNN(nn.Module):
    """Compact CNN for flattened CIFAR-10 (3072) or MNIST (784)."""

    def __init__(self, input_size, num_classes=10, dropout=0.25, base_channels=32):
        super().__init__()
        if input_size == 3072:
            self.c, self.h, self.w = 3, 32, 32
        elif input_size == 784:
            self.c, self.h, self.w = 1, 28, 28
        else:
            raise ValueError(
                f"SmallImageCNN supports input_size 3072 (CIFAR-10) or 784 (MNIST), got {input_size}"
            )
        ch1 = int(base_channels)
        ch2 = ch1 * 2
        d = float(dropout)
        self.features = nn.Sequential(
            nn.Conv2d(self.c, ch1, kernel_size=3, padding=1),
            nn.BatchNorm2d(ch1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout2d(d) if d > 0 else nn.Identity(),
            nn.Conv2d(ch1, ch2, kernel_size=3, padding=1),
            nn.BatchNorm2d(ch2),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout2d(d) if d > 0 else nn.Identity(),
            nn.Conv2d(ch2, ch2, kernel_size=3, padding=1),
            nn.BatchNorm2d(ch2),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.fc = nn.Linear(ch2, int(num_classes))

    def forward(self, x):
        x = x.view(x.size(0), self.c, self.h, self.w)
        x = self.features(x)
        x = x.flatten(1)
        return self.fc(x)


class SimpleFTTransformer(nn.Module):
    def __init__(self, input_size, **kwargs):
        super().__init__()
        config = DEFAULT_PYTORCH_PARAMS['ft_transformer_simple'].copy()
        config.update(kwargs)

        self.d_model = config['d_model']
        num_classes = int(config.get('num_classes', 1))
        self.input_projection = nn.Linear(input_size, self.d_model)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.d_model,
            nhead=config['nhead'],
            dim_feedforward=config['dim_feedforward'],
            dropout=config['dropout'],
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=config['num_layers'])
        self.output_layer = nn.Linear(self.d_model, num_classes)

    def forward(self, x):
        x = self.input_projection(x)
        x = x.unsqueeze(1)
        x = self.transformer_encoder(x)
        x = x.squeeze(1)
        x = self.output_layer(x)
        return x


class PyTorchModelWrapper(BaseModel):
    """Обертка для PyTorch моделей для совместимости.
    Регрессия (MSELoss), бинарная классификация (BCEWithLogitsLoss),
    многоклассовая классификация (CrossEntropyLoss, K логитов).
    """

    def __init__(self, input_size, model_architecture='simple', device=DEVICE, task_type='regression', pos_weight=None, **kwargs):
        super().__init__()
        self.input_size = input_size
        self.device = device
        self.model_architecture = model_architecture
        self.task_type = task_type

        learning_rate = kwargs.pop('learning_rate', 0.001)
        num_classes_kw = kwargs.pop('num_classes', None)
        if num_classes_kw is None:
            num_classes_kw = kwargs.pop('num_class', None)

        if task_type == 'multiclass_classification':
            if num_classes_kw is None:
                raise ValueError(
                    "multiclass_classification requires num_classes or num_class for PyTorchModelWrapper"
                )
            out_dim = int(num_classes_kw)
            self.num_classes = out_dim
        else:
            out_dim = 1
            self.num_classes = None

        if model_architecture == 'cnn_small':
            dropout = float(kwargs.pop('dropout', DEFAULT_CNN_SMALL_PARAMS['dropout']))
            base_channels = int(kwargs.pop('base_channels', DEFAULT_CNN_SMALL_PARAMS['base_channels']))
            self.model = SmallImageCNN(
                input_size, num_classes=out_dim, dropout=dropout, base_channels=base_channels
            ).to(device)
        elif model_architecture == 'improved':
            kwargs['output_size'] = out_dim
            self.model = ImprovedNN(input_size, **kwargs).to(device)
        elif model_architecture == 'ft_transformer':
            kwargs['num_classes'] = out_dim
            self.model = SimpleFTTransformer(input_size, **kwargs).to(device)
        elif model_architecture == 'ft_transformer_simple':
            kwargs['num_classes'] = out_dim
            self.model = SimpleFTTransformer(input_size, **kwargs).to(device)
        else:
            kwargs['output_size'] = out_dim
            self.model = SimpleNN(input_size, **kwargs).to(device)

        self.optimizer = optim.AdamW(
            self.model.parameters(),
            lr=learning_rate,
            weight_decay=1e-4
        )
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='min', factor=0.5, patience=10
        )
        if task_type == 'binary_classification':
            pw = None
            if pos_weight is not None:
                pw = torch.tensor([float(pos_weight)], device=device)
            self.criterion = nn.BCEWithLogitsLoss(pos_weight=pw)
        elif task_type == 'multiclass_classification':
            self.criterion = nn.CrossEntropyLoss()
        else:
            self.criterion = nn.MSELoss()
        self.val_losses_for_scheduler = []

    def fit(self, X, y, epochs=5, **kwargs):
        X_tensor = torch.FloatTensor(X).to(self.device)
        self.model.train()
        total_loss = 0
        if self.task_type == 'multiclass_classification':
            y_tensor = torch.LongTensor(np.asarray(y).astype(np.int64).ravel()).to(self.device)
            for _ in range(epochs):
                self.optimizer.zero_grad()
                output = self.model(X_tensor)
                loss = self.criterion(output, y_tensor)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
        else:
            y_tensor = torch.FloatTensor(y).reshape(-1, 1).to(self.device)
            for _ in range(epochs):
                self.optimizer.zero_grad()
                output = self.model(X_tensor)
                loss = self.criterion(output, y_tensor)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
        return total_loss / epochs

    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            out = self.model(X_tensor)
            if self.task_type == 'binary_classification':
                out = torch.sigmoid(out)
                return out.cpu().numpy().flatten()
            if self.task_type == 'multiclass_classification':
                return out.cpu().numpy()
            return out.cpu().numpy().flatten()

    def predict_proba(self, X):
        """Вероятности классов: binary — [P(0), P(1)]; multiclass — softmax."""
        self.model.eval()
        with torch.no_grad():
            if self.task_type == 'binary_classification':
                p1 = torch.sigmoid(self.model(torch.FloatTensor(X).to(self.device))).cpu().numpy().ravel()
                p1 = np.clip(p1, 1e-15, 1.0 - 1e-15)
                return np.column_stack([1.0 - p1, p1])
            if self.task_type == 'multiclass_classification':
                logits = self.model(torch.FloatTensor(X).to(self.device))
                return torch.softmax(logits, dim=1).cpu().numpy()
        raise AttributeError(
            f"predict_proba is not defined for task_type={self.task_type!r}"
        )

    def named_parameters(self):
        return self.model.named_parameters()

    def get_params(self, deep=True):
        """Возвращает параметры модели (совместимость с sklearn)"""
        return {
            'input_size': self.input_size,
            'model_architecture': self.model_architecture,
            'device': self.device
        }

    def set_params(self, **params):
        if 'model_architecture' in params:
            self.model_architecture = params['model_architecture']
        if 'device' in params:
            self.device = params['device']
        return self


class DistilledModelWrapper(BaseModel):
    """Обертка для дистилляции не-нейросетевых моделей в нейросеть"""

    def __init__(self, base_model, input_size, device='cpu', model_architecture='simple',
                 distillation_epochs=50, temperature=2.0, num_classes=1, task_type='regression'):
        super().__init__()
        self.base_model = base_model
        self.input_size = input_size
        self.device = device
        self.model_architecture = model_architecture
        self.distillation_epochs = distillation_epochs
        self.temperature = temperature
        self.num_classes = num_classes
        self.task_type = task_type
        self.is_distilled = False

        if model_architecture == 'improved':
            self.student_model = ImprovedNN(input_size, output_size=num_classes).to(device)
        elif model_architecture == 'cnn_small':
            self.student_model = SmallImageCNN(
                input_size, num_classes=num_classes, dropout=DEFAULT_CNN_SMALL_PARAMS['dropout'],
                base_channels=DEFAULT_CNN_SMALL_PARAMS['base_channels']
            ).to(device)
        else:
            self.student_model = SimpleNN(input_size, output_size=num_classes).to(device)

        self.optimizer = optim.Adam(self.student_model.parameters(),
                                    lr=DEFAULT_PYTORCH_PARAMS['simple']['learning_rate'])
        if task_type == 'binary_classification':
            self.criterion = nn.BCEWithLogitsLoss()
        elif task_type == 'multiclass_classification':
            self.criterion = nn.CrossEntropyLoss()
        else:
            self.criterion = nn.MSELoss()

    @staticmethod
    def _safe_probs(proba):
        arr = np.asarray(proba, dtype=np.float32)
        if arr.ndim == 1:
            arr = np.stack([1.0 - arr, arr], axis=1)
        row_sums = np.sum(arr, axis=1, keepdims=True)
        row_sums = np.clip(row_sums, 1e-12, None)
        arr = arr / row_sums
        return np.clip(arr, 1e-6, 1.0 - 1e-6)

    def _teacher_targets(self, X):
        if self.task_type == 'multiclass_classification':
            if hasattr(self.base_model, 'predict_proba'):
                return self._safe_probs(self.base_model.predict_proba(X))
            raw = np.asarray(self.base_model.predict(X))
            # LightGBM multiclass: predict даёт матрицу (N, C), не индексы классов.
            if raw.ndim == 2 and raw.shape[1] > 1:
                return self._safe_probs(raw)
            preds = raw.reshape(-1)
            idx = preds.astype(np.int64)
            idx = np.clip(idx, 0, max(int(self.num_classes) - 1, 0))
            one_hot = np.zeros((len(idx), int(self.num_classes)), dtype=np.float32)
            one_hot[np.arange(len(idx)), idx] = 1.0
            return one_hot

        if self.task_type == 'binary_classification':
            if hasattr(self.base_model, 'predict_proba'):
                probs = np.asarray(self.base_model.predict_proba(X))
                if probs.ndim == 2 and probs.shape[1] >= 2:
                    return np.clip(probs[:, 1], 1e-6, 1.0 - 1e-6).astype(np.float32).reshape(-1, 1)
                return np.clip(probs.reshape(-1), 1e-6, 1.0 - 1e-6).astype(np.float32).reshape(-1, 1)
            preds = np.asarray(self.base_model.predict(X)).reshape(-1)
            return np.clip(preds, 0.0, 1.0).astype(np.float32).reshape(-1, 1)

        preds = np.asarray(self.base_model.predict(X), dtype=np.float32).reshape(-1, 1)
        return preds

    def fit(self, X, y, epochs=None, X_val=None, y_val=None, **kwargs):
        from experiments.logger import debug_print
        # Сначала обучаем базовую модель
        debug_print("Training base model for distillation...")
        # Передаем параметры валидации базовой модели, если она их поддерживает
        fit_kwargs = {}
        if X_val is not None and y_val is not None:
            fit_kwargs['X_val'] = X_val
            fit_kwargs['y_val'] = y_val
        if epochs is not None:
            fit_kwargs['epochs'] = epochs

        self.base_model.fit(X, y, **fit_kwargs)

        # Получаем "мягкие" предсказания от базовой модели
        debug_print("Generating teacher predictions for distillation...")
        teacher_predictions = self._teacher_targets(X)
        teacher_predictions = np.asarray(teacher_predictions)

        # Преобразуем в тензоры: для многокласса храним вероятности по классам.
        X_tensor = torch.FloatTensor(X).to(self.device)
        teacher_tensor = torch.FloatTensor(teacher_predictions).to(self.device)

        X_val_tensor = None
        teacher_val_tensor = None
        if X_val is not None and y_val is not None:
            teacher_val_predictions = self._teacher_targets(X_val)
            X_val_tensor = torch.FloatTensor(X_val).to(self.device)
            teacher_val_tensor = torch.FloatTensor(teacher_val_predictions).to(self.device)

        # Обучаем студенческую модель имитировать учителя с early stopping по val loss.
        self.student_model.train()
        best_state = None
        best_val_loss = float('inf')
        best_train_loss = float('inf')
        patience = int(kwargs.get('distillation_patience', 30))
        min_delta = float(kwargs.get('distillation_min_delta', 1e-6))
        patience_counter = 0
        T = max(float(self.temperature), 1e-6)
        last_loss = None

        for epoch in range(self.distillation_epochs):
            self.optimizer.zero_grad()
            student_output = self.student_model(X_tensor)
            if self.task_type == 'multiclass_classification':
                # Classical KD for multiclass: KL(student/T || teacher_probs) * T^2.
                student_log_probs = torch.log_softmax(student_output / T, dim=1)
                loss = torch.nn.functional.kl_div(
                    student_log_probs, teacher_tensor, reduction='batchmean'
                ) * (T * T)
            else:
                loss = self.criterion(student_output, teacher_tensor)
            loss.backward()
            self.optimizer.step()
            last_loss = loss.item()

            with torch.no_grad():
                if X_val_tensor is not None and teacher_val_tensor is not None:
                    self.student_model.eval()
                    student_val_output = self.student_model(X_val_tensor)
                    if self.task_type == 'multiclass_classification':
                        student_val_log_probs = torch.log_softmax(student_val_output / T, dim=1)
                        val_loss = torch.nn.functional.kl_div(
                            student_val_log_probs, teacher_val_tensor, reduction='batchmean'
                        ) * (T * T)
                    else:
                        val_loss = self.criterion(student_val_output, teacher_val_tensor)
                    current_metric = float(val_loss.item())
                    self.student_model.train()
                else:
                    current_metric = float(last_loss)

            if current_metric + min_delta < best_val_loss:
                best_val_loss = current_metric
                best_train_loss = float(last_loss)
                best_state = {k: v.detach().clone() for k, v in self.student_model.state_dict().items()}
                patience_counter = 0
            else:
                patience_counter += 1

            if patience_counter >= patience:
                break

        if best_state is not None:
            self.student_model.load_state_dict(best_state)

        self.is_distilled = True
        debug_print("Distillation completed successfully!")
        return best_train_loss if np.isfinite(best_train_loss) else float(last_loss or 0.0)

    def predict(self, X):
        # Для согласованности с influence используем student после дистилляции.
        if not self.is_distilled:
            return self.base_model.predict(X)
        return self.student_predict(X)

    def student_predict(self, X):
        """Предсказания студенческой модели (для influence методов)"""
        if not self.is_distilled:
            raise ValueError("Student model not distilled yet. Call fit first.")

        self.student_model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            out = self.student_model(X_tensor)
            if self.task_type == 'binary_classification':
                out = torch.sigmoid(out)
                return out.cpu().numpy().flatten()
            out_np = out.cpu().numpy()
            return out_np.flatten() if out_np.ndim == 1 or out_np.shape[1] == 1 else out_np

    def predict_proba(self, X):
        """Вероятности классов студенческой модели для классификации."""
        if self.task_type not in ('binary_classification', 'multiclass_classification'):
            raise AttributeError("predict_proba is only defined for classification tasks")
        if not self.is_distilled:
            if hasattr(self.base_model, 'predict_proba'):
                return self.base_model.predict_proba(X)
            raise AttributeError("Student model not distilled yet and teacher has no predict_proba")

        self.student_model.eval()
        with torch.no_grad():
            logits = self.student_model(torch.FloatTensor(X).to(self.device))
            if self.task_type == 'binary_classification':
                p1 = torch.sigmoid(logits).cpu().numpy().reshape(-1)
                p0 = 1.0 - p1
                return np.column_stack([p0, p1])
            return torch.softmax(logits, dim=1).cpu().numpy()

    def named_parameters(self):
        """Предсказания параметров студенческой модели для influence методов"""
        if not self.is_distilled:
            raise ValueError("Student model not distilled yet. Call fit first.")
        return self.student_model.named_parameters()

    def get_params(self, deep=True):
        """Возвращает параметры модели (совместимость с sklearn)"""
        return {
            'base_model': self.base_model,
            'input_size': self.input_size,
            'device': self.device,
            'model_architecture': self.model_architecture,
            'distillation_epochs': self.distillation_epochs,
            'temperature': self.temperature,
            'task_type': self.task_type
        }

    def set_params(self, **params):
        if 'input_size' in params:
            self.input_size = params['input_size']
        if 'device' in params:
            self.device = params['device']
        if 'model_architecture' in params:
            self.model_architecture = params['model_architecture']
        if 'distillation_epochs' in params:
            self.distillation_epochs = params['distillation_epochs']
        if 'temperature' in params:
            self.temperature = params['temperature']
        return self
