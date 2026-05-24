# Обзор проекта для LaTeX (актуальное состояние репозитория)

Файл `docs/ARTICLE_FULL_RU.md` **не изменялся**. Ниже — готовый фрагмент для вставки в статью/отчёт; он согласован с описанием в `ARTICLE_FULL_RU.md` и текущей кодовой базой.

---

```latex
\newpage
\section{Обзор проекта: анализ методов влияния данных (в т.\,ч.\ датасет Zillow)}

Проект реализует программную систему для \textbf{эмпирического сравнения} методов оценки важности обучающих точек (valuation и influence functions) и анализа \textbf{кривых последовательного удаления} данных: как меняется качество модели на отложенной выборке при удалении объектов с наименьшим/наибольшим влиянием, случайно, по величине функции потерь и по комбинированным стратегиям. Датасет Zillow (предсказание \texttt{logerror} по сделкам недвижимости) является одним из поддерживаемых сценариев; наряду с ним в едином конвейере доступны табличные, текстовые и изображения (см.\ реестр датасетов).

\paragraph{Архитектура проекта.} Модульная структура с разделением ответственности:
\begin{itemize}
    \item \texttt{main.py} — точка входа CLI: выбор датасета (\texttt{CURRENT\_DATASET} или \texttt{--dataset}), сплиты данных, препроцессинг, запуск \texttt{ExperimentRunner}, сохранение артефактов и графиков;
    \item \texttt{config/settings.py} — централизованные флаги: датасет, режим подгонки модели (\texttt{normal}/\texttt{underfit}/\texttt{overfit}), параметры эксперимента, списки методов pyDVL, метрики, дистилляция, адаптивная модель при removal;
    \item \texttt{config/datasets/} — \texttt{BaseDatasetConfig}, конфигурации датасетов, \texttt{DatasetRegistry};
    \item \texttt{data/} — \texttt{DataLoaderFactory}, \texttt{data/cache.py} (кэширование), \texttt{data/preprocessing/} (таблицы, текст, изображения через \texttt{PreprocessorFactory});
    \item \texttt{models/} — \texttt{ModelFactory}: деревья (LightGBM, XGBoost, CatBoost, RandomForest), обёртки PyTorch, \texttt{DistilledModelWrapper};
    \item \texttt{influence/} — \texttt{InfluenceMethods}, \texttt{SafeModelWrapper}, скореры, утилиты статистики;
    \item \texttt{experiments/} — \texttt{runner.py} (baseline $\to$ influence $\to$ removal), \texttt{logger.py}, вспомогательные скрипты чувствительности параметров;
    \item \texttt{visualization/} — графики CLI, экспорт \texttt{removal\_metrics.csv}, доп.\ утилиты построения графиков;
    \item \texttt{utils/} — в т.\,ч.\ \texttt{removal\_adaptive\_params.py} (масштабирование архитектуры/гиперпараметров под размер подвыборки при удалении);
    \item \texttt{microservice/} — HTTP API (FastAPI), веб-интерфейс (Streamlit), очередь экспериментов, хранилище весов, экспорт подвыборок, Plotly-графики; \texttt{Dockerfile}, \texttt{docker-compose.yml};
    \item \texttt{scripts/} — например, \texttt{plot\_removal\_from\_weights.py}, крупные исследования/агрегация результатов;
    \item \texttt{synthetic\_data/}, \texttt{check\_overfitting.py} — дополнительные экспериментальные сценарии вне основного конвейера.
\end{itemize}

\paragraph{Данные и датасет Zillow.} Реестр поддерживает, в частности: \texttt{adult}, \texttt{housing}, \texttt{wine}, \texttt{zillow}, \texttt{covertype}, \texttt{electric}, \texttt{mnist}, \texttt{imdb}, \texttt{cifar10}. Для Zillow используются файлы \texttt{properties\_2016.csv} (признаки объектов), \texttt{train\_2016\_v2.csv} (целевая переменная \texttt{logerror}), слияние по идентификатору; в конфигурации задаются отбор признаков, порог пропусков (в т.\,ч.\ удаление колонок с долей пропусков выше порога), кодирование категорий, масштабирование числовых признаков, пользовательские шаги (разбор даты транзакции, агрегированные признаки). Для предотвращения утечки статистики предобработка \texttt{fit} выполняется на обучающей части и \texttt{transform} — на остальных. Предусмотрено файловое кэширование предобработанных данных (\texttt{USE\_CACHE}, \texttt{CACHE\_DIR}).

\paragraph{Модели машинного обучения.} Деревянные бустинги и лес, нейросети с выбором архитектуры (\texttt{simple}, \texttt{improved}, \texttt{ft\_transformer} и др.\ в зависимости от конфигурации). Гиперпараметры задаются через \texttt{get\_model\_config} с учётом \texttt{MODEL\_FIT\_MODE} и при необходимости \texttt{FIT\_MODE\_EPOCHS}. \textbf{Дистилляция:} обучение teacher-дерева с последующим student-нейросетью; influence для Hessian-методов извлекается из student. \textbf{Адаптивная модель при removal:} при уменьшении обучающей выборки возможны упрощение архитектуры и масштабирование числа листьев/глубины/оценщиков деревьев и размеров слоёв сети пропорционально $\sqrt{\text{доля оставшихся данных}}$.

\paragraph{Методы оценки влияния и базовые линии.} Через библиотеку \textbf{pyDVL}: valuation (в т.\,ч.\ LOO, Data Shapley, Beta-Shapley, Banzhaf, TMC-Shapley, Least Core) и influence для PyTorch (Direct, Arnoldi, CG, LISSA, Nyström sketch). Отдельные методы pyDVL намеренно отключаются при несовместимости с задачей или типом модели (см.\ ветки в \texttt{setup\_methods}). Дополнительно: пер-объектные потери \texttt{LossHigh}/\texttt{LossLow}, опционально вектор важности объектов CatBoost (\texttt{use\_catboost\_influence}). Параллелизм на уровне потоков (\texttt{N\_JOBS}), вычисления на GPU при наличии (\texttt{DEVICE}).

\paragraph{Экспериментальная установка.} После двухступенчатого разбиения (holdout для итоговой метрики \texttt{final\_metric}, внутренний train/test для ранней остановки и скорера valuation) выполняется baseline-обучение, расчёт scores, затем серии переобучения на подвыборках. Доли удаления задаются списком процентов от исходного train (\texttt{n\_remove\_linspace}), с ограничением минимального остатка (не менее 10 объектов) и опционально стратификацией по классам или квантилям целевой переменной. \textbf{Стратегии удаления} для influence-векторов: \texttt{lowest}, \texttt{highest}, \texttt{random}, \texttt{extremes}, \texttt{median}, \texttt{few\_*\_then\_random}. Для PyTorch на каждом шаге возможен выбор лучшего из \texttt{n\_retrain\_runs} прогонов по holdout; для случайного удаления — несколько независимых траекторий с агрегацией медианой. Режим \texttt{run\_mode=influence\_only} отключает фазу removal. Основная метрика задаётся типом задачи (\texttt{METRIC\_CONFIG}, список разрешённых метрик в конфиге датасета; для регрессии часто MAE).

\paragraph{Логирование, воспроизводимость и микросервис.} Каталоги экспериментов с \texttt{results.pkl}, текстовыми логами, сохранением конфигурации (JSON) и весов influence; при сбоях GPU — диагностика памяти. Сиды фиксируются глобально и для случайных стратегий удаления. Микросервис предоставляет REST API: справочники датасетов и методов, старт/статус/результаты экспериментов, только removal по сохранённым весам, выдачу данных для Plotly (в т.\,ч.\ опциональное сглаживание кривых \emph{только для отображения}), скачивание артефактов, экспорт CSV подвыборки train. UI на Streamlit опрашивает API. Зависимости перечислены в \texttt{requirements.txt} (pandas, scikit-learn, torch, pydvl, бустинги, FastAPI, Streamlit, Plotly и др.).
```

---

## Примечания для вёрстки

- В заголовке секции можно оставить акцент на Zillow или заменить на нейтральный «Система сравнения методов влияния данных», если отчёт не привязан к одному датасету.
- При необходимости добавьте ссылку на pyDVL с версией из окружения (`import pydvl; pydvl.__version__`).
- Число записей в \texttt{properties\_2016.csv} в коде не захардкожено; при желании уточните по фактическому файлу в вашей копии данных.
