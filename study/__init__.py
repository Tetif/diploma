"""Influence / data-valuation study: does removing low-value training points help?

Entry point: ``run_study.py`` (repository root). Layout:
  config.py   - RunSpec, the main study and the sensitivity sweep grids
  data.py     - dataset loading, per-seed splits, label/target noise injection
  values.py   - data values per method (LOO, TMC, KNN-Shapley, Data-OOB, Influence, LiSSA, LossHigh)
  protocol.py - one (study, dataset, seed): baseline, values, removal curves, noise detection
  io.py       - results/<study>/<dataset>/<method>/seed<k>/results.json
"""
