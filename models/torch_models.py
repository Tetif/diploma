import torch
import torch.nn as nn
import torch.optim as optim
from .base import BaseModel
from config.settings import MODEL_CONFIGS, DEVICE


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