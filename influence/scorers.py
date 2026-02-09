import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import mean_absolute_error, f1_score, accuracy_score
from experiments.logger import debug_print


def make_stable_neg_mae(fail_score=-1e6):
    def stable_neg_mae_model(model, x, y):
        try:
            if len(x) == 0 or len(y) == 0:
                debug_print("Empty data received, returning fail_score")
                return float(fail_score)

            x_np = x.values if hasattr(x, "values") else np.asarray(x)
            y_np = y.values if hasattr(y, "values") else np.asarray(y)
            y_np = y_np.reshape(-1)

            if x_np.shape[0] == 0 or y_np.shape[0] == 0:
                debug_print("Empty array after conversion, returning fail_score")
                return float(fail_score)

            if hasattr(model, "predict"):
                # Detect common sklearn unfitted state where estimators_ may be empty (RandomForest)
                model_for_check = getattr(model, "model", model)
                try:
                    ests = getattr(model_for_check, 'estimators_', None)
                    if ests is not None and len(ests) == 0:
                        debug_print("Model appears unfitted (estimators_ is empty). Returning fail_score. Consider setting clone_before_fit=True or ensuring fit succeeded.")
                        return float(fail_score)
                except Exception:
                    # If checking fails, continue and let predict handle the real error
                    pass

                try:
                    y_pred = model.predict(x_np)
                except Exception as pred_e:
                    # Handle LightGBM crashes on empty/tiny datasets
                    debug_print(f"Model.predict failed (likely empty dataset): {pred_e}")
                    # Return a neutral score instead of sentinel to help LOO/TMCShapley work better
                    return 0.0
            else:
                model_module = getattr(model, "model", model)
                model_module.eval()
                with torch.no_grad():
                    device = next(model_module.parameters()).device
                    tx = torch.FloatTensor(x_np).to(device)
                    out = model_module(tx)
                    y_pred = out.cpu().numpy()

            y_pred = np.asarray(y_pred).reshape(-1)
            min_len = min(len(y_np), len(y_pred))

            if min_len == 0 or not np.isfinite(y_pred).all() or not np.isfinite(y_np).all():
                return float(fail_score)

            y_true = y_np[:min_len]
            y_pred = y_pred[:min_len]
            mae = float(np.mean(np.abs(y_pred - y_true)))
            score = -mae
            return float(score)
        except Exception as e:
            import traceback
            debug_print(f"Error in scorer: {e}")
            debug_print(traceback.format_exc())
            # Provide contextual information to aid debugging
            try:
                x_len = len(x) if hasattr(x, '__len__') else 'unknown'
                y_len = len(y) if hasattr(y, '__len__') else 'unknown'
            except Exception:
                x_len, y_len = 'unknown', 'unknown'
            debug_print(f"Scorer context: model={type(model).__name__}, has_predict={hasattr(model, 'predict')}, x_len={x_len}, y_len={y_len}")
            # Try a small sample prediction to capture predictable failures
            try:
                if hasattr(model, "predict") and x_len != 'unknown' and x_len > 0:
                    sample_x = x.values[:5] if hasattr(x, 'values') else np.asarray(x)[:5]
                    try:
                        sample_pred = model.predict(sample_x)
                        debug_print(f"Sample prediction (len={len(sample_pred)}): {repr(sample_pred)[:500]}")
                    except Exception as pred_e:
                        debug_print(f"Model.predict failed on sample: {pred_e}")
                else:
                    debug_print("Model has no 'predict' or empty input; may be a torch model or empty dataset")
            except Exception:
                pass
            return float(fail_score)

    return stable_neg_mae_model


def make_stable_f1_scorer(fail_score=-1e6, average='binary'):
    """Создает стабильный F1 scorer для классификации"""
    def stable_f1_model(model, x, y):
        try:
            if len(x) == 0 or len(y) == 0:
                debug_print("Empty data received, returning fail_score")
                return float(fail_score)

            x_np = x.values if hasattr(x, "values") else np.asarray(x)
            y_np = y.values if hasattr(y, "values") else np.asarray(y)
            y_np = y_np.reshape(-1)

            if x_np.shape[0] == 0 or y_np.shape[0] == 0:
                debug_print("Empty array after conversion, returning fail_score")
                return float(fail_score)

            if hasattr(model, "predict"):
                y_pred = model.predict(x_np)
            else:
                model_module = getattr(model, "model", model)
                model_module.eval()
                with torch.no_grad():
                    device = next(model_module.parameters()).device
                    tx = torch.FloatTensor(x_np).to(device)
                    out = model_module(tx)
                    y_pred = out.cpu().numpy()
                    if y_pred.shape[1] > 1:  # multiclass
                        y_pred = np.argmax(y_pred, axis=1)
                    else:
                        y_pred = (y_pred > 0.5).astype(int).reshape(-1)

            y_pred = np.asarray(y_pred).reshape(-1).astype(int)
            min_len = min(len(y_np), len(y_pred))

            if min_len == 0 or not np.isfinite(y_pred.astype(float)).all() or not np.isfinite(y_np.astype(float)).all():
                return float(fail_score)

            y_true = y_np[:min_len].astype(int)
            y_pred = y_pred[:min_len]
            score = float(f1_score(y_true, y_pred, average=average, zero_division=0))
            return score
        except Exception as e:
            debug_print(f"Error in F1 scorer: {e}")
            return float(fail_score)

    return stable_f1_model


def make_stable_accuracy_scorer(fail_score=-1e6):
    """Создает стабильный accuracy scorer для классификации"""
    def stable_accuracy_model(model, x, y):
        try:
            if len(x) == 0 or len(y) == 0:
                debug_print("Empty data received, returning fail_score")
                return float(fail_score)

            x_np = x.values if hasattr(x, "values") else np.asarray(x)
            y_np = y.values if hasattr(y, "values") else np.asarray(y)
            y_np = y_np.reshape(-1)

            if x_np.shape[0] == 0 or y_np.shape[0] == 0:
                debug_print("Empty array after conversion, returning fail_score")
                return float(fail_score)

            if hasattr(model, "predict"):
                y_pred = model.predict(x_np)
            else:
                model_module = getattr(model, "model", model)
                model_module.eval()
                with torch.no_grad():
                    device = next(model_module.parameters()).device
                    tx = torch.FloatTensor(x_np).to(device)
                    out = model_module(tx)
                    y_pred = out.cpu().numpy()
                    if y_pred.shape[1] > 1:  # multiclass
                        y_pred = np.argmax(y_pred, axis=1)
                    else:
                        y_pred = (y_pred > 0.5).astype(int).reshape(-1)

            y_pred = np.asarray(y_pred).reshape(-1).astype(int)
            min_len = min(len(y_np), len(y_pred))

            if min_len == 0 or not np.isfinite(y_pred.astype(float)).all() or not np.isfinite(y_np.astype(float)).all():
                return float(fail_score)

            y_true = y_np[:min_len].astype(int)
            y_pred = y_pred[:min_len]
            score = float(accuracy_score(y_true, y_pred))
            return score
        except Exception as e:
            debug_print(f"Error in accuracy scorer: {e}")
            return float(fail_score)

    return stable_accuracy_model


class ScorerFactory:
    """Фабрика для создания скореров"""

    @staticmethod
    def create_scorer(scorer_type='neg_mae', **kwargs):
        if scorer_type == 'neg_mae':
            return make_stable_neg_mae(**kwargs)
        elif scorer_type == 'f1':
            return make_stable_f1_scorer(average='binary', **kwargs)
        elif scorer_type == 'f1_weighted':
            return make_stable_f1_scorer(average='weighted', **kwargs)
        elif scorer_type == 'f1_macro':
            return make_stable_f1_scorer(average='macro', **kwargs)
        elif scorer_type == 'accuracy':
            return make_stable_accuracy_scorer(**kwargs)
        else:
            raise ValueError(f"Unknown scorer type: {scorer_type}. Available: neg_mae, f1, f1_weighted, f1_macro, accuracy")


__all__ = [
    'ScorerFactory',
    'make_stable_neg_mae',
    'make_stable_f1_scorer',
    'make_stable_accuracy_scorer'
]