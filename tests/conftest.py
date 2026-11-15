import os
import sys
import warnings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
warnings.filterwarnings("ignore")
# Порядок импорта как в main.py (иначе циклический импорт influence <-> experiments)
import experiments.logger  # noqa: E402,F401
import experiments  # noqa: E402,F401
