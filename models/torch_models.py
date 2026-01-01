import torch
import torch.nn as nn
import torch.optim as optim
from .base import BaseModel
from config.settings import MODEL_CONFIGS, DEVICE
from experiments.logger import debug_print

class SimpleNN(nn.Module):
    def __init__(self, input_size, layers=None, dropout=0.2):
        super(SimpleNN, self).__init__()
        if layers is None:
            layers = MODEL_CONFIGS['pytorch']['simple']['layers']

        modules = []
        prev_size = input_size

        for i, layer_size in enumerate(layers):
            modules.append(nn.Linear(prev_size, layer_size))
            modules.append(nn.ReLU())
            if dropout > 0:
                modules.append(nn.Dropout(dropout))
            prev_size = layer_size

        modules.append(nn.Linear(prev_size, 1))

        self.network = nn.Sequential(*modules)

    def forward(self, x):
        return self.network(x)


class ImprovedNN(nn.Module):
    def __init__(self, input_size, layers=None, dropout=None, batch_norm=True):
        super(ImprovedNN, self).__init__()
        if layers is None:
            layers = MODEL_CONFIGS['pytorch']['improved']['layers']
        if dropout is None:
            dropout = MODEL_CONFIGS['pytorch']['improved']['dropout']

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

        modules.append(nn.Linear(prev_size, 1))

        self.network = nn.Sequential(*modules)

    def forward(self, x):
        return self.network(x)


class SimpleFTTransformer(nn.Module):
    def __init__(self, input_size, **kwargs):
        super().__init__()
        config = MODEL_CONFIGS['pytorch']['ft_transformer_simple'].copy()
        config.update(kwargs)

        self.d_model = config['d_model']
        self.input_projection = nn.Linear(input_size, self.d_model)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.d_model,
            nhead=config['nhead'],
            dim_feedforward=config['dim_feedforward'],
            dropout=config['dropout'],
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=config['num_layers'])
        self.output_layer = nn.Linear(self.d_model, 1)

    def forward(self, x):
        x = self.input_projection(x)
        x = x.unsqueeze(1)
        x = self.transformer_encoder(x)
        x = x.squeeze(1)
        x = self.output_layer(x)
        return x


class PyTorchModelWrapper(BaseModel):
    """Обертка для PyTorch моделей для совместимости"""

    def __init__(self, input_size, model_architecture='simple', device=DEVICE, **kwargs):
        super().__init__()
        self.input_size = input_size
        self.device = device
        self.model_architecture = model_architecture

        if model_architecture == 'improved':
            self.model = ImprovedNN(input_size, **kwargs).to(device)
        elif model_architecture == 'ft_transformer':
            self.model = SimpleFTTransformer(input_size, **kwargs).to(device)
        elif model_architecture == 'ft_transformer_simple':
            self.model = SimpleFTTransformer(input_size, **kwargs).to(device)
        else:
            self.model = SimpleNN(input_size, **kwargs).to(device)

        self.optimizer = optim.Adam(self.model.parameters(),
                                    lr=kwargs.get('learning_rate', 0.001))
        self.criterion = nn.MSELoss()

    def fit(self, X, y, epochs=5, **kwargs):
        X_tensor = torch.FloatTensor(X).to(self.device)
        y_tensor = torch.FloatTensor(y).reshape(-1, 1).to(self.device)

        self.model.train()
        total_loss = 0
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
            return self.model(X_tensor).cpu().numpy().flatten()

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
                 distillation_epochs=50, temperature=2.0):
        super().__init__()
        self.base_model = base_model
        self.input_size = input_size
        self.device = device
        self.model_architecture = model_architecture
        self.distillation_epochs = distillation_epochs
        self.temperature = temperature
        self.is_distilled = False

        # Создаем студенческую нейросеть (без dropout для influence functions)
        if model_architecture == 'improved':
            self.student_model = ImprovedNN(input_size, dropout=0.0).to(device)  # Отключаем dropout
        else:
            self.student_model = SimpleNN(input_size, dropout=0.0).to(device)  # Отключаем dropout

        self.optimizer = optim.Adam(self.student_model.parameters(),
                                    lr=MODEL_CONFIGS['pytorch']['simple']['learning_rate'])
        self.criterion = nn.MSELoss()

    def fit(self, X, y, epochs=None, X_val=None, y_val=None, **kwargs):
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
        teacher_predictions = self.base_model.predict(X)

        # Преобразуем в тензоры
        X_tensor = torch.FloatTensor(X).to(self.device)
        teacher_tensor = torch.FloatTensor(teacher_predictions).reshape(-1, 1).to(self.device)

        # Обучаем студенческую модель имитировать учителя
        debug_print(f"Distilling knowledge for {self.distillation_epochs} epochs...")
        self.student_model.train()

        for epoch in range(self.distillation_epochs):
            self.optimizer.zero_grad()
            student_output = self.student_model(X_tensor)
            loss = self.criterion(student_output, teacher_tensor)
            loss.backward()
            self.optimizer.step()

            if (epoch + 1) % 10 == 0:
                debug_print(
                    f"Distillation epoch {epoch + 1}/{self.distillation_epochs}, Loss: {loss.item():.4f}")

        self.is_distilled = True
        debug_print("Distillation completed successfully!")
        return loss.item()

    def predict(self, X):
        # Используем базовую модель для предсказаний
        return self.base_model.predict(X)

    def student_predict(self, X):
        """Предсказания студенческой модели (для influence методов)"""
        if not self.is_distilled:
            raise ValueError("Student model not distilled yet. Call fit first.")

        self.student_model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            return self.student_model(X_tensor).cpu().numpy().flatten()

    def named_parameters(self):
        """Возвращает параметры студенческой модели для influence методов"""
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
            'temperature': self.temperature
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