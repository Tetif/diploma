import numpy as np
import torch
import torch.nn as nn
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

                y_pred = model.predict(x_np)
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


class ScorerFactory:
    """Фабрика для создания скореров"""

    @staticmethod
    def create_scorer(scorer_type='neg_mae', **kwargs):
        if scorer_type == 'neg_mae':
            return make_stable_neg_mae(**kwargs)
        else:
            raise ValueError(f"Unknown scorer type: {scorer_type}")