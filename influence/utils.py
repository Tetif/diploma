import numpy as np
from experiments.logger import debug_print


def _extract_numeric_values_from_result(result):
    """
    Расширенная диагностика извлечения значений из результатов pyDVL
    с улучшенной обработкой разных масштабов значений
    """
    debug_print(f"Extracting values from result type: {type(result)}")

    extraction_methods = [
        ('values()', lambda: result.values()),
        ('dict values', lambda: list(result.values()) if hasattr(result, 'values') else None),
        ('iteration', lambda: list(result)),
        ('direct access', lambda: [v for v in result] if hasattr(result, '__iter__') else None)
    ]

    for method_name, method in extraction_methods:
        try:
            items = method()
            if items is not None:
                print(
                    f"Success with {method_name}, got {len(list(items)) if hasattr(items, '__len__') else 'unknown'} items")
                items_list = list(items) if hasattr(items, '__iter__') and not isinstance(items, (int, float)) else [
                    items]
                break
        except Exception as e:
            print(f"Failed {method_name}: {e}")
            continue
    else:
        print("All extraction methods failed, returning zeros")
        return np.array([])

    numeric = []
    debug_print(f"Processing {len(items_list)} items...")

    for i, v in enumerate(items_list):
        if v is None:
            numeric.append(0.0)
            continue

        value_extractors = [
            ('direct', lambda x: float(x)),
            ('.value', lambda x: float(x.value)),
            ('.val', lambda x: float(x.val)),
            ('dict value', lambda x: float(x.get('value', 0)) if isinstance(x, dict) else None),
            ('dict val', lambda x: float(x.get('val', 0)) if isinstance(x, dict) else None),
        ]

        extracted = None
        for extractor_name, extractor in value_extractors:
            try:
                extracted = extractor(v)
                if i < 5:
                    debug_print(f"Item {i}: successfully extracted value {extracted} using {extractor_name}")
                break
            except (AttributeError, TypeError, ValueError, KeyError):
                continue

        if extracted is None:
            if i < 5:
                debug_print(f"Item {i}: failed to extract value from {type(v)}: {v}")
            numeric.append(0.0)
        else:
            numeric.append(extracted)

    result_array = np.asarray(numeric)

    # Detect sentinel fail_score values (e.g., +/-1e6 used by scorers) and neutralize them
    try:
        sentinel_mask = np.abs(result_array) > 9e5
        if np.any(sentinel_mask):
            debug_print(f"Detected sentinel fail_score values for {int(np.sum(sentinel_mask))} items, replacing with NaN for robust stats")
            # Log sample of original items that produced extreme values
            try:
                large_idx = np.where(sentinel_mask)[0][:10]
                for idx in large_idx:
                    debug_print(f"Large sentinel at index {idx}: value={result_array[idx]}, original_item_type={type(items_list[idx])}, repr={repr(items_list[idx])[:500]}")
            except Exception:
                pass
            result_array[sentinel_mask] = np.nan
    except Exception:
        # If something goes wrong with sentinel detection, continue gracefully
        pass

    if len(result_array) > 0:
        finite_mask = np.isfinite(result_array)
        if np.any(finite_mask):
            finite_vals = result_array[finite_mask]

            p1 = np.percentile(finite_vals, 1)
            p99 = np.percentile(finite_vals, 99)
            median = np.median(finite_vals)
            mean = np.mean(finite_vals)

            print(f"RAW VALUES BEFORE PROCESSING:")
            print(f"  Min: {np.min(finite_vals):.10f}")
            print(f"  Max: {np.max(finite_vals):.10f}")
            print(f"  Mean: {mean:.10f}")
            print(f"  Median: {median:.10f}")
            print(f"  P1: {p1:.10f}")
            print(f"  P99: {p99:.10f}")
            print(f"  Std: {np.std(finite_vals):.10f}")

            if np.max(finite_vals) - np.min(finite_vals) < 1e-10:
                debug_print("WARNING: All values are essentially the same!")
            else:
                debug_print(f"Value range: {np.max(finite_vals) - np.min(finite_vals):.10f}")

            abs_vals = np.abs(finite_vals)
            if np.max(abs_vals) < 1e-6:
                debug_print("WARNING: Values are very small, might be rounded to zero")

        else:
            debug_print("WARNING: No finite values found!")

    return result_array


def get_influence_statistics(scores):
    """Собирает статистику по influence scores"""
    stats = {}
    for method, values in scores.items():
        if len(values) > 0:
            stats[method] = {
                'min': float(np.min(values)),
                'max': float(np.max(values)),
                'mean': float(np.mean(values)),
                'median': float(np.median(values)),
                'std': float(np.std(values)),
                'q25': float(np.percentile(values, 25)),
                'q75': float(np.percentile(values, 75)),
                'non_zero_count': int(np.sum(values != 0)),
                'total_count': len(values)
            }
    return stats

