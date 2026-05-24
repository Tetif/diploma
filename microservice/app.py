"""Веб-интерфейс Streamlit для микросервиса influence."""
import sys
from pathlib import Path

# Корень проекта в sys.path (при запуске из каталога microservice/).
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import streamlit as st

try:
    from streamlit_autorefresh import st_autorefresh as _st_autorefresh
except ImportError:
    _st_autorefresh = None
import requests
import json
import time
import copy
import hashlib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
import os
from collections import defaultdict

from microservice.plotting import (
    plotly_computation_metric_bars,
    plotly_removal_auc_bars,
    plotly_removal_mean_pct_diff_from_pointwise_best_bars,
)

st.set_page_config(
    page_title="Influence Functions",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
# Клиентское автообновление страницы ожидания (мс), без sleep на сервере.
WORKSPACE_POLL_AUTOREFRESH_MS = 3500
# Ожидание завершения запуска с вкладки «Рабочая область» (не блокирует UI — см. rerun).
WORKSPACE_POLL_EXPERIMENT_ID_KEY = "workspace_poll_experiment_id"
WORKSPACE_POLL_KIND_KEY = "workspace_poll_kind"
# Свернуть форму параметров, оставив панель прогресса (не сбрасывает отслеживание эксперимента).
WORKSPACE_FORM_COLLAPSED_KEY = "workspace_form_collapsed"
# Запуск вне st.form: session_state внутри submit формы может не сохраниться до следующего клика.
PENDING_INFLUENCE_START_KEY = "workspace_pending_influence_config"
PENDING_REMOVAL_START_KEY = "workspace_pending_removal_start"
# connect, read — увеличенный read для тяжёлых JSON
DEFAULT_HTTP_TIMEOUT: Tuple[float, float] = (15.0, 900.0)
_LIGHT_GET_TIMEOUT: Tuple[float, float] = (5.0, 30.0)

_ANALYSIS_TAB_DIST = "Распределение весов influence"
_ANALYSIS_TAB_REMOVAL = "Удаление данных и метрика"
_ANALYSIS_TAB_EXAMPLES = "Ресурсы, время и примеры"

# Подписи к color_picker: не обрезать длинные имена методов (NystroemSketchInfluence_lowest и т.д.)
_COLOR_PICKER_LABEL_MAX_CHARS = 120

def _normalize_timeout(
    timeout: Optional[Union[int, float, Tuple[float, float]]],
) -> Union[float, Tuple[float, float]]:
    if timeout is None:
        return DEFAULT_HTTP_TIMEOUT
    if isinstance(timeout, (int, float)):
        return (min(15.0, float(timeout) / 3), float(timeout))
    return timeout


def _http_get_json_quiet(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, Tuple[float, float]]] = None,
) -> Optional[Dict]:
    """GET JSON; без st.* (для @st.cache_data)."""
    t = _normalize_timeout(timeout)
    try:
        response = requests.get(url, timeout=t, params=params)
        if response.status_code != 200:
            return None
        return response.json()
    except Exception:
        return None


def _params_tuple(params: Optional[Dict[str, Any]]) -> Tuple[Tuple[str, Any], ...]:
    if not params:
        return ()
    return tuple(sorted(params.items(), key=lambda x: x[0]))


@st.cache_data(ttl=12, show_spinner=False)
def _cached_api_health_ok(base_url: str) -> bool:
    try:
        r = requests.get(f"{base_url.rstrip('/')}/health", timeout=_LIGHT_GET_TIMEOUT)
        return r.status_code == 200
    except Exception:
        return False


@st.cache_data(ttl=300, show_spinner=False)
def _cached_api_models(base_url: str) -> List[str]:
    data = _http_get_json_quiet(
        f"{base_url.rstrip('/')}/info/models", timeout=_LIGHT_GET_TIMEOUT
    )
    if data and data.get("models"):
        return list(data["models"])
    return ["random_forest"]


@st.cache_data(ttl=25, show_spinner=False)
def _cached_api_experiments_list(base_url: str) -> Optional[Dict]:
    return _http_get_json_quiet(
        f"{base_url.rstrip('/')}/experiments", timeout=DEFAULT_HTTP_TIMEOUT
    )


@st.cache_data(ttl=90, show_spinner=False)
def _cached_api_experiment_results(
    base_url: str,
    experiment_id: str,
    params_key: Tuple[Tuple[str, Any], ...],
) -> Optional[Dict]:
    params = dict(params_key) if params_key else None
    return _http_get_json_quiet(
        f"{base_url.rstrip('/')}/experiments/{experiment_id}/results",
        params=params,
        timeout=DEFAULT_HTTP_TIMEOUT,
    )


@st.cache_data(ttl=15, show_spinner=False)
def _cached_api_graph_data(
    base_url: str,
    experiment_id: str,
    params_key: Tuple[Tuple[str, Any], ...],
) -> Optional[Dict]:
    params = dict(params_key) if params_key else None
    return _http_get_json_quiet(
        f"{base_url.rstrip('/')}/experiments/{experiment_id}/graph-data",
        params=params,
        timeout=DEFAULT_HTTP_TIMEOUT,
    )


@st.cache_data(ttl=90, show_spinner=False)
def _cached_api_train_targets(base_url: str, experiment_id: str) -> Optional[Dict]:
    return _http_get_json_quiet(
        f"{base_url.rstrip('/')}/experiments/{experiment_id}/train-targets",
        timeout=DEFAULT_HTTP_TIMEOUT,
    )


@st.cache_data(ttl=90, show_spinner=False)
def _cached_api_influence_weights(
    base_url: str, experiment_id: str, method: str
) -> Optional[Dict]:
    return _http_get_json_quiet(
        f"{base_url.rstrip('/')}/experiments/{experiment_id}/influence-weights/{method}",
        timeout=DEFAULT_HTTP_TIMEOUT,
    )


@st.cache_data(ttl=60, show_spinner=False)
def _cached_api_artifacts_list(base_url: str, experiment_id: str) -> Optional[Dict]:
    return _http_get_json_quiet(
        f"{base_url.rstrip('/')}/experiments/{experiment_id}/artifacts",
        timeout=DEFAULT_HTTP_TIMEOUT,
    )


def make_api_request(
    method: str,
    endpoint: str,
    data: Dict = None,
    timeout: Optional[Union[int, float, Tuple[float, float]]] = None,
    params: Optional[Dict[str, Union[str, int, float, bool]]] = None,
) -> Optional[Dict]:
    """Запрос к FastAPI; по умолчанию до 900 с на чтение ответа."""
    t = _normalize_timeout(timeout)
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=t, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=t)
        elif method == "DELETE":
            response = requests.delete(url, timeout=t)

        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                st.error("Ответ API не в формате JSON")
                return None
        else:
            st.error(f"Ошибка API {response.status_code}: {response.text[:2000]}")
            return None
    except requests.exceptions.Timeout:
        st.error(
            "Превышено время ожидания ответа API. Увеличьте таймаут или снизьте нагрузку на сервер. "
            f"Лимит чтения: {t[1] if isinstance(t, tuple) else t} с."
        )
        return None
    except requests.exceptions.ConnectionError:
        st.error(f"Нет соединения с API: {API_BASE_URL}")
        return None
    except requests.exceptions.RequestException as e:
        err = str(e)
        if "timed out" in err.lower() or "timeout" in err.lower():
            st.error(
                "Таймаут при обращении к API. "
                f"Проверьте доступность {API_BASE_URL}. ({err[:300]})"
            )
        else:
            st.error(f"Ошибка API: {err[:1500]}")
        return None
    except Exception as e:
        st.error(f"Ошибка API: {str(e)}")
        return None


def _resolve_workspace_poll() -> Tuple[Optional[str], Optional[str]]:
    """(experiment_id, kind) для панели прогресса; kind — influence | removal."""
    eid = st.session_state.get(WORKSPACE_POLL_EXPERIMENT_ID_KEY)
    kind = st.session_state.get(WORKSPACE_POLL_KIND_KEY)
    if eid and kind in ("influence", "removal"):
        return str(eid), str(kind)
    cur = st.session_state.get("current_experiment_id")
    if not cur:
        return None, None
    status = make_api_request("GET", f"/experiments/{cur}/status")
    if status and str(status.get("status", "")).lower() in (
        "running",
        "pending",
        "started",
    ):
        st.session_state[WORKSPACE_POLL_EXPERIMENT_ID_KEY] = cur
        st.session_state[WORKSPACE_POLL_KIND_KEY] = "influence"
        return str(cur), "influence"
    return None, None


def _resolve_workspace_influence_poll_id() -> Optional[str]:
    """ID influence-эксперимента для логики свёрнутой формы."""
    eid, kind = _resolve_workspace_poll()
    return eid if kind == "influence" else None


def _handle_workspace_poll_terminal(
    terminal: Dict[str, Any], poll_eid: str, poll_kind: str
) -> None:
    st.session_state.pop(WORKSPACE_POLL_EXPERIMENT_ID_KEY, None)
    st.session_state.pop(WORKSPACE_POLL_KIND_KEY, None)
    st.session_state.pop(WORKSPACE_FORM_COLLAPSED_KEY, None)
    sid = str((terminal.get("status") or "")).lower()
    msg = str(terminal.get("message") or "")
    if poll_kind == "removal":
        if sid == "completed":
            st.success(f"Removal завершён (`{poll_eid}`).")
        elif sid == "cancelled":
            st.warning(f"Removal остановлен (`{poll_eid}`).")
        elif sid != "failed" or msg != "timeout":
            st.error(
                f"Removal завершился с ошибкой (`{poll_eid}`): "
                f"{terminal.get('message', '—')}"
            )
        return
    if sid == "completed":
        st.session_state.experiment_done_banner = {"experiment_id": poll_eid}
        st.session_state.last_experiment_id = poll_eid
    elif sid == "cancelled":
        st.warning(f"Эксперимент остановлен (`{poll_eid}`).")
    elif sid != "failed" or msg != "timeout":
        st.error(
            f"Эксперимент завершился с ошибкой (`{poll_eid}`): "
            f"{terminal.get('message', '—')}"
        )
    _mark_inf_form_restore_needed()


def _render_workspace_active_poll() -> bool:
    """Панель прогресса над вкладками; True — эксперимент ещё выполняется."""
    poll_eid, poll_kind = _resolve_workspace_poll()
    if not poll_eid:
        return False
    heading = (
        "Removal выполняется…"
        if poll_kind == "removal"
        else "Эксперимент выполняется…"
    )
    form_collapsed = bool(st.session_state.get(WORKSPACE_FORM_COLLAPSED_KEY, False))
    enable_autorefresh = form_collapsed if poll_kind == "influence" else True
    terminal = _render_workspace_poll_block(
        poll_eid,
        heading=heading,
        enable_autorefresh=enable_autorefresh,
    )
    if terminal is not None:
        _handle_workspace_poll_terminal(terminal, poll_eid, poll_kind or "influence")
        st.cache_data.clear()
        st.rerun()
    return True


def _process_pending_influence_start() -> None:
    pending = st.session_state.pop(PENDING_INFLUENCE_START_KEY, None)
    if not pending:
        return
    with st.spinner("Запуск эксперимента…"):
        response = make_api_request("POST", "/experiments/start", {"config": pending})
    if response:
        experiment_id = response.get("experiment_id")
        st.session_state.current_experiment_id = experiment_id
        st.session_state.selected_experiment_id = experiment_id
        st.session_state[WORKSPACE_POLL_EXPERIMENT_ID_KEY] = experiment_id
        st.session_state[WORKSPACE_POLL_KIND_KEY] = "influence"
        st.session_state[WORKSPACE_FORM_COLLAPSED_KEY] = True
        st.success(f"Эксперимент запущен.\nID: {experiment_id}")
        st.cache_data.clear()
        st.rerun()


def _process_pending_removal_start() -> None:
    pending = st.session_state.pop(PENDING_REMOVAL_START_KEY, None)
    if not pending:
        return
    parent_id = pending.get("parent_id")
    body = pending.get("body")
    if not parent_id or not body:
        return
    with st.spinner("Запуск removal…"):
        resp = make_api_request(
            "POST",
            f"/experiments/{parent_id}/removal-runs/start",
            data=body,
        )
    if resp and resp.get("experiment_id"):
        cid = resp["experiment_id"]
        st.session_state.selected_experiment_id = cid
        st.session_state[WORKSPACE_POLL_EXPERIMENT_ID_KEY] = cid
        st.session_state[WORKSPACE_POLL_KIND_KEY] = "removal"
        st.success(f"Removal запущен: `{cid}`")
        st.cache_data.clear()
        st.rerun()


def _render_workspace_poll_block(
    experiment_id: str,
    *,
    heading: str = "Эксперимент выполняется…",
    max_wait_seconds: int = 3600,
    enable_autorefresh: bool = True,
) -> Optional[Dict]:
    """Показывает прогресс и кнопку остановки.

    Пока эксперимент не в финальном статусе, при наличии ``streamlit-autorefresh``
    включается клиентское автообновление; иначе статус обновляется кнопкой «Обновить прогресс».
    Без ``sleep`` и без серверного ``st.rerun()`` в цикле — иначе UI не интерактивен.

    Возвращает финальный JSON статуса при завершении / ошибке / отмене, иначе ``None``.
    """
    now = time.time()
    started = float(st.session_state.get("_workspace_poll_started_ts") or now)
    if st.session_state.get("_workspace_poll_started_eid") != experiment_id:
        st.session_state._workspace_poll_started_ts = now
        st.session_state._workspace_poll_started_eid = experiment_id
        started = now

    if now - started > max_wait_seconds:
        st.session_state.pop("_workspace_poll_started_ts", None)
        st.session_state.pop("_workspace_poll_started_eid", None)
        st.error("Превышено время ожидания эксперимента")
        return {"status": "failed", "message": "timeout", "experiment_id": experiment_id}

    st.markdown("---")
    hcol, bcol = st.columns([3, 1])
    with hcol:
        st.markdown(f"### {heading}")
        st.caption(f"ID: `{experiment_id}`")
    with bcol:
        if st.button(
            "Остановить",
            key=f"workspace_poll_stop_{experiment_id}",
            help="Запросить остановку (учитывается на следующих шагах прогресса)",
            use_container_width=True,
        ):
            resp = make_api_request("POST", f"/experiments/{experiment_id}/cancel")
            st.cache_data.clear()
            if resp:
                st.success("Запрос на остановку отправлен.")
                _mark_inf_form_restore_needed()
                st.rerun()

    status_response = make_api_request("GET", f"/experiments/{experiment_id}/status")

    if status_response:
        prog = min(float(status_response.get("progress", 0)) / 100.0, 1.0)
        st.progress(prog)

        si = status_response.get("stage_index")
        stot = status_response.get("stages_total")
        eta = status_response.get("eta_seconds")
        msg = status_response.get("message", "Processing...")
        line = str(msg)
        if si and stot:
            line = f"Этап {si}/{stot}: {msg}"
        if eta is not None and status_response.get("status") == "running":
            try:
                line += f" · ~{float(eta):.0f}s remaining"
            except (TypeError, ValueError):
                pass
        st.info(line)

        if status_response.get("status") in ["completed", "failed", "cancelled"]:
            st.session_state.pop("_workspace_poll_started_ts", None)
            st.session_state.pop("_workspace_poll_started_eid", None)
            return status_response
    else:
        st.warning("Не удалось получить статус эксперимента; повтор через несколько секунд.")

    # Не используем time.sleep + st.rerun(): выполнение скрипта блокируется до sleep,
    # виджеты не становятся интерактивными; постоянный rerun даёт лаги.
    refresh_ms = WORKSPACE_POLL_AUTOREFRESH_MS
    if not status_response:
        refresh_ms = max(refresh_ms, 6000)
    approx_sec = max(1, refresh_ms // 1000)
    if enable_autorefresh and _st_autorefresh is not None:
        st.caption(
            f"Обновление прогресса примерно каждые ~{approx_sec} с; «Остановить» доступна сразу."
        )
        _st_autorefresh(
            interval=refresh_ms, limit=None, key=f"ws_poll_refresh_{experiment_id}"
        )
    else:
        if not enable_autorefresh:
            st.caption(
                "Автообновление отключено, пока открыта полная форма параметров "
                "(так надёжнее работают кнопки). Нажмите «Обновить прогресс»."
            )
        else:
            st.caption(
                "Нажмите «Обновить прогресс», чтобы подтянуть статус "
                "(опционально: `pip install streamlit-autorefresh`)."
            )
        if st.button(
            "Обновить прогресс",
            key=f"ws_poll_manual_refresh_{experiment_id}",
        ):
            st.rerun()
    return None


def get_available_datasets() -> List[str]:
    """Список датасетов с API."""
    response = make_api_request("GET", "/info/datasets")
    if response:
        return response.get('datasets', [])
    return []


def get_available_models() -> List[str]:
    """Список моделей (кэш)."""
    return _cached_api_models(API_BASE_URL)


def get_available_methods() -> List[str]:
    """Список методов influence с API."""
    response = make_api_request("GET", "/info/influence-methods")
    if response:
        return response.get('methods', [])
    return []


_TASK_LABEL_RU_UI = {
    "regression": "Регрессия",
    "binary_classification": "Бинарная классификация",
    "multiclass_classification": "Мультиклассификация",
}

# Как _METRIC_BY_TASK в microservice/api/models.py
_METRIC_BY_TASK_UI = {
    "regression": frozenset({"mae", "rmse", "r2"}),
    "binary_classification": frozenset({"accuracy", "f1", "precision", "recall"}),
    "multiclass_classification": frozenset({"accuracy", "f1_weighted", "f1_macro"}),
}


def _is_classification_task_type(task_type: str) -> bool:
    return task_type in ("binary_classification", "multiclass_classification")


def _is_regression_task_type(task_type: str) -> bool:
    return task_type == "regression"


def _task_type_for_experiment_list_row(row: Dict[str, Any]) -> str:
    """По полю dataset в списке экспериментов API — task_type из DatasetRegistry."""
    ds = row.get("dataset") or row.get("dataset_name")
    if not ds:
        return ""
    try:
        from config import DatasetRegistry

        return DatasetRegistry.get(ds).get_info().get("task_type", "") or ""
    except Exception:
        return ""


def get_dataset_details_for_ui() -> List[Dict[str, Any]]:
    """Метаданные датасетов из DatasetRegistry (без лишнего HTTP к API)."""
    from config import DatasetRegistry
    from config.datasets.dataset_sizes import APPROX_N_SAMPLES, format_sample_size

    out: List[Dict[str, Any]] = []
    for name in DatasetRegistry.list():
        info = DatasetRegistry.get(name).get_info()
        tt = info["task_type"]
        n = APPROX_N_SAMPLES.get(name)
        out.append(
            {
                "name": name,
                "task_type": tt,
                "task_label_ru": _TASK_LABEL_RU_UI.get(tt, tt),
                "approximate_n_samples": n,
                "size_display": format_sample_size(n),
            }
        )
    return out


def build_dataset_rows_with_metrics(metric_config: Dict[str, str]) -> List[Dict[str, Any]]:
    """Добавляет список допустимых метрик по типу задачи (пересечение с конфигом датасета)."""
    from config import DatasetRegistry

    base = get_dataset_details_for_ui()
    out: List[Dict[str, Any]] = []
    for r in base:
        name = r["name"]
        info = DatasetRegistry.get(name).get_info()
        tt = info["task_type"]
        allowed = _METRIC_BY_TASK_UI[tt]
        ds_m = set(info.get("metrics") or [])
        metrics_allowed = sorted(ds_m & allowed)
        if not metrics_allowed:
            metrics_allowed = sorted(allowed)
        ddef = metric_config.get(tt, metrics_allowed[0])
        if ddef not in metrics_allowed:
            ddef = metrics_allowed[0]
        out.append(
            {
                **r,
                "metrics_allowed": metrics_allowed,
                "default_metric": ddef,
            }
        )
    return out


def load_influence_weights(experiment_id: str, method: str) -> Optional[Dict]:
    """Веса influence для метода (кэш)."""
    return _cached_api_influence_weights(API_BASE_URL, experiment_id, method)


def load_graph_data(experiment_id: str) -> Optional[Dict]:
    """Данные для графиков removal (кэш)."""
    return _cached_api_graph_data(API_BASE_URL, experiment_id, ())


def load_artifacts_list(experiment_id: str) -> Optional[Dict]:
    return _cached_api_artifacts_list(API_BASE_URL, experiment_id)


_CLASS_HIST_COLORS = [
    "#636EFA",
    "#EF553B",
    "#00CC96",
    "#AB63FA",
    "#FFA15A",
    "#19D3F3",
    "#FF6692",
    "#B6E880",
    "#FF97FF",
    "#FECB52",
]


def plot_influence_distribution_stacked_plotly(
    weights_by_method: Dict[str, List[float]],
    *,
    targets: Optional[List[int]] = None,
    group_label: str = "класс",
) -> go.Figure:
    """Все методы сверху вниз; при targets — гистограммы по группам (классы или страты y, overlay)."""
    methods = list(weights_by_method.keys())
    n = len(methods)
    if n == 0:
        fig = go.Figure()
        fig.update_layout(template="plotly_white", height=200)
        return fig

    fig = make_subplots(
        rows=n,
        cols=1,
        subplot_titles=list(methods),
        vertical_spacing=0.07 if n > 1 else 0.02,
    )
    use_group_color = (
        targets is not None
        and len(targets) > 0
        and all(
            len(np.asarray(weights_by_method[m]).ravel()) == len(targets)
            for m in methods
        )
    )
    t_arr = np.asarray(targets, dtype=int) if use_group_color else None

    for i, method in enumerate(methods, start=1):
        w = np.asarray(weights_by_method[method], dtype=float).ravel()
        if use_group_color and t_arr is not None and len(t_arr) == len(w):
            classes = sorted(np.unique(t_arr).tolist())
            for j, cls in enumerate(classes):
                mask = t_arr == cls
                if not np.any(mask):
                    continue
                fig.add_trace(
                    go.Histogram(
                        x=w[mask],
                        nbinsx=50,
                        name=f"{group_label} {cls}",
                        legendgroup=f"g{cls}",
                        showlegend=(i == 1),
                        marker_color=_CLASS_HIST_COLORS[j % len(_CLASS_HIST_COLORS)],
                        opacity=0.62,
                        marker_line_width=0.5,
                        marker_line_color="white",
                    ),
                    row=i,
                    col=1,
                )
        else:
            fig.add_trace(
                go.Histogram(
                    x=w,
                    nbinsx=50,
                    showlegend=False,
                    marker_color="rgba(55, 128, 191, 0.75)",
                    marker_line_width=0.5,
                    marker_line_color="white",
                ),
                row=i,
                col=1,
            )
        if w.size:
            mu = float(np.mean(w))
            fig.add_vline(
                x=mu,
                line_width=2,
                line_dash="dash",
                line_color="rgba(200, 80, 80, 0.85)",
                row=i,
                col=1,
            )

    fig.update_layout(
        barmode="overlay" if use_group_color else "relative",
        template="plotly_white",
        hovermode="x unified",
        height=max(320, 300 * n),
        showlegend=use_group_color,
    )
    for r in range(1, n + 1):
        fig.update_yaxes(title_text="Частота", row=r, col=1)
    fig.update_xaxes(title_text="Значение influence", row=n, col=1)
    return fig


_REMOVAL_SUFFIXES = (
    "_few_good_rand",
    "_few_median_rand",
    "_few_bad_rand",
    "_extremes",
    "_lowest",
    "_highest",
    "_median",
)


def _removal_base_name(method: str) -> str:
    """Базовое имя метода без суффикса стратегии (для цвета)."""
    for suf in _REMOVAL_SUFFIXES:
        if method.endswith(suf):
            return method[: -len(suf)]
    return method


# Согласовано с visualization/plots.py (trend_colors)
_DEFAULT_REMOVAL_TRACE_COLORS: Dict[str, str] = {
    "Baseline": "#000000",
    "LOO": "#2ecc71",
    "Banzhaf": "#1f77b4",
    "TMCShapley": "#ff7f0e",
    "DataShapley": "#3498db",
    "BetaShapley": "#e74c3c",
    "Influence": "#9b59b6",
    "ArnoldiInfluence": "#d62728",
    "CgInfluence": "#9467bd",
    "LissaInfluence": "#8c564b",
    "NystroemSketchInfluence": "#e377c2",
    "CatBoostInfluence": "#17becf",
    "LossHigh": "#2e7d32",
    "LossLow": "#1565C0",
    "random": "#f39c12",
    "Random": "#f39c12",
    "Shapley": "#F5B041",
    "PermutationImportance": "#F7DC6F",
}


def default_color_for_removal_trace(method: str) -> str:
    b = _removal_base_name(method)
    if method in _DEFAULT_REMOVAL_TRACE_COLORS:
        return _DEFAULT_REMOVAL_TRACE_COLORS[method]
    if b in _DEFAULT_REMOVAL_TRACE_COLORS:
        return _DEFAULT_REMOVAL_TRACE_COLORS[b]
    h = int(hashlib.md5(method.encode()).hexdigest()[:6], 16)
    return f"#{h:06x}"


def _plotly_line_marker_style(method: str, line_color: str) -> Dict[str, Any]:
    """
    Стили стратегий: lowest — сплошная + крупные залитые маркеры;
    highest — штрих-пунктир + маркер с обводкой; extremes — пунктир + квадраты.
    """
    if method.endswith("_lowest"):
        return {
            "line": dict(width=2.8, dash="solid", color=line_color),
            "marker": dict(
                size=12,
                symbol="circle",
                color=line_color,
                line=dict(width=0),
            ),
            "mode": "lines+markers",
        }
    if method.endswith("_highest"):
        return {
            "line": dict(width=2.5, dash="dashdot", color=line_color),
            "marker": dict(
                size=9,
                symbol="diamond",
                color=line_color,
                line=dict(width=1.8, color="#FFFFFF"),
            ),
            "mode": "lines+markers",
        }
    if method.endswith("_extremes"):
        return {
            "line": dict(width=2.5, dash="dash", color=line_color),
            "marker": dict(
                size=9,
                symbol="square",
                color=line_color,
                line=dict(width=0),
            ),
            "mode": "lines+markers",
        }
    if method.endswith("_median"):
        return {
            "line": dict(width=2.0, dash="dot", color=line_color),
            "marker": dict(size=7, symbol="circle", color=line_color),
            "mode": "lines+markers",
        }
    if method.endswith("_few_bad_rand"):
        return {
            "line": dict(width=2.0, dash="longdash", color=line_color),
            "marker": dict(size=7, symbol="square", color=line_color),
            "mode": "lines+markers",
        }
    if method.endswith("_few_median_rand"):
        return {
            "line": dict(width=2.0, dash="longdash", color=line_color),
            "marker": dict(size=7, symbol="diamond", color=line_color),
            "mode": "lines+markers",
        }
    if method.endswith("_few_good_rand"):
        return {
            "line": dict(width=2.0, dash="dot", color=line_color),
            "marker": dict(size=7, symbol="triangle-up", color=line_color),
            "mode": "lines+markers",
        }
    return {
        "line": dict(width=2.2, dash="solid", color=line_color),
        "marker": dict(size=8, symbol="circle", color=line_color),
        "mode": "lines+markers",
    }


def _parse_random_run_results(
    rrr: Optional[Dict[str, Any]],
) -> Optional[Dict[int, List[float]]]:
    if not rrr:
        return None
    out: Dict[int, List[float]] = {}
    for k, v in rrr.items():
        try:
            ki = int(k)
        except (TypeError, ValueError):
            continue
        if isinstance(v, list) and len(v) > 0:
            out[ki] = [float(x) for x in v]
    return out if out else None


def _x_extent_from_removal_data(removal_data: Dict[str, List[Dict]]) -> Tuple[float, float]:
    xs: List[float] = []
    for pts in removal_data.values():
        for d in pts:
            xs.append(float(d.get("percent", 0)))
    if not xs:
        return 0.0, 100.0
    return float(min(xs)), float(max(xs))


def _normalize_smooth_window(window: int, n: int) -> int:
    """Нечётное окно rolling mean в [3, n]; при n < 3 — 1 (без эффекта в _smooth_1d)."""
    if n < 3:
        return 1
    w = int(window)
    if w < 3:
        w = 3
    if w % 2 == 0:
        w += 1
    return min(w, n if n % 2 == 1 else n - 1) or 1


def _smooth_1d(y: List[float], window: int) -> List[float]:
    """Центрированное скользящее среднее; NaN сохраняются на позициях, где среднее не определено."""
    arr = np.asarray(y, dtype=float)
    n = len(arr)
    if n < 3 or window <= 1:
        return [float(x) for x in arr]
    w_eff = _normalize_smooth_window(window, n)
    if w_eff < 3:
        return [float(x) for x in arr]
    s = pd.Series(arr)
    out = s.rolling(window=w_eff, center=True, min_periods=1).mean()
    return [float(v) for v in out.to_numpy()]


def plot_removal_impact(
    removal_data: Dict[str, List[Dict]],
    metric_info: Optional[Dict[str, Any]] = None,
    color_overrides: Optional[Dict[str, str]] = None,
    baseline_metric: Optional[float] = None,
    random_run_results: Optional[Dict[str, Any]] = None,
    *,
    smooth: bool = False,
    smooth_window: int = 5,
) -> go.Figure:
    """График removal (Plotly); color_overrides: имя серии → #RRGGBB."""
    fig = go.Figure()
    overrides = color_overrides or {}

    y_title = "Metric"
    if metric_info:
        y_title = metric_info.get("short_label_ru") or metric_info.get("name", y_title)

    rrr_by_pct = _parse_random_run_results(random_run_results)
    use_random_ribbon = (
        rrr_by_pct is not None
        and "random" in removal_data
    )

    if use_random_ribbon and rrr_by_pct is not None:
        pct_sorted = sorted(p for p in rrr_by_pct if p > 0)
        x_rb: List[float] = []
        y_hi: List[float] = []
        y_lo: List[float] = []
        y_med: List[float] = []
        for p in pct_sorted:
            vals = rrr_by_pct.get(p)
            if not vals:
                continue
            arr = np.asarray(vals, dtype=float)
            x_rb.append(float(p))
            y_hi.append(float(np.max(arr)))
            y_lo.append(float(np.min(arr)))
            y_med.append(float(np.median(arr)))
        if smooth and len(y_med) >= 3:
            w = smooth_window
            y_hi = _smooth_1d(y_hi, w)
            y_lo = _smooth_1d(y_lo, w)
            y_med = _smooth_1d(y_med, w)
        if len(x_rb) >= 1:
            band_color = "rgba(243, 156, 18, 0.35)"
            med_color = overrides.get("random") or default_color_for_removal_trace(
                "random"
            )
            fig.add_trace(
                go.Scatter(
                    x=x_rb,
                    y=y_hi,
                    mode="lines",
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=x_rb,
                    y=y_lo,
                    mode="lines",
                    line=dict(width=0),
                    fill="tonexty",
                    fillcolor=band_color,
                    name="random (min–max)",
                    legendgroup="random_band",
                    hovertemplate=(
                        f"<b>random spread</b><br>Removal: %{{x}}%<br>"
                        f"min {y_title}: %{{customdata[0]:.4f}}<br>"
                        f"max {y_title}: %{{customdata[1]:.4f}}<extra></extra>"
                    ),
                    customdata=np.column_stack([y_lo, y_hi]),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=x_rb,
                    y=y_med,
                    mode="lines+markers",
                    name="random (median)",
                    legendgroup="random_band",
                    line=dict(color=med_color, width=3.8),
                    marker=dict(size=9, color=med_color, line=dict(width=0)),
                    hovertemplate=(
                        f"<b>random (median)</b><br>Removal: %{{x}}%<br>{y_title}: "
                        "%{y:.4f}<extra></extra>"
                    ),
                )
            )

    for method, data_points in removal_data.items():
        if not data_points:
            continue
        if use_random_ribbon and method == "random":
            continue

        sorted_data = sorted(data_points, key=lambda x: x.get("percent", 0))
        percentages = [d.get("percent", 0) for d in sorted_data]
        yvals = []
        for d in sorted_data:
            v = d.get("metric")
            if v is None:
                v = d.get("mae")
            yvals.append(v)

        if smooth and len(yvals) >= 3:
            yvals = _smooth_1d(yvals, smooth_window)

        line_color = overrides.get(method) or default_color_for_removal_trace(method)
        sty = _plotly_line_marker_style(method, line_color)
        fig.add_trace(
            go.Scatter(
                x=percentages,
                y=yvals,
                name=method,
                line=sty["line"],
                marker=sty["marker"],
                mode=sty["mode"],
                hovertemplate=(
                    f"<b>%{{fullData.name}}</b><br>Removal: %{{x}}%<br>{y_title}: "
                    "%{y:.4f}<extra></extra>"
                ),
            )
        )

    if baseline_metric is not None:
        try:
            yb = float(baseline_metric)
            if np.isfinite(yb):
                x_lo, x_hi = _x_extent_from_removal_data(removal_data)
                fig.add_trace(
                    go.Scatter(
                        x=[x_lo, x_hi],
                        y=[yb, yb],
                        mode="lines",
                        name=f"Baseline (full training set): {yb:.4f}",
                        line=dict(color="#424242", width=2.2, dash="dot"),
                        legendgroup="baseline",
                        hovertemplate=(
                            f"<b>Baseline</b> (модель на полном train, 0% удаления)<br>"
                            f"{y_title}: %{{y:.4f}}<extra></extra>"
                        ),
                    )
                )
        except (TypeError, ValueError):
            pass

    fig.update_layout(
        title="Метрика при удалении данных",
        xaxis_title="Доля удалённых данных (%)",
        yaxis_title=y_title,
        hovermode="x unified",
        template="plotly_white",
        height=520,
        font=dict(size=12),
        # Запас справа и шрифт легенды — длинные имена методов (стратегии, суффиксы) не съедаются
        margin=dict(l=70, r=260, t=60, b=60),
        # Клики по легенде не скрывают кривые: иначе столбцы AUC (multiselect) перестают
        # соответствовать тому, что видно на линейном графике (Streamlit не видит клики легенды).
        legend=dict(
            traceorder="normal",
            itemsizing="constant",
            itemclick=False,
            itemdoubleclick=False,
            font=dict(size=11),
            xref="paper",
            x=1.01,
            xanchor="left",
            y=1,
            yanchor="top",
        ),
    )

    return fig


def _experiment_removal_suffix(e: Dict[str, Any]) -> str:
    """Фрагмент подписи: REMOVAL_ADAPTIVE и removal по классам, только если включены."""
    parts: List[str] = []
    if bool(e.get("removal_adaptive_model")):
        parts.append("REMOVAL_ADAPTIVE")
    if bool(e.get("removal_per_class")):
        parts.append("removal по классам")
    if bool(e.get("removal_stratify_target")):
        parts.append("removal страты по y")
    if not parts:
        return ""
    return "  ·  " + "  ·  ".join(parts)


def _experiment_list_label(e: Dict[str, Any]) -> str:
    """Подпись эксперимента в селекте: модель, sample %, датасет, дата."""
    eid = (e.get("experiment_id") or "")[:8]
    model = e.get("model") or e.get("model_type") or "?"
    ds = e.get("dataset") or "?"
    sp = e.get("sample_size_percentage")
    if sp is None:
        sp_s = "?"
    else:
        try:
            sp_s = f"{float(sp):g}%"
        except (TypeError, ValueError):
            sp_s = str(sp)
    date = str(e.get("created_at", ""))[:10]
    base = f"{eid}…  {model}  ·  sample {sp_s}  ·  {ds}  ·  {date}"
    extra = _experiment_removal_suffix(e)
    return base + extra if extra else base


def _stable_color_picker_key(experiment_id: str, method: str) -> str:
    h = hashlib.md5(f"{experiment_id}::{method}".encode()).hexdigest()[:14]
    return f"rpcp_{experiment_id[:8]}_{h}"


def _series_checkbox_key(experiment_id: str, method: str) -> str:
    """Стабильный key для st.checkbox по эксперименту и полному имени серии."""
    h = hashlib.md5(f"{experiment_id}::{method}".encode()).hexdigest()[:18]
    return f"srchk_{experiment_id[:12]}_{h}"


def _methods_selection_signature(methods: List[str]) -> str:
    """Короткий идентификатор выбора серий для key у plotly_chart (перерисовка при смене выбора)."""
    return hashlib.md5(repr(methods).encode("utf-8")).hexdigest()[:20]


# Бэкап полей формы: при смене страницы Streamlit сбрасывает session_state виджетов.
INF_FORM_BACKUP_KEY = "inf_experiment_form_backup"
INF_FORM_FORCE_RESTORE_KEY = "_inf_force_form_restore"
# Виджеты вне st.form — их можно безопасно дописывать в бэкап на каждом rerun.
INF_FORM_OUTSIDE_WIDGET_KEYS = (
    "ws_full_pipeline",
    "ws_removal_adaptive",
    "ws_removal_per_class",
    "ws_removal_stratify_target",
    "inf_removal_stratify_n_bins",
    "new_experiment_dataset",
    "inf_use_tfidf_lsa",
    "inf_lsa_components",
)


def _inf_form_persist_keys(
    all_methods: List[str], removal_strategy_keys: List[str]
) -> List[str]:
    keys = [
        "ws_full_pipeline",
        "ws_removal_adaptive",
        "ws_removal_per_class",
        "ws_removal_stratify_target",
        "inf_removal_stratify_n_bins",
        "inf_model_type",
        "inf_model_architecture",
        "inf_model_fit_mode",
        "inf_primary_metric",
        "inf_sample_size",
        "inf_test_size",
        "inf_val_size",
        "inf_n_epochs",
        "inf_n_retrain_runs",
        "inf_random_state",
        "inf_device",
        "inf_n_jobs",
        "inf_use_cache",
        "inf_removal_range",
        "inf_removal_num_pts",
        "inf_n_random_runs",
        "inf_loss_high",
        "inf_loss_low",
        "inf_use_catboost_influence",
        "inf_show_top_bottom_influence",
        "inf_use_distillation",
        "inf_distillation_epochs",
        "inf_distillation_temperature",
        "inf_student_architecture",
        "inf_ip_reg",
        "inf_ip_bs",
        "inf_ip_vbs",
        "inf_lissa_scale",
        "inf_lissa_damp",
        "inf_cg_maxiter",
        "inf_cg_tol",
        "inf_arnoldi_rank",
        "inf_nyst_rank",
        "inf_debug_mode",
        "inf_fe_under",
        "inf_fe_over",
        "inf_overrides_json",
        "new_experiment_dataset",
        "inf_use_tfidf_lsa",
        "inf_lsa_components",
    ]
    keys.extend(f"method_{m}" for m in all_methods)
    keys.extend(f"rs_{k}" for k in removal_strategy_keys)
    return keys


def _seed_inf_form_backup_if_empty(
    *,
    models: List[str],
    all_methods: List[str],
    removal_strategy_keys: List[str],
    default_removal: List[str],
    selected_row: Dict[str, Any],
) -> None:
    """Однократное заполнение бэкапа дефолтами из settings (если бэкап ещё пустой)."""
    from config.settings import (
        PYDVL_CONFIG,
        MODEL_RUN_CONFIG,
        EXPERIMENT_CONFIG,
        DISTILLATION_CONFIG,
        DATASET_INFLUENCE_PARAMS,
        MODEL_FIT_MODE as DEFAULT_MODEL_FIT_MODE,
        RANDOM_STATE as DEFAULT_RANDOM_STATE,
        N_JOBS as DEFAULT_N_JOBS,
        FIT_MODE_EPOCHS as DEFAULT_FIT_MODE_EPOCHS,
        USE_CACHE as DEFAULT_USE_CACHE,
    )

    if INF_FORM_BACKUP_KEY not in st.session_state:
        st.session_state[INF_FORM_BACKUP_KEY] = {}
    b = st.session_state[INF_FORM_BACKUP_KEY]
    if b:
        return

    ds_name = selected_row["name"]
    _ip_base = copy.deepcopy(
        DATASET_INFLUENCE_PARAMS.get(ds_name, PYDVL_CONFIG["influence_params"])
    )
    _pydvl_ip = PYDVL_CONFIG["influence_params"]
    lp = _ip_base.get("lissa_params", _pydvl_ip["lissa_params"])
    cp = _ip_base.get("cg_params", _pydvl_ip["cg_params"])
    ap = _ip_base.get("arnoldi_params", _pydvl_ip["arnoldi_params"])
    np_ = _ip_base.get("nystroem_params", _pydvl_ip["nystroem_params"])
    arch_choices = ["simple", "improved", "ft_transformer", "ft_transformer_simple", "cnn_small"]
    default_arch = MODEL_RUN_CONFIG.get("model_architecture", "simple")
    _lin = EXPERIMENT_CONFIG.get("n_remove_linspace", (1, 90, 10))

    b["ws_full_pipeline"] = False
    b["ws_removal_adaptive"] = False
    b["ws_removal_per_class"] = bool(MODEL_RUN_CONFIG.get("removal_per_class", False))
    b["ws_removal_stratify_target"] = bool(
        MODEL_RUN_CONFIG.get("removal_stratify_target", False)
    )
    b["inf_removal_stratify_n_bins"] = int(
        MODEL_RUN_CONFIG.get("removal_stratify_n_bins", 10) or 10
    )
    b["inf_model_type"] = models[0] if models else "random_forest"
    b["inf_model_architecture"] = (
        default_arch if default_arch in arch_choices else arch_choices[0]
    )
    fit_choices = ["normal", "underfit", "overfit"]
    b["inf_model_fit_mode"] = (
        DEFAULT_MODEL_FIT_MODE
        if DEFAULT_MODEL_FIT_MODE in fit_choices
        else fit_choices[0]
    )
    b["inf_primary_metric"] = selected_row["default_metric"]
    b["inf_sample_size"] = int(EXPERIMENT_CONFIG.get("sample_size_percentage", 100))
    b["inf_test_size"] = float(EXPERIMENT_CONFIG.get("test_size", 0.2))
    b["inf_val_size"] = float(EXPERIMENT_CONFIG.get("val_size", 0.1))
    b["inf_n_epochs"] = int(EXPERIMENT_CONFIG.get("n_epochs", 500))
    b["inf_n_retrain_runs"] = int(EXPERIMENT_CONFIG.get("n_retrain_runs", 3))
    b["inf_random_state"] = int(DEFAULT_RANDOM_STATE)
    b["inf_device"] = "cuda"
    b["inf_n_jobs"] = int(DEFAULT_N_JOBS)
    b["inf_use_cache"] = bool(DEFAULT_USE_CACHE)
    b["inf_removal_range"] = (int(_lin[0]), int(_lin[1]))
    b["inf_removal_num_pts"] = int(_lin[2])
    b["inf_n_random_runs"] = int(EXPERIMENT_CONFIG.get("n_random_runs", 3))
    b["inf_loss_high"] = "loss_high" in (EXPERIMENT_CONFIG.get("loss_removal_methods") or [])
    b["inf_loss_low"] = "loss_low" in (EXPERIMENT_CONFIG.get("loss_removal_methods") or [])
    b["inf_use_catboost_influence"] = bool(
        EXPERIMENT_CONFIG.get("use_catboost_influence", False)
    )
    tb = EXPERIMENT_CONFIG.get("show_top_bottom_influence", 0)
    b["inf_show_top_bottom_influence"] = int((tb or 0) if tb is not False else 0)
    b["inf_use_distillation"] = bool(DISTILLATION_CONFIG.get("use_distillation", False))
    b["inf_distillation_epochs"] = int(DISTILLATION_CONFIG.get("distillation_epochs", 500))
    b["inf_distillation_temperature"] = float(DISTILLATION_CONFIG.get("temperature", 2.0))
    sa_choices = ["simple", "improved"]
    sa_def = DISTILLATION_CONFIG.get("student_architecture", "simple")
    b["inf_student_architecture"] = sa_def if sa_def in sa_choices else sa_choices[0]
    b["inf_ip_reg"] = float(_ip_base.get("regularization", _pydvl_ip["regularization"]))
    b["inf_ip_bs"] = int(_ip_base.get("batch_size", _pydvl_ip["batch_size"]))
    b["inf_ip_vbs"] = int(
        _ip_base.get(
            "influence_val_batch_size",
            _pydvl_ip.get("influence_val_batch_size", 500),
        )
    )
    b["inf_lissa_scale"] = int(lp.get("scale", 10))
    b["inf_lissa_damp"] = float(lp.get("damping", 0.1))
    b["inf_cg_maxiter"] = int(cp.get("maxiter", 100))
    b["inf_cg_tol"] = float(cp.get("tolerance", 1e-2))
    b["inf_arnoldi_rank"] = int(ap.get("rank", 10))
    b["inf_nyst_rank"] = int(np_.get("rank", 10))
    b["inf_debug_mode"] = False
    b["inf_fe_under"] = int(DEFAULT_FIT_MODE_EPOCHS.get("underfit", 10))
    b["inf_fe_over"] = int(DEFAULT_FIT_MODE_EPOCHS.get("overfit", 5000))
    b["inf_overrides_json"] = ""
    for m in all_methods:
        b[f"method_{m}"] = False
    for rk in removal_strategy_keys:
        b[f"rs_{rk}"] = rk in default_removal


def _mark_inf_form_restore_needed() -> None:
    """После остановки/завершения эксперимента — принудительно подтянуть бэкап в виджеты."""
    st.session_state[INF_FORM_FORCE_RESTORE_KEY] = True


def _restore_inf_form_widgets_from_backup(
    all_methods: List[str],
    removal_strategy_keys: List[str],
    *,
    force: bool = False,
) -> None:
    """Восстановить ключи виджетов из бэкапа (после размонтирования st.form)."""
    if INF_FORM_BACKUP_KEY not in st.session_state:
        return
    b = st.session_state[INF_FORM_BACKUP_KEY]
    for k in _inf_form_persist_keys(all_methods, removal_strategy_keys):
        if k in b and (force or k not in st.session_state):
            st.session_state[k] = copy.deepcopy(b[k])


def _apply_inf_form_backup_overrides(overrides: Dict[str, Any]) -> None:
    """Записать значения только в бэкап (не в session_state виджетов).

    После submit формы ключи виджетов уже синхронизированы Streamlit'ом;
    повторная запись в session_state после создания виджетов даёт StreamlitAPIException.
  """
    if INF_FORM_BACKUP_KEY not in st.session_state:
        st.session_state[INF_FORM_BACKUP_KEY] = {}
    b = st.session_state[INF_FORM_BACKUP_KEY]
    for k, v in overrides.items():
        b[k] = copy.deepcopy(v)


def _persist_inf_form_outside_widgets() -> None:
    """Сохранить только виджеты вне st.form (их state обновляется без submit)."""
    if INF_FORM_BACKUP_KEY not in st.session_state:
        st.session_state[INF_FORM_BACKUP_KEY] = {}
    b = st.session_state[INF_FORM_BACKUP_KEY]
    for k in INF_FORM_OUTSIDE_WIDGET_KEYS:
        if k in st.session_state:
            b[k] = copy.deepcopy(st.session_state[k])


def _persist_inf_form_backup(
    all_methods: List[str], removal_strategy_keys: List[str]
) -> None:
    """Сохранить session_state в бэкап (для ключей, уже попавших в state)."""
    if INF_FORM_BACKUP_KEY not in st.session_state:
        st.session_state[INF_FORM_BACKUP_KEY] = {}
    b = st.session_state[INF_FORM_BACKUP_KEY]
    for k in _inf_form_persist_keys(all_methods, removal_strategy_keys):
        if k in st.session_state:
            b[k] = copy.deepcopy(st.session_state[k])
    _persist_inf_form_outside_widgets()


def _render_inf_form_backup_summary(
    all_methods: List[str], removal_strategy_keys: List[str]
) -> None:
    """Краткий обзор параметров из бэкапа (без st.form — иначе ломается «Остановить» при autorefresh)."""
    b = st.session_state.get(INF_FORM_BACKUP_KEY) or {}
    if not b:
        st.info("Параметры запуска ещё не сохранены.")
        return
    with st.expander("Параметры текущего запуска", expanded=True):
        st.markdown(f"**Датасет:** `{b.get('new_experiment_dataset', '—')}`")
        st.markdown(
            f"**Модель:** `{b.get('inf_model_type', '—')}` · "
            f"`{b.get('inf_model_architecture', '—')}` · fit `{b.get('inf_model_fit_mode', '—')}`"
        )
        st.markdown(f"**Метрика:** `{b.get('inf_primary_metric', '—')}`")
        if b.get("ws_full_pipeline"):
            st.markdown("**Режим:** полный пайплайн (influence + removal)")
            rs = [k for k in removal_strategy_keys if b.get(f"rs_{k}")]
            if rs:
                st.markdown(f"**Removal strategies:** {', '.join(rs)}")
            _rr = b.get("inf_removal_range")
            _np = b.get("inf_removal_num_pts")
            if _rr is not None and _np is not None:
                st.markdown(
                    f"**Сетка удаления:** {_rr[0]}–{_rr[1]} %, {_np} точек · "
                    f"n_random_runs={b.get('inf_n_random_runs', '—')}"
                )
        else:
            st.markdown("**Режим:** только influence")
        if b.get("inf_use_distillation"):
            st.markdown(
                f"**Дистилляция:** да · epochs={b.get('inf_distillation_epochs')} · "
                f"T={b.get('inf_distillation_temperature')} · "
                f"student={b.get('inf_student_architecture')}"
            )
        methods = [m for m in all_methods if b.get(f"method_{m}")]
        if methods:
            st.caption(f"Valuation / influence: {', '.join(methods)}")
        else:
            st.caption("Valuation / influence: не выбраны")


def render_top_nav() -> str:
    """Верхняя навигация; возвращает ключ активной страницы."""
    if "main_page" not in st.session_state:
        st.session_state.main_page = "workspace"
    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    with c1:
        if st.button("Рабочая область", key="nav_workspace", use_container_width=True):
            st.session_state.main_page = "workspace"
            st.rerun()
    with c2:
        if st.button("Анализ", key="nav_analysis", use_container_width=True):
            st.session_state.main_page = "analysis"
            st.rerun()
    with c3:
        if st.button("Настройки", key="nav_settings", use_container_width=True):
            st.session_state.main_page = "settings"
            st.rerun()
    with c4:
        if st.button(
            "Обновить кэш API",
            key="top_clear_api_cache",
            help="Сбросить кэш списков экспериментов и графиков.",
        ):
            st.cache_data.clear()
            st.rerun()
    st.caption("")
    return st.session_state.main_page


def render_experiment_tree() -> None:
    """Левая панель: родительские эксперименты и дочерние removal."""
    _delete_btn_icon = "\U0001f5d1"
    st.subheader("Эксперименты")
    if _cached_api_health_ok(API_BASE_URL):
        st.caption("API: OK")
    else:
        st.caption("API: нет соединения")

    response = _cached_api_experiments_list(API_BASE_URL)
    if not response or not response.get("experiments"):
        st.info("Пока нет экспериментов.")
        return

    experiments = list(response["experiments"])
    exp_ids = {e["experiment_id"] for e in experiments}
    sel_cur = st.session_state.get("selected_experiment_id")
    if sel_cur and sel_cur not in exp_ids:
        parents_fix = [
            e for e in experiments if not e.get("parent_experiment_id")
        ]
        parents_fix.sort(key=lambda x: str(x.get("created_at") or ""), reverse=True)
        st.session_state.selected_experiment_id = (
            parents_fix[0]["experiment_id"] if parents_fix else None
        )

    pending_del = st.session_state.get("tree_pending_delete_id")
    if pending_del:
        st.warning(
            f"Удалить эксперимент `{pending_del[:8]}…`? Папка на сервере будет удалена."
        )
        dc1, dc2 = st.columns(2)
        if dc1.button("Да, удалить", key="tree_del_confirm_yes"):
            if make_api_request("DELETE", f"/experiments/{pending_del}"):
                st.session_state.tree_pending_delete_id = None
                if st.session_state.get("selected_experiment_id") == pending_del:
                    st.session_state.selected_experiment_id = None
                st.cache_data.clear()
                st.rerun()
        if dc2.button("Отмена", key="tree_del_confirm_no"):
            st.session_state.tree_pending_delete_id = None
            st.rerun()

    children_by_parent: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    parents: List[Dict[str, Any]] = []
    for e in experiments:
        pid = e.get("parent_experiment_id")
        if pid:
            children_by_parent[str(pid)].append(e)
        else:
            parents.append(e)

    parents.sort(key=lambda x: str(x.get("created_at") or ""), reverse=True)

    if "selected_experiment_id" not in st.session_state and parents:
        st.session_state.selected_experiment_id = parents[0]["experiment_id"]

    for p in parents:
        eid = p["experiment_id"]
        plab = _experiment_list_label(p)
        kids = sorted(
            children_by_parent.get(eid, []),
            key=lambda x: str(x.get("created_at") or ""),
            reverse=True,
        )

        with st.container(border=True):
            st.caption("Базовый эксперимент · influence")
            sel = st.session_state.get("selected_experiment_id") == eid
            running_p = str(p.get("status") or "").lower() == "running"
            b1, b_actions = st.columns([1, 0.36])
            with b1:
                if st.button(
                    plab,
                    key=f"tree_p_{eid}",
                    use_container_width=True,
                    type="primary" if sel else "secondary",
                ):
                    st.session_state.selected_experiment_id = eid
                    st.rerun()
            with b_actions:
                if running_p:
                    b_stop, b_del = st.columns(2)
                    with b_stop:
                        if st.button(
                            "Стоп",
                            key=f"tree_p_stop_{eid}",
                            help="Остановить эксперимент",
                            use_container_width=True,
                        ):
                            make_api_request("POST", f"/experiments/{eid}/cancel")
                            st.cache_data.clear()
                            st.rerun()
                    with b_del:
                        if st.button(
                            _delete_btn_icon,
                            key=f"tree_p_del_{eid}",
                            help="Удалить эксперимент",
                            use_container_width=True,
                        ):
                            st.session_state.tree_pending_delete_id = eid
                            st.rerun()
                else:
                    if st.button(
                        _delete_btn_icon,
                        key=f"tree_p_del_{eid}",
                        help="Удалить эксперимент",
                        use_container_width=True,
                    ):
                        st.session_state.tree_pending_delete_id = eid
                        st.rerun()

            if kids:
                with st.expander(
                    f"Подэксперименты removal · {len(kids)}",
                    expanded=False,
                ):
                    st.caption("Прогоны удаления данных относительно этого базового эксперимента.")
                    for ch in kids:
                        cid = ch["experiment_id"]
                        clab = _experiment_list_label(ch)
                        sel_c = st.session_state.get("selected_experiment_id") == cid
                        running_c = str(ch.get("status") or "").lower() == "running"
                        c1, c_actions = st.columns([1, 0.36])
                        with c1:
                            if st.button(
                                clab,
                                key=f"tree_c_{cid}",
                                use_container_width=True,
                                type="primary" if sel_c else "secondary",
                            ):
                                st.session_state.selected_experiment_id = cid
                                st.rerun()
                        with c_actions:
                            if running_c:
                                c_stop, c_del = st.columns(2)
                                with c_stop:
                                    if st.button(
                                        "Стоп",
                                        key=f"tree_c_stop_{cid}",
                                        help="Остановить эксперимент",
                                        use_container_width=True,
                                    ):
                                        make_api_request("POST", f"/experiments/{cid}/cancel")
                                        st.cache_data.clear()
                                        st.rerun()
                                with c_del:
                                    if st.button(
                                        _delete_btn_icon,
                                        key=f"tree_c_del_{cid}",
                                        help="Удалить эксперимент",
                                        use_container_width=True,
                                    ):
                                        st.session_state.tree_pending_delete_id = cid
                                        st.rerun()
                            else:
                                if st.button(
                                    _delete_btn_icon,
                                    key=f"tree_c_del_{cid}",
                                    help="Удалить эксперимент",
                                    use_container_width=True,
                                ):
                                    st.session_state.tree_pending_delete_id = cid
                                    st.rerun()


def page_workspace_removal() -> None:
    """Отдельный прогон removal от выбранного родителя."""
    from config.settings import EXPERIMENT_CONFIG, MODEL_RUN_CONFIG

    st.subheader("Removal (отдельный прогон)")
    st.caption(
        "Использует сохранённые веса influence родителя. В дереве слева выберите "
        "строку «Базовый эксперимент» в нужном блоке (не подэксперимент removal) и нажмите «Запуск removal»."
    )

    parent_id = st.session_state.get("selected_experiment_id")
    response = _cached_api_experiments_list(API_BASE_URL)
    experiments = (response or {}).get("experiments") or []
    by_id = {e["experiment_id"]: e for e in experiments}
    if parent_id and by_id.get(parent_id, {}).get("parent_experiment_id"):
        st.warning("Сейчас выбран дочерний removal-эксперимент. Выберите родителя в дереве слева.")
        parent_id = None

    if not parent_id or parent_id not in by_id:
        st.info(
            "Выберите базовый эксперимент в дереве слева. "
            "После выбора здесь появится форма с опцией «Адаптивный removal»."
        )
        return

    p = by_id[parent_id]
    st.markdown(f"**Родитель:** `{parent_id}` — {_experiment_list_label(p)}")

    parent_task_type = _task_type_for_experiment_list_row(p)
    show_removal_per_class_rem = _is_classification_task_type(parent_task_type)
    show_removal_stratify_rem = _is_regression_task_type(parent_task_type)

    removal_strategy_keys = [
        "lowest",
        "highest",
        "random",
        "extremes",
        "median",
        "few_bad_then_random",
        "few_median_then_random",
        "few_good_then_random",
    ]
    default_removal = list(
        EXPERIMENT_CONFIG.get("removal_strategies") or ["lowest", "highest", "random", "extremes"]
    )
    for _rk in removal_strategy_keys:
        _rsk = f"rem_rs_{_rk}"
        if _rsk not in st.session_state:
            st.session_state[_rsk] = _rk in default_removal

    with st.form("removal_child_form"):
        rcols = st.columns(4)
        removal_selected: List[str] = []
        for i, key in enumerate(removal_strategy_keys):
            with rcols[i % 4]:
                if st.checkbox(key, key=f"rem_rs_{key}"):
                    removal_selected.append(key)

        c_rm1, c_rm2 = st.columns(2)
        with c_rm1:
            removal_range = st.slider(
                "Диапазон % удаления",
                1,
                99,
                (
                    int(EXPERIMENT_CONFIG.get("n_remove_linspace", (1, 90, 10))[0]),
                    int(EXPERIMENT_CONFIG.get("n_remove_linspace", (1, 90, 10))[1]),
                ),
                1,
                key="rem_removal_range",
            )
        with c_rm2:
            num_removal_percentages = st.number_input(
                "Число точек сетки",
                min_value=2,
                max_value=100,
                value=int(EXPERIMENT_CONFIG.get("n_remove_linspace", (1, 90, 10))[2]),
                key="rem_num_pts",
            )
        n_remove_percentages = [
            int(x)
            for x in np.linspace(
                removal_range[0], removal_range[1], num_removal_percentages, dtype=int
            )
        ]
        n_random_runs = st.slider(
            "n_random_runs",
            1,
            50,
            int(EXPERIMENT_CONFIG.get("n_random_runs", 3)),
            key="rem_n_random_runs",
        )
        st.markdown("**Адаптивная модель**")
        st.checkbox(
            "Адаптивный removal: снижать ёмкость модели при меньшем train",
            value=False,
            key="rem_removal_adaptive",
            help="На каждом шаге removal: при меньшем train — проще архитектура / деревья (REMOVAL_ADAPTIVE_CONFIG).",
        )
        if show_removal_per_class_rem:
            st.checkbox(
                "Removal по классам",
                value=False,
                key="rem_removal_per_class",
                help="Ранжирование и удаление отдельно внутри каждого класса (доля по классам пропорциональна размеру).",
            )
        if show_removal_stratify_rem:
            st.checkbox(
                "Removal со стратификацией по целевой (квантильные бины)",
                value=False,
                key="rem_removal_stratify_target",
                help="Как removal по классам, но для регрессии: страты по квантилям y, доля удалений пропорциональна размеру страты.",
            )
            st.number_input(
                "Число квантильных бинов по y",
                min_value=2,
                max_value=100,
                value=int(
                    st.session_state.get(
                        "rem_removal_stratify_n_bins",
                        MODEL_RUN_CONFIG.get("removal_stratify_n_bins", 10) or 10,
                    )
                ),
                key="rem_removal_stratify_n_bins",
            )

        submitted = st.form_submit_button("Запуск removal", type="primary")

    if submitted:
        if not removal_selected:
            st.error("Выберите хотя бы одну стратегию removal.")
            return
        if "lowest" in removal_selected:
            removal_strategy = "remove_lowest_influence"
        elif "highest" in removal_selected:
            removal_strategy = "remove_highest_influence"
        else:
            removal_strategy = "remove_lowest_influence"

        body = {
            "removal_strategies": removal_selected,
            "n_remove_percentages": n_remove_percentages,
            "n_random_runs": int(n_random_runs),
            "removal_strategy": removal_strategy,
            "removal_adaptive_model": bool(st.session_state.get("rem_removal_adaptive", False)),
            "removal_per_class": (
                bool(st.session_state.get("rem_removal_per_class", False))
                if show_removal_per_class_rem
                else False
            ),
            "removal_stratify_target": (
                bool(st.session_state.get("rem_removal_stratify_target", False))
                if show_removal_stratify_rem
                else False
            ),
            "removal_stratify_n_bins": (
                int(st.session_state.get("rem_removal_stratify_n_bins", 10))
                if show_removal_stratify_rem
                else MODEL_RUN_CONFIG.get("removal_stratify_n_bins", 10)
            ),
        }
        st.session_state[PENDING_REMOVAL_START_KEY] = {
            "parent_id": parent_id,
            "body": body,
        }
        st.rerun()


def page_workspace() -> None:
    _process_pending_influence_start()
    _process_pending_removal_start()
    _render_workspace_active_poll()
    tab_inf, tab_rem = st.tabs(["Influence", "Removal"])
    with tab_inf:
        page_new_experiment()
    with tab_rem:
        page_workspace_removal()


def page_new_experiment():
    """Новый эксперимент; поля соответствуют config/settings.py и config_merge."""
    from config.settings import (
        PYDVL_CONFIG,
        METRIC_CONFIG,
        MODEL_RUN_CONFIG,
        EXPERIMENT_CONFIG,
        DISTILLATION_CONFIG,
        DATASET_INFLUENCE_PARAMS,
        MODEL_FIT_MODE as DEFAULT_MODEL_FIT_MODE,
        RANDOM_STATE as DEFAULT_RANDOM_STATE,
        N_JOBS as DEFAULT_N_JOBS,
        FIT_MODE_EPOCHS as DEFAULT_FIT_MODE_EPOCHS,
        USE_CACHE as DEFAULT_USE_CACHE,
    )

    st.title("Новый эксперимент")

    poll_running = bool(_resolve_workspace_influence_poll_id())
    form_collapsed = bool(st.session_state.get(WORKSPACE_FORM_COLLAPSED_KEY, False))

    models = get_available_models()

    all_methods = [
        "LOO",
        "DataShapley",
        "BetaShapley",
        "Banzhaf",
        "TMCShapley",
        "KNNShapley",
        "DataOOB",
        "LeastCore",
        "Influence",
        "ArnoldiInfluence",
        "CgInfluence",
        "LissaInfluence",
        "NystroemSketchInfluence",
    ]

    removal_strategy_keys = [
        "lowest",
        "highest",
        "random",
        "extremes",
        "median",
        "few_bad_then_random",
        "few_median_then_random",
        "few_good_then_random",
    ]
    default_removal = list(MODEL_RUN_CONFIG.get("removal_strategies") or ["lowest", "highest", "random", "extremes"])

    dataset_rows = build_dataset_rows_with_metrics(METRIC_CONFIG)
    if not dataset_rows:
        st.error("Нет зарегистрированных датасетов.")
        return

    _names_ok = {r["name"] for r in dataset_rows}
    if "new_experiment_dataset" not in st.session_state:
        _b_ds = (st.session_state.get(INF_FORM_BACKUP_KEY) or {}).get(
            "new_experiment_dataset"
        )
        if _b_ds and _b_ds in _names_ok:
            st.session_state.new_experiment_dataset = _b_ds
        else:
            st.session_state.new_experiment_dataset = dataset_rows[0]["name"]
    elif st.session_state.new_experiment_dataset not in _names_ok:
        st.session_state.new_experiment_dataset = dataset_rows[0]["name"]

    _seed_row = next(
        r
        for r in dataset_rows
        if r["name"] == st.session_state.new_experiment_dataset
    )
    _seed_inf_form_backup_if_empty(
        models=models,
        all_methods=all_methods,
        removal_strategy_keys=removal_strategy_keys,
        default_removal=default_removal,
        selected_row=_seed_row,
    )
    _force_restore = bool(st.session_state.pop(INF_FORM_FORCE_RESTORE_KEY, False))
    _restore_inf_form_widgets_from_backup(
        all_methods, removal_strategy_keys, force=_force_restore
    )

    if poll_running and form_collapsed:
        st.markdown("---")
        _render_inf_form_backup_summary(all_methods, removal_strategy_keys)
        if st.button(
            "Развернуть параметры",
            key="ws_expand_form_during_poll",
            help="Показать полную форму; панель прогресса останется сверху.",
        ):
            st.session_state[WORKSPACE_FORM_COLLAPSED_KEY] = False
            st.rerun()
        return

    if poll_running:
        st.markdown("---")
        _pc1, _pc2 = st.columns([3, 1])
        with _pc1:
            st.caption(
                "Эксперимент выполняется — прогресс и «Остановить» выше. "
                "Ниже можно менять параметры следующего запуска."
            )
        with _pc2:
            if st.button(
                "Свернуть параметры",
                key="ws_collapse_form_during_poll",
                use_container_width=True,
                help="Оставить только панель прогресса и краткую сводку.",
            ):
                st.session_state[WORKSPACE_FORM_COLLAPSED_KEY] = True
                st.rerun()

    st.subheader("1. Датасет")
    st.caption("Тип задачи и объём — оценочно; в пункте 3 доступна только метрика, подходящая к задаче.")
    _ncols = 3
    _grid = st.columns(_ncols)
    for _i, _r in enumerate(dataset_rows):
        with _grid[_i % _ncols]:
            _sel = st.session_state.new_experiment_dataset == _r["name"]
            st.caption(f"{_r['task_label_ru']} · {_r['size_display']}")
            if st.button(
                _r["name"],
                key=f"pick_dataset_{_r['name']}",
                use_container_width=True,
                type="primary" if _sel else "secondary",
            ):
                st.session_state.new_experiment_dataset = _r["name"]
                if INF_FORM_BACKUP_KEY not in st.session_state:
                    st.session_state[INF_FORM_BACKUP_KEY] = {}
                st.session_state[INF_FORM_BACKUP_KEY][
                    "new_experiment_dataset"
                ] = _r["name"]
                st.rerun()

    selected_row = next(
        r for r in dataset_rows if r["name"] == st.session_state.new_experiment_dataset
    )
    selected_dataset = selected_row["name"]

    _pm_key = "inf_primary_metric"
    _mopts_cur = selected_row["metrics_allowed"]
    _mdef_cur = selected_row["default_metric"]
    if _pm_key in st.session_state and st.session_state[_pm_key] not in _mopts_cur:
        st.session_state[_pm_key] = _mdef_cur

    # Вне формы: виджеты внутри st.form не обновляют session_state до submit, поэтому
    # при ws_full_pipeline внутри формы блок «6. Removal» никогда не показывался до отправки.
    st.checkbox(
        "Полный пайплайн (influence + removal в одном запуске)",
        value=False,
        key="ws_full_pipeline",
        help="Выключено: только подсчёт influence; removal — на вкладке «Removal».",
    )
    st.checkbox(
        "Адаптивный removal: снижать ёмкость модели при меньшем train",
        value=False,
        key="ws_removal_adaptive",
        help="На каждом шаге removal при меньшем train — проще архитектура PyTorch / деревья (см. REMOVAL_ADAPTIVE_CONFIG в settings). Учитывается только при включённом полном пайплайне.",
    )
    if _is_classification_task_type(selected_row["task_type"]):
        st.checkbox(
            "Removal по классам: ранжировать influence и удалять долю внутри каждого класса",
            value=bool(MODEL_RUN_CONFIG.get("removal_per_class", False)),
            key="ws_removal_per_class",
            help="Удаление не по одному глобальному рангу по всей выборке, а отдельно внутри каждого класса (доля удалений пропорциональна размеру класса).",
        )
    elif _is_regression_task_type(selected_row["task_type"]):
        st.checkbox(
            "Removal со стратификацией по целевой: квантильные страты по y",
            value=bool(MODEL_RUN_CONFIG.get("removal_stratify_target", False)),
            key="ws_removal_stratify_target",
            help="Аналог removal по классам: ранжирование и доля удалений отдельно внутри каждой страты (квантили целевой переменной).",
        )
        st.number_input(
            "Число квантильных бинов по y",
            min_value=2,
            max_value=100,
            value=int(MODEL_RUN_CONFIG.get("removal_stratify_n_bins", 10) or 10),
            key="inf_removal_stratify_n_bins",
        )

    use_tfidf_lsa = False
    lsa_components = 200
    if selected_dataset == "imdb":
        st.markdown("**TF-IDF / LSA**")
        c_lsa1, c_lsa2 = st.columns([1, 2])
        with c_lsa1:
            use_tfidf_lsa = st.checkbox(
                "Сжать TF-IDF (LSA)",
                value=False,
                key="inf_use_tfidf_lsa",
                help="Применить TruncatedSVD к TF-IDF-матрице IMDB для уменьшения размерности.",
            )
        with c_lsa2:
            lsa_components = st.slider(
                "LSA компоненты",
                50,
                500,
                200,
                10,
                key="inf_lsa_components",
                disabled=not use_tfidf_lsa,
                help="Выберите число компонент для TruncatedSVD (рекомендуется 100–300).",
            )

    with st.form("experiment_form"):
        st.markdown(f"**Выбран датасет:** `{selected_dataset}`")

        st.subheader("2. Модель (MODEL_RUN_CONFIG)")
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1:
            model_type = st.selectbox("model_type", models, key="inf_model_type")
        with c_m2:
            arch_choices = ["simple", "improved", "ft_transformer", "ft_transformer_simple", "cnn_small"]
            default_arch = MODEL_RUN_CONFIG.get("model_architecture", "simple")
            arch_idx = arch_choices.index(default_arch) if default_arch in arch_choices else 0
            model_architecture = st.selectbox(
                "model_architecture (PyTorch / distillation)",
                arch_choices,
                index=arch_idx,
                key="inf_model_architecture",
            )
        with c_m3:
            fit_choices = ["normal", "underfit", "overfit"]
            fit_idx = fit_choices.index(DEFAULT_MODEL_FIT_MODE) if DEFAULT_MODEL_FIT_MODE in fit_choices else 0
            model_fit_mode = st.selectbox(
                "MODEL_FIT_MODE", fit_choices, index=fit_idx, key="inf_model_fit_mode"
            )

        st.subheader("3. Метрики (METRIC_CONFIG)")
        _tt = selected_row["task_type"]
        _mopts = selected_row["metrics_allowed"]
        _mdef = selected_row["default_metric"]
        _midx = _mopts.index(_mdef) if _mdef in _mopts else 0
        primary_metric = st.selectbox(
            f"Метрика ({_TASK_LABEL_RU_UI.get(_tt, _tt)})",
            _mopts,
            index=_midx,
            key=_pm_key,
            help="Список ограничен типом задачи датасета и допустимыми значениями API.",
        )

        st.subheader("4. Данные и обучение (EXPERIMENT_CONFIG)")
        c_d1, c_d2, c_d3 = st.columns(3)
        with c_d1:
            sample_size = st.slider(
                "sample_size_percentage",
                1,
                100,
                int(EXPERIMENT_CONFIG.get("sample_size_percentage", 100)),
                key="inf_sample_size",
            )
        with c_d2:
            test_size = st.slider(
                "test_size",
                0.1,
                0.5,
                float(EXPERIMENT_CONFIG.get("test_size", 0.2)),
                0.01,
                key="inf_test_size",
            )
        with c_d3:
            val_size = st.slider(
                "val_size",
                0.05,
                0.3,
                float(EXPERIMENT_CONFIG.get("val_size", 0.1)),
                0.01,
                key="inf_val_size",
            )

        c_t1, c_t2, c_t3 = st.columns(3)
        with c_t1:
            n_epochs = st.slider(
                "n_epochs",
                10,
                5000,
                int(EXPERIMENT_CONFIG.get("n_epochs", 500)),
                1,
                key="inf_n_epochs",
            )
        with c_t2:
            n_retrain_runs = st.number_input(
                "n_retrain_runs (PyTorch)",
                min_value=1,
                max_value=20,
                value=int(EXPERIMENT_CONFIG.get("n_retrain_runs", 3)),
                help="Несколько переобучений, лучший run (см. EXPERIMENT_CONFIG)",
                key="inf_n_retrain_runs",
            )
        with c_t3:
            random_state = st.number_input(
                "RANDOM_STATE",
                0,
                100000,
                int(DEFAULT_RANDOM_STATE),
                key="inf_random_state",
            )

        st.subheader("5. Среда (DEVICE, N_JOBS, USE_CACHE)")
        c_e1, c_e2, c_e3 = st.columns(3)
        with c_e1:
            device_choice = st.selectbox(
                "DEVICE", ["cpu", "cuda"], index=1, key="inf_device"
            )
        with c_e2:
            n_jobs_ui = st.number_input(
                "N_JOBS", 1, 64, int(DEFAULT_N_JOBS), key="inf_n_jobs"
            )
        with c_e3:
            use_cache_ui = st.checkbox(
                "USE_CACHE", value=bool(DEFAULT_USE_CACHE), key="inf_use_cache"
            )

        if st.session_state.get("ws_full_pipeline", False):
            st.subheader("6. Removal: стратегии и сетка процентов")
            st.caption(
                "Соответствует MODEL_RUN_CONFIG['removal_strategies']; стратегия «random» включает случайный baseline. "
                "Адаптивная модель задаётся переключателем под «Полным пайплайном»."
            )
            rcols = st.columns(4)
            removal_selected = []
            for i, key in enumerate(removal_strategy_keys):
                with rcols[i % 4]:
                    if st.checkbox(key, key=f"rs_{key}"):
                        removal_selected.append(key)

            c_rm1, c_rm2 = st.columns(2)
            with c_rm1:
                removal_range = st.slider(
                    "Диапазон % удаления (n_remove_percentages)",
                    1,
                    99,
                    (
                        int(EXPERIMENT_CONFIG.get("n_remove_linspace", (1, 90, 10))[0]),
                        int(EXPERIMENT_CONFIG.get("n_remove_linspace", (1, 90, 10))[1]),
                    ),
                    1,
                    key="inf_removal_range",
                )
            with c_rm2:
                num_removal_percentages = st.number_input(
                    "Число точек сетки",
                    min_value=2,
                    max_value=100,
                    value=int(EXPERIMENT_CONFIG.get("n_remove_linspace", (1, 90, 10))[2]),
                    key="inf_removal_num_pts",
                )
            n_remove_percentages = [
                int(x)
                for x in np.linspace(
                    removal_range[0], removal_range[1], num_removal_percentages, dtype=int
                )
            ]
            st.info(
                f"Точки удаления ({len(n_remove_percentages)}): "
                f"{n_remove_percentages[:6]}{'…' if len(n_remove_percentages) > 6 else ''}"
            )

            st.markdown("**n_random_runs** (`EXPERIMENT_CONFIG`)")
            st.caption(
                "Сколько независимых случайных прогонов removal выполняется на каждом проценте "
                "удаления, если в `removal_strategies` включена стратегия «random» "
                "(как в `config/settings.py`)."
            )
            n_random_runs = st.slider(
                "n_random_runs",
                1,
                10,
                int(EXPERIMENT_CONFIG.get("n_random_runs", 3)),
                help="Совпадает с EXPERIMENT_CONFIG['n_random_runs'] в settings.py.",
                key="inf_n_random_runs",
            )
        else:
            removal_selected = ["lowest"]
            _lin = EXPERIMENT_CONFIG.get("n_remove_linspace", (1, 90, 10))
            n_remove_percentages = [
                int(x)
                for x in np.linspace(
                    int(_lin[0]), int(_lin[1]), int(_lin[2]), dtype=int
                )
            ]
            n_random_runs = int(EXPERIMENT_CONFIG.get("n_random_runs", 3))

        st.subheader("7. Loss, CatBoost, логи (EXPERIMENT_CONFIG)")
        c_l1, c_l2, c_l3 = st.columns(3)
        with c_l1:
            loss_high = st.checkbox(
                "loss_removal: loss_high",
                value="loss_high"
                in (EXPERIMENT_CONFIG.get("loss_removal_methods") or []),
                key="inf_loss_high",
            )
        with c_l2:
            loss_low = st.checkbox(
                "loss_removal: loss_low",
                value="loss_low"
                in (EXPERIMENT_CONFIG.get("loss_removal_methods") or []),
                key="inf_loss_low",
            )
        with c_l3:
            use_catboost_influence = st.checkbox(
                "use_catboost_influence",
                value=bool(EXPERIMENT_CONFIG.get("use_catboost_influence", False)),
                key="inf_use_catboost_influence",
            )
        show_tb_default = EXPERIMENT_CONFIG.get("show_top_bottom_influence", 0)
        if show_tb_default is False:
            show_tb_default = 0
        show_top_bottom_influence = st.number_input(
            "show_top_bottom_influence (0 = выкл.)",
            min_value=0,
            max_value=500,
            value=int(show_tb_default or 0),
            key="inf_show_top_bottom_influence",
        )

        st.subheader("8. Дистилляция (DISTILLATION_CONFIG)")
        use_distillation = st.checkbox(
            "use_distillation",
            value=bool(DISTILLATION_CONFIG.get("use_distillation", False)),
            key="inf_use_distillation",
        )
        c_di1, c_di2, c_di3 = st.columns(3)
        with c_di1:
            distillation_epochs = st.slider(
                "distillation_epochs",
                50,
                2000,
                int(DISTILLATION_CONFIG.get("distillation_epochs", 500)),
                50,
                key="inf_distillation_epochs",
            )
        with c_di2:
            distillation_temperature = st.number_input(
                "temperature",
                min_value=0.1,
                max_value=20.0,
                value=float(DISTILLATION_CONFIG.get("temperature", 2.0)),
                step=0.1,
                key="inf_distillation_temperature",
            )
        with c_di3:
            sa_choices = ["simple", "improved"]
            sa_def = DISTILLATION_CONFIG.get("student_architecture", "simple")
            student_architecture = st.selectbox(
                "student_architecture",
                sa_choices,
                index=sa_choices.index(sa_def) if sa_def in sa_choices else 0,
                key="inf_student_architecture",
            )

        _ip_base = copy.deepcopy(
            DATASET_INFLUENCE_PARAMS.get(
                selected_dataset, PYDVL_CONFIG["influence_params"]
            )
        )
        _pydvl_ip = PYDVL_CONFIG["influence_params"]
        st.subheader("9. Параметры influence (PYDVL_CONFIG, датасет)")
        with st.expander("Параметры influence-методов", expanded=False):
            ip_reg = st.number_input(
                "regularization",
                min_value=1e-12,
                max_value=1.0,
                value=float(_ip_base.get("regularization", _pydvl_ip["regularization"])),
                format="%.6e",
                key="inf_ip_reg",
            )
            ip_bs = st.number_input(
                "batch_size",
                min_value=1,
                max_value=2048,
                value=int(_ip_base.get("batch_size", _pydvl_ip["batch_size"])),
                key="inf_ip_bs",
            )
            ip_vbs = st.number_input(
                "influence_val_batch_size (0 = по умолчанию из базы)",
                min_value=0,
                max_value=10000,
                value=int(
                    _ip_base.get(
                        "influence_val_batch_size",
                        _pydvl_ip.get("influence_val_batch_size", 500),
                    )
                ),
                key="inf_ip_vbs",
            )
            st.markdown("**lissa_params**")
            c_li1, c_li2 = st.columns(2)
            lp = _ip_base.get("lissa_params", _pydvl_ip["lissa_params"])
            with c_li1:
                lissa_scale = st.number_input(
                    "scale", value=int(lp.get("scale", 10)), key="inf_lissa_scale"
                )
            with c_li2:
                lissa_damp = st.number_input(
                    "damping",
                    min_value=0.0,
                    max_value=1.0,
                    value=float(lp.get("damping", 0.1)),
                    key="inf_lissa_damp",
                )
            st.markdown("**cg_params**")
            c_cg1, c_cg2 = st.columns(2)
            cp = _ip_base.get("cg_params", _pydvl_ip["cg_params"])
            with c_cg1:
                cg_maxiter = st.number_input(
                    "maxiter", value=int(cp.get("maxiter", 100)), key="inf_cg_maxiter"
                )
            with c_cg2:
                cg_tol = st.number_input(
                    "tolerance",
                    min_value=1e-8,
                    max_value=1.0,
                    value=float(cp.get("tolerance", 1e-2)),
                    format="%.6e",
                    key="inf_cg_tol",
                )
            st.markdown("**arnoldi_params / nystroem_params**")
            c_ar1, c_ar2 = st.columns(2)
            ap = _ip_base.get("arnoldi_params", _pydvl_ip["arnoldi_params"])
            np_ = _ip_base.get("nystroem_params", _pydvl_ip["nystroem_params"])
            with c_ar1:
                arnoldi_rank = st.number_input(
                    "arnoldi rank",
                    min_value=1,
                    max_value=200,
                    value=int(ap.get("rank", 10)),
                    key="inf_arnoldi_rank",
                )
            with c_ar2:
                nyst_rank = st.number_input(
                    "nystroem rank",
                    min_value=1,
                    max_value=200,
                    value=int(np_.get("rank", 10)),
                    key="inf_nyst_rank",
                )

        st.subheader("10. Valuation и influence (INFLUENCE_METHODS_CONFIG)")
        col1, col2 = st.columns(2)
        shapley_methods = [
            "LOO",
            "DataShapley",
            "BetaShapley",
            "Banzhaf",
            "TMCShapley",
            "KNNShapley",
            "DataOOB",
            "LeastCore",
        ]
        influence_methods = [
            "Influence",
            "ArnoldiInfluence",
            "CgInfluence",
            "LissaInfluence",
            "NystroemSketchInfluence",
        ]
        selected_methods = []
        with col1:
            st.write("**valuation_methods**")
            for method in shapley_methods:
                if st.checkbox(method, key=f"method_{method}"):
                    selected_methods.append(method)
        with col2:
            st.write("**influence_methods**")
            for method in influence_methods:
                if st.checkbox(method, key=f"method_{method}"):
                    selected_methods.append(method)

        with st.expander("Прочее: DEBUG_MODE, FIT_MODE_EPOCHS, JSON overrides"):
            debug_mode = st.checkbox("DEBUG_MODE", value=False, key="inf_debug_mode")
            st.markdown("**FIT_MODE_EPOCHS** (эпохи PyTorch при underfit/overfit)")
            fe1, fe2 = st.columns(2)
            with fe1:
                fe_under = st.number_input(
                    "underfit",
                    1,
                    10000,
                    int(DEFAULT_FIT_MODE_EPOCHS.get("underfit", 10)),
                    key="inf_fe_under",
                )
            with fe2:
                fe_over = st.number_input(
                    "overfit",
                    1,
                    20000,
                    int(DEFAULT_FIT_MODE_EPOCHS.get("overfit", 5000)),
                    key="inf_fe_over",
                )
            overrides_json = st.text_area(
                "overrides (JSON) — глубокое слияние поверх settings",
                height=120,
                placeholder='{"PYDVL_CONFIG": {"n_steps": 10}}',
                key="inf_overrides_json",
            )

        st.markdown("---")
        c_sub1, c_sub2 = st.columns(2)
        with c_sub1:
            submit_button = st.form_submit_button(
                "Запустить эксперимент", width="stretch", type="primary"
            )
        with c_sub2:
            validate_button = st.form_submit_button("Проверить конфигурацию", width="stretch")

    def _commit_form_to_backup() -> None:
        """Сохранить фактические значения формы (из переменных submit, не устаревший session_state)."""
        _full = bool(st.session_state.get("ws_full_pipeline", False))
        overrides: Dict[str, Any] = {
            "new_experiment_dataset": selected_dataset,
            "inf_model_type": model_type,
            "inf_model_architecture": model_architecture,
            "inf_model_fit_mode": model_fit_mode,
            "inf_primary_metric": primary_metric,
            "inf_sample_size": int(sample_size),
            "inf_test_size": float(test_size),
            "inf_val_size": float(val_size),
            "inf_n_epochs": int(n_epochs),
            "inf_n_retrain_runs": int(n_retrain_runs),
            "inf_random_state": int(random_state),
            "inf_device": device_choice,
            "inf_n_jobs": int(n_jobs_ui),
            "inf_use_cache": bool(use_cache_ui),
            "inf_loss_high": bool(loss_high),
            "inf_loss_low": bool(loss_low),
            "inf_use_catboost_influence": bool(use_catboost_influence),
            "inf_show_top_bottom_influence": int(show_top_bottom_influence),
            "inf_use_distillation": bool(use_distillation),
            "inf_distillation_epochs": int(distillation_epochs),
            "inf_distillation_temperature": float(distillation_temperature),
            "inf_student_architecture": student_architecture,
            "inf_ip_reg": float(ip_reg),
            "inf_ip_bs": int(ip_bs),
            "inf_ip_vbs": int(ip_vbs),
            "inf_lissa_scale": int(lissa_scale),
            "inf_lissa_damp": float(lissa_damp),
            "inf_cg_maxiter": int(cg_maxiter),
            "inf_cg_tol": float(cg_tol),
            "inf_arnoldi_rank": int(arnoldi_rank),
            "inf_nyst_rank": int(nyst_rank),
            "inf_debug_mode": bool(debug_mode),
            "inf_fe_under": int(fe_under),
            "inf_fe_over": int(fe_over),
            "inf_overrides_json": str(overrides_json or ""),
            "ws_full_pipeline": _full,
            "ws_removal_adaptive": bool(
                st.session_state.get("ws_removal_adaptive", False)
            ),
            "inf_use_tfidf_lsa": bool(
                st.session_state.get("inf_use_tfidf_lsa", False)
            ),
            "inf_lsa_components": int(
                st.session_state.get("inf_lsa_components", 200)
            ),
        }
        if _is_classification_task_type(selected_row["task_type"]):
            overrides["ws_removal_per_class"] = bool(
                st.session_state.get("ws_removal_per_class", False)
            )
        if _is_regression_task_type(selected_row["task_type"]):
            overrides["ws_removal_stratify_target"] = bool(
                st.session_state.get("ws_removal_stratify_target", False)
            )
            overrides["inf_removal_stratify_n_bins"] = int(
                st.session_state.get(
                    "inf_removal_stratify_n_bins",
                    MODEL_RUN_CONFIG.get("removal_stratify_n_bins", 10) or 10,
                )
            )
        for m in all_methods:
            overrides[f"method_{m}"] = m in selected_methods
        if _full:
            for rk in removal_strategy_keys:
                overrides[f"rs_{rk}"] = rk in removal_selected
            overrides["inf_removal_range"] = tuple(removal_range)
            overrides["inf_removal_num_pts"] = int(num_removal_percentages)
            overrides["inf_n_random_runs"] = int(n_random_runs)
        _apply_inf_form_backup_overrides(overrides)

    if validate_button:
        _commit_form_to_backup()
        st.success("Конфигурация допустима (запрос к API не отправлялся).")

    if submit_button:
        st.session_state.pop("experiment_done_banner", None)

        if st.session_state.get("ws_full_pipeline", False) and not removal_selected:
            st.error("Выберите хотя бы одну removal_strategies.")
            return

        overrides_payload = None
        if overrides_json and str(overrides_json).strip():
            try:
                overrides_payload = json.loads(overrides_json)
                if not isinstance(overrides_payload, dict):
                    st.error("Overrides JSON: корень должен быть объектом.")
                    return
            except json.JSONDecodeError as je:
                st.error(f"Неверный JSON overrides: {je}")
                return

        loss_removal_methods = []
        if loss_high:
            loss_removal_methods.append("loss_high")
        if loss_low:
            loss_removal_methods.append("loss_low")

        if "lowest" in removal_selected:
            removal_strategy = "remove_lowest_influence"
        elif "highest" in removal_selected:
            removal_strategy = "remove_highest_influence"
        else:
            removal_strategy = "remove_lowest_influence"

        influence_params = {
            "regularization": float(ip_reg),
            "batch_size": int(ip_bs),
            "lissa_params": {"scale": int(lissa_scale), "damping": float(lissa_damp)},
            "cg_params": {"maxiter": int(cg_maxiter), "tolerance": float(cg_tol)},
            "arnoldi_params": {"rank": int(arnoldi_rank)},
            "nystroem_params": {"rank": int(nyst_rank)},
        }
        base_vbs = int(
            _ip_base.get(
                "influence_val_batch_size",
                _pydvl_ip.get("influence_val_batch_size", 500),
            )
        )
        if ip_vbs and ip_vbs != base_vbs:
            influence_params["influence_val_batch_size"] = int(ip_vbs)

        _run_mode = "full" if st.session_state.get("ws_full_pipeline", False) else "influence_only"
        _adaptive = bool(st.session_state.get("ws_removal_adaptive", False))
        config = {
            "dataset_name": selected_dataset,
            "model_type": model_type,
            "model_params": {"model_architecture": model_architecture},
            "removal_strategy": removal_strategy,
            "removal_strategies": removal_selected,
            "n_remove_percentages": n_remove_percentages,
            "removal_adaptive_model": _adaptive if _run_mode == "full" else False,
            "removal_per_class": (
                bool(st.session_state.get("ws_removal_per_class", False))
                if _is_classification_task_type(selected_row["task_type"])
                else False
            ),
            "removal_stratify_target": (
                bool(st.session_state.get("ws_removal_stratify_target", False))
                if _is_regression_task_type(selected_row["task_type"])
                else False
            ),
            "removal_stratify_n_bins": int(
                st.session_state.get(
                    "inf_removal_stratify_n_bins",
                    MODEL_RUN_CONFIG.get("removal_stratify_n_bins", 10) or 10,
                )
            )
            if _is_regression_task_type(selected_row["task_type"])
            else MODEL_RUN_CONFIG.get("removal_stratify_n_bins", 10),
            "sample_size_percentage": float(sample_size),
            "test_size": float(test_size),
            "val_size": float(val_size),
            "n_epochs": int(n_epochs),
            "n_random_runs": int(n_random_runs),
            "n_retrain_runs": int(n_retrain_runs),
            "run_mode": _run_mode,
            "selected_influence_methods": selected_methods,
            "use_distillation": use_distillation,
            "distillation_epochs": int(distillation_epochs),
            "distillation_temperature": float(distillation_temperature),
            "student_architecture": student_architecture,
            "random_state": int(random_state),
            "debug_mode": debug_mode,
            "model_fit_mode": model_fit_mode,
            "metric_config": {
                **dict(METRIC_CONFIG),
                selected_row["task_type"]: primary_metric,
            },
            "loss_removal_methods": loss_removal_methods,
            "use_catboost_influence": use_catboost_influence,
            "show_top_bottom_influence": int(show_top_bottom_influence),
            "use_tfidf_lsa": bool(use_tfidf_lsa),
            "lsa_components": int(lsa_components) if use_tfidf_lsa else None,
            "influence_params": influence_params,
            "device": device_choice,
            "use_cache": use_cache_ui,
            "n_jobs": int(n_jobs_ui),
            "fit_mode_epochs": {"underfit": int(fe_under), "overfit": int(fe_over)},
        }
        if overrides_payload is not None:
            config["overrides"] = overrides_payload

        _commit_form_to_backup()
        st.session_state[PENDING_INFLUENCE_START_KEY] = config
        st.rerun()


    if st.session_state.get("experiment_done_banner"):
        b = st.session_state.experiment_done_banner
        eid = b.get("experiment_id", "")
        st.markdown("---")
        st.success(
            f"Эксперимент завершён.\n\n"
            f"ID: `{eid}` — результаты сохранены; откройте раздел «Анализ» для графиков."
        )

    _persist_inf_form_outside_widgets()


def page_analysis():
    """Страница анализа результатов."""
    st.title("Анализ эксперимента")

    response = _cached_api_experiments_list(API_BASE_URL)
    if not response or not response.get("experiments"):
        st.info("Нет экспериментов. Сначала запустите эксперимент на вкладке «Рабочая область».")
        return

    experiments = response.get("experiments", [])

    exp_options = [_experiment_list_label(e) for e in experiments]
    exp_ids = [e["experiment_id"] for e in experiments]

    sel_tree = st.session_state.get("selected_experiment_id")
    if sel_tree and sel_tree in exp_ids:
        selected_exp_id = sel_tree
        st.caption(f"Текущий эксперимент: `{selected_exp_id}`")
    else:
        default_idx = 0
        selected_idx = st.selectbox(
            "Эксперимент",
            range(len(exp_options)),
            index=default_idx,
            format_func=lambda i: exp_options[i],
            key="analysis_exp_select",
        )
        selected_exp_id = exp_ids[selected_idx]
        st.session_state.selected_experiment_id = selected_exp_id

    _res_params = _params_tuple(
        {"include_results": False, "include_scores_raw": False}
    )
    results_response = _cached_api_experiment_results(
        API_BASE_URL, selected_exp_id, _res_params
    )

    if not results_response:
        st.error("Не удалось загрузить результаты эксперимента")
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Датасет", results_response.get("config", {}).get("dataset_name", "—"))
    with col2:
        st.metric("Модель", results_response.get("config", {}).get("model_type", "—"))
    with col3:
        st.metric("Объём", results_response.get("samples_count", "—"))
    with col4:
        exec_time = results_response.get("execution_time", 0)
        st.metric("Время", f"{exec_time:.1f} с")

    available_methods = results_response.get("influence_methods", [])

    # Раздел: отдельный persist — ключ виджета может пропасть при размонтировании
    # страницы; при смене эксперимента принудительно подставляем persist в key виджета,
    # чтобы не сбрасываться на первый раздел.
    _section_opts = (
        _ANALYSIS_TAB_DIST,
        _ANALYSIS_TAB_REMOVAL,
        _ANALYSIS_TAB_EXAMPLES,
    )
    _ap = "analysis_section_persist"
    if _ap not in st.session_state:
        st.session_state[_ap] = _ANALYSIS_TAB_DIST
    elif st.session_state[_ap] not in _section_opts:
        st.session_state[_ap] = _ANALYSIS_TAB_DIST

    _last_analysis_exp = st.session_state.get("_analysis_ui_exp_id")
    if _last_analysis_exp != selected_exp_id:
        st.session_state["_analysis_ui_exp_id"] = selected_exp_id
        st.session_state["analysis_section"] = st.session_state[_ap]
    elif "analysis_section" not in st.session_state:
        st.session_state["analysis_section"] = st.session_state[_ap]

    analysis_section = st.radio(
        "Раздел",
        _section_opts,
        horizontal=True,
        key="analysis_section",
    )
    st.session_state[_ap] = analysis_section

    if analysis_section == _ANALYSIS_TAB_DIST:
        st.subheader("Распределение весов influence")

        if available_methods:
            cfg_an = results_response.get("config") or {}
            task_type = cfg_an.get("task_type") or ""
            if not task_type and cfg_an.get("dataset_name"):
                try:
                    from config import DatasetRegistry

                    task_type = (
                        DatasetRegistry.get(cfg_an["dataset_name"])
                        .get_info()
                        .get("task_type", "")
                    )
                except Exception:
                    task_type = ""
            is_classification = task_type in (
                "binary_classification",
                "multiclass_classification",
            )
            is_regression = task_type == "regression"

            targets_list: Optional[List[int]] = None
            color_by_target = False
            group_label = "класс"
            if is_classification:
                color_by_target = st.toggle(
                    "Показать распределение по классам таргета",
                    value=False,
                    key=f"dist_color_target_{selected_exp_id}",
                    help="Гистограммы по классам (тот же порядок примеров, что у весов influence).",
                )
                if color_by_target:
                    td = _cached_api_train_targets(API_BASE_URL, selected_exp_id)
                    if td and td.get("targets"):
                        targets_list = td["targets"]
                    else:
                        st.warning(
                            "Не удалось загрузить метки train (проверьте датасет и config)."
                        )
            elif is_regression:
                group_label = "страта"
                color_by_target = st.toggle(
                    "Показать распределение по стратам целевой (квантильные бины)",
                    value=False,
                    key=f"dist_color_strata_{selected_exp_id}",
                    help="Как removal со стратификацией: те же квантильные страты по y, порядок строк как у весов influence.",
                )
                if color_by_target:
                    td = _cached_api_train_targets(API_BASE_URL, selected_exp_id)
                    if td and td.get("targets"):
                        targets_list = td["targets"]
                    else:
                        st.warning(
                            "Не удалось загрузить страты train (проверьте датасет и config)."
                        )

            weights_by_method: Dict[str, List[float]] = {}
            stats_rows: List[Dict[str, Any]] = []
            for m in available_methods:
                wr = load_influence_weights(selected_exp_id, m)
                if wr and wr.get("weights"):
                    weights_by_method[m] = wr["weights"]
                    stt = wr.get("statistics") or {}
                    stats_rows.append(
                        {
                            "Метод": m,
                            "min": stt.get("min"),
                            "max": stt.get("max"),
                            "mean": stt.get("mean"),
                            "std": stt.get("std"),
                            "n": wr.get("count", len(wr["weights"])),
                        }
                    )

            if not weights_by_method:
                st.error("Не удалось загрузить веса influence")
            else:
                if (
                    targets_list
                    and color_by_target
                    and (is_classification or is_regression)
                ):
                    n_w = len(next(iter(weights_by_method.values())))
                    if len(targets_list) != n_w:
                        st.warning(
                            f"Число меток/страт ({len(targets_list)}) не совпадает с числом весов ({n_w}); "
                            "раскраска отключена."
                        )
                        targets_list = None

                if stats_rows:
                    st.dataframe(
                        pd.DataFrame(stats_rows),
                        use_container_width=True,
                        hide_index=True,
                    )

                fig = plot_influence_distribution_stacked_plotly(
                    weights_by_method,
                    targets=targets_list
                    if (
                        color_by_target
                        and targets_list
                        and (is_classification or is_regression)
                    )
                    else None,
                    group_label=group_label,
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Для этого эксперимента не посчитаны методы influence")

    elif analysis_section == _ANALYSIS_TAB_REMOVAL:
        st.subheader("Метрика модели при удалении данных")
        st.caption(
            "Пунктирная серая линия — baseline на полном train. "
            "Для стратегии random: полупрозрачная полоса min–max по независимым прогонам и яркая линия медианы. "
            "Какие серии видны на графике, в AUC и в средней разнице с лучшим в точке — "
            "только отмеченные чекбоксами "
            "(клик по легенде Plotly отключён, чтобы графики не расходились)."
        )

        removal_smooth_on = st.checkbox(
            "Сглаживание кривых (только отображение)",
            value=False,
            key=f"removal_smooth_{selected_exp_id}",
            help="Скользящее среднее вдоль оси X (доля удаления); удобно при плотной сетке точек.",
        )
        removal_smooth_win = 5
        if removal_smooth_on:
            st.caption(
                "Сглаживание меняет только линии на графике removal; AUC, столбцы «средняя разница с лучшим в точке» "
                "и таблица — по исходным точкам."
            )
            removal_smooth_win = st.slider(
                "Окно сглаживания (точек)",
                min_value=3,
                max_value=31,
                value=5,
                step=2,
                key=f"removal_smooth_win_{selected_exp_id}",
            )

        graph_data_response = load_graph_data(selected_exp_id)
        _cfg_an = (graph_data_response or {}).get("config") or {}
        if "removal_adaptive_model" in _cfg_an:
            if _cfg_an.get("removal_adaptive_model"):
                st.caption(
                    "Адаптивная модель для removal: включена (ёмкость снижалась при меньшем train)."
                )
            else:
                st.caption(
                    "Адаптивная модель для removal: выключена (та же ёмкость на всех шагах removal)."
                )

        baseline_val = None
        rrr_payload = None
        if graph_data_response:
            baseline_val = graph_data_response.get("baseline_metric")
            rrr_payload = graph_data_response.get("random_run_results")

        if graph_data_response and graph_data_response.get("removal_data"):
            removal_data = graph_data_response.get("removal_data", {})
            metric_info = graph_data_response.get("metric") or {}

            all_series = sorted(removal_data.keys())
            if all_series:
                st.markdown(
                    "**Серии на графике** — полные имена; отметьте, что показывать на графике, в AUC и в % к лучшему в точке"
                )
                b_all, b_none, _sp = st.columns([1, 1, 6])
                with b_all:
                    if st.button(
                        "Включить все",
                        key=f"series_all_{selected_exp_id}",
                    ):
                        for m in all_series:
                            st.session_state[_series_checkbox_key(selected_exp_id, m)] = True
                        st.rerun()
                with b_none:
                    if st.button(
                        "Выключить все",
                        key=f"series_none_{selected_exp_id}",
                    ):
                        for m in all_series:
                            st.session_state[_series_checkbox_key(selected_exp_id, m)] = False
                        st.rerun()

                methods_to_compare: List[str] = []
                half = (len(all_series) + 1) // 2
                col_cb_l, col_cb_r = st.columns(2)
                for i, m in enumerate(all_series):
                    ck = _series_checkbox_key(selected_exp_id, m)
                    with col_cb_l if i < half else col_cb_r:
                        if st.checkbox(
                            m.replace("_", " "),
                            value=True,
                            key=ck,
                        ):
                            methods_to_compare.append(m)

                if methods_to_compare:
                    filtered_removal_data = {
                        m: removal_data[m] for m in methods_to_compare if m in removal_data
                    }

                    if filtered_removal_data:
                        with st.expander("Цвета линий (Plotly)", expanded=False):
                            st.caption(
                                "Суффиксы _lowest / _highest / _extremes — разный стиль линии и маркеров."
                            )
                            color_overrides: Dict[str, str] = {}
                            n = len(methods_to_compare)
                            # Две колонки — шире блоки, длинные имена методов помещаются лучше, чем при 4 колонках
                            ncols = min(2, max(1, n))
                            for row_start in range(0, n, ncols):
                                cols = st.columns(ncols)
                                for j in range(ncols):
                                    idx = row_start + j
                                    if idx >= n:
                                        break
                                    m = methods_to_compare[idx]
                                    def_hex = default_color_for_removal_trace(m)
                                    label = m.replace("_", " ")
                                    if len(label) > _COLOR_PICKER_LABEL_MAX_CHARS:
                                        label = label[: _COLOR_PICKER_LABEL_MAX_CHARS] + "…"
                                    with cols[j]:
                                        color_overrides[m] = st.color_picker(
                                            label,
                                            value=def_hex,
                                            key=_stable_color_picker_key(selected_exp_id, m),
                                        )

                        fig = plot_removal_impact(
                            filtered_removal_data,
                            metric_info=metric_info,
                            color_overrides=color_overrides,
                            baseline_metric=baseline_val,
                            random_run_results=rrr_payload,
                            smooth=removal_smooth_on,
                            smooth_window=removal_smooth_win,
                        )
                        _sig = _methods_selection_signature(methods_to_compare)
                        st.plotly_chart(
                            fig,
                            use_container_width=True,
                            key=(
                                f"pl_removal_{selected_exp_id}_{_sig}_"
                                f"{removal_smooth_on}_{removal_smooth_win}"
                            ),
                        )

                        aucs_payload = (
                            graph_data_response.get("removal_curve_aucs") or {}
                        )
                        mn = metric_info.get("name") or "metric"
                        ms = metric_info.get("short_label_ru") or mn
                        if aucs_payload:
                            st.subheader("AUC кривых removal")
                            st.caption(
                                "Столбцы только для отмеченных чекбоксами методов "
                                "(те же, что и кривые выше). Слева — лучше по rank_score."
                            )
                            fig_auc = plotly_removal_auc_bars(
                                aucs_payload,
                                methods_to_compare,
                                mn,
                                metric_short=ms,
                            )
                            st.plotly_chart(
                                fig_auc,
                                use_container_width=True,
                                key=f"pl_auc_{selected_exp_id}_{_sig}",
                            )

                        st.subheader("Средняя разница с лучшим в точке")
                        
                        fig_mpp = plotly_removal_mean_pct_diff_from_pointwise_best_bars(
                            filtered_removal_data,
                            methods_to_compare,
                            mn,
                            metric_short=ms,
                        )
                        st.plotly_chart(
                            fig_mpp,
                            use_container_width=True,
                            key=f"pl_pct_best_{selected_exp_id}_{_sig}",
                        )

                        st.subheader("Таблица стратегий")
                        table_data = []
                        dataset_name = results_response.get("config", {}).get("dataset_name", "—")
                        model_type = results_response.get("config", {}).get("model_type", "—")
                        auc_random = aucs_payload.get("random") if aucs_payload else None
                        for m in methods_to_compare:
                            removal = removal_data.get(m, [])
                            metric_10 = next((r['metric'] for r in removal if r['percent'] == 10), None)
                            metric_90 = next((r['metric'] for r in removal if r['percent'] == 90), None)
                            random_10 = np.median(rrr_payload.get("10", [])) if rrr_payload and "10" in rrr_payload else None
                            random_90 = np.median(rrr_payload.get("90", [])) if rrr_payload and "90" in rrr_payload else None
                            delta_rand_10 = (
                                f"{(metric_10 - random_10) / random_10 * 100:+.2f}%"
                                if metric_10 is not None and random_10 not in (None, 0)
                                else "-"
                            )
                            delta_base_10 = (
                                f"{(metric_10 - baseline_val) / baseline_val * 100:+.2f}%"
                                if metric_10 is not None and baseline_val not in (None, 0)
                                else "-"
                            )
                            delta_rand_90 = (
                                f"{(metric_90 - random_90) / random_90 * 100:+.2f}%"
                                if metric_90 is not None and random_90 not in (None, 0)
                                else "-"
                            )
                            delta_base_90 = (
                                f"{(metric_90 - baseline_val) / baseline_val * 100:+.2f}%"
                                if metric_90 is not None and baseline_val not in (None, 0)
                                else "-"
                            )
                            auc_method = aucs_payload.get(m) if aucs_payload else None
                            delta_auc = (
                                f"{(auc_method - auc_random) * 100:+.4f}%"
                                if auc_method is not None and auc_random is not None
                                else "-"
                            )
                            table_data.append({
                                "Датасет": dataset_name,
                                "Модель": model_type,
                                "Baseline": f"{baseline_val:.4f}" if baseline_val is not None else "—",
                                "Metric 10%": f"{metric_10:.4f}" if metric_10 is not None else "—",
                                "Metric 90%": f"{metric_90:.4f}" if metric_90 is not None else "—",
                                "Δ rand 10%": delta_rand_10,
                                "Δ base 10%": delta_base_10,
                                "Δ rand 90%": delta_rand_90,
                                "Δ base 90%": delta_base_90,
                                "Δ AUC": delta_auc,
                                "Метод": m,
                            })
                        if table_data:
                            df = pd.DataFrame(table_data)
                            st.dataframe(df, use_container_width=True)
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="Скачать таблицу как CSV",
                                data=csv,
                                file_name=f"strategies_table_{selected_exp_id}.csv",
                                mime="text/csv",
                                key=f"download_table_{selected_exp_id}",
                            )
                    else:
                        st.warning("Нет данных для выбранных серий")
                else:
                    st.info("Отметьте хотя бы одну серию чекбоксом выше.")
            else:
                st.warning("Нет серий removal в ответе graph-data")
        else:
            st.warning(
                "Нет данных removal: эксперимент ещё выполняется, не удался или removal не запускался."
            )

        st.divider()
        st.subheader("Экспорт подвыборки train после удаления")
        st.caption(
            "Тот же порядок удаления, что в runner: для influence-методов — стратегия "
            "(lowest, highest, extremes, median); для LossHigh / LossLow порядок фиксирован, стратегия не задаётся."
        )
        ex_m = st.selectbox(
            "Метод influence",
            available_methods if available_methods else ["NystroemSketchInfluence"],
            key="ex_method",
        )
        _export_loss_fixed = ex_m in ("LossHigh", "LossLow")
        if _export_loss_fixed:
            ex_s = "highest" if ex_m == "LossHigh" else "lowest"
        else:
            ex_s = st.selectbox(
                "Стратегия",
                ["lowest", "highest", "extremes", "median"],
                key="ex_strat",
            )
        ex_p = st.slider("Доля удаления, %", 0, 100, 10, key="ex_pct")
        if st.button("Сформировать CSV (API)", key="ex_btn"):
            try:
                url = f"{API_BASE_URL}/experiments/{selected_exp_id}/export-train-subset"
                resp = requests.post(
                    url,
                    json={
                        "method": ex_m,
                        "strategy": ex_s,
                        "removal_percent": int(ex_p),
                    },
                    timeout=(30.0, 1800.0),
                )
                if resp.status_code == 200:
                    st.download_button(
                        "Скачать CSV (train)",
                        resp.content,
                        f"train_subset_{selected_exp_id[:8]}_{ex_m}_{ex_s}_{ex_p}.csv",
                        "text/csv",
                        key="dl_export",
                    )
                    st.success("Файл готов — нажмите кнопку загрузки ниже.")
                else:
                    st.error(f"Ошибка экспорта: {resp.status_code} {resp.text}")
            except Exception as ex:
                st.error(str(ex))

    else:
        gd_res = load_graph_data(selected_exp_id)
        st.subheader("Ресурсы и время (этапы *_computation)")
        st.caption(
            "Данные из results.pkl каталога эксперимента: GPU (max_wanted), RSS, длительность. "
            "Если каталог на сервере недоступен — блок будет пустым."
        )
        comp_rows = (gd_res or {}).get("computation_timings") or []
        if comp_rows:
            f_mw = plotly_computation_metric_bars(
                comp_rows,
                "max_wanted_mb",
                "GPU: max_wanted_MB по методам",
                "max_wanted_MB",
                "%.2f",
            )
            st.plotly_chart(f_mw, use_container_width=True)
            f_ram = plotly_computation_metric_bars(
                comp_rows,
                "ram_mb",
                "RAM: RSS peak (MB) по методам",
                "RAM_MB",
                "%.2f",
            )
            st.plotly_chart(f_ram, use_container_width=True)
            f_sec = plotly_computation_metric_bars(
                comp_rows,
                "duration_s",
                "Время вычисления влияния по методам",
                "s (seconds)",
                "%.2f",
            )
            st.plotly_chart(f_sec, use_container_width=True)
        else:
            st.info(
                "Нет строк *_computation в timings (results.pkl). "
                "Запустите полный пайплайн с логированием в каталог experiment_logs."
            )

        st.divider()
        st.subheader("Крайние примеры influence (top / bottom)")
        art = load_artifacts_list(selected_exp_id)
        if art and art.get("files"):
            tb_files = [
                f for f in art["files"] if f.startswith("top_bottom_") and f.endswith(".csv")
            ]
            if tb_files:
                pick = st.selectbox("Файл CSV", tb_files, key="tb_csv_pick")
                try:
                    url = f"{API_BASE_URL}/experiments/{selected_exp_id}/artifacts/download"
                    r = requests.get(
                        url, params={"filename": pick}, timeout=DEFAULT_HTTP_TIMEOUT
                    )
                    if r.status_code == 200:
                        import io as _io

                        df_tb = pd.read_csv(_io.StringIO(r.text))
                        st.dataframe(df_tb, use_container_width=True, height=360)
                        st.download_button(
                            "Скачать CSV",
                            r.text.encode("utf-8"),
                            pick,
                            "text/csv",
                            key="dl_tb_csv",
                        )
                    else:
                        st.error(f"Не удалось загрузить артефакт ({r.status_code})")
                except Exception as ex:
                    st.error(str(ex))
            else:
                st.info(
                    "Нет файлов top_bottom_*.csv. Задайте show_top_bottom_influence > 0 "
                    "в overrides или config/settings.py и перезапустите эксперимент."
                )
        else:
            st.warning("Не удалось получить список артефактов (нет каталога эксперимента?).")


def page_settings():
    """Настройки приложения."""
    st.title("Настройки")
    
    with st.form("settings_form"):
        st.subheader("API")
        api_url = st.text_input(
            "Базовый URL API",
            value=API_BASE_URL,
            help="Адрес бэкенда FastAPI",
        )

        poll_interval = st.slider(
            "Интервал опроса статуса (с)",
            min_value=1,
            max_value=10,
            value=2,
            help="Как часто запрашивать статус эксперимента",
        )

        st.subheader("Хранилище")
        max_experiments = st.number_input(
            "Макс. число экспериментов",
            min_value=10,
            max_value=1000,
            value=200,
            help="Ограничение списка (если реализовано на сервере)",
        )

        st.subheader("Отображение")
        theme_options = ["light", "dark", "auto"]
        theme_index = theme_options.index("auto") if "auto" in theme_options else 0
        theme = st.selectbox(
            "Тема",
            theme_options,
            index=theme_index,
            help="Тема интерфейса Streamlit",
        )
        
        if st.form_submit_button("Сохранить"):
            st.success("Сохранено. Смена URL API требует перезапуска сервера.")


def main():
    """Точка входа Streamlit."""
    if 'selected_methods' not in st.session_state:
        st.session_state.selected_methods = []
    if 'current_experiment_id' not in st.session_state:
        st.session_state.current_experiment_id = None

    page = render_top_nav()

    if page != "workspace":
        st.session_state.pop("experiment_done_banner", None)

    if page in ("workspace", "analysis"):
        col_tree, col_main = st.columns([1, 3], gap="medium")
        with col_tree:
            render_experiment_tree()
        with col_main:
            if page == "workspace":
                page_workspace()
            else:
                page_analysis()
    elif page == "settings":
        page_settings()


if __name__ == "__main__":
    main()
