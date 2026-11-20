# Paired comparison with random removal

'removed = auc' is the mean signed gain over the whole removal grid (relative to the full-data model).

| study | dataset | method | strategy | removed | n | Δ vs random | 95 % CI | p | better |
|---|---|---|---|---|---|---|---|---|---|
| clean | adult | DataOOB | lowest | 5 % | 5 | +0.0004 | [-0.0037, +0.0078] | 0.924 | 1/5 |
| clean | adult | DataOOB | lowest | 10 % | 5 | -0.0014 | [-0.0047, +0.0022] | 0.513 | 2/5 |
| clean | adult | DataOOB | lowest | 20 % | 5 | +0.0080 | [-0.0027, +0.0189] | 0.272 | 3/5 |
| clean | adult | DataOOB | lowest | 30 % | 5 | -0.0125 | [-0.0191, -0.0051] | 0.036 | 1/5 |
| clean | adult | DataOOB | lowest | auc | 5 | +0.0003 | [-0.0050, +0.0051] | 0.919 | 3/5 |
| clean | adult | DataOOB | highest | 5 % | 5 | +0.0005 | [-0.0026, +0.0037] | 0.784 | 2/5 |
| clean | adult | DataOOB | highest | 10 % | 5 | +0.0015 | [-0.0037, +0.0080] | 0.669 | 2/5 |
| clean | adult | DataOOB | highest | 20 % | 5 | -0.0009 | [-0.0154, +0.0091] | 0.907 | 4/5 |
| clean | adult | DataOOB | highest | 30 % | 5 | -0.0109 | [-0.0248, -0.0021] | 0.193 | 0/5 |
| clean | adult | DataOOB | highest | auc | 5 | -0.0017 | [-0.0079, +0.0043] | 0.661 | 2/5 |
| clean | adult | Influence | lowest | 5 % | 5 | -0.0054 | [-0.0093, -0.0006] | 0.103 | 1/5 |
| clean | adult | Influence | lowest | 10 % | 5 | +0.0004 | [-0.0028, +0.0036] | 0.827 | 3/5 |
| clean | adult | Influence | lowest | 20 % | 5 | +0.0000 | [-0.0133, +0.0100] | 0.997 | 3/5 |
| clean | adult | Influence | lowest | 30 % | 5 | -0.0054 | [-0.0134, +0.0036] | 0.336 | 1/5 |
| clean | adult | Influence | lowest | auc | 5 | -0.0017 | [-0.0049, +0.0021] | 0.451 | 1/5 |
| clean | adult | Influence | highest | 5 % | 5 | +0.0034 | [-0.0018, +0.0097] | 0.390 | 3/5 |
| clean | adult | Influence | highest | 10 % | 5 | -0.0078 | [-0.0125, -0.0032] | 0.045 | 0/5 |
| clean | adult | Influence | highest | 20 % | 5 | +0.0041 | [-0.0006, +0.0091] | 0.220 | 4/5 |
| clean | adult | Influence | highest | 30 % | 5 | -0.0065 | [-0.0158, +0.0022] | 0.286 | 1/5 |
| clean | adult | Influence | highest | auc | 5 | -0.0011 | [-0.0023, +0.0001] | 0.189 | 1/5 |
| clean | adult | KNNShapley | lowest | 5 % | 5 | +0.0055 | [-0.0011, +0.0124] | 0.229 | 3/5 |
| clean | adult | KNNShapley | lowest | 10 % | 5 | +0.0020 | [-0.0051, +0.0116] | 0.705 | 2/5 |
| clean | adult | KNNShapley | lowest | 20 % | 5 | -0.0054 | [-0.0174, +0.0020] | 0.427 | 3/5 |
| clean | adult | KNNShapley | lowest | 30 % | 5 | -0.0206 | [-0.0288, -0.0125] | 0.011 | 0/5 |
| clean | adult | KNNShapley | lowest | auc | 5 | -0.0038 | [-0.0096, +0.0019] | 0.321 | 1/5 |
| clean | adult | KNNShapley | highest | 5 % | 5 | -0.0042 | [-0.0078, -0.0004] | 0.127 | 1/5 |
| clean | adult | KNNShapley | highest | 10 % | 5 | -0.0125 | [-0.0215, -0.0036] | 0.082 | 0/5 |
| clean | adult | KNNShapley | highest | 20 % | 5 | -0.0266 | [-0.0491, -0.0041] | 0.111 | 2/5 |
| clean | adult | KNNShapley | highest | 30 % | 5 | -0.0442 | [-0.0638, -0.0259] | 0.014 | 0/5 |
| clean | adult | KNNShapley | highest | auc | 5 | -0.0201 | [-0.0305, -0.0075] | 0.037 | 1/5 |
| clean | adult | LOO | lowest | 5 % | 5 | +0.0009 | [-0.0072, +0.0097] | 0.869 | 3/5 |
| clean | adult | LOO | lowest | 10 % | 5 | +0.0035 | [-0.0007, +0.0070] | 0.191 | 4/5 |
| clean | adult | LOO | lowest | 20 % | 5 | +0.0055 | [-0.0001, +0.0106] | 0.152 | 4/5 |
| clean | adult | LOO | lowest | 30 % | 5 | -0.0063 | [-0.0149, +0.0026] | 0.287 | 2/5 |
| clean | adult | LOO | lowest | auc | 5 | +0.0018 | [-0.0020, +0.0053] | 0.430 | 3/5 |
| clean | adult | LOO | highest | 5 % | 5 | +0.0013 | [-0.0025, +0.0066] | 0.659 | 2/5 |
| clean | adult | LOO | highest | 10 % | 5 | +0.0007 | [-0.0016, +0.0030] | 0.624 | 3/5 |
| clean | adult | LOO | highest | 20 % | 5 | +0.0014 | [-0.0050, +0.0079] | 0.721 | 3/5 |
| clean | adult | LOO | highest | 30 % | 5 | -0.0034 | [-0.0112, +0.0032] | 0.457 | 2/5 |
| clean | adult | LOO | highest | auc | 5 | +0.0003 | [-0.0024, +0.0032] | 0.864 | 2/5 |
| clean | adult | LissaInfluence | lowest | 5 % | 5 | -0.0022 | [-0.0100, +0.0066] | 0.676 | 2/5 |
| clean | adult | LissaInfluence | lowest | 10 % | 5 | -0.0140 | [-0.0294, -0.0007] | 0.159 | 1/5 |
| clean | adult | LissaInfluence | lowest | 20 % | 5 | -0.0241 | [-0.0426, -0.0055] | 0.087 | 1/5 |
| clean | adult | LissaInfluence | lowest | 30 % | 5 | -0.0462 | [-0.0613, -0.0311] | 0.006 | 0/5 |
| clean | adult | LissaInfluence | lowest | auc | 5 | -0.0196 | [-0.0317, -0.0062] | 0.056 | 1/5 |
| clean | adult | LissaInfluence | highest | 5 % | 5 | -0.0037 | [-0.0087, +0.0013] | 0.299 | 1/5 |
| clean | adult | LissaInfluence | highest | 10 % | 5 | -0.0098 | [-0.0172, -0.0028] | 0.077 | 1/5 |
| clean | adult | LissaInfluence | highest | 20 % | 5 | -0.0207 | [-0.0404, -0.0036] | 0.120 | 0/5 |
| clean | adult | LissaInfluence | highest | 30 % | 5 | -0.0528 | [-0.0935, -0.0208] | 0.064 | 0/5 |
| clean | adult | LissaInfluence | highest | auc | 5 | -0.0188 | [-0.0293, -0.0082] | 0.035 | 0/5 |
| clean | adult | LossHigh | lowest | 5 % | 5 | +0.0035 | [+0.0005, +0.0066] | 0.113 | 4/5 |
| clean | adult | LossHigh | lowest | 10 % | 5 | +0.0075 | [+0.0032, +0.0120] | 0.041 | 5/5 |
| clean | adult | LossHigh | lowest | 20 % | 5 | -0.0001 | [-0.0116, +0.0116] | 0.984 | 2/5 |
| clean | adult | LossHigh | lowest | 30 % | 5 | -0.0123 | [-0.0200, -0.0032] | 0.069 | 1/5 |
| clean | adult | LossHigh | lowest | auc | 5 | +0.0004 | [-0.0055, +0.0067] | 0.919 | 2/5 |
| clean | adult | LossHigh | highest | 5 % | 5 | -0.0074 | [-0.0132, -0.0029] | 0.072 | 0/5 |
| clean | adult | LossHigh | highest | 10 % | 5 | +0.0011 | [-0.0013, +0.0028] | 0.406 | 4/5 |
| clean | adult | LossHigh | highest | 20 % | 5 | +0.0018 | [-0.0058, +0.0101] | 0.716 | 3/5 |
| clean | adult | LossHigh | highest | 30 % | 5 | -0.0014 | [-0.0083, +0.0057] | 0.743 | 2/5 |
| clean | adult | LossHigh | highest | auc | 5 | -0.0006 | [-0.0041, +0.0034] | 0.799 | 2/5 |
| clean | covertype | DataOOB | lowest | 5 % | 5 | +0.0030 | [-0.0035, +0.0073] | 0.403 | 4/5 |
| clean | covertype | DataOOB | lowest | 10 % | 5 | +0.0024 | [-0.0037, +0.0082] | 0.535 | 3/5 |
| clean | covertype | DataOOB | lowest | 20 % | 5 | +0.0027 | [-0.0064, +0.0102] | 0.600 | 3/5 |
| clean | covertype | DataOOB | lowest | 30 % | 5 | -0.0023 | [-0.0076, +0.0014] | 0.440 | 2/5 |
| clean | covertype | DataOOB | lowest | auc | 5 | +0.0016 | [-0.0045, +0.0063] | 0.628 | 3/5 |
| clean | covertype | DataOOB | highest | 5 % | 5 | -0.0016 | [-0.0094, +0.0042] | 0.704 | 3/5 |
| clean | covertype | DataOOB | highest | 10 % | 5 | +0.0026 | [-0.0005, +0.0054] | 0.216 | 4/5 |
| clean | covertype | DataOOB | highest | 20 % | 5 | -0.0031 | [-0.0058, -0.0008] | 0.095 | 0/5 |
| clean | covertype | DataOOB | highest | 30 % | 5 | -0.0156 | [-0.0194, -0.0118] | 0.002 | 0/5 |
| clean | covertype | DataOOB | highest | auc | 5 | -0.0033 | [-0.0052, -0.0011] | 0.051 | 1/5 |
| clean | covertype | Influence | lowest | 5 % | 5 | +0.0004 | [-0.0044, +0.0052] | 0.885 | 3/5 |
| clean | covertype | Influence | lowest | 10 % | 5 | -0.0013 | [-0.0037, +0.0016] | 0.434 | 1/5 |
| clean | covertype | Influence | lowest | 20 % | 5 | -0.0062 | [-0.0132, -0.0012] | 0.164 | 0/5 |
| clean | covertype | Influence | lowest | 30 % | 5 | -0.0090 | [-0.0132, -0.0048] | 0.019 | 0/5 |
| clean | covertype | Influence | lowest | auc | 5 | -0.0038 | [-0.0073, -0.0006] | 0.121 | 1/5 |
| clean | covertype | Influence | highest | 5 % | 5 | -0.0035 | [-0.0080, +0.0023] | 0.296 | 1/5 |
| clean | covertype | Influence | highest | 10 % | 5 | -0.0070 | [-0.0141, -0.0005] | 0.154 | 1/5 |
| clean | covertype | Influence | highest | 20 % | 5 | -0.0134 | [-0.0228, -0.0034] | 0.080 | 1/5 |
| clean | covertype | Influence | highest | 30 % | 5 | -0.0173 | [-0.0220, -0.0122] | 0.003 | 0/5 |
| clean | covertype | Influence | highest | auc | 5 | -0.0097 | [-0.0131, -0.0057] | 0.010 | 0/5 |
| clean | covertype | KNNShapley | lowest | 5 % | 5 | -0.0012 | [-0.0075, +0.0038] | 0.729 | 3/5 |
| clean | covertype | KNNShapley | lowest | 10 % | 5 | -0.0040 | [-0.0090, +0.0001] | 0.184 | 1/5 |
| clean | covertype | KNNShapley | lowest | 20 % | 5 | -0.0299 | [-0.0392, -0.0232] | 0.003 | 0/5 |
| clean | covertype | KNNShapley | lowest | 30 % | 5 | -0.0492 | [-0.0541, -0.0432] | 0.000 | 0/5 |
| clean | covertype | KNNShapley | lowest | auc | 5 | -0.0194 | [-0.0238, -0.0161] | 0.001 | 0/5 |
| clean | covertype | KNNShapley | highest | 5 % | 5 | -0.0079 | [-0.0151, -0.0003] | 0.128 | 1/5 |
| clean | covertype | KNNShapley | highest | 10 % | 5 | -0.0202 | [-0.0306, -0.0107] | 0.025 | 0/5 |
| clean | covertype | KNNShapley | highest | 20 % | 5 | -0.0462 | [-0.0667, -0.0251] | 0.018 | 0/5 |
| clean | covertype | KNNShapley | highest | 30 % | 5 | -0.0904 | [-0.1090, -0.0721] | 0.001 | 0/5 |
| clean | covertype | KNNShapley | highest | auc | 5 | -0.0368 | [-0.0489, -0.0248] | 0.006 | 0/5 |
| clean | covertype | LOO | lowest | 5 % | 5 | +0.0032 | [-0.0038, +0.0090] | 0.440 | 4/5 |
| clean | covertype | LOO | lowest | 10 % | 5 | +0.0017 | [-0.0020, +0.0066] | 0.516 | 2/5 |
| clean | covertype | LOO | lowest | 20 % | 5 | -0.0012 | [-0.0045, +0.0032] | 0.624 | 1/5 |
| clean | covertype | LOO | lowest | 30 % | 5 | -0.0027 | [-0.0047, -0.0003] | 0.105 | 1/5 |
| clean | covertype | LOO | lowest | auc | 5 | +0.0001 | [-0.0017, +0.0027] | 0.942 | 2/5 |
| clean | covertype | LOO | highest | 5 % | 5 | +0.0011 | [-0.0043, +0.0070] | 0.758 | 2/5 |
| clean | covertype | LOO | highest | 10 % | 5 | -0.0012 | [-0.0039, +0.0005] | 0.416 | 2/5 |
| clean | covertype | LOO | highest | 20 % | 5 | -0.0050 | [-0.0114, +0.0016] | 0.247 | 1/5 |
| clean | covertype | LOO | highest | 30 % | 5 | -0.0086 | [-0.0140, -0.0032] | 0.055 | 1/5 |
| clean | covertype | LOO | highest | auc | 5 | -0.0032 | [-0.0067, -0.0001] | 0.182 | 1/5 |
| clean | covertype | LissaInfluence | lowest | 5 % | 5 | -0.0003 | [-0.0050, +0.0040] | 0.909 | 3/5 |
| clean | covertype | LissaInfluence | lowest | 10 % | 5 | -0.0096 | [-0.0148, -0.0046] | 0.036 | 0/5 |
| clean | covertype | LissaInfluence | lowest | 20 % | 5 | -0.0399 | [-0.0473, -0.0319] | 0.001 | 0/5 |
| clean | covertype | LissaInfluence | lowest | 30 % | 5 | -0.0736 | [-0.0876, -0.0624] | 0.001 | 0/5 |
| clean | covertype | LissaInfluence | lowest | auc | 5 | -0.0280 | [-0.0344, -0.0217] | 0.002 | 0/5 |
| clean | covertype | LissaInfluence | highest | 5 % | 5 | -0.0090 | [-0.0138, -0.0043] | 0.030 | 0/5 |
| clean | covertype | LissaInfluence | highest | 10 % | 5 | -0.0192 | [-0.0243, -0.0152] | 0.002 | 0/5 |
| clean | covertype | LissaInfluence | highest | 20 % | 5 | -0.0410 | [-0.0500, -0.0308] | 0.002 | 0/5 |
| clean | covertype | LissaInfluence | highest | 30 % | 5 | -0.0653 | [-0.0882, -0.0484] | 0.005 | 0/5 |
| clean | covertype | LissaInfluence | highest | auc | 5 | -0.0309 | [-0.0374, -0.0244] | 0.001 | 0/5 |
| clean | covertype | LossHigh | lowest | 5 % | 5 | +0.0004 | [-0.0060, +0.0054] | 0.911 | 3/5 |
| clean | covertype | LossHigh | lowest | 10 % | 5 | -0.0003 | [-0.0049, +0.0043] | 0.923 | 2/5 |
| clean | covertype | LossHigh | lowest | 20 % | 5 | -0.0068 | [-0.0116, -0.0022] | 0.071 | 0/5 |
| clean | covertype | LossHigh | lowest | 30 % | 5 | -0.0126 | [-0.0193, -0.0070] | 0.021 | 0/5 |
| clean | covertype | LossHigh | lowest | auc | 5 | -0.0044 | [-0.0059, -0.0034] | 0.005 | 0/5 |
| clean | covertype | LossHigh | highest | 5 % | 5 | -0.0014 | [-0.0069, +0.0054] | 0.722 | 1/5 |
| clean | covertype | LossHigh | highest | 10 % | 5 | -0.0009 | [-0.0055, +0.0033] | 0.725 | 2/5 |
| clean | covertype | LossHigh | highest | 20 % | 5 | -0.0053 | [-0.0082, -0.0012] | 0.056 | 1/5 |
| clean | covertype | LossHigh | highest | 30 % | 5 | -0.0206 | [-0.0310, -0.0122] | 0.016 | 0/5 |
| clean | covertype | LossHigh | highest | auc | 5 | -0.0057 | [-0.0091, -0.0022] | 0.049 | 1/5 |
| clean | housing | DataOOB | lowest | 5 % | 5 | +188.3127 | [-464.2836, +840.9091] | 0.647 | 2/5 |
| clean | housing | DataOOB | lowest | 10 % | 5 | -86.7043 | [-750.2040, +576.7955] | 0.832 | 2/5 |
| clean | housing | DataOOB | lowest | 20 % | 5 | +127.9468 | [-824.7759, +1101.0884] | 0.828 | 2/5 |
| clean | housing | DataOOB | lowest | 30 % | 5 | -858.3854 | [-1898.6393, -56.5397] | 0.184 | 1/5 |
| clean | housing | DataOOB | lowest | auc | 5 | -90.7059 | [-714.6349, +373.8259] | 0.787 | 3/5 |
| clean | housing | DataOOB | highest | 5 % | 5 | -567.4196 | [-1271.4868, +156.2539] | 0.243 | 1/5 |
| clean | housing | DataOOB | highest | 10 % | 5 | -1227.2136 | [-2198.4158, -164.9305] | 0.119 | 1/5 |
| clean | housing | DataOOB | highest | 20 % | 5 | -2039.3349 | [-3717.5922, -265.9227] | 0.108 | 1/5 |
| clean | housing | DataOOB | highest | 30 % | 5 | -4216.3018 | [-5798.5462, -2703.3011] | 0.009 | 0/5 |
| clean | housing | DataOOB | highest | auc | 5 | -1783.8686 | [-2696.4413, -748.4970] | 0.035 | 1/5 |
| clean | housing | Influence | lowest | 5 % | 5 | +214.7079 | [+26.0311, +403.3848] | 0.127 | 4/5 |
| clean | housing | Influence | lowest | 10 % | 5 | +8.6481 | [-1060.8838, +1064.5115] | 0.989 | 2/5 |
| clean | housing | Influence | lowest | 20 % | 5 | +921.7117 | [+288.9165, +1554.5069] | 0.069 | 5/5 |
| clean | housing | Influence | lowest | 30 % | 5 | -252.9411 | [-977.9219, +606.1958] | 0.618 | 2/5 |
| clean | housing | Influence | lowest | auc | 5 | +303.0270 | [+23.9532, +609.1294] | 0.165 | 4/5 |
| clean | housing | Influence | highest | 5 % | 5 | +64.7236 | [-846.1345, +975.5817] | 0.911 | 3/5 |
| clean | housing | Influence | highest | 10 % | 5 | +2.7468 | [-409.3544, +602.0575] | 0.993 | 1/5 |
| clean | housing | Influence | highest | 20 % | 5 | +145.6073 | [-817.2897, +1247.2935] | 0.818 | 2/5 |
| clean | housing | Influence | highest | 30 % | 5 | -481.7680 | [-1389.2364, +346.5814] | 0.391 | 2/5 |
| clean | housing | Influence | highest | auc | 5 | -20.2850 | [-545.7402, +508.0821] | 0.951 | 3/5 |
| clean | housing | LOO | lowest | 5 % | 5 | +435.0200 | [-347.6417, +1320.4005] | 0.413 | 3/5 |
| clean | housing | LOO | lowest | 10 % | 5 | +85.3570 | [-263.4151, +445.9425] | 0.678 | 4/5 |
| clean | housing | LOO | lowest | 20 % | 5 | +362.2533 | [-357.5621, +1293.5704] | 0.507 | 2/5 |
| clean | housing | LOO | lowest | 30 % | 5 | +366.3320 | [-686.3770, +1468.3187] | 0.593 | 2/5 |
| clean | housing | LOO | lowest | auc | 5 | +275.6490 | [-137.4388, +799.4468] | 0.365 | 3/5 |
| clean | housing | LOO | highest | 5 % | 5 | -16.9761 | [-425.8117, +457.9236] | 0.950 | 2/5 |
| clean | housing | LOO | highest | 10 % | 5 | +107.2191 | [-571.0267, +845.3830] | 0.806 | 3/5 |
| clean | housing | LOO | highest | 20 % | 5 | -556.3795 | [-1231.4081, +226.7322] | 0.241 | 1/5 |
| clean | housing | LOO | highest | 30 % | 5 | -841.9005 | [-2117.3875, +513.7754] | 0.329 | 2/5 |
| clean | housing | LOO | highest | auc | 5 | -301.8012 | [-816.3567, +282.3251] | 0.390 | 2/5 |
| clean | housing | LissaInfluence | lowest | 5 % | 5 | +577.8886 | [-131.1513, +1279.4229] | 0.235 | 4/5 |
| clean | housing | LissaInfluence | lowest | 10 % | 5 | +220.4069 | [-460.1687, +1075.7626] | 0.648 | 2/5 |
| clean | housing | LissaInfluence | lowest | 20 % | 5 | -442.8412 | [-1703.3926, +733.2870] | 0.559 | 2/5 |
| clean | housing | LissaInfluence | lowest | 30 % | 5 | -1665.7576 | [-3249.8382, -618.7248] | 0.102 | 0/5 |
| clean | housing | LissaInfluence | lowest | auc | 5 | -273.8235 | [-1088.3380, +279.9786] | 0.547 | 2/5 |
| clean | housing | LissaInfluence | highest | 5 % | 5 | -1471.6908 | [-2216.7852, -614.4552] | 0.036 | 1/5 |
| clean | housing | LissaInfluence | highest | 10 % | 5 | -2824.2340 | [-3356.0055, -2319.2422] | 0.001 | 0/5 |
| clean | housing | LissaInfluence | highest | 20 % | 5 | -5880.3472 | [-6898.7141, -4889.3690] | 0.001 | 0/5 |
| clean | housing | LissaInfluence | highest | 30 % | 5 | -8228.3259 | [-9291.7039, -7168.7358] | 0.000 | 0/5 |
| clean | housing | LissaInfluence | highest | auc | 5 | -4282.8437 | [-4847.5922, -3719.0231] | 0.000 | 0/5 |
| clean | housing | LossHigh | lowest | 5 % | 5 | +215.8601 | [-199.6819, +530.7694] | 0.363 | 4/5 |
| clean | housing | LossHigh | lowest | 10 % | 5 | +345.6100 | [-391.8732, +1033.2760] | 0.450 | 3/5 |
| clean | housing | LossHigh | lowest | 20 % | 5 | +225.6039 | [-402.6008, +975.3652] | 0.591 | 2/5 |
| clean | housing | LossHigh | lowest | 30 % | 5 | -111.6791 | [-1000.8184, +472.3481] | 0.812 | 3/5 |
| clean | housing | LossHigh | lowest | auc | 5 | +178.9673 | [-139.1385, +489.6641] | 0.375 | 3/5 |
| clean | housing | LossHigh | highest | 5 % | 5 | -440.2972 | [-1123.0885, +364.1215] | 0.368 | 1/5 |
| clean | housing | LossHigh | highest | 10 % | 5 | +375.7061 | [-790.8373, +1229.3138] | 0.574 | 4/5 |
| clean | housing | LossHigh | highest | 20 % | 5 | +1431.5938 | [+49.8071, +2930.0422] | 0.157 | 4/5 |
| clean | housing | LossHigh | highest | 30 % | 5 | +233.5288 | [-1342.7179, +1798.2236] | 0.812 | 3/5 |
| clean | housing | LossHigh | highest | auc | 5 | +536.6631 | [+172.6854, +1149.2920] | 0.154 | 5/5 |
| clean | wine | DataOOB | lowest | 5 % | 5 | -0.0071 | [-0.0101, -0.0027] | 0.029 | 1/5 |
| clean | wine | DataOOB | lowest | 10 % | 5 | -0.0112 | [-0.0161, -0.0063] | 0.019 | 0/5 |
| clean | wine | DataOOB | lowest | 20 % | 5 | +0.0017 | [-0.0087, +0.0090] | 0.755 | 4/5 |
| clean | wine | DataOOB | lowest | 30 % | 5 | +0.0126 | [-0.0023, +0.0229] | 0.171 | 4/5 |
| clean | wine | DataOOB | lowest | auc | 5 | -0.0013 | [-0.0080, +0.0039] | 0.706 | 3/5 |
| clean | wine | DataOOB | highest | 5 % | 5 | -0.0068 | [-0.0098, -0.0036] | 0.019 | 0/5 |
| clean | wine | DataOOB | highest | 10 % | 5 | -0.0166 | [-0.0184, -0.0152] | 0.000 | 0/5 |
| clean | wine | DataOOB | highest | 20 % | 5 | -0.0264 | [-0.0325, -0.0186] | 0.003 | 0/5 |
| clean | wine | DataOOB | highest | 30 % | 5 | -0.0404 | [-0.0496, -0.0317] | 0.001 | 0/5 |
| clean | wine | DataOOB | highest | auc | 5 | -0.0208 | [-0.0245, -0.0166] | 0.001 | 0/5 |
| clean | wine | Influence | lowest | 5 % | 5 | -0.0078 | [-0.0108, -0.0048] | 0.011 | 0/5 |
| clean | wine | Influence | lowest | 10 % | 5 | -0.0057 | [-0.0106, -0.0007] | 0.115 | 1/5 |
| clean | wine | Influence | lowest | 20 % | 5 | -0.0023 | [-0.0101, +0.0056] | 0.633 | 2/5 |
| clean | wine | Influence | lowest | 30 % | 5 | -0.0023 | [-0.0148, +0.0106] | 0.771 | 2/5 |
| clean | wine | Influence | lowest | auc | 5 | -0.0039 | [-0.0101, +0.0023] | 0.338 | 2/5 |
| clean | wine | Influence | highest | 5 % | 5 | -0.0010 | [-0.0074, +0.0058] | 0.811 | 3/5 |
| clean | wine | Influence | highest | 10 % | 5 | +0.0025 | [-0.0044, +0.0095] | 0.579 | 3/5 |
| clean | wine | Influence | highest | 20 % | 5 | +0.0051 | [-0.0020, +0.0123] | 0.274 | 4/5 |
| clean | wine | Influence | highest | 30 % | 5 | +0.0070 | [+0.0022, +0.0119] | 0.069 | 4/5 |
| clean | wine | Influence | highest | auc | 5 | +0.0034 | [-0.0010, +0.0074] | 0.240 | 4/5 |
| clean | wine | LOO | lowest | 5 % | 5 | -0.0004 | [-0.0072, +0.0076] | 0.934 | 2/5 |
| clean | wine | LOO | lowest | 10 % | 5 | +0.0061 | [-0.0016, +0.0167] | 0.326 | 3/5 |
| clean | wine | LOO | lowest | 20 % | 5 | +0.0079 | [-0.0031, +0.0200] | 0.281 | 4/5 |
| clean | wine | LOO | lowest | 30 % | 5 | +0.0106 | [+0.0009, +0.0203] | 0.136 | 3/5 |
| clean | wine | LOO | lowest | auc | 5 | +0.0058 | [-0.0022, +0.0149] | 0.305 | 4/5 |
| clean | wine | LOO | highest | 5 % | 5 | -0.0057 | [-0.0095, -0.0012] | 0.076 | 1/5 |
| clean | wine | LOO | highest | 10 % | 5 | -0.0108 | [-0.0137, -0.0079] | 0.003 | 0/5 |
| clean | wine | LOO | highest | 20 % | 5 | -0.0147 | [-0.0233, -0.0050] | 0.047 | 1/5 |
| clean | wine | LOO | highest | 30 % | 5 | -0.0226 | [-0.0349, -0.0121] | 0.028 | 0/5 |
| clean | wine | LOO | highest | auc | 5 | -0.0123 | [-0.0178, -0.0067] | 0.019 | 0/5 |
| clean | wine | LissaInfluence | lowest | 5 % | 5 | +0.0002 | [-0.0057, +0.0069] | 0.962 | 2/5 |
| clean | wine | LissaInfluence | lowest | 10 % | 5 | -0.0005 | [-0.0106, +0.0095] | 0.931 | 2/5 |
| clean | wine | LissaInfluence | lowest | 20 % | 5 | -0.0091 | [-0.0230, +0.0089] | 0.383 | 1/5 |
| clean | wine | LissaInfluence | lowest | 30 % | 5 | -0.0158 | [-0.0327, +0.0021] | 0.204 | 1/5 |
| clean | wine | LissaInfluence | lowest | auc | 5 | -0.0058 | [-0.0159, +0.0060] | 0.422 | 1/5 |
| clean | wine | LissaInfluence | highest | 5 % | 5 | -0.0123 | [-0.0224, -0.0049] | 0.083 | 0/5 |
| clean | wine | LissaInfluence | highest | 10 % | 5 | -0.0190 | [-0.0294, -0.0097] | 0.029 | 0/5 |
| clean | wine | LissaInfluence | highest | 20 % | 5 | -0.0364 | [-0.0466, -0.0264] | 0.003 | 0/5 |
| clean | wine | LissaInfluence | highest | 30 % | 5 | -0.0676 | [-0.0861, -0.0492] | 0.003 | 0/5 |
| clean | wine | LissaInfluence | highest | auc | 5 | -0.0302 | [-0.0382, -0.0223] | 0.003 | 0/5 |
| clean | wine | LossHigh | lowest | 5 % | 5 | -0.0047 | [-0.0074, -0.0021] | 0.039 | 0/5 |
| clean | wine | LossHigh | lowest | 10 % | 5 | -0.0101 | [-0.0158, -0.0052] | 0.033 | 0/5 |
| clean | wine | LossHigh | lowest | 20 % | 5 | +0.0073 | [-0.0026, +0.0172] | 0.261 | 3/5 |
| clean | wine | LossHigh | lowest | 30 % | 5 | +0.0225 | [+0.0096, +0.0349] | 0.038 | 4/5 |
| clean | wine | LossHigh | lowest | auc | 5 | +0.0029 | [-0.0038, +0.0093] | 0.489 | 3/5 |
| clean | wine | LossHigh | highest | 5 % | 5 | +0.0004 | [-0.0026, +0.0032] | 0.836 | 3/5 |
| clean | wine | LossHigh | highest | 10 % | 5 | +0.0021 | [-0.0023, +0.0074] | 0.478 | 2/5 |
| clean | wine | LossHigh | highest | 20 % | 5 | -0.0053 | [-0.0095, +0.0006] | 0.152 | 1/5 |
| clean | wine | LossHigh | highest | 30 % | 5 | -0.0203 | [-0.0258, -0.0147] | 0.003 | 0/5 |
| clean | wine | LossHigh | highest | auc | 5 | -0.0045 | [-0.0067, -0.0024] | 0.027 | 0/5 |
| clean | wine | TMCShapley | lowest | 5 % | 5 | -0.0035 | [-0.0093, +0.0059] | 0.488 | 1/5 |
| clean | wine | TMCShapley | lowest | 10 % | 5 | -0.0037 | [-0.0114, +0.0038] | 0.433 | 1/5 |
| clean | wine | TMCShapley | lowest | 20 % | 5 | +0.0007 | [-0.0096, +0.0141] | 0.916 | 2/5 |
| clean | wine | TMCShapley | lowest | 30 % | 5 | +0.0030 | [-0.0099, +0.0183] | 0.729 | 2/5 |
| clean | wine | TMCShapley | lowest | auc | 5 | -0.0008 | [-0.0086, +0.0092] | 0.890 | 2/5 |
| clean | wine | TMCShapley | highest | 5 % | 5 | -0.0003 | [-0.0032, +0.0028] | 0.885 | 2/5 |
| clean | wine | TMCShapley | highest | 10 % | 5 | -0.0050 | [-0.0095, +0.0005] | 0.158 | 1/5 |
| clean | wine | TMCShapley | highest | 20 % | 5 | -0.0060 | [-0.0083, -0.0033] | 0.017 | 0/5 |
| clean | wine | TMCShapley | highest | 30 % | 5 | -0.0110 | [-0.0188, -0.0014] | 0.093 | 1/5 |
| clean | wine | TMCShapley | highest | auc | 5 | -0.0051 | [-0.0076, -0.0021] | 0.032 | 0/5 |
| damp-linear-0.0001 | adult | Influence | lowest | 5 % | 3 | +0.0059 | [-0.0022, +0.0203] | 0.497 | 1/3 |
| damp-linear-0.0001 | adult | Influence | lowest | 10 % | 3 | +0.0062 | [+0.0011, +0.0110] | 0.160 | 3/3 |
| damp-linear-0.0001 | adult | Influence | lowest | 20 % | 3 | -0.0044 | [-0.0119, +0.0048] | 0.464 | 1/3 |
| damp-linear-0.0001 | adult | Influence | lowest | auc | 3 | +0.0027 | [+0.0011, +0.0046] | 0.114 | 3/3 |
| damp-linear-0.0001 | adult | LissaInfluence | lowest | 5 % | 3 | +0.0071 | [-0.0001, +0.0205] | 0.402 | 2/3 |
| damp-linear-0.0001 | adult | LissaInfluence | lowest | 10 % | 3 | +0.0073 | [-0.0009, +0.0236] | 0.462 | 1/3 |
| damp-linear-0.0001 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0001 | [-0.0020, +0.0018] | 0.967 | 2/3 |
| damp-linear-0.0001 | adult | LissaInfluence | lowest | auc | 3 | +0.0045 | [-0.0008, +0.0144] | 0.459 | 1/3 |
| damp-linear-0.0001 | adult | LossHigh | lowest | 5 % | 3 | +0.0018 | [-0.0150, +0.0203] | 0.880 | 1/3 |
| damp-linear-0.0001 | adult | LossHigh | lowest | 10 % | 3 | +0.0089 | [+0.0031, +0.0166] | 0.158 | 3/3 |
| damp-linear-0.0001 | adult | LossHigh | lowest | 20 % | 3 | +0.0020 | [-0.0077, +0.0084] | 0.724 | 2/3 |
| damp-linear-0.0001 | adult | LossHigh | lowest | auc | 3 | +0.0043 | [-0.0005, +0.0093] | 0.272 | 2/3 |
| damp-linear-0.0001 | covertype | Influence | lowest | 5 % | 3 | -0.0057 | [-0.0210, +0.0066] | 0.557 | 1/3 |
| damp-linear-0.0001 | covertype | Influence | lowest | 10 % | 3 | -0.0033 | [-0.0100, +0.0008] | 0.437 | 1/3 |
| damp-linear-0.0001 | covertype | Influence | lowest | 20 % | 3 | -0.0334 | [-0.0394, -0.0294] | 0.008 | 0/3 |
| damp-linear-0.0001 | covertype | Influence | lowest | auc | 3 | -0.0110 | [-0.0128, -0.0100] | 0.007 | 0/3 |
| damp-linear-0.0001 | covertype | LissaInfluence | lowest | 5 % | 3 | -0.0128 | [-0.0390, +0.0052] | 0.440 | 1/3 |
| damp-linear-0.0001 | covertype | LissaInfluence | lowest | 10 % | 3 | -0.0116 | [-0.0168, -0.0042] | 0.093 | 0/3 |
| damp-linear-0.0001 | covertype | LissaInfluence | lowest | 20 % | 3 | -0.0403 | [-0.0488, -0.0278] | 0.024 | 0/3 |
| damp-linear-0.0001 | covertype | LissaInfluence | lowest | auc | 3 | -0.0176 | [-0.0185, -0.0161] | 0.002 | 0/3 |
| damp-linear-0.0001 | covertype | LossHigh | lowest | 5 % | 3 | +0.0017 | [-0.0012, +0.0072] | 0.608 | 1/3 |
| damp-linear-0.0001 | covertype | LossHigh | lowest | 10 % | 3 | +0.0077 | [-0.0022, +0.0246] | 0.458 | 2/3 |
| damp-linear-0.0001 | covertype | LossHigh | lowest | 20 % | 3 | -0.0109 | [-0.0158, -0.0010] | 0.159 | 0/3 |
| damp-linear-0.0001 | covertype | LossHigh | lowest | auc | 3 | +0.0006 | [-0.0039, +0.0050] | 0.837 | 2/3 |
| damp-linear-0.0001 | housing | Influence | lowest | 5 % | 3 | -396.2137 | [-2756.4626, +2019.9753] | 0.801 | 1/3 |
| damp-linear-0.0001 | housing | Influence | lowest | 10 % | 3 | -2549.2715 | [-5333.5081, +13.5215] | 0.241 | 1/3 |
| damp-linear-0.0001 | housing | Influence | lowest | 20 % | 3 | -5463.5794 | [-6978.4391, -2938.6505] | 0.050 | 0/3 |
| damp-linear-0.0001 | housing | Influence | lowest | auc | 3 | -2420.9251 | [-4433.7910, -224.5982] | 0.185 | 0/3 |
| damp-linear-0.0001 | housing | LissaInfluence | lowest | 5 % | 3 | -824.8658 | [-2829.7506, +1552.7098] | 0.585 | 1/3 |
| damp-linear-0.0001 | housing | LissaInfluence | lowest | 10 % | 3 | -3225.2854 | [-5112.5917, -1669.2404] | 0.085 | 0/3 |
| damp-linear-0.0001 | housing | LissaInfluence | lowest | 20 % | 3 | -7214.7882 | [-8388.2275, -5087.4745] | 0.021 | 0/3 |
| damp-linear-0.0001 | housing | LissaInfluence | lowest | auc | 3 | -3219.3955 | [-4666.8251, -1509.6563] | 0.073 | 0/3 |
| damp-linear-0.0001 | housing | LossHigh | lowest | 5 % | 3 | -310.1900 | [-1051.8491, +753.0087] | 0.627 | 1/3 |
| damp-linear-0.0001 | housing | LossHigh | lowest | 10 % | 3 | +856.4098 | [+496.8211, +1484.8543] | 0.113 | 3/3 |
| damp-linear-0.0001 | housing | LossHigh | lowest | 20 % | 3 | +1751.1071 | [+842.2871, +3112.4525] | 0.127 | 3/3 |
| damp-linear-0.0001 | housing | LossHigh | lowest | auc | 3 | +681.3829 | [+133.9174, +1523.1857] | 0.252 | 3/3 |
| damp-linear-0.0001 | wine | Influence | lowest | 5 % | 3 | +0.0053 | [-0.0065, +0.0130] | 0.468 | 2/3 |
| damp-linear-0.0001 | wine | Influence | lowest | 10 % | 3 | +0.0004 | [-0.0156, +0.0190] | 0.969 | 1/3 |
| damp-linear-0.0001 | wine | Influence | lowest | 20 % | 3 | -0.0077 | [-0.0369, +0.0091] | 0.653 | 2/3 |
| damp-linear-0.0001 | wine | Influence | lowest | auc | 3 | -0.0004 | [-0.0167, +0.0107] | 0.965 | 2/3 |
| damp-linear-0.0001 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0019 | [-0.0076, +0.0110] | 0.763 | 2/3 |
| damp-linear-0.0001 | wine | LissaInfluence | lowest | 10 % | 3 | +0.0022 | [-0.0206, +0.0176] | 0.865 | 2/3 |
| damp-linear-0.0001 | wine | LissaInfluence | lowest | 20 % | 3 | -0.0122 | [-0.0506, +0.0094] | 0.591 | 2/3 |
| damp-linear-0.0001 | wine | LissaInfluence | lowest | auc | 3 | -0.0017 | [-0.0222, +0.0117] | 0.882 | 2/3 |
| damp-linear-0.0001 | wine | LossHigh | lowest | 5 % | 3 | -0.0061 | [-0.0125, +0.0021] | 0.294 | 1/3 |
| damp-linear-0.0001 | wine | LossHigh | lowest | 10 % | 3 | +0.0033 | [-0.0045, +0.0106] | 0.532 | 2/3 |
| damp-linear-0.0001 | wine | LossHigh | lowest | 20 % | 3 | +0.0060 | [-0.0078, +0.0149] | 0.479 | 2/3 |
| damp-linear-0.0001 | wine | LossHigh | lowest | auc | 3 | +0.0012 | [-0.0056, +0.0082] | 0.791 | 2/3 |
| damp-linear-0.01 | adult | Influence | lowest | 5 % | 3 | +0.0028 | [-0.0096, +0.0174] | 0.758 | 2/3 |
| damp-linear-0.01 | adult | Influence | lowest | 10 % | 3 | +0.0119 | [+0.0068, +0.0157] | 0.046 | 3/3 |
| damp-linear-0.01 | adult | Influence | lowest | 20 % | 3 | +0.0018 | [-0.0014, +0.0035] | 0.388 | 2/3 |
| damp-linear-0.01 | adult | Influence | lowest | auc | 3 | +0.0056 | [+0.0010, +0.0089] | 0.140 | 3/3 |
| damp-linear-0.01 | adult | LissaInfluence | lowest | 5 % | 3 | +0.0071 | [-0.0001, +0.0205] | 0.402 | 2/3 |
| damp-linear-0.01 | adult | LissaInfluence | lowest | 10 % | 3 | +0.0073 | [-0.0009, +0.0236] | 0.462 | 1/3 |
| damp-linear-0.01 | adult | LissaInfluence | lowest | 20 % | 3 | +0.0021 | [-0.0003, +0.0055] | 0.344 | 2/3 |
| damp-linear-0.01 | adult | LissaInfluence | lowest | auc | 3 | +0.0050 | [-0.0003, +0.0153] | 0.430 | 2/3 |
| damp-linear-0.01 | adult | LossHigh | lowest | 5 % | 3 | +0.0018 | [-0.0150, +0.0203] | 0.880 | 1/3 |
| damp-linear-0.01 | adult | LossHigh | lowest | 10 % | 3 | +0.0089 | [+0.0031, +0.0166] | 0.158 | 3/3 |
| damp-linear-0.01 | adult | LossHigh | lowest | 20 % | 3 | +0.0020 | [-0.0077, +0.0084] | 0.724 | 2/3 |
| damp-linear-0.01 | adult | LossHigh | lowest | auc | 3 | +0.0043 | [-0.0005, +0.0093] | 0.272 | 2/3 |
| damp-linear-0.01 | covertype | Influence | lowest | 5 % | 3 | -0.0109 | [-0.0300, +0.0030] | 0.386 | 1/3 |
| damp-linear-0.01 | covertype | Influence | lowest | 10 % | 3 | -0.0116 | [-0.0286, +0.0000] | 0.313 | 0/3 |
| damp-linear-0.01 | covertype | Influence | lowest | 20 % | 3 | -0.0294 | [-0.0380, -0.0188] | 0.035 | 0/3 |
| damp-linear-0.01 | covertype | Influence | lowest | auc | 3 | -0.0144 | [-0.0178, -0.0122] | 0.014 | 0/3 |
| damp-linear-0.01 | covertype | LissaInfluence | lowest | 5 % | 3 | -0.0138 | [-0.0390, +0.0022] | 0.392 | 1/3 |
| damp-linear-0.01 | covertype | LissaInfluence | lowest | 10 % | 3 | -0.0102 | [-0.0158, -0.0042] | 0.093 | 0/3 |
| damp-linear-0.01 | covertype | LissaInfluence | lowest | 20 % | 3 | -0.0461 | [-0.0554, -0.0346] | 0.017 | 0/3 |
| damp-linear-0.01 | covertype | LissaInfluence | lowest | auc | 3 | -0.0188 | [-0.0200, -0.0172] | 0.002 | 0/3 |
| damp-linear-0.01 | covertype | LossHigh | lowest | 5 % | 3 | +0.0017 | [-0.0012, +0.0072] | 0.608 | 1/3 |
| damp-linear-0.01 | covertype | LossHigh | lowest | 10 % | 3 | +0.0077 | [-0.0022, +0.0246] | 0.458 | 2/3 |
| damp-linear-0.01 | covertype | LossHigh | lowest | 20 % | 3 | -0.0109 | [-0.0158, -0.0010] | 0.159 | 0/3 |
| damp-linear-0.01 | covertype | LossHigh | lowest | auc | 3 | +0.0006 | [-0.0039, +0.0050] | 0.837 | 2/3 |
| damp-linear-0.01 | housing | Influence | lowest | 5 % | 3 | -414.8675 | [-2947.7231, +2158.1689] | 0.805 | 1/3 |
| damp-linear-0.01 | housing | Influence | lowest | 10 % | 3 | -2507.7621 | [-4863.7779, -396.8389] | 0.192 | 0/3 |
| damp-linear-0.01 | housing | Influence | lowest | 20 % | 3 | -5924.3544 | [-7573.3776, -3620.5963] | 0.038 | 0/3 |
| damp-linear-0.01 | housing | Influence | lowest | auc | 3 | -2525.2163 | [-4454.1919, -514.4214] | 0.157 | 0/3 |
| damp-linear-0.01 | housing | LissaInfluence | lowest | 5 % | 3 | -899.4260 | [-2829.7506, +1329.0291] | 0.535 | 1/3 |
| damp-linear-0.01 | housing | LissaInfluence | lowest | 10 % | 3 | -3519.9257 | [-5758.1557, -1669.2404] | 0.099 | 0/3 |
| damp-linear-0.01 | housing | LissaInfluence | lowest | 20 % | 3 | -7214.7882 | [-8388.2275, -5087.4745] | 0.021 | 0/3 |
| damp-linear-0.01 | housing | LissaInfluence | lowest | auc | 3 | -3348.5257 | [-4908.9116, -1565.5765] | 0.075 | 0/3 |
| damp-linear-0.01 | housing | LossHigh | lowest | 5 % | 3 | -310.1900 | [-1051.8491, +753.0087] | 0.627 | 1/3 |
| damp-linear-0.01 | housing | LossHigh | lowest | 10 % | 3 | +856.4098 | [+496.8211, +1484.8543] | 0.113 | 3/3 |
| damp-linear-0.01 | housing | LossHigh | lowest | 20 % | 3 | +1751.1071 | [+842.2871, +3112.4525] | 0.127 | 3/3 |
| damp-linear-0.01 | housing | LossHigh | lowest | auc | 3 | +681.3829 | [+133.9174, +1523.1857] | 0.252 | 3/3 |
| damp-linear-0.01 | wine | Influence | lowest | 5 % | 3 | +0.0053 | [-0.0065, +0.0130] | 0.468 | 2/3 |
| damp-linear-0.01 | wine | Influence | lowest | 10 % | 3 | -0.0003 | [-0.0156, +0.0173] | 0.978 | 1/3 |
| damp-linear-0.01 | wine | Influence | lowest | 20 % | 3 | -0.0081 | [-0.0369, +0.0126] | 0.639 | 1/3 |
| damp-linear-0.01 | wine | Influence | lowest | auc | 3 | -0.0008 | [-0.0167, +0.0089] | 0.929 | 2/3 |
| damp-linear-0.01 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0019 | [-0.0076, +0.0110] | 0.763 | 2/3 |
| damp-linear-0.01 | wine | LissaInfluence | lowest | 10 % | 3 | +0.0025 | [-0.0206, +0.0183] | 0.852 | 2/3 |
| damp-linear-0.01 | wine | LissaInfluence | lowest | 20 % | 3 | -0.0122 | [-0.0506, +0.0094] | 0.591 | 2/3 |
| damp-linear-0.01 | wine | LissaInfluence | lowest | auc | 3 | -0.0017 | [-0.0222, +0.0120] | 0.889 | 2/3 |
| damp-linear-0.01 | wine | LossHigh | lowest | 5 % | 3 | -0.0061 | [-0.0125, +0.0021] | 0.294 | 1/3 |
| damp-linear-0.01 | wine | LossHigh | lowest | 10 % | 3 | +0.0033 | [-0.0045, +0.0106] | 0.532 | 2/3 |
| damp-linear-0.01 | wine | LossHigh | lowest | 20 % | 3 | +0.0060 | [-0.0078, +0.0149] | 0.479 | 2/3 |
| damp-linear-0.01 | wine | LossHigh | lowest | auc | 3 | +0.0012 | [-0.0056, +0.0082] | 0.791 | 2/3 |
| damp-linear-1 | adult | Influence | lowest | 5 % | 3 | +0.0002 | [-0.0028, +0.0030] | 0.931 | 2/3 |
| damp-linear-1 | adult | Influence | lowest | 10 % | 3 | +0.0091 | [-0.0015, +0.0242] | 0.362 | 2/3 |
| damp-linear-1 | adult | Influence | lowest | 20 % | 3 | +0.0087 | [+0.0042, +0.0151] | 0.118 | 3/3 |
| damp-linear-1 | adult | Influence | lowest | auc | 3 | +0.0056 | [+0.0025, +0.0115] | 0.197 | 3/3 |
| damp-linear-1 | adult | LissaInfluence | lowest | 5 % | 3 | +0.0042 | [-0.0037, +0.0185] | 0.616 | 1/3 |
| damp-linear-1 | adult | LissaInfluence | lowest | 10 % | 3 | +0.0109 | [+0.0013, +0.0287] | 0.346 | 3/3 |
| damp-linear-1 | adult | LissaInfluence | lowest | 20 % | 3 | +0.0072 | [+0.0064, +0.0080] | 0.004 | 3/3 |
| damp-linear-1 | adult | LissaInfluence | lowest | auc | 3 | +0.0069 | [+0.0015, +0.0171] | 0.308 | 3/3 |
| damp-linear-1 | adult | LossHigh | lowest | 5 % | 3 | +0.0018 | [-0.0150, +0.0203] | 0.880 | 1/3 |
| damp-linear-1 | adult | LossHigh | lowest | 10 % | 3 | +0.0089 | [+0.0031, +0.0166] | 0.158 | 3/3 |
| damp-linear-1 | adult | LossHigh | lowest | 20 % | 3 | +0.0020 | [-0.0077, +0.0084] | 0.724 | 2/3 |
| damp-linear-1 | adult | LossHigh | lowest | auc | 3 | +0.0043 | [-0.0005, +0.0093] | 0.272 | 2/3 |
| damp-linear-1 | covertype | Influence | lowest | 5 % | 3 | -0.0157 | [-0.0320, -0.0046] | 0.199 | 0/3 |
| damp-linear-1 | covertype | Influence | lowest | 10 % | 3 | -0.0137 | [-0.0252, +0.0026] | 0.244 | 1/3 |
| damp-linear-1 | covertype | Influence | lowest | 20 % | 3 | -0.0475 | [-0.0556, -0.0354] | 0.016 | 0/3 |
| damp-linear-1 | covertype | Influence | lowest | auc | 3 | -0.0209 | [-0.0235, -0.0159] | 0.014 | 0/3 |
| damp-linear-1 | covertype | LissaInfluence | lowest | 5 % | 3 | -0.0085 | [-0.0172, -0.0032] | 0.194 | 0/3 |
| damp-linear-1 | covertype | LissaInfluence | lowest | 10 % | 3 | -0.0143 | [-0.0264, +0.0006] | 0.212 | 1/3 |
| damp-linear-1 | covertype | LissaInfluence | lowest | 20 % | 3 | -0.0506 | [-0.0576, -0.0382] | 0.015 | 0/3 |
| damp-linear-1 | covertype | LissaInfluence | lowest | auc | 3 | -0.0201 | [-0.0247, -0.0136] | 0.026 | 0/3 |
| damp-linear-1 | covertype | LossHigh | lowest | 5 % | 3 | +0.0017 | [-0.0012, +0.0072] | 0.608 | 1/3 |
| damp-linear-1 | covertype | LossHigh | lowest | 10 % | 3 | +0.0077 | [-0.0022, +0.0246] | 0.458 | 2/3 |
| damp-linear-1 | covertype | LossHigh | lowest | 20 % | 3 | -0.0109 | [-0.0158, -0.0010] | 0.159 | 0/3 |
| damp-linear-1 | covertype | LossHigh | lowest | auc | 3 | +0.0006 | [-0.0039, +0.0050] | 0.837 | 2/3 |
| damp-linear-1 | housing | Influence | lowest | 5 % | 3 | -1060.7138 | [-3427.6756, +2039.3843] | 0.580 | 1/3 |
| damp-linear-1 | housing | Influence | lowest | 10 % | 3 | -3181.9777 | [-4821.1404, -811.9326] | 0.120 | 0/3 |
| damp-linear-1 | housing | Influence | lowest | 20 % | 3 | -7505.4062 | [-9382.3398, -4628.5392] | 0.036 | 0/3 |
| damp-linear-1 | housing | Influence | lowest | auc | 3 | -3334.7716 | [-4791.1814, -951.7634] | 0.109 | 0/3 |
| damp-linear-1 | housing | LissaInfluence | lowest | 5 % | 3 | -1302.5583 | [-2860.8688, +1206.9607] | 0.412 | 1/3 |
| damp-linear-1 | housing | LissaInfluence | lowest | 10 % | 3 | -3888.3271 | [-6576.1537, -1082.3973] | 0.134 | 0/3 |
| damp-linear-1 | housing | LissaInfluence | lowest | 20 % | 3 | -7384.6920 | [-8947.5301, -4674.7889] | 0.032 | 0/3 |
| damp-linear-1 | housing | LissaInfluence | lowest | auc | 3 | -3629.9352 | [-5314.2141, -1272.8560] | 0.096 | 0/3 |
| damp-linear-1 | housing | LossHigh | lowest | 5 % | 3 | -310.1900 | [-1051.8491, +753.0087] | 0.627 | 1/3 |
| damp-linear-1 | housing | LossHigh | lowest | 10 % | 3 | +856.4098 | [+496.8211, +1484.8543] | 0.113 | 3/3 |
| damp-linear-1 | housing | LossHigh | lowest | 20 % | 3 | +1751.1071 | [+842.2871, +3112.4525] | 0.127 | 3/3 |
| damp-linear-1 | housing | LossHigh | lowest | auc | 3 | +681.3829 | [+133.9174, +1523.1857] | 0.252 | 3/3 |
| damp-linear-1 | wine | Influence | lowest | 5 % | 3 | +0.0042 | [-0.0048, +0.0135] | 0.506 | 2/3 |
| damp-linear-1 | wine | Influence | lowest | 10 % | 3 | -0.0022 | [-0.0170, +0.0074] | 0.800 | 2/3 |
| damp-linear-1 | wine | Influence | lowest | 20 % | 3 | -0.0094 | [-0.0349, +0.0049] | 0.539 | 2/3 |
| damp-linear-1 | wine | Influence | lowest | auc | 3 | -0.0021 | [-0.0163, +0.0066] | 0.797 | 2/3 |
| damp-linear-1 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0059 | [-0.0036, +0.0165] | 0.415 | 2/3 |
| damp-linear-1 | wine | LissaInfluence | lowest | 10 % | 3 | -0.0004 | [-0.0184, +0.0126] | 0.969 | 2/3 |
| damp-linear-1 | wine | LissaInfluence | lowest | 20 % | 3 | -0.0106 | [-0.0452, +0.0121] | 0.606 | 2/3 |
| damp-linear-1 | wine | LissaInfluence | lowest | auc | 3 | -0.0013 | [-0.0191, +0.0088] | 0.895 | 2/3 |
| damp-linear-1 | wine | LossHigh | lowest | 5 % | 3 | -0.0061 | [-0.0125, +0.0021] | 0.294 | 1/3 |
| damp-linear-1 | wine | LossHigh | lowest | 10 % | 3 | +0.0033 | [-0.0045, +0.0106] | 0.532 | 2/3 |
| damp-linear-1 | wine | LossHigh | lowest | 20 % | 3 | +0.0060 | [-0.0078, +0.0149] | 0.479 | 2/3 |
| damp-linear-1 | wine | LossHigh | lowest | auc | 3 | +0.0012 | [-0.0056, +0.0082] | 0.791 | 2/3 |
| damp-linear-1e-06 | adult | Influence | lowest | 5 % | 3 | +0.0055 | [-0.0012, +0.0156] | 0.394 | 2/3 |
| damp-linear-1e-06 | adult | Influence | lowest | 10 % | 3 | +0.0114 | [+0.0081, +0.0136] | 0.021 | 3/3 |
| damp-linear-1e-06 | adult | Influence | lowest | 20 % | 3 | +0.0006 | [-0.0140, +0.0148] | 0.952 | 2/3 |
| damp-linear-1e-06 | adult | Influence | lowest | auc | 3 | +0.0058 | [+0.0046, +0.0073] | 0.018 | 3/3 |
| damp-linear-1e-06 | adult | LissaInfluence | lowest | 5 % | 3 | +0.0071 | [-0.0001, +0.0205] | 0.402 | 2/3 |
| damp-linear-1e-06 | adult | LissaInfluence | lowest | 10 % | 3 | +0.0073 | [-0.0009, +0.0236] | 0.462 | 1/3 |
| damp-linear-1e-06 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0001 | [-0.0020, +0.0018] | 0.967 | 2/3 |
| damp-linear-1e-06 | adult | LissaInfluence | lowest | auc | 3 | +0.0045 | [-0.0008, +0.0144] | 0.459 | 1/3 |
| damp-linear-1e-06 | adult | LossHigh | lowest | 5 % | 3 | +0.0018 | [-0.0150, +0.0203] | 0.880 | 1/3 |
| damp-linear-1e-06 | adult | LossHigh | lowest | 10 % | 3 | +0.0089 | [+0.0031, +0.0166] | 0.158 | 3/3 |
| damp-linear-1e-06 | adult | LossHigh | lowest | 20 % | 3 | +0.0020 | [-0.0077, +0.0084] | 0.724 | 2/3 |
| damp-linear-1e-06 | adult | LossHigh | lowest | auc | 3 | +0.0043 | [-0.0005, +0.0093] | 0.272 | 2/3 |
| damp-linear-1e-06 | covertype | Influence | lowest | 5 % | 3 | -0.0073 | [-0.0240, +0.0040] | 0.484 | 1/3 |
| damp-linear-1e-06 | covertype | Influence | lowest | 10 % | 3 | -0.0059 | [-0.0152, -0.0006] | 0.330 | 0/3 |
| damp-linear-1e-06 | covertype | Influence | lowest | 20 % | 3 | -0.0336 | [-0.0362, -0.0294] | 0.004 | 0/3 |
| damp-linear-1e-06 | covertype | Influence | lowest | auc | 3 | -0.0124 | [-0.0136, -0.0103] | 0.008 | 0/3 |
| damp-linear-1e-06 | covertype | LissaInfluence | lowest | 5 % | 3 | -0.0128 | [-0.0390, +0.0052] | 0.440 | 1/3 |
| damp-linear-1e-06 | covertype | LissaInfluence | lowest | 10 % | 3 | -0.0116 | [-0.0168, -0.0042] | 0.093 | 0/3 |
| damp-linear-1e-06 | covertype | LissaInfluence | lowest | 20 % | 3 | -0.0403 | [-0.0488, -0.0278] | 0.024 | 0/3 |
| damp-linear-1e-06 | covertype | LissaInfluence | lowest | auc | 3 | -0.0176 | [-0.0185, -0.0161] | 0.002 | 0/3 |
| damp-linear-1e-06 | covertype | LossHigh | lowest | 5 % | 3 | +0.0017 | [-0.0012, +0.0072] | 0.608 | 1/3 |
| damp-linear-1e-06 | covertype | LossHigh | lowest | 10 % | 3 | +0.0077 | [-0.0022, +0.0246] | 0.458 | 2/3 |
| damp-linear-1e-06 | covertype | LossHigh | lowest | 20 % | 3 | -0.0109 | [-0.0158, -0.0010] | 0.159 | 0/3 |
| damp-linear-1e-06 | covertype | LossHigh | lowest | auc | 3 | +0.0006 | [-0.0039, +0.0050] | 0.837 | 2/3 |
| damp-linear-1e-06 | housing | Influence | lowest | 5 % | 3 | -396.2137 | [-2756.4626, +2019.9753] | 0.801 | 1/3 |
| damp-linear-1e-06 | housing | Influence | lowest | 10 % | 3 | -2549.2715 | [-5333.5081, +13.5215] | 0.241 | 1/3 |
| damp-linear-1e-06 | housing | Influence | lowest | 20 % | 3 | -5531.1040 | [-7181.0129, -2938.6505] | 0.052 | 0/3 |
| damp-linear-1e-06 | housing | Influence | lowest | auc | 3 | -2437.8062 | [-4484.4344, -224.5982] | 0.187 | 0/3 |
| damp-linear-1e-06 | housing | LissaInfluence | lowest | 5 % | 3 | -824.8658 | [-2829.7506, +1552.7098] | 0.585 | 1/3 |
| damp-linear-1e-06 | housing | LissaInfluence | lowest | 10 % | 3 | -3225.2854 | [-5112.5917, -1669.2404] | 0.085 | 0/3 |
| damp-linear-1e-06 | housing | LissaInfluence | lowest | 20 % | 3 | -7241.2884 | [-8388.2275, -5087.4745] | 0.021 | 0/3 |
| damp-linear-1e-06 | housing | LissaInfluence | lowest | auc | 3 | -3226.0205 | [-4686.7003, -1509.6563] | 0.073 | 0/3 |
| damp-linear-1e-06 | housing | LossHigh | lowest | 5 % | 3 | -310.1900 | [-1051.8491, +753.0087] | 0.627 | 1/3 |
| damp-linear-1e-06 | housing | LossHigh | lowest | 10 % | 3 | +856.4098 | [+496.8211, +1484.8543] | 0.113 | 3/3 |
| damp-linear-1e-06 | housing | LossHigh | lowest | 20 % | 3 | +1751.1071 | [+842.2871, +3112.4525] | 0.127 | 3/3 |
| damp-linear-1e-06 | housing | LossHigh | lowest | auc | 3 | +681.3829 | [+133.9174, +1523.1857] | 0.252 | 3/3 |
| damp-linear-1e-06 | wine | Influence | lowest | 5 % | 3 | +0.0053 | [-0.0065, +0.0130] | 0.468 | 2/3 |
| damp-linear-1e-06 | wine | Influence | lowest | 10 % | 3 | +0.0004 | [-0.0156, +0.0190] | 0.969 | 1/3 |
| damp-linear-1e-06 | wine | Influence | lowest | 20 % | 3 | -0.0077 | [-0.0369, +0.0091] | 0.653 | 2/3 |
| damp-linear-1e-06 | wine | Influence | lowest | auc | 3 | -0.0004 | [-0.0167, +0.0107] | 0.965 | 2/3 |
| damp-linear-1e-06 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0019 | [-0.0076, +0.0110] | 0.763 | 2/3 |
| damp-linear-1e-06 | wine | LissaInfluence | lowest | 10 % | 3 | +0.0022 | [-0.0206, +0.0176] | 0.865 | 2/3 |
| damp-linear-1e-06 | wine | LissaInfluence | lowest | 20 % | 3 | -0.0122 | [-0.0506, +0.0094] | 0.591 | 2/3 |
| damp-linear-1e-06 | wine | LissaInfluence | lowest | auc | 3 | -0.0017 | [-0.0222, +0.0117] | 0.882 | 2/3 |
| damp-linear-1e-06 | wine | LossHigh | lowest | 5 % | 3 | -0.0061 | [-0.0125, +0.0021] | 0.294 | 1/3 |
| damp-linear-1e-06 | wine | LossHigh | lowest | 10 % | 3 | +0.0033 | [-0.0045, +0.0106] | 0.532 | 2/3 |
| damp-linear-1e-06 | wine | LossHigh | lowest | 20 % | 3 | +0.0060 | [-0.0078, +0.0149] | 0.479 | 2/3 |
| damp-linear-1e-06 | wine | LossHigh | lowest | auc | 3 | +0.0012 | [-0.0056, +0.0082] | 0.791 | 2/3 |
| damp-mlp-0.0001 | adult | Influence | lowest | 5 % | 3 | +0.0040 | [+0.0018, +0.0070] | 0.122 | 3/3 |
| damp-mlp-0.0001 | adult | Influence | lowest | 10 % | 3 | -0.0070 | [-0.0129, -0.0018] | 0.159 | 0/3 |
| damp-mlp-0.0001 | adult | Influence | lowest | 20 % | 3 | +0.0078 | [-0.0108, +0.0192] | 0.492 | 2/3 |
| damp-mlp-0.0001 | adult | Influence | lowest | auc | 3 | +0.0003 | [-0.0026, +0.0031] | 0.862 | 2/3 |
| damp-mlp-0.0001 | adult | LissaInfluence | lowest | 5 % | 3 | -0.0030 | [-0.0173, +0.0048] | 0.720 | 2/3 |
| damp-mlp-0.0001 | adult | LissaInfluence | lowest | 10 % | 3 | -0.0044 | [-0.0125, +0.0026] | 0.424 | 1/3 |
| damp-mlp-0.0001 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0155 | [-0.0287, +0.0019] | 0.230 | 1/3 |
| damp-mlp-0.0001 | adult | LissaInfluence | lowest | auc | 3 | -0.0063 | [-0.0162, +0.0027] | 0.371 | 1/3 |
| damp-mlp-0.0001 | adult | LossHigh | lowest | 5 % | 3 | +0.0036 | [-0.0006, +0.0076] | 0.264 | 2/3 |
| damp-mlp-0.0001 | adult | LossHigh | lowest | 10 % | 3 | -0.0046 | [-0.0075, -0.0009] | 0.139 | 0/3 |
| damp-mlp-0.0001 | adult | LossHigh | lowest | 20 % | 3 | -0.0128 | [-0.0249, -0.0041] | 0.178 | 0/3 |
| damp-mlp-0.0001 | adult | LossHigh | lowest | auc | 3 | -0.0040 | [-0.0047, -0.0033] | 0.009 | 0/3 |
| damp-mlp-0.0001 | housing | Influence | lowest | 5 % | 3 | +710.4238 | [-444.1957, +1593.8517] | 0.360 | 2/3 |
| damp-mlp-0.0001 | housing | Influence | lowest | 10 % | 3 | +1393.9779 | [+625.4683, +2361.3379] | 0.112 | 3/3 |
| damp-mlp-0.0001 | housing | Influence | lowest | 20 % | 3 | +1172.2944 | [-150.1665, +2361.6460] | 0.249 | 2/3 |
| damp-mlp-0.0001 | housing | Influence | lowest | auc | 3 | +993.4213 | [+85.9601, +1874.3761] | 0.194 | 3/3 |
| damp-mlp-0.0001 | housing | LissaInfluence | lowest | 5 % | 3 | +495.2529 | [-972.9307, +2427.3406] | 0.672 | 2/3 |
| damp-mlp-0.0001 | housing | LissaInfluence | lowest | 10 % | 3 | +758.7728 | [-559.1536, +2451.9052] | 0.483 | 2/3 |
| damp-mlp-0.0001 | housing | LissaInfluence | lowest | 20 % | 3 | -1064.9412 | [-2503.8692, +140.4905] | 0.302 | 1/3 |
| damp-mlp-0.0001 | housing | LissaInfluence | lowest | auc | 3 | +142.1177 | [-1078.8826, +1561.4222] | 0.870 | 1/3 |
| damp-mlp-0.0001 | housing | LossHigh | lowest | 5 % | 3 | -854.5566 | [-2476.7996, +84.1066] | 0.404 | 1/3 |
| damp-mlp-0.0001 | housing | LossHigh | lowest | 10 % | 3 | +3343.0733 | [+2049.3794, +4228.3931] | 0.037 | 3/3 |
| damp-mlp-0.0001 | housing | LossHigh | lowest | 20 % | 3 | +3239.0433 | [+1404.2656, +4165.5563] | 0.072 | 3/3 |
| damp-mlp-0.0001 | housing | LossHigh | lowest | auc | 3 | +1849.7741 | [+500.3838, +2579.7301] | 0.111 | 3/3 |
| damp-mlp-0.0001 | wine | Influence | lowest | 5 % | 3 | -0.0165 | [-0.0351, -0.0062] | 0.219 | 0/3 |
| damp-mlp-0.0001 | wine | Influence | lowest | 10 % | 3 | -0.0069 | [-0.0405, +0.0192] | 0.734 | 2/3 |
| damp-mlp-0.0001 | wine | Influence | lowest | 20 % | 3 | -0.0033 | [-0.0298, +0.0130] | 0.828 | 2/3 |
| damp-mlp-0.0001 | wine | Influence | lowest | auc | 3 | -0.0075 | [-0.0314, +0.0089] | 0.600 | 1/3 |
| damp-mlp-0.0001 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0063 | [-0.0159, +0.0325] | 0.700 | 2/3 |
| damp-mlp-0.0001 | wine | LissaInfluence | lowest | 10 % | 3 | +0.0006 | [-0.0328, +0.0267] | 0.977 | 2/3 |
| damp-mlp-0.0001 | wine | LissaInfluence | lowest | 20 % | 3 | +0.0049 | [-0.0135, +0.0184] | 0.659 | 2/3 |
| damp-mlp-0.0001 | wine | LissaInfluence | lowest | auc | 3 | +0.0030 | [-0.0197, +0.0206] | 0.824 | 2/3 |
| damp-mlp-0.0001 | wine | LossHigh | lowest | 5 % | 3 | -0.0201 | [-0.0247, -0.0125] | 0.034 | 0/3 |
| damp-mlp-0.0001 | wine | LossHigh | lowest | 10 % | 3 | +0.0063 | [-0.0082, +0.0163] | 0.486 | 2/3 |
| damp-mlp-0.0001 | wine | LossHigh | lowest | 20 % | 3 | -0.0029 | [-0.0060, +0.0013] | 0.315 | 1/3 |
| damp-mlp-0.0001 | wine | LossHigh | lowest | auc | 3 | -0.0034 | [-0.0072, -0.0014] | 0.216 | 0/3 |
| damp-mlp-0.01 | adult | Influence | lowest | 5 % | 3 | -0.0018 | [-0.0129, +0.0048] | 0.772 | 2/3 |
| damp-mlp-0.01 | adult | Influence | lowest | 10 % | 3 | +0.0039 | [-0.0102, +0.0170] | 0.669 | 2/3 |
| damp-mlp-0.01 | adult | Influence | lowest | 20 % | 3 | -0.0051 | [-0.0265, +0.0097] | 0.688 | 2/3 |
| damp-mlp-0.01 | adult | Influence | lowest | auc | 3 | -0.0003 | [-0.0137, +0.0080] | 0.972 | 2/3 |
| damp-mlp-0.01 | adult | LissaInfluence | lowest | 5 % | 3 | -0.0057 | [-0.0128, +0.0048] | 0.401 | 1/3 |
| damp-mlp-0.01 | adult | LissaInfluence | lowest | 10 % | 3 | -0.0050 | [-0.0125, +0.0026] | 0.372 | 1/3 |
| damp-mlp-0.01 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0165 | [-0.0283, -0.0016] | 0.170 | 0/3 |
| damp-mlp-0.01 | adult | LissaInfluence | lowest | auc | 3 | -0.0074 | [-0.0149, +0.0018] | 0.269 | 1/3 |
| damp-mlp-0.01 | adult | LossHigh | lowest | 5 % | 3 | +0.0036 | [-0.0006, +0.0076] | 0.264 | 2/3 |
| damp-mlp-0.01 | adult | LossHigh | lowest | 10 % | 3 | -0.0046 | [-0.0075, -0.0009] | 0.139 | 0/3 |
| damp-mlp-0.01 | adult | LossHigh | lowest | 20 % | 3 | -0.0128 | [-0.0249, -0.0041] | 0.178 | 0/3 |
| damp-mlp-0.01 | adult | LossHigh | lowest | auc | 3 | -0.0040 | [-0.0047, -0.0033] | 0.009 | 0/3 |
| damp-mlp-0.01 | housing | Influence | lowest | 5 % | 3 | +249.7485 | [+199.2103, +342.6246] | 0.033 | 3/3 |
| damp-mlp-0.01 | housing | Influence | lowest | 10 % | 3 | +1156.7629 | [+258.2869, +2244.5015] | 0.185 | 3/3 |
| damp-mlp-0.01 | housing | Influence | lowest | 20 % | 3 | +1037.1098 | [+626.8405, +1507.8716] | 0.056 | 3/3 |
| damp-mlp-0.01 | housing | Influence | lowest | auc | 3 | +755.5007 | [+303.3703, +1304.3121] | 0.123 | 3/3 |
| damp-mlp-0.01 | housing | LissaInfluence | lowest | 5 % | 3 | +808.7258 | [-32.5120, +2427.3406] | 0.423 | 2/3 |
| damp-mlp-0.01 | housing | LissaInfluence | lowest | 10 % | 3 | +844.3344 | [-680.6141, +2830.0506] | 0.502 | 2/3 |
| damp-mlp-0.01 | housing | LissaInfluence | lowest | 20 % | 3 | -1064.6261 | [-2605.3523, -132.6604] | 0.304 | 0/3 |
| damp-mlp-0.01 | housing | LissaInfluence | lowest | auc | 3 | +252.6503 | [-914.6964, +1634.9390] | 0.766 | 2/3 |
| damp-mlp-0.01 | housing | LossHigh | lowest | 5 % | 3 | -854.5566 | [-2476.7996, +84.1066] | 0.404 | 1/3 |
| damp-mlp-0.01 | housing | LossHigh | lowest | 10 % | 3 | +3343.0733 | [+2049.3794, +4228.3931] | 0.037 | 3/3 |
| damp-mlp-0.01 | housing | LossHigh | lowest | 20 % | 3 | +3239.0433 | [+1404.2656, +4165.5563] | 0.072 | 3/3 |
| damp-mlp-0.01 | housing | LossHigh | lowest | auc | 3 | +1849.7741 | [+500.3838, +2579.7301] | 0.111 | 3/3 |
| damp-mlp-0.01 | wine | Influence | lowest | 5 % | 3 | -0.0032 | [-0.0082, +0.0034] | 0.450 | 1/3 |
| damp-mlp-0.01 | wine | Influence | lowest | 10 % | 3 | +0.0001 | [-0.0014, +0.0014] | 0.952 | 2/3 |
| damp-mlp-0.01 | wine | Influence | lowest | 20 % | 3 | +0.0158 | [+0.0069, +0.0258] | 0.103 | 3/3 |
| damp-mlp-0.01 | wine | Influence | lowest | auc | 3 | +0.0032 | [+0.0002, +0.0074] | 0.282 | 3/3 |
| damp-mlp-0.01 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0072 | [-0.0159, +0.0325] | 0.659 | 2/3 |
| damp-mlp-0.01 | wine | LissaInfluence | lowest | 10 % | 3 | -0.0005 | [-0.0362, +0.0267] | 0.979 | 2/3 |
| damp-mlp-0.01 | wine | LissaInfluence | lowest | 20 % | 3 | +0.0049 | [-0.0135, +0.0184] | 0.659 | 2/3 |
| damp-mlp-0.01 | wine | LissaInfluence | lowest | auc | 3 | +0.0028 | [-0.0209, +0.0206] | 0.841 | 2/3 |
| damp-mlp-0.01 | wine | LossHigh | lowest | 5 % | 3 | -0.0201 | [-0.0247, -0.0125] | 0.034 | 0/3 |
| damp-mlp-0.01 | wine | LossHigh | lowest | 10 % | 3 | +0.0063 | [-0.0082, +0.0163] | 0.486 | 2/3 |
| damp-mlp-0.01 | wine | LossHigh | lowest | 20 % | 3 | -0.0029 | [-0.0060, +0.0013] | 0.315 | 1/3 |
| damp-mlp-0.01 | wine | LossHigh | lowest | auc | 3 | -0.0034 | [-0.0072, -0.0014] | 0.216 | 0/3 |
| damp-mlp-0.1 | adult | Influence | lowest | 5 % | 3 | -0.0047 | [-0.0115, +0.0065] | 0.494 | 1/3 |
| damp-mlp-0.1 | adult | Influence | lowest | 10 % | 3 | +0.0014 | [-0.0047, +0.0124] | 0.829 | 1/3 |
| damp-mlp-0.1 | adult | Influence | lowest | 20 % | 3 | -0.0153 | [-0.0225, -0.0068] | 0.079 | 0/3 |
| damp-mlp-0.1 | adult | Influence | lowest | auc | 3 | -0.0045 | [-0.0103, +0.0046] | 0.431 | 1/3 |
| damp-mlp-0.1 | covertype | Influence | lowest | 5 % | 3 | +0.0014 | [-0.0060, +0.0116] | 0.815 | 1/3 |
| damp-mlp-0.1 | covertype | Influence | lowest | 10 % | 3 | -0.0010 | [-0.0098, +0.0088] | 0.870 | 1/3 |
| damp-mlp-0.1 | covertype | Influence | lowest | 20 % | 3 | -0.0121 | [-0.0200, -0.0064] | 0.096 | 0/3 |
| damp-mlp-0.1 | covertype | Influence | lowest | auc | 3 | -0.0031 | [-0.0077, +0.0046] | 0.511 | 1/3 |
| damp-mlp-0.1 | housing | Influence | lowest | 5 % | 3 | +1366.3658 | [-225.9619, +3478.8269] | 0.340 | 2/3 |
| damp-mlp-0.1 | housing | Influence | lowest | 10 % | 3 | +1885.5575 | [-211.4721, +3837.3875] | 0.249 | 2/3 |
| damp-mlp-0.1 | housing | Influence | lowest | 20 % | 3 | +1492.7878 | [-1371.6938, +3071.0708] | 0.407 | 2/3 |
| damp-mlp-0.1 | housing | Influence | lowest | auc | 3 | +1421.8725 | [-478.7159, +3003.4737] | 0.297 | 2/3 |
| damp-mlp-0.1 | wine | Influence | lowest | 5 % | 3 | -0.0021 | [-0.0213, +0.0243] | 0.893 | 1/3 |
| damp-mlp-0.1 | wine | Influence | lowest | 10 % | 3 | +0.0005 | [-0.0217, +0.0217] | 0.971 | 2/3 |
| damp-mlp-0.1 | wine | Influence | lowest | 20 % | 3 | +0.0090 | [-0.0004, +0.0139] | 0.196 | 2/3 |
| damp-mlp-0.1 | wine | Influence | lowest | auc | 3 | +0.0019 | [-0.0136, +0.0177] | 0.850 | 2/3 |
| damp-mlp-1 | adult | Influence | lowest | 5 % | 3 | +0.0089 | [+0.0048, +0.0131] | 0.065 | 3/3 |
| damp-mlp-1 | adult | Influence | lowest | 10 % | 3 | -0.0056 | [-0.0125, +0.0037] | 0.363 | 1/3 |
| damp-mlp-1 | adult | Influence | lowest | 20 % | 3 | -0.0050 | [-0.0058, -0.0037] | 0.016 | 0/3 |
| damp-mlp-1 | adult | Influence | lowest | auc | 3 | -0.0011 | [-0.0034, +0.0012] | 0.488 | 1/3 |
| damp-mlp-1 | adult | LissaInfluence | lowest | 5 % | 3 | +0.0047 | [+0.0010, +0.0078] | 0.140 | 3/3 |
| damp-mlp-1 | adult | LissaInfluence | lowest | 10 % | 3 | -0.0013 | [-0.0068, +0.0032] | 0.704 | 1/3 |
| damp-mlp-1 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0069 | [-0.0102, -0.0018] | 0.116 | 0/3 |
| damp-mlp-1 | adult | LissaInfluence | lowest | auc | 3 | -0.0010 | [-0.0028, +0.0021] | 0.581 | 1/3 |
| damp-mlp-1 | adult | LossHigh | lowest | 5 % | 3 | +0.0036 | [-0.0006, +0.0076] | 0.264 | 2/3 |
| damp-mlp-1 | adult | LossHigh | lowest | 10 % | 3 | -0.0046 | [-0.0075, -0.0009] | 0.139 | 0/3 |
| damp-mlp-1 | adult | LossHigh | lowest | 20 % | 3 | -0.0128 | [-0.0249, -0.0041] | 0.178 | 0/3 |
| damp-mlp-1 | adult | LossHigh | lowest | auc | 3 | -0.0040 | [-0.0047, -0.0033] | 0.009 | 0/3 |
| damp-mlp-1 | covertype | Influence | lowest | 5 % | 3 | +0.0025 | [-0.0076, +0.0116] | 0.701 | 2/3 |
| damp-mlp-1 | covertype | Influence | lowest | 10 % | 3 | -0.0094 | [-0.0112, -0.0078] | 0.011 | 0/3 |
| damp-mlp-1 | covertype | Influence | lowest | 20 % | 3 | -0.0221 | [-0.0288, -0.0172] | 0.024 | 0/3 |
| damp-mlp-1 | covertype | Influence | lowest | auc | 3 | -0.0084 | [-0.0126, -0.0051] | 0.061 | 0/3 |
| damp-mlp-1 | housing | Influence | lowest | 5 % | 3 | +706.5716 | [-1191.9079, +2618.1408] | 0.586 | 2/3 |
| damp-mlp-1 | housing | Influence | lowest | 10 % | 3 | +80.0817 | [-1634.6509, +3386.7027] | 0.966 | 1/3 |
| damp-mlp-1 | housing | Influence | lowest | 20 % | 3 | -2302.0705 | [-4321.0757, +877.3865] | 0.289 | 1/3 |
| damp-mlp-1 | housing | Influence | lowest | auc | 3 | -368.8441 | [-1776.6017, +2143.8953] | 0.797 | 1/3 |
| damp-mlp-1 | housing | LissaInfluence | lowest | 5 % | 3 | +232.0585 | [-1515.3091, +2972.2958] | 0.883 | 1/3 |
| damp-mlp-1 | housing | LissaInfluence | lowest | 10 % | 3 | -381.8816 | [-2005.6929, +2691.4456] | 0.827 | 1/3 |
| damp-mlp-1 | housing | LissaInfluence | lowest | 20 % | 3 | -3632.2904 | [-5743.7790, -48.8913] | 0.181 | 0/3 |
| damp-mlp-1 | housing | LissaInfluence | lowest | auc | 3 | -993.2636 | [-2378.2823, +1740.1432] | 0.543 | 1/3 |
| damp-mlp-1 | housing | LossHigh | lowest | 5 % | 3 | -854.5566 | [-2476.7996, +84.1066] | 0.404 | 1/3 |
| damp-mlp-1 | housing | LossHigh | lowest | 10 % | 3 | +3343.0733 | [+2049.3794, +4228.3931] | 0.037 | 3/3 |
| damp-mlp-1 | housing | LossHigh | lowest | 20 % | 3 | +3239.0433 | [+1404.2656, +4165.5563] | 0.072 | 3/3 |
| damp-mlp-1 | housing | LossHigh | lowest | auc | 3 | +1849.7741 | [+500.3838, +2579.7301] | 0.111 | 3/3 |
| damp-mlp-1 | wine | Influence | lowest | 5 % | 3 | -0.0015 | [-0.0189, +0.0185] | 0.900 | 1/3 |
| damp-mlp-1 | wine | Influence | lowest | 10 % | 3 | +0.0018 | [-0.0256, +0.0256] | 0.917 | 2/3 |
| damp-mlp-1 | wine | Influence | lowest | 20 % | 3 | -0.0006 | [-0.0083, +0.0072] | 0.900 | 1/3 |
| damp-mlp-1 | wine | Influence | lowest | auc | 3 | +0.0001 | [-0.0164, +0.0140] | 0.991 | 2/3 |
| damp-mlp-1 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0039 | [-0.0109, +0.0199] | 0.702 | 2/3 |
| damp-mlp-1 | wine | LissaInfluence | lowest | 10 % | 3 | +0.0052 | [-0.0251, +0.0301] | 0.778 | 2/3 |
| damp-mlp-1 | wine | LissaInfluence | lowest | 20 % | 3 | -0.0002 | [-0.0054, +0.0069] | 0.964 | 1/3 |
| damp-mlp-1 | wine | LissaInfluence | lowest | auc | 3 | +0.0029 | [-0.0135, +0.0158] | 0.769 | 2/3 |
| damp-mlp-1 | wine | LossHigh | lowest | 5 % | 3 | -0.0201 | [-0.0247, -0.0125] | 0.034 | 0/3 |
| damp-mlp-1 | wine | LossHigh | lowest | 10 % | 3 | +0.0063 | [-0.0082, +0.0163] | 0.486 | 2/3 |
| damp-mlp-1 | wine | LossHigh | lowest | 20 % | 3 | -0.0029 | [-0.0060, +0.0013] | 0.315 | 1/3 |
| damp-mlp-1 | wine | LossHigh | lowest | auc | 3 | -0.0034 | [-0.0072, -0.0014] | 0.216 | 0/3 |
| damp-mlp-1e-06 | adult | Influence | lowest | 5 % | 3 | +0.0037 | [-0.0003, +0.0075] | 0.248 | 2/3 |
| damp-mlp-1e-06 | adult | Influence | lowest | 10 % | 3 | +0.0039 | [-0.0046, +0.0100] | 0.468 | 2/3 |
| damp-mlp-1e-06 | adult | Influence | lowest | 20 % | 3 | +0.0116 | [-0.0044, +0.0269] | 0.328 | 2/3 |
| damp-mlp-1e-06 | adult | Influence | lowest | auc | 3 | +0.0053 | [+0.0023, +0.0104] | 0.177 | 3/3 |
| damp-mlp-1e-06 | adult | LissaInfluence | lowest | 5 % | 3 | -0.0030 | [-0.0173, +0.0048] | 0.720 | 2/3 |
| damp-mlp-1e-06 | adult | LissaInfluence | lowest | 10 % | 3 | -0.0044 | [-0.0125, +0.0026] | 0.424 | 1/3 |
| damp-mlp-1e-06 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0155 | [-0.0287, +0.0019] | 0.230 | 1/3 |
| damp-mlp-1e-06 | adult | LissaInfluence | lowest | auc | 3 | -0.0063 | [-0.0162, +0.0027] | 0.371 | 1/3 |
| damp-mlp-1e-06 | adult | LossHigh | lowest | 5 % | 3 | +0.0036 | [-0.0006, +0.0076] | 0.264 | 2/3 |
| damp-mlp-1e-06 | adult | LossHigh | lowest | 10 % | 3 | -0.0046 | [-0.0075, -0.0009] | 0.139 | 0/3 |
| damp-mlp-1e-06 | adult | LossHigh | lowest | 20 % | 3 | -0.0128 | [-0.0249, -0.0041] | 0.178 | 0/3 |
| damp-mlp-1e-06 | adult | LossHigh | lowest | auc | 3 | -0.0040 | [-0.0047, -0.0033] | 0.009 | 0/3 |
| damp-mlp-1e-06 | housing | Influence | lowest | 5 % | 3 | +1368.5569 | [+671.8163, +2206.4939] | 0.093 | 3/3 |
| damp-mlp-1e-06 | housing | Influence | lowest | 10 % | 3 | +1121.1233 | [-324.8015, +2028.6864] | 0.265 | 2/3 |
| damp-mlp-1e-06 | housing | Influence | lowest | 20 % | 3 | +1395.1332 | [+367.3079, +1915.1507] | 0.113 | 3/3 |
| damp-mlp-1e-06 | housing | Influence | lowest | auc | 3 | +1111.3438 | [+137.9805, +1652.7180] | 0.150 | 3/3 |
| damp-mlp-1e-06 | housing | LissaInfluence | lowest | 5 % | 3 | +495.2529 | [-972.9307, +2427.3406] | 0.672 | 2/3 |
| damp-mlp-1e-06 | housing | LissaInfluence | lowest | 10 % | 3 | +758.7728 | [-559.1536, +2451.9052] | 0.483 | 2/3 |
| damp-mlp-1e-06 | housing | LissaInfluence | lowest | 20 % | 3 | -1064.9412 | [-2503.8692, +140.4905] | 0.302 | 1/3 |
| damp-mlp-1e-06 | housing | LissaInfluence | lowest | auc | 3 | +142.1177 | [-1078.8826, +1561.4222] | 0.870 | 1/3 |
| damp-mlp-1e-06 | housing | LossHigh | lowest | 5 % | 3 | -854.5566 | [-2476.7996, +84.1066] | 0.404 | 1/3 |
| damp-mlp-1e-06 | housing | LossHigh | lowest | 10 % | 3 | +3343.0733 | [+2049.3794, +4228.3931] | 0.037 | 3/3 |
| damp-mlp-1e-06 | housing | LossHigh | lowest | 20 % | 3 | +3239.0433 | [+1404.2656, +4165.5563] | 0.072 | 3/3 |
| damp-mlp-1e-06 | housing | LossHigh | lowest | auc | 3 | +1849.7741 | [+500.3838, +2579.7301] | 0.111 | 3/3 |
| damp-mlp-1e-06 | wine | Influence | lowest | 5 % | 3 | +0.0041 | [-0.0087, +0.0142] | 0.603 | 2/3 |
| damp-mlp-1e-06 | wine | Influence | lowest | 10 % | 3 | +0.0059 | [-0.0127, +0.0220] | 0.617 | 2/3 |
| damp-mlp-1e-06 | wine | Influence | lowest | 20 % | 3 | +0.0110 | [+0.0060, +0.0185] | 0.102 | 3/3 |
| damp-mlp-1e-06 | wine | Influence | lowest | auc | 3 | +0.0060 | [-0.0054, +0.0140] | 0.413 | 2/3 |
| damp-mlp-1e-06 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0063 | [-0.0159, +0.0325] | 0.700 | 2/3 |
| damp-mlp-1e-06 | wine | LissaInfluence | lowest | 10 % | 3 | +0.0006 | [-0.0328, +0.0267] | 0.977 | 2/3 |
| damp-mlp-1e-06 | wine | LissaInfluence | lowest | 20 % | 3 | +0.0049 | [-0.0135, +0.0184] | 0.659 | 2/3 |
| damp-mlp-1e-06 | wine | LissaInfluence | lowest | auc | 3 | +0.0030 | [-0.0197, +0.0206] | 0.824 | 2/3 |
| damp-mlp-1e-06 | wine | LossHigh | lowest | 5 % | 3 | -0.0201 | [-0.0247, -0.0125] | 0.034 | 0/3 |
| damp-mlp-1e-06 | wine | LossHigh | lowest | 10 % | 3 | +0.0063 | [-0.0082, +0.0163] | 0.486 | 2/3 |
| damp-mlp-1e-06 | wine | LossHigh | lowest | 20 % | 3 | -0.0029 | [-0.0060, +0.0013] | 0.315 | 1/3 |
| damp-mlp-1e-06 | wine | LossHigh | lowest | auc | 3 | -0.0034 | [-0.0072, -0.0014] | 0.216 | 0/3 |
| distill-catboost-noise10 | adult | CatBoostLFC | lowest | 5 % | 3 | +0.0110 | [+0.0008, +0.0198] | 0.185 | 3/3 |
| distill-catboost-noise10 | adult | CatBoostLFC | lowest | 10 % | 3 | +0.0065 | [+0.0014, +0.0103] | 0.134 | 3/3 |
| distill-catboost-noise10 | adult | CatBoostLFC | lowest | 20 % | 3 | +0.0122 | [+0.0003, +0.0296] | 0.303 | 3/3 |
| distill-catboost-noise10 | adult | CatBoostLFC | lowest | auc | 3 | +0.0082 | [+0.0008, +0.0162] | 0.206 | 3/3 |
| distill-catboost-noise10 | adult | DataOOB | lowest | 5 % | 3 | +0.0054 | [-0.0051, +0.0153] | 0.459 | 2/3 |
| distill-catboost-noise10 | adult | DataOOB | lowest | 10 % | 3 | +0.0070 | [-0.0042, +0.0187] | 0.398 | 2/3 |
| distill-catboost-noise10 | adult | DataOOB | lowest | 20 % | 3 | +0.0021 | [-0.0145, +0.0164] | 0.836 | 2/3 |
| distill-catboost-noise10 | adult | DataOOB | lowest | auc | 3 | +0.0045 | [-0.0065, +0.0149] | 0.542 | 2/3 |
| distill-catboost-noise10 | adult | Influence | lowest | 5 % | 3 | -0.0038 | [-0.0134, +0.0094] | 0.631 | 1/3 |
| distill-catboost-noise10 | adult | Influence | lowest | 10 % | 3 | -0.0026 | [-0.0046, -0.0007] | 0.149 | 0/3 |
| distill-catboost-noise10 | adult | Influence | lowest | 20 % | 3 | +0.0017 | [-0.0049, +0.0129] | 0.786 | 1/3 |
| distill-catboost-noise10 | adult | Influence | lowest | auc | 3 | -0.0015 | [-0.0050, +0.0053] | 0.703 | 1/3 |
| distill-catboost-noise10 | adult | LissaInfluence | lowest | 5 % | 3 | +0.0053 | [+0.0003, +0.0085] | 0.171 | 3/3 |
| distill-catboost-noise10 | adult | LissaInfluence | lowest | 10 % | 3 | -0.0051 | [-0.0099, +0.0035] | 0.359 | 1/3 |
| distill-catboost-noise10 | adult | LissaInfluence | lowest | 20 % | 3 | +0.0032 | [-0.0054, +0.0196] | 0.731 | 1/3 |
| distill-catboost-noise10 | adult | LissaInfluence | lowest | auc | 3 | +0.0002 | [-0.0050, +0.0080] | 0.959 | 1/3 |
| distill-catboost-noise10 | adult | LossHigh | lowest | 5 % | 3 | +0.0048 | [-0.0061, +0.0123] | 0.478 | 2/3 |
| distill-catboost-noise10 | adult | LossHigh | lowest | 10 % | 3 | +0.0024 | [-0.0036, +0.0134] | 0.701 | 1/3 |
| distill-catboost-noise10 | adult | LossHigh | lowest | 20 % | 3 | -0.0046 | [-0.0144, +0.0052] | 0.502 | 1/3 |
| distill-catboost-noise10 | adult | LossHigh | lowest | auc | 3 | +0.0010 | [-0.0065, +0.0094] | 0.852 | 2/3 |
| distill-catboost-noise10 | covertype | DataOOB | lowest | 5 % | 3 | -0.0004 | [-0.0016, +0.0006] | 0.597 | 1/3 |
| distill-catboost-noise10 | covertype | DataOOB | lowest | 10 % | 3 | +0.0049 | [-0.0008, +0.0084] | 0.231 | 2/3 |
| distill-catboost-noise10 | covertype | DataOOB | lowest | 20 % | 3 | +0.0067 | [+0.0026, +0.0096] | 0.086 | 3/3 |
| distill-catboost-noise10 | covertype | DataOOB | lowest | auc | 3 | +0.0034 | [-0.0001, +0.0052] | 0.188 | 2/3 |
| distill-catboost-noise10 | covertype | Influence | lowest | 5 % | 3 | -0.0003 | [-0.0046, +0.0074] | 0.951 | 1/3 |
| distill-catboost-noise10 | covertype | Influence | lowest | 10 % | 3 | +0.0021 | [-0.0090, +0.0092] | 0.741 | 2/3 |
| distill-catboost-noise10 | covertype | Influence | lowest | 20 % | 3 | +0.0013 | [-0.0094, +0.0128] | 0.855 | 2/3 |
| distill-catboost-noise10 | covertype | Influence | lowest | auc | 3 | +0.0011 | [-0.0069, +0.0085] | 0.833 | 2/3 |
| distill-catboost-noise10 | covertype | LissaInfluence | lowest | 5 % | 3 | -0.0006 | [-0.0078, +0.0066] | 0.898 | 1/3 |
| distill-catboost-noise10 | covertype | LissaInfluence | lowest | 10 % | 3 | +0.0034 | [+0.0014, +0.0058] | 0.118 | 3/3 |
| distill-catboost-noise10 | covertype | LissaInfluence | lowest | 20 % | 3 | +0.0009 | [-0.0008, +0.0040] | 0.606 | 1/3 |
| distill-catboost-noise10 | covertype | LissaInfluence | lowest | auc | 3 | +0.0014 | [-0.0015, +0.0036] | 0.465 | 2/3 |
| distill-catboost-noise10 | covertype | LossHigh | lowest | 5 % | 3 | -0.0020 | [-0.0066, +0.0050] | 0.631 | 1/3 |
| distill-catboost-noise10 | covertype | LossHigh | lowest | 10 % | 3 | +0.0003 | [-0.0028, +0.0032] | 0.892 | 2/3 |
| distill-catboost-noise10 | covertype | LossHigh | lowest | 20 % | 3 | -0.0011 | [-0.0046, +0.0042] | 0.716 | 1/3 |
| distill-catboost-noise10 | covertype | LossHigh | lowest | auc | 3 | -0.0007 | [-0.0010, -0.0004] | 0.066 | 0/3 |
| distill-catboost-noise10 | housing | DataOOB | lowest | 5 % | 3 | -705.7830 | [-1082.1158, -121.8948] | 0.140 | 0/3 |
| distill-catboost-noise10 | housing | DataOOB | lowest | 10 % | 3 | +631.2582 | [+313.2068, +999.9195] | 0.087 | 3/3 |
| distill-catboost-noise10 | housing | DataOOB | lowest | 20 % | 3 | +790.5610 | [+462.4824, +1123.6446] | 0.054 | 3/3 |
| distill-catboost-noise10 | housing | DataOOB | lowest | auc | 3 | +257.9163 | [+43.3126, +427.5463] | 0.150 | 3/3 |
| distill-catboost-noise10 | housing | Influence | lowest | 5 % | 3 | -391.9832 | [-643.7685, -110.1903] | 0.127 | 0/3 |
| distill-catboost-noise10 | housing | Influence | lowest | 10 % | 3 | -434.9632 | [-997.4223, +193.4456] | 0.335 | 1/3 |
| distill-catboost-noise10 | housing | Influence | lowest | 20 % | 3 | -167.9500 | [-1161.3508, +414.7432] | 0.769 | 2/3 |
| distill-catboost-noise10 | housing | Influence | lowest | auc | 3 | -303.0945 | [-825.3132, +70.7302] | 0.377 | 1/3 |
| distill-catboost-noise10 | housing | LissaInfluence | lowest | 5 % | 3 | +198.8925 | [+20.6583, +390.7383] | 0.204 | 3/3 |
| distill-catboost-noise10 | housing | LissaInfluence | lowest | 10 % | 3 | +186.4929 | [-575.7097, +866.4477] | 0.699 | 2/3 |
| distill-catboost-noise10 | housing | LissaInfluence | lowest | 20 % | 3 | -2114.3137 | [-2846.3080, -1464.3246] | 0.034 | 0/3 |
| distill-catboost-noise10 | housing | LissaInfluence | lowest | auc | 3 | -408.9205 | [-881.1479, +56.5213] | 0.270 | 1/3 |
| distill-catboost-noise10 | housing | LossHigh | lowest | 5 % | 3 | -419.7930 | [-847.6688, +69.5950] | 0.256 | 1/3 |
| distill-catboost-noise10 | housing | LossHigh | lowest | 10 % | 3 | +27.3921 | [-180.2062, +304.3895] | 0.867 | 1/3 |
| distill-catboost-noise10 | housing | LossHigh | lowest | 20 % | 3 | -2651.8197 | [-2912.5560, -2490.7250] | 0.002 | 0/3 |
| distill-catboost-noise10 | housing | LossHigh | lowest | auc | 3 | -757.6312 | [-917.5391, -628.8615] | 0.012 | 0/3 |
| distill-catboost-noise10 | wine | DataOOB | lowest | 5 % | 3 | +0.0077 | [-0.0059, +0.0233] | 0.463 | 2/3 |
| distill-catboost-noise10 | wine | DataOOB | lowest | 10 % | 3 | +0.0053 | [+0.0027, +0.0095] | 0.130 | 3/3 |
| distill-catboost-noise10 | wine | DataOOB | lowest | 20 % | 3 | +0.0076 | [-0.0072, +0.0218] | 0.460 | 2/3 |
| distill-catboost-noise10 | wine | DataOOB | lowest | auc | 3 | +0.0058 | [+0.0050, +0.0070] | 0.011 | 3/3 |
| distill-catboost-noise10 | wine | Influence | lowest | 5 % | 3 | +0.0136 | [+0.0064, +0.0265] | 0.169 | 3/3 |
| distill-catboost-noise10 | wine | Influence | lowest | 10 % | 3 | +0.0040 | [+0.0024, +0.0051] | 0.040 | 3/3 |
| distill-catboost-noise10 | wine | Influence | lowest | 20 % | 3 | -0.0052 | [-0.0326, +0.0147] | 0.750 | 2/3 |
| distill-catboost-noise10 | wine | Influence | lowest | auc | 3 | +0.0036 | [-0.0006, +0.0070] | 0.249 | 2/3 |
| distill-catboost-noise10 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0152 | [+0.0074, +0.0290] | 0.159 | 3/3 |
| distill-catboost-noise10 | wine | LissaInfluence | lowest | 10 % | 3 | +0.0146 | [+0.0131, +0.0174] | 0.009 | 3/3 |
| distill-catboost-noise10 | wine | LissaInfluence | lowest | 20 % | 3 | +0.0194 | [+0.0122, +0.0250] | 0.036 | 3/3 |
| distill-catboost-noise10 | wine | LissaInfluence | lowest | auc | 3 | +0.0141 | [+0.0124, +0.0153] | 0.004 | 3/3 |
| distill-catboost-noise10 | wine | LossHigh | lowest | 5 % | 3 | +0.0105 | [+0.0034, +0.0239] | 0.258 | 3/3 |
| distill-catboost-noise10 | wine | LossHigh | lowest | 10 % | 3 | +0.0055 | [+0.0032, +0.0087] | 0.083 | 3/3 |
| distill-catboost-noise10 | wine | LossHigh | lowest | 20 % | 3 | +0.0065 | [-0.0077, +0.0230] | 0.540 | 2/3 |
| distill-catboost-noise10 | wine | LossHigh | lowest | auc | 3 | +0.0063 | [+0.0038, +0.0099] | 0.075 | 3/3 |
| distill-lightgbm-noise10 | adult | BoostIn | lowest | 5 % | 3 | -0.0052 | [-0.0127, +0.0007] | 0.318 | 1/3 |
| distill-lightgbm-noise10 | adult | BoostIn | lowest | 10 % | 3 | +0.0015 | [-0.0074, +0.0109] | 0.808 | 2/3 |
| distill-lightgbm-noise10 | adult | BoostIn | lowest | 20 % | 3 | +0.0129 | [-0.0101, +0.0267] | 0.381 | 2/3 |
| distill-lightgbm-noise10 | adult | BoostIn | lowest | auc | 3 | +0.0025 | [-0.0020, +0.0076] | 0.468 | 2/3 |
| distill-lightgbm-noise10 | adult | DataOOB | lowest | 5 % | 3 | +0.0012 | [-0.0000, +0.0020] | 0.193 | 2/3 |
| distill-lightgbm-noise10 | adult | DataOOB | lowest | 10 % | 3 | +0.0001 | [-0.0052, +0.0027] | 0.984 | 2/3 |
| distill-lightgbm-noise10 | adult | DataOOB | lowest | 20 % | 3 | +0.0096 | [+0.0063, +0.0133] | 0.041 | 3/3 |
| distill-lightgbm-noise10 | adult | DataOOB | lowest | auc | 3 | +0.0027 | [+0.0018, +0.0038] | 0.043 | 3/3 |
| distill-lightgbm-noise10 | adult | Influence | lowest | 5 % | 3 | -0.0091 | [-0.0205, +0.0027] | 0.306 | 1/3 |
| distill-lightgbm-noise10 | adult | Influence | lowest | 10 % | 3 | -0.0027 | [-0.0166, +0.0110] | 0.766 | 1/3 |
| distill-lightgbm-noise10 | adult | Influence | lowest | 20 % | 3 | +0.0044 | [-0.0014, +0.0088] | 0.280 | 2/3 |
| distill-lightgbm-noise10 | adult | Influence | lowest | auc | 3 | -0.0022 | [-0.0117, +0.0032] | 0.691 | 2/3 |
| distill-lightgbm-noise10 | adult | LissaInfluence | lowest | 5 % | 3 | -0.0033 | [-0.0118, +0.0035] | 0.543 | 1/3 |
| distill-lightgbm-noise10 | adult | LissaInfluence | lowest | 10 % | 3 | +0.0012 | [-0.0068, +0.0150] | 0.879 | 1/3 |
| distill-lightgbm-noise10 | adult | LissaInfluence | lowest | 20 % | 3 | +0.0010 | [-0.0025, +0.0075] | 0.776 | 1/3 |
| distill-lightgbm-noise10 | adult | LissaInfluence | lowest | auc | 3 | -0.0001 | [-0.0060, +0.0059] | 0.978 | 1/3 |
| distill-lightgbm-noise10 | adult | LossHigh | lowest | 5 % | 3 | +0.0034 | [+0.0007, +0.0072] | 0.229 | 3/3 |
| distill-lightgbm-noise10 | adult | LossHigh | lowest | 10 % | 3 | +0.0061 | [-0.0038, +0.0160] | 0.399 | 2/3 |
| distill-lightgbm-noise10 | adult | LossHigh | lowest | 20 % | 3 | -0.0051 | [-0.0115, -0.0015] | 0.252 | 0/3 |
| distill-lightgbm-noise10 | adult | LossHigh | lowest | auc | 3 | +0.0019 | [-0.0037, +0.0058] | 0.585 | 2/3 |
| distill-lightgbm-noise10 | covertype | BoostIn | lowest | 5 % | 3 | +0.0008 | [-0.0014, +0.0024] | 0.555 | 2/3 |
| distill-lightgbm-noise10 | covertype | BoostIn | lowest | 10 % | 3 | -0.0038 | [-0.0084, +0.0012] | 0.305 | 1/3 |
| distill-lightgbm-noise10 | covertype | BoostIn | lowest | 20 % | 3 | -0.0007 | [-0.0092, +0.0052] | 0.893 | 2/3 |
| distill-lightgbm-noise10 | covertype | BoostIn | lowest | auc | 3 | -0.0014 | [-0.0042, +0.0013] | 0.475 | 1/3 |
| distill-lightgbm-noise10 | covertype | DataOOB | lowest | 5 % | 3 | -0.0005 | [-0.0068, +0.0050] | 0.891 | 2/3 |
| distill-lightgbm-noise10 | covertype | DataOOB | lowest | 10 % | 3 | -0.0004 | [-0.0070, +0.0094] | 0.943 | 1/3 |
| distill-lightgbm-noise10 | covertype | DataOOB | lowest | 20 % | 3 | +0.0023 | [-0.0054, +0.0090] | 0.634 | 2/3 |
| distill-lightgbm-noise10 | covertype | DataOOB | lowest | auc | 3 | +0.0003 | [-0.0039, +0.0027] | 0.900 | 2/3 |
| distill-lightgbm-noise10 | covertype | Influence | lowest | 5 % | 3 | -0.0024 | [-0.0128, +0.0038] | 0.691 | 2/3 |
| distill-lightgbm-noise10 | covertype | Influence | lowest | 10 % | 3 | -0.0049 | [-0.0084, -0.0022] | 0.118 | 0/3 |
| distill-lightgbm-noise10 | covertype | Influence | lowest | 20 % | 3 | -0.0033 | [-0.0092, +0.0000] | 0.375 | 0/3 |
| distill-lightgbm-noise10 | covertype | Influence | lowest | auc | 3 | -0.0033 | [-0.0063, -0.0006] | 0.191 | 0/3 |
| distill-lightgbm-noise10 | covertype | LissaInfluence | lowest | 5 % | 3 | -0.0003 | [-0.0034, +0.0038] | 0.891 | 1/3 |
| distill-lightgbm-noise10 | covertype | LissaInfluence | lowest | 10 % | 3 | -0.0043 | [-0.0130, +0.0026] | 0.444 | 1/3 |
| distill-lightgbm-noise10 | covertype | LissaInfluence | lowest | 20 % | 3 | -0.0100 | [-0.0196, -0.0032] | 0.180 | 0/3 |
| distill-lightgbm-noise10 | covertype | LissaInfluence | lowest | auc | 3 | -0.0042 | [-0.0065, -0.0012] | 0.117 | 0/3 |
| distill-lightgbm-noise10 | covertype | LossHigh | lowest | 5 % | 3 | -0.0002 | [-0.0036, +0.0036] | 0.932 | 1/3 |
| distill-lightgbm-noise10 | covertype | LossHigh | lowest | 10 % | 3 | -0.0022 | [-0.0066, +0.0044] | 0.580 | 1/3 |
| distill-lightgbm-noise10 | covertype | LossHigh | lowest | 20 % | 3 | +0.0043 | [+0.0016, +0.0072] | 0.119 | 3/3 |
| distill-lightgbm-noise10 | covertype | LossHigh | lowest | auc | 3 | +0.0002 | [-0.0016, +0.0025] | 0.888 | 1/3 |
| distill-lightgbm-noise10 | housing | BoostIn | lowest | 5 % | 3 | +943.3804 | [-272.1836, +1638.8781] | 0.262 | 2/3 |
| distill-lightgbm-noise10 | housing | BoostIn | lowest | 10 % | 3 | +1988.6946 | [+1300.4803, +3066.7183] | 0.068 | 3/3 |
| distill-lightgbm-noise10 | housing | BoostIn | lowest | 20 % | 3 | +23.5340 | [-3056.4259, +2711.0429] | 0.990 | 2/3 |
| distill-lightgbm-noise10 | housing | BoostIn | lowest | auc | 3 | +987.4891 | [+795.6324, +1097.3949] | 0.009 | 3/3 |
| distill-lightgbm-noise10 | housing | DataOOB | lowest | 5 % | 3 | +1433.5032 | [+979.1229, +1740.6574] | 0.025 | 3/3 |
| distill-lightgbm-noise10 | housing | DataOOB | lowest | 10 % | 3 | +5553.8897 | [+4428.8704, +7242.0858] | 0.023 | 3/3 |
| distill-lightgbm-noise10 | housing | DataOOB | lowest | 20 % | 3 | +5207.4013 | [+2431.6878, +6711.0285] | 0.064 | 3/3 |
| distill-lightgbm-noise10 | housing | DataOOB | lowest | auc | 3 | +3742.9348 | [+2663.9307, +4770.8185] | 0.025 | 3/3 |
| distill-lightgbm-noise10 | housing | Influence | lowest | 5 % | 3 | +71.0264 | [-1565.6686, +1085.5802] | 0.939 | 2/3 |
| distill-lightgbm-noise10 | housing | Influence | lowest | 10 % | 3 | +2259.5183 | [+721.2313, +3331.0200] | 0.103 | 3/3 |
| distill-lightgbm-noise10 | housing | Influence | lowest | 20 % | 3 | +2643.9877 | [+1810.4311, +3742.0053] | 0.044 | 3/3 |
| distill-lightgbm-noise10 | housing | Influence | lowest | auc | 3 | +1526.0729 | [+896.3614, +2115.4092] | 0.049 | 3/3 |
| distill-lightgbm-noise10 | housing | LissaInfluence | lowest | 5 % | 3 | +521.0282 | [-238.5639, +969.9699] | 0.306 | 2/3 |
| distill-lightgbm-noise10 | housing | LissaInfluence | lowest | 10 % | 3 | +852.5488 | [+298.4968, +1746.3914] | 0.199 | 3/3 |
| distill-lightgbm-noise10 | housing | LissaInfluence | lowest | 20 % | 3 | -465.6205 | [-4123.5744, +2264.1073] | 0.829 | 2/3 |
| distill-lightgbm-noise10 | housing | LissaInfluence | lowest | auc | 3 | +333.5577 | [-711.0377, +1013.0406] | 0.594 | 2/3 |
| distill-lightgbm-noise10 | housing | LossHigh | lowest | 5 % | 3 | +58.7851 | [-194.0009, +409.4536] | 0.776 | 1/3 |
| distill-lightgbm-noise10 | housing | LossHigh | lowest | 10 % | 3 | +4914.3750 | [+4350.7689, +5957.8855] | 0.011 | 3/3 |
| distill-lightgbm-noise10 | housing | LossHigh | lowest | 20 % | 3 | +4176.7226 | [+1514.8539, +6190.0496] | 0.095 | 3/3 |
| distill-lightgbm-noise10 | housing | LossHigh | lowest | auc | 3 | +2901.7675 | [+1961.7516, +3542.8866] | 0.026 | 3/3 |
| distill-lightgbm-noise10 | wine | BoostIn | lowest | 5 % | 3 | +0.0108 | [-0.0162, +0.0342] | 0.536 | 2/3 |
| distill-lightgbm-noise10 | wine | BoostIn | lowest | 10 % | 3 | -0.0087 | [-0.0188, +0.0083] | 0.417 | 1/3 |
| distill-lightgbm-noise10 | wine | BoostIn | lowest | 20 % | 3 | +0.0046 | [-0.0235, +0.0206] | 0.775 | 2/3 |
| distill-lightgbm-noise10 | wine | BoostIn | lowest | auc | 3 | +0.0006 | [-0.0057, +0.0066] | 0.879 | 2/3 |
| distill-lightgbm-noise10 | wine | DataOOB | lowest | 5 % | 3 | +0.0091 | [-0.0061, +0.0192] | 0.361 | 2/3 |
| distill-lightgbm-noise10 | wine | DataOOB | lowest | 10 % | 3 | -0.0044 | [-0.0228, +0.0314] | 0.827 | 1/3 |
| distill-lightgbm-noise10 | wine | DataOOB | lowest | 20 % | 3 | -0.0055 | [-0.0137, +0.0057] | 0.443 | 1/3 |
| distill-lightgbm-noise10 | wine | DataOOB | lowest | auc | 3 | -0.0008 | [-0.0118, +0.0118] | 0.921 | 1/3 |
| distill-lightgbm-noise10 | wine | Influence | lowest | 5 % | 3 | +0.0165 | [-0.0114, +0.0450] | 0.417 | 2/3 |
| distill-lightgbm-noise10 | wine | Influence | lowest | 10 % | 3 | -0.0158 | [-0.0381, +0.0193] | 0.468 | 1/3 |
| distill-lightgbm-noise10 | wine | Influence | lowest | 20 % | 3 | +0.0014 | [-0.0197, +0.0148] | 0.905 | 2/3 |
| distill-lightgbm-noise10 | wine | Influence | lowest | auc | 3 | -0.0014 | [-0.0148, +0.0222] | 0.915 | 1/3 |
| distill-lightgbm-noise10 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0279 | [+0.0276, +0.0281] | 0.000 | 3/3 |
| distill-lightgbm-noise10 | wine | LissaInfluence | lowest | 10 % | 3 | -0.0069 | [-0.0123, +0.0009] | 0.224 | 1/3 |
| distill-lightgbm-noise10 | wine | LissaInfluence | lowest | 20 % | 3 | +0.0054 | [-0.0243, +0.0233] | 0.753 | 2/3 |
| distill-lightgbm-noise10 | wine | LissaInfluence | lowest | auc | 3 | +0.0057 | [+0.0011, +0.0093] | 0.141 | 3/3 |
| distill-lightgbm-noise10 | wine | LossHigh | lowest | 5 % | 3 | -0.0014 | [-0.0174, +0.0095] | 0.879 | 2/3 |
| distill-lightgbm-noise10 | wine | LossHigh | lowest | 10 % | 3 | -0.0030 | [-0.0247, +0.0303] | 0.876 | 1/3 |
| distill-lightgbm-noise10 | wine | LossHigh | lowest | 20 % | 3 | -0.0096 | [-0.0220, +0.0004] | 0.282 | 1/3 |
| distill-lightgbm-noise10 | wine | LossHigh | lowest | auc | 3 | -0.0039 | [-0.0124, +0.0105] | 0.646 | 1/3 |
| models-catboost-clean | adult | CatBoostLFC | lowest | 5 % | 3 | +0.0023 | [-0.0056, +0.0077] | 0.629 | 2/3 |
| models-catboost-clean | adult | CatBoostLFC | lowest | 10 % | 3 | -0.0002 | [-0.0195, +0.0151] | 0.987 | 2/3 |
| models-catboost-clean | adult | CatBoostLFC | lowest | 20 % | 3 | -0.0065 | [-0.0180, +0.0030] | 0.404 | 1/3 |
| models-catboost-clean | adult | CatBoostLFC | lowest | 30 % | 3 | +0.0018 | [-0.0086, +0.0091] | 0.770 | 2/3 |
| models-catboost-clean | adult | CatBoostLFC | lowest | auc | 3 | -0.0015 | [-0.0132, +0.0069] | 0.823 | 2/3 |
| models-catboost-clean | adult | CatBoostLFC | highest | 5 % | 3 | -0.0047 | [-0.0085, -0.0006] | 0.173 | 0/3 |
| models-catboost-clean | adult | CatBoostLFC | highest | 10 % | 3 | -0.0114 | [-0.0168, -0.0045] | 0.088 | 0/3 |
| models-catboost-clean | adult | CatBoostLFC | highest | 20 % | 3 | -0.0222 | [-0.0418, -0.0096] | 0.155 | 0/3 |
| models-catboost-clean | adult | CatBoostLFC | highest | 30 % | 3 | -0.0236 | [-0.0388, -0.0153] | 0.090 | 0/3 |
| models-catboost-clean | adult | CatBoostLFC | highest | auc | 3 | -0.0150 | [-0.0254, -0.0070] | 0.112 | 0/3 |
| models-catboost-clean | adult | DataOOB | lowest | 5 % | 3 | +0.0034 | [+0.0022, +0.0045] | 0.037 | 3/3 |
| models-catboost-clean | adult | DataOOB | lowest | 10 % | 3 | -0.0029 | [-0.0100, +0.0062] | 0.610 | 1/3 |
| models-catboost-clean | adult | DataOOB | lowest | 20 % | 3 | -0.0117 | [-0.0248, +0.0015] | 0.264 | 1/3 |
| models-catboost-clean | adult | DataOOB | lowest | 30 % | 3 | -0.0067 | [-0.0180, +0.0088] | 0.489 | 1/3 |
| models-catboost-clean | adult | DataOOB | lowest | auc | 3 | -0.0052 | [-0.0134, +0.0041] | 0.416 | 1/3 |
| models-catboost-clean | adult | DataOOB | highest | 5 % | 3 | +0.0036 | [-0.0048, +0.0091] | 0.486 | 2/3 |
| models-catboost-clean | adult | DataOOB | highest | 10 % | 3 | -0.0058 | [-0.0104, -0.0020] | 0.145 | 0/3 |
| models-catboost-clean | adult | DataOOB | highest | 20 % | 3 | -0.0115 | [-0.0211, -0.0008] | 0.191 | 0/3 |
| models-catboost-clean | adult | DataOOB | highest | 30 % | 3 | -0.0122 | [-0.0164, -0.0066] | 0.052 | 0/3 |
| models-catboost-clean | adult | DataOOB | highest | auc | 3 | -0.0067 | [-0.0103, -0.0008] | 0.154 | 0/3 |
| models-catboost-clean | adult | KNNShapley | lowest | 5 % | 3 | -0.0001 | [-0.0080, +0.0113] | 0.983 | 1/3 |
| models-catboost-clean | adult | KNNShapley | lowest | 10 % | 3 | -0.0056 | [-0.0184, +0.0088] | 0.550 | 1/3 |
| models-catboost-clean | adult | KNNShapley | lowest | 20 % | 3 | -0.0124 | [-0.0173, -0.0071] | 0.053 | 0/3 |
| models-catboost-clean | adult | KNNShapley | lowest | 30 % | 3 | -0.0218 | [-0.0302, -0.0165] | 0.036 | 0/3 |
| models-catboost-clean | adult | KNNShapley | lowest | auc | 3 | -0.0092 | [-0.0144, -0.0014] | 0.148 | 0/3 |
| models-catboost-clean | adult | KNNShapley | highest | 5 % | 3 | -0.0030 | [-0.0060, +0.0004] | 0.242 | 1/3 |
| models-catboost-clean | adult | KNNShapley | highest | 10 % | 3 | -0.0109 | [-0.0224, -0.0050] | 0.196 | 0/3 |
| models-catboost-clean | adult | KNNShapley | highest | 20 % | 3 | -0.0364 | [-0.0498, -0.0152] | 0.077 | 0/3 |
| models-catboost-clean | adult | KNNShapley | highest | 30 % | 3 | -0.0474 | [-0.0734, -0.0288] | 0.072 | 0/3 |
| models-catboost-clean | adult | KNNShapley | highest | auc | 3 | -0.0233 | [-0.0301, -0.0121] | 0.054 | 0/3 |
| models-catboost-clean | adult | LOO | lowest | 5 % | 3 | +0.0004 | [-0.0095, +0.0055] | 0.944 | 2/3 |
| models-catboost-clean | adult | LOO | lowest | 10 % | 3 | +0.0013 | [-0.0023, +0.0062] | 0.649 | 2/3 |
| models-catboost-clean | adult | LOO | lowest | 20 % | 3 | +0.0017 | [-0.0105, +0.0082] | 0.803 | 2/3 |
| models-catboost-clean | adult | LOO | lowest | 30 % | 3 | +0.0101 | [+0.0099, +0.0104] | 0.000 | 3/3 |
| models-catboost-clean | adult | LOO | lowest | auc | 3 | +0.0027 | [-0.0015, +0.0066] | 0.378 | 2/3 |
| models-catboost-clean | adult | LOO | highest | 5 % | 3 | +0.0049 | [+0.0031, +0.0076] | 0.072 | 3/3 |
| models-catboost-clean | adult | LOO | highest | 10 % | 3 | +0.0032 | [-0.0024, +0.0117] | 0.538 | 2/3 |
| models-catboost-clean | adult | LOO | highest | 20 % | 3 | -0.0058 | [-0.0150, +0.0025] | 0.371 | 1/3 |
| models-catboost-clean | adult | LOO | highest | 30 % | 3 | -0.0060 | [-0.0098, -0.0011] | 0.145 | 0/3 |
| models-catboost-clean | adult | LOO | highest | auc | 3 | -0.0013 | [-0.0067, +0.0032] | 0.691 | 1/3 |
| models-catboost-clean | adult | LossHigh | lowest | 5 % | 3 | +0.0025 | [-0.0015, +0.0045] | 0.338 | 2/3 |
| models-catboost-clean | adult | LossHigh | lowest | 10 % | 3 | -0.0023 | [-0.0103, +0.0048] | 0.651 | 1/3 |
| models-catboost-clean | adult | LossHigh | lowest | 20 % | 3 | -0.0094 | [-0.0146, -0.0036] | 0.099 | 0/3 |
| models-catboost-clean | adult | LossHigh | lowest | 30 % | 3 | -0.0115 | [-0.0133, -0.0086] | 0.016 | 0/3 |
| models-catboost-clean | adult | LossHigh | lowest | auc | 3 | -0.0052 | [-0.0098, -0.0007] | 0.186 | 0/3 |
| models-catboost-clean | adult | LossHigh | highest | 5 % | 3 | +0.0029 | [-0.0008, +0.0069] | 0.327 | 2/3 |
| models-catboost-clean | adult | LossHigh | highest | 10 % | 3 | +0.0045 | [+0.0013, +0.0067] | 0.111 | 3/3 |
| models-catboost-clean | adult | LossHigh | highest | 20 % | 3 | -0.0019 | [-0.0074, +0.0069] | 0.713 | 1/3 |
| models-catboost-clean | adult | LossHigh | highest | 30 % | 3 | -0.0068 | [-0.0124, +0.0007] | 0.224 | 1/3 |
| models-catboost-clean | adult | LossHigh | highest | auc | 3 | -0.0001 | [-0.0033, +0.0036] | 0.949 | 1/3 |
| models-catboost-clean | covertype | DataOOB | lowest | 5 % | 3 | -0.0003 | [-0.0036, +0.0018] | 0.859 | 2/3 |
| models-catboost-clean | covertype | DataOOB | lowest | 10 % | 3 | -0.0032 | [-0.0096, +0.0018] | 0.442 | 1/3 |
| models-catboost-clean | covertype | DataOOB | lowest | 20 % | 3 | -0.0037 | [-0.0110, +0.0042] | 0.486 | 1/3 |
| models-catboost-clean | covertype | DataOOB | lowest | 30 % | 3 | +0.0041 | [-0.0054, +0.0168] | 0.595 | 2/3 |
| models-catboost-clean | covertype | DataOOB | lowest | auc | 3 | -0.0014 | [-0.0045, +0.0032] | 0.605 | 1/3 |
| models-catboost-clean | covertype | DataOOB | highest | 5 % | 3 | +0.0008 | [-0.0016, +0.0056] | 0.771 | 1/3 |
| models-catboost-clean | covertype | DataOOB | highest | 10 % | 3 | -0.0025 | [-0.0060, -0.0008] | 0.281 | 0/3 |
| models-catboost-clean | covertype | DataOOB | highest | 20 % | 3 | -0.0021 | [-0.0044, +0.0022] | 0.429 | 1/3 |
| models-catboost-clean | covertype | DataOOB | highest | 30 % | 3 | -0.0071 | [-0.0166, +0.0018] | 0.316 | 1/3 |
| models-catboost-clean | covertype | DataOOB | highest | auc | 3 | -0.0024 | [-0.0046, +0.0004] | 0.247 | 1/3 |
| models-catboost-clean | covertype | KNNShapley | lowest | 5 % | 3 | +0.0048 | [-0.0008, +0.0084] | 0.233 | 2/3 |
| models-catboost-clean | covertype | KNNShapley | lowest | 10 % | 3 | -0.0023 | [-0.0076, +0.0052] | 0.607 | 1/3 |
| models-catboost-clean | covertype | KNNShapley | lowest | 20 % | 3 | -0.0022 | [-0.0028, -0.0014] | 0.034 | 0/3 |
| models-catboost-clean | covertype | KNNShapley | lowest | 30 % | 3 | -0.0060 | [-0.0132, +0.0018] | 0.301 | 1/3 |
| models-catboost-clean | covertype | KNNShapley | lowest | auc | 3 | -0.0015 | [-0.0020, -0.0010] | 0.033 | 0/3 |
| models-catboost-clean | covertype | KNNShapley | highest | 5 % | 3 | -0.0033 | [-0.0096, +0.0042] | 0.502 | 1/3 |
| models-catboost-clean | covertype | KNNShapley | highest | 10 % | 3 | -0.0161 | [-0.0210, -0.0124] | 0.024 | 0/3 |
| models-catboost-clean | covertype | KNNShapley | highest | 20 % | 3 | -0.0281 | [-0.0384, -0.0122] | 0.073 | 0/3 |
| models-catboost-clean | covertype | KNNShapley | highest | 30 % | 3 | -0.0534 | [-0.0814, -0.0300] | 0.071 | 0/3 |
| models-catboost-clean | covertype | KNNShapley | highest | auc | 3 | -0.0228 | [-0.0332, -0.0115] | 0.068 | 0/3 |
| models-catboost-clean | covertype | LOO | lowest | 5 % | 3 | -0.0057 | [-0.0070, -0.0044] | 0.017 | 0/3 |
| models-catboost-clean | covertype | LOO | lowest | 10 % | 3 | -0.0022 | [-0.0046, +0.0022] | 0.423 | 1/3 |
| models-catboost-clean | covertype | LOO | lowest | 20 % | 3 | +0.0012 | [-0.0066, +0.0072] | 0.797 | 2/3 |
| models-catboost-clean | covertype | LOO | lowest | 30 % | 3 | +0.0074 | [-0.0070, +0.0156] | 0.413 | 2/3 |
| models-catboost-clean | covertype | LOO | lowest | auc | 3 | +0.0001 | [-0.0053, +0.0030] | 0.964 | 2/3 |
| models-catboost-clean | covertype | LOO | highest | 5 % | 3 | -0.0020 | [-0.0040, +0.0018] | 0.403 | 1/3 |
| models-catboost-clean | covertype | LOO | highest | 10 % | 3 | -0.0051 | [-0.0094, +0.0032] | 0.343 | 1/3 |
| models-catboost-clean | covertype | LOO | highest | 20 % | 3 | -0.0014 | [-0.0074, +0.0024] | 0.690 | 2/3 |
| models-catboost-clean | covertype | LOO | highest | 30 % | 3 | +0.0095 | [+0.0022, +0.0190] | 0.198 | 3/3 |
| models-catboost-clean | covertype | LOO | highest | auc | 3 | -0.0005 | [-0.0041, +0.0016] | 0.808 | 2/3 |
| models-catboost-clean | covertype | LossHigh | lowest | 5 % | 3 | +0.0017 | [-0.0008, +0.0048] | 0.419 | 2/3 |
| models-catboost-clean | covertype | LossHigh | lowest | 10 % | 3 | -0.0039 | [-0.0058, -0.0010] | 0.118 | 0/3 |
| models-catboost-clean | covertype | LossHigh | lowest | 20 % | 3 | +0.0019 | [-0.0002, +0.0030] | 0.213 | 2/3 |
| models-catboost-clean | covertype | LossHigh | lowest | 30 % | 3 | +0.0019 | [+0.0000, +0.0030] | 0.186 | 2/3 |
| models-catboost-clean | covertype | LossHigh | lowest | auc | 3 | +0.0002 | [-0.0008, +0.0015] | 0.753 | 2/3 |
| models-catboost-clean | covertype | LossHigh | highest | 5 % | 3 | +0.0002 | [-0.0022, +0.0016] | 0.883 | 2/3 |
| models-catboost-clean | covertype | LossHigh | highest | 10 % | 3 | +0.0010 | [-0.0004, +0.0020] | 0.300 | 2/3 |
| models-catboost-clean | covertype | LossHigh | highest | 20 % | 3 | +0.0031 | [-0.0006, +0.0088] | 0.402 | 2/3 |
| models-catboost-clean | covertype | LossHigh | highest | 30 % | 3 | +0.0053 | [-0.0024, +0.0126] | 0.348 | 2/3 |
| models-catboost-clean | covertype | LossHigh | highest | auc | 3 | +0.0022 | [+0.0002, +0.0044] | 0.218 | 3/3 |
| models-catboost-clean | housing | CatBoostLFC | lowest | 5 % | 3 | -343.4175 | [-944.0169, +120.4163] | 0.389 | 1/3 |
| models-catboost-clean | housing | CatBoostLFC | lowest | 10 % | 3 | -774.0691 | [-1460.6300, +231.8779] | 0.271 | 1/3 |
| models-catboost-clean | housing | CatBoostLFC | lowest | 20 % | 3 | -1551.7571 | [-2743.3793, -364.9141] | 0.152 | 0/3 |
| models-catboost-clean | housing | CatBoostLFC | lowest | 30 % | 3 | -2210.7893 | [-3740.1456, -296.8669] | 0.161 | 0/3 |
| models-catboost-clean | housing | CatBoostLFC | lowest | auc | 3 | -1136.4708 | [-2060.3110, -93.0770] | 0.185 | 0/3 |
| models-catboost-clean | housing | CatBoostLFC | highest | 5 % | 3 | -553.6989 | [-1060.5163, +181.5365] | 0.279 | 1/3 |
| models-catboost-clean | housing | CatBoostLFC | highest | 10 % | 3 | -508.9373 | [-1645.2460, +963.3904] | 0.577 | 1/3 |
| models-catboost-clean | housing | CatBoostLFC | highest | 20 % | 3 | -2152.3906 | [-3498.0162, -129.0958] | 0.172 | 0/3 |
| models-catboost-clean | housing | CatBoostLFC | highest | 30 % | 3 | -2799.9758 | [-4312.1371, -619.3597] | 0.129 | 0/3 |
| models-catboost-clean | housing | CatBoostLFC | highest | auc | 3 | -1403.6436 | [-2226.2868, +124.8451] | 0.208 | 1/3 |
| models-catboost-clean | housing | DataOOB | lowest | 5 % | 3 | -487.0995 | [-954.0763, +36.5348] | 0.232 | 1/3 |
| models-catboost-clean | housing | DataOOB | lowest | 10 % | 3 | -734.4651 | [-968.3781, -573.9486] | 0.026 | 0/3 |
| models-catboost-clean | housing | DataOOB | lowest | 20 % | 3 | -1168.5224 | [-1262.7913, -1038.7096] | 0.003 | 0/3 |
| models-catboost-clean | housing | DataOOB | lowest | 30 % | 3 | -1245.6948 | [-1669.2585, -1031.5927] | 0.028 | 0/3 |
| models-catboost-clean | housing | DataOOB | lowest | auc | 3 | -861.9228 | [-974.3948, -761.8443] | 0.005 | 0/3 |
| models-catboost-clean | housing | DataOOB | highest | 5 % | 3 | -884.1301 | [-1291.7683, -253.2106] | 0.110 | 0/3 |
| models-catboost-clean | housing | DataOOB | highest | 10 % | 3 | -1166.5442 | [-1874.9328, -378.5130] | 0.115 | 0/3 |
| models-catboost-clean | housing | DataOOB | highest | 20 % | 3 | -2402.7955 | [-3226.6631, -1504.7225] | 0.040 | 0/3 |
| models-catboost-clean | housing | DataOOB | highest | 30 % | 3 | -4796.9567 | [-6944.4644, -2804.7903] | 0.057 | 0/3 |
| models-catboost-clean | housing | DataOOB | highest | auc | 3 | -2039.4157 | [-2916.9930, -1105.8692] | 0.060 | 0/3 |
| models-catboost-clean | housing | LOO | lowest | 5 % | 3 | -94.5326 | [-292.5668, +22.6774] | 0.443 | 1/3 |
| models-catboost-clean | housing | LOO | lowest | 10 % | 3 | -3.6400 | [-289.4319, +147.0023] | 0.982 | 2/3 |
| models-catboost-clean | housing | LOO | lowest | 20 % | 3 | +104.4346 | [-15.7622, +215.4737] | 0.259 | 2/3 |
| models-catboost-clean | housing | LOO | lowest | 30 % | 3 | +496.3162 | [-149.7080, +1260.0177] | 0.351 | 2/3 |
| models-catboost-clean | housing | LOO | lowest | auc | 3 | +100.8655 | [-151.3245, +278.4597] | 0.518 | 2/3 |
| models-catboost-clean | housing | LOO | highest | 5 % | 3 | -276.3875 | [-374.4501, -137.7690] | 0.061 | 0/3 |
| models-catboost-clean | housing | LOO | highest | 10 % | 3 | -97.4525 | [-785.2435, +315.2737] | 0.805 | 2/3 |
| models-catboost-clean | housing | LOO | highest | 20 % | 3 | -132.2030 | [-421.8105, +126.3813] | 0.493 | 1/3 |
| models-catboost-clean | housing | LOO | highest | 30 % | 3 | -261.9707 | [-1438.2926, +447.2844] | 0.702 | 2/3 |
| models-catboost-clean | housing | LOO | highest | auc | 3 | -158.1572 | [-532.1613, +172.5314] | 0.520 | 1/3 |
| models-catboost-clean | housing | LossHigh | lowest | 5 % | 3 | -1208.6537 | [-1706.9130, -810.8191] | 0.044 | 0/3 |
| models-catboost-clean | housing | LossHigh | lowest | 10 % | 3 | -1884.9066 | [-2029.8661, -1762.4276] | 0.002 | 0/3 |
| models-catboost-clean | housing | LossHigh | lowest | 20 % | 3 | -3405.7846 | [-3439.3232, -3339.2274] | 0.000 | 0/3 |
| models-catboost-clean | housing | LossHigh | lowest | 30 % | 3 | -4320.3755 | [-5087.2861, -3762.0488] | 0.008 | 0/3 |
| models-catboost-clean | housing | LossHigh | lowest | auc | 3 | -2527.9931 | [-2594.8918, -2465.1763] | 0.000 | 0/3 |
| models-catboost-clean | housing | LossHigh | highest | 5 % | 3 | +454.2099 | [+325.3916, +575.7154] | 0.024 | 3/3 |
| models-catboost-clean | housing | LossHigh | highest | 10 % | 3 | +1141.8155 | [+1082.6707, +1230.4319] | 0.002 | 3/3 |
| models-catboost-clean | housing | LossHigh | highest | 20 % | 3 | +2147.6878 | [+1823.5973, +2665.1586] | 0.015 | 3/3 |
| models-catboost-clean | housing | LossHigh | highest | 30 % | 3 | +3042.2090 | [+2666.2188, +3596.5358] | 0.009 | 3/3 |
| models-catboost-clean | housing | LossHigh | highest | auc | 3 | +1584.0863 | [+1399.8237, +1891.3694] | 0.009 | 3/3 |
| models-catboost-clean | wine | CatBoostLFC | lowest | 5 % | 3 | -0.0081 | [-0.0164, -0.0038] | 0.193 | 0/3 |
| models-catboost-clean | wine | CatBoostLFC | lowest | 10 % | 3 | -0.0038 | [-0.0124, +0.0009] | 0.470 | 2/3 |
| models-catboost-clean | wine | CatBoostLFC | lowest | 20 % | 3 | +0.0083 | [-0.0210, +0.0413] | 0.691 | 2/3 |
| models-catboost-clean | wine | CatBoostLFC | lowest | 30 % | 3 | +0.0014 | [-0.0378, +0.0339] | 0.953 | 2/3 |
| models-catboost-clean | wine | CatBoostLFC | lowest | auc | 3 | +0.0007 | [-0.0160, +0.0157] | 0.946 | 2/3 |
| models-catboost-clean | wine | CatBoostLFC | highest | 5 % | 3 | -0.0152 | [-0.0251, -0.0011] | 0.170 | 0/3 |
| models-catboost-clean | wine | CatBoostLFC | highest | 10 % | 3 | -0.0285 | [-0.0411, -0.0147] | 0.065 | 0/3 |
| models-catboost-clean | wine | CatBoostLFC | highest | 20 % | 3 | -0.0320 | [-0.0566, -0.0146] | 0.127 | 0/3 |
| models-catboost-clean | wine | CatBoostLFC | highest | 30 % | 3 | -0.0592 | [-0.0865, -0.0443] | 0.050 | 0/3 |
| models-catboost-clean | wine | CatBoostLFC | highest | auc | 3 | -0.0302 | [-0.0478, -0.0195] | 0.076 | 0/3 |
| models-catboost-clean | wine | DataOOB | lowest | 5 % | 3 | -0.0064 | [-0.0123, -0.0010] | 0.187 | 0/3 |
| models-catboost-clean | wine | DataOOB | lowest | 10 % | 3 | +0.0020 | [-0.0036, +0.0068] | 0.573 | 2/3 |
| models-catboost-clean | wine | DataOOB | lowest | 20 % | 3 | +0.0114 | [+0.0024, +0.0172] | 0.130 | 3/3 |
| models-catboost-clean | wine | DataOOB | lowest | 30 % | 3 | -0.0129 | [-0.0646, +0.0139] | 0.667 | 2/3 |
| models-catboost-clean | wine | DataOOB | lowest | auc | 3 | +0.0011 | [-0.0094, +0.0069] | 0.854 | 2/3 |
| models-catboost-clean | wine | DataOOB | highest | 5 % | 3 | -0.0038 | [-0.0093, -0.0006] | 0.309 | 0/3 |
| models-catboost-clean | wine | DataOOB | highest | 10 % | 3 | -0.0047 | [-0.0121, -0.0006] | 0.340 | 0/3 |
| models-catboost-clean | wine | DataOOB | highest | 20 % | 3 | -0.0252 | [-0.0434, -0.0146] | 0.110 | 0/3 |
| models-catboost-clean | wine | DataOOB | highest | 30 % | 3 | -0.0923 | [-0.1197, -0.0467] | 0.057 | 0/3 |
| models-catboost-clean | wine | DataOOB | highest | auc | 3 | -0.0256 | [-0.0390, -0.0131] | 0.076 | 0/3 |
| models-catboost-clean | wine | LOO | lowest | 5 % | 3 | -0.0029 | [-0.0130, +0.0029] | 0.626 | 2/3 |
| models-catboost-clean | wine | LOO | lowest | 10 % | 3 | -0.0027 | [-0.0117, +0.0022] | 0.614 | 2/3 |
| models-catboost-clean | wine | LOO | lowest | 20 % | 3 | +0.0019 | [-0.0151, +0.0206] | 0.872 | 2/3 |
| models-catboost-clean | wine | LOO | lowest | 30 % | 3 | -0.0014 | [-0.0101, +0.0114] | 0.852 | 1/3 |
| models-catboost-clean | wine | LOO | lowest | auc | 3 | -0.0007 | [-0.0118, +0.0098] | 0.915 | 1/3 |
| models-catboost-clean | wine | LOO | highest | 5 % | 3 | -0.0104 | [-0.0206, -0.0035] | 0.185 | 0/3 |
| models-catboost-clean | wine | LOO | highest | 10 % | 3 | -0.0106 | [-0.0211, -0.0039] | 0.185 | 0/3 |
| models-catboost-clean | wine | LOO | highest | 20 % | 3 | +0.0002 | [-0.0129, +0.0080] | 0.977 | 2/3 |
| models-catboost-clean | wine | LOO | highest | 30 % | 3 | -0.0081 | [-0.0173, -0.0027] | 0.222 | 0/3 |
| models-catboost-clean | wine | LOO | highest | auc | 3 | -0.0057 | [-0.0159, +0.0001] | 0.385 | 1/3 |
| models-catboost-clean | wine | LossHigh | lowest | 5 % | 3 | -0.0040 | [-0.0092, +0.0052] | 0.478 | 1/3 |
| models-catboost-clean | wine | LossHigh | lowest | 10 % | 3 | -0.0038 | [-0.0070, -0.0020] | 0.144 | 0/3 |
| models-catboost-clean | wine | LossHigh | lowest | 20 % | 3 | +0.0023 | [-0.0018, +0.0073] | 0.480 | 2/3 |
| models-catboost-clean | wine | LossHigh | lowest | 30 % | 3 | +0.0055 | [+0.0037, +0.0072] | 0.031 | 3/3 |
| models-catboost-clean | wine | LossHigh | lowest | auc | 3 | +0.0001 | [-0.0014, +0.0009] | 0.929 | 2/3 |
| models-catboost-clean | wine | LossHigh | highest | 5 % | 3 | -0.0140 | [-0.0413, +0.0083] | 0.437 | 1/3 |
| models-catboost-clean | wine | LossHigh | highest | 10 % | 3 | +0.0165 | [-0.0461, +0.0734] | 0.680 | 2/3 |
| models-catboost-clean | wine | LossHigh | highest | 20 % | 3 | +0.0040 | [-0.0849, +0.0922] | 0.945 | 2/3 |
| models-catboost-clean | wine | LossHigh | highest | 30 % | 3 | -0.0061 | [-0.1043, +0.0963] | 0.926 | 1/3 |
| models-catboost-clean | wine | LossHigh | highest | auc | 3 | +0.0021 | [-0.0641, +0.0665] | 0.960 | 2/3 |
| models-catboost-noise10 | adult | CatBoostLFC | lowest | 5 % | 3 | +0.0075 | [+0.0018, +0.0125] | 0.139 | 3/3 |
| models-catboost-noise10 | adult | CatBoostLFC | lowest | 10 % | 3 | +0.0052 | [+0.0000, +0.0144] | 0.380 | 3/3 |
| models-catboost-noise10 | adult | CatBoostLFC | lowest | 20 % | 3 | +0.0067 | [-0.0024, +0.0177] | 0.371 | 2/3 |
| models-catboost-noise10 | adult | CatBoostLFC | lowest | auc | 3 | +0.0055 | [-0.0001, +0.0129] | 0.294 | 2/3 |
| models-catboost-noise10 | adult | DataOOB | lowest | 5 % | 3 | +0.0028 | [-0.0033, +0.0100] | 0.553 | 2/3 |
| models-catboost-noise10 | adult | DataOOB | lowest | 10 % | 3 | -0.0020 | [-0.0074, +0.0037] | 0.589 | 1/3 |
| models-catboost-noise10 | adult | DataOOB | lowest | 20 % | 3 | +0.0016 | [-0.0031, +0.0091] | 0.706 | 1/3 |
| models-catboost-noise10 | adult | DataOOB | lowest | auc | 3 | +0.0003 | [-0.0044, +0.0062] | 0.924 | 1/3 |
| models-catboost-noise10 | adult | KNNShapley | lowest | 5 % | 3 | +0.0040 | [-0.0000, +0.0108] | 0.368 | 2/3 |
| models-catboost-noise10 | adult | KNNShapley | lowest | 10 % | 3 | -0.0062 | [-0.0172, +0.0026] | 0.397 | 1/3 |
| models-catboost-noise10 | adult | KNNShapley | lowest | 20 % | 3 | -0.0075 | [-0.0150, +0.0030] | 0.301 | 1/3 |
| models-catboost-noise10 | adult | KNNShapley | lowest | auc | 3 | -0.0032 | [-0.0091, +0.0044] | 0.505 | 1/3 |
| models-catboost-noise10 | adult | LOO | lowest | 5 % | 3 | +0.0032 | [-0.0025, +0.0122] | 0.561 | 1/3 |
| models-catboost-noise10 | adult | LOO | lowest | 10 % | 3 | -0.0023 | [-0.0118, +0.0083] | 0.736 | 1/3 |
| models-catboost-noise10 | adult | LOO | lowest | 20 % | 3 | +0.0014 | [-0.0100, +0.0098] | 0.830 | 2/3 |
| models-catboost-noise10 | adult | LOO | lowest | auc | 3 | +0.0003 | [-0.0070, +0.0086] | 0.952 | 1/3 |
| models-catboost-noise10 | adult | LossHigh | lowest | 5 % | 3 | +0.0059 | [-0.0034, +0.0145] | 0.372 | 2/3 |
| models-catboost-noise10 | adult | LossHigh | lowest | 10 % | 3 | -0.0001 | [-0.0073, +0.0051] | 0.972 | 2/3 |
| models-catboost-noise10 | adult | LossHigh | lowest | 20 % | 3 | -0.0064 | [-0.0134, +0.0012] | 0.267 | 1/3 |
| models-catboost-noise10 | adult | LossHigh | lowest | auc | 3 | -0.0002 | [-0.0069, +0.0038] | 0.961 | 2/3 |
| models-catboost-noise10 | covertype | DataOOB | lowest | 5 % | 3 | +0.0083 | [+0.0028, +0.0142] | 0.129 | 3/3 |
| models-catboost-noise10 | covertype | DataOOB | lowest | 10 % | 3 | +0.0105 | [+0.0018, +0.0178] | 0.153 | 3/3 |
| models-catboost-noise10 | covertype | DataOOB | lowest | 20 % | 3 | +0.0124 | [+0.0044, +0.0210] | 0.123 | 3/3 |
| models-catboost-noise10 | covertype | DataOOB | lowest | auc | 3 | +0.0091 | [+0.0056, +0.0126] | 0.046 | 3/3 |
| models-catboost-noise10 | covertype | KNNShapley | lowest | 5 % | 3 | +0.0097 | [+0.0046, +0.0128] | 0.063 | 3/3 |
| models-catboost-noise10 | covertype | KNNShapley | lowest | 10 % | 3 | +0.0073 | [-0.0046, +0.0158] | 0.357 | 2/3 |
| models-catboost-noise10 | covertype | KNNShapley | lowest | 20 % | 3 | +0.0051 | [-0.0020, +0.0114] | 0.322 | 2/3 |
| models-catboost-noise10 | covertype | KNNShapley | lowest | auc | 3 | +0.0064 | [+0.0043, +0.0083] | 0.031 | 3/3 |
| models-catboost-noise10 | covertype | LOO | lowest | 5 % | 3 | -0.0008 | [-0.0068, +0.0038] | 0.823 | 2/3 |
| models-catboost-noise10 | covertype | LOO | lowest | 10 % | 3 | +0.0017 | [-0.0034, +0.0072] | 0.629 | 2/3 |
| models-catboost-noise10 | covertype | LOO | lowest | 20 % | 3 | -0.0027 | [-0.0122, +0.0054] | 0.655 | 1/3 |
| models-catboost-noise10 | covertype | LOO | lowest | auc | 3 | -0.0002 | [-0.0015, +0.0006] | 0.767 | 2/3 |
| models-catboost-noise10 | covertype | LossHigh | lowest | 5 % | 3 | +0.0031 | [-0.0016, +0.0072] | 0.346 | 2/3 |
| models-catboost-noise10 | covertype | LossHigh | lowest | 10 % | 3 | +0.0071 | [-0.0020, +0.0174] | 0.337 | 2/3 |
| models-catboost-noise10 | covertype | LossHigh | lowest | 20 % | 3 | +0.0075 | [+0.0014, +0.0150] | 0.199 | 3/3 |
| models-catboost-noise10 | covertype | LossHigh | lowest | auc | 3 | +0.0053 | [+0.0018, +0.0087] | 0.117 | 3/3 |
| models-catboost-noise10 | housing | CatBoostLFC | lowest | 5 % | 3 | +65.4427 | [-419.9297, +376.1546] | 0.815 | 2/3 |
| models-catboost-noise10 | housing | CatBoostLFC | lowest | 10 % | 3 | -233.3696 | [-945.6264, +415.5591] | 0.614 | 1/3 |
| models-catboost-noise10 | housing | CatBoostLFC | lowest | 20 % | 3 | -878.1415 | [-1631.7184, -64.1442] | 0.192 | 0/3 |
| models-catboost-noise10 | housing | CatBoostLFC | lowest | auc | 3 | -290.6883 | [-867.5219, +233.8373] | 0.458 | 1/3 |
| models-catboost-noise10 | housing | DataOOB | lowest | 5 % | 3 | +24.6136 | [-441.3428, +395.5612] | 0.929 | 2/3 |
| models-catboost-noise10 | housing | DataOOB | lowest | 10 % | 3 | +628.2457 | [+123.6250, +993.4884] | 0.137 | 3/3 |
| models-catboost-noise10 | housing | DataOOB | lowest | 20 % | 3 | +752.7081 | [+200.3652, +1430.7696] | 0.172 | 3/3 |
| models-catboost-noise10 | housing | DataOOB | lowest | auc | 3 | +429.9226 | [+293.7161, +628.1958] | 0.051 | 3/3 |
| models-catboost-noise10 | housing | LOO | lowest | 5 % | 3 | +181.0700 | [-202.3457, +550.0185] | 0.492 | 2/3 |
| models-catboost-noise10 | housing | LOO | lowest | 10 % | 3 | +388.5239 | [-502.5437, +1097.2304] | 0.496 | 2/3 |
| models-catboost-noise10 | housing | LOO | lowest | 20 % | 3 | +952.1327 | [+720.6158, +1269.6605] | 0.028 | 3/3 |
| models-catboost-noise10 | housing | LOO | lowest | auc | 3 | +428.9971 | [-22.5098, +729.1200] | 0.203 | 2/3 |
| models-catboost-noise10 | housing | LossHigh | lowest | 5 % | 3 | -288.4241 | [-637.5971, +58.4906] | 0.288 | 1/3 |
| models-catboost-noise10 | housing | LossHigh | lowest | 10 % | 3 | +553.9986 | [-62.5957, +960.2575] | 0.219 | 2/3 |
| models-catboost-noise10 | housing | LossHigh | lowest | 20 % | 3 | -987.6153 | [-1708.7695, -600.1616] | 0.112 | 0/3 |
| models-catboost-noise10 | housing | LossHigh | lowest | auc | 3 | -111.2604 | [-332.9131, +125.0764] | 0.489 | 1/3 |
| models-catboost-noise10 | wine | CatBoostLFC | lowest | 5 % | 3 | +0.0051 | [-0.0095, +0.0212] | 0.626 | 2/3 |
| models-catboost-noise10 | wine | CatBoostLFC | lowest | 10 % | 3 | +0.0027 | [-0.0025, +0.0060] | 0.413 | 2/3 |
| models-catboost-noise10 | wine | CatBoostLFC | lowest | 20 % | 3 | +0.0088 | [+0.0045, +0.0113] | 0.055 | 3/3 |
| models-catboost-noise10 | wine | CatBoostLFC | lowest | auc | 3 | +0.0045 | [-0.0006, +0.0103] | 0.296 | 2/3 |
| models-catboost-noise10 | wine | DataOOB | lowest | 5 % | 3 | +0.0073 | [-0.0038, +0.0202] | 0.406 | 2/3 |
| models-catboost-noise10 | wine | DataOOB | lowest | 10 % | 3 | +0.0034 | [-0.0020, +0.0062] | 0.338 | 2/3 |
| models-catboost-noise10 | wine | DataOOB | lowest | 20 % | 3 | +0.0065 | [-0.0005, +0.0135] | 0.249 | 2/3 |
| models-catboost-noise10 | wine | DataOOB | lowest | auc | 3 | +0.0047 | [+0.0016, +0.0072] | 0.102 | 3/3 |
| models-catboost-noise10 | wine | LOO | lowest | 5 % | 3 | -0.0202 | [-0.0540, -0.0001] | 0.356 | 0/3 |
| models-catboost-noise10 | wine | LOO | lowest | 10 % | 3 | -0.0206 | [-0.0670, +0.0050] | 0.469 | 2/3 |
| models-catboost-noise10 | wine | LOO | lowest | 20 % | 3 | -0.0173 | [-0.0761, +0.0184] | 0.618 | 2/3 |
| models-catboost-noise10 | wine | LOO | lowest | auc | 3 | -0.0171 | [-0.0576, +0.0064] | 0.489 | 1/3 |
| models-catboost-noise10 | wine | LossHigh | lowest | 5 % | 3 | +0.0070 | [-0.0004, +0.0194] | 0.380 | 2/3 |
| models-catboost-noise10 | wine | LossHigh | lowest | 10 % | 3 | +0.0056 | [+0.0010, +0.0094] | 0.150 | 3/3 |
| models-catboost-noise10 | wine | LossHigh | lowest | 20 % | 3 | +0.0069 | [-0.0011, +0.0142] | 0.262 | 2/3 |
| models-catboost-noise10 | wine | LossHigh | lowest | auc | 3 | +0.0056 | [+0.0044, +0.0070] | 0.017 | 3/3 |
| models-lightgbm-clean | adult | BoostIn | lowest | 5 % | 3 | +0.0027 | [-0.0081, +0.0128] | 0.698 | 2/3 |
| models-lightgbm-clean | adult | BoostIn | lowest | 10 % | 3 | -0.0066 | [-0.0308, +0.0163] | 0.676 | 1/3 |
| models-lightgbm-clean | adult | BoostIn | lowest | 20 % | 3 | -0.0277 | [-0.0694, -0.0043] | 0.316 | 0/3 |
| models-lightgbm-clean | adult | BoostIn | lowest | 30 % | 3 | -0.0374 | [-0.0518, -0.0277] | 0.036 | 0/3 |
| models-lightgbm-clean | adult | BoostIn | lowest | auc | 3 | -0.0167 | [-0.0389, -0.0007] | 0.283 | 0/3 |
| models-lightgbm-clean | adult | BoostIn | highest | 5 % | 3 | -0.0059 | [-0.0122, -0.0027] | 0.204 | 0/3 |
| models-lightgbm-clean | adult | BoostIn | highest | 10 % | 3 | -0.0288 | [-0.0350, -0.0219] | 0.017 | 0/3 |
| models-lightgbm-clean | adult | BoostIn | highest | 20 % | 3 | -0.0565 | [-0.0766, -0.0401] | 0.034 | 0/3 |
| models-lightgbm-clean | adult | BoostIn | highest | 30 % | 3 | -0.0896 | [-0.1226, -0.0722] | 0.032 | 0/3 |
| models-lightgbm-clean | adult | BoostIn | highest | auc | 3 | -0.0419 | [-0.0568, -0.0316] | 0.031 | 0/3 |
| models-lightgbm-clean | adult | DataOOB | lowest | 5 % | 3 | -0.0035 | [-0.0120, +0.0041] | 0.530 | 1/3 |
| models-lightgbm-clean | adult | DataOOB | lowest | 10 % | 3 | -0.0189 | [-0.0276, -0.0051] | 0.113 | 0/3 |
| models-lightgbm-clean | adult | DataOOB | lowest | 20 % | 3 | -0.0197 | [-0.0388, -0.0009] | 0.213 | 0/3 |
| models-lightgbm-clean | adult | DataOOB | lowest | 30 % | 3 | -0.0263 | [-0.0289, -0.0242] | 0.003 | 0/3 |
| models-lightgbm-clean | adult | DataOOB | lowest | auc | 3 | -0.0163 | [-0.0267, -0.0050] | 0.123 | 0/3 |
| models-lightgbm-clean | adult | DataOOB | highest | 5 % | 3 | +0.0038 | [-0.0003, +0.0084] | 0.270 | 2/3 |
| models-lightgbm-clean | adult | DataOOB | highest | 10 % | 3 | -0.0126 | [-0.0199, -0.0052] | 0.098 | 0/3 |
| models-lightgbm-clean | adult | DataOOB | highest | 20 % | 3 | -0.0161 | [-0.0303, -0.0039] | 0.171 | 0/3 |
| models-lightgbm-clean | adult | DataOOB | highest | 30 % | 3 | -0.0194 | [-0.0367, -0.0023] | 0.190 | 0/3 |
| models-lightgbm-clean | adult | DataOOB | highest | auc | 3 | -0.0111 | [-0.0155, -0.0073] | 0.043 | 0/3 |
| models-lightgbm-clean | adult | KNNShapley | lowest | 5 % | 3 | +0.0089 | [-0.0017, +0.0279] | 0.452 | 2/3 |
| models-lightgbm-clean | adult | KNNShapley | lowest | 10 % | 3 | -0.0103 | [-0.0207, +0.0061] | 0.341 | 1/3 |
| models-lightgbm-clean | adult | KNNShapley | lowest | 20 % | 3 | -0.0187 | [-0.0375, -0.0040] | 0.199 | 0/3 |
| models-lightgbm-clean | adult | KNNShapley | lowest | 30 % | 3 | -0.0351 | [-0.0467, -0.0121] | 0.093 | 0/3 |
| models-lightgbm-clean | adult | KNNShapley | lowest | auc | 3 | -0.0132 | [-0.0257, -0.0064] | 0.172 | 0/3 |
| models-lightgbm-clean | adult | KNNShapley | highest | 5 % | 3 | +0.0001 | [-0.0046, +0.0036] | 0.983 | 2/3 |
| models-lightgbm-clean | adult | KNNShapley | highest | 10 % | 3 | -0.0067 | [-0.0108, -0.0017] | 0.130 | 0/3 |
| models-lightgbm-clean | adult | KNNShapley | highest | 20 % | 3 | -0.0165 | [-0.0215, -0.0079] | 0.063 | 0/3 |
| models-lightgbm-clean | adult | KNNShapley | highest | 30 % | 3 | -0.0804 | [-0.1128, -0.0497] | 0.048 | 0/3 |
| models-lightgbm-clean | adult | KNNShapley | highest | auc | 3 | -0.0206 | [-0.0282, -0.0159] | 0.033 | 0/3 |
| models-lightgbm-clean | adult | LOO | lowest | 5 % | 3 | -0.0030 | [-0.0075, -0.0003] | 0.316 | 0/3 |
| models-lightgbm-clean | adult | LOO | lowest | 10 % | 3 | +0.0002 | [-0.0057, +0.0085] | 0.975 | 1/3 |
| models-lightgbm-clean | adult | LOO | lowest | 20 % | 3 | -0.0062 | [-0.0139, -0.0011] | 0.257 | 0/3 |
| models-lightgbm-clean | adult | LOO | lowest | 30 % | 3 | -0.0100 | [-0.0135, -0.0057] | 0.049 | 0/3 |
| models-lightgbm-clean | adult | LOO | lowest | auc | 3 | -0.0042 | [-0.0084, -0.0010] | 0.195 | 0/3 |
| models-lightgbm-clean | adult | LOO | highest | 5 % | 3 | +0.0075 | [-0.0032, +0.0196] | 0.378 | 2/3 |
| models-lightgbm-clean | adult | LOO | highest | 10 % | 3 | -0.0057 | [-0.0135, +0.0048] | 0.407 | 1/3 |
| models-lightgbm-clean | adult | LOO | highest | 20 % | 3 | -0.0015 | [-0.0141, +0.0059] | 0.838 | 2/3 |
| models-lightgbm-clean | adult | LOO | highest | 30 % | 3 | -0.0040 | [-0.0190, +0.0049] | 0.646 | 2/3 |
| models-lightgbm-clean | adult | LOO | highest | auc | 3 | -0.0013 | [-0.0083, +0.0033] | 0.739 | 2/3 |
| models-lightgbm-clean | adult | LossHigh | lowest | 5 % | 3 | +0.0008 | [-0.0081, +0.0126] | 0.905 | 1/3 |
| models-lightgbm-clean | adult | LossHigh | lowest | 10 % | 3 | -0.0225 | [-0.0273, -0.0157] | 0.023 | 0/3 |
| models-lightgbm-clean | adult | LossHigh | lowest | 20 % | 3 | -0.0165 | [-0.0301, +0.0025] | 0.235 | 1/3 |
| models-lightgbm-clean | adult | LossHigh | lowest | 30 % | 3 | -0.0291 | [-0.0404, -0.0208] | 0.038 | 0/3 |
| models-lightgbm-clean | adult | LossHigh | lowest | auc | 3 | -0.0158 | [-0.0249, -0.0066] | 0.096 | 0/3 |
| models-lightgbm-clean | adult | LossHigh | highest | 5 % | 3 | +0.0107 | [+0.0041, +0.0159] | 0.092 | 3/3 |
| models-lightgbm-clean | adult | LossHigh | highest | 10 % | 3 | +0.0028 | [-0.0015, +0.0085] | 0.444 | 2/3 |
| models-lightgbm-clean | adult | LossHigh | highest | 20 % | 3 | -0.0037 | [-0.0096, +0.0023] | 0.398 | 1/3 |
| models-lightgbm-clean | adult | LossHigh | highest | 30 % | 3 | -0.0183 | [-0.0319, +0.0015] | 0.213 | 1/3 |
| models-lightgbm-clean | adult | LossHigh | highest | auc | 3 | -0.0018 | [-0.0045, +0.0007] | 0.353 | 1/3 |
| models-lightgbm-clean | covertype | BoostIn | lowest | 5 % | 3 | +0.0057 | [-0.0074, +0.0156] | 0.490 | 2/3 |
| models-lightgbm-clean | covertype | BoostIn | lowest | 10 % | 3 | -0.0040 | [-0.0108, -0.0006] | 0.360 | 0/3 |
| models-lightgbm-clean | covertype | BoostIn | lowest | 20 % | 3 | -0.0001 | [-0.0106, +0.0104] | 0.992 | 1/3 |
| models-lightgbm-clean | covertype | BoostIn | lowest | 30 % | 3 | -0.0058 | [-0.0096, -0.0006] | 0.164 | 0/3 |
| models-lightgbm-clean | covertype | BoostIn | lowest | auc | 3 | -0.0010 | [-0.0087, +0.0058] | 0.829 | 1/3 |
| models-lightgbm-clean | covertype | BoostIn | highest | 5 % | 3 | -0.0162 | [-0.0196, -0.0118] | 0.020 | 0/3 |
| models-lightgbm-clean | covertype | BoostIn | highest | 10 % | 3 | -0.0319 | [-0.0436, -0.0230] | 0.035 | 0/3 |
| models-lightgbm-clean | covertype | BoostIn | highest | 20 % | 3 | -0.0613 | [-0.0872, -0.0346] | 0.056 | 0/3 |
| models-lightgbm-clean | covertype | BoostIn | highest | 30 % | 3 | -0.0813 | [-0.1014, -0.0488] | 0.038 | 0/3 |
| models-lightgbm-clean | covertype | BoostIn | highest | auc | 3 | -0.0446 | [-0.0552, -0.0283] | 0.033 | 0/3 |
| models-lightgbm-clean | covertype | DataOOB | lowest | 5 % | 3 | -0.0107 | [-0.0212, +0.0000] | 0.223 | 0/3 |
| models-lightgbm-clean | covertype | DataOOB | lowest | 10 % | 3 | -0.0054 | [-0.0080, -0.0018] | 0.101 | 0/3 |
| models-lightgbm-clean | covertype | DataOOB | lowest | 20 % | 3 | -0.0084 | [-0.0208, +0.0052] | 0.381 | 1/3 |
| models-lightgbm-clean | covertype | DataOOB | lowest | 30 % | 3 | -0.0071 | [-0.0174, +0.0040] | 0.368 | 1/3 |
| models-lightgbm-clean | covertype | DataOOB | lowest | auc | 3 | -0.0071 | [-0.0138, -0.0010] | 0.195 | 0/3 |
| models-lightgbm-clean | covertype | DataOOB | highest | 5 % | 3 | -0.0025 | [-0.0092, +0.0036] | 0.565 | 1/3 |
| models-lightgbm-clean | covertype | DataOOB | highest | 10 % | 3 | +0.0018 | [-0.0046, +0.0054] | 0.631 | 2/3 |
| models-lightgbm-clean | covertype | DataOOB | highest | 20 % | 3 | -0.0022 | [-0.0054, +0.0006] | 0.334 | 1/3 |
| models-lightgbm-clean | covertype | DataOOB | highest | 30 % | 3 | -0.0139 | [-0.0282, -0.0064] | 0.193 | 0/3 |
| models-lightgbm-clean | covertype | DataOOB | highest | auc | 3 | -0.0030 | [-0.0067, -0.0008] | 0.243 | 0/3 |
| models-lightgbm-clean | covertype | KNNShapley | lowest | 5 % | 3 | +0.0014 | [-0.0052, +0.0086] | 0.759 | 2/3 |
| models-lightgbm-clean | covertype | KNNShapley | lowest | 10 % | 3 | -0.0015 | [-0.0128, +0.0064] | 0.816 | 2/3 |
| models-lightgbm-clean | covertype | KNNShapley | lowest | 20 % | 3 | +0.0079 | [-0.0090, +0.0178] | 0.449 | 2/3 |
| models-lightgbm-clean | covertype | KNNShapley | lowest | 30 % | 3 | -0.0059 | [-0.0156, -0.0008] | 0.351 | 0/3 |
| models-lightgbm-clean | covertype | KNNShapley | lowest | auc | 3 | +0.0015 | [-0.0097, +0.0076] | 0.812 | 2/3 |
| models-lightgbm-clean | covertype | KNNShapley | highest | 5 % | 3 | -0.0066 | [-0.0130, -0.0010] | 0.199 | 0/3 |
| models-lightgbm-clean | covertype | KNNShapley | highest | 10 % | 3 | -0.0193 | [-0.0228, -0.0136] | 0.022 | 0/3 |
| models-lightgbm-clean | covertype | KNNShapley | highest | 20 % | 3 | -0.0245 | [-0.0348, -0.0076] | 0.103 | 0/3 |
| models-lightgbm-clean | covertype | KNNShapley | highest | 30 % | 3 | -0.0508 | [-0.0634, -0.0320] | 0.034 | 0/3 |
| models-lightgbm-clean | covertype | KNNShapley | highest | auc | 3 | -0.0226 | [-0.0285, -0.0114] | 0.056 | 0/3 |
| models-lightgbm-clean | covertype | LOO | lowest | 5 % | 3 | -0.0019 | [-0.0104, +0.0062] | 0.735 | 1/3 |
| models-lightgbm-clean | covertype | LOO | lowest | 10 % | 3 | +0.0040 | [+0.0024, +0.0052] | 0.041 | 3/3 |
| models-lightgbm-clean | covertype | LOO | lowest | 20 % | 3 | +0.0057 | [-0.0080, +0.0172] | 0.521 | 2/3 |
| models-lightgbm-clean | covertype | LOO | lowest | 30 % | 3 | -0.0037 | [-0.0128, +0.0132] | 0.706 | 1/3 |
| models-lightgbm-clean | covertype | LOO | lowest | auc | 3 | +0.0020 | [-0.0052, +0.0096] | 0.690 | 2/3 |
| models-lightgbm-clean | covertype | LOO | highest | 5 % | 3 | -0.0052 | [-0.0078, -0.0008] | 0.143 | 0/3 |
| models-lightgbm-clean | covertype | LOO | highest | 10 % | 3 | -0.0036 | [-0.0068, +0.0022] | 0.341 | 1/3 |
| models-lightgbm-clean | covertype | LOO | highest | 20 % | 3 | -0.0013 | [-0.0094, +0.0082] | 0.828 | 1/3 |
| models-lightgbm-clean | covertype | LOO | highest | 30 % | 3 | +0.0083 | [+0.0002, +0.0184] | 0.259 | 3/3 |
| models-lightgbm-clean | covertype | LOO | highest | auc | 3 | -0.0008 | [-0.0037, +0.0030] | 0.724 | 1/3 |
| models-lightgbm-clean | covertype | LossHigh | lowest | 5 % | 3 | -0.0055 | [-0.0198, +0.0070] | 0.551 | 1/3 |
| models-lightgbm-clean | covertype | LossHigh | lowest | 10 % | 3 | -0.0058 | [-0.0084, -0.0022] | 0.089 | 0/3 |
| models-lightgbm-clean | covertype | LossHigh | lowest | 20 % | 3 | -0.0007 | [-0.0134, +0.0090] | 0.922 | 2/3 |
| models-lightgbm-clean | covertype | LossHigh | lowest | 30 % | 3 | -0.0113 | [-0.0212, +0.0038] | 0.279 | 1/3 |
| models-lightgbm-clean | covertype | LossHigh | lowest | auc | 3 | -0.0045 | [-0.0130, +0.0009] | 0.406 | 1/3 |
| models-lightgbm-clean | covertype | LossHigh | highest | 5 % | 3 | -0.0017 | [-0.0042, +0.0004] | 0.342 | 1/3 |
| models-lightgbm-clean | covertype | LossHigh | highest | 10 % | 3 | +0.0012 | [-0.0062, +0.0126] | 0.855 | 1/3 |
| models-lightgbm-clean | covertype | LossHigh | highest | 20 % | 3 | +0.0005 | [-0.0092, +0.0084] | 0.927 | 2/3 |
| models-lightgbm-clean | covertype | LossHigh | highest | 30 % | 3 | +0.0027 | [-0.0014, +0.0056] | 0.332 | 2/3 |
| models-lightgbm-clean | covertype | LossHigh | highest | auc | 3 | +0.0006 | [-0.0047, +0.0070] | 0.867 | 1/3 |
| models-lightgbm-clean | housing | BoostIn | lowest | 5 % | 3 | -853.3275 | [-1272.1023, -619.5056] | 0.055 | 0/3 |
| models-lightgbm-clean | housing | BoostIn | lowest | 10 % | 3 | -1794.4216 | [-1933.8078, -1689.6741] | 0.002 | 0/3 |
| models-lightgbm-clean | housing | BoostIn | lowest | 20 % | 3 | -5338.4707 | [-5577.4139, -4893.8466] | 0.002 | 0/3 |
| models-lightgbm-clean | housing | BoostIn | lowest | 30 % | 3 | -12250.6669 | [-14056.8969, -10662.8188] | 0.006 | 0/3 |
| models-lightgbm-clean | housing | BoostIn | lowest | auc | 3 | -4412.0947 | [-4626.0611, -4231.1222] | 0.001 | 0/3 |
| models-lightgbm-clean | housing | BoostIn | highest | 5 % | 3 | -2648.3792 | [-3024.7572, -2167.0734] | 0.009 | 0/3 |
| models-lightgbm-clean | housing | BoostIn | highest | 10 % | 3 | -4740.7468 | [-5888.7172, -3478.5443] | 0.021 | 0/3 |
| models-lightgbm-clean | housing | BoostIn | highest | 20 % | 3 | -11456.6381 | [-11896.8586, -10760.6129] | 0.001 | 0/3 |
| models-lightgbm-clean | housing | BoostIn | highest | 30 % | 3 | -17290.0696 | [-17449.1416, -17198.2508] | 0.000 | 0/3 |
| models-lightgbm-clean | housing | BoostIn | highest | auc | 3 | -8327.1409 | [-8603.8809, -8167.6904] | 0.000 | 0/3 |
| models-lightgbm-clean | housing | DataOOB | lowest | 5 % | 3 | +717.8156 | [+15.1426, +1556.9949] | 0.252 | 3/3 |
| models-lightgbm-clean | housing | DataOOB | lowest | 10 % | 3 | +409.1903 | [-353.2521, +1251.6091] | 0.472 | 2/3 |
| models-lightgbm-clean | housing | DataOOB | lowest | 20 % | 3 | -726.3995 | [-1064.5260, -222.8348] | 0.105 | 0/3 |
| models-lightgbm-clean | housing | DataOOB | lowest | 30 % | 3 | -127.5016 | [-1016.1649, +732.0611] | 0.824 | 1/3 |
| models-lightgbm-clean | housing | DataOOB | lowest | auc | 3 | -41.4499 | [-208.7768, +251.1241] | 0.804 | 1/3 |
| models-lightgbm-clean | housing | DataOOB | highest | 5 % | 3 | -1.3460 | [-407.7865, +631.7152] | 0.997 | 1/3 |
| models-lightgbm-clean | housing | DataOOB | highest | 10 % | 3 | +16.7552 | [+3.9888, +25.1303] | 0.123 | 3/3 |
| models-lightgbm-clean | housing | DataOOB | highest | 20 % | 3 | +263.9725 | [-493.2077, +725.5186] | 0.561 | 2/3 |
| models-lightgbm-clean | housing | DataOOB | highest | 30 % | 3 | +838.2401 | [+83.0521, +1791.4175] | 0.238 | 3/3 |
| models-lightgbm-clean | housing | DataOOB | highest | auc | 3 | +231.6620 | [+222.9738, +245.7355] | 0.001 | 3/3 |
| models-lightgbm-clean | housing | LOO | lowest | 5 % | 3 | +587.3509 | [+368.6715, +888.9264] | 0.064 | 3/3 |
| models-lightgbm-clean | housing | LOO | lowest | 10 % | 3 | +33.6842 | [-542.9599, +481.7089] | 0.922 | 2/3 |
| models-lightgbm-clean | housing | LOO | lowest | 20 % | 3 | +848.4101 | [+318.2932, +1158.1414] | 0.086 | 3/3 |
| models-lightgbm-clean | housing | LOO | lowest | 30 % | 3 | +1309.4064 | [+293.3312, +2942.8580] | 0.253 | 3/3 |
| models-lightgbm-clean | housing | LOO | lowest | auc | 3 | +607.3506 | [+353.4896, +1058.3960] | 0.115 | 3/3 |
| models-lightgbm-clean | housing | LOO | highest | 5 % | 3 | -93.5618 | [-1230.1615, +1189.5075] | 0.906 | 1/3 |
| models-lightgbm-clean | housing | LOO | highest | 10 % | 3 | -188.8879 | [-1129.1424, +936.7206] | 0.784 | 1/3 |
| models-lightgbm-clean | housing | LOO | highest | 20 % | 3 | +493.1351 | [-68.5757, +1073.5074] | 0.274 | 2/3 |
| models-lightgbm-clean | housing | LOO | highest | 30 % | 3 | +648.6870 | [-59.1921, +1789.7145] | 0.377 | 2/3 |
| models-lightgbm-clean | housing | LOO | highest | auc | 3 | +209.6773 | [-285.5229, +1088.5530] | 0.681 | 1/3 |
| models-lightgbm-clean | housing | LossHigh | lowest | 5 % | 3 | +708.7066 | [-176.8141, +1501.8989] | 0.283 | 2/3 |
| models-lightgbm-clean | housing | LossHigh | lowest | 10 % | 3 | +1055.9282 | [+613.6849, +1323.0094] | 0.042 | 3/3 |
| models-lightgbm-clean | housing | LossHigh | lowest | 20 % | 3 | +1577.5469 | [+922.7588, +2450.2488] | 0.074 | 3/3 |
| models-lightgbm-clean | housing | LossHigh | lowest | 30 % | 3 | +2008.4518 | [+736.3013, +2897.5735] | 0.091 | 3/3 |
| models-lightgbm-clean | housing | LossHigh | lowest | auc | 3 | +1242.6907 | [+708.6067, +1880.7473] | 0.068 | 3/3 |
| models-lightgbm-clean | housing | LossHigh | highest | 5 % | 3 | -104.8554 | [-642.7347, +813.3224] | 0.841 | 1/3 |
| models-lightgbm-clean | housing | LossHigh | highest | 10 % | 3 | +77.4212 | [-402.4328, +348.6727] | 0.778 | 2/3 |
| models-lightgbm-clean | housing | LossHigh | highest | 20 % | 3 | +373.1723 | [-137.9180, +737.2415] | 0.292 | 2/3 |
| models-lightgbm-clean | housing | LossHigh | highest | 30 % | 3 | +1651.0523 | [+984.2657, +2891.2958] | 0.117 | 3/3 |
| models-lightgbm-clean | housing | LossHigh | highest | auc | 3 | +401.4456 | [+98.1173, +690.2260] | 0.144 | 3/3 |
| models-lightgbm-clean | wine | BoostIn | lowest | 5 % | 3 | -0.0209 | [-0.0339, -0.0112] | 0.092 | 0/3 |
| models-lightgbm-clean | wine | BoostIn | lowest | 10 % | 3 | -0.0078 | [-0.0366, +0.0396] | 0.776 | 1/3 |
| models-lightgbm-clean | wine | BoostIn | lowest | 20 % | 3 | -0.0516 | [-0.1175, +0.0103] | 0.297 | 1/3 |
| models-lightgbm-clean | wine | BoostIn | lowest | 30 % | 3 | -0.0678 | [-0.0963, -0.0163] | 0.119 | 0/3 |
| models-lightgbm-clean | wine | BoostIn | lowest | auc | 3 | -0.0339 | [-0.0663, +0.0088] | 0.267 | 1/3 |
| models-lightgbm-clean | wine | BoostIn | highest | 5 % | 3 | -0.0178 | [-0.0254, -0.0057] | 0.100 | 0/3 |
| models-lightgbm-clean | wine | BoostIn | highest | 10 % | 3 | -0.0268 | [-0.0383, -0.0118] | 0.076 | 0/3 |
| models-lightgbm-clean | wine | BoostIn | highest | 20 % | 3 | -0.0751 | [-0.1267, -0.0399] | 0.104 | 0/3 |
| models-lightgbm-clean | wine | BoostIn | highest | 30 % | 3 | -0.0900 | [-0.1265, -0.0419] | 0.070 | 0/3 |
| models-lightgbm-clean | wine | BoostIn | highest | auc | 3 | -0.0497 | [-0.0719, -0.0275] | 0.061 | 0/3 |
| models-lightgbm-clean | wine | DataOOB | lowest | 5 % | 3 | -0.0015 | [-0.0283, +0.0381] | 0.948 | 1/3 |
| models-lightgbm-clean | wine | DataOOB | lowest | 10 % | 3 | -0.0053 | [-0.0344, +0.0287] | 0.799 | 1/3 |
| models-lightgbm-clean | wine | DataOOB | lowest | 20 % | 3 | -0.0170 | [-0.1088, +0.0466] | 0.752 | 2/3 |
| models-lightgbm-clean | wine | DataOOB | lowest | 30 % | 3 | -0.0014 | [-0.0529, +0.0259] | 0.963 | 2/3 |
| models-lightgbm-clean | wine | DataOOB | lowest | auc | 3 | -0.0075 | [-0.0584, +0.0211] | 0.797 | 2/3 |
| models-lightgbm-clean | wine | DataOOB | highest | 5 % | 3 | -0.0154 | [-0.0463, +0.0144] | 0.472 | 1/3 |
| models-lightgbm-clean | wine | DataOOB | highest | 10 % | 3 | +0.0092 | [-0.0049, +0.0184] | 0.326 | 2/3 |
| models-lightgbm-clean | wine | DataOOB | highest | 20 % | 3 | -0.0364 | [-0.1217, +0.0110] | 0.483 | 2/3 |
| models-lightgbm-clean | wine | DataOOB | highest | 30 % | 3 | -0.0460 | [-0.0823, -0.0234] | 0.128 | 0/3 |
| models-lightgbm-clean | wine | DataOOB | highest | auc | 3 | -0.0201 | [-0.0574, +0.0042] | 0.400 | 1/3 |
| models-lightgbm-clean | wine | LOO | lowest | 5 % | 3 | +0.0039 | [-0.0191, +0.0249] | 0.790 | 2/3 |
| models-lightgbm-clean | wine | LOO | lowest | 10 % | 3 | +0.0046 | [-0.0160, +0.0352] | 0.796 | 1/3 |
| models-lightgbm-clean | wine | LOO | lowest | 20 % | 3 | -0.0125 | [-0.0897, +0.0468] | 0.787 | 2/3 |
| models-lightgbm-clean | wine | LOO | lowest | 30 % | 3 | -0.0409 | [-0.0958, +0.0163] | 0.334 | 1/3 |
| models-lightgbm-clean | wine | LOO | lowest | auc | 3 | -0.0092 | [-0.0489, +0.0312] | 0.730 | 1/3 |
| models-lightgbm-clean | wine | LOO | highest | 5 % | 3 | -0.0256 | [-0.0422, +0.0056] | 0.243 | 1/3 |
| models-lightgbm-clean | wine | LOO | highest | 10 % | 3 | -0.0091 | [-0.0275, +0.0043] | 0.439 | 1/3 |
| models-lightgbm-clean | wine | LOO | highest | 20 % | 3 | -0.0324 | [-0.0836, -0.0015] | 0.336 | 0/3 |
| models-lightgbm-clean | wine | LOO | highest | 30 % | 3 | -0.0251 | [-0.0551, -0.0058] | 0.240 | 0/3 |
| models-lightgbm-clean | wine | LOO | highest | auc | 3 | -0.0215 | [-0.0506, +0.0005] | 0.292 | 1/3 |
| models-lightgbm-clean | wine | LossHigh | lowest | 5 % | 3 | -0.0043 | [-0.0247, +0.0225] | 0.787 | 1/3 |
| models-lightgbm-clean | wine | LossHigh | lowest | 10 % | 3 | -0.0064 | [-0.0315, +0.0124] | 0.672 | 1/3 |
| models-lightgbm-clean | wine | LossHigh | lowest | 20 % | 3 | -0.0279 | [-0.0905, +0.0117] | 0.471 | 1/3 |
| models-lightgbm-clean | wine | LossHigh | lowest | 30 % | 3 | -0.0035 | [-0.0449, +0.0387] | 0.899 | 1/3 |
| models-lightgbm-clean | wine | LossHigh | lowest | auc | 3 | -0.0122 | [-0.0496, +0.0172] | 0.599 | 1/3 |
| models-lightgbm-clean | wine | LossHigh | highest | 5 % | 3 | -0.0114 | [-0.0277, +0.0022] | 0.321 | 1/3 |
| models-lightgbm-clean | wine | LossHigh | highest | 10 % | 3 | -0.0147 | [-0.0443, +0.0124] | 0.465 | 1/3 |
| models-lightgbm-clean | wine | LossHigh | highest | 20 % | 3 | -0.0328 | [-0.0843, -0.0023] | 0.334 | 0/3 |
| models-lightgbm-clean | wine | LossHigh | highest | 30 % | 3 | -0.0368 | [-0.0580, -0.0246] | 0.074 | 0/3 |
| models-lightgbm-clean | wine | LossHigh | highest | auc | 3 | -0.0226 | [-0.0485, -0.0069] | 0.224 | 0/3 |
| models-lightgbm-noise10 | adult | BoostIn | lowest | 5 % | 3 | +0.0107 | [-0.0038, +0.0302] | 0.400 | 2/3 |
| models-lightgbm-noise10 | adult | BoostIn | lowest | 10 % | 3 | +0.0164 | [+0.0105, +0.0261] | 0.079 | 3/3 |
| models-lightgbm-noise10 | adult | BoostIn | lowest | 20 % | 3 | +0.0206 | [+0.0069, +0.0319] | 0.106 | 3/3 |
| models-lightgbm-noise10 | adult | BoostIn | lowest | auc | 3 | +0.0140 | [+0.0111, +0.0191] | 0.032 | 3/3 |
| models-lightgbm-noise10 | adult | DataOOB | lowest | 5 % | 3 | +0.0212 | [+0.0092, +0.0390] | 0.144 | 3/3 |
| models-lightgbm-noise10 | adult | DataOOB | lowest | 10 % | 3 | +0.0105 | [+0.0072, +0.0124] | 0.023 | 3/3 |
| models-lightgbm-noise10 | adult | DataOOB | lowest | 20 % | 3 | +0.0040 | [-0.0057, +0.0164] | 0.602 | 2/3 |
| models-lightgbm-noise10 | adult | DataOOB | lowest | auc | 3 | +0.0102 | [+0.0053, +0.0129] | 0.053 | 3/3 |
| models-lightgbm-noise10 | adult | KNNShapley | lowest | 5 % | 3 | +0.0209 | [+0.0096, +0.0391] | 0.151 | 3/3 |
| models-lightgbm-noise10 | adult | KNNShapley | lowest | 10 % | 3 | +0.0190 | [+0.0172, +0.0213] | 0.004 | 3/3 |
| models-lightgbm-noise10 | adult | KNNShapley | lowest | 20 % | 3 | +0.0067 | [-0.0028, +0.0222] | 0.482 | 2/3 |
| models-lightgbm-noise10 | adult | KNNShapley | lowest | auc | 3 | +0.0140 | [+0.0108, +0.0168] | 0.015 | 3/3 |
| models-lightgbm-noise10 | adult | LOO | lowest | 5 % | 3 | +0.0019 | [-0.0020, +0.0041] | 0.427 | 2/3 |
| models-lightgbm-noise10 | adult | LOO | lowest | 10 % | 3 | +0.0011 | [-0.0127, +0.0166] | 0.909 | 1/3 |
| models-lightgbm-noise10 | adult | LOO | lowest | 20 % | 3 | -0.0129 | [-0.0472, +0.0093] | 0.537 | 1/3 |
| models-lightgbm-noise10 | adult | LOO | lowest | auc | 3 | -0.0023 | [-0.0110, +0.0081] | 0.717 | 1/3 |
| models-lightgbm-noise10 | adult | LossHigh | lowest | 5 % | 3 | +0.0205 | [+0.0074, +0.0428] | 0.209 | 3/3 |
| models-lightgbm-noise10 | adult | LossHigh | lowest | 10 % | 3 | +0.0202 | [+0.0123, +0.0246] | 0.037 | 3/3 |
| models-lightgbm-noise10 | adult | LossHigh | lowest | 20 % | 3 | +0.0042 | [-0.0197, +0.0169] | 0.758 | 2/3 |
| models-lightgbm-noise10 | adult | LossHigh | lowest | auc | 3 | +0.0138 | [+0.0015, +0.0242] | 0.172 | 3/3 |
| models-lightgbm-noise10 | covertype | BoostIn | lowest | 5 % | 3 | +0.0090 | [+0.0052, +0.0112] | 0.042 | 3/3 |
| models-lightgbm-noise10 | covertype | BoostIn | lowest | 10 % | 3 | +0.0042 | [-0.0038, +0.0086] | 0.405 | 2/3 |
| models-lightgbm-noise10 | covertype | BoostIn | lowest | 20 % | 3 | +0.0069 | [+0.0034, +0.0112] | 0.096 | 3/3 |
| models-lightgbm-noise10 | covertype | BoostIn | lowest | auc | 3 | +0.0055 | [+0.0014, +0.0088] | 0.128 | 3/3 |
| models-lightgbm-noise10 | covertype | DataOOB | lowest | 5 % | 3 | +0.0089 | [+0.0004, +0.0160] | 0.189 | 3/3 |
| models-lightgbm-noise10 | covertype | DataOOB | lowest | 10 % | 3 | +0.0101 | [+0.0006, +0.0164] | 0.172 | 3/3 |
| models-lightgbm-noise10 | covertype | DataOOB | lowest | 20 % | 3 | +0.0026 | [-0.0076, +0.0086] | 0.662 | 2/3 |
| models-lightgbm-noise10 | covertype | DataOOB | lowest | auc | 3 | +0.0067 | [+0.0057, +0.0084] | 0.016 | 3/3 |
| models-lightgbm-noise10 | covertype | KNNShapley | lowest | 5 % | 3 | +0.0073 | [-0.0008, +0.0162] | 0.278 | 2/3 |
| models-lightgbm-noise10 | covertype | KNNShapley | lowest | 10 % | 3 | +0.0071 | [+0.0036, +0.0104] | 0.069 | 3/3 |
| models-lightgbm-noise10 | covertype | KNNShapley | lowest | 20 % | 3 | +0.0143 | [+0.0080, +0.0174] | 0.045 | 3/3 |
| models-lightgbm-noise10 | covertype | KNNShapley | lowest | auc | 3 | +0.0080 | [+0.0063, +0.0097] | 0.015 | 3/3 |
| models-lightgbm-noise10 | covertype | LOO | lowest | 5 % | 3 | +0.0041 | [+0.0006, +0.0084] | 0.218 | 3/3 |
| models-lightgbm-noise10 | covertype | LOO | lowest | 10 % | 3 | -0.0001 | [-0.0076, +0.0062] | 0.977 | 2/3 |
| models-lightgbm-noise10 | covertype | LOO | lowest | 20 % | 3 | +0.0033 | [-0.0024, +0.0112] | 0.508 | 2/3 |
| models-lightgbm-noise10 | covertype | LOO | lowest | auc | 3 | +0.0018 | [-0.0026, +0.0053] | 0.525 | 2/3 |
| models-lightgbm-noise10 | covertype | LossHigh | lowest | 5 % | 3 | +0.0076 | [+0.0056, +0.0100] | 0.027 | 3/3 |
| models-lightgbm-noise10 | covertype | LossHigh | lowest | 10 % | 3 | +0.0039 | [+0.0032, +0.0044] | 0.009 | 3/3 |
| models-lightgbm-noise10 | covertype | LossHigh | lowest | 20 % | 3 | +0.0061 | [-0.0018, +0.0220] | 0.520 | 1/3 |
| models-lightgbm-noise10 | covertype | LossHigh | lowest | auc | 3 | +0.0049 | [+0.0026, +0.0085] | 0.117 | 3/3 |
| models-lightgbm-noise10 | housing | BoostIn | lowest | 5 % | 3 | +201.7631 | [-1213.4166, +1381.3102] | 0.815 | 2/3 |
| models-lightgbm-noise10 | housing | BoostIn | lowest | 10 % | 3 | -3852.2450 | [-5314.2988, -1242.6739] | 0.099 | 0/3 |
| models-lightgbm-noise10 | housing | BoostIn | lowest | 20 % | 3 | -16321.4882 | [-23135.8958, -12725.7206] | 0.041 | 0/3 |
| models-lightgbm-noise10 | housing | BoostIn | lowest | auc | 3 | -5474.5232 | [-7313.5573, -3950.7870] | 0.031 | 0/3 |
| models-lightgbm-noise10 | housing | DataOOB | lowest | 5 % | 3 | +2662.3371 | [+1587.5531, +3724.8145] | 0.050 | 3/3 |
| models-lightgbm-noise10 | housing | DataOOB | lowest | 10 % | 3 | +11158.0396 | [+10639.5999, +11599.8227] | 0.001 | 3/3 |
| models-lightgbm-noise10 | housing | DataOOB | lowest | 20 % | 3 | +11713.3481 | [+11295.5522, +12192.2703] | 0.000 | 3/3 |
| models-lightgbm-noise10 | housing | DataOOB | lowest | auc | 3 | +7778.1861 | [+7482.3989, +8194.1926] | 0.001 | 3/3 |
| models-lightgbm-noise10 | housing | LOO | lowest | 5 % | 3 | +1556.7066 | [-247.5015, +4317.3807] | 0.382 | 2/3 |
| models-lightgbm-noise10 | housing | LOO | lowest | 10 % | 3 | +425.2823 | [+99.4542, +830.6197] | 0.186 | 3/3 |
| models-lightgbm-noise10 | housing | LOO | lowest | 20 % | 3 | +1451.1297 | [+1254.9393, +1686.4560] | 0.007 | 3/3 |
| models-lightgbm-noise10 | housing | LOO | lowest | auc | 3 | +911.4399 | [+289.1548, +1630.6241] | 0.145 | 3/3 |
| models-lightgbm-noise10 | housing | LossHigh | lowest | 5 % | 3 | +2384.8541 | [+684.1655, +3942.2598] | 0.127 | 3/3 |
| models-lightgbm-noise10 | housing | LossHigh | lowest | 10 % | 3 | +9760.2142 | [+9435.0396, +9946.1439] | 0.000 | 3/3 |
| models-lightgbm-noise10 | housing | LossHigh | lowest | 20 % | 3 | +12096.3694 | [+11199.4716, +13299.0693] | 0.003 | 3/3 |
| models-lightgbm-noise10 | housing | LossHigh | lowest | auc | 3 | +7280.3862 | [+7225.6127, +7323.5727] | 0.000 | 3/3 |
| models-lightgbm-noise10 | wine | BoostIn | lowest | 5 % | 3 | +0.0061 | [-0.0106, +0.0299] | 0.667 | 1/3 |
| models-lightgbm-noise10 | wine | BoostIn | lowest | 10 % | 3 | -0.0401 | [-0.0833, +0.0136] | 0.294 | 1/3 |
| models-lightgbm-noise10 | wine | BoostIn | lowest | 20 % | 3 | -0.0401 | [-0.0843, +0.0450] | 0.446 | 1/3 |
| models-lightgbm-noise10 | wine | BoostIn | lowest | auc | 3 | -0.0235 | [-0.0541, +0.0238] | 0.430 | 1/3 |
| models-lightgbm-noise10 | wine | DataOOB | lowest | 5 % | 3 | +0.0420 | [+0.0212, +0.0761] | 0.134 | 3/3 |
| models-lightgbm-noise10 | wine | DataOOB | lowest | 10 % | 3 | +0.0208 | [-0.0198, +0.0475] | 0.419 | 2/3 |
| models-lightgbm-noise10 | wine | DataOOB | lowest | 20 % | 3 | +0.0670 | [+0.0136, +0.1019] | 0.132 | 3/3 |
| models-lightgbm-noise10 | wine | DataOOB | lowest | auc | 3 | +0.0351 | [+0.0013, +0.0582] | 0.180 | 3/3 |
| models-lightgbm-noise10 | wine | LOO | lowest | 5 % | 3 | +0.0220 | [-0.0016, +0.0416] | 0.224 | 2/3 |
| models-lightgbm-noise10 | wine | LOO | lowest | 10 % | 3 | -0.0126 | [-0.0363, +0.0072] | 0.426 | 1/3 |
| models-lightgbm-noise10 | wine | LOO | lowest | 20 % | 3 | +0.0128 | [-0.0346, +0.0455] | 0.650 | 2/3 |
| models-lightgbm-noise10 | wine | LOO | lowest | auc | 3 | +0.0040 | [-0.0227, +0.0245] | 0.803 | 2/3 |
| models-lightgbm-noise10 | wine | LossHigh | lowest | 5 % | 3 | +0.0261 | [-0.0008, +0.0497] | 0.217 | 2/3 |
| models-lightgbm-noise10 | wine | LossHigh | lowest | 10 % | 3 | +0.0278 | [+0.0052, +0.0492] | 0.160 | 3/3 |
| models-lightgbm-noise10 | wine | LossHigh | lowest | 20 % | 3 | +0.0499 | [-0.0171, +0.0981] | 0.286 | 2/3 |
| models-lightgbm-noise10 | wine | LossHigh | lowest | auc | 3 | +0.0294 | [-0.0025, +0.0554] | 0.225 | 2/3 |
| models-random_forest-clean | adult | DataOOB | lowest | 5 % | 3 | -0.0006 | [-0.0058, +0.0066] | 0.890 | 1/3 |
| models-random_forest-clean | adult | DataOOB | lowest | 10 % | 3 | -0.0012 | [-0.0026, +0.0008] | 0.363 | 1/3 |
| models-random_forest-clean | adult | DataOOB | lowest | 20 % | 3 | -0.0100 | [-0.0219, -0.0014] | 0.246 | 0/3 |
| models-random_forest-clean | adult | DataOOB | lowest | 30 % | 3 | -0.0109 | [-0.0162, -0.0036] | 0.102 | 0/3 |
| models-random_forest-clean | adult | DataOOB | lowest | auc | 3 | -0.0055 | [-0.0096, -0.0024] | 0.124 | 0/3 |
| models-random_forest-clean | adult | DataOOB | highest | 5 % | 3 | -0.0033 | [-0.0105, +0.0070] | 0.593 | 1/3 |
| models-random_forest-clean | adult | DataOOB | highest | 10 % | 3 | -0.0107 | [-0.0269, -0.0020] | 0.320 | 0/3 |
| models-random_forest-clean | adult | DataOOB | highest | 20 % | 3 | -0.0069 | [-0.0143, +0.0009] | 0.254 | 1/3 |
| models-random_forest-clean | adult | DataOOB | highest | 30 % | 3 | -0.0147 | [-0.0203, -0.0104] | 0.038 | 0/3 |
| models-random_forest-clean | adult | DataOOB | highest | auc | 3 | -0.0080 | [-0.0137, -0.0035] | 0.117 | 0/3 |
| models-random_forest-clean | adult | KNNShapley | lowest | 5 % | 3 | +0.0003 | [-0.0026, +0.0047] | 0.895 | 1/3 |
| models-random_forest-clean | adult | KNNShapley | lowest | 10 % | 3 | -0.0008 | [-0.0022, +0.0002] | 0.415 | 1/3 |
| models-random_forest-clean | adult | KNNShapley | lowest | 20 % | 3 | -0.0114 | [-0.0141, -0.0096] | 0.015 | 0/3 |
| models-random_forest-clean | adult | KNNShapley | lowest | 30 % | 3 | -0.0218 | [-0.0306, -0.0152] | 0.041 | 0/3 |
| models-random_forest-clean | adult | KNNShapley | lowest | auc | 3 | -0.0075 | [-0.0108, -0.0058] | 0.043 | 0/3 |
| models-random_forest-clean | adult | KNNShapley | highest | 5 % | 3 | -0.0084 | [-0.0129, -0.0006] | 0.164 | 0/3 |
| models-random_forest-clean | adult | KNNShapley | highest | 10 % | 3 | -0.0117 | [-0.0151, -0.0061] | 0.054 | 0/3 |
| models-random_forest-clean | adult | KNNShapley | highest | 20 % | 3 | -0.0269 | [-0.0393, -0.0118] | 0.079 | 0/3 |
| models-random_forest-clean | adult | KNNShapley | highest | 30 % | 3 | -0.0517 | [-0.0784, -0.0289] | 0.070 | 0/3 |
| models-random_forest-clean | adult | KNNShapley | highest | auc | 3 | -0.0219 | [-0.0316, -0.0104] | 0.072 | 0/3 |
| models-random_forest-clean | adult | LOO | lowest | 5 % | 3 | +0.0041 | [-0.0044, +0.0099] | 0.446 | 2/3 |
| models-random_forest-clean | adult | LOO | lowest | 10 % | 3 | +0.0008 | [-0.0037, +0.0047] | 0.765 | 2/3 |
| models-random_forest-clean | adult | LOO | lowest | 20 % | 3 | -0.0018 | [-0.0055, +0.0050] | 0.655 | 1/3 |
| models-random_forest-clean | adult | LOO | lowest | 30 % | 3 | -0.0002 | [-0.0048, +0.0032] | 0.943 | 2/3 |
| models-random_forest-clean | adult | LOO | lowest | auc | 3 | +0.0003 | [-0.0016, +0.0037] | 0.889 | 1/3 |
| models-random_forest-clean | adult | LOO | highest | 5 % | 3 | +0.0006 | [-0.0004, +0.0012] | 0.331 | 2/3 |
| models-random_forest-clean | adult | LOO | highest | 10 % | 3 | +0.0020 | [-0.0032, +0.0091] | 0.648 | 1/3 |
| models-random_forest-clean | adult | LOO | highest | 20 % | 3 | +0.0014 | [-0.0018, +0.0048] | 0.542 | 2/3 |
| models-random_forest-clean | adult | LOO | highest | 30 % | 3 | -0.0060 | [-0.0098, +0.0000] | 0.187 | 1/3 |
| models-random_forest-clean | adult | LOO | highest | auc | 3 | +0.0001 | [-0.0023, +0.0040] | 0.978 | 1/3 |
| models-random_forest-clean | adult | LossHigh | lowest | 5 % | 3 | -0.0023 | [-0.0076, +0.0077] | 0.696 | 1/3 |
| models-random_forest-clean | adult | LossHigh | lowest | 10 % | 3 | -0.0066 | [-0.0104, -0.0018] | 0.120 | 0/3 |
| models-random_forest-clean | adult | LossHigh | lowest | 20 % | 3 | -0.0176 | [-0.0198, -0.0157] | 0.005 | 0/3 |
| models-random_forest-clean | adult | LossHigh | lowest | 30 % | 3 | -0.0395 | [-0.0488, -0.0288] | 0.021 | 0/3 |
| models-random_forest-clean | adult | LossHigh | lowest | auc | 3 | -0.0145 | [-0.0156, -0.0125] | 0.005 | 0/3 |
| models-random_forest-clean | adult | LossHigh | highest | 5 % | 3 | +0.0022 | [-0.0008, +0.0058] | 0.378 | 2/3 |
| models-random_forest-clean | adult | LossHigh | highest | 10 % | 3 | +0.0032 | [-0.0014, +0.0062] | 0.309 | 2/3 |
| models-random_forest-clean | adult | LossHigh | highest | 20 % | 3 | +0.0004 | [-0.0033, +0.0044] | 0.869 | 2/3 |
| models-random_forest-clean | adult | LossHigh | highest | 30 % | 3 | +0.0026 | [-0.0086, +0.0088] | 0.684 | 2/3 |
| models-random_forest-clean | adult | LossHigh | highest | auc | 3 | +0.0017 | [-0.0019, +0.0049] | 0.473 | 2/3 |
| models-random_forest-clean | covertype | DataOOB | lowest | 5 % | 3 | -0.0023 | [-0.0094, +0.0030] | 0.591 | 1/3 |
| models-random_forest-clean | covertype | DataOOB | lowest | 10 % | 3 | +0.0004 | [-0.0032, +0.0030] | 0.850 | 2/3 |
| models-random_forest-clean | covertype | DataOOB | lowest | 20 % | 3 | -0.0025 | [-0.0066, +0.0044] | 0.550 | 1/3 |
| models-random_forest-clean | covertype | DataOOB | lowest | 30 % | 3 | +0.0009 | [-0.0056, +0.0044] | 0.802 | 2/3 |
| models-random_forest-clean | covertype | DataOOB | lowest | auc | 3 | -0.0010 | [-0.0050, +0.0035] | 0.735 | 1/3 |
| models-random_forest-clean | covertype | DataOOB | highest | 5 % | 3 | +0.0010 | [-0.0074, +0.0090] | 0.852 | 2/3 |
| models-random_forest-clean | covertype | DataOOB | highest | 10 % | 3 | +0.0015 | [-0.0008, +0.0042] | 0.402 | 2/3 |
| models-random_forest-clean | covertype | DataOOB | highest | 20 % | 3 | -0.0021 | [-0.0090, +0.0028] | 0.608 | 1/3 |
| models-random_forest-clean | covertype | DataOOB | highest | 30 % | 3 | -0.0021 | [-0.0136, +0.0068] | 0.765 | 2/3 |
| models-random_forest-clean | covertype | DataOOB | highest | auc | 3 | -0.0005 | [-0.0067, +0.0039] | 0.888 | 2/3 |
| models-random_forest-clean | covertype | KNNShapley | lowest | 5 % | 3 | -0.0026 | [-0.0106, +0.0020] | 0.584 | 2/3 |
| models-random_forest-clean | covertype | KNNShapley | lowest | 10 % | 3 | +0.0014 | [-0.0018, +0.0036] | 0.483 | 2/3 |
| models-random_forest-clean | covertype | KNNShapley | lowest | 20 % | 3 | -0.0110 | [-0.0228, -0.0024] | 0.213 | 0/3 |
| models-random_forest-clean | covertype | KNNShapley | lowest | 30 % | 3 | -0.0164 | [-0.0242, -0.0048] | 0.109 | 0/3 |
| models-random_forest-clean | covertype | KNNShapley | lowest | auc | 3 | -0.0065 | [-0.0120, -0.0007] | 0.185 | 0/3 |
| models-random_forest-clean | covertype | KNNShapley | highest | 5 % | 3 | -0.0025 | [-0.0066, +0.0020] | 0.417 | 1/3 |
| models-random_forest-clean | covertype | KNNShapley | highest | 10 % | 3 | -0.0110 | [-0.0168, -0.0038] | 0.102 | 0/3 |
| models-random_forest-clean | covertype | KNNShapley | highest | 20 % | 3 | -0.0287 | [-0.0456, -0.0142] | 0.088 | 0/3 |
| models-random_forest-clean | covertype | KNNShapley | highest | 30 % | 3 | -0.0537 | [-0.0658, -0.0372] | 0.024 | 0/3 |
| models-random_forest-clean | covertype | KNNShapley | highest | auc | 3 | -0.0217 | [-0.0315, -0.0116] | 0.064 | 0/3 |
| models-random_forest-clean | covertype | LOO | lowest | 5 % | 3 | -0.0032 | [-0.0064, +0.0014] | 0.308 | 1/3 |
| models-random_forest-clean | covertype | LOO | lowest | 10 % | 3 | +0.0036 | [+0.0014, +0.0060] | 0.114 | 3/3 |
| models-random_forest-clean | covertype | LOO | lowest | 20 % | 3 | -0.0029 | [-0.0076, +0.0012] | 0.380 | 1/3 |
| models-random_forest-clean | covertype | LOO | lowest | 30 % | 3 | +0.0009 | [-0.0066, +0.0062] | 0.843 | 2/3 |
| models-random_forest-clean | covertype | LOO | lowest | auc | 3 | -0.0004 | [-0.0041, +0.0032] | 0.851 | 1/3 |
| models-random_forest-clean | covertype | LOO | highest | 5 % | 3 | -0.0031 | [-0.0094, +0.0014] | 0.446 | 1/3 |
| models-random_forest-clean | covertype | LOO | highest | 10 % | 3 | -0.0013 | [-0.0026, +0.0004] | 0.287 | 1/3 |
| models-random_forest-clean | covertype | LOO | highest | 20 % | 3 | -0.0014 | [-0.0064, +0.0064] | 0.757 | 1/3 |
| models-random_forest-clean | covertype | LOO | highest | 30 % | 3 | +0.0027 | [-0.0014, +0.0108] | 0.568 | 1/3 |
| models-random_forest-clean | covertype | LOO | highest | auc | 3 | -0.0008 | [-0.0038, +0.0023] | 0.682 | 1/3 |
| models-random_forest-clean | covertype | LossHigh | lowest | 5 % | 3 | -0.0022 | [-0.0078, +0.0008] | 0.515 | 2/3 |
| models-random_forest-clean | covertype | LossHigh | lowest | 10 % | 3 | -0.0015 | [-0.0038, +0.0008] | 0.368 | 1/3 |
| models-random_forest-clean | covertype | LossHigh | lowest | 20 % | 3 | -0.0022 | [-0.0080, +0.0036] | 0.579 | 1/3 |
| models-random_forest-clean | covertype | LossHigh | lowest | 30 % | 3 | -0.0007 | [-0.0060, +0.0050] | 0.839 | 1/3 |
| models-random_forest-clean | covertype | LossHigh | lowest | auc | 3 | -0.0016 | [-0.0059, +0.0013] | 0.541 | 1/3 |
| models-random_forest-clean | covertype | LossHigh | highest | 5 % | 3 | +0.0005 | [-0.0062, +0.0104] | 0.925 | 1/3 |
| models-random_forest-clean | covertype | LossHigh | highest | 10 % | 3 | +0.0009 | [-0.0028, +0.0076] | 0.821 | 1/3 |
| models-random_forest-clean | covertype | LossHigh | highest | 20 % | 3 | +0.0029 | [-0.0034, +0.0148] | 0.678 | 1/3 |
| models-random_forest-clean | covertype | LossHigh | highest | 30 % | 3 | -0.0458 | [-0.0628, -0.0288] | 0.043 | 0/3 |
| models-random_forest-clean | covertype | LossHigh | highest | auc | 3 | -0.0064 | [-0.0124, +0.0038] | 0.338 | 1/3 |
| models-random_forest-clean | housing | DataOOB | lowest | 5 % | 3 | +208.7462 | [-919.1521, +1518.4847] | 0.796 | 2/3 |
| models-random_forest-clean | housing | DataOOB | lowest | 10 % | 3 | -238.0681 | [-1241.3526, +286.2113] | 0.682 | 2/3 |
| models-random_forest-clean | housing | DataOOB | lowest | 20 % | 3 | -669.4925 | [-1082.5239, -390.8327] | 0.086 | 0/3 |
| models-random_forest-clean | housing | DataOOB | lowest | 30 % | 3 | -874.7459 | [-2319.2484, +136.7435] | 0.359 | 1/3 |
| models-random_forest-clean | housing | DataOOB | lowest | auc | 3 | -393.6811 | [-1210.9129, +217.1466] | 0.452 | 1/3 |
| models-random_forest-clean | housing | DataOOB | highest | 5 % | 3 | +245.0822 | [-180.9258, +864.2936] | 0.520 | 2/3 |
| models-random_forest-clean | housing | DataOOB | highest | 10 % | 3 | +249.6784 | [-28.6870, +773.8800] | 0.442 | 2/3 |
| models-random_forest-clean | housing | DataOOB | highest | 20 % | 3 | -28.5675 | [-292.4411, +437.8070] | 0.914 | 1/3 |
| models-random_forest-clean | housing | DataOOB | highest | 30 % | 3 | -1766.2974 | [-2420.6059, -828.6050] | 0.067 | 0/3 |
| models-random_forest-clean | housing | DataOOB | highest | auc | 3 | -200.6387 | [-364.0375, -21.3589] | 0.181 | 0/3 |
| models-random_forest-clean | housing | LOO | lowest | 5 % | 3 | +224.5203 | [-425.4063, +725.7269] | 0.577 | 2/3 |
| models-random_forest-clean | housing | LOO | lowest | 10 % | 3 | +470.7105 | [-305.1743, +1050.2038] | 0.364 | 2/3 |
| models-random_forest-clean | housing | LOO | lowest | 20 % | 3 | +1078.6055 | [+523.7084, +1370.6051] | 0.060 | 3/3 |
| models-random_forest-clean | housing | LOO | lowest | 30 % | 3 | +1100.8980 | [+519.1682, +1807.7354] | 0.100 | 3/3 |
| models-random_forest-clean | housing | LOO | lowest | auc | 3 | +698.1158 | [+113.9029, +1131.9623] | 0.148 | 3/3 |
| models-random_forest-clean | housing | LOO | highest | 5 % | 3 | -180.6589 | [-482.1986, +104.5801] | 0.398 | 1/3 |
| models-random_forest-clean | housing | LOO | highest | 10 % | 3 | -360.1184 | [-577.9902, -245.3563] | 0.081 | 0/3 |
| models-random_forest-clean | housing | LOO | highest | 20 % | 3 | +124.2874 | [-263.2440, +435.4885] | 0.606 | 2/3 |
| models-random_forest-clean | housing | LOO | highest | 30 % | 3 | -440.7160 | [-1973.5825, +603.0759] | 0.630 | 2/3 |
| models-random_forest-clean | housing | LOO | highest | auc | 3 | -152.1629 | [-486.9218, +156.9434] | 0.500 | 1/3 |
| models-random_forest-clean | housing | LossHigh | lowest | 5 % | 3 | +110.5213 | [-979.8058, +1023.3594] | 0.868 | 2/3 |
| models-random_forest-clean | housing | LossHigh | lowest | 10 % | 3 | +10.5535 | [-793.0589, +555.1236] | 0.982 | 2/3 |
| models-random_forest-clean | housing | LossHigh | lowest | 20 % | 3 | -385.9348 | [-594.2256, -52.5705] | 0.149 | 0/3 |
| models-random_forest-clean | housing | LossHigh | lowest | 30 % | 3 | -474.9145 | [-1162.4071, +629.9097] | 0.484 | 1/3 |
| models-random_forest-clean | housing | LossHigh | lowest | auc | 3 | -186.7387 | [-725.6363, +202.8621] | 0.571 | 1/3 |
| models-random_forest-clean | housing | LossHigh | highest | 5 % | 3 | +254.6572 | [+112.3677, +438.2723] | 0.118 | 3/3 |
| models-random_forest-clean | housing | LossHigh | highest | 10 % | 3 | +664.5707 | [+407.4806, +1164.7464] | 0.117 | 3/3 |
| models-random_forest-clean | housing | LossHigh | highest | 20 % | 3 | +1689.3590 | [+1430.3959, +1863.1533] | 0.006 | 3/3 |
| models-random_forest-clean | housing | LossHigh | highest | 30 % | 3 | +1600.0881 | [+1114.4939, +2417.5348] | 0.060 | 3/3 |
| models-random_forest-clean | housing | LossHigh | highest | auc | 3 | +1038.3866 | [+863.0868, +1304.3463] | 0.017 | 3/3 |
| models-random_forest-clean | wine | DataOOB | lowest | 5 % | 3 | +0.0020 | [-0.0166, +0.0239] | 0.881 | 1/3 |
| models-random_forest-clean | wine | DataOOB | lowest | 10 % | 3 | -0.0144 | [-0.0301, -0.0033] | 0.217 | 0/3 |
| models-random_forest-clean | wine | DataOOB | lowest | 20 % | 3 | -0.0075 | [-0.0407, +0.0261] | 0.735 | 1/3 |
| models-random_forest-clean | wine | DataOOB | lowest | 30 % | 3 | +0.0039 | [-0.0187, +0.0235] | 0.780 | 2/3 |
| models-random_forest-clean | wine | DataOOB | lowest | auc | 3 | -0.0051 | [-0.0270, +0.0114] | 0.697 | 2/3 |
| models-random_forest-clean | wine | DataOOB | highest | 5 % | 3 | +0.0053 | [-0.0077, +0.0202] | 0.580 | 2/3 |
| models-random_forest-clean | wine | DataOOB | highest | 10 % | 3 | -0.0199 | [-0.0245, -0.0155] | 0.017 | 0/3 |
| models-random_forest-clean | wine | DataOOB | highest | 20 % | 3 | -0.0276 | [-0.0402, -0.0157] | 0.060 | 0/3 |
| models-random_forest-clean | wine | DataOOB | highest | 30 % | 3 | -0.0542 | [-0.0646, -0.0451] | 0.011 | 0/3 |
| models-random_forest-clean | wine | DataOOB | highest | auc | 3 | -0.0223 | [-0.0284, -0.0188] | 0.018 | 0/3 |
| models-random_forest-clean | wine | LOO | lowest | 5 % | 3 | +0.0035 | [-0.0178, +0.0263] | 0.810 | 2/3 |
| models-random_forest-clean | wine | LOO | lowest | 10 % | 3 | -0.0015 | [-0.0173, +0.0093] | 0.866 | 2/3 |
| models-random_forest-clean | wine | LOO | lowest | 20 % | 3 | -0.0056 | [-0.0215, +0.0138] | 0.642 | 1/3 |
| models-random_forest-clean | wine | LOO | lowest | 30 % | 3 | -0.0017 | [-0.0043, +0.0034] | 0.566 | 1/3 |
| models-random_forest-clean | wine | LOO | lowest | auc | 3 | -0.0020 | [-0.0085, +0.0104] | 0.780 | 1/3 |
| models-random_forest-clean | wine | LOO | highest | 5 % | 3 | +0.0049 | [+0.0027, +0.0065] | 0.050 | 3/3 |
| models-random_forest-clean | wine | LOO | highest | 10 % | 3 | -0.0055 | [-0.0235, +0.0065] | 0.612 | 2/3 |
| models-random_forest-clean | wine | LOO | highest | 20 % | 3 | -0.0071 | [-0.0228, +0.0064] | 0.491 | 1/3 |
| models-random_forest-clean | wine | LOO | highest | 30 % | 3 | -0.0107 | [-0.0182, -0.0047] | 0.113 | 0/3 |
| models-random_forest-clean | wine | LOO | highest | auc | 3 | -0.0047 | [-0.0134, +0.0018] | 0.405 | 1/3 |
| models-random_forest-clean | wine | LossHigh | lowest | 5 % | 3 | -0.0046 | [-0.0251, +0.0153] | 0.734 | 1/3 |
| models-random_forest-clean | wine | LossHigh | lowest | 10 % | 3 | -0.0070 | [-0.0324, +0.0064] | 0.634 | 2/3 |
| models-random_forest-clean | wine | LossHigh | lowest | 20 % | 3 | +0.0041 | [-0.0117, +0.0225] | 0.722 | 2/3 |
| models-random_forest-clean | wine | LossHigh | lowest | 30 % | 3 | +0.0120 | [-0.0021, +0.0275] | 0.295 | 2/3 |
| models-random_forest-clean | wine | LossHigh | lowest | auc | 3 | +0.0008 | [-0.0165, +0.0159] | 0.937 | 2/3 |
| models-random_forest-clean | wine | LossHigh | highest | 5 % | 3 | -0.0059 | [-0.0215, +0.0094] | 0.575 | 1/3 |
| models-random_forest-clean | wine | LossHigh | highest | 10 % | 3 | -0.0054 | [-0.0130, -0.0004] | 0.293 | 0/3 |
| models-random_forest-clean | wine | LossHigh | highest | 20 % | 3 | -0.0260 | [-0.0393, -0.0062] | 0.124 | 0/3 |
| models-random_forest-clean | wine | LossHigh | highest | 30 % | 3 | -0.0421 | [-0.0650, -0.0235] | 0.074 | 0/3 |
| models-random_forest-clean | wine | LossHigh | highest | auc | 3 | -0.0180 | [-0.0238, -0.0114] | 0.037 | 0/3 |
| models-random_forest-noise10 | adult | DataOOB | lowest | 5 % | 3 | -0.0005 | [-0.0010, +0.0000] | 0.268 | 0/3 |
| models-random_forest-noise10 | adult | DataOOB | lowest | 10 % | 3 | -0.0051 | [-0.0094, -0.0019] | 0.152 | 0/3 |
| models-random_forest-noise10 | adult | DataOOB | lowest | 20 % | 3 | -0.0050 | [-0.0085, -0.0022] | 0.119 | 0/3 |
| models-random_forest-noise10 | adult | DataOOB | lowest | auc | 3 | -0.0033 | [-0.0058, -0.0020] | 0.120 | 0/3 |
| models-random_forest-noise10 | adult | KNNShapley | lowest | 5 % | 3 | -0.0020 | [-0.0036, -0.0004] | 0.156 | 0/3 |
| models-random_forest-noise10 | adult | KNNShapley | lowest | 10 % | 3 | -0.0013 | [-0.0093, +0.0090] | 0.835 | 1/3 |
| models-random_forest-noise10 | adult | KNNShapley | lowest | 20 % | 3 | -0.0132 | [-0.0166, -0.0069] | 0.053 | 0/3 |
| models-random_forest-noise10 | adult | KNNShapley | lowest | auc | 3 | -0.0043 | [-0.0081, +0.0016] | 0.285 | 1/3 |
| models-random_forest-noise10 | adult | LOO | lowest | 5 % | 3 | -0.0010 | [-0.0073, +0.0039] | 0.791 | 2/3 |
| models-random_forest-noise10 | adult | LOO | lowest | 10 % | 3 | -0.0036 | [-0.0113, +0.0098] | 0.648 | 1/3 |
| models-random_forest-noise10 | adult | LOO | lowest | 20 % | 3 | -0.0004 | [-0.0090, +0.0067] | 0.931 | 2/3 |
| models-random_forest-noise10 | adult | LOO | lowest | auc | 3 | -0.0017 | [-0.0056, +0.0049] | 0.659 | 1/3 |
| models-random_forest-noise10 | adult | LossHigh | lowest | 5 % | 3 | -0.0028 | [-0.0062, +0.0000] | 0.267 | 0/3 |
| models-random_forest-noise10 | adult | LossHigh | lowest | 10 % | 3 | -0.0115 | [-0.0214, -0.0025] | 0.170 | 0/3 |
| models-random_forest-noise10 | adult | LossHigh | lowest | 20 % | 3 | -0.0163 | [-0.0245, -0.0074] | 0.081 | 0/3 |
| models-random_forest-noise10 | adult | LossHigh | lowest | auc | 3 | -0.0091 | [-0.0128, -0.0028] | 0.102 | 0/3 |
| models-random_forest-noise10 | covertype | DataOOB | lowest | 5 % | 3 | +0.0021 | [-0.0042, +0.0084] | 0.627 | 2/3 |
| models-random_forest-noise10 | covertype | DataOOB | lowest | 10 % | 3 | +0.0068 | [+0.0026, +0.0090] | 0.084 | 3/3 |
| models-random_forest-noise10 | covertype | DataOOB | lowest | 20 % | 3 | +0.0116 | [+0.0038, +0.0200] | 0.132 | 3/3 |
| models-random_forest-noise10 | covertype | DataOOB | lowest | auc | 3 | +0.0060 | [+0.0027, +0.0088] | 0.079 | 3/3 |
| models-random_forest-noise10 | covertype | KNNShapley | lowest | 5 % | 3 | -0.0014 | [-0.0072, +0.0026] | 0.684 | 2/3 |
| models-random_forest-noise10 | covertype | KNNShapley | lowest | 10 % | 3 | +0.0035 | [-0.0060, +0.0082] | 0.540 | 2/3 |
| models-random_forest-noise10 | covertype | KNNShapley | lowest | 20 % | 3 | -0.0015 | [-0.0162, +0.0064] | 0.854 | 2/3 |
| models-random_forest-noise10 | covertype | KNNShapley | lowest | auc | 3 | +0.0006 | [-0.0081, +0.0053] | 0.908 | 2/3 |
| models-random_forest-noise10 | covertype | LOO | lowest | 5 % | 3 | -0.0043 | [-0.0052, -0.0034] | 0.015 | 0/3 |
| models-random_forest-noise10 | covertype | LOO | lowest | 10 % | 3 | +0.0028 | [+0.0000, +0.0082] | 0.409 | 2/3 |
| models-random_forest-noise10 | covertype | LOO | lowest | 20 % | 3 | +0.0101 | [+0.0032, +0.0214] | 0.220 | 3/3 |
| models-random_forest-noise10 | covertype | LOO | lowest | auc | 3 | +0.0025 | [-0.0005, +0.0074] | 0.416 | 2/3 |
| models-random_forest-noise10 | covertype | LossHigh | lowest | 5 % | 3 | -0.0011 | [-0.0080, +0.0060] | 0.817 | 1/3 |
| models-random_forest-noise10 | covertype | LossHigh | lowest | 10 % | 3 | +0.0073 | [+0.0042, +0.0104] | 0.055 | 3/3 |
| models-random_forest-noise10 | covertype | LossHigh | lowest | 20 % | 3 | +0.0069 | [+0.0026, +0.0094] | 0.086 | 3/3 |
| models-random_forest-noise10 | covertype | LossHigh | lowest | auc | 3 | +0.0042 | [+0.0031, +0.0053] | 0.021 | 3/3 |
| models-random_forest-noise10 | housing | DataOOB | lowest | 5 % | 3 | +1258.1091 | [+724.3347, +1981.0687] | 0.078 | 3/3 |
| models-random_forest-noise10 | housing | DataOOB | lowest | 10 % | 3 | +6252.7464 | [+5199.7431, +6819.9581] | 0.007 | 3/3 |
| models-random_forest-noise10 | housing | DataOOB | lowest | 20 % | 3 | +6681.5103 | [+4686.1439, +8041.1264] | 0.022 | 3/3 |
| models-random_forest-noise10 | housing | DataOOB | lowest | auc | 3 | +4329.6848 | [+3388.6706, +4882.0666] | 0.012 | 3/3 |
| models-random_forest-noise10 | housing | LOO | lowest | 5 % | 3 | +1361.3380 | [+778.5380, +2133.3118] | 0.077 | 3/3 |
| models-random_forest-noise10 | housing | LOO | lowest | 10 % | 3 | +573.5562 | [+254.9021, +1199.2199] | 0.208 | 3/3 |
| models-random_forest-noise10 | housing | LOO | lowest | 20 % | 3 | +1248.7082 | [+309.8583, +2197.1147] | 0.149 | 3/3 |
| models-random_forest-noise10 | housing | LOO | lowest | auc | 3 | +867.5951 | [+466.0939, +1292.8234] | 0.068 | 3/3 |
| models-random_forest-noise10 | housing | LossHigh | lowest | 5 % | 3 | +843.0887 | [+239.6066, +1702.5913] | 0.196 | 3/3 |
| models-random_forest-noise10 | housing | LossHigh | lowest | 10 % | 3 | +5707.4811 | [+4287.0395, +7136.0675] | 0.020 | 3/3 |
| models-random_forest-noise10 | housing | LossHigh | lowest | 20 % | 3 | +5974.2763 | [+4404.6851, +7071.2955] | 0.018 | 3/3 |
| models-random_forest-noise10 | housing | LossHigh | lowest | auc | 3 | +3844.6467 | [+2855.5782, +4713.3852] | 0.019 | 3/3 |
| models-random_forest-noise10 | wine | DataOOB | lowest | 5 % | 3 | +0.0172 | [-0.0138, +0.0388] | 0.393 | 2/3 |
| models-random_forest-noise10 | wine | DataOOB | lowest | 10 % | 3 | +0.0445 | [-0.0000, +0.0863] | 0.217 | 2/3 |
| models-random_forest-noise10 | wine | DataOOB | lowest | 20 % | 3 | +0.0396 | [+0.0131, +0.0564] | 0.098 | 3/3 |
| models-random_forest-noise10 | wine | DataOOB | lowest | auc | 3 | +0.0308 | [+0.0099, +0.0544] | 0.139 | 3/3 |
| models-random_forest-noise10 | wine | LOO | lowest | 5 % | 3 | +0.0006 | [-0.0195, +0.0165] | 0.961 | 2/3 |
| models-random_forest-noise10 | wine | LOO | lowest | 10 % | 3 | -0.0013 | [-0.0500, +0.0398] | 0.965 | 2/3 |
| models-random_forest-noise10 | wine | LOO | lowest | 20 % | 3 | +0.0135 | [-0.0278, +0.0426] | 0.590 | 2/3 |
| models-random_forest-noise10 | wine | LOO | lowest | auc | 3 | +0.0030 | [-0.0245, +0.0297] | 0.864 | 2/3 |
| models-random_forest-noise10 | wine | LossHigh | lowest | 5 % | 3 | +0.0202 | [-0.0158, +0.0385] | 0.378 | 2/3 |
| models-random_forest-noise10 | wine | LossHigh | lowest | 10 % | 3 | +0.0299 | [+0.0138, +0.0522] | 0.122 | 3/3 |
| models-random_forest-noise10 | wine | LossHigh | lowest | 20 % | 3 | +0.0398 | [+0.0167, +0.0526] | 0.075 | 3/3 |
| models-random_forest-noise10 | wine | LossHigh | lowest | auc | 3 | +0.0262 | [+0.0175, +0.0422] | 0.082 | 3/3 |
| models-xgboost-clean | adult | DataOOB | lowest | 5 % | 3 | +0.0138 | [-0.0014, +0.0346] | 0.328 | 2/3 |
| models-xgboost-clean | adult | DataOOB | lowest | 10 % | 3 | +0.0166 | [+0.0039, +0.0298] | 0.156 | 3/3 |
| models-xgboost-clean | adult | DataOOB | lowest | 20 % | 3 | +0.0193 | [+0.0054, +0.0289] | 0.113 | 3/3 |
| models-xgboost-clean | adult | DataOOB | lowest | 30 % | 3 | +0.0192 | [-0.0013, +0.0381] | 0.234 | 2/3 |
| models-xgboost-clean | adult | DataOOB | lowest | auc | 3 | +0.0161 | [+0.0039, +0.0263] | 0.133 | 3/3 |
| models-xgboost-clean | adult | DataOOB | highest | 5 % | 3 | +0.0030 | [-0.0104, +0.0126] | 0.709 | 2/3 |
| models-xgboost-clean | adult | DataOOB | highest | 10 % | 3 | -0.0109 | [-0.0143, -0.0078] | 0.028 | 0/3 |
| models-xgboost-clean | adult | DataOOB | highest | 20 % | 3 | -0.0180 | [-0.0277, -0.0121] | 0.066 | 0/3 |
| models-xgboost-clean | adult | DataOOB | highest | 30 % | 3 | -0.0274 | [-0.0321, -0.0235] | 0.008 | 0/3 |
| models-xgboost-clean | adult | DataOOB | highest | auc | 3 | -0.0128 | [-0.0161, -0.0107] | 0.017 | 0/3 |
| models-xgboost-clean | adult | KNNShapley | lowest | 5 % | 3 | +0.0172 | [+0.0111, +0.0260] | 0.062 | 3/3 |
| models-xgboost-clean | adult | KNNShapley | lowest | 10 % | 3 | +0.0147 | [-0.0032, +0.0345] | 0.312 | 2/3 |
| models-xgboost-clean | adult | KNNShapley | lowest | 20 % | 3 | +0.0038 | [-0.0147, +0.0180] | 0.731 | 2/3 |
| models-xgboost-clean | adult | KNNShapley | lowest | 30 % | 3 | -0.0081 | [-0.0378, +0.0079] | 0.638 | 2/3 |
| models-xgboost-clean | adult | KNNShapley | lowest | auc | 3 | +0.0065 | [-0.0102, +0.0184] | 0.530 | 2/3 |
| models-xgboost-clean | adult | KNNShapley | highest | 5 % | 3 | -0.0109 | [-0.0291, +0.0024] | 0.369 | 1/3 |
| models-xgboost-clean | adult | KNNShapley | highest | 10 % | 3 | -0.0150 | [-0.0258, +0.0028] | 0.237 | 1/3 |
| models-xgboost-clean | adult | KNNShapley | highest | 20 % | 3 | -0.0436 | [-0.0637, -0.0246] | 0.061 | 0/3 |
| models-xgboost-clean | adult | KNNShapley | highest | 30 % | 3 | -0.0720 | [-0.0955, -0.0543] | 0.028 | 0/3 |
| models-xgboost-clean | adult | KNNShapley | highest | auc | 3 | -0.0321 | [-0.0484, -0.0161] | 0.075 | 0/3 |
| models-xgboost-clean | adult | LOO | lowest | 5 % | 3 | -0.0045 | [-0.0113, +0.0071] | 0.524 | 1/3 |
| models-xgboost-clean | adult | LOO | lowest | 10 % | 3 | -0.0021 | [-0.0188, +0.0083] | 0.822 | 2/3 |
| models-xgboost-clean | adult | LOO | lowest | 20 % | 3 | -0.0021 | [-0.0206, +0.0086] | 0.840 | 2/3 |
| models-xgboost-clean | adult | LOO | lowest | 30 % | 3 | -0.0048 | [-0.0173, +0.0053] | 0.543 | 1/3 |
| models-xgboost-clean | adult | LOO | lowest | auc | 3 | -0.0028 | [-0.0163, +0.0043] | 0.720 | 2/3 |
| models-xgboost-clean | adult | LOO | highest | 5 % | 3 | -0.0046 | [-0.0260, +0.0156] | 0.740 | 1/3 |
| models-xgboost-clean | adult | LOO | highest | 10 % | 3 | +0.0037 | [-0.0130, +0.0230] | 0.756 | 2/3 |
| models-xgboost-clean | adult | LOO | highest | 20 % | 3 | -0.0044 | [-0.0095, +0.0045] | 0.430 | 1/3 |
| models-xgboost-clean | adult | LOO | highest | 30 % | 3 | -0.0156 | [-0.0194, -0.0120] | 0.018 | 0/3 |
| models-xgboost-clean | adult | LOO | highest | auc | 3 | -0.0039 | [-0.0095, +0.0037] | 0.427 | 1/3 |
| models-xgboost-clean | adult | LossHigh | lowest | 5 % | 3 | +0.0127 | [+0.0033, +0.0187] | 0.116 | 3/3 |
| models-xgboost-clean | adult | LossHigh | lowest | 10 % | 3 | +0.0227 | [+0.0190, +0.0250] | 0.006 | 3/3 |
| models-xgboost-clean | adult | LossHigh | lowest | 20 % | 3 | +0.0184 | [+0.0053, +0.0354] | 0.174 | 3/3 |
| models-xgboost-clean | adult | LossHigh | lowest | 30 % | 3 | +0.0214 | [+0.0055, +0.0388] | 0.157 | 3/3 |
| models-xgboost-clean | adult | LossHigh | lowest | auc | 3 | +0.0175 | [+0.0101, +0.0248] | 0.054 | 3/3 |
| models-xgboost-clean | adult | LossHigh | highest | 5 % | 3 | -0.0013 | [-0.0151, +0.0148] | 0.892 | 1/3 |
| models-xgboost-clean | adult | LossHigh | highest | 10 % | 3 | -0.0040 | [-0.0067, -0.0002] | 0.175 | 0/3 |
| models-xgboost-clean | adult | LossHigh | highest | 20 % | 3 | +0.0001 | [-0.0092, +0.0113] | 0.984 | 1/3 |
| models-xgboost-clean | adult | LossHigh | highest | 30 % | 3 | +0.0004 | [-0.0063, +0.0054] | 0.915 | 2/3 |
| models-xgboost-clean | adult | LossHigh | highest | auc | 3 | -0.0011 | [-0.0064, +0.0027] | 0.725 | 2/3 |
| models-xgboost-clean | covertype | DataOOB | lowest | 5 % | 3 | +0.0053 | [+0.0008, +0.0088] | 0.153 | 3/3 |
| models-xgboost-clean | covertype | DataOOB | lowest | 10 % | 3 | +0.0082 | [+0.0018, +0.0128] | 0.131 | 3/3 |
| models-xgboost-clean | covertype | DataOOB | lowest | 20 % | 3 | +0.0077 | [+0.0044, +0.0120] | 0.077 | 3/3 |
| models-xgboost-clean | covertype | DataOOB | lowest | 30 % | 3 | +0.0047 | [-0.0046, +0.0112] | 0.430 | 2/3 |
| models-xgboost-clean | covertype | DataOOB | lowest | auc | 3 | +0.0063 | [+0.0050, +0.0080] | 0.021 | 3/3 |
| models-xgboost-clean | covertype | DataOOB | highest | 5 % | 3 | -0.0032 | [-0.0072, +0.0006] | 0.292 | 1/3 |
| models-xgboost-clean | covertype | DataOOB | highest | 10 % | 3 | +0.0027 | [-0.0066, +0.0096] | 0.636 | 2/3 |
| models-xgboost-clean | covertype | DataOOB | highest | 20 % | 3 | -0.0085 | [-0.0146, -0.0038] | 0.116 | 0/3 |
| models-xgboost-clean | covertype | DataOOB | highest | 30 % | 3 | -0.0237 | [-0.0318, -0.0142] | 0.044 | 0/3 |
| models-xgboost-clean | covertype | DataOOB | highest | auc | 3 | -0.0067 | [-0.0123, -0.0034] | 0.143 | 0/3 |
| models-xgboost-clean | covertype | KNNShapley | lowest | 5 % | 3 | +0.0051 | [+0.0008, +0.0080] | 0.146 | 3/3 |
| models-xgboost-clean | covertype | KNNShapley | lowest | 10 % | 3 | +0.0136 | [+0.0130, +0.0140] | 0.001 | 3/3 |
| models-xgboost-clean | covertype | KNNShapley | lowest | 20 % | 3 | +0.0057 | [+0.0026, +0.0090] | 0.090 | 3/3 |
| models-xgboost-clean | covertype | KNNShapley | lowest | 30 % | 3 | +0.0033 | [-0.0020, +0.0112] | 0.494 | 2/3 |
| models-xgboost-clean | covertype | KNNShapley | lowest | auc | 3 | +0.0067 | [+0.0055, +0.0085] | 0.018 | 3/3 |
| models-xgboost-clean | covertype | KNNShapley | highest | 5 % | 3 | -0.0043 | [-0.0096, -0.0008] | 0.248 | 0/3 |
| models-xgboost-clean | covertype | KNNShapley | highest | 10 % | 3 | -0.0077 | [-0.0146, -0.0022] | 0.171 | 0/3 |
| models-xgboost-clean | covertype | KNNShapley | highest | 20 % | 3 | -0.0210 | [-0.0304, -0.0140] | 0.050 | 0/3 |
| models-xgboost-clean | covertype | KNNShapley | highest | 30 % | 3 | -0.0419 | [-0.0522, -0.0360] | 0.015 | 0/3 |
| models-xgboost-clean | covertype | KNNShapley | highest | auc | 3 | -0.0166 | [-0.0214, -0.0116] | 0.028 | 0/3 |
| models-xgboost-clean | covertype | LOO | lowest | 5 % | 3 | -0.0043 | [-0.0112, +0.0048] | 0.458 | 1/3 |
| models-xgboost-clean | covertype | LOO | lowest | 10 % | 3 | +0.0021 | [-0.0042, +0.0058] | 0.579 | 2/3 |
| models-xgboost-clean | covertype | LOO | lowest | 20 % | 3 | +0.0027 | [+0.0012, +0.0042] | 0.088 | 3/3 |
| models-xgboost-clean | covertype | LOO | lowest | 30 % | 3 | +0.0003 | [-0.0098, +0.0090] | 0.957 | 2/3 |
| models-xgboost-clean | covertype | LOO | lowest | auc | 3 | +0.0008 | [-0.0015, +0.0044] | 0.717 | 1/3 |
| models-xgboost-clean | covertype | LOO | highest | 5 % | 3 | -0.0022 | [-0.0070, +0.0034] | 0.543 | 1/3 |
| models-xgboost-clean | covertype | LOO | highest | 10 % | 3 | +0.0035 | [-0.0028, +0.0102] | 0.454 | 2/3 |
| models-xgboost-clean | covertype | LOO | highest | 20 % | 3 | -0.0021 | [-0.0060, +0.0016] | 0.446 | 1/3 |
| models-xgboost-clean | covertype | LOO | highest | 30 % | 3 | +0.0019 | [-0.0040, +0.0100] | 0.700 | 1/3 |
| models-xgboost-clean | covertype | LOO | highest | auc | 3 | +0.0001 | [-0.0015, +0.0024] | 0.928 | 1/3 |
| models-xgboost-clean | covertype | LossHigh | lowest | 5 % | 3 | +0.0007 | [-0.0010, +0.0036] | 0.662 | 1/3 |
| models-xgboost-clean | covertype | LossHigh | lowest | 10 % | 3 | +0.0068 | [+0.0026, +0.0118] | 0.127 | 3/3 |
| models-xgboost-clean | covertype | LossHigh | lowest | 20 % | 3 | +0.0048 | [-0.0012, +0.0104] | 0.289 | 2/3 |
| models-xgboost-clean | covertype | LossHigh | lowest | 30 % | 3 | +0.0067 | [+0.0010, +0.0118] | 0.165 | 3/3 |
| models-xgboost-clean | covertype | LossHigh | lowest | auc | 3 | +0.0045 | [+0.0030, +0.0072] | 0.076 | 3/3 |
| models-xgboost-clean | covertype | LossHigh | highest | 5 % | 3 | +0.0011 | [-0.0020, +0.0066] | 0.737 | 1/3 |
| models-xgboost-clean | covertype | LossHigh | highest | 10 % | 3 | +0.0025 | [+0.0012, +0.0034] | 0.065 | 3/3 |
| models-xgboost-clean | covertype | LossHigh | highest | 20 % | 3 | +0.0089 | [+0.0080, +0.0096] | 0.003 | 3/3 |
| models-xgboost-clean | covertype | LossHigh | highest | 30 % | 3 | +0.0045 | [-0.0014, +0.0114] | 0.348 | 2/3 |
| models-xgboost-clean | covertype | LossHigh | highest | auc | 3 | +0.0045 | [+0.0034, +0.0065] | 0.045 | 3/3 |
| models-xgboost-clean | housing | DataOOB | lowest | 5 % | 3 | +1555.7409 | [+540.7860, +3245.8323] | 0.209 | 3/3 |
| models-xgboost-clean | housing | DataOOB | lowest | 10 % | 3 | +1918.6824 | [+1090.7266, +2359.4049] | 0.044 | 3/3 |
| models-xgboost-clean | housing | DataOOB | lowest | 20 % | 3 | +509.9313 | [-687.6492, +1171.2130] | 0.485 | 2/3 |
| models-xgboost-clean | housing | DataOOB | lowest | 30 % | 3 | +86.4879 | [-1468.2441, +1671.8408] | 0.933 | 2/3 |
| models-xgboost-clean | housing | DataOOB | lowest | auc | 3 | +923.3525 | [+199.5438, +1744.8345] | 0.176 | 3/3 |
| models-xgboost-clean | housing | DataOOB | highest | 5 % | 3 | +58.0295 | [-663.2597, +1327.3412] | 0.936 | 1/3 |
| models-xgboost-clean | housing | DataOOB | highest | 10 % | 3 | -29.3207 | [-267.2008, +197.7332] | 0.847 | 1/3 |
| models-xgboost-clean | housing | DataOOB | highest | 20 % | 3 | -43.6662 | [-1076.8493, +1179.5069] | 0.953 | 1/3 |
| models-xgboost-clean | housing | DataOOB | highest | 30 % | 3 | -576.4939 | [-1391.0583, +421.4354] | 0.391 | 1/3 |
| models-xgboost-clean | housing | DataOOB | highest | auc | 3 | -108.2963 | [-466.0540, +129.0937] | 0.612 | 2/3 |
| models-xgboost-clean | housing | LOO | lowest | 5 % | 3 | -148.8645 | [-1058.5480, +385.6321] | 0.776 | 2/3 |
| models-xgboost-clean | housing | LOO | lowest | 10 % | 3 | +861.0602 | [+56.1890, +1759.7178] | 0.223 | 3/3 |
| models-xgboost-clean | housing | LOO | lowest | 20 % | 3 | +1048.7353 | [+56.8065, +2009.0841] | 0.204 | 3/3 |
| models-xgboost-clean | housing | LOO | lowest | 30 % | 3 | +352.1699 | [+18.0193, +744.4509] | 0.238 | 3/3 |
| models-xgboost-clean | housing | LOO | lowest | auc | 3 | +598.7277 | [-19.3668, +1222.9028] | 0.237 | 2/3 |
| models-xgboost-clean | housing | LOO | highest | 5 % | 3 | -97.6023 | [-312.8816, +317.1320] | 0.684 | 1/3 |
| models-xgboost-clean | housing | LOO | highest | 10 % | 3 | -220.8531 | [-885.0223, +465.3064] | 0.628 | 1/3 |
| models-xgboost-clean | housing | LOO | highest | 20 % | 3 | +452.3707 | [-538.3639, +1588.3201] | 0.540 | 2/3 |
| models-xgboost-clean | housing | LOO | highest | 30 % | 3 | +256.4523 | [-310.2872, +771.1905] | 0.499 | 2/3 |
| models-xgboost-clean | housing | LOO | highest | auc | 3 | +122.0520 | [-116.9709, +364.8677] | 0.473 | 2/3 |
| models-xgboost-clean | housing | LossHigh | lowest | 5 % | 3 | +1230.5084 | [+600.5175, +2270.5333] | 0.143 | 3/3 |
| models-xgboost-clean | housing | LossHigh | lowest | 10 % | 3 | +1551.6381 | [+1134.3909, +1944.3746] | 0.022 | 3/3 |
| models-xgboost-clean | housing | LossHigh | lowest | 20 % | 3 | +1696.4288 | [+592.7273, +2483.8639] | 0.096 | 3/3 |
| models-xgboost-clean | housing | LossHigh | lowest | 30 % | 3 | +2141.1453 | [+400.1154, +3603.7705] | 0.149 | 3/3 |
| models-xgboost-clean | housing | LossHigh | lowest | auc | 3 | +1515.3281 | [+984.5181, +2201.0425] | 0.052 | 3/3 |
| models-xgboost-clean | housing | LossHigh | highest | 5 % | 3 | +393.3166 | [+318.3908, +451.7145] | 0.010 | 3/3 |
| models-xgboost-clean | housing | LossHigh | highest | 10 % | 3 | +201.7058 | [-470.2215, +787.4252] | 0.637 | 2/3 |
| models-xgboost-clean | housing | LossHigh | highest | 20 % | 3 | +275.3081 | [-1067.1345, +1406.2656] | 0.740 | 2/3 |
| models-xgboost-clean | housing | LossHigh | highest | 30 % | 3 | +713.9304 | [-149.1110, +2220.0640] | 0.445 | 2/3 |
| models-xgboost-clean | housing | LossHigh | highest | auc | 3 | +326.7370 | [-196.6409, +1103.9295] | 0.496 | 2/3 |
| models-xgboost-clean | wine | DataOOB | lowest | 5 % | 3 | -0.0103 | [-0.0357, +0.0086] | 0.516 | 1/3 |
| models-xgboost-clean | wine | DataOOB | lowest | 10 % | 3 | -0.0040 | [-0.0619, +0.0371] | 0.904 | 2/3 |
| models-xgboost-clean | wine | DataOOB | lowest | 20 % | 3 | +0.0020 | [-0.0157, +0.0218] | 0.872 | 1/3 |
| models-xgboost-clean | wine | DataOOB | lowest | 30 % | 3 | +0.0207 | [+0.0107, +0.0380] | 0.139 | 3/3 |
| models-xgboost-clean | wine | DataOOB | lowest | auc | 3 | +0.0014 | [-0.0244, +0.0170] | 0.925 | 2/3 |
| models-xgboost-clean | wine | DataOOB | highest | 5 % | 3 | -0.0082 | [-0.0243, +0.0050] | 0.439 | 1/3 |
| models-xgboost-clean | wine | DataOOB | highest | 10 % | 3 | -0.0112 | [-0.0421, +0.0435] | 0.722 | 1/3 |
| models-xgboost-clean | wine | DataOOB | highest | 20 % | 3 | -0.0142 | [-0.0583, +0.0249] | 0.615 | 1/3 |
| models-xgboost-clean | wine | DataOOB | highest | 30 % | 3 | -0.0094 | [-0.0284, +0.0117] | 0.504 | 1/3 |
| models-xgboost-clean | wine | DataOOB | highest | auc | 3 | -0.0105 | [-0.0157, -0.0061] | 0.064 | 0/3 |
| models-xgboost-clean | wine | LOO | lowest | 5 % | 3 | -0.0177 | [-0.0457, -0.0008] | 0.335 | 0/3 |
| models-xgboost-clean | wine | LOO | lowest | 10 % | 3 | +0.0161 | [+0.0055, +0.0303] | 0.161 | 3/3 |
| models-xgboost-clean | wine | LOO | lowest | 20 % | 3 | -0.0073 | [-0.0331, +0.0152] | 0.655 | 1/3 |
| models-xgboost-clean | wine | LOO | lowest | 30 % | 3 | -0.0347 | [-0.0625, -0.0182] | 0.131 | 0/3 |
| models-xgboost-clean | wine | LOO | lowest | auc | 3 | -0.0071 | [-0.0194, +0.0020] | 0.380 | 1/3 |
| models-xgboost-clean | wine | LOO | highest | 5 % | 3 | -0.0145 | [-0.0303, +0.0066] | 0.316 | 1/3 |
| models-xgboost-clean | wine | LOO | highest | 10 % | 3 | +0.0087 | [-0.0264, +0.0434] | 0.708 | 2/3 |
| models-xgboost-clean | wine | LOO | highest | 20 % | 3 | -0.0048 | [-0.0344, +0.0226] | 0.798 | 1/3 |
| models-xgboost-clean | wine | LOO | highest | 30 % | 3 | -0.0084 | [-0.0121, -0.0049] | 0.056 | 0/3 |
| models-xgboost-clean | wine | LOO | highest | auc | 3 | -0.0033 | [-0.0150, +0.0181] | 0.789 | 1/3 |
| models-xgboost-clean | wine | LossHigh | lowest | 5 % | 3 | -0.0111 | [-0.0360, +0.0152] | 0.532 | 1/3 |
| models-xgboost-clean | wine | LossHigh | lowest | 10 % | 3 | -0.0193 | [-0.0805, +0.0342] | 0.621 | 1/3 |
| models-xgboost-clean | wine | LossHigh | lowest | 20 % | 3 | +0.0056 | [-0.0129, +0.0220] | 0.637 | 2/3 |
| models-xgboost-clean | wine | LossHigh | lowest | 30 % | 3 | +0.0009 | [-0.0551, +0.0419] | 0.977 | 2/3 |
| models-xgboost-clean | wine | LossHigh | lowest | auc | 3 | -0.0047 | [-0.0277, +0.0160] | 0.749 | 1/3 |
| models-xgboost-clean | wine | LossHigh | highest | 5 % | 3 | -0.0158 | [-0.0351, -0.0017] | 0.255 | 0/3 |
| models-xgboost-clean | wine | LossHigh | highest | 10 % | 3 | +0.0061 | [-0.0302, +0.0343] | 0.777 | 2/3 |
| models-xgboost-clean | wine | LossHigh | highest | 20 % | 3 | -0.0109 | [-0.0357, +0.0265] | 0.625 | 1/3 |
| models-xgboost-clean | wine | LossHigh | highest | 30 % | 3 | +0.0058 | [-0.0114, +0.0182] | 0.581 | 2/3 |
| models-xgboost-clean | wine | LossHigh | highest | auc | 3 | -0.0037 | [-0.0181, +0.0102] | 0.692 | 1/3 |
| models-xgboost-noise10 | adult | DataOOB | lowest | 5 % | 3 | +0.0425 | [+0.0375, +0.0523] | 0.013 | 3/3 |
| models-xgboost-noise10 | adult | DataOOB | lowest | 10 % | 3 | +0.0609 | [+0.0497, +0.0749] | 0.014 | 3/3 |
| models-xgboost-noise10 | adult | DataOOB | lowest | 20 % | 3 | +0.0703 | [+0.0616, +0.0849] | 0.011 | 3/3 |
| models-xgboost-noise10 | adult | DataOOB | lowest | auc | 3 | +0.0510 | [+0.0441, +0.0566] | 0.005 | 3/3 |
| models-xgboost-noise10 | adult | KNNShapley | lowest | 5 % | 3 | +0.0483 | [+0.0369, +0.0598] | 0.018 | 3/3 |
| models-xgboost-noise10 | adult | KNNShapley | lowest | 10 % | 3 | +0.0670 | [+0.0579, +0.0779] | 0.008 | 3/3 |
| models-xgboost-noise10 | adult | KNNShapley | lowest | 20 % | 3 | +0.0615 | [+0.0565, +0.0693] | 0.004 | 3/3 |
| models-xgboost-noise10 | adult | KNNShapley | lowest | auc | 3 | +0.0525 | [+0.0483, +0.0583] | 0.003 | 3/3 |
| models-xgboost-noise10 | adult | LOO | lowest | 5 % | 3 | +0.0133 | [+0.0063, +0.0258] | 0.168 | 3/3 |
| models-xgboost-noise10 | adult | LOO | lowest | 10 % | 3 | +0.0193 | [-0.0018, +0.0489] | 0.334 | 2/3 |
| models-xgboost-noise10 | adult | LOO | lowest | 20 % | 3 | +0.0065 | [-0.0161, +0.0224] | 0.631 | 2/3 |
| models-xgboost-noise10 | adult | LOO | lowest | auc | 3 | +0.0122 | [-0.0028, +0.0304] | 0.336 | 2/3 |
| models-xgboost-noise10 | adult | LossHigh | lowest | 5 % | 3 | +0.0178 | [+0.0092, +0.0275] | 0.078 | 3/3 |
| models-xgboost-noise10 | adult | LossHigh | lowest | 10 % | 3 | +0.0379 | [+0.0261, +0.0547] | 0.048 | 3/3 |
| models-xgboost-noise10 | adult | LossHigh | lowest | 20 % | 3 | +0.0484 | [+0.0417, +0.0529] | 0.005 | 3/3 |
| models-xgboost-noise10 | adult | LossHigh | lowest | auc | 3 | +0.0308 | [+0.0244, +0.0406] | 0.025 | 3/3 |
| models-xgboost-noise10 | covertype | DataOOB | lowest | 5 % | 3 | +0.0065 | [+0.0008, +0.0098] | 0.151 | 3/3 |
| models-xgboost-noise10 | covertype | DataOOB | lowest | 10 % | 3 | +0.0117 | [+0.0074, +0.0186] | 0.079 | 3/3 |
| models-xgboost-noise10 | covertype | DataOOB | lowest | 20 % | 3 | +0.0153 | [+0.0064, +0.0298] | 0.170 | 3/3 |
| models-xgboost-noise10 | covertype | DataOOB | lowest | auc | 3 | +0.0098 | [+0.0054, +0.0169] | 0.110 | 3/3 |
| models-xgboost-noise10 | covertype | KNNShapley | lowest | 5 % | 3 | +0.0035 | [+0.0020, +0.0052] | 0.065 | 3/3 |
| models-xgboost-noise10 | covertype | KNNShapley | lowest | 10 % | 3 | +0.0091 | [+0.0032, +0.0172] | 0.160 | 3/3 |
| models-xgboost-noise10 | covertype | KNNShapley | lowest | 20 % | 3 | +0.0127 | [+0.0054, +0.0172] | 0.075 | 3/3 |
| models-xgboost-noise10 | covertype | KNNShapley | lowest | auc | 3 | +0.0075 | [+0.0048, +0.0120] | 0.083 | 3/3 |
| models-xgboost-noise10 | covertype | LOO | lowest | 5 % | 3 | -0.0044 | [-0.0086, -0.0012] | 0.183 | 0/3 |
| models-xgboost-noise10 | covertype | LOO | lowest | 10 % | 3 | -0.0035 | [-0.0052, -0.0022] | 0.061 | 0/3 |
| models-xgboost-noise10 | covertype | LOO | lowest | 20 % | 3 | -0.0031 | [-0.0086, +0.0014] | 0.406 | 1/3 |
| models-xgboost-noise10 | covertype | LOO | lowest | auc | 3 | -0.0032 | [-0.0062, -0.0011] | 0.182 | 0/3 |
| models-xgboost-noise10 | covertype | LossHigh | lowest | 5 % | 3 | -0.0029 | [-0.0032, -0.0026] | 0.004 | 0/3 |
| models-xgboost-noise10 | covertype | LossHigh | lowest | 10 % | 3 | +0.0071 | [+0.0056, +0.0082] | 0.012 | 3/3 |
| models-xgboost-noise10 | covertype | LossHigh | lowest | 20 % | 3 | +0.0022 | [-0.0068, +0.0106] | 0.705 | 2/3 |
| models-xgboost-noise10 | covertype | LossHigh | lowest | auc | 3 | +0.0025 | [-0.0003, +0.0050] | 0.245 | 2/3 |
| models-xgboost-noise10 | housing | DataOOB | lowest | 5 % | 3 | +10396.1133 | [+8207.9602, +11573.3843] | 0.011 | 3/3 |
| models-xgboost-noise10 | housing | DataOOB | lowest | 10 % | 3 | +24639.3921 | [+23370.9966, +26435.8101] | 0.001 | 3/3 |
| models-xgboost-noise10 | housing | DataOOB | lowest | 20 % | 3 | +25014.5229 | [+24210.4227, +26454.4031] | 0.001 | 3/3 |
| models-xgboost-noise10 | housing | DataOOB | lowest | auc | 3 | +18092.4311 | [+17188.4393, +19378.7784] | 0.001 | 3/3 |
| models-xgboost-noise10 | housing | LOO | lowest | 5 % | 3 | -505.4736 | [-3015.7656, +1943.8904] | 0.758 | 1/3 |
| models-xgboost-noise10 | housing | LOO | lowest | 10 % | 3 | +161.4626 | [-322.7033, +785.9955] | 0.671 | 2/3 |
| models-xgboost-noise10 | housing | LOO | lowest | 20 % | 3 | -934.1572 | [-1690.8997, -343.1050] | 0.143 | 0/3 |
| models-xgboost-noise10 | housing | LOO | lowest | auc | 3 | -299.3592 | [-1168.7554, +694.9447] | 0.636 | 1/3 |
| models-xgboost-noise10 | housing | LossHigh | lowest | 5 % | 3 | +7127.1924 | [+6127.4321, +8505.1989] | 0.010 | 3/3 |
| models-xgboost-noise10 | housing | LossHigh | lowest | 10 % | 3 | +10114.1414 | [+9401.5268, +10558.7768] | 0.001 | 3/3 |
| models-xgboost-noise10 | housing | LossHigh | lowest | 20 % | 3 | +13951.5979 | [+12373.4049, +15079.9796] | 0.003 | 3/3 |
| models-xgboost-noise10 | housing | LossHigh | lowest | auc | 3 | +9062.5006 | [+8518.5045, +9686.1933] | 0.001 | 3/3 |
| models-xgboost-noise10 | wine | DataOOB | lowest | 5 % | 3 | +0.0779 | [+0.0109, +0.1310] | 0.158 | 3/3 |
| models-xgboost-noise10 | wine | DataOOB | lowest | 10 % | 3 | +0.1320 | [+0.0923, +0.1904] | 0.047 | 3/3 |
| models-xgboost-noise10 | wine | DataOOB | lowest | 20 % | 3 | +0.1531 | [+0.1437, +0.1652] | 0.002 | 3/3 |
| models-xgboost-noise10 | wine | DataOOB | lowest | auc | 3 | +0.1072 | [+0.0865, +0.1319] | 0.015 | 3/3 |
| models-xgboost-noise10 | wine | LOO | lowest | 5 % | 3 | -0.0179 | [-0.0268, -0.0040] | 0.126 | 0/3 |
| models-xgboost-noise10 | wine | LOO | lowest | 10 % | 3 | -0.0079 | [-0.0512, +0.0195] | 0.754 | 2/3 |
| models-xgboost-noise10 | wine | LOO | lowest | 20 % | 3 | +0.0242 | [-0.0195, +0.0884] | 0.538 | 2/3 |
| models-xgboost-noise10 | wine | LOO | lowest | auc | 3 | -0.0014 | [-0.0076, +0.0019] | 0.699 | 2/3 |
| models-xgboost-noise10 | wine | LossHigh | lowest | 5 % | 3 | +0.0615 | [+0.0197, +0.0942] | 0.108 | 3/3 |
| models-xgboost-noise10 | wine | LossHigh | lowest | 10 % | 3 | +0.0393 | [-0.0337, +0.1127] | 0.450 | 2/3 |
| models-xgboost-noise10 | wine | LossHigh | lowest | 20 % | 3 | +0.0359 | [-0.0102, +0.0834] | 0.315 | 2/3 |
| models-xgboost-noise10 | wine | LossHigh | lowest | auc | 3 | +0.0391 | [+0.0084, +0.0558] | 0.126 | 3/3 |
| noise10 | adult | DataOOB | lowest | 5 % | 5 | +0.0006 | [-0.0054, +0.0063] | 0.866 | 2/5 |
| noise10 | adult | DataOOB | lowest | 10 % | 5 | -0.0009 | [-0.0047, +0.0029] | 0.702 | 2/5 |
| noise10 | adult | DataOOB | lowest | 20 % | 5 | +0.0017 | [-0.0099, +0.0133] | 0.818 | 3/5 |
| noise10 | adult | DataOOB | lowest | auc | 5 | +0.0003 | [-0.0047, +0.0047] | 0.932 | 3/5 |
| noise10 | adult | Influence | lowest | 5 % | 5 | +0.0029 | [-0.0030, +0.0082] | 0.422 | 3/5 |
| noise10 | adult | Influence | lowest | 10 % | 5 | -0.0016 | [-0.0099, +0.0058] | 0.744 | 3/5 |
| noise10 | adult | Influence | lowest | 20 % | 5 | +0.0001 | [-0.0121, +0.0114] | 0.989 | 2/5 |
| noise10 | adult | Influence | lowest | auc | 5 | +0.0002 | [-0.0067, +0.0057] | 0.966 | 3/5 |
| noise10 | adult | KNNShapley | lowest | 5 % | 5 | -0.0033 | [-0.0105, +0.0038] | 0.457 | 2/5 |
| noise10 | adult | KNNShapley | lowest | 10 % | 5 | -0.0044 | [-0.0137, +0.0022] | 0.406 | 2/5 |
| noise10 | adult | KNNShapley | lowest | 20 % | 5 | -0.0146 | [-0.0245, -0.0039] | 0.067 | 1/5 |
| noise10 | adult | KNNShapley | lowest | auc | 5 | -0.0061 | [-0.0134, -0.0012] | 0.165 | 1/5 |
| noise10 | adult | LOO | lowest | 5 % | 5 | +0.0006 | [-0.0035, +0.0046] | 0.827 | 3/5 |
| noise10 | adult | LOO | lowest | 10 % | 5 | -0.0075 | [-0.0251, +0.0052] | 0.445 | 2/5 |
| noise10 | adult | LOO | lowest | 20 % | 5 | -0.0020 | [-0.0117, +0.0062] | 0.706 | 3/5 |
| noise10 | adult | LOO | lowest | auc | 5 | -0.0032 | [-0.0114, +0.0025] | 0.472 | 1/5 |
| noise10 | adult | LissaInfluence | lowest | 5 % | 5 | +0.0046 | [+0.0014, +0.0076] | 0.050 | 4/5 |
| noise10 | adult | LissaInfluence | lowest | 10 % | 5 | -0.0026 | [-0.0087, +0.0044] | 0.525 | 2/5 |
| noise10 | adult | LissaInfluence | lowest | 20 % | 5 | -0.0029 | [-0.0080, +0.0023] | 0.405 | 2/5 |
| noise10 | adult | LissaInfluence | lowest | auc | 5 | -0.0005 | [-0.0032, +0.0027] | 0.770 | 2/5 |
| noise10 | adult | LossHigh | lowest | 5 % | 5 | +0.0008 | [-0.0070, +0.0066] | 0.850 | 3/5 |
| noise10 | adult | LossHigh | lowest | 10 % | 5 | -0.0031 | [-0.0059, -0.0004] | 0.131 | 1/5 |
| noise10 | adult | LossHigh | lowest | 20 % | 5 | -0.0101 | [-0.0176, -0.0033] | 0.076 | 0/5 |
| noise10 | adult | LossHigh | lowest | auc | 5 | -0.0035 | [-0.0051, -0.0015] | 0.028 | 1/5 |
| noise10 | covertype | DataOOB | lowest | 5 % | 5 | +0.0031 | [-0.0017, +0.0079] | 0.343 | 3/5 |
| noise10 | covertype | DataOOB | lowest | 10 % | 5 | -0.0009 | [-0.0128, +0.0077] | 0.884 | 4/5 |
| noise10 | covertype | DataOOB | lowest | 20 % | 5 | +0.0061 | [+0.0002, +0.0117] | 0.138 | 4/5 |
| noise10 | covertype | DataOOB | lowest | auc | 5 | +0.0019 | [-0.0024, +0.0060] | 0.466 | 3/5 |
| noise10 | covertype | Influence | lowest | 5 % | 5 | -0.0026 | [-0.0067, +0.0022] | 0.344 | 1/5 |
| noise10 | covertype | Influence | lowest | 10 % | 5 | -0.0084 | [-0.0178, -0.0006] | 0.161 | 1/5 |
| noise10 | covertype | Influence | lowest | 20 % | 5 | -0.0017 | [-0.0093, +0.0058] | 0.719 | 2/5 |
| noise10 | covertype | Influence | lowest | auc | 5 | -0.0042 | [-0.0091, +0.0006] | 0.212 | 2/5 |
| noise10 | covertype | KNNShapley | lowest | 5 % | 5 | -0.0024 | [-0.0100, +0.0042] | 0.580 | 2/5 |
| noise10 | covertype | KNNShapley | lowest | 10 % | 5 | -0.0044 | [-0.0068, -0.0010] | 0.065 | 1/5 |
| noise10 | covertype | KNNShapley | lowest | 20 % | 5 | -0.0180 | [-0.0214, -0.0140] | 0.001 | 0/5 |
| noise10 | covertype | KNNShapley | lowest | auc | 5 | -0.0067 | [-0.0084, -0.0048] | 0.003 | 0/5 |
| noise10 | covertype | LOO | lowest | 5 % | 5 | +0.0008 | [-0.0028, +0.0038] | 0.717 | 4/5 |
| noise10 | covertype | LOO | lowest | 10 % | 5 | +0.0005 | [-0.0046, +0.0048] | 0.872 | 3/5 |
| noise10 | covertype | LOO | lowest | 20 % | 5 | +0.0042 | [+0.0010, +0.0073] | 0.087 | 4/5 |
| noise10 | covertype | LOO | lowest | auc | 5 | +0.0014 | [-0.0022, +0.0044] | 0.478 | 4/5 |
| noise10 | covertype | LissaInfluence | lowest | 5 % | 5 | -0.0030 | [-0.0084, +0.0029] | 0.405 | 1/5 |
| noise10 | covertype | LissaInfluence | lowest | 10 % | 5 | -0.0166 | [-0.0213, -0.0120] | 0.004 | 0/5 |
| noise10 | covertype | LissaInfluence | lowest | 20 % | 5 | -0.0191 | [-0.0222, -0.0163] | 0.000 | 0/5 |
| noise10 | covertype | LissaInfluence | lowest | auc | 5 | -0.0117 | [-0.0142, -0.0097] | 0.001 | 0/5 |
| noise10 | covertype | LossHigh | lowest | 5 % | 5 | +0.0006 | [-0.0030, +0.0042] | 0.803 | 3/5 |
| noise10 | covertype | LossHigh | lowest | 10 % | 5 | +0.0006 | [-0.0038, +0.0049] | 0.840 | 3/5 |
| noise10 | covertype | LossHigh | lowest | 20 % | 5 | +0.0004 | [-0.0060, +0.0068] | 0.919 | 2/5 |
| noise10 | covertype | LossHigh | lowest | auc | 5 | +0.0005 | [-0.0027, +0.0036] | 0.814 | 3/5 |
| noise10 | housing | DataOOB | lowest | 5 % | 5 | +54.2835 | [-1113.5773, +1222.1444] | 0.938 | 2/5 |
| noise10 | housing | DataOOB | lowest | 10 % | 5 | +2808.6122 | [+1800.4945, +3769.9845] | 0.009 | 5/5 |
| noise10 | housing | DataOOB | lowest | 20 % | 5 | +3315.7293 | [+2036.2193, +4838.7419] | 0.015 | 5/5 |
| noise10 | housing | DataOOB | lowest | auc | 5 | +1895.7328 | [+1036.4507, +2810.2916] | 0.023 | 5/5 |
| noise10 | housing | Influence | lowest | 5 % | 5 | +374.2439 | [-294.0344, +1088.2883] | 0.396 | 3/5 |
| noise10 | housing | Influence | lowest | 10 % | 5 | +1102.7100 | [+557.9677, +1780.9219] | 0.035 | 5/5 |
| noise10 | housing | Influence | lowest | 20 % | 5 | +792.7648 | [-568.4956, +2058.3764] | 0.356 | 3/5 |
| noise10 | housing | Influence | lowest | auc | 5 | +705.2684 | [-9.9536, +1345.8032] | 0.148 | 4/5 |
| noise10 | housing | LOO | lowest | 5 % | 5 | +412.4940 | [-242.7034, +1025.9837] | 0.308 | 4/5 |
| noise10 | housing | LOO | lowest | 10 % | 5 | +1307.4687 | [+678.4053, +1804.0815] | 0.014 | 5/5 |
| noise10 | housing | LOO | lowest | 20 % | 5 | +2446.9629 | [+1749.1968, +3149.7883] | 0.004 | 5/5 |
| noise10 | housing | LOO | lowest | auc | 5 | +1205.1650 | [+996.6104, +1471.1173] | 0.001 | 5/5 |
| noise10 | housing | LissaInfluence | lowest | 5 % | 5 | +648.0796 | [-1057.1841, +2353.3434] | 0.546 | 2/5 |
| noise10 | housing | LissaInfluence | lowest | 10 % | 5 | -142.6407 | [-2246.1782, +2035.6313] | 0.914 | 2/5 |
| noise10 | housing | LissaInfluence | lowest | 20 % | 5 | -4273.5011 | [-8065.3305, -481.6718] | 0.117 | 1/5 |
| noise10 | housing | LissaInfluence | lowest | auc | 5 | -959.8456 | [-3122.9455, +1203.2542] | 0.480 | 2/5 |
| noise10 | housing | LossHigh | lowest | 5 % | 5 | -1494.5019 | [-2497.5587, -479.0913] | 0.066 | 1/5 |
| noise10 | housing | LossHigh | lowest | 10 % | 5 | +2650.3623 | [+1650.8477, +3697.2012] | 0.011 | 5/5 |
| noise10 | housing | LossHigh | lowest | 20 % | 5 | +2929.0527 | [+1622.5316, +4140.0334] | 0.017 | 5/5 |
| noise10 | housing | LossHigh | lowest | auc | 5 | +1352.5235 | [+424.1962, +2280.8509] | 0.062 | 4/5 |
| noise10 | wine | DataOOB | lowest | 5 % | 5 | -0.0049 | [-0.0105, -0.0001] | 0.164 | 1/5 |
| noise10 | wine | DataOOB | lowest | 10 % | 5 | +0.0014 | [-0.0020, +0.0040] | 0.474 | 4/5 |
| noise10 | wine | DataOOB | lowest | 20 % | 5 | +0.0023 | [-0.0053, +0.0089] | 0.599 | 4/5 |
| noise10 | wine | DataOOB | lowest | auc | 5 | -0.0001 | [-0.0017, +0.0012] | 0.889 | 3/5 |
| noise10 | wine | Influence | lowest | 5 % | 5 | -0.0114 | [-0.0243, -0.0017] | 0.150 | 1/5 |
| noise10 | wine | Influence | lowest | 10 % | 5 | -0.0022 | [-0.0224, +0.0152] | 0.851 | 3/5 |
| noise10 | wine | Influence | lowest | 20 % | 5 | +0.0056 | [-0.0151, +0.0253] | 0.648 | 3/5 |
| noise10 | wine | Influence | lowest | auc | 5 | -0.0023 | [-0.0184, +0.0108] | 0.801 | 2/5 |
| noise10 | wine | LOO | lowest | 5 % | 5 | +0.0054 | [+0.0025, +0.0084] | 0.033 | 5/5 |
| noise10 | wine | LOO | lowest | 10 % | 5 | +0.0139 | [+0.0078, +0.0199] | 0.016 | 5/5 |
| noise10 | wine | LOO | lowest | 20 % | 5 | +0.0225 | [+0.0130, +0.0316] | 0.014 | 5/5 |
| noise10 | wine | LOO | lowest | auc | 5 | +0.0122 | [+0.0079, +0.0158] | 0.005 | 5/5 |
| noise10 | wine | LissaInfluence | lowest | 5 % | 5 | -0.0009 | [-0.0080, +0.0066] | 0.837 | 2/5 |
| noise10 | wine | LissaInfluence | lowest | 10 % | 5 | -0.0078 | [-0.0224, +0.0099] | 0.438 | 2/5 |
| noise10 | wine | LissaInfluence | lowest | 20 % | 5 | -0.0141 | [-0.0331, +0.0049] | 0.266 | 2/5 |
| noise10 | wine | LissaInfluence | lowest | auc | 5 | -0.0067 | [-0.0184, +0.0063] | 0.395 | 2/5 |
| noise10 | wine | LossHigh | lowest | 5 % | 5 | -0.0123 | [-0.0216, -0.0029] | 0.079 | 0/5 |
| noise10 | wine | LossHigh | lowest | 10 % | 5 | +0.0038 | [-0.0038, +0.0115] | 0.440 | 3/5 |
| noise10 | wine | LossHigh | lowest | 20 % | 5 | +0.0025 | [-0.0038, +0.0093] | 0.536 | 3/5 |
| noise10 | wine | LossHigh | lowest | auc | 5 | -0.0010 | [-0.0042, +0.0018] | 0.608 | 2/5 |
| noise10 | wine | TMCShapley | lowest | 5 % | 5 | +0.0030 | [+0.0002, +0.0058] | 0.137 | 3/5 |
| noise10 | wine | TMCShapley | lowest | 10 % | 5 | +0.0143 | [+0.0067, +0.0218] | 0.032 | 5/5 |
| noise10 | wine | TMCShapley | lowest | 20 % | 5 | +0.0194 | [+0.0015, +0.0360] | 0.141 | 4/5 |
| noise10 | wine | TMCShapley | lowest | auc | 5 | +0.0110 | [+0.0028, +0.0184] | 0.069 | 4/5 |
| noise20 | adult | DataOOB | lowest | 5 % | 3 | +0.0018 | [+0.0004, +0.0033] | 0.165 | 3/3 |
| noise20 | adult | DataOOB | lowest | 10 % | 3 | -0.0012 | [-0.0134, +0.0074] | 0.870 | 2/3 |
| noise20 | adult | DataOOB | lowest | 20 % | 3 | +0.0013 | [-0.0130, +0.0140] | 0.882 | 2/3 |
| noise20 | adult | DataOOB | lowest | auc | 3 | +0.0003 | [-0.0079, +0.0064] | 0.945 | 2/3 |
| noise20 | adult | Influence | lowest | 5 % | 3 | +0.0099 | [+0.0012, +0.0151] | 0.153 | 3/3 |
| noise20 | adult | Influence | lowest | 10 % | 3 | +0.0032 | [-0.0061, +0.0100] | 0.575 | 2/3 |
| noise20 | adult | Influence | lowest | 20 % | 3 | +0.0117 | [+0.0053, +0.0170] | 0.076 | 3/3 |
| noise20 | adult | Influence | lowest | auc | 3 | +0.0066 | [+0.0013, +0.0118] | 0.162 | 3/3 |
| noise20 | adult | KNNShapley | lowest | 5 % | 3 | -0.0025 | [-0.0238, +0.0162] | 0.852 | 2/3 |
| noise20 | adult | KNNShapley | lowest | 10 % | 3 | -0.0082 | [-0.0108, -0.0059] | 0.028 | 0/3 |
| noise20 | adult | KNNShapley | lowest | 20 % | 3 | -0.0133 | [-0.0209, -0.0061] | 0.090 | 0/3 |
| noise20 | adult | KNNShapley | lowest | auc | 3 | -0.0070 | [-0.0142, -0.0014] | 0.204 | 0/3 |
| noise20 | adult | LissaInfluence | lowest | 5 % | 3 | +0.0010 | [-0.0064, +0.0054] | 0.820 | 2/3 |
| noise20 | adult | LissaInfluence | lowest | 10 % | 3 | +0.0046 | [-0.0046, +0.0119] | 0.442 | 2/3 |
| noise20 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0130 | [-0.0176, -0.0043] | 0.097 | 0/3 |
| noise20 | adult | LissaInfluence | lowest | auc | 3 | -0.0013 | [-0.0076, +0.0048] | 0.752 | 1/3 |
| noise20 | adult | LossHigh | lowest | 5 % | 3 | +0.0093 | [+0.0001, +0.0152] | 0.185 | 3/3 |
| noise20 | adult | LossHigh | lowest | 10 % | 3 | +0.0101 | [+0.0018, +0.0189] | 0.177 | 3/3 |
| noise20 | adult | LossHigh | lowest | 20 % | 3 | -0.0023 | [-0.0124, +0.0143] | 0.808 | 1/3 |
| noise20 | adult | LossHigh | lowest | auc | 3 | +0.0055 | [-0.0015, +0.0144] | 0.359 | 2/3 |
| noise20 | covertype | DataOOB | lowest | 5 % | 3 | +0.0035 | [-0.0022, +0.0066] | 0.343 | 2/3 |
| noise20 | covertype | DataOOB | lowest | 10 % | 3 | +0.0125 | [+0.0048, +0.0184] | 0.090 | 3/3 |
| noise20 | covertype | DataOOB | lowest | 20 % | 3 | +0.0077 | [+0.0006, +0.0124] | 0.166 | 3/3 |
| noise20 | covertype | DataOOB | lowest | auc | 3 | +0.0075 | [+0.0049, +0.0110] | 0.054 | 3/3 |
| noise20 | covertype | KNNShapley | lowest | 5 % | 3 | +0.0024 | [+0.0014, +0.0036] | 0.065 | 3/3 |
| noise20 | covertype | KNNShapley | lowest | 10 % | 3 | +0.0055 | [-0.0060, +0.0158] | 0.474 | 2/3 |
| noise20 | covertype | KNNShapley | lowest | 20 % | 3 | -0.0195 | [-0.0322, -0.0098] | 0.099 | 0/3 |
| noise20 | covertype | KNNShapley | lowest | auc | 3 | -0.0022 | [-0.0046, +0.0024] | 0.439 | 1/3 |
| noise20 | covertype | LissaInfluence | lowest | 5 % | 3 | -0.0005 | [-0.0028, +0.0010] | 0.690 | 2/3 |
| noise20 | covertype | LissaInfluence | lowest | 10 % | 3 | -0.0001 | [-0.0092, +0.0104] | 0.992 | 1/3 |
| noise20 | covertype | LissaInfluence | lowest | 20 % | 3 | -0.0153 | [-0.0310, +0.0016] | 0.246 | 1/3 |
| noise20 | covertype | LissaInfluence | lowest | auc | 3 | -0.0040 | [-0.0119, +0.0001] | 0.419 | 1/3 |
| noise20 | covertype | LossHigh | lowest | 5 % | 3 | +0.0021 | [-0.0032, +0.0090] | 0.614 | 2/3 |
| noise20 | covertype | LossHigh | lowest | 10 % | 3 | +0.0051 | [-0.0054, +0.0150] | 0.476 | 2/3 |
| noise20 | covertype | LossHigh | lowest | 20 % | 3 | +0.0021 | [-0.0102, +0.0108] | 0.768 | 2/3 |
| noise20 | covertype | LossHigh | lowest | auc | 3 | +0.0030 | [-0.0001, +0.0072] | 0.306 | 2/3 |
| noise20 | housing | DataOOB | lowest | 5 % | 3 | -1396.6890 | [-1935.4649, -1040.7813] | 0.036 | 0/3 |
| noise20 | housing | DataOOB | lowest | 10 % | 3 | -1348.3992 | [-2215.4855, -701.4526] | 0.096 | 0/3 |
| noise20 | housing | DataOOB | lowest | 20 % | 3 | +5975.4094 | [+4588.0948, +6944.8826] | 0.014 | 3/3 |
| noise20 | housing | DataOOB | lowest | auc | 3 | +639.0304 | [+283.6394, +1212.9806] | 0.158 | 3/3 |
| noise20 | housing | Influence | lowest | 5 % | 3 | +884.1673 | [+20.2021, +1802.0744] | 0.228 | 3/3 |
| noise20 | housing | Influence | lowest | 10 % | 3 | +1693.0527 | [+469.0810, +2310.8704] | 0.110 | 3/3 |
| noise20 | housing | Influence | lowest | 20 % | 3 | +1227.1951 | [-258.7948, +3017.4601] | 0.329 | 2/3 |
| noise20 | housing | Influence | lowest | auc | 3 | +1162.7354 | [+318.7630, +2071.4600] | 0.149 | 3/3 |
| noise20 | housing | LissaInfluence | lowest | 5 % | 3 | -215.3577 | [-3078.7926, +3953.8472] | 0.929 | 1/3 |
| noise20 | housing | LissaInfluence | lowest | 10 % | 3 | -3991.2597 | [-10340.5210, +3038.5030] | 0.411 | 1/3 |
| noise20 | housing | LissaInfluence | lowest | 20 % | 3 | -8743.1722 | [-20122.8632, -95.4601] | 0.279 | 0/3 |
| noise20 | housing | LissaInfluence | lowest | auc | 3 | -3736.3549 | [-9678.1093, +2104.0354] | 0.387 | 1/3 |
| noise20 | housing | LossHigh | lowest | 5 % | 3 | -3832.0336 | [-5561.3722, -2190.7681] | 0.059 | 0/3 |
| noise20 | housing | LossHigh | lowest | 10 % | 3 | -4068.3273 | [-4410.0284, -3788.8743] | 0.002 | 0/3 |
| noise20 | housing | LossHigh | lowest | 20 % | 3 | +5785.1138 | [+5035.2121, +6472.9583] | 0.005 | 3/3 |
| noise20 | housing | LossHigh | lowest | auc | 3 | -1037.3527 | [-1582.3109, -431.7322] | 0.090 | 0/3 |
| noise20 | wine | DataOOB | lowest | 5 % | 3 | +0.0040 | [-0.0083, +0.0256] | 0.747 | 1/3 |
| noise20 | wine | DataOOB | lowest | 10 % | 3 | +0.0225 | [-0.0089, +0.0602] | 0.382 | 2/3 |
| noise20 | wine | DataOOB | lowest | 20 % | 3 | +0.0168 | [-0.0020, +0.0377] | 0.282 | 2/3 |
| noise20 | wine | DataOOB | lowest | auc | 3 | +0.0136 | [-0.0059, +0.0384] | 0.406 | 2/3 |
| noise20 | wine | Influence | lowest | 5 % | 3 | -0.0035 | [-0.0054, -0.0007] | 0.137 | 0/3 |
| noise20 | wine | Influence | lowest | 10 % | 3 | +0.0199 | [+0.0097, +0.0266] | 0.062 | 3/3 |
| noise20 | wine | Influence | lowest | 20 % | 3 | +0.0044 | [-0.0004, +0.0133] | 0.423 | 2/3 |
| noise20 | wine | Influence | lowest | auc | 3 | +0.0077 | [+0.0036, +0.0122] | 0.091 | 3/3 |
| noise20 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0059 | [-0.0190, +0.0382] | 0.760 | 1/3 |
| noise20 | wine | LissaInfluence | lowest | 10 % | 3 | +0.0019 | [-0.0187, +0.0376] | 0.924 | 1/3 |
| noise20 | wine | LissaInfluence | lowest | 20 % | 3 | -0.0484 | [-0.1162, +0.0000] | 0.300 | 1/3 |
| noise20 | wine | LissaInfluence | lowest | auc | 3 | -0.0099 | [-0.0344, +0.0236] | 0.626 | 1/3 |
| noise20 | wine | LossHigh | lowest | 5 % | 3 | -0.0017 | [-0.0163, +0.0266] | 0.916 | 1/3 |
| noise20 | wine | LossHigh | lowest | 10 % | 3 | +0.0005 | [-0.0200, +0.0403] | 0.982 | 1/3 |
| noise20 | wine | LossHigh | lowest | 20 % | 3 | +0.0131 | [-0.0030, +0.0280] | 0.283 | 2/3 |
| noise20 | wine | LossHigh | lowest | auc | 3 | +0.0030 | [-0.0116, +0.0288] | 0.836 | 1/3 |
| noise5 | adult | DataOOB | lowest | 5 % | 3 | +0.0024 | [-0.0010, +0.0061] | 0.356 | 2/3 |
| noise5 | adult | DataOOB | lowest | 10 % | 3 | -0.0088 | [-0.0209, +0.0025] | 0.322 | 1/3 |
| noise5 | adult | DataOOB | lowest | 20 % | 3 | -0.0113 | [-0.0288, -0.0003] | 0.331 | 0/3 |
| noise5 | adult | DataOOB | lowest | auc | 3 | -0.0055 | [-0.0084, -0.0016] | 0.112 | 0/3 |
| noise5 | adult | Influence | lowest | 5 % | 3 | -0.0005 | [-0.0018, +0.0017] | 0.683 | 1/3 |
| noise5 | adult | Influence | lowest | 10 % | 3 | -0.0061 | [-0.0128, +0.0029] | 0.322 | 1/3 |
| noise5 | adult | Influence | lowest | 20 % | 3 | -0.0057 | [-0.0102, -0.0019] | 0.140 | 0/3 |
| noise5 | adult | Influence | lowest | auc | 3 | -0.0039 | [-0.0069, +0.0003] | 0.213 | 1/3 |
| noise5 | adult | KNNShapley | lowest | 5 % | 3 | +0.0034 | [-0.0014, +0.0067] | 0.298 | 2/3 |
| noise5 | adult | KNNShapley | lowest | 10 % | 3 | -0.0175 | [-0.0240, -0.0092] | 0.057 | 0/3 |
| noise5 | adult | KNNShapley | lowest | 20 % | 3 | -0.0205 | [-0.0308, -0.0101] | 0.076 | 0/3 |
| noise5 | adult | KNNShapley | lowest | auc | 3 | -0.0108 | [-0.0154, -0.0043] | 0.084 | 0/3 |
| noise5 | adult | LissaInfluence | lowest | 5 % | 3 | -0.0131 | [-0.0257, +0.0036] | 0.271 | 1/3 |
| noise5 | adult | LissaInfluence | lowest | 10 % | 3 | -0.0151 | [-0.0316, -0.0034] | 0.217 | 0/3 |
| noise5 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0180 | [-0.0430, +0.0002] | 0.297 | 1/3 |
| noise5 | adult | LissaInfluence | lowest | auc | 3 | -0.0134 | [-0.0290, -0.0029] | 0.232 | 0/3 |
| noise5 | adult | LossHigh | lowest | 5 % | 3 | -0.0032 | [-0.0110, +0.0034] | 0.532 | 1/3 |
| noise5 | adult | LossHigh | lowest | 10 % | 3 | -0.0062 | [-0.0126, +0.0047] | 0.376 | 1/3 |
| noise5 | adult | LossHigh | lowest | 20 % | 3 | -0.0071 | [-0.0114, +0.0015] | 0.240 | 1/3 |
| noise5 | adult | LossHigh | lowest | auc | 3 | -0.0049 | [-0.0059, -0.0039] | 0.015 | 0/3 |
| noise5 | covertype | DataOOB | lowest | 5 % | 3 | +0.0057 | [+0.0000, +0.0090] | 0.184 | 2/3 |
| noise5 | covertype | DataOOB | lowest | 10 % | 3 | +0.0061 | [+0.0028, +0.0122] | 0.181 | 3/3 |
| noise5 | covertype | DataOOB | lowest | 20 % | 3 | +0.0048 | [-0.0016, +0.0122] | 0.354 | 2/3 |
| noise5 | covertype | DataOOB | lowest | auc | 3 | +0.0049 | [+0.0020, +0.0099] | 0.186 | 3/3 |
| noise5 | covertype | KNNShapley | lowest | 5 % | 3 | +0.0092 | [+0.0058, +0.0120] | 0.037 | 3/3 |
| noise5 | covertype | KNNShapley | lowest | 10 % | 3 | -0.0005 | [-0.0030, +0.0020] | 0.777 | 1/3 |
| noise5 | covertype | KNNShapley | lowest | 20 % | 3 | -0.0201 | [-0.0282, -0.0132] | 0.044 | 0/3 |
| noise5 | covertype | KNNShapley | lowest | auc | 3 | -0.0029 | [-0.0047, -0.0014] | 0.097 | 0/3 |
| noise5 | covertype | LissaInfluence | lowest | 5 % | 3 | +0.0051 | [+0.0000, +0.0102] | 0.223 | 2/3 |
| noise5 | covertype | LissaInfluence | lowest | 10 % | 3 | -0.0034 | [-0.0042, -0.0020] | 0.040 | 0/3 |
| noise5 | covertype | LissaInfluence | lowest | 20 % | 3 | -0.0329 | [-0.0486, -0.0194] | 0.061 | 0/3 |
| noise5 | covertype | LissaInfluence | lowest | auc | 3 | -0.0082 | [-0.0123, -0.0058] | 0.058 | 0/3 |
| noise5 | covertype | LossHigh | lowest | 5 % | 3 | +0.0011 | [-0.0016, +0.0046] | 0.598 | 2/3 |
| noise5 | covertype | LossHigh | lowest | 10 % | 3 | +0.0001 | [-0.0006, +0.0006] | 0.754 | 2/3 |
| noise5 | covertype | LossHigh | lowest | 20 % | 3 | +0.0042 | [+0.0002, +0.0078] | 0.197 | 3/3 |
| noise5 | covertype | LossHigh | lowest | auc | 3 | +0.0014 | [-0.0001, +0.0033] | 0.297 | 2/3 |
| noise5 | housing | DataOOB | lowest | 5 % | 3 | +2167.2835 | [+216.8214, +3918.2090] | 0.181 | 3/3 |
| noise5 | housing | DataOOB | lowest | 10 % | 3 | +2158.2768 | [+871.7306, +3385.5529] | 0.097 | 3/3 |
| noise5 | housing | DataOOB | lowest | 20 % | 3 | +2279.4071 | [+1266.1929, +3859.1003] | 0.104 | 3/3 |
| noise5 | housing | DataOOB | lowest | auc | 3 | +1921.0264 | [+697.6526, +2677.3666] | 0.090 | 3/3 |
| noise5 | housing | Influence | lowest | 5 % | 3 | +1320.9502 | [+177.9185, +2468.3396] | 0.184 | 3/3 |
| noise5 | housing | Influence | lowest | 10 % | 3 | +1203.9871 | [+512.1962, +1837.2781] | 0.088 | 3/3 |
| noise5 | housing | Influence | lowest | 20 % | 3 | +1418.1372 | [+946.1979, +1841.1606] | 0.032 | 3/3 |
| noise5 | housing | Influence | lowest | auc | 3 | +1136.2670 | [+603.3165, +1478.4175] | 0.052 | 3/3 |
| noise5 | housing | LissaInfluence | lowest | 5 % | 3 | +1689.1056 | [-797.7116, +3361.9385] | 0.314 | 2/3 |
| noise5 | housing | LissaInfluence | lowest | 10 % | 3 | +1012.8909 | [-1264.1186, +2895.7495] | 0.493 | 2/3 |
| noise5 | housing | LissaInfluence | lowest | 20 % | 3 | -1242.3060 | [-4382.8946, +2932.6944] | 0.625 | 1/3 |
| noise5 | housing | LissaInfluence | lowest | auc | 3 | +491.5340 | [-1769.1960, +2659.5643] | 0.738 | 2/3 |
| noise5 | housing | LossHigh | lowest | 5 % | 3 | +3009.6369 | [+1451.8532, +4184.2461] | 0.066 | 3/3 |
| noise5 | housing | LossHigh | lowest | 10 % | 3 | +2570.4254 | [+1116.3001, +3483.6762] | 0.073 | 3/3 |
| noise5 | housing | LossHigh | lowest | 20 % | 3 | +2126.2487 | [+529.6523, +2991.6537] | 0.117 | 3/3 |
| noise5 | housing | LossHigh | lowest | auc | 3 | +2247.8810 | [+913.9889, +3066.8002] | 0.079 | 3/3 |
| noise5 | wine | DataOOB | lowest | 5 % | 3 | -0.0019 | [-0.0089, +0.0075] | 0.739 | 1/3 |
| noise5 | wine | DataOOB | lowest | 10 % | 3 | -0.0084 | [-0.0230, +0.0182] | 0.594 | 1/3 |
| noise5 | wine | DataOOB | lowest | 20 % | 3 | -0.0092 | [-0.0189, +0.0004] | 0.239 | 1/3 |
| noise5 | wine | DataOOB | lowest | auc | 3 | -0.0059 | [-0.0145, +0.0088] | 0.508 | 1/3 |
| noise5 | wine | Influence | lowest | 5 % | 3 | -0.0006 | [-0.0033, +0.0013] | 0.713 | 2/3 |
| noise5 | wine | Influence | lowest | 10 % | 3 | -0.0009 | [-0.0074, +0.0118] | 0.896 | 1/3 |
| noise5 | wine | Influence | lowest | 20 % | 3 | +0.0046 | [+0.0011, +0.0068] | 0.123 | 3/3 |
| noise5 | wine | Influence | lowest | auc | 3 | +0.0007 | [-0.0022, +0.0060] | 0.830 | 1/3 |
| noise5 | wine | LissaInfluence | lowest | 5 % | 3 | -0.0067 | [-0.0256, +0.0061] | 0.557 | 1/3 |
| noise5 | wine | LissaInfluence | lowest | 10 % | 3 | -0.0157 | [-0.0388, +0.0161] | 0.440 | 1/3 |
| noise5 | wine | LissaInfluence | lowest | 20 % | 3 | -0.0216 | [-0.0459, +0.0045] | 0.277 | 1/3 |
| noise5 | wine | LissaInfluence | lowest | auc | 3 | -0.0130 | [-0.0324, +0.0087] | 0.390 | 1/3 |
| noise5 | wine | LossHigh | lowest | 5 % | 3 | -0.0029 | [-0.0146, +0.0074] | 0.693 | 1/3 |
| noise5 | wine | LossHigh | lowest | 10 % | 3 | -0.0069 | [-0.0220, +0.0158] | 0.610 | 1/3 |
| noise5 | wine | LossHigh | lowest | 20 % | 3 | -0.0073 | [-0.0157, +0.0016] | 0.283 | 1/3 |
| noise5 | wine | LossHigh | lowest | auc | 3 | -0.0051 | [-0.0130, +0.0082] | 0.523 | 1/3 |
| sweep-base | adult | DataOOB | lowest | 5 % | 3 | +0.0008 | [-0.0014, +0.0039] | 0.670 | 1/3 |
| sweep-base | adult | DataOOB | lowest | 10 % | 3 | -0.0007 | [-0.0050, +0.0047] | 0.820 | 1/3 |
| sweep-base | adult | DataOOB | lowest | 20 % | 3 | +0.0043 | [-0.0136, +0.0233] | 0.723 | 2/3 |
| sweep-base | adult | DataOOB | lowest | auc | 3 | +0.0010 | [-0.0044, +0.0049] | 0.755 | 2/3 |
| sweep-base | adult | Influence | lowest | 5 % | 3 | +0.0043 | [-0.0011, +0.0078] | 0.258 | 2/3 |
| sweep-base | adult | Influence | lowest | 10 % | 3 | +0.0056 | [+0.0050, +0.0069] | 0.013 | 3/3 |
| sweep-base | adult | Influence | lowest | 20 % | 3 | +0.0084 | [-0.0005, +0.0164] | 0.229 | 2/3 |
| sweep-base | adult | Influence | lowest | auc | 3 | +0.0053 | [+0.0033, +0.0079] | 0.062 | 3/3 |
| sweep-base | adult | KNNShapley | lowest | 5 % | 3 | -0.0065 | [-0.0147, +0.0053] | 0.397 | 1/3 |
| sweep-base | adult | KNNShapley | lowest | 10 % | 3 | -0.0079 | [-0.0223, +0.0039] | 0.413 | 1/3 |
| sweep-base | adult | KNNShapley | lowest | 20 % | 3 | -0.0151 | [-0.0317, +0.0046] | 0.289 | 1/3 |
| sweep-base | adult | KNNShapley | lowest | auc | 3 | -0.0084 | [-0.0200, +0.0005] | 0.302 | 1/3 |
| sweep-base | adult | LOO | lowest | 5 % | 3 | +0.0041 | [+0.0018, +0.0069] | 0.110 | 3/3 |
| sweep-base | adult | LOO | lowest | 10 % | 3 | -0.0107 | [-0.0408, +0.0104] | 0.561 | 1/3 |
| sweep-base | adult | LOO | lowest | 20 % | 3 | -0.0063 | [-0.0199, +0.0006] | 0.451 | 2/3 |
| sweep-base | adult | LOO | lowest | auc | 3 | -0.0046 | [-0.0185, +0.0049] | 0.589 | 1/3 |
| sweep-base | adult | LissaInfluence | lowest | 5 % | 3 | +0.0045 | [-0.0010, +0.0095] | 0.276 | 2/3 |
| sweep-base | adult | LissaInfluence | lowest | 10 % | 3 | +0.0008 | [-0.0085, +0.0099] | 0.894 | 2/3 |
| sweep-base | adult | LissaInfluence | lowest | 20 % | 3 | -0.0017 | [-0.0061, +0.0044] | 0.641 | 1/3 |
| sweep-base | adult | LissaInfluence | lowest | auc | 3 | +0.0010 | [-0.0034, +0.0052] | 0.726 | 2/3 |
| sweep-base | adult | LossHigh | lowest | 5 % | 3 | +0.0036 | [-0.0006, +0.0076] | 0.264 | 2/3 |
| sweep-base | adult | LossHigh | lowest | 10 % | 3 | -0.0046 | [-0.0075, -0.0009] | 0.139 | 0/3 |
| sweep-base | adult | LossHigh | lowest | 20 % | 3 | -0.0128 | [-0.0249, -0.0041] | 0.178 | 0/3 |
| sweep-base | adult | LossHigh | lowest | auc | 3 | -0.0040 | [-0.0047, -0.0033] | 0.009 | 0/3 |
| sweep-batch_size-0 | adult | DataOOB | lowest | 5 % | 3 | +0.0028 | [-0.0017, +0.0051] | 0.338 | 2/3 |
| sweep-batch_size-0 | adult | DataOOB | lowest | 10 % | 3 | -0.0063 | [-0.0225, +0.0074] | 0.548 | 1/3 |
| sweep-batch_size-0 | adult | DataOOB | lowest | 20 % | 3 | -0.0069 | [-0.0194, +0.0052] | 0.432 | 1/3 |
| sweep-batch_size-0 | adult | DataOOB | lowest | auc | 3 | -0.0034 | [-0.0120, +0.0053] | 0.568 | 1/3 |
| sweep-batch_size-0 | adult | Influence | lowest | 5 % | 3 | +0.0017 | [+0.0013, +0.0023] | 0.033 | 3/3 |
| sweep-batch_size-0 | adult | Influence | lowest | 10 % | 3 | -0.0035 | [-0.0204, +0.0058] | 0.717 | 2/3 |
| sweep-batch_size-0 | adult | Influence | lowest | 20 % | 3 | -0.0010 | [-0.0106, +0.0125] | 0.898 | 1/3 |
| sweep-batch_size-0 | adult | Influence | lowest | auc | 3 | -0.0012 | [-0.0085, +0.0059] | 0.807 | 1/3 |
| sweep-batch_size-0 | adult | KNNShapley | lowest | 5 % | 3 | -0.0022 | [-0.0060, +0.0009] | 0.384 | 1/3 |
| sweep-batch_size-0 | adult | KNNShapley | lowest | 10 % | 3 | -0.0049 | [-0.0151, +0.0072] | 0.531 | 1/3 |
| sweep-batch_size-0 | adult | KNNShapley | lowest | 20 % | 3 | -0.0113 | [-0.0145, -0.0094] | 0.019 | 0/3 |
| sweep-batch_size-0 | adult | KNNShapley | lowest | auc | 3 | -0.0052 | [-0.0097, +0.0006] | 0.228 | 1/3 |
| sweep-batch_size-0 | adult | LOO | lowest | 5 % | 3 | -0.0075 | [-0.0098, -0.0062] | 0.022 | 0/3 |
| sweep-batch_size-0 | adult | LOO | lowest | 10 % | 3 | -0.0065 | [-0.0104, -0.0019] | 0.120 | 0/3 |
| sweep-batch_size-0 | adult | LOO | lowest | 20 % | 3 | -0.0104 | [-0.0360, +0.0086] | 0.516 | 1/3 |
| sweep-batch_size-0 | adult | LOO | lowest | auc | 3 | -0.0069 | [-0.0133, -0.0034] | 0.160 | 0/3 |
| sweep-batch_size-0 | adult | LissaInfluence | lowest | 5 % | 3 | -0.0053 | [-0.0173, +0.0049] | 0.495 | 1/3 |
| sweep-batch_size-0 | adult | LissaInfluence | lowest | 10 % | 3 | +0.0018 | [-0.0082, +0.0114] | 0.786 | 2/3 |
| sweep-batch_size-0 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0207 | [-0.0473, -0.0016] | 0.270 | 0/3 |
| sweep-batch_size-0 | adult | LissaInfluence | lowest | auc | 3 | -0.0058 | [-0.0120, +0.0051] | 0.399 | 1/3 |
| sweep-batch_size-0 | adult | LossHigh | lowest | 5 % | 3 | -0.0013 | [-0.0055, +0.0059] | 0.760 | 1/3 |
| sweep-batch_size-0 | adult | LossHigh | lowest | 10 % | 3 | -0.0205 | [-0.0458, +0.0111] | 0.345 | 1/3 |
| sweep-batch_size-0 | adult | LossHigh | lowest | 20 % | 3 | -0.0220 | [-0.0590, +0.0062] | 0.374 | 1/3 |
| sweep-batch_size-0 | adult | LossHigh | lowest | auc | 3 | -0.0135 | [-0.0333, +0.0072] | 0.368 | 1/3 |
| sweep-fit_mode-overfit | adult | DataOOB | lowest | 5 % | 3 | -0.0118 | [-0.0245, +0.0095] | 0.385 | 1/3 |
| sweep-fit_mode-overfit | adult | DataOOB | lowest | 10 % | 3 | +0.0180 | [+0.0098, +0.0257] | 0.059 | 3/3 |
| sweep-fit_mode-overfit | adult | DataOOB | lowest | 20 % | 3 | -0.0017 | [-0.0242, +0.0397] | 0.942 | 1/3 |
| sweep-fit_mode-overfit | adult | DataOOB | lowest | auc | 3 | +0.0034 | [-0.0076, +0.0118] | 0.617 | 2/3 |
| sweep-fit_mode-overfit | adult | KNNShapley | lowest | 5 % | 3 | -0.0260 | [-0.0579, -0.0013] | 0.261 | 0/3 |
| sweep-fit_mode-overfit | adult | KNNShapley | lowest | 10 % | 3 | -0.0078 | [-0.0339, +0.0089] | 0.613 | 2/3 |
| sweep-fit_mode-overfit | adult | KNNShapley | lowest | 20 % | 3 | -0.0107 | [-0.0178, -0.0065] | 0.094 | 0/3 |
| sweep-fit_mode-overfit | adult | KNNShapley | lowest | auc | 3 | -0.0121 | [-0.0159, -0.0058] | 0.063 | 0/3 |
| sweep-fit_mode-overfit | adult | LOO | lowest | 5 % | 3 | -0.0097 | [-0.0202, +0.0012] | 0.257 | 1/3 |
| sweep-fit_mode-overfit | adult | LOO | lowest | 10 % | 3 | +0.0108 | [-0.0026, +0.0304] | 0.396 | 2/3 |
| sweep-fit_mode-overfit | adult | LOO | lowest | 20 % | 3 | -0.0125 | [-0.0493, +0.0290] | 0.638 | 1/3 |
| sweep-fit_mode-overfit | adult | LOO | lowest | auc | 3 | -0.0015 | [-0.0060, +0.0064] | 0.743 | 1/3 |
| sweep-fit_mode-overfit | adult | LissaInfluence | lowest | 5 % | 3 | -0.0108 | [-0.0278, -0.0001] | 0.333 | 0/3 |
| sweep-fit_mode-overfit | adult | LissaInfluence | lowest | 10 % | 3 | -0.0019 | [-0.0197, +0.0204] | 0.889 | 1/3 |
| sweep-fit_mode-overfit | adult | LissaInfluence | lowest | 20 % | 3 | -0.0078 | [-0.0320, +0.0102] | 0.600 | 1/3 |
| sweep-fit_mode-overfit | adult | LissaInfluence | lowest | auc | 3 | -0.0053 | [-0.0089, +0.0002] | 0.196 | 1/3 |
| sweep-fit_mode-overfit | adult | LossHigh | lowest | 5 % | 3 | -0.0056 | [-0.0079, -0.0018] | 0.100 | 0/3 |
| sweep-fit_mode-overfit | adult | LossHigh | lowest | 10 % | 3 | +0.0060 | [-0.0165, +0.0234] | 0.662 | 2/3 |
| sweep-fit_mode-overfit | adult | LossHigh | lowest | 20 % | 3 | -0.0070 | [-0.0415, +0.0301] | 0.766 | 1/3 |
| sweep-fit_mode-overfit | adult | LossHigh | lowest | auc | 3 | -0.0009 | [-0.0020, -0.0002] | 0.252 | 0/3 |
| sweep-fit_mode-underfit | adult | DataOOB | lowest | 5 % | 3 | +0.0018 | [-0.0025, +0.0080] | 0.621 | 1/3 |
| sweep-fit_mode-underfit | adult | DataOOB | lowest | 10 % | 3 | +0.0040 | [+0.0000, +0.0120] | 0.423 | 1/3 |
| sweep-fit_mode-underfit | adult | DataOOB | lowest | 20 % | 3 | +0.0066 | [+0.0000, +0.0124] | 0.207 | 2/3 |
| sweep-fit_mode-underfit | adult | DataOOB | lowest | auc | 3 | +0.0036 | [+0.0000, +0.0096] | 0.352 | 2/3 |
| sweep-fit_mode-underfit | adult | Influence | lowest | 5 % | 3 | -0.0004 | [-0.0025, +0.0014] | 0.766 | 1/3 |
| sweep-fit_mode-underfit | adult | Influence | lowest | 10 % | 3 | +0.0006 | [+0.0000, +0.0019] | 0.418 | 2/3 |
| sweep-fit_mode-underfit | adult | Influence | lowest | 20 % | 3 | +0.0045 | [+0.0000, +0.0075] | 0.189 | 2/3 |
| sweep-fit_mode-underfit | adult | Influence | lowest | auc | 3 | +0.0013 | [+0.0000, +0.0025] | 0.226 | 2/3 |
| sweep-fit_mode-underfit | adult | KNNShapley | lowest | 5 % | 3 | +0.0019 | [-0.0025, +0.0083] | 0.616 | 1/3 |
| sweep-fit_mode-underfit | adult | KNNShapley | lowest | 10 % | 3 | +0.0047 | [+0.0000, +0.0117] | 0.315 | 2/3 |
| sweep-fit_mode-underfit | adult | KNNShapley | lowest | 20 % | 3 | +0.0076 | [+0.0000, +0.0152] | 0.227 | 2/3 |
| sweep-fit_mode-underfit | adult | KNNShapley | lowest | auc | 3 | +0.0041 | [+0.0000, +0.0103] | 0.315 | 2/3 |
| sweep-fit_mode-underfit | adult | LOO | lowest | 5 % | 3 | +0.0045 | [+0.0000, +0.0135] | 0.422 | 2/3 |
| sweep-fit_mode-underfit | adult | LOO | lowest | 10 % | 3 | +0.0003 | [-0.0000, +0.0010] | 0.432 | 1/3 |
| sweep-fit_mode-underfit | adult | LOO | lowest | 20 % | 3 | +0.0026 | [+0.0000, +0.0075] | 0.396 | 2/3 |
| sweep-fit_mode-underfit | adult | LOO | lowest | auc | 3 | +0.0019 | [+0.0000, +0.0038] | 0.227 | 2/3 |
| sweep-fit_mode-underfit | adult | LissaInfluence | lowest | 5 % | 3 | +0.0052 | [-0.0025, +0.0182] | 0.506 | 1/3 |
| sweep-fit_mode-underfit | adult | LissaInfluence | lowest | 10 % | 3 | +0.0065 | [+0.0000, +0.0171] | 0.345 | 2/3 |
| sweep-fit_mode-underfit | adult | LissaInfluence | lowest | 20 % | 3 | +0.0104 | [+0.0000, +0.0238] | 0.276 | 2/3 |
| sweep-fit_mode-underfit | adult | LissaInfluence | lowest | auc | 3 | +0.0064 | [+0.0000, +0.0169] | 0.353 | 2/3 |
| sweep-fit_mode-underfit | adult | LossHigh | lowest | 5 % | 3 | +0.0038 | [-0.0025, +0.0141] | 0.534 | 1/3 |
| sweep-fit_mode-underfit | adult | LossHigh | lowest | 10 % | 3 | +0.0063 | [-0.0000, +0.0188] | 0.424 | 1/3 |
| sweep-fit_mode-underfit | adult | LossHigh | lowest | 20 % | 3 | +0.0084 | [+0.0000, +0.0202] | 0.301 | 2/3 |
| sweep-fit_mode-underfit | adult | LossHigh | lowest | auc | 3 | +0.0054 | [+0.0000, +0.0156] | 0.401 | 2/3 |
| sweep-sample_scale-0.1 | adult | DataOOB | lowest | 5 % | 3 | -0.0169 | [-0.0914, +0.0274] | 0.697 | 2/3 |
| sweep-sample_scale-0.1 | adult | DataOOB | lowest | 10 % | 3 | +0.0481 | [-0.0033, +0.1286] | 0.359 | 2/3 |
| sweep-sample_scale-0.1 | adult | DataOOB | lowest | 20 % | 3 | +0.0066 | [-0.0059, +0.0272] | 0.590 | 1/3 |
| sweep-sample_scale-0.1 | adult | DataOOB | lowest | auc | 3 | +0.0155 | [+0.0052, +0.0239] | 0.106 | 3/3 |
| sweep-sample_scale-0.1 | adult | Influence | lowest | 5 % | 3 | +0.0130 | [+0.0047, +0.0231] | 0.137 | 3/3 |
| sweep-sample_scale-0.1 | adult | Influence | lowest | 10 % | 3 | +0.0913 | [+0.0176, +0.2161] | 0.283 | 3/3 |
| sweep-sample_scale-0.1 | adult | Influence | lowest | 20 % | 3 | +0.0004 | [-0.0296, +0.0245] | 0.983 | 2/3 |
| sweep-sample_scale-0.1 | adult | Influence | lowest | auc | 3 | +0.0376 | [+0.0139, +0.0748] | 0.184 | 3/3 |
| sweep-sample_scale-0.1 | adult | KNNShapley | lowest | 5 % | 3 | +0.0172 | [+0.0084, +0.0270] | 0.086 | 3/3 |
| sweep-sample_scale-0.1 | adult | KNNShapley | lowest | 10 % | 3 | +0.0642 | [+0.0215, +0.1470] | 0.261 | 3/3 |
| sweep-sample_scale-0.1 | adult | KNNShapley | lowest | 20 % | 3 | -0.0002 | [-0.0217, +0.0133] | 0.985 | 2/3 |
| sweep-sample_scale-0.1 | adult | KNNShapley | lowest | auc | 3 | +0.0283 | [+0.0165, +0.0518] | 0.137 | 3/3 |
| sweep-sample_scale-0.1 | adult | LOO | lowest | 5 % | 3 | -0.0129 | [-0.0284, +0.0085] | 0.363 | 1/3 |
| sweep-sample_scale-0.1 | adult | LOO | lowest | 10 % | 3 | +0.0801 | [-0.0011, +0.2183] | 0.368 | 2/3 |
| sweep-sample_scale-0.1 | adult | LOO | lowest | 20 % | 3 | -0.0628 | [-0.1820, +0.0269] | 0.418 | 1/3 |
| sweep-sample_scale-0.1 | adult | LOO | lowest | auc | 3 | +0.0111 | [-0.0158, +0.0317] | 0.513 | 2/3 |
| sweep-sample_scale-0.1 | adult | LissaInfluence | lowest | 5 % | 3 | +0.0271 | [+0.0138, +0.0392] | 0.067 | 3/3 |
| sweep-sample_scale-0.1 | adult | LissaInfluence | lowest | 10 % | 3 | +0.0765 | [+0.0228, +0.1800] | 0.277 | 3/3 |
| sweep-sample_scale-0.1 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0012 | [-0.0220, +0.0198] | 0.931 | 1/3 |
| sweep-sample_scale-0.1 | adult | LissaInfluence | lowest | auc | 3 | +0.0352 | [+0.0152, +0.0718] | 0.195 | 3/3 |
| sweep-sample_scale-0.1 | adult | LossHigh | lowest | 5 % | 3 | -0.0325 | [-0.1287, +0.0239] | 0.570 | 2/3 |
| sweep-sample_scale-0.1 | adult | LossHigh | lowest | 10 % | 3 | +0.0602 | [+0.0149, +0.1377] | 0.262 | 3/3 |
| sweep-sample_scale-0.1 | adult | LossHigh | lowest | 20 % | 3 | -0.0191 | [-0.0917, +0.0231] | 0.654 | 2/3 |
| sweep-sample_scale-0.1 | adult | LossHigh | lowest | auc | 3 | +0.0097 | [-0.0035, +0.0181] | 0.283 | 2/3 |
| sweep-sample_scale-0.3 | adult | DataOOB | lowest | 5 % | 3 | -0.0038 | [-0.0086, -0.0010] | 0.252 | 0/3 |
| sweep-sample_scale-0.3 | adult | DataOOB | lowest | 10 % | 3 | +0.0046 | [-0.0065, +0.0117] | 0.500 | 2/3 |
| sweep-sample_scale-0.3 | adult | DataOOB | lowest | 20 % | 3 | +0.0091 | [+0.0033, +0.0143] | 0.103 | 3/3 |
| sweep-sample_scale-0.3 | adult | DataOOB | lowest | auc | 3 | +0.0030 | [+0.0009, +0.0064] | 0.213 | 3/3 |
| sweep-sample_scale-0.3 | adult | Influence | lowest | 5 % | 3 | +0.0041 | [-0.0075, +0.0193] | 0.659 | 2/3 |
| sweep-sample_scale-0.3 | adult | Influence | lowest | 10 % | 3 | +0.0032 | [+0.0002, +0.0048] | 0.163 | 3/3 |
| sweep-sample_scale-0.3 | adult | Influence | lowest | 20 % | 3 | +0.0023 | [-0.0114, +0.0206] | 0.829 | 1/3 |
| sweep-sample_scale-0.3 | adult | Influence | lowest | auc | 3 | +0.0028 | [-0.0030, +0.0101] | 0.543 | 2/3 |
| sweep-sample_scale-0.3 | adult | KNNShapley | lowest | 5 % | 3 | -0.0028 | [-0.0078, +0.0050] | 0.552 | 1/3 |
| sweep-sample_scale-0.3 | adult | KNNShapley | lowest | 10 % | 3 | -0.0017 | [-0.0039, +0.0026] | 0.505 | 1/3 |
| sweep-sample_scale-0.3 | adult | KNNShapley | lowest | 20 % | 3 | -0.0141 | [-0.0403, +0.0209] | 0.521 | 1/3 |
| sweep-sample_scale-0.3 | adult | KNNShapley | lowest | auc | 3 | -0.0049 | [-0.0105, +0.0050] | 0.430 | 1/3 |
| sweep-sample_scale-0.3 | adult | LOO | lowest | 5 % | 3 | +0.0012 | [-0.0034, +0.0039] | 0.655 | 2/3 |
| sweep-sample_scale-0.3 | adult | LOO | lowest | 10 % | 3 | +0.0026 | [-0.0017, +0.0094] | 0.527 | 2/3 |
| sweep-sample_scale-0.3 | adult | LOO | lowest | 20 % | 3 | +0.0129 | [+0.0008, +0.0372] | 0.398 | 3/3 |
| sweep-sample_scale-0.3 | adult | LOO | lowest | auc | 3 | +0.0045 | [+0.0003, +0.0085] | 0.197 | 3/3 |
| sweep-sample_scale-0.3 | adult | LissaInfluence | lowest | 5 % | 3 | +0.0009 | [-0.0118, +0.0090] | 0.899 | 2/3 |
| sweep-sample_scale-0.3 | adult | LissaInfluence | lowest | 10 % | 3 | +0.0053 | [+0.0014, +0.0082] | 0.122 | 3/3 |
| sweep-sample_scale-0.3 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0067 | [-0.0301, +0.0067] | 0.626 | 2/3 |
| sweep-sample_scale-0.3 | adult | LissaInfluence | lowest | auc | 3 | +0.0005 | [-0.0081, +0.0062] | 0.913 | 2/3 |
| sweep-sample_scale-0.3 | adult | LossHigh | lowest | 5 % | 3 | +0.0033 | [-0.0026, +0.0076] | 0.395 | 2/3 |
| sweep-sample_scale-0.3 | adult | LossHigh | lowest | 10 % | 3 | +0.0038 | [-0.0048, +0.0102] | 0.484 | 2/3 |
| sweep-sample_scale-0.3 | adult | LossHigh | lowest | 20 % | 3 | +0.0022 | [-0.0033, +0.0051] | 0.507 | 2/3 |
| sweep-sample_scale-0.3 | adult | LossHigh | lowest | auc | 3 | +0.0028 | [+0.0013, +0.0044] | 0.092 | 3/3 |
| sweep-valuation_epochs-10 | adult | LOO | lowest | 5 % | 3 | -0.0043 | [-0.0127, +0.0097] | 0.604 | 1/3 |
| sweep-valuation_epochs-10 | adult | LOO | lowest | 10 % | 3 | -0.0001 | [-0.0110, +0.0075] | 0.987 | 2/3 |
| sweep-valuation_epochs-10 | adult | LOO | lowest | 20 % | 3 | +0.0044 | [-0.0092, +0.0265] | 0.733 | 1/3 |
| sweep-valuation_epochs-10 | adult | LOO | lowest | auc | 3 | -0.0000 | [-0.0076, +0.0102] | 0.997 | 1/3 |
| sweep-valuation_epochs-60 | adult | LOO | lowest | 5 % | 3 | +0.0032 | [-0.0031, +0.0095] | 0.471 | 2/3 |
| sweep-valuation_epochs-60 | adult | LOO | lowest | 10 % | 3 | -0.0001 | [-0.0101, +0.0104] | 0.982 | 1/3 |
| sweep-valuation_epochs-60 | adult | LOO | lowest | 20 % | 3 | +0.0020 | [-0.0126, +0.0168] | 0.837 | 2/3 |
| sweep-valuation_epochs-60 | adult | LOO | lowest | auc | 3 | +0.0012 | [-0.0025, +0.0063] | 0.683 | 1/3 |
| sysnoise10 | adult | DataOOB | lowest | 5 % | 3 | -0.0034 | [-0.0071, +0.0002] | 0.250 | 1/3 |
| sysnoise10 | adult | DataOOB | lowest | 10 % | 3 | -0.0016 | [-0.0083, +0.0057] | 0.734 | 1/3 |
| sysnoise10 | adult | DataOOB | lowest | 20 % | 3 | -0.0202 | [-0.0406, -0.0030] | 0.206 | 0/3 |
| sysnoise10 | adult | DataOOB | lowest | auc | 3 | -0.0065 | [-0.0141, +0.0014] | 0.284 | 1/3 |
| sysnoise10 | adult | Influence | lowest | 5 % | 3 | -0.0010 | [-0.0098, +0.0041] | 0.837 | 2/3 |
| sysnoise10 | adult | Influence | lowest | 10 % | 3 | +0.0035 | [-0.0081, +0.0138] | 0.641 | 2/3 |
| sysnoise10 | adult | Influence | lowest | 20 % | 3 | -0.0024 | [-0.0125, +0.0066] | 0.703 | 1/3 |
| sysnoise10 | adult | Influence | lowest | auc | 3 | +0.0004 | [-0.0058, +0.0075] | 0.922 | 1/3 |
| sysnoise10 | adult | KNNShapley | lowest | 5 % | 3 | +0.0029 | [+0.0010, +0.0060] | 0.212 | 3/3 |
| sysnoise10 | adult | KNNShapley | lowest | 10 % | 3 | -0.0005 | [-0.0044, +0.0026] | 0.827 | 2/3 |
| sysnoise10 | adult | KNNShapley | lowest | 20 % | 3 | -0.0123 | [-0.0169, -0.0033] | 0.111 | 0/3 |
| sysnoise10 | adult | KNNShapley | lowest | auc | 3 | -0.0025 | [-0.0056, +0.0008] | 0.303 | 1/3 |
| sysnoise10 | adult | LissaInfluence | lowest | 5 % | 3 | -0.0033 | [-0.0227, +0.0175] | 0.800 | 1/3 |
| sysnoise10 | adult | LissaInfluence | lowest | 10 % | 3 | +0.0068 | [-0.0101, +0.0255] | 0.579 | 2/3 |
| sysnoise10 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0012 | [-0.0161, +0.0204] | 0.925 | 1/3 |
| sysnoise10 | adult | LissaInfluence | lowest | auc | 3 | +0.0014 | [-0.0114, +0.0190] | 0.891 | 1/3 |
| sysnoise10 | adult | LossHigh | lowest | 5 % | 3 | +0.0003 | [-0.0059, +0.0098] | 0.962 | 1/3 |
| sysnoise10 | adult | LossHigh | lowest | 10 % | 3 | -0.0070 | [-0.0326, +0.0095] | 0.643 | 2/3 |
| sysnoise10 | adult | LossHigh | lowest | 20 % | 3 | -0.0218 | [-0.0488, +0.0049] | 0.295 | 1/3 |
| sysnoise10 | adult | LossHigh | lowest | auc | 3 | -0.0080 | [-0.0259, +0.0072] | 0.494 | 1/3 |
| sysnoise10 | covertype | DataOOB | lowest | 5 % | 3 | +0.0065 | [+0.0002, +0.0148] | 0.275 | 3/3 |
| sysnoise10 | covertype | DataOOB | lowest | 10 % | 3 | +0.0141 | [-0.0036, +0.0414] | 0.417 | 2/3 |
| sysnoise10 | covertype | DataOOB | lowest | 20 % | 3 | +0.0044 | [-0.0096, +0.0172] | 0.628 | 2/3 |
| sysnoise10 | covertype | DataOOB | lowest | auc | 3 | +0.0080 | [+0.0001, +0.0209] | 0.345 | 3/3 |
| sysnoise10 | covertype | KNNShapley | lowest | 5 % | 3 | -0.0073 | [-0.0168, +0.0046] | 0.364 | 1/3 |
| sysnoise10 | covertype | KNNShapley | lowest | 10 % | 3 | +0.0149 | [-0.0030, +0.0454] | 0.432 | 2/3 |
| sysnoise10 | covertype | KNNShapley | lowest | 20 % | 3 | -0.0159 | [-0.0174, -0.0148] | 0.002 | 0/3 |
| sysnoise10 | covertype | KNNShapley | lowest | auc | 3 | -0.0002 | [-0.0075, +0.0091] | 0.969 | 1/3 |
| sysnoise10 | covertype | LissaInfluence | lowest | 5 % | 3 | -0.0001 | [-0.0062, +0.0044] | 0.970 | 2/3 |
| sysnoise10 | covertype | LissaInfluence | lowest | 10 % | 3 | +0.0069 | [-0.0094, +0.0360] | 0.684 | 1/3 |
| sysnoise10 | covertype | LissaInfluence | lowest | 20 % | 3 | -0.0412 | [-0.0624, -0.0202] | 0.077 | 0/3 |
| sysnoise10 | covertype | LissaInfluence | lowest | auc | 3 | -0.0078 | [-0.0207, +0.0088] | 0.467 | 1/3 |
| sysnoise10 | covertype | LossHigh | lowest | 5 % | 3 | -0.0021 | [-0.0088, +0.0104] | 0.766 | 1/3 |
| sysnoise10 | covertype | LossHigh | lowest | 10 % | 3 | +0.0133 | [-0.0026, +0.0420] | 0.451 | 2/3 |
| sysnoise10 | covertype | LossHigh | lowest | 20 % | 3 | -0.0056 | [-0.0112, +0.0008] | 0.250 | 1/3 |
| sysnoise10 | covertype | LossHigh | lowest | auc | 3 | +0.0031 | [-0.0060, +0.0186] | 0.731 | 1/3 |
| sysnoise10 | housing | DataOOB | lowest | 5 % | 3 | +719.0291 | [-603.1127, +2287.7757] | 0.484 | 2/3 |
| sysnoise10 | housing | DataOOB | lowest | 10 % | 3 | -738.7783 | [-2439.6941, +228.1392] | 0.478 | 1/3 |
| sysnoise10 | housing | DataOOB | lowest | 20 % | 3 | +951.6019 | [-483.9244, +3233.8242] | 0.496 | 2/3 |
| sysnoise10 | housing | DataOOB | lowest | auc | 3 | +140.6159 | [-38.9995, +465.5147] | 0.479 | 1/3 |
| sysnoise10 | housing | Influence | lowest | 5 % | 3 | +1982.4657 | [+765.0941, +4314.5411] | 0.231 | 3/3 |
| sysnoise10 | housing | Influence | lowest | 10 % | 3 | +2406.8096 | [+1903.0323, +2949.9630] | 0.015 | 3/3 |
| sysnoise10 | housing | Influence | lowest | 20 % | 3 | +3327.9036 | [+164.3346, +7918.0326] | 0.292 | 3/3 |
| sysnoise10 | housing | Influence | lowest | auc | 3 | +2230.1459 | [+1338.5933, +3771.7806] | 0.102 | 3/3 |
| sysnoise10 | housing | LissaInfluence | lowest | 5 % | 3 | +7088.0474 | [+5134.1934, +8484.6765] | 0.020 | 3/3 |
| sysnoise10 | housing | LissaInfluence | lowest | 10 % | 3 | +11320.8359 | [+9559.5044, +14129.2381] | 0.015 | 3/3 |
| sysnoise10 | housing | LissaInfluence | lowest | 20 % | 3 | +9409.5236 | [+7545.8591, +11125.1696] | 0.012 | 3/3 |
| sysnoise10 | housing | LissaInfluence | lowest | auc | 3 | +8369.7062 | [+6754.8273, +9809.0189] | 0.011 | 3/3 |
| sysnoise10 | housing | LossHigh | lowest | 5 % | 3 | +3117.8325 | [+329.9824, +5192.6029] | 0.164 | 3/3 |
| sysnoise10 | housing | LossHigh | lowest | 10 % | 3 | +3908.2607 | [+1820.2384, +5127.9969] | 0.065 | 3/3 |
| sysnoise10 | housing | LossHigh | lowest | 20 % | 3 | +5672.0770 | [+4090.5348, +7263.8964] | 0.025 | 3/3 |
| sysnoise10 | housing | LossHigh | lowest | auc | 3 | +3663.0752 | [+2896.3343, +4296.1769] | 0.012 | 3/3 |
| sysnoise10 | wine | DataOOB | lowest | 5 % | 3 | +0.0107 | [-0.0041, +0.0246] | 0.325 | 2/3 |
| sysnoise10 | wine | DataOOB | lowest | 10 % | 3 | +0.0101 | [-0.0111, +0.0444] | 0.617 | 1/3 |
| sysnoise10 | wine | DataOOB | lowest | 20 % | 3 | -0.0126 | [-0.0367, +0.0077] | 0.433 | 1/3 |
| sysnoise10 | wine | DataOOB | lowest | auc | 3 | +0.0033 | [-0.0072, +0.0174] | 0.693 | 1/3 |
| sysnoise10 | wine | Influence | lowest | 5 % | 3 | +0.0142 | [+0.0003, +0.0287] | 0.225 | 3/3 |
| sysnoise10 | wine | Influence | lowest | 10 % | 3 | +0.0285 | [+0.0064, +0.0450] | 0.131 | 3/3 |
| sysnoise10 | wine | Influence | lowest | 20 % | 3 | +0.0195 | [+0.0098, +0.0317] | 0.093 | 3/3 |
| sysnoise10 | wine | Influence | lowest | auc | 3 | +0.0191 | [+0.0049, +0.0282] | 0.117 | 3/3 |
| sysnoise10 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0474 | [+0.0196, +0.0646] | 0.078 | 3/3 |
| sysnoise10 | wine | LissaInfluence | lowest | 10 % | 3 | +0.0750 | [+0.0389, +0.0979] | 0.055 | 3/3 |
| sysnoise10 | wine | LissaInfluence | lowest | 20 % | 3 | +0.0365 | [+0.0181, +0.0544] | 0.073 | 3/3 |
| sysnoise10 | wine | LissaInfluence | lowest | auc | 3 | +0.0491 | [+0.0331, +0.0574] | 0.026 | 3/3 |
| sysnoise10 | wine | LossHigh | lowest | 5 % | 3 | +0.0126 | [+0.0057, +0.0228] | 0.135 | 3/3 |
| sysnoise10 | wine | LossHigh | lowest | 10 % | 3 | +0.0238 | [+0.0159, +0.0294] | 0.028 | 3/3 |
| sysnoise10 | wine | LossHigh | lowest | 20 % | 3 | +0.0072 | [-0.0080, +0.0218] | 0.490 | 2/3 |
| sysnoise10 | wine | LossHigh | lowest | auc | 3 | +0.0139 | [+0.0135, +0.0144] | 0.000 | 3/3 |
| sysnoise20 | adult | DataOOB | lowest | 5 % | 3 | -0.0040 | [-0.0112, +0.0066] | 0.538 | 1/3 |
| sysnoise20 | adult | DataOOB | lowest | 10 % | 3 | -0.0020 | [-0.0050, +0.0006] | 0.341 | 1/3 |
| sysnoise20 | adult | DataOOB | lowest | 20 % | 3 | -0.0139 | [-0.0176, -0.0086] | 0.036 | 0/3 |
| sysnoise20 | adult | DataOOB | lowest | auc | 3 | -0.0052 | [-0.0073, -0.0025] | 0.065 | 0/3 |
| sysnoise20 | adult | Influence | lowest | 5 % | 3 | +0.0029 | [-0.0085, +0.0165] | 0.724 | 2/3 |
| sysnoise20 | adult | Influence | lowest | 10 % | 3 | -0.0030 | [-0.0073, +0.0032] | 0.448 | 1/3 |
| sysnoise20 | adult | Influence | lowest | 20 % | 3 | -0.0032 | [-0.0134, +0.0064] | 0.636 | 1/3 |
| sysnoise20 | adult | Influence | lowest | auc | 3 | -0.0012 | [-0.0046, +0.0030] | 0.650 | 1/3 |
| sysnoise20 | adult | KNNShapley | lowest | 5 % | 3 | -0.0037 | [-0.0086, +0.0014] | 0.328 | 1/3 |
| sysnoise20 | adult | KNNShapley | lowest | 10 % | 3 | -0.0083 | [-0.0144, -0.0002] | 0.189 | 0/3 |
| sysnoise20 | adult | KNNShapley | lowest | 20 % | 3 | -0.0279 | [-0.0347, -0.0197] | 0.024 | 0/3 |
| sysnoise20 | adult | KNNShapley | lowest | auc | 3 | -0.0110 | [-0.0149, -0.0084] | 0.031 | 0/3 |
| sysnoise20 | adult | LissaInfluence | lowest | 5 % | 3 | -0.0119 | [-0.0219, -0.0011] | 0.188 | 0/3 |
| sysnoise20 | adult | LissaInfluence | lowest | 10 % | 3 | -0.0117 | [-0.0193, -0.0036] | 0.124 | 0/3 |
| sysnoise20 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0205 | [-0.0382, -0.0041] | 0.173 | 0/3 |
| sysnoise20 | adult | LissaInfluence | lowest | auc | 3 | -0.0125 | [-0.0199, -0.0026] | 0.136 | 0/3 |
| sysnoise20 | adult | LossHigh | lowest | 5 % | 3 | -0.0014 | [-0.0145, +0.0178] | 0.897 | 1/3 |
| sysnoise20 | adult | LossHigh | lowest | 10 % | 3 | -0.0092 | [-0.0130, -0.0067] | 0.040 | 0/3 |
| sysnoise20 | adult | LossHigh | lowest | 20 % | 3 | -0.0257 | [-0.0360, -0.0141] | 0.056 | 0/3 |
| sysnoise20 | adult | LossHigh | lowest | auc | 3 | -0.0102 | [-0.0151, -0.0039] | 0.090 | 0/3 |
| sysnoise20 | covertype | DataOOB | lowest | 5 % | 3 | +0.0091 | [-0.0318, +0.0504] | 0.737 | 2/3 |
| sysnoise20 | covertype | DataOOB | lowest | 10 % | 3 | +0.0567 | [+0.0494, +0.0676] | 0.009 | 3/3 |
| sysnoise20 | covertype | DataOOB | lowest | 20 % | 3 | +0.0516 | [+0.0486, +0.0536] | 0.001 | 3/3 |
| sysnoise20 | covertype | DataOOB | lowest | auc | 3 | +0.0365 | [+0.0305, +0.0445] | 0.013 | 3/3 |
| sysnoise20 | covertype | KNNShapley | lowest | 5 % | 3 | +0.0112 | [-0.0206, +0.0622] | 0.706 | 1/3 |
| sysnoise20 | covertype | KNNShapley | lowest | 10 % | 3 | +0.0519 | [+0.0436, +0.0596] | 0.008 | 3/3 |
| sysnoise20 | covertype | KNNShapley | lowest | 20 % | 3 | +0.0280 | [+0.0242, +0.0304] | 0.005 | 3/3 |
| sysnoise20 | covertype | KNNShapley | lowest | auc | 3 | +0.0292 | [+0.0232, +0.0395] | 0.030 | 3/3 |
| sysnoise20 | covertype | LissaInfluence | lowest | 5 % | 3 | +0.0105 | [-0.0152, +0.0424] | 0.597 | 2/3 |
| sysnoise20 | covertype | LissaInfluence | lowest | 10 % | 3 | +0.0409 | [+0.0242, +0.0686] | 0.099 | 3/3 |
| sysnoise20 | covertype | LissaInfluence | lowest | 20 % | 3 | +0.0125 | [-0.0104, +0.0248] | 0.390 | 2/3 |
| sysnoise20 | covertype | LissaInfluence | lowest | auc | 3 | +0.0211 | [+0.0098, +0.0281] | 0.066 | 3/3 |
| sysnoise20 | covertype | LossHigh | lowest | 5 % | 3 | +0.0190 | [-0.0238, +0.0686] | 0.553 | 2/3 |
| sysnoise20 | covertype | LossHigh | lowest | 10 % | 3 | +0.0505 | [+0.0382, +0.0672] | 0.028 | 3/3 |
| sysnoise20 | covertype | LossHigh | lowest | 20 % | 3 | +0.0398 | [+0.0266, +0.0472] | 0.027 | 3/3 |
| sysnoise20 | covertype | LossHigh | lowest | auc | 3 | +0.0336 | [+0.0270, +0.0433] | 0.021 | 3/3 |
| sysnoise20 | housing | DataOOB | lowest | 5 % | 3 | +4579.0434 | [+3570.5263, +6419.2025] | 0.038 | 3/3 |
| sysnoise20 | housing | DataOOB | lowest | 10 % | 3 | +5110.5036 | [+4537.4548, +6045.2006] | 0.008 | 3/3 |
| sysnoise20 | housing | DataOOB | lowest | 20 % | 3 | +7649.6118 | [+4999.3616, +10966.0282] | 0.049 | 3/3 |
| sysnoise20 | housing | DataOOB | lowest | auc | 3 | +4973.6026 | [+4409.4222, +5379.9029] | 0.003 | 3/3 |
| sysnoise20 | housing | Influence | lowest | 5 % | 3 | +3900.5069 | [+2472.5019, +5091.3695] | 0.036 | 3/3 |
| sysnoise20 | housing | Influence | lowest | 10 % | 3 | +4505.5693 | [+1865.1626, +6086.8433] | 0.077 | 3/3 |
| sysnoise20 | housing | Influence | lowest | 20 % | 3 | +7515.2158 | [+4691.6083, +12412.0255] | 0.092 | 3/3 |
| sysnoise20 | housing | Influence | lowest | auc | 3 | +4543.5191 | [+2678.0648, +6658.4150] | 0.059 | 3/3 |
| sysnoise20 | housing | LissaInfluence | lowest | 5 % | 3 | +6883.5669 | [+4909.7125, +7930.2688] | 0.020 | 3/3 |
| sysnoise20 | housing | LissaInfluence | lowest | 10 % | 3 | +13040.2039 | [+11942.8479, +13667.4565] | 0.002 | 3/3 |
| sysnoise20 | housing | LissaInfluence | lowest | 20 % | 3 | +21353.0661 | [+19832.9588, +22348.4269] | 0.001 | 3/3 |
| sysnoise20 | housing | LissaInfluence | lowest | auc | 3 | +11949.2347 | [+11419.3748, +12488.4983] | 0.001 | 3/3 |
| sysnoise20 | housing | LossHigh | lowest | 5 % | 3 | +4616.3309 | [+353.3697, +8971.8569] | 0.205 | 3/3 |
| sysnoise20 | housing | LossHigh | lowest | 10 % | 3 | +9321.4320 | [+6396.0801, +12275.2820] | 0.032 | 3/3 |
| sysnoise20 | housing | LossHigh | lowest | 20 % | 3 | +13239.5312 | [+10073.5166, +18509.4865] | 0.038 | 3/3 |
| sysnoise20 | housing | LossHigh | lowest | auc | 3 | +7959.5025 | [+6047.8507, +11473.5666] | 0.046 | 3/3 |
| sysnoise20 | wine | DataOOB | lowest | 5 % | 3 | -0.0031 | [-0.0105, +0.0043] | 0.549 | 1/3 |
| sysnoise20 | wine | DataOOB | lowest | 10 % | 3 | -0.0063 | [-0.0148, +0.0092] | 0.501 | 1/3 |
| sysnoise20 | wine | DataOOB | lowest | 20 % | 3 | +0.0081 | [-0.0049, +0.0270] | 0.490 | 2/3 |
| sysnoise20 | wine | DataOOB | lowest | auc | 3 | -0.0011 | [-0.0076, +0.0113] | 0.876 | 1/3 |
| sysnoise20 | wine | Influence | lowest | 5 % | 3 | +0.0107 | [+0.0042, +0.0151] | 0.084 | 3/3 |
| sysnoise20 | wine | Influence | lowest | 10 % | 3 | +0.0189 | [+0.0103, +0.0267] | 0.058 | 3/3 |
| sysnoise20 | wine | Influence | lowest | 20 % | 3 | +0.0370 | [+0.0192, +0.0546] | 0.069 | 3/3 |
| sysnoise20 | wine | Influence | lowest | auc | 3 | +0.0190 | [+0.0097, +0.0249] | 0.056 | 3/3 |
| sysnoise20 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0370 | [+0.0330, +0.0393] | 0.003 | 3/3 |
| sysnoise20 | wine | LissaInfluence | lowest | 10 % | 3 | +0.0436 | [+0.0235, +0.0559] | 0.050 | 3/3 |
| sysnoise20 | wine | LissaInfluence | lowest | 20 % | 3 | +0.0819 | [+0.0730, +0.0942] | 0.006 | 3/3 |
| sysnoise20 | wine | LissaInfluence | lowest | auc | 3 | +0.0461 | [+0.0369, +0.0527] | 0.010 | 3/3 |
| sysnoise20 | wine | LossHigh | lowest | 5 % | 3 | +0.0116 | [-0.0078, +0.0214] | 0.354 | 2/3 |
| sysnoise20 | wine | LossHigh | lowest | 10 % | 3 | +0.0323 | [+0.0276, +0.0375] | 0.008 | 3/3 |
| sysnoise20 | wine | LossHigh | lowest | 20 % | 3 | +0.0355 | [+0.0344, +0.0364] | 0.000 | 3/3 |
| sysnoise20 | wine | LossHigh | lowest | auc | 3 | +0.0239 | [+0.0189, +0.0280] | 0.012 | 3/3 |
| sysnoise5 | adult | DataOOB | lowest | 5 % | 3 | -0.0005 | [-0.0076, +0.0055] | 0.916 | 2/3 |
| sysnoise5 | adult | DataOOB | lowest | 10 % | 3 | -0.0000 | [-0.0119, +0.0197] | 0.997 | 1/3 |
| sysnoise5 | adult | DataOOB | lowest | 20 % | 3 | -0.0039 | [-0.0119, +0.0045] | 0.496 | 1/3 |
| sysnoise5 | adult | DataOOB | lowest | auc | 3 | -0.0011 | [-0.0072, +0.0099] | 0.859 | 1/3 |
| sysnoise5 | adult | Influence | lowest | 5 % | 3 | -0.0033 | [-0.0068, +0.0002] | 0.245 | 1/3 |
| sysnoise5 | adult | Influence | lowest | 10 % | 3 | -0.0027 | [-0.0076, +0.0044] | 0.537 | 1/3 |
| sysnoise5 | adult | Influence | lowest | 20 % | 3 | +0.0058 | [+0.0036, +0.0095] | 0.092 | 3/3 |
| sysnoise5 | adult | Influence | lowest | auc | 3 | -0.0004 | [-0.0027, +0.0041] | 0.879 | 1/3 |
| sysnoise5 | adult | KNNShapley | lowest | 5 % | 3 | -0.0060 | [-0.0101, -0.0021] | 0.120 | 0/3 |
| sysnoise5 | adult | KNNShapley | lowest | 10 % | 3 | -0.0077 | [-0.0118, +0.0000] | 0.184 | 1/3 |
| sysnoise5 | adult | KNNShapley | lowest | 20 % | 3 | -0.0128 | [-0.0293, +0.0011] | 0.286 | 1/3 |
| sysnoise5 | adult | KNNShapley | lowest | auc | 3 | -0.0076 | [-0.0142, -0.0012] | 0.183 | 0/3 |
| sysnoise5 | adult | LissaInfluence | lowest | 5 % | 3 | -0.0029 | [-0.0158, +0.0086] | 0.725 | 1/3 |
| sysnoise5 | adult | LissaInfluence | lowest | 10 % | 3 | -0.0138 | [-0.0332, +0.0044] | 0.331 | 1/3 |
| sysnoise5 | adult | LissaInfluence | lowest | 20 % | 3 | -0.0151 | [-0.0375, -0.0039] | 0.309 | 0/3 |
| sysnoise5 | adult | LissaInfluence | lowest | auc | 3 | -0.0097 | [-0.0258, +0.0028] | 0.370 | 1/3 |
| sysnoise5 | adult | LossHigh | lowest | 5 % | 3 | +0.0029 | [-0.0091, +0.0171] | 0.741 | 2/3 |
| sysnoise5 | adult | LossHigh | lowest | 10 % | 3 | -0.0009 | [-0.0093, +0.0152] | 0.918 | 1/3 |
| sysnoise5 | adult | LossHigh | lowest | 20 % | 3 | -0.0044 | [-0.0106, -0.0011] | 0.297 | 0/3 |
| sysnoise5 | adult | LossHigh | lowest | auc | 3 | -0.0007 | [-0.0060, +0.0096] | 0.902 | 1/3 |
| sysnoise5 | covertype | DataOOB | lowest | 5 % | 3 | +0.0067 | [+0.0046, +0.0094] | 0.041 | 3/3 |
| sysnoise5 | covertype | DataOOB | lowest | 10 % | 3 | +0.0071 | [-0.0024, +0.0124] | 0.274 | 2/3 |
| sysnoise5 | covertype | DataOOB | lowest | 20 % | 3 | +0.0099 | [+0.0018, +0.0194] | 0.192 | 3/3 |
| sysnoise5 | covertype | DataOOB | lowest | auc | 3 | +0.0068 | [+0.0036, +0.0103] | 0.071 | 3/3 |
| sysnoise5 | covertype | KNNShapley | lowest | 5 % | 3 | +0.0002 | [-0.0046, +0.0060] | 0.954 | 1/3 |
| sysnoise5 | covertype | KNNShapley | lowest | 10 % | 3 | -0.0043 | [-0.0102, -0.0010] | 0.279 | 0/3 |
| sysnoise5 | covertype | KNNShapley | lowest | 20 % | 3 | -0.0179 | [-0.0258, -0.0084] | 0.072 | 0/3 |
| sysnoise5 | covertype | KNNShapley | lowest | auc | 3 | -0.0061 | [-0.0072, -0.0039] | 0.030 | 0/3 |
| sysnoise5 | covertype | LissaInfluence | lowest | 5 % | 3 | -0.0031 | [-0.0052, +0.0006] | 0.236 | 1/3 |
| sysnoise5 | covertype | LissaInfluence | lowest | 10 % | 3 | -0.0136 | [-0.0146, -0.0120] | 0.004 | 0/3 |
| sysnoise5 | covertype | LissaInfluence | lowest | 20 % | 3 | -0.0394 | [-0.0600, -0.0190] | 0.080 | 0/3 |
| sysnoise5 | covertype | LissaInfluence | lowest | auc | 3 | -0.0157 | [-0.0203, -0.0105] | 0.031 | 0/3 |
| sysnoise5 | covertype | LossHigh | lowest | 5 % | 3 | +0.0069 | [-0.0032, +0.0174] | 0.364 | 2/3 |
| sysnoise5 | covertype | LossHigh | lowest | 10 % | 3 | +0.0022 | [-0.0036, +0.0134] | 0.732 | 1/3 |
| sysnoise5 | covertype | LossHigh | lowest | 20 % | 3 | -0.0001 | [-0.0018, +0.0034] | 0.973 | 1/3 |
| sysnoise5 | covertype | LossHigh | lowest | auc | 3 | +0.0025 | [-0.0011, +0.0089] | 0.511 | 1/3 |
| sysnoise5 | housing | DataOOB | lowest | 5 % | 3 | +713.8513 | [+311.4143, +1168.3144] | 0.103 | 3/3 |
| sysnoise5 | housing | DataOOB | lowest | 10 % | 3 | -356.6845 | [-786.3352, +276.3611] | 0.385 | 1/3 |
| sysnoise5 | housing | DataOOB | lowest | 20 % | 3 | -431.4857 | [-1526.0885, +215.8809] | 0.515 | 2/3 |
| sysnoise5 | housing | DataOOB | lowest | auc | 3 | -63.1653 | [-426.0956, +185.4266] | 0.766 | 2/3 |
| sysnoise5 | housing | Influence | lowest | 5 % | 3 | +1950.3768 | [+1269.8915, +2973.9722] | 0.065 | 3/3 |
| sysnoise5 | housing | Influence | lowest | 10 % | 3 | +2046.6421 | [+978.9746, +3927.6219] | 0.162 | 3/3 |
| sysnoise5 | housing | Influence | lowest | 20 % | 3 | +2057.7258 | [+609.7234, +2949.9927] | 0.106 | 3/3 |
| sysnoise5 | housing | Influence | lowest | auc | 3 | +1769.5164 | [+921.3630, +2953.8495] | 0.101 | 3/3 |
| sysnoise5 | housing | LissaInfluence | lowest | 5 % | 3 | +6007.8428 | [+4634.2016, +8091.4214] | 0.030 | 3/3 |
| sysnoise5 | housing | LissaInfluence | lowest | 10 % | 3 | +4065.7437 | [+2642.3946, +6048.6878] | 0.058 | 3/3 |
| sysnoise5 | housing | LissaInfluence | lowest | 20 % | 3 | +1702.4402 | [+794.9205, +2255.8652] | 0.065 | 3/3 |
| sysnoise5 | housing | LissaInfluence | lowest | auc | 3 | +3452.2247 | [+2663.5821, +4855.0796] | 0.039 | 3/3 |
| sysnoise5 | housing | LossHigh | lowest | 5 % | 3 | +3466.0234 | [+3387.9716, +3608.1711] | 0.000 | 3/3 |
| sysnoise5 | housing | LossHigh | lowest | 10 % | 3 | +3283.8526 | [+2204.0852, +4898.4631] | 0.057 | 3/3 |
| sysnoise5 | housing | LossHigh | lowest | 20 % | 3 | +3302.0653 | [+2599.0240, +3784.8938] | 0.012 | 3/3 |
| sysnoise5 | housing | LossHigh | lowest | auc | 3 | +2923.4669 | [+2323.2809, +3633.6290] | 0.017 | 3/3 |
| sysnoise5 | wine | DataOOB | lowest | 5 % | 3 | -0.0112 | [-0.0248, +0.0001] | 0.264 | 1/3 |
| sysnoise5 | wine | DataOOB | lowest | 10 % | 3 | -0.0105 | [-0.0165, -0.0036] | 0.109 | 0/3 |
| sysnoise5 | wine | DataOOB | lowest | 20 % | 3 | -0.0004 | [-0.0126, +0.0138] | 0.963 | 1/3 |
| sysnoise5 | wine | DataOOB | lowest | auc | 3 | -0.0068 | [-0.0155, +0.0021] | 0.313 | 1/3 |
| sysnoise5 | wine | Influence | lowest | 5 % | 3 | -0.0017 | [-0.0053, +0.0053] | 0.669 | 1/3 |
| sysnoise5 | wine | Influence | lowest | 10 % | 3 | +0.0064 | [-0.0017, +0.0118] | 0.262 | 2/3 |
| sysnoise5 | wine | Influence | lowest | 20 % | 3 | +0.0184 | [+0.0036, +0.0263] | 0.131 | 3/3 |
| sysnoise5 | wine | Influence | lowest | auc | 3 | +0.0066 | [-0.0010, +0.0113] | 0.229 | 2/3 |
| sysnoise5 | wine | LissaInfluence | lowest | 5 % | 3 | +0.0284 | [+0.0196, +0.0452] | 0.077 | 3/3 |
| sysnoise5 | wine | LissaInfluence | lowest | 10 % | 3 | +0.0349 | [+0.0294, +0.0453] | 0.021 | 3/3 |
| sysnoise5 | wine | LissaInfluence | lowest | 20 % | 3 | +0.0267 | [-0.0015, +0.0451] | 0.204 | 2/3 |
| sysnoise5 | wine | LissaInfluence | lowest | auc | 3 | +0.0268 | [+0.0252, +0.0279] | 0.001 | 3/3 |
| sysnoise5 | wine | LossHigh | lowest | 5 % | 3 | -0.0002 | [-0.0046, +0.0029] | 0.931 | 2/3 |
| sysnoise5 | wine | LossHigh | lowest | 10 % | 3 | +0.0020 | [-0.0003, +0.0036] | 0.234 | 2/3 |
| sysnoise5 | wine | LossHigh | lowest | 20 % | 3 | +0.0192 | [+0.0110, +0.0239] | 0.043 | 3/3 |
| sysnoise5 | wine | LossHigh | lowest | auc | 3 | +0.0055 | [+0.0044, +0.0076] | 0.037 | 3/3 |
| transfer-catboost | adult | any.DataOOB | lowest | 5 % | 3 | +0.0028 | [-0.0033, +0.0100] | 0.553 | 2/3 |
| transfer-catboost | adult | any.DataOOB | lowest | 10 % | 3 | -0.0020 | [-0.0074, +0.0037] | 0.589 | 1/3 |
| transfer-catboost | adult | any.DataOOB | lowest | 20 % | 3 | +0.0016 | [-0.0031, +0.0091] | 0.706 | 1/3 |
| transfer-catboost | adult | any.DataOOB | lowest | auc | 3 | +0.0003 | [-0.0044, +0.0062] | 0.924 | 1/3 |
| transfer-catboost | adult | any.KNNShapley | lowest | 5 % | 3 | +0.0040 | [-0.0000, +0.0108] | 0.368 | 2/3 |
| transfer-catboost | adult | any.KNNShapley | lowest | 10 % | 3 | -0.0062 | [-0.0172, +0.0026] | 0.397 | 1/3 |
| transfer-catboost | adult | any.KNNShapley | lowest | 20 % | 3 | -0.0075 | [-0.0150, +0.0030] | 0.301 | 1/3 |
| transfer-catboost | adult | any.KNNShapley | lowest | auc | 3 | -0.0032 | [-0.0091, +0.0044] | 0.505 | 1/3 |
| transfer-catboost | adult | catboost.CatBoostLFC | lowest | 5 % | 3 | +0.0075 | [+0.0018, +0.0125] | 0.139 | 3/3 |
| transfer-catboost | adult | catboost.CatBoostLFC | lowest | 10 % | 3 | +0.0052 | [+0.0000, +0.0144] | 0.380 | 3/3 |
| transfer-catboost | adult | catboost.CatBoostLFC | lowest | 20 % | 3 | +0.0067 | [-0.0024, +0.0177] | 0.371 | 2/3 |
| transfer-catboost | adult | catboost.CatBoostLFC | lowest | auc | 3 | +0.0055 | [-0.0001, +0.0129] | 0.294 | 2/3 |
| transfer-catboost | adult | catboost.LOO | lowest | 5 % | 3 | +0.0032 | [-0.0025, +0.0122] | 0.561 | 1/3 |
| transfer-catboost | adult | catboost.LOO | lowest | 10 % | 3 | -0.0023 | [-0.0118, +0.0083] | 0.736 | 1/3 |
| transfer-catboost | adult | catboost.LOO | lowest | 20 % | 3 | +0.0014 | [-0.0100, +0.0098] | 0.830 | 2/3 |
| transfer-catboost | adult | catboost.LOO | lowest | auc | 3 | +0.0003 | [-0.0070, +0.0086] | 0.952 | 1/3 |
| transfer-catboost | adult | catboost.LossHigh | lowest | 5 % | 3 | +0.0059 | [-0.0034, +0.0145] | 0.372 | 2/3 |
| transfer-catboost | adult | catboost.LossHigh | lowest | 10 % | 3 | -0.0001 | [-0.0073, +0.0051] | 0.972 | 2/3 |
| transfer-catboost | adult | catboost.LossHigh | lowest | 20 % | 3 | -0.0064 | [-0.0134, +0.0012] | 0.267 | 1/3 |
| transfer-catboost | adult | catboost.LossHigh | lowest | auc | 3 | -0.0002 | [-0.0069, +0.0038] | 0.961 | 2/3 |
| transfer-catboost | adult | distill-lightgbm.Influence | lowest | 5 % | 3 | +0.0045 | [+0.0035, +0.0063] | 0.037 | 3/3 |
| transfer-catboost | adult | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0011 | [-0.0047, +0.0042] | 0.751 | 2/3 |
| transfer-catboost | adult | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0027 | [+0.0011, +0.0035] | 0.078 | 3/3 |
| transfer-catboost | adult | distill-lightgbm.Influence | lowest | auc | 3 | +0.0022 | [+0.0001, +0.0033] | 0.176 | 3/3 |
| transfer-catboost | adult | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0044 | [+0.0007, +0.0093] | 0.228 | 3/3 |
| transfer-catboost | adult | distill-lightgbm.LossHigh | lowest | 10 % | 3 | -0.0007 | [-0.0039, +0.0020] | 0.715 | 1/3 |
| transfer-catboost | adult | distill-lightgbm.LossHigh | lowest | 20 % | 3 | -0.0053 | [-0.0142, +0.0060] | 0.465 | 1/3 |
| transfer-catboost | adult | distill-lightgbm.LossHigh | lowest | auc | 3 | -0.0005 | [-0.0048, +0.0046] | 0.870 | 1/3 |
| transfer-catboost | adult | lightgbm.LOO | lowest | 5 % | 3 | +0.0058 | [-0.0007, +0.0182] | 0.444 | 2/3 |
| transfer-catboost | adult | lightgbm.LOO | lowest | 10 % | 3 | -0.0013 | [-0.0150, +0.0097] | 0.873 | 2/3 |
| transfer-catboost | adult | lightgbm.LOO | lowest | 20 % | 3 | -0.0029 | [-0.0152, +0.0141] | 0.773 | 1/3 |
| transfer-catboost | adult | lightgbm.LOO | lowest | auc | 3 | +0.0002 | [-0.0094, +0.0117] | 0.972 | 1/3 |
| transfer-catboost | adult | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0001 | [-0.0049, +0.0065] | 0.973 | 1/3 |
| transfer-catboost | adult | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0013 | [-0.0050, +0.0062] | 0.735 | 2/3 |
| transfer-catboost | adult | lightgbm.LossHigh | lowest | 20 % | 3 | -0.0018 | [-0.0108, +0.0049] | 0.741 | 2/3 |
| transfer-catboost | adult | lightgbm.LossHigh | lowest | auc | 3 | +0.0001 | [-0.0058, +0.0041] | 0.983 | 2/3 |
| transfer-catboost | adult | pytorch.Influence | lowest | 5 % | 3 | +0.0048 | [+0.0006, +0.0111] | 0.273 | 3/3 |
| transfer-catboost | adult | pytorch.Influence | lowest | 10 % | 3 | +0.0065 | [-0.0015, +0.0217] | 0.482 | 1/3 |
| transfer-catboost | adult | pytorch.Influence | lowest | 20 % | 3 | +0.0052 | [-0.0061, +0.0209] | 0.587 | 2/3 |
| transfer-catboost | adult | pytorch.Influence | lowest | auc | 3 | +0.0049 | [-0.0014, +0.0161] | 0.472 | 2/3 |
| transfer-catboost | adult | pytorch.LOO | lowest | 5 % | 3 | +0.0054 | [-0.0025, +0.0098] | 0.306 | 2/3 |
| transfer-catboost | adult | pytorch.LOO | lowest | 10 % | 3 | -0.0027 | [-0.0080, +0.0051] | 0.565 | 1/3 |
| transfer-catboost | adult | pytorch.LOO | lowest | 20 % | 3 | +0.0001 | [-0.0048, +0.0070] | 0.972 | 1/3 |
| transfer-catboost | adult | pytorch.LOO | lowest | auc | 3 | +0.0004 | [-0.0041, +0.0059] | 0.913 | 1/3 |
| transfer-catboost | adult | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0092 | [+0.0046, +0.0147] | 0.089 | 3/3 |
| transfer-catboost | adult | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0035 | [-0.0045, +0.0146] | 0.600 | 2/3 |
| transfer-catboost | adult | pytorch.LissaInfluence | lowest | 20 % | 3 | +0.0014 | [-0.0022, +0.0067] | 0.664 | 1/3 |
| transfer-catboost | adult | pytorch.LissaInfluence | lowest | auc | 3 | +0.0040 | [+0.0003, +0.0108] | 0.366 | 3/3 |
| transfer-catboost | adult | pytorch.LossHigh | lowest | 5 % | 3 | +0.0085 | [+0.0039, +0.0138] | 0.099 | 3/3 |
| transfer-catboost | adult | pytorch.LossHigh | lowest | 10 % | 3 | -0.0032 | [-0.0050, -0.0002] | 0.165 | 0/3 |
| transfer-catboost | adult | pytorch.LossHigh | lowest | 20 % | 3 | -0.0012 | [-0.0078, +0.0096] | 0.850 | 1/3 |
| transfer-catboost | adult | pytorch.LossHigh | lowest | auc | 3 | +0.0006 | [-0.0026, +0.0058] | 0.836 | 1/3 |
| transfer-catboost | adult | random_forest.LOO | lowest | 5 % | 3 | -0.0001 | [-0.0148, +0.0179] | 0.990 | 1/3 |
| transfer-catboost | adult | random_forest.LOO | lowest | 10 % | 3 | +0.0018 | [-0.0043, +0.0136] | 0.784 | 1/3 |
| transfer-catboost | adult | random_forest.LOO | lowest | 20 % | 3 | -0.0016 | [-0.0133, +0.0135] | 0.861 | 1/3 |
| transfer-catboost | adult | random_forest.LOO | lowest | auc | 3 | +0.0003 | [-0.0086, +0.0130] | 0.971 | 1/3 |
| transfer-catboost | adult | random_forest.LossHigh | lowest | 5 % | 3 | +0.0009 | [-0.0086, +0.0121] | 0.898 | 1/3 |
| transfer-catboost | adult | random_forest.LossHigh | lowest | 10 % | 3 | -0.0037 | [-0.0075, +0.0027] | 0.371 | 1/3 |
| transfer-catboost | adult | random_forest.LossHigh | lowest | 20 % | 3 | -0.0015 | [-0.0114, +0.0049] | 0.801 | 2/3 |
| transfer-catboost | adult | random_forest.LossHigh | lowest | auc | 3 | -0.0015 | [-0.0078, +0.0046] | 0.711 | 1/3 |
| transfer-catboost | adult | xgboost.LOO | lowest | 5 % | 3 | +0.0051 | [+0.0007, +0.0083] | 0.152 | 3/3 |
| transfer-catboost | adult | xgboost.LOO | lowest | 10 % | 3 | -0.0015 | [-0.0087, +0.0065] | 0.767 | 1/3 |
| transfer-catboost | adult | xgboost.LOO | lowest | 20 % | 3 | +0.0008 | [-0.0039, +0.0091] | 0.869 | 1/3 |
| transfer-catboost | adult | xgboost.LOO | lowest | auc | 3 | +0.0009 | [-0.0038, +0.0068] | 0.798 | 1/3 |
| transfer-catboost | adult | xgboost.LossHigh | lowest | 5 % | 3 | +0.0013 | [-0.0017, +0.0058] | 0.623 | 1/3 |
| transfer-catboost | adult | xgboost.LossHigh | lowest | 10 % | 3 | +0.0014 | [-0.0058, +0.0082] | 0.768 | 2/3 |
| transfer-catboost | adult | xgboost.LossHigh | lowest | 20 % | 3 | -0.0016 | [-0.0121, +0.0039] | 0.795 | 2/3 |
| transfer-catboost | adult | xgboost.LossHigh | lowest | auc | 3 | +0.0005 | [-0.0056, +0.0054] | 0.901 | 2/3 |
| transfer-catboost | covertype | any.DataOOB | lowest | 5 % | 3 | +0.0083 | [+0.0028, +0.0142] | 0.129 | 3/3 |
| transfer-catboost | covertype | any.DataOOB | lowest | 10 % | 3 | +0.0077 | [+0.0018, +0.0120] | 0.127 | 3/3 |
| transfer-catboost | covertype | any.DataOOB | lowest | 20 % | 3 | +0.0124 | [+0.0044, +0.0210] | 0.123 | 3/3 |
| transfer-catboost | covertype | any.DataOOB | lowest | auc | 3 | +0.0081 | [+0.0056, +0.0095] | 0.023 | 3/3 |
| transfer-catboost | covertype | any.KNNShapley | lowest | 5 % | 3 | +0.0097 | [+0.0046, +0.0128] | 0.063 | 3/3 |
| transfer-catboost | covertype | any.KNNShapley | lowest | 10 % | 3 | +0.0073 | [-0.0046, +0.0158] | 0.357 | 2/3 |
| transfer-catboost | covertype | any.KNNShapley | lowest | 20 % | 3 | +0.0051 | [-0.0020, +0.0114] | 0.322 | 2/3 |
| transfer-catboost | covertype | any.KNNShapley | lowest | auc | 3 | +0.0064 | [+0.0043, +0.0083] | 0.031 | 3/3 |
| transfer-catboost | covertype | catboost.LOO | lowest | 5 % | 3 | -0.0008 | [-0.0068, +0.0038] | 0.823 | 2/3 |
| transfer-catboost | covertype | catboost.LOO | lowest | 10 % | 3 | +0.0017 | [-0.0034, +0.0072] | 0.629 | 2/3 |
| transfer-catboost | covertype | catboost.LOO | lowest | 20 % | 3 | -0.0027 | [-0.0122, +0.0054] | 0.655 | 1/3 |
| transfer-catboost | covertype | catboost.LOO | lowest | auc | 3 | -0.0002 | [-0.0015, +0.0006] | 0.767 | 2/3 |
| transfer-catboost | covertype | catboost.LossHigh | lowest | 5 % | 3 | +0.0031 | [-0.0016, +0.0072] | 0.346 | 2/3 |
| transfer-catboost | covertype | catboost.LossHigh | lowest | 10 % | 3 | +0.0071 | [-0.0020, +0.0174] | 0.337 | 2/3 |
| transfer-catboost | covertype | catboost.LossHigh | lowest | 20 % | 3 | +0.0075 | [+0.0014, +0.0150] | 0.199 | 3/3 |
| transfer-catboost | covertype | catboost.LossHigh | lowest | auc | 3 | +0.0053 | [+0.0018, +0.0087] | 0.117 | 3/3 |
| transfer-catboost | covertype | distill-lightgbm.Influence | lowest | 5 % | 3 | +0.0035 | [+0.0018, +0.0062] | 0.128 | 3/3 |
| transfer-catboost | covertype | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0063 | [-0.0036, +0.0122] | 0.334 | 2/3 |
| transfer-catboost | covertype | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0029 | [-0.0020, +0.0082] | 0.434 | 2/3 |
| transfer-catboost | covertype | distill-lightgbm.Influence | lowest | auc | 3 | +0.0039 | [+0.0013, +0.0056] | 0.098 | 3/3 |
| transfer-catboost | covertype | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0059 | [+0.0012, +0.0098] | 0.143 | 3/3 |
| transfer-catboost | covertype | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0106 | [+0.0064, +0.0172] | 0.087 | 3/3 |
| transfer-catboost | covertype | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0220 | [+0.0166, +0.0270] | 0.018 | 3/3 |
| transfer-catboost | covertype | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0110 | [+0.0083, +0.0131] | 0.016 | 3/3 |
| transfer-catboost | covertype | lightgbm.LOO | lowest | 5 % | 3 | +0.0022 | [+0.0004, +0.0042] | 0.184 | 3/3 |
| transfer-catboost | covertype | lightgbm.LOO | lowest | 10 % | 3 | -0.0074 | [-0.0122, -0.0008] | 0.162 | 0/3 |
| transfer-catboost | covertype | lightgbm.LOO | lowest | 20 % | 3 | -0.0003 | [-0.0048, +0.0032] | 0.921 | 2/3 |
| transfer-catboost | covertype | lightgbm.LOO | lowest | auc | 3 | -0.0023 | [-0.0032, -0.0010] | 0.073 | 0/3 |
| transfer-catboost | covertype | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0057 | [+0.0002, +0.0154] | 0.365 | 3/3 |
| transfer-catboost | covertype | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0064 | [+0.0008, +0.0166] | 0.337 | 3/3 |
| transfer-catboost | covertype | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0118 | [+0.0050, +0.0192] | 0.103 | 3/3 |
| transfer-catboost | covertype | lightgbm.LossHigh | lowest | auc | 3 | +0.0068 | [+0.0035, +0.0113] | 0.102 | 3/3 |
| transfer-catboost | covertype | pytorch.Influence | lowest | 5 % | 3 | +0.0049 | [-0.0008, +0.0102] | 0.266 | 2/3 |
| transfer-catboost | covertype | pytorch.Influence | lowest | 10 % | 3 | +0.0023 | [-0.0020, +0.0074] | 0.484 | 2/3 |
| transfer-catboost | covertype | pytorch.Influence | lowest | 20 % | 3 | +0.0039 | [-0.0072, +0.0130] | 0.575 | 2/3 |
| transfer-catboost | covertype | pytorch.Influence | lowest | auc | 3 | +0.0031 | [+0.0023, +0.0035] | 0.016 | 3/3 |
| transfer-catboost | covertype | pytorch.LOO | lowest | 5 % | 3 | +0.0034 | [-0.0056, +0.0130] | 0.592 | 2/3 |
| transfer-catboost | covertype | pytorch.LOO | lowest | 10 % | 3 | +0.0029 | [-0.0038, +0.0088] | 0.515 | 2/3 |
| transfer-catboost | covertype | pytorch.LOO | lowest | 20 % | 3 | +0.0028 | [-0.0070, +0.0098] | 0.635 | 2/3 |
| transfer-catboost | covertype | pytorch.LOO | lowest | auc | 3 | +0.0026 | [+0.0007, +0.0048] | 0.159 | 3/3 |
| transfer-catboost | covertype | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0050 | [-0.0014, +0.0140] | 0.393 | 2/3 |
| transfer-catboost | covertype | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0045 | [-0.0172, +0.0234] | 0.741 | 2/3 |
| transfer-catboost | covertype | pytorch.LissaInfluence | lowest | 20 % | 3 | -0.0001 | [-0.0032, +0.0042] | 0.979 | 1/3 |
| transfer-catboost | covertype | pytorch.LissaInfluence | lowest | auc | 3 | +0.0029 | [-0.0061, +0.0133] | 0.659 | 2/3 |
| transfer-catboost | covertype | pytorch.LossHigh | lowest | 5 % | 3 | +0.0100 | [+0.0034, +0.0178] | 0.140 | 3/3 |
| transfer-catboost | covertype | pytorch.LossHigh | lowest | 10 % | 3 | +0.0115 | [-0.0004, +0.0178] | 0.193 | 2/3 |
| transfer-catboost | covertype | pytorch.LossHigh | lowest | 20 % | 3 | +0.0183 | [+0.0172, +0.0204] | 0.003 | 3/3 |
| transfer-catboost | covertype | pytorch.LossHigh | lowest | auc | 3 | +0.0114 | [+0.0064, +0.0154] | 0.050 | 3/3 |
| transfer-catboost | covertype | random_forest.LOO | lowest | 5 % | 3 | +0.0022 | [-0.0014, +0.0076] | 0.508 | 2/3 |
| transfer-catboost | covertype | random_forest.LOO | lowest | 10 % | 3 | +0.0037 | [-0.0014, +0.0072] | 0.294 | 2/3 |
| transfer-catboost | covertype | random_forest.LOO | lowest | 20 % | 3 | -0.0001 | [-0.0056, +0.0046] | 0.984 | 2/3 |
| transfer-catboost | covertype | random_forest.LOO | lowest | auc | 3 | +0.0019 | [+0.0014, +0.0025] | 0.029 | 3/3 |
| transfer-catboost | covertype | random_forest.LossHigh | lowest | 5 % | 3 | +0.0071 | [+0.0020, +0.0162] | 0.263 | 3/3 |
| transfer-catboost | covertype | random_forest.LossHigh | lowest | 10 % | 3 | +0.0036 | [-0.0032, +0.0126] | 0.523 | 2/3 |
| transfer-catboost | covertype | random_forest.LossHigh | lowest | 20 % | 3 | +0.0055 | [+0.0028, +0.0090] | 0.097 | 3/3 |
| transfer-catboost | covertype | random_forest.LossHigh | lowest | auc | 3 | +0.0045 | [+0.0003, +0.0099] | 0.257 | 3/3 |
| transfer-catboost | covertype | xgboost.LOO | lowest | 5 % | 3 | +0.0075 | [+0.0028, +0.0122] | 0.111 | 3/3 |
| transfer-catboost | covertype | xgboost.LOO | lowest | 10 % | 3 | -0.0003 | [-0.0076, +0.0076] | 0.957 | 1/3 |
| transfer-catboost | covertype | xgboost.LOO | lowest | 20 % | 3 | +0.0007 | [-0.0028, +0.0054] | 0.792 | 1/3 |
| transfer-catboost | covertype | xgboost.LOO | lowest | auc | 3 | +0.0020 | [+0.0003, +0.0052] | 0.353 | 3/3 |
| transfer-catboost | covertype | xgboost.LossHigh | lowest | 5 % | 3 | +0.0042 | [-0.0036, +0.0120] | 0.449 | 2/3 |
| transfer-catboost | covertype | xgboost.LossHigh | lowest | 10 % | 3 | +0.0039 | [+0.0002, +0.0104] | 0.359 | 3/3 |
| transfer-catboost | covertype | xgboost.LossHigh | lowest | 20 % | 3 | +0.0042 | [-0.0010, +0.0124] | 0.418 | 2/3 |
| transfer-catboost | covertype | xgboost.LossHigh | lowest | auc | 3 | +0.0035 | [+0.0017, +0.0066] | 0.150 | 3/3 |
| transfer-catboost | housing | any.DataOOB | lowest | 5 % | 3 | +24.6136 | [-441.3428, +395.5612] | 0.929 | 2/3 |
| transfer-catboost | housing | any.DataOOB | lowest | 10 % | 3 | +628.2457 | [+123.6250, +993.4884] | 0.137 | 3/3 |
| transfer-catboost | housing | any.DataOOB | lowest | 20 % | 3 | +752.7081 | [+200.3652, +1430.7696] | 0.172 | 3/3 |
| transfer-catboost | housing | any.DataOOB | lowest | auc | 3 | +429.9226 | [+293.7161, +628.1958] | 0.051 | 3/3 |
| transfer-catboost | housing | catboost.CatBoostLFC | lowest | 5 % | 3 | +65.4427 | [-419.9297, +376.1546] | 0.815 | 2/3 |
| transfer-catboost | housing | catboost.CatBoostLFC | lowest | 10 % | 3 | -233.3696 | [-945.6264, +415.5591] | 0.614 | 1/3 |
| transfer-catboost | housing | catboost.CatBoostLFC | lowest | 20 % | 3 | -878.1415 | [-1631.7184, -64.1442] | 0.192 | 0/3 |
| transfer-catboost | housing | catboost.CatBoostLFC | lowest | auc | 3 | -290.6883 | [-867.5219, +233.8373] | 0.458 | 1/3 |
| transfer-catboost | housing | catboost.LOO | lowest | 5 % | 3 | +181.0700 | [-202.3457, +550.0185] | 0.492 | 2/3 |
| transfer-catboost | housing | catboost.LOO | lowest | 10 % | 3 | +388.5239 | [-502.5437, +1097.2304] | 0.496 | 2/3 |
| transfer-catboost | housing | catboost.LOO | lowest | 20 % | 3 | +952.1327 | [+720.6158, +1269.6605] | 0.028 | 3/3 |
| transfer-catboost | housing | catboost.LOO | lowest | auc | 3 | +428.9971 | [-22.5098, +729.1200] | 0.203 | 2/3 |
| transfer-catboost | housing | catboost.LossHigh | lowest | 5 % | 3 | -288.4241 | [-637.5971, +58.4906] | 0.288 | 1/3 |
| transfer-catboost | housing | catboost.LossHigh | lowest | 10 % | 3 | +553.9986 | [-62.5957, +960.2575] | 0.219 | 2/3 |
| transfer-catboost | housing | catboost.LossHigh | lowest | 20 % | 3 | -987.6153 | [-1708.7695, -600.1616] | 0.112 | 0/3 |
| transfer-catboost | housing | catboost.LossHigh | lowest | auc | 3 | -111.2604 | [-332.9131, +125.0764] | 0.489 | 1/3 |
| transfer-catboost | housing | distill-lightgbm.Influence | lowest | 5 % | 3 | -265.9682 | [-387.5731, -159.0823] | 0.057 | 0/3 |
| transfer-catboost | housing | distill-lightgbm.Influence | lowest | 10 % | 3 | -263.9269 | [-1069.1880, +185.6702] | 0.580 | 2/3 |
| transfer-catboost | housing | distill-lightgbm.Influence | lowest | 20 % | 3 | -470.2793 | [-944.7262, +318.4101] | 0.358 | 1/3 |
| transfer-catboost | housing | distill-lightgbm.Influence | lowest | auc | 3 | -283.0344 | [-734.0204, +86.4166] | 0.360 | 1/3 |
| transfer-catboost | housing | distill-lightgbm.LossHigh | lowest | 5 % | 3 | -163.2163 | [-379.5161, +15.2709] | 0.293 | 1/3 |
| transfer-catboost | housing | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +651.9291 | [-25.6847, +1142.0315] | 0.203 | 2/3 |
| transfer-catboost | housing | distill-lightgbm.LossHigh | lowest | 20 % | 3 | -665.0904 | [-995.7016, -370.1636] | 0.067 | 0/3 |
| transfer-catboost | housing | distill-lightgbm.LossHigh | lowest | auc | 3 | +37.3967 | [-197.0517, +183.1542] | 0.782 | 2/3 |
| transfer-catboost | housing | lightgbm.LOO | lowest | 5 % | 3 | -219.6876 | [-856.5480, +384.5844] | 0.603 | 1/3 |
| transfer-catboost | housing | lightgbm.LOO | lowest | 10 % | 3 | +260.3903 | [-308.9410, +679.3149] | 0.471 | 2/3 |
| transfer-catboost | housing | lightgbm.LOO | lowest | 20 % | 3 | +817.3513 | [+394.0835, +1465.7059] | 0.131 | 3/3 |
| transfer-catboost | housing | lightgbm.LOO | lowest | auc | 3 | +247.0623 | [-181.9237, +574.3948] | 0.385 | 2/3 |
| transfer-catboost | housing | lightgbm.LossHigh | lowest | 5 % | 3 | +104.5254 | [-349.4539, +483.3558] | 0.709 | 2/3 |
| transfer-catboost | housing | lightgbm.LossHigh | lowest | 10 % | 3 | +675.6095 | [+127.9341, +999.0552] | 0.134 | 3/3 |
| transfer-catboost | housing | lightgbm.LossHigh | lowest | 20 % | 3 | +102.6742 | [-53.5621, +191.7825] | 0.320 | 2/3 |
| transfer-catboost | housing | lightgbm.LossHigh | lowest | auc | 3 | +305.1534 | [+8.5574, +482.0941] | 0.178 | 3/3 |
| transfer-catboost | housing | pytorch.Influence | lowest | 5 % | 3 | -35.6090 | [-467.2200, +262.9318] | 0.887 | 2/3 |
| transfer-catboost | housing | pytorch.Influence | lowest | 10 % | 3 | +80.4612 | [-914.2495, +741.3751] | 0.888 | 2/3 |
| transfer-catboost | housing | pytorch.Influence | lowest | 20 % | 3 | -169.0679 | [-633.2269, +102.2511] | 0.544 | 2/3 |
| transfer-catboost | housing | pytorch.Influence | lowest | auc | 3 | -20.9963 | [-617.9553, +308.3239] | 0.950 | 2/3 |
| transfer-catboost | housing | pytorch.LOO | lowest | 5 % | 3 | -101.2647 | [-454.2027, +360.2328] | 0.716 | 1/3 |
| transfer-catboost | housing | pytorch.LOO | lowest | 10 % | 3 | +96.5300 | [-227.1479, +661.0527] | 0.766 | 1/3 |
| transfer-catboost | housing | pytorch.LOO | lowest | 20 % | 3 | +387.0155 | [+286.8515, +499.6418] | 0.025 | 3/3 |
| transfer-catboost | housing | pytorch.LOO | lowest | auc | 3 | +107.6365 | [-74.0304, +409.6658] | 0.552 | 1/3 |
| transfer-catboost | housing | pytorch.LissaInfluence | lowest | 5 % | 3 | +677.5556 | [+7.5896, +1108.0443] | 0.184 | 3/3 |
| transfer-catboost | housing | pytorch.LissaInfluence | lowest | 10 % | 3 | +800.4042 | [+152.8733, +1617.5369] | 0.205 | 3/3 |
| transfer-catboost | housing | pytorch.LissaInfluence | lowest | 20 % | 3 | +316.9069 | [-651.6472, +1019.6759] | 0.591 | 2/3 |
| transfer-catboost | housing | pytorch.LissaInfluence | lowest | auc | 3 | +548.7672 | [+302.8973, +1029.2604] | 0.150 | 3/3 |
| transfer-catboost | housing | pytorch.LossHigh | lowest | 5 % | 3 | -348.7476 | [-466.9295, -213.1614] | 0.042 | 0/3 |
| transfer-catboost | housing | pytorch.LossHigh | lowest | 10 % | 3 | +741.4699 | [-118.5112, +1451.8079] | 0.248 | 2/3 |
| transfer-catboost | housing | pytorch.LossHigh | lowest | 20 % | 3 | -458.2383 | [-661.2042, -247.7329] | 0.062 | 0/3 |
| transfer-catboost | housing | pytorch.LossHigh | lowest | auc | 3 | +76.3047 | [-223.1073, +374.6932] | 0.702 | 2/3 |
| transfer-catboost | housing | random_forest.LOO | lowest | 5 % | 3 | +5.1148 | [-268.1018, +234.4799] | 0.975 | 2/3 |
| transfer-catboost | housing | random_forest.LOO | lowest | 10 % | 3 | +340.6117 | [-331.8934, +874.4870] | 0.439 | 2/3 |
| transfer-catboost | housing | random_forest.LOO | lowest | 20 % | 3 | +917.4751 | [+692.5328, +1071.7204] | 0.015 | 3/3 |
| transfer-catboost | housing | random_forest.LOO | lowest | auc | 3 | +358.3769 | [-18.3523, +654.4827] | 0.213 | 2/3 |
| transfer-catboost | housing | random_forest.LossHigh | lowest | 5 % | 3 | -21.7893 | [-523.7946, +356.1993] | 0.941 | 2/3 |
| transfer-catboost | housing | random_forest.LossHigh | lowest | 10 % | 3 | +605.9540 | [+40.9376, +999.8085] | 0.172 | 3/3 |
| transfer-catboost | housing | random_forest.LossHigh | lowest | 20 % | 3 | +351.8906 | [+26.0128, +662.9141] | 0.196 | 3/3 |
| transfer-catboost | housing | random_forest.LossHigh | lowest | auc | 3 | +309.7580 | [+50.1315, +470.4812] | 0.142 | 3/3 |
| transfer-catboost | housing | xgboost.LOO | lowest | 5 % | 3 | -78.8932 | [-222.0686, +26.8512] | 0.399 | 1/3 |
| transfer-catboost | housing | xgboost.LOO | lowest | 10 % | 3 | -1.5088 | [-325.2909, +200.5364] | 0.993 | 2/3 |
| transfer-catboost | housing | xgboost.LOO | lowest | 20 % | 3 | +656.7398 | [+375.2679, +1032.4394] | 0.078 | 3/3 |
| transfer-catboost | housing | xgboost.LOO | lowest | auc | 3 | +143.8958 | [-83.6843, +309.9081] | 0.346 | 2/3 |
| transfer-catboost | housing | xgboost.LossHigh | lowest | 5 % | 3 | -24.9416 | [-269.8605, +262.3633] | 0.887 | 1/3 |
| transfer-catboost | housing | xgboost.LossHigh | lowest | 10 % | 3 | -12.7237 | [-803.4154, +575.3833] | 0.978 | 2/3 |
| transfer-catboost | housing | xgboost.LossHigh | lowest | 20 % | 3 | +609.0182 | [+309.9228, +909.3504] | 0.072 | 3/3 |
| transfer-catboost | housing | xgboost.LossHigh | lowest | auc | 3 | +141.2477 | [-291.2652, +508.6971] | 0.606 | 2/3 |
| transfer-catboost | wine | any.DataOOB | lowest | 5 % | 3 | +0.0073 | [-0.0038, +0.0202] | 0.406 | 2/3 |
| transfer-catboost | wine | any.DataOOB | lowest | 10 % | 3 | +0.0034 | [-0.0020, +0.0062] | 0.338 | 2/3 |
| transfer-catboost | wine | any.DataOOB | lowest | 20 % | 3 | +0.0065 | [-0.0005, +0.0135] | 0.249 | 2/3 |
| transfer-catboost | wine | any.DataOOB | lowest | auc | 3 | +0.0047 | [+0.0016, +0.0072] | 0.102 | 3/3 |
| transfer-catboost | wine | catboost.CatBoostLFC | lowest | 5 % | 3 | +0.0051 | [-0.0095, +0.0212] | 0.626 | 2/3 |
| transfer-catboost | wine | catboost.CatBoostLFC | lowest | 10 % | 3 | +0.0027 | [-0.0025, +0.0060] | 0.413 | 2/3 |
| transfer-catboost | wine | catboost.CatBoostLFC | lowest | 20 % | 3 | +0.0088 | [+0.0045, +0.0113] | 0.055 | 3/3 |
| transfer-catboost | wine | catboost.CatBoostLFC | lowest | auc | 3 | +0.0045 | [-0.0006, +0.0103] | 0.296 | 2/3 |
| transfer-catboost | wine | catboost.LOO | lowest | 5 % | 3 | -0.0202 | [-0.0540, -0.0001] | 0.356 | 0/3 |
| transfer-catboost | wine | catboost.LOO | lowest | 10 % | 3 | -0.0206 | [-0.0670, +0.0050] | 0.469 | 2/3 |
| transfer-catboost | wine | catboost.LOO | lowest | 20 % | 3 | -0.0173 | [-0.0761, +0.0184] | 0.618 | 2/3 |
| transfer-catboost | wine | catboost.LOO | lowest | auc | 3 | -0.0171 | [-0.0576, +0.0064] | 0.489 | 1/3 |
| transfer-catboost | wine | catboost.LossHigh | lowest | 5 % | 3 | +0.0070 | [-0.0004, +0.0194] | 0.380 | 2/3 |
| transfer-catboost | wine | catboost.LossHigh | lowest | 10 % | 3 | +0.0056 | [+0.0010, +0.0094] | 0.150 | 3/3 |
| transfer-catboost | wine | catboost.LossHigh | lowest | 20 % | 3 | +0.0069 | [-0.0011, +0.0142] | 0.262 | 2/3 |
| transfer-catboost | wine | catboost.LossHigh | lowest | auc | 3 | +0.0056 | [+0.0044, +0.0070] | 0.017 | 3/3 |
| transfer-catboost | wine | distill-lightgbm.Influence | lowest | 5 % | 3 | +0.0049 | [-0.0022, +0.0176] | 0.524 | 1/3 |
| transfer-catboost | wine | distill-lightgbm.Influence | lowest | 10 % | 3 | -0.0072 | [-0.0125, -0.0023] | 0.136 | 0/3 |
| transfer-catboost | wine | distill-lightgbm.Influence | lowest | 20 % | 3 | -0.0127 | [-0.0543, +0.0098] | 0.606 | 2/3 |
| transfer-catboost | wine | distill-lightgbm.Influence | lowest | auc | 3 | -0.0046 | [-0.0139, +0.0006] | 0.423 | 1/3 |
| transfer-catboost | wine | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0094 | [-0.0010, +0.0197] | 0.257 | 2/3 |
| transfer-catboost | wine | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0012 | [-0.0007, +0.0034] | 0.414 | 2/3 |
| transfer-catboost | wine | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0073 | [+0.0031, +0.0149] | 0.195 | 3/3 |
| transfer-catboost | wine | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0046 | [+0.0002, +0.0072] | 0.170 | 3/3 |
| transfer-catboost | wine | lightgbm.LOO | lowest | 5 % | 3 | +0.0054 | [-0.0062, +0.0188] | 0.537 | 2/3 |
| transfer-catboost | wine | lightgbm.LOO | lowest | 10 % | 3 | +0.0016 | [-0.0029, +0.0098] | 0.725 | 1/3 |
| transfer-catboost | wine | lightgbm.LOO | lowest | 20 % | 3 | +0.0110 | [+0.0066, +0.0162] | 0.059 | 3/3 |
| transfer-catboost | wine | lightgbm.LOO | lowest | auc | 3 | +0.0047 | [+0.0002, +0.0100] | 0.241 | 3/3 |
| transfer-catboost | wine | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0096 | [+0.0031, +0.0206] | 0.221 | 3/3 |
| transfer-catboost | wine | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0019 | [-0.0007, +0.0060] | 0.458 | 2/3 |
| transfer-catboost | wine | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0124 | [+0.0094, +0.0157] | 0.021 | 3/3 |
| transfer-catboost | wine | lightgbm.LossHigh | lowest | auc | 3 | +0.0062 | [+0.0044, +0.0098] | 0.072 | 3/3 |
| transfer-catboost | wine | pytorch.Influence | lowest | 5 % | 3 | +0.0004 | [-0.0021, +0.0030] | 0.826 | 2/3 |
| transfer-catboost | wine | pytorch.Influence | lowest | 10 % | 3 | -0.0016 | [-0.0051, +0.0012] | 0.484 | 1/3 |
| transfer-catboost | wine | pytorch.Influence | lowest | 20 % | 3 | -0.0129 | [-0.0694, +0.0163] | 0.692 | 2/3 |
| transfer-catboost | wine | pytorch.Influence | lowest | auc | 3 | -0.0037 | [-0.0198, +0.0045] | 0.688 | 2/3 |
| transfer-catboost | wine | pytorch.LOO | lowest | 5 % | 3 | -0.0051 | [-0.0164, +0.0043] | 0.488 | 1/3 |
| transfer-catboost | wine | pytorch.LOO | lowest | 10 % | 3 | +0.0042 | [-0.0006, +0.0080] | 0.239 | 2/3 |
| transfer-catboost | wine | pytorch.LOO | lowest | 20 % | 3 | +0.0115 | [+0.0043, +0.0174] | 0.096 | 3/3 |
| transfer-catboost | wine | pytorch.LOO | lowest | auc | 3 | +0.0032 | [+0.0022, +0.0041] | 0.029 | 3/3 |
| transfer-catboost | wine | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0120 | [+0.0027, +0.0252] | 0.219 | 3/3 |
| transfer-catboost | wine | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0115 | [+0.0047, +0.0168] | 0.084 | 3/3 |
| transfer-catboost | wine | pytorch.LissaInfluence | lowest | 20 % | 3 | +0.0133 | [+0.0019, +0.0298] | 0.256 | 3/3 |
| transfer-catboost | wine | pytorch.LissaInfluence | lowest | auc | 3 | +0.0106 | [+0.0073, +0.0146] | 0.039 | 3/3 |
| transfer-catboost | wine | pytorch.LossHigh | lowest | 5 % | 3 | +0.0072 | [-0.0002, +0.0161] | 0.273 | 2/3 |
| transfer-catboost | wine | pytorch.LossHigh | lowest | 10 % | 3 | +0.0029 | [-0.0018, +0.0105] | 0.532 | 1/3 |
| transfer-catboost | wine | pytorch.LossHigh | lowest | 20 % | 3 | +0.0080 | [+0.0019, +0.0124] | 0.126 | 3/3 |
| transfer-catboost | wine | pytorch.LossHigh | lowest | auc | 3 | +0.0049 | [+0.0012, +0.0104] | 0.226 | 3/3 |
| transfer-catboost | wine | random_forest.LOO | lowest | 5 % | 3 | +0.0041 | [-0.0151, +0.0205] | 0.733 | 2/3 |
| transfer-catboost | wine | random_forest.LOO | lowest | 10 % | 3 | +0.0017 | [-0.0019, +0.0039] | 0.454 | 2/3 |
| transfer-catboost | wine | random_forest.LOO | lowest | 20 % | 3 | +0.0000 | [-0.0084, +0.0079] | 0.993 | 2/3 |
| transfer-catboost | wine | random_forest.LOO | lowest | auc | 3 | +0.0017 | [-0.0025, +0.0045] | 0.518 | 2/3 |
| transfer-catboost | wine | random_forest.LossHigh | lowest | 5 % | 3 | +0.0069 | [-0.0003, +0.0174] | 0.328 | 2/3 |
| transfer-catboost | wine | random_forest.LossHigh | lowest | 10 % | 3 | +0.0017 | [-0.0036, +0.0092] | 0.699 | 1/3 |
| transfer-catboost | wine | random_forest.LossHigh | lowest | 20 % | 3 | +0.0092 | [-0.0009, +0.0173] | 0.227 | 2/3 |
| transfer-catboost | wine | random_forest.LossHigh | lowest | auc | 3 | +0.0047 | [+0.0023, +0.0076] | 0.094 | 3/3 |
| transfer-catboost | wine | xgboost.LOO | lowest | 5 % | 3 | +0.0055 | [-0.0012, +0.0173] | 0.449 | 2/3 |
| transfer-catboost | wine | xgboost.LOO | lowest | 10 % | 3 | +0.0017 | [-0.0112, +0.0111] | 0.823 | 2/3 |
| transfer-catboost | wine | xgboost.LOO | lowest | 20 % | 3 | +0.0092 | [-0.0012, +0.0186] | 0.249 | 2/3 |
| transfer-catboost | wine | xgboost.LOO | lowest | auc | 3 | +0.0043 | [-0.0015, +0.0082] | 0.284 | 2/3 |
| transfer-catboost | wine | xgboost.LossHigh | lowest | 5 % | 3 | -0.0027 | [-0.0071, +0.0022] | 0.414 | 1/3 |
| transfer-catboost | wine | xgboost.LossHigh | lowest | 10 % | 3 | -0.0132 | [-0.0479, +0.0106] | 0.534 | 1/3 |
| transfer-catboost | wine | xgboost.LossHigh | lowest | 20 % | 3 | -0.0001 | [-0.0043, +0.0045] | 0.981 | 1/3 |
| transfer-catboost | wine | xgboost.LossHigh | lowest | auc | 3 | -0.0057 | [-0.0208, +0.0057] | 0.547 | 1/3 |
| transfer-distill-lightgbm | adult | any.DataOOB | lowest | 5 % | 3 | +0.0012 | [-0.0000, +0.0020] | 0.193 | 2/3 |
| transfer-distill-lightgbm | adult | any.DataOOB | lowest | 10 % | 3 | +0.0001 | [-0.0052, +0.0027] | 0.984 | 2/3 |
| transfer-distill-lightgbm | adult | any.DataOOB | lowest | 20 % | 3 | +0.0096 | [+0.0063, +0.0133] | 0.041 | 3/3 |
| transfer-distill-lightgbm | adult | any.DataOOB | lowest | auc | 3 | +0.0027 | [+0.0018, +0.0038] | 0.043 | 3/3 |
| transfer-distill-lightgbm | adult | any.KNNShapley | lowest | 5 % | 3 | -0.0011 | [-0.0095, +0.0054] | 0.826 | 2/3 |
| transfer-distill-lightgbm | adult | any.KNNShapley | lowest | 10 % | 3 | +0.0004 | [-0.0003, +0.0014] | 0.544 | 2/3 |
| transfer-distill-lightgbm | adult | any.KNNShapley | lowest | 20 % | 3 | -0.0121 | [-0.0234, +0.0056] | 0.311 | 1/3 |
| transfer-distill-lightgbm | adult | any.KNNShapley | lowest | auc | 3 | -0.0031 | [-0.0071, +0.0028] | 0.406 | 1/3 |
| transfer-distill-lightgbm | adult | catboost.CatBoostLFC | lowest | 5 % | 3 | -0.0085 | [-0.0231, +0.0049] | 0.406 | 1/3 |
| transfer-distill-lightgbm | adult | catboost.CatBoostLFC | lowest | 10 % | 3 | +0.0081 | [+0.0057, +0.0113] | 0.040 | 3/3 |
| transfer-distill-lightgbm | adult | catboost.CatBoostLFC | lowest | 20 % | 3 | +0.0017 | [-0.0074, +0.0108] | 0.783 | 2/3 |
| transfer-distill-lightgbm | adult | catboost.CatBoostLFC | lowest | auc | 3 | +0.0013 | [-0.0027, +0.0082] | 0.739 | 1/3 |
| transfer-distill-lightgbm | adult | catboost.LOO | lowest | 5 % | 3 | -0.0049 | [-0.0119, +0.0078] | 0.521 | 1/3 |
| transfer-distill-lightgbm | adult | catboost.LOO | lowest | 10 % | 3 | -0.0058 | [-0.0106, +0.0012] | 0.246 | 1/3 |
| transfer-distill-lightgbm | adult | catboost.LOO | lowest | 20 % | 3 | +0.0008 | [-0.0029, +0.0041] | 0.728 | 2/3 |
| transfer-distill-lightgbm | adult | catboost.LOO | lowest | auc | 3 | -0.0032 | [-0.0074, +0.0000] | 0.282 | 1/3 |
| transfer-distill-lightgbm | adult | catboost.LossHigh | lowest | 5 % | 3 | -0.0012 | [-0.0065, +0.0023] | 0.710 | 2/3 |
| transfer-distill-lightgbm | adult | catboost.LossHigh | lowest | 10 % | 3 | +0.0075 | [-0.0019, +0.0124] | 0.252 | 2/3 |
| transfer-distill-lightgbm | adult | catboost.LossHigh | lowest | 20 % | 3 | -0.0017 | [-0.0121, +0.0095] | 0.809 | 1/3 |
| transfer-distill-lightgbm | adult | catboost.LossHigh | lowest | auc | 3 | +0.0021 | [-0.0054, +0.0076] | 0.641 | 2/3 |
| transfer-distill-lightgbm | adult | distill-lightgbm.Influence | lowest | 5 % | 3 | -0.0091 | [-0.0205, +0.0027] | 0.306 | 1/3 |
| transfer-distill-lightgbm | adult | distill-lightgbm.Influence | lowest | 10 % | 3 | -0.0027 | [-0.0166, +0.0110] | 0.766 | 1/3 |
| transfer-distill-lightgbm | adult | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0044 | [-0.0014, +0.0088] | 0.280 | 2/3 |
| transfer-distill-lightgbm | adult | distill-lightgbm.Influence | lowest | auc | 3 | -0.0022 | [-0.0117, +0.0032] | 0.691 | 2/3 |
| transfer-distill-lightgbm | adult | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0034 | [+0.0007, +0.0072] | 0.229 | 3/3 |
| transfer-distill-lightgbm | adult | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0061 | [-0.0038, +0.0160] | 0.399 | 2/3 |
| transfer-distill-lightgbm | adult | distill-lightgbm.LossHigh | lowest | 20 % | 3 | -0.0051 | [-0.0115, -0.0015] | 0.252 | 0/3 |
| transfer-distill-lightgbm | adult | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0019 | [-0.0037, +0.0058] | 0.585 | 2/3 |
| transfer-distill-lightgbm | adult | lightgbm.LOO | lowest | 5 % | 3 | -0.0164 | [-0.0313, +0.0046] | 0.268 | 1/3 |
| transfer-distill-lightgbm | adult | lightgbm.LOO | lowest | 10 % | 3 | +0.0015 | [-0.0046, +0.0063] | 0.686 | 2/3 |
| transfer-distill-lightgbm | adult | lightgbm.LOO | lowest | 20 % | 3 | -0.0027 | [-0.0134, +0.0088] | 0.718 | 1/3 |
| transfer-distill-lightgbm | adult | lightgbm.LOO | lowest | auc | 3 | -0.0042 | [-0.0063, -0.0023] | 0.068 | 0/3 |
| transfer-distill-lightgbm | adult | lightgbm.LossHigh | lowest | 5 % | 3 | -0.0035 | [-0.0156, +0.0092] | 0.676 | 1/3 |
| transfer-distill-lightgbm | adult | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0001 | [-0.0083, +0.0052] | 0.990 | 2/3 |
| transfer-distill-lightgbm | adult | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0013 | [-0.0046, +0.0067] | 0.727 | 2/3 |
| transfer-distill-lightgbm | adult | lightgbm.LossHigh | lowest | auc | 3 | -0.0005 | [-0.0019, +0.0007] | 0.564 | 1/3 |
| transfer-distill-lightgbm | adult | pytorch.Influence | lowest | 5 % | 3 | +0.0041 | [-0.0020, +0.0107] | 0.379 | 2/3 |
| transfer-distill-lightgbm | adult | pytorch.Influence | lowest | 10 % | 3 | +0.0108 | [+0.0070, +0.0137] | 0.032 | 3/3 |
| transfer-distill-lightgbm | adult | pytorch.Influence | lowest | 20 % | 3 | +0.0082 | [-0.0107, +0.0222] | 0.490 | 2/3 |
| transfer-distill-lightgbm | adult | pytorch.Influence | lowest | auc | 3 | +0.0072 | [+0.0026, +0.0102] | 0.090 | 3/3 |
| transfer-distill-lightgbm | adult | pytorch.LOO | lowest | 5 % | 3 | -0.0087 | [-0.0129, -0.0023] | 0.116 | 0/3 |
| transfer-distill-lightgbm | adult | pytorch.LOO | lowest | 10 % | 3 | -0.0073 | [-0.0318, +0.0155] | 0.649 | 1/3 |
| transfer-distill-lightgbm | adult | pytorch.LOO | lowest | 20 % | 3 | -0.0185 | [-0.0314, -0.0041] | 0.144 | 0/3 |
| transfer-distill-lightgbm | adult | pytorch.LOO | lowest | auc | 3 | -0.0095 | [-0.0225, +0.0042] | 0.343 | 1/3 |
| transfer-distill-lightgbm | adult | pytorch.LissaInfluence | lowest | 5 % | 3 | -0.0080 | [-0.0127, -0.0015] | 0.139 | 0/3 |
| transfer-distill-lightgbm | adult | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0020 | [-0.0030, +0.0062] | 0.535 | 2/3 |
| transfer-distill-lightgbm | adult | pytorch.LissaInfluence | lowest | 20 % | 3 | +0.0055 | [-0.0079, +0.0243] | 0.628 | 2/3 |
| transfer-distill-lightgbm | adult | pytorch.LissaInfluence | lowest | auc | 3 | +0.0001 | [-0.0036, +0.0039] | 0.964 | 1/3 |
| transfer-distill-lightgbm | adult | pytorch.LossHigh | lowest | 5 % | 3 | -0.0009 | [-0.0074, +0.0039] | 0.810 | 2/3 |
| transfer-distill-lightgbm | adult | pytorch.LossHigh | lowest | 10 % | 3 | +0.0058 | [-0.0089, +0.0178] | 0.537 | 2/3 |
| transfer-distill-lightgbm | adult | pytorch.LossHigh | lowest | 20 % | 3 | -0.0020 | [-0.0120, +0.0114] | 0.797 | 1/3 |
| transfer-distill-lightgbm | adult | pytorch.LossHigh | lowest | auc | 3 | +0.0014 | [-0.0082, +0.0069] | 0.795 | 2/3 |
| transfer-distill-lightgbm | adult | random_forest.LOO | lowest | 5 % | 3 | -0.0100 | [-0.0142, -0.0042] | 0.080 | 0/3 |
| transfer-distill-lightgbm | adult | random_forest.LOO | lowest | 10 % | 3 | -0.0032 | [-0.0088, +0.0040] | 0.486 | 1/3 |
| transfer-distill-lightgbm | adult | random_forest.LOO | lowest | 20 % | 3 | -0.0093 | [-0.0190, +0.0078] | 0.392 | 1/3 |
| transfer-distill-lightgbm | adult | random_forest.LOO | lowest | auc | 3 | -0.0060 | [-0.0109, -0.0034] | 0.134 | 0/3 |
| transfer-distill-lightgbm | adult | random_forest.LossHigh | lowest | 5 % | 3 | -0.0039 | [-0.0053, -0.0017] | 0.071 | 0/3 |
| transfer-distill-lightgbm | adult | random_forest.LossHigh | lowest | 10 % | 3 | +0.0037 | [-0.0010, +0.0073] | 0.268 | 2/3 |
| transfer-distill-lightgbm | adult | random_forest.LossHigh | lowest | 20 % | 3 | -0.0002 | [-0.0196, +0.0125] | 0.987 | 2/3 |
| transfer-distill-lightgbm | adult | random_forest.LossHigh | lowest | auc | 3 | +0.0004 | [-0.0042, +0.0030] | 0.882 | 2/3 |
| transfer-distill-lightgbm | adult | xgboost.LOO | lowest | 5 % | 3 | -0.0113 | [-0.0123, -0.0097] | 0.005 | 0/3 |
| transfer-distill-lightgbm | adult | xgboost.LOO | lowest | 10 % | 3 | -0.0107 | [-0.0182, -0.0050] | 0.111 | 0/3 |
| transfer-distill-lightgbm | adult | xgboost.LOO | lowest | 20 % | 3 | -0.0236 | [-0.0452, -0.0023] | 0.197 | 0/3 |
| transfer-distill-lightgbm | adult | xgboost.LOO | lowest | auc | 3 | -0.0127 | [-0.0156, -0.0104] | 0.014 | 0/3 |
| transfer-distill-lightgbm | adult | xgboost.LossHigh | lowest | 5 % | 3 | -0.0025 | [-0.0055, +0.0029] | 0.452 | 1/3 |
| transfer-distill-lightgbm | adult | xgboost.LossHigh | lowest | 10 % | 3 | +0.0037 | [-0.0004, +0.0062] | 0.218 | 2/3 |
| transfer-distill-lightgbm | adult | xgboost.LossHigh | lowest | 20 % | 3 | -0.0027 | [-0.0105, +0.0023] | 0.562 | 2/3 |
| transfer-distill-lightgbm | adult | xgboost.LossHigh | lowest | auc | 3 | +0.0001 | [-0.0021, +0.0015] | 0.948 | 2/3 |
| transfer-distill-lightgbm | covertype | any.DataOOB | lowest | 5 % | 3 | -0.0005 | [-0.0068, +0.0050] | 0.891 | 2/3 |
| transfer-distill-lightgbm | covertype | any.DataOOB | lowest | 10 % | 3 | +0.0013 | [-0.0070, +0.0094] | 0.814 | 2/3 |
| transfer-distill-lightgbm | covertype | any.DataOOB | lowest | 20 % | 3 | +0.0023 | [-0.0054, +0.0090] | 0.634 | 2/3 |
| transfer-distill-lightgbm | covertype | any.DataOOB | lowest | auc | 3 | +0.0009 | [-0.0039, +0.0040] | 0.743 | 2/3 |
| transfer-distill-lightgbm | covertype | any.KNNShapley | lowest | 5 % | 3 | +0.0013 | [-0.0066, +0.0090] | 0.805 | 2/3 |
| transfer-distill-lightgbm | covertype | any.KNNShapley | lowest | 10 % | 3 | -0.0054 | [-0.0124, +0.0072] | 0.482 | 1/3 |
| transfer-distill-lightgbm | covertype | any.KNNShapley | lowest | 20 % | 3 | -0.0119 | [-0.0246, +0.0002] | 0.238 | 1/3 |
| transfer-distill-lightgbm | covertype | any.KNNShapley | lowest | auc | 3 | -0.0047 | [-0.0125, +0.0002] | 0.354 | 1/3 |
| transfer-distill-lightgbm | covertype | catboost.LOO | lowest | 5 % | 3 | -0.0031 | [-0.0060, -0.0004] | 0.199 | 0/3 |
| transfer-distill-lightgbm | covertype | catboost.LOO | lowest | 10 % | 3 | -0.0020 | [-0.0050, +0.0020] | 0.438 | 1/3 |
| transfer-distill-lightgbm | covertype | catboost.LOO | lowest | 20 % | 3 | -0.0021 | [-0.0050, +0.0010] | 0.355 | 1/3 |
| transfer-distill-lightgbm | covertype | catboost.LOO | lowest | auc | 3 | -0.0020 | [-0.0031, -0.0005] | 0.123 | 0/3 |
| transfer-distill-lightgbm | covertype | catboost.LossHigh | lowest | 5 % | 3 | -0.0038 | [-0.0072, +0.0012] | 0.275 | 1/3 |
| transfer-distill-lightgbm | covertype | catboost.LossHigh | lowest | 10 % | 3 | +0.0019 | [-0.0054, +0.0072] | 0.660 | 2/3 |
| transfer-distill-lightgbm | covertype | catboost.LossHigh | lowest | 20 % | 3 | +0.0013 | [-0.0064, +0.0090] | 0.803 | 2/3 |
| transfer-distill-lightgbm | covertype | catboost.LossHigh | lowest | auc | 3 | +0.0001 | [-0.0054, +0.0040] | 0.977 | 2/3 |
| transfer-distill-lightgbm | covertype | distill-lightgbm.Influence | lowest | 5 % | 3 | -0.0024 | [-0.0128, +0.0038] | 0.691 | 2/3 |
| transfer-distill-lightgbm | covertype | distill-lightgbm.Influence | lowest | 10 % | 3 | -0.0049 | [-0.0084, -0.0022] | 0.118 | 0/3 |
| transfer-distill-lightgbm | covertype | distill-lightgbm.Influence | lowest | 20 % | 3 | -0.0033 | [-0.0092, +0.0000] | 0.375 | 0/3 |
| transfer-distill-lightgbm | covertype | distill-lightgbm.Influence | lowest | auc | 3 | -0.0033 | [-0.0063, -0.0006] | 0.191 | 0/3 |
| transfer-distill-lightgbm | covertype | distill-lightgbm.LossHigh | lowest | 5 % | 3 | -0.0002 | [-0.0036, +0.0036] | 0.932 | 1/3 |
| transfer-distill-lightgbm | covertype | distill-lightgbm.LossHigh | lowest | 10 % | 3 | -0.0022 | [-0.0066, +0.0044] | 0.580 | 1/3 |
| transfer-distill-lightgbm | covertype | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0043 | [+0.0016, +0.0072] | 0.119 | 3/3 |
| transfer-distill-lightgbm | covertype | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0002 | [-0.0016, +0.0025] | 0.888 | 1/3 |
| transfer-distill-lightgbm | covertype | lightgbm.LOO | lowest | 5 % | 3 | -0.0003 | [-0.0048, +0.0034] | 0.922 | 2/3 |
| transfer-distill-lightgbm | covertype | lightgbm.LOO | lowest | 10 % | 3 | -0.0026 | [-0.0074, +0.0016] | 0.425 | 1/3 |
| transfer-distill-lightgbm | covertype | lightgbm.LOO | lowest | 20 % | 3 | -0.0005 | [-0.0018, +0.0018] | 0.693 | 1/3 |
| transfer-distill-lightgbm | covertype | lightgbm.LOO | lowest | auc | 3 | -0.0012 | [-0.0024, +0.0012] | 0.427 | 1/3 |
| transfer-distill-lightgbm | covertype | lightgbm.LossHigh | lowest | 5 % | 3 | -0.0007 | [-0.0040, +0.0036] | 0.794 | 1/3 |
| transfer-distill-lightgbm | covertype | lightgbm.LossHigh | lowest | 10 % | 3 | -0.0029 | [-0.0124, +0.0028] | 0.601 | 2/3 |
| transfer-distill-lightgbm | covertype | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0039 | [+0.0030, +0.0054] | 0.034 | 3/3 |
| transfer-distill-lightgbm | covertype | lightgbm.LossHigh | lowest | auc | 3 | -0.0003 | [-0.0049, +0.0033] | 0.918 | 2/3 |
| transfer-distill-lightgbm | covertype | pytorch.Influence | lowest | 5 % | 3 | -0.0015 | [-0.0080, +0.0064] | 0.761 | 1/3 |
| transfer-distill-lightgbm | covertype | pytorch.Influence | lowest | 10 % | 3 | -0.0105 | [-0.0128, -0.0084] | 0.014 | 0/3 |
| transfer-distill-lightgbm | covertype | pytorch.Influence | lowest | 20 % | 3 | -0.0036 | [-0.0142, +0.0062] | 0.604 | 1/3 |
| transfer-distill-lightgbm | covertype | pytorch.Influence | lowest | auc | 3 | -0.0052 | [-0.0087, -0.0031] | 0.097 | 0/3 |
| transfer-distill-lightgbm | covertype | pytorch.LOO | lowest | 5 % | 3 | -0.0004 | [-0.0064, +0.0068] | 0.927 | 1/3 |
| transfer-distill-lightgbm | covertype | pytorch.LOO | lowest | 10 % | 3 | -0.0039 | [-0.0106, +0.0004] | 0.374 | 1/3 |
| transfer-distill-lightgbm | covertype | pytorch.LOO | lowest | 20 % | 3 | +0.0018 | [-0.0052, +0.0102] | 0.728 | 2/3 |
| transfer-distill-lightgbm | covertype | pytorch.LOO | lowest | auc | 3 | -0.0011 | [-0.0030, +0.0013] | 0.475 | 1/3 |
| transfer-distill-lightgbm | covertype | pytorch.LissaInfluence | lowest | 5 % | 3 | -0.0051 | [-0.0112, +0.0038] | 0.377 | 1/3 |
| transfer-distill-lightgbm | covertype | pytorch.LissaInfluence | lowest | 10 % | 3 | -0.0147 | [-0.0280, -0.0056] | 0.164 | 0/3 |
| transfer-distill-lightgbm | covertype | pytorch.LissaInfluence | lowest | 20 % | 3 | -0.0206 | [-0.0314, -0.0142] | 0.063 | 0/3 |
| transfer-distill-lightgbm | covertype | pytorch.LissaInfluence | lowest | auc | 3 | -0.0119 | [-0.0204, -0.0065] | 0.108 | 0/3 |
| transfer-distill-lightgbm | covertype | pytorch.LossHigh | lowest | 5 % | 3 | -0.0013 | [-0.0068, +0.0038] | 0.706 | 1/3 |
| transfer-distill-lightgbm | covertype | pytorch.LossHigh | lowest | 10 % | 3 | +0.0038 | [+0.0018, +0.0076] | 0.184 | 3/3 |
| transfer-distill-lightgbm | covertype | pytorch.LossHigh | lowest | 20 % | 3 | +0.0025 | [-0.0006, +0.0056] | 0.302 | 2/3 |
| transfer-distill-lightgbm | covertype | pytorch.LossHigh | lowest | auc | 3 | +0.0017 | [+0.0010, +0.0023] | 0.046 | 3/3 |
| transfer-distill-lightgbm | covertype | random_forest.LOO | lowest | 5 % | 3 | -0.0017 | [-0.0112, +0.0050] | 0.756 | 2/3 |
| transfer-distill-lightgbm | covertype | random_forest.LOO | lowest | 10 % | 3 | -0.0005 | [-0.0032, +0.0028] | 0.815 | 1/3 |
| transfer-distill-lightgbm | covertype | random_forest.LOO | lowest | 20 % | 3 | -0.0024 | [-0.0092, +0.0016] | 0.555 | 2/3 |
| transfer-distill-lightgbm | covertype | random_forest.LOO | lowest | auc | 3 | -0.0012 | [-0.0040, +0.0010] | 0.502 | 1/3 |
| transfer-distill-lightgbm | covertype | random_forest.LossHigh | lowest | 5 % | 3 | -0.0056 | [-0.0130, -0.0010] | 0.273 | 0/3 |
| transfer-distill-lightgbm | covertype | random_forest.LossHigh | lowest | 10 % | 3 | -0.0030 | [-0.0054, -0.0008] | 0.153 | 0/3 |
| transfer-distill-lightgbm | covertype | random_forest.LossHigh | lowest | 20 % | 3 | -0.0046 | [-0.0084, -0.0008] | 0.171 | 0/3 |
| transfer-distill-lightgbm | covertype | random_forest.LossHigh | lowest | auc | 3 | -0.0037 | [-0.0055, -0.0022] | 0.063 | 0/3 |
| transfer-distill-lightgbm | covertype | xgboost.LOO | lowest | 5 % | 3 | +0.0027 | [+0.0010, +0.0046] | 0.120 | 3/3 |
| transfer-distill-lightgbm | covertype | xgboost.LOO | lowest | 10 % | 3 | +0.0034 | [+0.0002, +0.0064] | 0.198 | 3/3 |
| transfer-distill-lightgbm | covertype | xgboost.LOO | lowest | 20 % | 3 | +0.0009 | [-0.0072, +0.0100] | 0.878 | 1/3 |
| transfer-distill-lightgbm | covertype | xgboost.LOO | lowest | auc | 3 | +0.0022 | [-0.0002, +0.0060] | 0.381 | 2/3 |
| transfer-distill-lightgbm | covertype | xgboost.LossHigh | lowest | 5 % | 3 | +0.0015 | [-0.0068, +0.0104] | 0.796 | 2/3 |
| transfer-distill-lightgbm | covertype | xgboost.LossHigh | lowest | 10 % | 3 | -0.0009 | [-0.0072, +0.0062] | 0.844 | 1/3 |
| transfer-distill-lightgbm | covertype | xgboost.LossHigh | lowest | 20 % | 3 | +0.0000 | [-0.0024, +0.0032] | 1.000 | 1/3 |
| transfer-distill-lightgbm | covertype | xgboost.LossHigh | lowest | auc | 3 | +0.0000 | [-0.0007, +0.0004] | 0.921 | 2/3 |
| transfer-distill-lightgbm | housing | any.DataOOB | lowest | 5 % | 3 | +1433.5032 | [+979.1229, +1740.6574] | 0.025 | 3/3 |
| transfer-distill-lightgbm | housing | any.DataOOB | lowest | 10 % | 3 | +5553.8897 | [+4428.8704, +7242.0858] | 0.023 | 3/3 |
| transfer-distill-lightgbm | housing | any.DataOOB | lowest | 20 % | 3 | +5207.4013 | [+2431.6878, +6711.0285] | 0.064 | 3/3 |
| transfer-distill-lightgbm | housing | any.DataOOB | lowest | auc | 3 | +3742.9348 | [+2663.9307, +4770.8185] | 0.025 | 3/3 |
| transfer-distill-lightgbm | housing | catboost.CatBoostLFC | lowest | 5 % | 3 | -2385.5214 | [-3434.9762, -714.0734] | 0.106 | 0/3 |
| transfer-distill-lightgbm | housing | catboost.CatBoostLFC | lowest | 10 % | 3 | -1709.4571 | [-3104.2485, -748.3947] | 0.139 | 0/3 |
| transfer-distill-lightgbm | housing | catboost.CatBoostLFC | lowest | 20 % | 3 | -3757.8833 | [-5297.3420, -2680.7163] | 0.041 | 0/3 |
| transfer-distill-lightgbm | housing | catboost.CatBoostLFC | lowest | auc | 3 | -2176.8976 | [-3347.1727, -1283.0643] | 0.071 | 0/3 |
| transfer-distill-lightgbm | housing | catboost.LOO | lowest | 5 % | 3 | -1109.1805 | [-2063.6304, +250.3746] | 0.253 | 1/3 |
| transfer-distill-lightgbm | housing | catboost.LOO | lowest | 10 % | 3 | +1177.9872 | [+122.7838, +3003.8328] | 0.327 | 3/3 |
| transfer-distill-lightgbm | housing | catboost.LOO | lowest | 20 % | 3 | +1503.2175 | [+1154.9937, +2193.0266] | 0.049 | 3/3 |
| transfer-distill-lightgbm | housing | catboost.LOO | lowest | auc | 3 | +540.2544 | [+62.9314, +1479.4389] | 0.369 | 3/3 |
| transfer-distill-lightgbm | housing | catboost.LossHigh | lowest | 5 % | 3 | -159.3792 | [-435.9962, +216.8264] | 0.499 | 1/3 |
| transfer-distill-lightgbm | housing | catboost.LossHigh | lowest | 10 % | 3 | +4362.9224 | [+3525.5185, +5046.5759] | 0.010 | 3/3 |
| transfer-distill-lightgbm | housing | catboost.LossHigh | lowest | 20 % | 3 | +4723.1958 | [+2193.5505, +7124.7261] | 0.080 | 3/3 |
| transfer-distill-lightgbm | housing | catboost.LossHigh | lowest | auc | 3 | +2777.0500 | [+1805.7151, +3529.1404] | 0.032 | 3/3 |
| transfer-distill-lightgbm | housing | distill-lightgbm.Influence | lowest | 5 % | 3 | +71.0264 | [-1565.6686, +1085.5802] | 0.939 | 2/3 |
| transfer-distill-lightgbm | housing | distill-lightgbm.Influence | lowest | 10 % | 3 | +2259.5183 | [+721.2313, +3331.0200] | 0.103 | 3/3 |
| transfer-distill-lightgbm | housing | distill-lightgbm.Influence | lowest | 20 % | 3 | +2643.9877 | [+1810.4311, +3742.0053] | 0.044 | 3/3 |
| transfer-distill-lightgbm | housing | distill-lightgbm.Influence | lowest | auc | 3 | +1526.0729 | [+896.3614, +2115.4092] | 0.049 | 3/3 |
| transfer-distill-lightgbm | housing | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +58.7851 | [-194.0009, +409.4536] | 0.776 | 1/3 |
| transfer-distill-lightgbm | housing | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +4914.3750 | [+4350.7689, +5957.8855] | 0.011 | 3/3 |
| transfer-distill-lightgbm | housing | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +4176.7226 | [+1514.8539, +6190.0496] | 0.095 | 3/3 |
| transfer-distill-lightgbm | housing | distill-lightgbm.LossHigh | lowest | auc | 3 | +2901.7675 | [+1961.7516, +3542.8866] | 0.026 | 3/3 |
| transfer-distill-lightgbm | housing | lightgbm.LOO | lowest | 5 % | 3 | -1448.8976 | [-2228.6201, -177.8670] | 0.152 | 0/3 |
| transfer-distill-lightgbm | housing | lightgbm.LOO | lowest | 10 % | 3 | +809.3488 | [-872.8618, +1726.5971] | 0.438 | 2/3 |
| transfer-distill-lightgbm | housing | lightgbm.LOO | lowest | 20 % | 3 | +1392.3741 | [+1023.1999, +1784.3230] | 0.024 | 3/3 |
| transfer-distill-lightgbm | housing | lightgbm.LOO | lowest | auc | 3 | +289.3750 | [-29.3900, +551.3960] | 0.231 | 2/3 |
| transfer-distill-lightgbm | housing | lightgbm.LossHigh | lowest | 5 % | 3 | +127.5599 | [-1117.8478, +1132.8768] | 0.865 | 2/3 |
| transfer-distill-lightgbm | housing | lightgbm.LossHigh | lowest | 10 % | 3 | +4401.5079 | [+3756.8139, +4813.0669] | 0.005 | 3/3 |
| transfer-distill-lightgbm | housing | lightgbm.LossHigh | lowest | 20 % | 3 | +5130.1642 | [+2437.4112, +6502.3347] | 0.062 | 3/3 |
| transfer-distill-lightgbm | housing | lightgbm.LossHigh | lowest | auc | 3 | +2964.9965 | [+1738.6960, +3633.8970] | 0.040 | 3/3 |
| transfer-distill-lightgbm | housing | pytorch.Influence | lowest | 5 % | 3 | -487.9608 | [-1180.4588, +327.0134] | 0.382 | 1/3 |
| transfer-distill-lightgbm | housing | pytorch.Influence | lowest | 10 % | 3 | +846.1504 | [+128.1995, +1707.0086] | 0.208 | 3/3 |
| transfer-distill-lightgbm | housing | pytorch.Influence | lowest | 20 % | 3 | +1022.2915 | [-303.7831, +2381.3247] | 0.318 | 2/3 |
| transfer-distill-lightgbm | housing | pytorch.Influence | lowest | auc | 3 | +450.8891 | [+348.2913, +645.9358] | 0.044 | 3/3 |
| transfer-distill-lightgbm | housing | pytorch.LOO | lowest | 5 % | 3 | +131.7415 | [-1491.3153, +1569.8182] | 0.896 | 2/3 |
| transfer-distill-lightgbm | housing | pytorch.LOO | lowest | 10 % | 3 | +1279.9899 | [+728.0138, +2222.2007] | 0.114 | 3/3 |
| transfer-distill-lightgbm | housing | pytorch.LOO | lowest | 20 % | 3 | +1975.1466 | [+1392.8148, +2692.8467] | 0.035 | 3/3 |
| transfer-distill-lightgbm | housing | pytorch.LOO | lowest | auc | 3 | +1006.7182 | [+634.0410, +1685.7244] | 0.098 | 3/3 |
| transfer-distill-lightgbm | housing | pytorch.LissaInfluence | lowest | 5 % | 3 | -605.8980 | [-3156.3172, +1760.6695] | 0.712 | 1/3 |
| transfer-distill-lightgbm | housing | pytorch.LissaInfluence | lowest | 10 % | 3 | -883.3105 | [-2741.5788, +2815.8156] | 0.680 | 1/3 |
| transfer-distill-lightgbm | housing | pytorch.LissaInfluence | lowest | 20 % | 3 | -5749.7811 | [-11669.0330, +1712.6305] | 0.282 | 1/3 |
| transfer-distill-lightgbm | housing | pytorch.LissaInfluence | lowest | auc | 3 | -1920.1612 | [-4044.3329, +1924.2558] | 0.424 | 1/3 |
| transfer-distill-lightgbm | housing | pytorch.LossHigh | lowest | 5 % | 3 | -324.9961 | [-796.6284, +77.3522] | 0.330 | 1/3 |
| transfer-distill-lightgbm | housing | pytorch.LossHigh | lowest | 10 % | 3 | +4956.9502 | [+4073.7189, +5703.6452] | 0.009 | 3/3 |
| transfer-distill-lightgbm | housing | pytorch.LossHigh | lowest | 20 % | 3 | +3949.6507 | [+743.9550, +6388.5940] | 0.142 | 3/3 |
| transfer-distill-lightgbm | housing | pytorch.LossHigh | lowest | auc | 3 | +2765.0200 | [+1732.9714, +3308.0488] | 0.033 | 3/3 |
| transfer-distill-lightgbm | housing | random_forest.LOO | lowest | 5 % | 3 | -311.1750 | [-1818.9846, +475.1697] | 0.720 | 2/3 |
| transfer-distill-lightgbm | housing | random_forest.LOO | lowest | 10 % | 3 | +1585.3600 | [+1175.8406, +2397.7865] | 0.060 | 3/3 |
| transfer-distill-lightgbm | housing | random_forest.LOO | lowest | 20 % | 3 | +2796.8215 | [+2330.2844, +3546.0645] | 0.018 | 3/3 |
| transfer-distill-lightgbm | housing | random_forest.LOO | lowest | auc | 3 | +1215.9216 | [+875.1899, +1630.2712] | 0.031 | 3/3 |
| transfer-distill-lightgbm | housing | random_forest.LossHigh | lowest | 5 % | 3 | +413.2394 | [-569.3950, +1162.4862] | 0.505 | 2/3 |
| transfer-distill-lightgbm | housing | random_forest.LossHigh | lowest | 10 % | 3 | +4467.2436 | [+3946.8342, +4886.1929] | 0.004 | 3/3 |
| transfer-distill-lightgbm | housing | random_forest.LossHigh | lowest | 20 % | 3 | +5112.1977 | [+2162.9924, +6630.0588] | 0.074 | 3/3 |
| transfer-distill-lightgbm | housing | random_forest.LossHigh | lowest | auc | 3 | +3056.5756 | [+2182.4677, +3758.8294] | 0.022 | 3/3 |
| transfer-distill-lightgbm | housing | xgboost.LOO | lowest | 5 % | 3 | -1178.8153 | [-3124.3132, +731.7247] | 0.401 | 1/3 |
| transfer-distill-lightgbm | housing | xgboost.LOO | lowest | 10 % | 3 | +535.9571 | [-569.1349, +1732.1253] | 0.505 | 2/3 |
| transfer-distill-lightgbm | housing | xgboost.LOO | lowest | 20 % | 3 | +795.1282 | [+474.7383, +990.2942] | 0.039 | 3/3 |
| transfer-distill-lightgbm | housing | xgboost.LOO | lowest | auc | 3 | +105.0621 | [-384.1600, +1080.0517] | 0.849 | 1/3 |
| transfer-distill-lightgbm | housing | xgboost.LossHigh | lowest | 5 % | 3 | +390.7317 | [-1174.0145, +1922.8191] | 0.705 | 2/3 |
| transfer-distill-lightgbm | housing | xgboost.LossHigh | lowest | 10 % | 3 | +2089.5572 | [+1820.6211, +2402.6441] | 0.007 | 3/3 |
| transfer-distill-lightgbm | housing | xgboost.LossHigh | lowest | 20 % | 3 | +2139.7887 | [-65.8044, +5023.5972] | 0.292 | 2/3 |
| transfer-distill-lightgbm | housing | xgboost.LossHigh | lowest | auc | 3 | +1416.2141 | [+772.1294, +1863.3872] | 0.050 | 3/3 |
| transfer-distill-lightgbm | wine | any.DataOOB | lowest | 5 % | 3 | +0.0091 | [-0.0061, +0.0192] | 0.361 | 2/3 |
| transfer-distill-lightgbm | wine | any.DataOOB | lowest | 10 % | 3 | -0.0044 | [-0.0228, +0.0314] | 0.827 | 1/3 |
| transfer-distill-lightgbm | wine | any.DataOOB | lowest | 20 % | 3 | -0.0055 | [-0.0137, +0.0057] | 0.443 | 1/3 |
| transfer-distill-lightgbm | wine | any.DataOOB | lowest | auc | 3 | -0.0008 | [-0.0118, +0.0118] | 0.921 | 1/3 |
| transfer-distill-lightgbm | wine | catboost.CatBoostLFC | lowest | 5 % | 3 | +0.0093 | [+0.0075, +0.0118] | 0.020 | 3/3 |
| transfer-distill-lightgbm | wine | catboost.CatBoostLFC | lowest | 10 % | 3 | -0.0202 | [-0.0321, -0.0055] | 0.122 | 0/3 |
| transfer-distill-lightgbm | wine | catboost.CatBoostLFC | lowest | 20 % | 3 | -0.0384 | [-0.0572, -0.0268] | 0.056 | 0/3 |
| transfer-distill-lightgbm | wine | catboost.CatBoostLFC | lowest | auc | 3 | -0.0148 | [-0.0168, -0.0134] | 0.005 | 0/3 |
| transfer-distill-lightgbm | wine | catboost.LOO | lowest | 5 % | 3 | -0.0007 | [-0.0161, +0.0078] | 0.938 | 2/3 |
| transfer-distill-lightgbm | wine | catboost.LOO | lowest | 10 % | 3 | -0.0223 | [-0.0484, +0.0148] | 0.362 | 1/3 |
| transfer-distill-lightgbm | wine | catboost.LOO | lowest | 20 % | 3 | -0.0141 | [-0.0150, -0.0127] | 0.002 | 0/3 |
| transfer-distill-lightgbm | wine | catboost.LOO | lowest | auc | 3 | -0.0121 | [-0.0203, -0.0021] | 0.152 | 0/3 |
| transfer-distill-lightgbm | wine | catboost.LossHigh | lowest | 5 % | 3 | -0.0041 | [-0.0257, +0.0077] | 0.741 | 2/3 |
| transfer-distill-lightgbm | wine | catboost.LossHigh | lowest | 10 % | 3 | -0.0099 | [-0.0316, +0.0223] | 0.608 | 1/3 |
| transfer-distill-lightgbm | wine | catboost.LossHigh | lowest | 20 % | 3 | -0.0051 | [-0.0095, +0.0026] | 0.318 | 1/3 |
| transfer-distill-lightgbm | wine | catboost.LossHigh | lowest | auc | 3 | -0.0060 | [-0.0134, +0.0079] | 0.479 | 1/3 |
| transfer-distill-lightgbm | wine | distill-lightgbm.Influence | lowest | 5 % | 3 | +0.0165 | [-0.0114, +0.0450] | 0.417 | 2/3 |
| transfer-distill-lightgbm | wine | distill-lightgbm.Influence | lowest | 10 % | 3 | -0.0158 | [-0.0381, +0.0193] | 0.468 | 1/3 |
| transfer-distill-lightgbm | wine | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0014 | [-0.0197, +0.0148] | 0.905 | 2/3 |
| transfer-distill-lightgbm | wine | distill-lightgbm.Influence | lowest | auc | 3 | -0.0014 | [-0.0148, +0.0222] | 0.915 | 1/3 |
| transfer-distill-lightgbm | wine | distill-lightgbm.LossHigh | lowest | 5 % | 3 | -0.0014 | [-0.0174, +0.0095] | 0.879 | 2/3 |
| transfer-distill-lightgbm | wine | distill-lightgbm.LossHigh | lowest | 10 % | 3 | -0.0030 | [-0.0247, +0.0303] | 0.876 | 1/3 |
| transfer-distill-lightgbm | wine | distill-lightgbm.LossHigh | lowest | 20 % | 3 | -0.0096 | [-0.0220, +0.0004] | 0.282 | 1/3 |
| transfer-distill-lightgbm | wine | distill-lightgbm.LossHigh | lowest | auc | 3 | -0.0039 | [-0.0124, +0.0105] | 0.646 | 1/3 |
| transfer-distill-lightgbm | wine | lightgbm.LOO | lowest | 5 % | 3 | +0.0074 | [+0.0047, +0.0114] | 0.067 | 3/3 |
| transfer-distill-lightgbm | wine | lightgbm.LOO | lowest | 10 % | 3 | -0.0281 | [-0.0380, -0.0132] | 0.066 | 0/3 |
| transfer-distill-lightgbm | wine | lightgbm.LOO | lowest | 20 % | 3 | -0.0086 | [-0.0207, -0.0003] | 0.300 | 0/3 |
| transfer-distill-lightgbm | wine | lightgbm.LOO | lowest | auc | 3 | -0.0108 | [-0.0131, -0.0086] | 0.014 | 0/3 |
| transfer-distill-lightgbm | wine | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0218 | [+0.0066, +0.0298] | 0.104 | 3/3 |
| transfer-distill-lightgbm | wine | lightgbm.LossHigh | lowest | 10 % | 3 | -0.0004 | [-0.0163, +0.0308] | 0.982 | 1/3 |
| transfer-distill-lightgbm | wine | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0081 | [+0.0030, +0.0161] | 0.186 | 3/3 |
| transfer-distill-lightgbm | wine | lightgbm.LossHigh | lowest | auc | 3 | +0.0073 | [-0.0035, +0.0228] | 0.455 | 2/3 |
| transfer-distill-lightgbm | wine | pytorch.Influence | lowest | 5 % | 3 | +0.0046 | [-0.0024, +0.0104] | 0.339 | 2/3 |
| transfer-distill-lightgbm | wine | pytorch.Influence | lowest | 10 % | 3 | -0.0199 | [-0.0258, -0.0148] | 0.025 | 0/3 |
| transfer-distill-lightgbm | wine | pytorch.Influence | lowest | 20 % | 3 | -0.0090 | [-0.0437, +0.0136] | 0.660 | 2/3 |
| transfer-distill-lightgbm | wine | pytorch.Influence | lowest | auc | 3 | -0.0086 | [-0.0171, -0.0012] | 0.204 | 0/3 |
| transfer-distill-lightgbm | wine | pytorch.LOO | lowest | 5 % | 3 | +0.0178 | [+0.0091, +0.0232] | 0.056 | 3/3 |
| transfer-distill-lightgbm | wine | pytorch.LOO | lowest | 10 % | 3 | -0.0038 | [-0.0285, +0.0255] | 0.833 | 1/3 |
| transfer-distill-lightgbm | wine | pytorch.LOO | lowest | 20 % | 3 | +0.0025 | [-0.0161, +0.0231] | 0.847 | 2/3 |
| transfer-distill-lightgbm | wine | pytorch.LOO | lowest | auc | 3 | +0.0036 | [-0.0048, +0.0108] | 0.506 | 2/3 |
| transfer-distill-lightgbm | wine | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0279 | [+0.0229, +0.0363] | 0.022 | 3/3 |
| transfer-distill-lightgbm | wine | pytorch.LissaInfluence | lowest | 10 % | 3 | -0.0069 | [-0.0207, +0.0095] | 0.517 | 1/3 |
| transfer-distill-lightgbm | wine | pytorch.LissaInfluence | lowest | 20 % | 3 | -0.0040 | [-0.0232, +0.0276] | 0.824 | 1/3 |
| transfer-distill-lightgbm | wine | pytorch.LissaInfluence | lowest | auc | 3 | +0.0034 | [-0.0028, +0.0095] | 0.440 | 2/3 |
| transfer-distill-lightgbm | wine | pytorch.LossHigh | lowest | 5 % | 3 | -0.0007 | [-0.0121, +0.0093] | 0.916 | 2/3 |
| transfer-distill-lightgbm | wine | pytorch.LossHigh | lowest | 10 % | 3 | +0.0040 | [-0.0250, +0.0469] | 0.871 | 1/3 |
| transfer-distill-lightgbm | wine | pytorch.LossHigh | lowest | 20 % | 3 | -0.0060 | [-0.0125, +0.0033] | 0.335 | 1/3 |
| transfer-distill-lightgbm | wine | pytorch.LossHigh | lowest | auc | 3 | -0.0002 | [-0.0102, +0.0186] | 0.987 | 1/3 |
| transfer-distill-lightgbm | wine | random_forest.LOO | lowest | 5 % | 3 | +0.0141 | [+0.0069, +0.0191] | 0.062 | 3/3 |
| transfer-distill-lightgbm | wine | random_forest.LOO | lowest | 10 % | 3 | -0.0099 | [-0.0207, +0.0081] | 0.389 | 1/3 |
| transfer-distill-lightgbm | wine | random_forest.LOO | lowest | 20 % | 3 | +0.0030 | [-0.0092, +0.0176] | 0.741 | 2/3 |
| transfer-distill-lightgbm | wine | random_forest.LOO | lowest | auc | 3 | +0.0005 | [-0.0016, +0.0048] | 0.821 | 1/3 |
| transfer-distill-lightgbm | wine | random_forest.LossHigh | lowest | 5 % | 3 | +0.0081 | [-0.0022, +0.0137] | 0.256 | 2/3 |
| transfer-distill-lightgbm | wine | random_forest.LossHigh | lowest | 10 % | 3 | -0.0062 | [-0.0264, +0.0200] | 0.694 | 1/3 |
| transfer-distill-lightgbm | wine | random_forest.LossHigh | lowest | 20 % | 3 | +0.0084 | [-0.0053, +0.0191] | 0.362 | 2/3 |
| transfer-distill-lightgbm | wine | random_forest.LossHigh | lowest | auc | 3 | +0.0018 | [-0.0118, +0.0155] | 0.841 | 2/3 |
| transfer-distill-lightgbm | wine | xgboost.LOO | lowest | 5 % | 3 | +0.0097 | [-0.0039, +0.0168] | 0.292 | 2/3 |
| transfer-distill-lightgbm | wine | xgboost.LOO | lowest | 10 % | 3 | -0.0183 | [-0.0541, +0.0193] | 0.478 | 1/3 |
| transfer-distill-lightgbm | wine | xgboost.LOO | lowest | 20 % | 3 | -0.0173 | [-0.0405, +0.0066] | 0.331 | 1/3 |
| transfer-distill-lightgbm | wine | xgboost.LOO | lowest | auc | 3 | -0.0088 | [-0.0207, +0.0013] | 0.305 | 1/3 |
| transfer-distill-lightgbm | wine | xgboost.LossHigh | lowest | 5 % | 3 | +0.0206 | [+0.0048, +0.0422] | 0.206 | 3/3 |
| transfer-distill-lightgbm | wine | xgboost.LossHigh | lowest | 10 % | 3 | -0.0028 | [-0.0156, +0.0075] | 0.717 | 1/3 |
| transfer-distill-lightgbm | wine | xgboost.LossHigh | lowest | 20 % | 3 | -0.0146 | [-0.0208, -0.0111] | 0.042 | 0/3 |
| transfer-distill-lightgbm | wine | xgboost.LossHigh | lowest | auc | 3 | +0.0004 | [-0.0099, +0.0106] | 0.948 | 2/3 |
| transfer-lightgbm | adult | any.DataOOB | lowest | 5 % | 3 | +0.0212 | [+0.0092, +0.0390] | 0.144 | 3/3 |
| transfer-lightgbm | adult | any.DataOOB | lowest | 10 % | 3 | +0.0105 | [+0.0072, +0.0124] | 0.023 | 3/3 |
| transfer-lightgbm | adult | any.DataOOB | lowest | 20 % | 3 | +0.0040 | [-0.0057, +0.0164] | 0.602 | 2/3 |
| transfer-lightgbm | adult | any.DataOOB | lowest | auc | 3 | +0.0102 | [+0.0053, +0.0129] | 0.053 | 3/3 |
| transfer-lightgbm | adult | any.KNNShapley | lowest | 5 % | 3 | +0.0209 | [+0.0096, +0.0391] | 0.151 | 3/3 |
| transfer-lightgbm | adult | any.KNNShapley | lowest | 10 % | 3 | +0.0190 | [+0.0172, +0.0213] | 0.004 | 3/3 |
| transfer-lightgbm | adult | any.KNNShapley | lowest | 20 % | 3 | +0.0067 | [-0.0028, +0.0222] | 0.482 | 2/3 |
| transfer-lightgbm | adult | any.KNNShapley | lowest | auc | 3 | +0.0140 | [+0.0108, +0.0168] | 0.015 | 3/3 |
| transfer-lightgbm | adult | catboost.CatBoostLFC | lowest | 5 % | 3 | +0.0118 | [+0.0028, +0.0219] | 0.166 | 3/3 |
| transfer-lightgbm | adult | catboost.CatBoostLFC | lowest | 10 % | 3 | -0.0045 | [-0.0140, +0.0065] | 0.527 | 1/3 |
| transfer-lightgbm | adult | catboost.CatBoostLFC | lowest | 20 % | 3 | -0.0073 | [-0.0169, -0.0002] | 0.280 | 0/3 |
| transfer-lightgbm | adult | catboost.CatBoostLFC | lowest | auc | 3 | -0.0006 | [-0.0040, +0.0051] | 0.858 | 1/3 |
| transfer-lightgbm | adult | catboost.LOO | lowest | 5 % | 3 | +0.0087 | [-0.0003, +0.0163] | 0.214 | 2/3 |
| transfer-lightgbm | adult | catboost.LOO | lowest | 10 % | 3 | +0.0091 | [+0.0087, +0.0093] | 0.000 | 3/3 |
| transfer-lightgbm | adult | catboost.LOO | lowest | 20 % | 3 | +0.0024 | [-0.0109, +0.0131] | 0.766 | 2/3 |
| transfer-lightgbm | adult | catboost.LOO | lowest | auc | 3 | +0.0062 | [+0.0033, +0.0088] | 0.060 | 3/3 |
| transfer-lightgbm | adult | catboost.LossHigh | lowest | 5 % | 3 | +0.0273 | [+0.0065, +0.0536] | 0.189 | 3/3 |
| transfer-lightgbm | adult | catboost.LossHigh | lowest | 10 % | 3 | +0.0173 | [+0.0058, +0.0289] | 0.122 | 3/3 |
| transfer-lightgbm | adult | catboost.LossHigh | lowest | 20 % | 3 | +0.0015 | [-0.0057, +0.0084] | 0.744 | 2/3 |
| transfer-lightgbm | adult | catboost.LossHigh | lowest | auc | 3 | +0.0137 | [+0.0024, +0.0247] | 0.168 | 3/3 |
| transfer-lightgbm | adult | distill-lightgbm.Influence | lowest | 5 % | 3 | +0.0060 | [-0.0128, +0.0213] | 0.610 | 2/3 |
| transfer-lightgbm | adult | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0120 | [+0.0068, +0.0208] | 0.114 | 3/3 |
| transfer-lightgbm | adult | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0022 | [-0.0022, +0.0081] | 0.546 | 2/3 |
| transfer-lightgbm | adult | distill-lightgbm.Influence | lowest | auc | 3 | +0.0065 | [-0.0005, +0.0126] | 0.227 | 2/3 |
| transfer-lightgbm | adult | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0266 | [+0.0102, +0.0504] | 0.161 | 3/3 |
| transfer-lightgbm | adult | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0151 | [-0.0048, +0.0260] | 0.269 | 2/3 |
| transfer-lightgbm | adult | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0010 | [-0.0042, +0.0043] | 0.740 | 2/3 |
| transfer-lightgbm | adult | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0126 | [-0.0003, +0.0224] | 0.203 | 2/3 |
| transfer-lightgbm | adult | lightgbm.LOO | lowest | 5 % | 3 | +0.0019 | [-0.0020, +0.0041] | 0.427 | 2/3 |
| transfer-lightgbm | adult | lightgbm.LOO | lowest | 10 % | 3 | +0.0011 | [-0.0127, +0.0166] | 0.909 | 1/3 |
| transfer-lightgbm | adult | lightgbm.LOO | lowest | 20 % | 3 | -0.0129 | [-0.0472, +0.0093] | 0.537 | 1/3 |
| transfer-lightgbm | adult | lightgbm.LOO | lowest | auc | 3 | -0.0023 | [-0.0110, +0.0081] | 0.717 | 1/3 |
| transfer-lightgbm | adult | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0205 | [+0.0074, +0.0428] | 0.209 | 3/3 |
| transfer-lightgbm | adult | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0202 | [+0.0123, +0.0246] | 0.037 | 3/3 |
| transfer-lightgbm | adult | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0042 | [-0.0197, +0.0169] | 0.758 | 2/3 |
| transfer-lightgbm | adult | lightgbm.LossHigh | lowest | auc | 3 | +0.0138 | [+0.0015, +0.0242] | 0.172 | 3/3 |
| transfer-lightgbm | adult | pytorch.Influence | lowest | 5 % | 3 | +0.0219 | [-0.0073, +0.0486] | 0.309 | 2/3 |
| transfer-lightgbm | adult | pytorch.Influence | lowest | 10 % | 3 | +0.0168 | [+0.0141, +0.0221] | 0.025 | 3/3 |
| transfer-lightgbm | adult | pytorch.Influence | lowest | 20 % | 3 | +0.0174 | [-0.0020, +0.0325] | 0.231 | 2/3 |
| transfer-lightgbm | adult | pytorch.Influence | lowest | auc | 3 | +0.0161 | [+0.0116, +0.0198] | 0.022 | 3/3 |
| transfer-lightgbm | adult | pytorch.LOO | lowest | 5 % | 3 | +0.0066 | [-0.0055, +0.0145] | 0.396 | 2/3 |
| transfer-lightgbm | adult | pytorch.LOO | lowest | 10 % | 3 | -0.0093 | [-0.0263, +0.0081] | 0.449 | 1/3 |
| transfer-lightgbm | adult | pytorch.LOO | lowest | 20 % | 3 | -0.0043 | [-0.0139, +0.0050] | 0.518 | 1/3 |
| transfer-lightgbm | adult | pytorch.LOO | lowest | auc | 3 | -0.0029 | [-0.0122, +0.0070] | 0.655 | 1/3 |
| transfer-lightgbm | adult | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0118 | [-0.0108, +0.0469] | 0.576 | 1/3 |
| transfer-lightgbm | adult | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0153 | [+0.0039, +0.0335] | 0.238 | 3/3 |
| transfer-lightgbm | adult | pytorch.LissaInfluence | lowest | 20 % | 3 | +0.0100 | [-0.0046, +0.0269] | 0.388 | 2/3 |
| transfer-lightgbm | adult | pytorch.LissaInfluence | lowest | auc | 3 | +0.0112 | [+0.0032, +0.0231] | 0.207 | 3/3 |
| transfer-lightgbm | adult | pytorch.LossHigh | lowest | 5 % | 3 | +0.0255 | [+0.0049, +0.0568] | 0.251 | 3/3 |
| transfer-lightgbm | adult | pytorch.LossHigh | lowest | 10 % | 3 | +0.0160 | [-0.0025, +0.0350] | 0.278 | 2/3 |
| transfer-lightgbm | adult | pytorch.LossHigh | lowest | 20 % | 3 | +0.0053 | [-0.0036, +0.0126] | 0.377 | 2/3 |
| transfer-lightgbm | adult | pytorch.LossHigh | lowest | auc | 3 | +0.0137 | [-0.0006, +0.0291] | 0.252 | 2/3 |
| transfer-lightgbm | adult | random_forest.LOO | lowest | 5 % | 3 | -0.0028 | [-0.0156, +0.0057] | 0.713 | 2/3 |
| transfer-lightgbm | adult | random_forest.LOO | lowest | 10 % | 3 | -0.0004 | [-0.0112, +0.0089] | 0.952 | 2/3 |
| transfer-lightgbm | adult | random_forest.LOO | lowest | 20 % | 3 | -0.0111 | [-0.0227, +0.0044] | 0.302 | 1/3 |
| transfer-lightgbm | adult | random_forest.LOO | lowest | auc | 3 | -0.0036 | [-0.0084, +0.0019] | 0.351 | 1/3 |
| transfer-lightgbm | adult | random_forest.LossHigh | lowest | 5 % | 3 | +0.0247 | [+0.0092, +0.0533] | 0.227 | 3/3 |
| transfer-lightgbm | adult | random_forest.LossHigh | lowest | 10 % | 3 | +0.0169 | [+0.0078, +0.0295] | 0.122 | 3/3 |
| transfer-lightgbm | adult | random_forest.LossHigh | lowest | 20 % | 3 | +0.0043 | [-0.0079, +0.0123] | 0.560 | 2/3 |
| transfer-lightgbm | adult | random_forest.LossHigh | lowest | auc | 3 | +0.0136 | [+0.0033, +0.0265] | 0.185 | 3/3 |
| transfer-lightgbm | adult | xgboost.LOO | lowest | 5 % | 3 | +0.0063 | [-0.0034, +0.0191] | 0.443 | 2/3 |
| transfer-lightgbm | adult | xgboost.LOO | lowest | 10 % | 3 | -0.0080 | [-0.0150, -0.0003] | 0.201 | 0/3 |
| transfer-lightgbm | adult | xgboost.LOO | lowest | 20 % | 3 | -0.0209 | [-0.0375, -0.0066] | 0.145 | 0/3 |
| transfer-lightgbm | adult | xgboost.LOO | lowest | auc | 3 | -0.0067 | [-0.0081, -0.0047] | 0.023 | 0/3 |
| transfer-lightgbm | adult | xgboost.LossHigh | lowest | 5 % | 3 | +0.0131 | [-0.0011, +0.0320] | 0.315 | 2/3 |
| transfer-lightgbm | adult | xgboost.LossHigh | lowest | 10 % | 3 | +0.0101 | [+0.0033, +0.0187] | 0.155 | 3/3 |
| transfer-lightgbm | adult | xgboost.LossHigh | lowest | 20 % | 3 | +0.0023 | [-0.0041, +0.0121] | 0.690 | 1/3 |
| transfer-lightgbm | adult | xgboost.LossHigh | lowest | auc | 3 | +0.0076 | [-0.0001, +0.0147] | 0.216 | 2/3 |
| transfer-lightgbm | covertype | any.DataOOB | lowest | 5 % | 3 | +0.0089 | [+0.0004, +0.0160] | 0.189 | 3/3 |
| transfer-lightgbm | covertype | any.DataOOB | lowest | 10 % | 3 | +0.0088 | [+0.0006, +0.0134] | 0.166 | 3/3 |
| transfer-lightgbm | covertype | any.DataOOB | lowest | 20 % | 3 | +0.0026 | [-0.0076, +0.0086] | 0.662 | 2/3 |
| transfer-lightgbm | covertype | any.DataOOB | lowest | auc | 3 | +0.0062 | [+0.0057, +0.0069] | 0.003 | 3/3 |
| transfer-lightgbm | covertype | any.KNNShapley | lowest | 5 % | 3 | +0.0073 | [-0.0008, +0.0162] | 0.278 | 2/3 |
| transfer-lightgbm | covertype | any.KNNShapley | lowest | 10 % | 3 | +0.0071 | [+0.0036, +0.0104] | 0.069 | 3/3 |
| transfer-lightgbm | covertype | any.KNNShapley | lowest | 20 % | 3 | +0.0143 | [+0.0080, +0.0174] | 0.045 | 3/3 |
| transfer-lightgbm | covertype | any.KNNShapley | lowest | auc | 3 | +0.0080 | [+0.0063, +0.0097] | 0.015 | 3/3 |
| transfer-lightgbm | covertype | catboost.LOO | lowest | 5 % | 3 | +0.0040 | [-0.0044, +0.0112] | 0.471 | 2/3 |
| transfer-lightgbm | covertype | catboost.LOO | lowest | 10 % | 3 | -0.0018 | [-0.0076, +0.0074] | 0.736 | 1/3 |
| transfer-lightgbm | covertype | catboost.LOO | lowest | 20 % | 3 | +0.0074 | [+0.0050, +0.0104] | 0.043 | 3/3 |
| transfer-lightgbm | covertype | catboost.LOO | lowest | auc | 3 | +0.0022 | [-0.0004, +0.0068] | 0.449 | 2/3 |
| transfer-lightgbm | covertype | catboost.LossHigh | lowest | 5 % | 3 | +0.0062 | [-0.0042, +0.0114] | 0.355 | 2/3 |
| transfer-lightgbm | covertype | catboost.LossHigh | lowest | 10 % | 3 | +0.0032 | [+0.0014, +0.0060] | 0.153 | 3/3 |
| transfer-lightgbm | covertype | catboost.LossHigh | lowest | 20 % | 3 | +0.0065 | [-0.0054, +0.0226] | 0.516 | 2/3 |
| transfer-lightgbm | covertype | catboost.LossHigh | lowest | auc | 3 | +0.0044 | [+0.0020, +0.0068] | 0.088 | 3/3 |
| transfer-lightgbm | covertype | distill-lightgbm.Influence | lowest | 5 % | 3 | -0.0007 | [-0.0034, +0.0044] | 0.817 | 1/3 |
| transfer-lightgbm | covertype | distill-lightgbm.Influence | lowest | 10 % | 3 | -0.0013 | [-0.0034, +0.0012] | 0.444 | 1/3 |
| transfer-lightgbm | covertype | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0097 | [+0.0056, +0.0128] | 0.045 | 3/3 |
| transfer-lightgbm | covertype | distill-lightgbm.Influence | lowest | auc | 3 | +0.0018 | [+0.0010, +0.0025] | 0.053 | 3/3 |
| transfer-lightgbm | covertype | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0042 | [-0.0044, +0.0102] | 0.441 | 2/3 |
| transfer-lightgbm | covertype | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0095 | [+0.0040, +0.0178] | 0.155 | 3/3 |
| transfer-lightgbm | covertype | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0105 | [+0.0036, +0.0216] | 0.200 | 3/3 |
| transfer-lightgbm | covertype | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0072 | [+0.0058, +0.0100] | 0.034 | 3/3 |
| transfer-lightgbm | covertype | lightgbm.LOO | lowest | 5 % | 3 | +0.0041 | [+0.0006, +0.0084] | 0.218 | 3/3 |
| transfer-lightgbm | covertype | lightgbm.LOO | lowest | 10 % | 3 | -0.0001 | [-0.0076, +0.0062] | 0.977 | 2/3 |
| transfer-lightgbm | covertype | lightgbm.LOO | lowest | 20 % | 3 | +0.0033 | [-0.0024, +0.0112] | 0.508 | 2/3 |
| transfer-lightgbm | covertype | lightgbm.LOO | lowest | auc | 3 | +0.0018 | [-0.0026, +0.0053] | 0.525 | 2/3 |
| transfer-lightgbm | covertype | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0076 | [+0.0056, +0.0100] | 0.027 | 3/3 |
| transfer-lightgbm | covertype | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0039 | [+0.0032, +0.0044] | 0.009 | 3/3 |
| transfer-lightgbm | covertype | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0061 | [-0.0018, +0.0220] | 0.520 | 1/3 |
| transfer-lightgbm | covertype | lightgbm.LossHigh | lowest | auc | 3 | +0.0049 | [+0.0026, +0.0085] | 0.117 | 3/3 |
| transfer-lightgbm | covertype | pytorch.Influence | lowest | 5 % | 3 | +0.0055 | [-0.0036, +0.0198] | 0.524 | 2/3 |
| transfer-lightgbm | covertype | pytorch.Influence | lowest | 10 % | 3 | +0.0069 | [+0.0020, +0.0098] | 0.107 | 3/3 |
| transfer-lightgbm | covertype | pytorch.Influence | lowest | 20 % | 3 | +0.0099 | [-0.0022, +0.0190] | 0.257 | 2/3 |
| transfer-lightgbm | covertype | pytorch.Influence | lowest | auc | 3 | +0.0064 | [+0.0003, +0.0115] | 0.189 | 3/3 |
| transfer-lightgbm | covertype | pytorch.LOO | lowest | 5 % | 3 | -0.0002 | [-0.0080, +0.0094] | 0.972 | 1/3 |
| transfer-lightgbm | covertype | pytorch.LOO | lowest | 10 % | 3 | -0.0047 | [-0.0124, +0.0004] | 0.357 | 1/3 |
| transfer-lightgbm | covertype | pytorch.LOO | lowest | 20 % | 3 | +0.0047 | [-0.0020, +0.0092] | 0.304 | 2/3 |
| transfer-lightgbm | covertype | pytorch.LOO | lowest | auc | 3 | -0.0006 | [-0.0057, +0.0039] | 0.840 | 1/3 |
| transfer-lightgbm | covertype | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0006 | [-0.0024, +0.0056] | 0.834 | 1/3 |
| transfer-lightgbm | covertype | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0038 | [-0.0002, +0.0080] | 0.250 | 2/3 |
| transfer-lightgbm | covertype | pytorch.LissaInfluence | lowest | 20 % | 3 | +0.0073 | [-0.0024, +0.0158] | 0.303 | 2/3 |
| transfer-lightgbm | covertype | pytorch.LissaInfluence | lowest | auc | 3 | +0.0034 | [-0.0010, +0.0084] | 0.339 | 2/3 |
| transfer-lightgbm | covertype | pytorch.LossHigh | lowest | 5 % | 3 | +0.0119 | [+0.0026, +0.0198] | 0.141 | 3/3 |
| transfer-lightgbm | covertype | pytorch.LossHigh | lowest | 10 % | 3 | +0.0157 | [+0.0058, +0.0298] | 0.162 | 3/3 |
| transfer-lightgbm | covertype | pytorch.LossHigh | lowest | 20 % | 3 | +0.0069 | [-0.0028, +0.0186] | 0.387 | 2/3 |
| transfer-lightgbm | covertype | pytorch.LossHigh | lowest | auc | 3 | +0.0106 | [+0.0064, +0.0165] | 0.073 | 3/3 |
| transfer-lightgbm | covertype | random_forest.LOO | lowest | 5 % | 3 | +0.0040 | [-0.0088, +0.0198] | 0.681 | 2/3 |
| transfer-lightgbm | covertype | random_forest.LOO | lowest | 10 % | 3 | -0.0035 | [-0.0070, +0.0010] | 0.279 | 1/3 |
| transfer-lightgbm | covertype | random_forest.LOO | lowest | 20 % | 3 | +0.0051 | [+0.0006, +0.0122] | 0.288 | 3/3 |
| transfer-lightgbm | covertype | random_forest.LOO | lowest | auc | 3 | +0.0010 | [-0.0022, +0.0039] | 0.637 | 2/3 |
| transfer-lightgbm | covertype | random_forest.LossHigh | lowest | 5 % | 3 | +0.0053 | [-0.0046, +0.0118] | 0.404 | 2/3 |
| transfer-lightgbm | covertype | random_forest.LossHigh | lowest | 10 % | 3 | +0.0020 | [-0.0068, +0.0064] | 0.694 | 2/3 |
| transfer-lightgbm | covertype | random_forest.LossHigh | lowest | 20 % | 3 | -0.0000 | [-0.0072, +0.0110] | 1.000 | 1/3 |
| transfer-lightgbm | covertype | random_forest.LossHigh | lowest | auc | 3 | +0.0021 | [-0.0014, +0.0040] | 0.356 | 2/3 |
| transfer-lightgbm | covertype | xgboost.LOO | lowest | 5 % | 3 | -0.0016 | [-0.0038, -0.0002] | 0.287 | 0/3 |
| transfer-lightgbm | covertype | xgboost.LOO | lowest | 10 % | 3 | +0.0003 | [-0.0096, +0.0058] | 0.953 | 2/3 |
| transfer-lightgbm | covertype | xgboost.LOO | lowest | 20 % | 3 | +0.0078 | [+0.0046, +0.0122] | 0.076 | 3/3 |
| transfer-lightgbm | covertype | xgboost.LOO | lowest | auc | 3 | +0.0017 | [-0.0025, +0.0043] | 0.510 | 2/3 |
| transfer-lightgbm | covertype | xgboost.LossHigh | lowest | 5 % | 3 | +0.0091 | [+0.0046, +0.0164] | 0.134 | 3/3 |
| transfer-lightgbm | covertype | xgboost.LossHigh | lowest | 10 % | 3 | +0.0069 | [+0.0000, +0.0114] | 0.188 | 2/3 |
| transfer-lightgbm | covertype | xgboost.LossHigh | lowest | 20 % | 3 | +0.0049 | [-0.0012, +0.0146] | 0.419 | 2/3 |
| transfer-lightgbm | covertype | xgboost.LossHigh | lowest | auc | 3 | +0.0061 | [+0.0038, +0.0095] | 0.073 | 3/3 |
| transfer-lightgbm | housing | any.DataOOB | lowest | 5 % | 3 | +2662.3371 | [+1587.5531, +3724.8145] | 0.050 | 3/3 |
| transfer-lightgbm | housing | any.DataOOB | lowest | 10 % | 3 | +11158.0396 | [+10639.5999, +11599.8227] | 0.001 | 3/3 |
| transfer-lightgbm | housing | any.DataOOB | lowest | 20 % | 3 | +11713.3481 | [+11295.5522, +12192.2703] | 0.000 | 3/3 |
| transfer-lightgbm | housing | any.DataOOB | lowest | auc | 3 | +7778.1861 | [+7482.3989, +8194.1926] | 0.001 | 3/3 |
| transfer-lightgbm | housing | catboost.CatBoostLFC | lowest | 5 % | 3 | -56.6313 | [-877.2492, +1547.0940] | 0.950 | 1/3 |
| transfer-lightgbm | housing | catboost.CatBoostLFC | lowest | 10 % | 3 | -2112.4125 | [-2637.0913, -1331.8949] | 0.034 | 0/3 |
| transfer-lightgbm | housing | catboost.CatBoostLFC | lowest | 20 % | 3 | -5340.6895 | [-7843.9707, -3659.1474] | 0.053 | 0/3 |
| transfer-lightgbm | housing | catboost.CatBoostLFC | lowest | auc | 3 | -2141.4849 | [-2563.1284, -1633.5598] | 0.016 | 0/3 |
| transfer-lightgbm | housing | catboost.LOO | lowest | 5 % | 3 | +420.2495 | [-1121.0962, +2606.0466] | 0.744 | 1/3 |
| transfer-lightgbm | housing | catboost.LOO | lowest | 10 % | 3 | +270.0835 | [-2380.5906, +2072.6526] | 0.860 | 2/3 |
| transfer-lightgbm | housing | catboost.LOO | lowest | 20 % | 3 | +698.9559 | [-1252.8702, +1839.1829] | 0.550 | 2/3 |
| transfer-lightgbm | housing | catboost.LOO | lowest | auc | 3 | +381.0827 | [-488.9762, +874.6094] | 0.475 | 2/3 |
| transfer-lightgbm | housing | catboost.LossHigh | lowest | 5 % | 3 | +3055.0569 | [+1503.2368, +5134.1569] | 0.106 | 3/3 |
| transfer-lightgbm | housing | catboost.LossHigh | lowest | 10 % | 3 | +9808.8397 | [+8638.4754, +11135.5124] | 0.005 | 3/3 |
| transfer-lightgbm | housing | catboost.LossHigh | lowest | 20 % | 3 | +10627.9648 | [+10530.8659, +10747.9252] | 0.000 | 3/3 |
| transfer-lightgbm | housing | catboost.LossHigh | lowest | auc | 3 | +7099.0703 | [+6522.6484, +8092.0728] | 0.005 | 3/3 |
| transfer-lightgbm | housing | distill-lightgbm.Influence | lowest | 5 % | 3 | +2113.8369 | [+801.0861, +4309.2808] | 0.196 | 3/3 |
| transfer-lightgbm | housing | distill-lightgbm.Influence | lowest | 10 % | 3 | +1702.8132 | [+1219.0739, +2258.3146] | 0.030 | 3/3 |
| transfer-lightgbm | housing | distill-lightgbm.Influence | lowest | 20 % | 3 | +619.5081 | [-870.5559, +1830.7573] | 0.516 | 2/3 |
| transfer-lightgbm | housing | distill-lightgbm.Influence | lowest | auc | 3 | +1321.8912 | [+1144.0108, +1504.8288] | 0.006 | 3/3 |
| transfer-lightgbm | housing | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +1521.0484 | [-356.2235, +2851.2225] | 0.256 | 2/3 |
| transfer-lightgbm | housing | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +10515.8005 | [+10300.3001, +10780.0675] | 0.000 | 3/3 |
| transfer-lightgbm | housing | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +11430.2224 | [+10886.0832, +11995.3791] | 0.001 | 3/3 |
| transfer-lightgbm | housing | distill-lightgbm.LossHigh | lowest | auc | 3 | +7181.2429 | [+6952.3142, +7490.2446] | 0.000 | 3/3 |
| transfer-lightgbm | housing | lightgbm.LOO | lowest | 5 % | 3 | +1556.7066 | [-247.5015, +4317.3807] | 0.382 | 2/3 |
| transfer-lightgbm | housing | lightgbm.LOO | lowest | 10 % | 3 | +425.2823 | [+99.4542, +830.6197] | 0.186 | 3/3 |
| transfer-lightgbm | housing | lightgbm.LOO | lowest | 20 % | 3 | +1451.1297 | [+1254.9393, +1686.4560] | 0.007 | 3/3 |
| transfer-lightgbm | housing | lightgbm.LOO | lowest | auc | 3 | +911.4399 | [+289.1548, +1630.6241] | 0.145 | 3/3 |
| transfer-lightgbm | housing | lightgbm.LossHigh | lowest | 5 % | 3 | +2384.8541 | [+684.1655, +3942.2598] | 0.127 | 3/3 |
| transfer-lightgbm | housing | lightgbm.LossHigh | lowest | 10 % | 3 | +9760.2142 | [+9435.0396, +9946.1439] | 0.000 | 3/3 |
| transfer-lightgbm | housing | lightgbm.LossHigh | lowest | 20 % | 3 | +12096.3694 | [+11199.4716, +13299.0693] | 0.003 | 3/3 |
| transfer-lightgbm | housing | lightgbm.LossHigh | lowest | auc | 3 | +7280.3862 | [+7225.6127, +7323.5727] | 0.000 | 3/3 |
| transfer-lightgbm | housing | pytorch.Influence | lowest | 5 % | 3 | +2506.4222 | [+1145.0747, +4818.1804] | 0.164 | 3/3 |
| transfer-lightgbm | housing | pytorch.Influence | lowest | 10 % | 3 | +2438.5099 | [+1075.3577, +3568.0220] | 0.079 | 3/3 |
| transfer-lightgbm | housing | pytorch.Influence | lowest | 20 % | 3 | +2459.9087 | [+1967.0776, +2822.8531] | 0.011 | 3/3 |
| transfer-lightgbm | housing | pytorch.Influence | lowest | auc | 3 | +2156.0239 | [+1780.0944, +2432.7244] | 0.008 | 3/3 |
| transfer-lightgbm | housing | pytorch.LOO | lowest | 5 % | 3 | +1127.8161 | [+256.4949, +2659.1710] | 0.280 | 3/3 |
| transfer-lightgbm | housing | pytorch.LOO | lowest | 10 % | 3 | +425.0330 | [+150.0660, +691.5958] | 0.113 | 3/3 |
| transfer-lightgbm | housing | pytorch.LOO | lowest | 20 % | 3 | +1775.9413 | [+791.9535, +2329.2477] | 0.069 | 3/3 |
| transfer-lightgbm | housing | pytorch.LOO | lowest | auc | 3 | +885.3267 | [+808.9746, +927.9497] | 0.002 | 3/3 |
| transfer-lightgbm | housing | pytorch.LissaInfluence | lowest | 5 % | 3 | +2038.5987 | [-756.6266, +7038.0668] | 0.501 | 1/3 |
| transfer-lightgbm | housing | pytorch.LissaInfluence | lowest | 10 % | 3 | -183.2791 | [-2437.4614, +4121.6353] | 0.940 | 1/3 |
| transfer-lightgbm | housing | pytorch.LissaInfluence | lowest | 20 % | 3 | -3883.9208 | [-7074.0229, +1250.0720] | 0.273 | 1/3 |
| transfer-lightgbm | housing | pytorch.LissaInfluence | lowest | auc | 3 | -530.0602 | [-2647.6710, +3617.6479] | 0.822 | 1/3 |
| transfer-lightgbm | housing | pytorch.LossHigh | lowest | 5 % | 3 | +2534.2880 | [+783.8605, +3849.2702] | 0.109 | 3/3 |
| transfer-lightgbm | housing | pytorch.LossHigh | lowest | 10 % | 3 | +10433.7511 | [+10134.3889, +11008.2759] | 0.001 | 3/3 |
| transfer-lightgbm | housing | pytorch.LossHigh | lowest | 20 % | 3 | +11318.5166 | [+10297.7825, +12155.6663] | 0.002 | 3/3 |
| transfer-lightgbm | housing | pytorch.LossHigh | lowest | auc | 3 | +7375.8578 | [+7117.2748, +7647.3135] | 0.000 | 3/3 |
| transfer-lightgbm | housing | random_forest.LOO | lowest | 5 % | 3 | +742.5427 | [-825.1217, +2462.2870] | 0.517 | 2/3 |
| transfer-lightgbm | housing | random_forest.LOO | lowest | 10 % | 3 | +182.4413 | [-189.6691, +741.0899] | 0.587 | 1/3 |
| transfer-lightgbm | housing | random_forest.LOO | lowest | 20 % | 3 | +1153.4582 | [-729.0525, +2103.3839] | 0.345 | 2/3 |
| transfer-lightgbm | housing | random_forest.LOO | lowest | auc | 3 | +542.4157 | [+362.1827, +667.5903] | 0.028 | 3/3 |
| transfer-lightgbm | housing | random_forest.LossHigh | lowest | 5 % | 3 | +2643.3169 | [+1335.4545, +3513.9868] | 0.058 | 3/3 |
| transfer-lightgbm | housing | random_forest.LossHigh | lowest | 10 % | 3 | +10039.8640 | [+9092.9073, +10733.7378] | 0.002 | 3/3 |
| transfer-lightgbm | housing | random_forest.LossHigh | lowest | 20 % | 3 | +11418.9302 | [+10986.3685, +12056.9050] | 0.001 | 3/3 |
| transfer-lightgbm | housing | random_forest.LossHigh | lowest | auc | 3 | +7280.5108 | [+6983.3468, +7650.2405] | 0.001 | 3/3 |
| transfer-lightgbm | housing | xgboost.LOO | lowest | 5 % | 3 | +1199.9276 | [-513.1841, +4236.5123] | 0.513 | 1/3 |
| transfer-lightgbm | housing | xgboost.LOO | lowest | 10 % | 3 | +87.7592 | [-875.3341, +919.5577] | 0.882 | 2/3 |
| transfer-lightgbm | housing | xgboost.LOO | lowest | 20 % | 3 | +246.4064 | [-1849.9867, +1577.3413] | 0.838 | 2/3 |
| transfer-lightgbm | housing | xgboost.LOO | lowest | auc | 3 | +394.4932 | [+268.3811, +566.9139] | 0.048 | 3/3 |
| transfer-lightgbm | housing | xgboost.LossHigh | lowest | 5 % | 3 | +2470.0824 | [+1044.0335, +4949.3390] | 0.186 | 3/3 |
| transfer-lightgbm | housing | xgboost.LossHigh | lowest | 10 % | 3 | +2197.5915 | [+2031.1699, +2443.2949] | 0.003 | 3/3 |
| transfer-lightgbm | housing | xgboost.LossHigh | lowest | 20 % | 3 | +4760.3783 | [+2826.1534, +5775.3607] | 0.039 | 3/3 |
| transfer-lightgbm | housing | xgboost.LossHigh | lowest | auc | 3 | +2631.7120 | [+2568.4900, +2705.5618] | 0.000 | 3/3 |
| transfer-lightgbm | wine | any.DataOOB | lowest | 5 % | 3 | +0.0420 | [+0.0212, +0.0761] | 0.134 | 3/3 |
| transfer-lightgbm | wine | any.DataOOB | lowest | 10 % | 3 | +0.0208 | [-0.0198, +0.0475] | 0.419 | 2/3 |
| transfer-lightgbm | wine | any.DataOOB | lowest | 20 % | 3 | +0.0670 | [+0.0136, +0.1019] | 0.132 | 3/3 |
| transfer-lightgbm | wine | any.DataOOB | lowest | auc | 3 | +0.0351 | [+0.0013, +0.0582] | 0.180 | 3/3 |
| transfer-lightgbm | wine | catboost.CatBoostLFC | lowest | 5 % | 3 | +0.0041 | [-0.0044, +0.0201] | 0.660 | 1/3 |
| transfer-lightgbm | wine | catboost.CatBoostLFC | lowest | 10 % | 3 | -0.0172 | [-0.0510, +0.0104] | 0.441 | 1/3 |
| transfer-lightgbm | wine | catboost.CatBoostLFC | lowest | 20 % | 3 | +0.0127 | [-0.0211, +0.0568] | 0.637 | 2/3 |
| transfer-lightgbm | wine | catboost.CatBoostLFC | lowest | auc | 3 | -0.0022 | [-0.0253, +0.0170] | 0.873 | 2/3 |
| transfer-lightgbm | wine | catboost.LOO | lowest | 5 % | 3 | +0.0087 | [-0.0002, +0.0204] | 0.291 | 2/3 |
| transfer-lightgbm | wine | catboost.LOO | lowest | 10 % | 3 | -0.0305 | [-0.0663, -0.0098] | 0.232 | 0/3 |
| transfer-lightgbm | wine | catboost.LOO | lowest | 20 % | 3 | -0.0107 | [-0.0640, +0.0221] | 0.729 | 2/3 |
| transfer-lightgbm | wine | catboost.LOO | lowest | auc | 3 | -0.0119 | [-0.0409, +0.0069] | 0.502 | 1/3 |
| transfer-lightgbm | wine | catboost.LossHigh | lowest | 5 % | 3 | +0.0363 | [+0.0181, +0.0500] | 0.062 | 3/3 |
| transfer-lightgbm | wine | catboost.LossHigh | lowest | 10 % | 3 | +0.0293 | [-0.0028, +0.0599] | 0.247 | 2/3 |
| transfer-lightgbm | wine | catboost.LossHigh | lowest | 20 % | 3 | +0.0594 | [-0.0211, +0.1042] | 0.279 | 2/3 |
| transfer-lightgbm | wine | catboost.LossHigh | lowest | auc | 3 | +0.0349 | [-0.0018, +0.0587] | 0.202 | 2/3 |
| transfer-lightgbm | wine | distill-lightgbm.Influence | lowest | 5 % | 3 | +0.0233 | [+0.0039, +0.0399] | 0.156 | 3/3 |
| transfer-lightgbm | wine | distill-lightgbm.Influence | lowest | 10 % | 3 | -0.0076 | [-0.0369, +0.0098] | 0.658 | 2/3 |
| transfer-lightgbm | wine | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0533 | [-0.0159, +0.0952] | 0.266 | 2/3 |
| transfer-lightgbm | wine | distill-lightgbm.Influence | lowest | auc | 3 | +0.0163 | [-0.0168, +0.0338] | 0.429 | 2/3 |
| transfer-lightgbm | wine | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0145 | [+0.0016, +0.0265] | 0.181 | 3/3 |
| transfer-lightgbm | wine | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0346 | [+0.0003, +0.0762] | 0.260 | 3/3 |
| transfer-lightgbm | wine | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0683 | [-0.0038, +0.1192] | 0.207 | 2/3 |
| transfer-lightgbm | wine | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0337 | [-0.0005, +0.0575] | 0.194 | 2/3 |
| transfer-lightgbm | wine | lightgbm.LOO | lowest | 5 % | 3 | +0.0220 | [-0.0016, +0.0416] | 0.224 | 2/3 |
| transfer-lightgbm | wine | lightgbm.LOO | lowest | 10 % | 3 | -0.0126 | [-0.0363, +0.0072] | 0.426 | 1/3 |
| transfer-lightgbm | wine | lightgbm.LOO | lowest | 20 % | 3 | +0.0128 | [-0.0346, +0.0455] | 0.650 | 2/3 |
| transfer-lightgbm | wine | lightgbm.LOO | lowest | auc | 3 | +0.0040 | [-0.0227, +0.0245] | 0.803 | 2/3 |
| transfer-lightgbm | wine | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0261 | [-0.0008, +0.0497] | 0.217 | 2/3 |
| transfer-lightgbm | wine | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0278 | [+0.0052, +0.0492] | 0.160 | 3/3 |
| transfer-lightgbm | wine | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0499 | [-0.0171, +0.0981] | 0.286 | 2/3 |
| transfer-lightgbm | wine | lightgbm.LossHigh | lowest | auc | 3 | +0.0294 | [-0.0025, +0.0554] | 0.225 | 2/3 |
| transfer-lightgbm | wine | pytorch.Influence | lowest | 5 % | 3 | +0.0026 | [-0.0154, +0.0224] | 0.835 | 2/3 |
| transfer-lightgbm | wine | pytorch.Influence | lowest | 10 % | 3 | -0.0132 | [-0.0229, +0.0009] | 0.209 | 1/3 |
| transfer-lightgbm | wine | pytorch.Influence | lowest | 20 % | 3 | -0.0101 | [-0.0388, +0.0279] | 0.661 | 1/3 |
| transfer-lightgbm | wine | pytorch.Influence | lowest | auc | 3 | -0.0068 | [-0.0222, +0.0075] | 0.509 | 1/3 |
| transfer-lightgbm | wine | pytorch.LOO | lowest | 5 % | 3 | +0.0214 | [-0.0004, +0.0413] | 0.219 | 2/3 |
| transfer-lightgbm | wine | pytorch.LOO | lowest | 10 % | 3 | -0.0118 | [-0.0325, +0.0293] | 0.624 | 1/3 |
| transfer-lightgbm | wine | pytorch.LOO | lowest | 20 % | 3 | +0.0388 | [-0.0041, +0.0840] | 0.267 | 2/3 |
| transfer-lightgbm | wine | pytorch.LOO | lowest | auc | 3 | +0.0106 | [-0.0029, +0.0319] | 0.428 | 2/3 |
| transfer-lightgbm | wine | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0196 | [+0.0047, +0.0374] | 0.177 | 3/3 |
| transfer-lightgbm | wine | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0087 | [-0.0359, +0.0402] | 0.741 | 2/3 |
| transfer-lightgbm | wine | pytorch.LissaInfluence | lowest | 20 % | 3 | +0.0399 | [-0.0245, +0.0726] | 0.341 | 2/3 |
| transfer-lightgbm | wine | pytorch.LissaInfluence | lowest | auc | 3 | +0.0181 | [-0.0184, +0.0371] | 0.426 | 2/3 |
| transfer-lightgbm | wine | pytorch.LossHigh | lowest | 5 % | 3 | +0.0191 | [-0.0120, +0.0441] | 0.367 | 2/3 |
| transfer-lightgbm | wine | pytorch.LossHigh | lowest | 10 % | 3 | +0.0500 | [+0.0007, +0.0749] | 0.180 | 3/3 |
| transfer-lightgbm | wine | pytorch.LossHigh | lowest | 20 % | 3 | +0.0721 | [+0.0042, +0.1235] | 0.179 | 3/3 |
| transfer-lightgbm | wine | pytorch.LossHigh | lowest | auc | 3 | +0.0415 | [+0.0076, +0.0611] | 0.135 | 3/3 |
| transfer-lightgbm | wine | random_forest.LOO | lowest | 5 % | 3 | +0.0100 | [+0.0040, +0.0171] | 0.122 | 3/3 |
| transfer-lightgbm | wine | random_forest.LOO | lowest | 10 % | 3 | -0.0281 | [-0.0443, -0.0177] | 0.076 | 0/3 |
| transfer-lightgbm | wine | random_forest.LOO | lowest | 20 % | 3 | +0.0084 | [-0.0404, +0.0340] | 0.763 | 2/3 |
| transfer-lightgbm | wine | random_forest.LOO | lowest | auc | 3 | -0.0059 | [-0.0245, +0.0056] | 0.591 | 2/3 |
| transfer-lightgbm | wine | random_forest.LossHigh | lowest | 5 % | 3 | +0.0287 | [+0.0020, +0.0528] | 0.191 | 3/3 |
| transfer-lightgbm | wine | random_forest.LossHigh | lowest | 10 % | 3 | +0.0116 | [-0.0094, +0.0278] | 0.402 | 2/3 |
| transfer-lightgbm | wine | random_forest.LossHigh | lowest | 20 % | 3 | +0.0667 | [+0.0265, +0.0920] | 0.082 | 3/3 |
| transfer-lightgbm | wine | random_forest.LossHigh | lowest | auc | 3 | +0.0282 | [+0.0109, +0.0398] | 0.085 | 3/3 |
| transfer-lightgbm | wine | xgboost.LOO | lowest | 5 % | 3 | +0.0148 | [+0.0002, +0.0290] | 0.218 | 3/3 |
| transfer-lightgbm | wine | xgboost.LOO | lowest | 10 % | 3 | -0.0100 | [-0.0511, +0.0286] | 0.706 | 1/3 |
| transfer-lightgbm | wine | xgboost.LOO | lowest | 20 % | 3 | +0.0222 | [-0.0151, +0.0531] | 0.382 | 2/3 |
| transfer-lightgbm | wine | xgboost.LOO | lowest | auc | 3 | +0.0055 | [-0.0157, +0.0278] | 0.706 | 2/3 |
| transfer-lightgbm | wine | xgboost.LossHigh | lowest | 5 % | 3 | +0.0263 | [+0.0239, +0.0312] | 0.008 | 3/3 |
| transfer-lightgbm | wine | xgboost.LossHigh | lowest | 10 % | 3 | -0.0053 | [-0.0101, +0.0022] | 0.298 | 1/3 |
| transfer-lightgbm | wine | xgboost.LossHigh | lowest | 20 % | 3 | +0.0005 | [-0.0319, +0.0241] | 0.981 | 2/3 |
| transfer-lightgbm | wine | xgboost.LossHigh | lowest | auc | 3 | +0.0047 | [-0.0040, +0.0129] | 0.435 | 2/3 |
| transfer-pytorch | adult | any.DataOOB | lowest | 5 % | 3 | +0.0008 | [-0.0014, +0.0039] | 0.670 | 1/3 |
| transfer-pytorch | adult | any.DataOOB | lowest | 10 % | 3 | -0.0007 | [-0.0050, +0.0047] | 0.820 | 1/3 |
| transfer-pytorch | adult | any.DataOOB | lowest | 20 % | 3 | +0.0043 | [-0.0136, +0.0233] | 0.723 | 2/3 |
| transfer-pytorch | adult | any.DataOOB | lowest | auc | 3 | +0.0010 | [-0.0044, +0.0049] | 0.755 | 2/3 |
| transfer-pytorch | adult | any.KNNShapley | lowest | 5 % | 3 | -0.0065 | [-0.0147, +0.0053] | 0.397 | 1/3 |
| transfer-pytorch | adult | any.KNNShapley | lowest | 10 % | 3 | -0.0079 | [-0.0223, +0.0039] | 0.413 | 1/3 |
| transfer-pytorch | adult | any.KNNShapley | lowest | 20 % | 3 | -0.0151 | [-0.0317, +0.0046] | 0.289 | 1/3 |
| transfer-pytorch | adult | any.KNNShapley | lowest | auc | 3 | -0.0084 | [-0.0200, +0.0005] | 0.302 | 1/3 |
| transfer-pytorch | adult | catboost.CatBoostLFC | lowest | 5 % | 3 | -0.0033 | [-0.0252, +0.0078] | 0.795 | 2/3 |
| transfer-pytorch | adult | catboost.CatBoostLFC | lowest | 10 % | 3 | -0.0005 | [-0.0065, +0.0075] | 0.918 | 1/3 |
| transfer-pytorch | adult | catboost.CatBoostLFC | lowest | 20 % | 3 | -0.0041 | [-0.0087, +0.0040] | 0.416 | 1/3 |
| transfer-pytorch | adult | catboost.CatBoostLFC | lowest | auc | 3 | -0.0020 | [-0.0094, +0.0057] | 0.688 | 1/3 |
| transfer-pytorch | adult | catboost.LOO | lowest | 5 % | 3 | -0.0045 | [-0.0164, +0.0040] | 0.544 | 1/3 |
| transfer-pytorch | adult | catboost.LOO | lowest | 10 % | 3 | -0.0060 | [-0.0198, +0.0064] | 0.513 | 1/3 |
| transfer-pytorch | adult | catboost.LOO | lowest | 20 % | 3 | -0.0049 | [-0.0118, +0.0059] | 0.464 | 1/3 |
| transfer-pytorch | adult | catboost.LOO | lowest | auc | 3 | -0.0046 | [-0.0137, +0.0049] | 0.483 | 1/3 |
| transfer-pytorch | adult | catboost.LossHigh | lowest | 5 % | 3 | +0.0027 | [-0.0015, +0.0050] | 0.327 | 2/3 |
| transfer-pytorch | adult | catboost.LossHigh | lowest | 10 % | 3 | +0.0029 | [-0.0034, +0.0060] | 0.455 | 2/3 |
| transfer-pytorch | adult | catboost.LossHigh | lowest | 20 % | 3 | -0.0041 | [-0.0099, +0.0074] | 0.550 | 1/3 |
| transfer-pytorch | adult | catboost.LossHigh | lowest | auc | 3 | +0.0007 | [-0.0026, +0.0053] | 0.787 | 1/3 |
| transfer-pytorch | adult | distill-lightgbm.Influence | lowest | 5 % | 3 | +0.0028 | [-0.0076, +0.0106] | 0.660 | 2/3 |
| transfer-pytorch | adult | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0002 | [-0.0066, +0.0133] | 0.977 | 1/3 |
| transfer-pytorch | adult | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0059 | [-0.0061, +0.0202] | 0.522 | 2/3 |
| transfer-pytorch | adult | distill-lightgbm.Influence | lowest | auc | 3 | +0.0022 | [-0.0033, +0.0061] | 0.510 | 2/3 |
| transfer-pytorch | adult | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0043 | [-0.0031, +0.0097] | 0.376 | 2/3 |
| transfer-pytorch | adult | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0033 | [-0.0014, +0.0118] | 0.514 | 1/3 |
| transfer-pytorch | adult | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0022 | [-0.0065, +0.0153] | 0.769 | 1/3 |
| transfer-pytorch | adult | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0029 | [-0.0025, +0.0057] | 0.398 | 2/3 |
| transfer-pytorch | adult | lightgbm.LOO | lowest | 5 % | 3 | +0.0008 | [-0.0063, +0.0057] | 0.842 | 2/3 |
| transfer-pytorch | adult | lightgbm.LOO | lowest | 10 % | 3 | -0.0014 | [-0.0044, +0.0038] | 0.638 | 1/3 |
| transfer-pytorch | adult | lightgbm.LOO | lowest | 20 % | 3 | +0.0014 | [-0.0097, +0.0176] | 0.885 | 1/3 |
| transfer-pytorch | adult | lightgbm.LOO | lowest | auc | 3 | +0.0000 | [-0.0053, +0.0042] | 0.998 | 2/3 |
| transfer-pytorch | adult | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0070 | [+0.0008, +0.0137] | 0.203 | 3/3 |
| transfer-pytorch | adult | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0012 | [-0.0025, +0.0066] | 0.717 | 1/3 |
| transfer-pytorch | adult | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0048 | [-0.0142, +0.0299] | 0.751 | 1/3 |
| transfer-pytorch | adult | lightgbm.LossHigh | lowest | auc | 3 | +0.0034 | [-0.0011, +0.0088] | 0.366 | 2/3 |
| transfer-pytorch | adult | pytorch.Influence | lowest | 5 % | 3 | +0.0043 | [-0.0011, +0.0078] | 0.258 | 2/3 |
| transfer-pytorch | adult | pytorch.Influence | lowest | 10 % | 3 | +0.0056 | [+0.0050, +0.0069] | 0.013 | 3/3 |
| transfer-pytorch | adult | pytorch.Influence | lowest | 20 % | 3 | +0.0084 | [-0.0005, +0.0164] | 0.229 | 2/3 |
| transfer-pytorch | adult | pytorch.Influence | lowest | auc | 3 | +0.0053 | [+0.0033, +0.0079] | 0.062 | 3/3 |
| transfer-pytorch | adult | pytorch.LOO | lowest | 5 % | 3 | +0.0041 | [+0.0018, +0.0069] | 0.110 | 3/3 |
| transfer-pytorch | adult | pytorch.LOO | lowest | 10 % | 3 | -0.0107 | [-0.0408, +0.0104] | 0.561 | 1/3 |
| transfer-pytorch | adult | pytorch.LOO | lowest | 20 % | 3 | -0.0063 | [-0.0199, +0.0006] | 0.451 | 2/3 |
| transfer-pytorch | adult | pytorch.LOO | lowest | auc | 3 | -0.0046 | [-0.0185, +0.0049] | 0.589 | 1/3 |
| transfer-pytorch | adult | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0045 | [-0.0010, +0.0095] | 0.276 | 2/3 |
| transfer-pytorch | adult | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0008 | [-0.0085, +0.0099] | 0.894 | 2/3 |
| transfer-pytorch | adult | pytorch.LissaInfluence | lowest | 20 % | 3 | -0.0017 | [-0.0061, +0.0044] | 0.641 | 1/3 |
| transfer-pytorch | adult | pytorch.LissaInfluence | lowest | auc | 3 | +0.0010 | [-0.0034, +0.0052] | 0.726 | 2/3 |
| transfer-pytorch | adult | pytorch.LossHigh | lowest | 5 % | 3 | +0.0036 | [-0.0006, +0.0076] | 0.264 | 2/3 |
| transfer-pytorch | adult | pytorch.LossHigh | lowest | 10 % | 3 | -0.0046 | [-0.0075, -0.0009] | 0.139 | 0/3 |
| transfer-pytorch | adult | pytorch.LossHigh | lowest | 20 % | 3 | -0.0128 | [-0.0249, -0.0041] | 0.178 | 0/3 |
| transfer-pytorch | adult | pytorch.LossHigh | lowest | auc | 3 | -0.0040 | [-0.0047, -0.0033] | 0.009 | 0/3 |
| transfer-pytorch | adult | random_forest.LOO | lowest | 5 % | 3 | +0.0030 | [+0.0020, +0.0043] | 0.049 | 3/3 |
| transfer-pytorch | adult | random_forest.LOO | lowest | 10 % | 3 | +0.0063 | [-0.0031, +0.0115] | 0.312 | 2/3 |
| transfer-pytorch | adult | random_forest.LOO | lowest | 20 % | 3 | +0.0044 | [-0.0102, +0.0237] | 0.704 | 1/3 |
| transfer-pytorch | adult | random_forest.LOO | lowest | auc | 3 | +0.0042 | [-0.0006, +0.0113] | 0.362 | 2/3 |
| transfer-pytorch | adult | random_forest.LossHigh | lowest | 5 % | 3 | -0.0002 | [-0.0049, +0.0029] | 0.934 | 2/3 |
| transfer-pytorch | adult | random_forest.LossHigh | lowest | 10 % | 3 | -0.0010 | [-0.0088, +0.0069] | 0.842 | 1/3 |
| transfer-pytorch | adult | random_forest.LossHigh | lowest | 20 % | 3 | -0.0133 | [-0.0226, -0.0081] | 0.103 | 0/3 |
| transfer-pytorch | adult | random_forest.LossHigh | lowest | auc | 3 | -0.0038 | [-0.0068, -0.0021] | 0.134 | 0/3 |
| transfer-pytorch | adult | xgboost.LOO | lowest | 5 % | 3 | +0.0068 | [+0.0043, +0.0087] | 0.035 | 3/3 |
| transfer-pytorch | adult | xgboost.LOO | lowest | 10 % | 3 | +0.0034 | [-0.0011, +0.0095] | 0.398 | 2/3 |
| transfer-pytorch | adult | xgboost.LOO | lowest | 20 % | 3 | +0.0068 | [-0.0048, +0.0209] | 0.461 | 2/3 |
| transfer-pytorch | adult | xgboost.LOO | lowest | auc | 3 | +0.0047 | [+0.0028, +0.0070] | 0.062 | 3/3 |
| transfer-pytorch | adult | xgboost.LossHigh | lowest | 5 % | 3 | -0.0023 | [-0.0192, +0.0084] | 0.816 | 2/3 |
| transfer-pytorch | adult | xgboost.LossHigh | lowest | 10 % | 3 | +0.0019 | [-0.0021, +0.0057] | 0.482 | 2/3 |
| transfer-pytorch | adult | xgboost.LossHigh | lowest | 20 % | 3 | +0.0008 | [-0.0030, +0.0053] | 0.773 | 2/3 |
| transfer-pytorch | adult | xgboost.LossHigh | lowest | auc | 3 | +0.0003 | [-0.0056, +0.0056] | 0.924 | 2/3 |
| transfer-pytorch | covertype | any.DataOOB | lowest | 5 % | 3 | +0.0054 | [-0.0012, +0.0108] | 0.264 | 2/3 |
| transfer-pytorch | covertype | any.DataOOB | lowest | 10 % | 3 | -0.0031 | [-0.0232, +0.0128] | 0.800 | 2/3 |
| transfer-pytorch | covertype | any.DataOOB | lowest | 20 % | 3 | +0.0063 | [-0.0036, +0.0140] | 0.351 | 2/3 |
| transfer-pytorch | covertype | any.DataOOB | lowest | auc | 3 | +0.0018 | [-0.0055, +0.0085] | 0.706 | 2/3 |
| transfer-pytorch | covertype | any.KNNShapley | lowest | 5 % | 3 | +0.0002 | [-0.0068, +0.0086] | 0.969 | 1/3 |
| transfer-pytorch | covertype | any.KNNShapley | lowest | 10 % | 3 | -0.0026 | [-0.0058, +0.0022] | 0.399 | 1/3 |
| transfer-pytorch | covertype | any.KNNShapley | lowest | 20 % | 3 | -0.0189 | [-0.0212, -0.0148] | 0.012 | 0/3 |
| transfer-pytorch | covertype | any.KNNShapley | lowest | auc | 3 | -0.0057 | [-0.0078, -0.0031] | 0.053 | 0/3 |
| transfer-pytorch | covertype | catboost.LOO | lowest | 5 % | 3 | +0.0011 | [-0.0032, +0.0062] | 0.735 | 2/3 |
| transfer-pytorch | covertype | catboost.LOO | lowest | 10 % | 3 | +0.0021 | [-0.0052, +0.0104] | 0.693 | 2/3 |
| transfer-pytorch | covertype | catboost.LOO | lowest | 20 % | 3 | +0.0001 | [-0.0078, +0.0048] | 0.976 | 2/3 |
| transfer-pytorch | covertype | catboost.LOO | lowest | auc | 3 | +0.0011 | [-0.0039, +0.0063] | 0.749 | 2/3 |
| transfer-pytorch | covertype | catboost.LossHigh | lowest | 5 % | 3 | +0.0044 | [-0.0028, +0.0088] | 0.349 | 2/3 |
| transfer-pytorch | covertype | catboost.LossHigh | lowest | 10 % | 3 | +0.0009 | [-0.0066, +0.0084] | 0.849 | 2/3 |
| transfer-pytorch | covertype | catboost.LossHigh | lowest | 20 % | 3 | +0.0066 | [+0.0022, +0.0092] | 0.096 | 3/3 |
| transfer-pytorch | covertype | catboost.LossHigh | lowest | auc | 3 | +0.0031 | [+0.0020, +0.0045] | 0.054 | 3/3 |
| transfer-pytorch | covertype | distill-lightgbm.Influence | lowest | 5 % | 3 | -0.0021 | [-0.0046, +0.0006] | 0.293 | 1/3 |
| transfer-pytorch | covertype | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0027 | [-0.0044, +0.0084] | 0.551 | 2/3 |
| transfer-pytorch | covertype | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0041 | [+0.0004, +0.0076] | 0.186 | 3/3 |
| transfer-pytorch | covertype | distill-lightgbm.Influence | lowest | auc | 3 | +0.0015 | [-0.0021, +0.0044] | 0.518 | 2/3 |
| transfer-pytorch | covertype | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0037 | [-0.0008, +0.0066] | 0.245 | 2/3 |
| transfer-pytorch | covertype | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0019 | [-0.0050, +0.0056] | 0.633 | 2/3 |
| transfer-pytorch | covertype | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0069 | [-0.0008, +0.0124] | 0.225 | 2/3 |
| transfer-pytorch | covertype | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0034 | [-0.0004, +0.0057] | 0.220 | 2/3 |
| transfer-pytorch | covertype | lightgbm.LOO | lowest | 5 % | 3 | -0.0028 | [-0.0108, +0.0064] | 0.632 | 1/3 |
| transfer-pytorch | covertype | lightgbm.LOO | lowest | 10 % | 3 | -0.0024 | [-0.0158, +0.0070] | 0.760 | 2/3 |
| transfer-pytorch | covertype | lightgbm.LOO | lowest | 20 % | 3 | -0.0059 | [-0.0124, +0.0004] | 0.253 | 1/3 |
| transfer-pytorch | covertype | lightgbm.LOO | lowest | auc | 3 | -0.0031 | [-0.0100, +0.0008] | 0.472 | 2/3 |
| transfer-pytorch | covertype | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0008 | [-0.0108, +0.0080] | 0.904 | 2/3 |
| transfer-pytorch | covertype | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0055 | [-0.0044, +0.0116] | 0.387 | 2/3 |
| transfer-pytorch | covertype | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0023 | [-0.0050, +0.0068] | 0.600 | 2/3 |
| transfer-pytorch | covertype | lightgbm.LossHigh | lowest | auc | 3 | +0.0028 | [+0.0013, +0.0042] | 0.076 | 3/3 |
| transfer-pytorch | covertype | pytorch.Influence | lowest | 5 % | 3 | -0.0021 | [-0.0090, +0.0058] | 0.669 | 1/3 |
| transfer-pytorch | covertype | pytorch.Influence | lowest | 10 % | 3 | -0.0095 | [-0.0252, -0.0004] | 0.349 | 0/3 |
| transfer-pytorch | covertype | pytorch.Influence | lowest | 20 % | 3 | -0.0027 | [-0.0106, +0.0032] | 0.574 | 1/3 |
| transfer-pytorch | covertype | pytorch.Influence | lowest | auc | 3 | -0.0048 | [-0.0129, +0.0001] | 0.362 | 1/3 |
| transfer-pytorch | covertype | pytorch.LOO | lowest | 5 % | 3 | +0.0021 | [+0.0002, +0.0050] | 0.299 | 3/3 |
| transfer-pytorch | covertype | pytorch.LOO | lowest | 10 % | 3 | +0.0043 | [+0.0014, +0.0060] | 0.098 | 3/3 |
| transfer-pytorch | covertype | pytorch.LOO | lowest | 20 % | 3 | +0.0055 | [+0.0008, +0.0100] | 0.176 | 3/3 |
| transfer-pytorch | covertype | pytorch.LOO | lowest | auc | 3 | +0.0035 | [+0.0022, +0.0060] | 0.110 | 3/3 |
| transfer-pytorch | covertype | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0005 | [-0.0044, +0.0078] | 0.899 | 1/3 |
| transfer-pytorch | covertype | pytorch.LissaInfluence | lowest | 10 % | 3 | -0.0189 | [-0.0248, -0.0122] | 0.035 | 0/3 |
| transfer-pytorch | covertype | pytorch.LissaInfluence | lowest | 20 % | 3 | -0.0187 | [-0.0240, -0.0152] | 0.020 | 0/3 |
| transfer-pytorch | covertype | pytorch.LissaInfluence | lowest | auc | 3 | -0.0116 | [-0.0164, -0.0088] | 0.040 | 0/3 |
| transfer-pytorch | covertype | pytorch.LossHigh | lowest | 5 % | 3 | +0.0017 | [-0.0040, +0.0048] | 0.617 | 2/3 |
| transfer-pytorch | covertype | pytorch.LossHigh | lowest | 10 % | 3 | +0.0005 | [-0.0076, +0.0072] | 0.913 | 2/3 |
| transfer-pytorch | covertype | pytorch.LossHigh | lowest | 20 % | 3 | +0.0001 | [-0.0056, +0.0086] | 0.989 | 1/3 |
| transfer-pytorch | covertype | pytorch.LossHigh | lowest | auc | 3 | +0.0006 | [-0.0030, +0.0038] | 0.782 | 2/3 |
| transfer-pytorch | covertype | random_forest.LOO | lowest | 5 % | 3 | -0.0047 | [-0.0076, +0.0004] | 0.208 | 1/3 |
| transfer-pytorch | covertype | random_forest.LOO | lowest | 10 % | 3 | -0.0011 | [-0.0098, +0.0056] | 0.837 | 2/3 |
| transfer-pytorch | covertype | random_forest.LOO | lowest | 20 % | 3 | +0.0023 | [-0.0032, +0.0082] | 0.552 | 2/3 |
| transfer-pytorch | covertype | random_forest.LOO | lowest | auc | 3 | -0.0010 | [-0.0031, +0.0023] | 0.610 | 1/3 |
| transfer-pytorch | covertype | random_forest.LossHigh | lowest | 5 % | 3 | +0.0084 | [+0.0032, +0.0134] | 0.104 | 3/3 |
| transfer-pytorch | covertype | random_forest.LossHigh | lowest | 10 % | 3 | -0.0037 | [-0.0100, +0.0006] | 0.374 | 1/3 |
| transfer-pytorch | covertype | random_forest.LossHigh | lowest | 20 % | 3 | +0.0052 | [-0.0054, +0.0124] | 0.438 | 2/3 |
| transfer-pytorch | covertype | random_forest.LossHigh | lowest | auc | 3 | +0.0020 | [+0.0002, +0.0032] | 0.159 | 3/3 |
| transfer-pytorch | covertype | xgboost.LOO | lowest | 5 % | 3 | -0.0021 | [-0.0064, +0.0062] | 0.660 | 1/3 |
| transfer-pytorch | covertype | xgboost.LOO | lowest | 10 % | 3 | -0.0029 | [-0.0066, +0.0002] | 0.277 | 1/3 |
| transfer-pytorch | covertype | xgboost.LOO | lowest | 20 % | 3 | +0.0033 | [-0.0022, +0.0070] | 0.363 | 2/3 |
| transfer-pytorch | covertype | xgboost.LOO | lowest | auc | 3 | -0.0008 | [-0.0046, +0.0019] | 0.715 | 2/3 |
| transfer-pytorch | covertype | xgboost.LossHigh | lowest | 5 % | 3 | +0.0013 | [-0.0134, +0.0122] | 0.883 | 2/3 |
| transfer-pytorch | covertype | xgboost.LossHigh | lowest | 10 % | 3 | +0.0012 | [-0.0070, +0.0130] | 0.861 | 1/3 |
| transfer-pytorch | covertype | xgboost.LossHigh | lowest | 20 % | 3 | -0.0047 | [-0.0100, +0.0032] | 0.365 | 1/3 |
| transfer-pytorch | covertype | xgboost.LossHigh | lowest | auc | 3 | -0.0004 | [-0.0032, +0.0023] | 0.825 | 1/3 |
| transfer-pytorch | housing | any.DataOOB | lowest | 5 % | 3 | +976.4361 | [-252.1054, +1656.1852] | 0.254 | 2/3 |
| transfer-pytorch | housing | any.DataOOB | lowest | 10 % | 3 | +3600.0929 | [+2750.6349, +4047.9916] | 0.014 | 3/3 |
| transfer-pytorch | housing | any.DataOOB | lowest | 20 % | 3 | +3765.2398 | [+2429.3987, +6057.7926] | 0.082 | 3/3 |
| transfer-pytorch | housing | any.DataOOB | lowest | auc | 3 | +2535.4538 | [+1575.8114, +3429.1140] | 0.042 | 3/3 |
| transfer-pytorch | housing | catboost.CatBoostLFC | lowest | 5 % | 3 | -1481.4244 | [-2441.6418, -759.4160] | 0.098 | 0/3 |
| transfer-pytorch | housing | catboost.CatBoostLFC | lowest | 10 % | 3 | -1397.2190 | [-2522.3927, -496.7459] | 0.144 | 0/3 |
| transfer-pytorch | housing | catboost.CatBoostLFC | lowest | 20 % | 3 | -3821.0108 | [-6398.1899, -1392.0980] | 0.118 | 0/3 |
| transfer-pytorch | housing | catboost.CatBoostLFC | lowest | auc | 3 | -1849.5659 | [-3155.8552, -845.1080] | 0.114 | 0/3 |
| transfer-pytorch | housing | catboost.LOO | lowest | 5 % | 3 | -184.8278 | [-331.3505, +82.1125] | 0.301 | 1/3 |
| transfer-pytorch | housing | catboost.LOO | lowest | 10 % | 3 | +496.9297 | [-209.5025, +1054.0146] | 0.314 | 2/3 |
| transfer-pytorch | housing | catboost.LOO | lowest | 20 % | 3 | +1402.8520 | [+641.5789, +1833.7392] | 0.067 | 3/3 |
| transfer-pytorch | housing | catboost.LOO | lowest | auc | 3 | +490.8547 | [-1.0063, +874.2184] | 0.198 | 2/3 |
| transfer-pytorch | housing | catboost.LossHigh | lowest | 5 % | 3 | -479.8773 | [-1797.7080, +1679.1177] | 0.702 | 1/3 |
| transfer-pytorch | housing | catboost.LossHigh | lowest | 10 % | 3 | +2993.3073 | [+1145.6594, +4633.7281] | 0.098 | 3/3 |
| transfer-pytorch | housing | catboost.LossHigh | lowest | 20 % | 3 | +1739.9680 | [-3.7353, +3532.5749] | 0.231 | 2/3 |
| transfer-pytorch | housing | catboost.LossHigh | lowest | auc | 3 | +1437.5129 | [+402.9614, +3040.5712] | 0.219 | 3/3 |
| transfer-pytorch | housing | distill-lightgbm.Influence | lowest | 5 % | 3 | +994.0222 | [+401.2208, +1293.4626] | 0.079 | 3/3 |
| transfer-pytorch | housing | distill-lightgbm.Influence | lowest | 10 % | 3 | +1279.9329 | [+484.4500, +2165.8211] | 0.120 | 3/3 |
| transfer-pytorch | housing | distill-lightgbm.Influence | lowest | 20 % | 3 | +1725.7078 | [+1151.5086, +2620.9557] | 0.063 | 3/3 |
| transfer-pytorch | housing | distill-lightgbm.Influence | lowest | auc | 3 | +1159.9074 | [+1055.7958, +1263.6529] | 0.003 | 3/3 |
| transfer-pytorch | housing | distill-lightgbm.LossHigh | lowest | 5 % | 3 | -903.7067 | [-1827.6278, +37.2976] | 0.235 | 1/3 |
| transfer-pytorch | housing | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +3154.5216 | [+1871.9739, +4249.2331] | 0.045 | 3/3 |
| transfer-pytorch | housing | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +2690.0502 | [+784.6007, +4560.0700] | 0.132 | 3/3 |
| transfer-pytorch | housing | distill-lightgbm.LossHigh | lowest | auc | 3 | +1629.5315 | [+441.2334, +2742.8043] | 0.134 | 3/3 |
| transfer-pytorch | housing | lightgbm.LOO | lowest | 5 % | 3 | -296.9609 | [-683.6935, +180.8217] | 0.362 | 1/3 |
| transfer-pytorch | housing | lightgbm.LOO | lowest | 10 % | 3 | +1481.1774 | [+1026.0507, +1878.3582] | 0.027 | 3/3 |
| transfer-pytorch | housing | lightgbm.LOO | lowest | 20 % | 3 | +1385.7385 | [+910.0349, +1784.9537] | 0.032 | 3/3 |
| transfer-pytorch | housing | lightgbm.LOO | lowest | auc | 3 | +827.6359 | [+441.3544, +1195.8282] | 0.063 | 3/3 |
| transfer-pytorch | housing | lightgbm.LossHigh | lowest | 5 % | 3 | +259.9339 | [-323.0816, +843.7562] | 0.521 | 2/3 |
| transfer-pytorch | housing | lightgbm.LossHigh | lowest | 10 % | 3 | +3154.2434 | [+2209.8544, +3689.3960] | 0.022 | 3/3 |
| transfer-pytorch | housing | lightgbm.LossHigh | lowest | 20 % | 3 | +3583.0696 | [+2489.8289, +5427.6286] | 0.061 | 3/3 |
| transfer-pytorch | housing | lightgbm.LossHigh | lowest | auc | 3 | +2143.5922 | [+1455.8628, +2805.2124] | 0.032 | 3/3 |
| transfer-pytorch | housing | pytorch.Influence | lowest | 5 % | 3 | +710.4238 | [-444.1957, +1593.8517] | 0.360 | 2/3 |
| transfer-pytorch | housing | pytorch.Influence | lowest | 10 % | 3 | +1393.9779 | [+625.4683, +2361.3379] | 0.112 | 3/3 |
| transfer-pytorch | housing | pytorch.Influence | lowest | 20 % | 3 | +1172.2944 | [-150.1665, +2361.6460] | 0.249 | 2/3 |
| transfer-pytorch | housing | pytorch.Influence | lowest | auc | 3 | +993.4213 | [+85.9601, +1874.3761] | 0.194 | 3/3 |
| transfer-pytorch | housing | pytorch.LOO | lowest | 5 % | 3 | +62.2869 | [-700.1889, +743.5161] | 0.895 | 2/3 |
| transfer-pytorch | housing | pytorch.LOO | lowest | 10 % | 3 | +1068.0070 | [+177.0936, +1615.0508] | 0.141 | 3/3 |
| transfer-pytorch | housing | pytorch.LOO | lowest | 20 % | 3 | +2548.8631 | [+2109.9783, +3283.1767] | 0.020 | 3/3 |
| transfer-pytorch | housing | pytorch.LOO | lowest | auc | 3 | +1053.2901 | [+881.9011, +1204.8860] | 0.008 | 3/3 |
| transfer-pytorch | housing | pytorch.LissaInfluence | lowest | 5 % | 3 | +234.3438 | [-1478.3535, +3229.8973] | 0.890 | 1/3 |
| transfer-pytorch | housing | pytorch.LissaInfluence | lowest | 10 % | 3 | -499.3142 | [-2656.3544, +3278.0195] | 0.817 | 1/3 |
| transfer-pytorch | housing | pytorch.LissaInfluence | lowest | 20 % | 3 | -5551.2628 | [-9490.0062, +1366.0688] | 0.251 | 1/3 |
| transfer-pytorch | housing | pytorch.LissaInfluence | lowest | auc | 3 | -1516.4726 | [-3536.9429, +2378.2488] | 0.518 | 1/3 |
| transfer-pytorch | housing | pytorch.LossHigh | lowest | 5 % | 3 | -854.5566 | [-2476.7996, +84.1066] | 0.404 | 1/3 |
| transfer-pytorch | housing | pytorch.LossHigh | lowest | 10 % | 3 | +3343.0733 | [+2049.3794, +4228.3931] | 0.037 | 3/3 |
| transfer-pytorch | housing | pytorch.LossHigh | lowest | 20 % | 3 | +3239.0433 | [+1404.2656, +4165.5563] | 0.072 | 3/3 |
| transfer-pytorch | housing | pytorch.LossHigh | lowest | auc | 3 | +1849.7741 | [+500.3838, +2579.7301] | 0.111 | 3/3 |
| transfer-pytorch | housing | random_forest.LOO | lowest | 5 % | 3 | +117.6257 | [-386.0083, +873.7716] | 0.789 | 1/3 |
| transfer-pytorch | housing | random_forest.LOO | lowest | 10 % | 3 | +918.1296 | [+173.6565, +1632.7386] | 0.161 | 3/3 |
| transfer-pytorch | housing | random_forest.LOO | lowest | 20 % | 3 | +1259.8984 | [+45.1095, +2267.4414] | 0.192 | 3/3 |
| transfer-pytorch | housing | random_forest.LOO | lowest | auc | 3 | +688.6796 | [+42.6770, +1397.5802] | 0.221 | 3/3 |
| transfer-pytorch | housing | random_forest.LossHigh | lowest | 5 % | 3 | -239.1222 | [-1556.5567, +954.9822] | 0.774 | 1/3 |
| transfer-pytorch | housing | random_forest.LossHigh | lowest | 10 % | 3 | +3357.6166 | [+2668.1597, +3776.0269] | 0.011 | 3/3 |
| transfer-pytorch | housing | random_forest.LossHigh | lowest | 20 % | 3 | +3973.3424 | [+2399.6040, +5596.9767] | 0.050 | 3/3 |
| transfer-pytorch | housing | random_forest.LossHigh | lowest | auc | 3 | +2192.6612 | [+1571.5128, +2580.3558] | 0.020 | 3/3 |
| transfer-pytorch | housing | xgboost.LOO | lowest | 5 % | 3 | +414.3357 | [-559.5340, +948.7159] | 0.485 | 2/3 |
| transfer-pytorch | housing | xgboost.LOO | lowest | 10 % | 3 | +25.8590 | [-448.2269, +657.3645] | 0.944 | 1/3 |
| transfer-pytorch | housing | xgboost.LOO | lowest | 20 % | 3 | +445.9033 | [-322.6150, +1265.6400] | 0.434 | 2/3 |
| transfer-pytorch | housing | xgboost.LOO | lowest | auc | 3 | +224.7569 | [+83.4674, +385.5039] | 0.125 | 3/3 |
| transfer-pytorch | housing | xgboost.LossHigh | lowest | 5 % | 3 | +299.6116 | [-543.6746, +937.0491] | 0.566 | 2/3 |
| transfer-pytorch | housing | xgboost.LossHigh | lowest | 10 % | 3 | +378.1992 | [-386.2603, +1705.6548] | 0.628 | 1/3 |
| transfer-pytorch | housing | xgboost.LossHigh | lowest | 20 % | 3 | +1762.3775 | [+359.4989, +2516.0462] | 0.129 | 3/3 |
| transfer-pytorch | housing | xgboost.LossHigh | lowest | auc | 3 | +657.3220 | [+71.3922, +1132.7134] | 0.169 | 3/3 |
| transfer-pytorch | wine | any.DataOOB | lowest | 5 % | 3 | -0.0081 | [-0.0149, -0.0039] | 0.145 | 0/3 |
| transfer-pytorch | wine | any.DataOOB | lowest | 10 % | 3 | +0.0037 | [+0.0028, +0.0050] | 0.032 | 3/3 |
| transfer-pytorch | wine | any.DataOOB | lowest | 20 % | 3 | -0.0018 | [-0.0108, +0.0053] | 0.740 | 2/3 |
| transfer-pytorch | wine | any.DataOOB | lowest | auc | 3 | -0.0011 | [-0.0030, +0.0002] | 0.381 | 1/3 |
| transfer-pytorch | wine | catboost.CatBoostLFC | lowest | 5 % | 3 | -0.0095 | [-0.0173, +0.0017] | 0.241 | 1/3 |
| transfer-pytorch | wine | catboost.CatBoostLFC | lowest | 10 % | 3 | -0.0158 | [-0.0306, +0.0073] | 0.311 | 1/3 |
| transfer-pytorch | wine | catboost.CatBoostLFC | lowest | 20 % | 3 | -0.0193 | [-0.0325, -0.0009] | 0.178 | 0/3 |
| transfer-pytorch | wine | catboost.CatBoostLFC | lowest | auc | 3 | -0.0131 | [-0.0228, +0.0030] | 0.247 | 1/3 |
| transfer-pytorch | wine | catboost.LOO | lowest | 5 % | 3 | +0.0023 | [-0.0120, +0.0107] | 0.777 | 2/3 |
| transfer-pytorch | wine | catboost.LOO | lowest | 10 % | 3 | -0.0048 | [-0.0086, +0.0019] | 0.286 | 1/3 |
| transfer-pytorch | wine | catboost.LOO | lowest | 20 % | 3 | +0.0027 | [-0.0009, +0.0099] | 0.527 | 1/3 |
| transfer-pytorch | wine | catboost.LOO | lowest | auc | 3 | -0.0006 | [-0.0061, +0.0058] | 0.888 | 1/3 |
| transfer-pytorch | wine | catboost.LossHigh | lowest | 5 % | 3 | -0.0245 | [-0.0313, -0.0160] | 0.032 | 0/3 |
| transfer-pytorch | wine | catboost.LossHigh | lowest | 10 % | 3 | +0.0074 | [-0.0073, +0.0225] | 0.478 | 2/3 |
| transfer-pytorch | wine | catboost.LossHigh | lowest | 20 % | 3 | -0.0093 | [-0.0142, -0.0048] | 0.077 | 0/3 |
| transfer-pytorch | wine | catboost.LossHigh | lowest | auc | 3 | -0.0057 | [-0.0129, -0.0016] | 0.258 | 0/3 |
| transfer-pytorch | wine | distill-lightgbm.Influence | lowest | 5 % | 3 | -0.0040 | [-0.0101, +0.0037] | 0.431 | 1/3 |
| transfer-pytorch | wine | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0005 | [-0.0053, +0.0115] | 0.930 | 1/3 |
| transfer-pytorch | wine | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0066 | [-0.0033, +0.0184] | 0.410 | 2/3 |
| transfer-pytorch | wine | distill-lightgbm.Influence | lowest | auc | 3 | +0.0009 | [-0.0042, +0.0038] | 0.769 | 2/3 |
| transfer-pytorch | wine | distill-lightgbm.LossHigh | lowest | 5 % | 3 | -0.0169 | [-0.0274, -0.0083] | 0.095 | 0/3 |
| transfer-pytorch | wine | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0035 | [-0.0057, +0.0153] | 0.630 | 2/3 |
| transfer-pytorch | wine | distill-lightgbm.LossHigh | lowest | 20 % | 3 | -0.0025 | [-0.0093, +0.0030] | 0.555 | 1/3 |
| transfer-pytorch | wine | distill-lightgbm.LossHigh | lowest | auc | 3 | -0.0035 | [-0.0051, -0.0015] | 0.082 | 0/3 |
| transfer-pytorch | wine | lightgbm.LOO | lowest | 5 % | 3 | -0.0053 | [-0.0176, +0.0034] | 0.495 | 1/3 |
| transfer-pytorch | wine | lightgbm.LOO | lowest | 10 % | 3 | -0.0007 | [-0.0067, +0.0043] | 0.841 | 2/3 |
| transfer-pytorch | wine | lightgbm.LOO | lowest | 20 % | 3 | +0.0044 | [+0.0033, +0.0066] | 0.056 | 3/3 |
| transfer-pytorch | wine | lightgbm.LOO | lowest | auc | 3 | -0.0005 | [-0.0061, +0.0026] | 0.881 | 2/3 |
| transfer-pytorch | wine | lightgbm.LossHigh | lowest | 5 % | 3 | -0.0073 | [-0.0097, -0.0052] | 0.031 | 0/3 |
| transfer-pytorch | wine | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0017 | [-0.0124, +0.0115] | 0.837 | 2/3 |
| transfer-pytorch | wine | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0037 | [-0.0017, +0.0067] | 0.305 | 2/3 |
| transfer-pytorch | wine | lightgbm.LossHigh | lowest | auc | 3 | -0.0003 | [-0.0075, +0.0041] | 0.947 | 2/3 |
| transfer-pytorch | wine | pytorch.Influence | lowest | 5 % | 3 | -0.0165 | [-0.0351, -0.0062] | 0.219 | 0/3 |
| transfer-pytorch | wine | pytorch.Influence | lowest | 10 % | 3 | -0.0069 | [-0.0405, +0.0192] | 0.734 | 2/3 |
| transfer-pytorch | wine | pytorch.Influence | lowest | 20 % | 3 | -0.0033 | [-0.0298, +0.0130] | 0.828 | 2/3 |
| transfer-pytorch | wine | pytorch.Influence | lowest | auc | 3 | -0.0075 | [-0.0314, +0.0089] | 0.600 | 1/3 |
| transfer-pytorch | wine | pytorch.LOO | lowest | 5 % | 3 | +0.0053 | [+0.0015, +0.0080] | 0.114 | 3/3 |
| transfer-pytorch | wine | pytorch.LOO | lowest | 10 % | 3 | +0.0115 | [+0.0035, +0.0221] | 0.174 | 3/3 |
| transfer-pytorch | wine | pytorch.LOO | lowest | 20 % | 3 | +0.0154 | [+0.0056, +0.0249] | 0.111 | 3/3 |
| transfer-pytorch | wine | pytorch.LOO | lowest | auc | 3 | +0.0095 | [+0.0051, +0.0138] | 0.064 | 3/3 |
| transfer-pytorch | wine | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0040 | [-0.0019, +0.0117] | 0.424 | 2/3 |
| transfer-pytorch | wine | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0028 | [-0.0166, +0.0237] | 0.833 | 2/3 |
| transfer-pytorch | wine | pytorch.LissaInfluence | lowest | 20 % | 3 | +0.0015 | [-0.0156, +0.0177] | 0.892 | 2/3 |
| transfer-pytorch | wine | pytorch.LissaInfluence | lowest | auc | 3 | +0.0024 | [-0.0106, +0.0162] | 0.785 | 2/3 |
| transfer-pytorch | wine | pytorch.LossHigh | lowest | 5 % | 3 | -0.0201 | [-0.0247, -0.0125] | 0.034 | 0/3 |
| transfer-pytorch | wine | pytorch.LossHigh | lowest | 10 % | 3 | +0.0063 | [-0.0082, +0.0163] | 0.486 | 2/3 |
| transfer-pytorch | wine | pytorch.LossHigh | lowest | 20 % | 3 | -0.0029 | [-0.0060, +0.0013] | 0.315 | 1/3 |
| transfer-pytorch | wine | pytorch.LossHigh | lowest | auc | 3 | -0.0034 | [-0.0072, -0.0014] | 0.216 | 0/3 |
| transfer-pytorch | wine | random_forest.LOO | lowest | 5 % | 3 | -0.0053 | [-0.0111, -0.0016] | 0.207 | 0/3 |
| transfer-pytorch | wine | random_forest.LOO | lowest | 10 % | 3 | +0.0033 | [-0.0078, +0.0172] | 0.694 | 2/3 |
| transfer-pytorch | wine | random_forest.LOO | lowest | 20 % | 3 | +0.0096 | [+0.0011, +0.0174] | 0.178 | 3/3 |
| transfer-pytorch | wine | random_forest.LOO | lowest | auc | 3 | +0.0023 | [-0.0054, +0.0104] | 0.663 | 2/3 |
| transfer-pytorch | wine | random_forest.LossHigh | lowest | 5 % | 3 | +0.0008 | [-0.0085, +0.0068] | 0.881 | 2/3 |
| transfer-pytorch | wine | random_forest.LossHigh | lowest | 10 % | 3 | -0.0005 | [-0.0057, +0.0093] | 0.924 | 1/3 |
| transfer-pytorch | wine | random_forest.LossHigh | lowest | 20 % | 3 | +0.0014 | [-0.0003, +0.0047] | 0.473 | 1/3 |
| transfer-pytorch | wine | random_forest.LossHigh | lowest | auc | 3 | +0.0004 | [-0.0042, +0.0045] | 0.900 | 2/3 |
| transfer-pytorch | wine | xgboost.LOO | lowest | 5 % | 3 | +0.0016 | [-0.0074, +0.0142] | 0.825 | 1/3 |
| transfer-pytorch | wine | xgboost.LOO | lowest | 10 % | 3 | +0.0081 | [-0.0064, +0.0309] | 0.554 | 1/3 |
| transfer-pytorch | wine | xgboost.LOO | lowest | 20 % | 3 | +0.0016 | [-0.0091, +0.0100] | 0.805 | 2/3 |
| transfer-pytorch | wine | xgboost.LOO | lowest | auc | 3 | +0.0039 | [-0.0065, +0.0161] | 0.619 | 2/3 |
| transfer-pytorch | wine | xgboost.LossHigh | lowest | 5 % | 3 | +0.0008 | [-0.0019, +0.0041] | 0.684 | 2/3 |
| transfer-pytorch | wine | xgboost.LossHigh | lowest | 10 % | 3 | +0.0064 | [+0.0035, +0.0111] | 0.112 | 3/3 |
| transfer-pytorch | wine | xgboost.LossHigh | lowest | 20 % | 3 | +0.0065 | [+0.0024, +0.0130] | 0.186 | 3/3 |
| transfer-pytorch | wine | xgboost.LossHigh | lowest | auc | 3 | +0.0042 | [+0.0030, +0.0052] | 0.024 | 3/3 |
| transfer-random_forest | adult | any.DataOOB | lowest | 5 % | 3 | -0.0005 | [-0.0010, +0.0000] | 0.268 | 0/3 |
| transfer-random_forest | adult | any.DataOOB | lowest | 10 % | 3 | -0.0051 | [-0.0094, -0.0019] | 0.152 | 0/3 |
| transfer-random_forest | adult | any.DataOOB | lowest | 20 % | 3 | -0.0050 | [-0.0085, -0.0022] | 0.119 | 0/3 |
| transfer-random_forest | adult | any.DataOOB | lowest | auc | 3 | -0.0033 | [-0.0058, -0.0020] | 0.120 | 0/3 |
| transfer-random_forest | adult | any.KNNShapley | lowest | 5 % | 3 | -0.0020 | [-0.0036, -0.0004] | 0.156 | 0/3 |
| transfer-random_forest | adult | any.KNNShapley | lowest | 10 % | 3 | -0.0013 | [-0.0093, +0.0090] | 0.835 | 1/3 |
| transfer-random_forest | adult | any.KNNShapley | lowest | 20 % | 3 | -0.0132 | [-0.0166, -0.0069] | 0.053 | 0/3 |
| transfer-random_forest | adult | any.KNNShapley | lowest | auc | 3 | -0.0043 | [-0.0081, +0.0016] | 0.285 | 1/3 |
| transfer-random_forest | adult | catboost.CatBoostLFC | lowest | 5 % | 3 | +0.0044 | [-0.0017, +0.0119] | 0.388 | 2/3 |
| transfer-random_forest | adult | catboost.CatBoostLFC | lowest | 10 % | 3 | -0.0006 | [-0.0125, +0.0143] | 0.947 | 1/3 |
| transfer-random_forest | adult | catboost.CatBoostLFC | lowest | 20 % | 3 | +0.0072 | [-0.0074, +0.0265] | 0.547 | 2/3 |
| transfer-random_forest | adult | catboost.CatBoostLFC | lowest | auc | 3 | +0.0027 | [-0.0045, +0.0149] | 0.707 | 1/3 |
| transfer-random_forest | adult | catboost.LOO | lowest | 5 % | 3 | -0.0040 | [-0.0078, -0.0019] | 0.173 | 0/3 |
| transfer-random_forest | adult | catboost.LOO | lowest | 10 % | 3 | -0.0011 | [-0.0164, +0.0168] | 0.918 | 1/3 |
| transfer-random_forest | adult | catboost.LOO | lowest | 20 % | 3 | -0.0026 | [-0.0030, -0.0019] | 0.021 | 0/3 |
| transfer-random_forest | adult | catboost.LOO | lowest | auc | 3 | -0.0021 | [-0.0086, +0.0051] | 0.653 | 1/3 |
| transfer-random_forest | adult | catboost.LossHigh | lowest | 5 % | 3 | -0.0002 | [-0.0029, +0.0026] | 0.903 | 1/3 |
| transfer-random_forest | adult | catboost.LossHigh | lowest | 10 % | 3 | -0.0111 | [-0.0191, -0.0022] | 0.152 | 0/3 |
| transfer-random_forest | adult | catboost.LossHigh | lowest | 20 % | 3 | -0.0139 | [-0.0183, -0.0089] | 0.036 | 0/3 |
| transfer-random_forest | adult | catboost.LossHigh | lowest | auc | 3 | -0.0077 | [-0.0115, -0.0024] | 0.106 | 0/3 |
| transfer-random_forest | adult | distill-lightgbm.Influence | lowest | 5 % | 3 | +0.0040 | [-0.0036, +0.0090] | 0.407 | 2/3 |
| transfer-random_forest | adult | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0007 | [-0.0064, +0.0099] | 0.901 | 1/3 |
| transfer-random_forest | adult | distill-lightgbm.Influence | lowest | 20 % | 3 | -0.0005 | [-0.0044, +0.0053] | 0.872 | 1/3 |
| transfer-random_forest | adult | distill-lightgbm.Influence | lowest | auc | 3 | +0.0011 | [-0.0026, +0.0048] | 0.649 | 2/3 |
| transfer-random_forest | adult | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0047 | [+0.0004, +0.0071] | 0.163 | 3/3 |
| transfer-random_forest | adult | distill-lightgbm.LossHigh | lowest | 10 % | 3 | -0.0069 | [-0.0141, -0.0027] | 0.196 | 0/3 |
| transfer-random_forest | adult | distill-lightgbm.LossHigh | lowest | 20 % | 3 | -0.0143 | [-0.0167, -0.0116] | 0.011 | 0/3 |
| transfer-random_forest | adult | distill-lightgbm.LossHigh | lowest | auc | 3 | -0.0050 | [-0.0077, -0.0035] | 0.066 | 0/3 |
| transfer-random_forest | adult | lightgbm.LOO | lowest | 5 % | 3 | -0.0015 | [-0.0086, +0.0066] | 0.762 | 1/3 |
| transfer-random_forest | adult | lightgbm.LOO | lowest | 10 % | 3 | -0.0011 | [-0.0111, +0.0069] | 0.860 | 2/3 |
| transfer-random_forest | adult | lightgbm.LOO | lowest | 20 % | 3 | -0.0034 | [-0.0110, +0.0040] | 0.515 | 1/3 |
| transfer-random_forest | adult | lightgbm.LOO | lowest | auc | 3 | -0.0016 | [-0.0056, +0.0052] | 0.682 | 1/3 |
| transfer-random_forest | adult | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0004 | [-0.0032, +0.0052] | 0.879 | 1/3 |
| transfer-random_forest | adult | lightgbm.LossHigh | lowest | 10 % | 3 | -0.0061 | [-0.0133, -0.0021] | 0.232 | 0/3 |
| transfer-random_forest | adult | lightgbm.LossHigh | lowest | 20 % | 3 | -0.0034 | [-0.0049, -0.0008] | 0.122 | 0/3 |
| transfer-random_forest | adult | lightgbm.LossHigh | lowest | auc | 3 | -0.0030 | [-0.0054, -0.0009] | 0.144 | 0/3 |
| transfer-random_forest | adult | pytorch.Influence | lowest | 5 % | 3 | +0.0011 | [-0.0039, +0.0054] | 0.720 | 2/3 |
| transfer-random_forest | adult | pytorch.Influence | lowest | 10 % | 3 | +0.0015 | [-0.0088, +0.0084] | 0.806 | 2/3 |
| transfer-random_forest | adult | pytorch.Influence | lowest | 20 % | 3 | -0.0002 | [-0.0068, +0.0070] | 0.967 | 1/3 |
| transfer-random_forest | adult | pytorch.Influence | lowest | auc | 3 | +0.0008 | [-0.0060, +0.0054] | 0.842 | 2/3 |
| transfer-random_forest | adult | pytorch.LOO | lowest | 5 % | 3 | +0.0006 | [-0.0004, +0.0018] | 0.456 | 2/3 |
| transfer-random_forest | adult | pytorch.LOO | lowest | 10 % | 3 | +0.0004 | [-0.0071, +0.0046] | 0.930 | 2/3 |
| transfer-random_forest | adult | pytorch.LOO | lowest | 20 % | 3 | +0.0035 | [+0.0008, +0.0049] | 0.120 | 3/3 |
| transfer-random_forest | adult | pytorch.LOO | lowest | auc | 3 | +0.0012 | [-0.0014, +0.0030] | 0.476 | 2/3 |
| transfer-random_forest | adult | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0015 | [-0.0035, +0.0080] | 0.696 | 2/3 |
| transfer-random_forest | adult | pytorch.LissaInfluence | lowest | 10 % | 3 | -0.0074 | [-0.0244, +0.0032] | 0.478 | 1/3 |
| transfer-random_forest | adult | pytorch.LissaInfluence | lowest | 20 % | 3 | -0.0066 | [-0.0082, -0.0041] | 0.034 | 0/3 |
| transfer-random_forest | adult | pytorch.LissaInfluence | lowest | auc | 3 | -0.0040 | [-0.0119, +0.0002] | 0.410 | 1/3 |
| transfer-random_forest | adult | pytorch.LossHigh | lowest | 5 % | 3 | +0.0012 | [-0.0039, +0.0051] | 0.691 | 2/3 |
| transfer-random_forest | adult | pytorch.LossHigh | lowest | 10 % | 3 | -0.0072 | [-0.0165, -0.0021] | 0.260 | 0/3 |
| transfer-random_forest | adult | pytorch.LossHigh | lowest | 20 % | 3 | -0.0175 | [-0.0213, -0.0126] | 0.021 | 0/3 |
| transfer-random_forest | adult | pytorch.LossHigh | lowest | auc | 3 | -0.0068 | [-0.0102, -0.0049] | 0.059 | 0/3 |
| transfer-random_forest | adult | random_forest.LOO | lowest | 5 % | 3 | -0.0010 | [-0.0073, +0.0039] | 0.791 | 2/3 |
| transfer-random_forest | adult | random_forest.LOO | lowest | 10 % | 3 | -0.0036 | [-0.0113, +0.0098] | 0.648 | 1/3 |
| transfer-random_forest | adult | random_forest.LOO | lowest | 20 % | 3 | -0.0004 | [-0.0090, +0.0067] | 0.931 | 2/3 |
| transfer-random_forest | adult | random_forest.LOO | lowest | auc | 3 | -0.0017 | [-0.0056, +0.0049] | 0.659 | 1/3 |
| transfer-random_forest | adult | random_forest.LossHigh | lowest | 5 % | 3 | -0.0028 | [-0.0062, +0.0000] | 0.267 | 0/3 |
| transfer-random_forest | adult | random_forest.LossHigh | lowest | 10 % | 3 | -0.0115 | [-0.0214, -0.0025] | 0.170 | 0/3 |
| transfer-random_forest | adult | random_forest.LossHigh | lowest | 20 % | 3 | -0.0163 | [-0.0245, -0.0074] | 0.081 | 0/3 |
| transfer-random_forest | adult | random_forest.LossHigh | lowest | auc | 3 | -0.0091 | [-0.0128, -0.0028] | 0.102 | 0/3 |
| transfer-random_forest | adult | xgboost.LOO | lowest | 5 % | 3 | -0.0014 | [-0.0091, +0.0060] | 0.779 | 1/3 |
| transfer-random_forest | adult | xgboost.LOO | lowest | 10 % | 3 | -0.0065 | [-0.0206, +0.0067] | 0.499 | 1/3 |
| transfer-random_forest | adult | xgboost.LOO | lowest | 20 % | 3 | -0.0022 | [-0.0082, +0.0028] | 0.566 | 1/3 |
| transfer-random_forest | adult | xgboost.LOO | lowest | auc | 3 | -0.0033 | [-0.0093, +0.0002] | 0.385 | 1/3 |
| transfer-random_forest | adult | xgboost.LossHigh | lowest | 5 % | 3 | -0.0024 | [-0.0087, +0.0018] | 0.525 | 1/3 |
| transfer-random_forest | adult | xgboost.LossHigh | lowest | 10 % | 3 | -0.0026 | [-0.0094, +0.0048] | 0.591 | 1/3 |
| transfer-random_forest | adult | xgboost.LossHigh | lowest | 20 % | 3 | -0.0048 | [-0.0108, -0.0002] | 0.268 | 0/3 |
| transfer-random_forest | adult | xgboost.LossHigh | lowest | auc | 3 | -0.0028 | [-0.0065, -0.0008] | 0.277 | 0/3 |
| transfer-random_forest | covertype | any.DataOOB | lowest | 5 % | 3 | +0.0021 | [-0.0042, +0.0084] | 0.627 | 2/3 |
| transfer-random_forest | covertype | any.DataOOB | lowest | 10 % | 3 | +0.0059 | [+0.0026, +0.0088] | 0.082 | 3/3 |
| transfer-random_forest | covertype | any.DataOOB | lowest | 20 % | 3 | +0.0116 | [+0.0038, +0.0200] | 0.132 | 3/3 |
| transfer-random_forest | covertype | any.DataOOB | lowest | auc | 3 | +0.0056 | [+0.0027, +0.0088] | 0.087 | 3/3 |
| transfer-random_forest | covertype | any.KNNShapley | lowest | 5 % | 3 | -0.0014 | [-0.0072, +0.0026] | 0.684 | 2/3 |
| transfer-random_forest | covertype | any.KNNShapley | lowest | 10 % | 3 | +0.0035 | [-0.0060, +0.0082] | 0.540 | 2/3 |
| transfer-random_forest | covertype | any.KNNShapley | lowest | 20 % | 3 | -0.0015 | [-0.0162, +0.0064] | 0.854 | 2/3 |
| transfer-random_forest | covertype | any.KNNShapley | lowest | auc | 3 | +0.0006 | [-0.0081, +0.0053] | 0.908 | 2/3 |
| transfer-random_forest | covertype | catboost.LOO | lowest | 5 % | 3 | -0.0042 | [-0.0088, -0.0004] | 0.230 | 0/3 |
| transfer-random_forest | covertype | catboost.LOO | lowest | 10 % | 3 | +0.0047 | [+0.0012, +0.0096] | 0.201 | 3/3 |
| transfer-random_forest | covertype | catboost.LOO | lowest | 20 % | 3 | +0.0066 | [-0.0066, +0.0198] | 0.478 | 2/3 |
| transfer-random_forest | covertype | catboost.LOO | lowest | auc | 3 | +0.0024 | [-0.0034, +0.0077] | 0.537 | 2/3 |
| transfer-random_forest | covertype | catboost.LossHigh | lowest | 5 % | 3 | -0.0005 | [-0.0038, +0.0048] | 0.877 | 1/3 |
| transfer-random_forest | covertype | catboost.LossHigh | lowest | 10 % | 3 | +0.0059 | [+0.0036, +0.0072] | 0.037 | 3/3 |
| transfer-random_forest | covertype | catboost.LossHigh | lowest | 20 % | 3 | +0.0106 | [+0.0014, +0.0188] | 0.171 | 3/3 |
| transfer-random_forest | covertype | catboost.LossHigh | lowest | auc | 3 | +0.0048 | [+0.0011, +0.0067] | 0.122 | 3/3 |
| transfer-random_forest | covertype | distill-lightgbm.Influence | lowest | 5 % | 3 | -0.0035 | [-0.0082, -0.0006] | 0.273 | 0/3 |
| transfer-random_forest | covertype | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0044 | [+0.0024, +0.0078] | 0.123 | 3/3 |
| transfer-random_forest | covertype | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0088 | [+0.0038, +0.0130] | 0.082 | 3/3 |
| transfer-random_forest | covertype | distill-lightgbm.Influence | lowest | auc | 3 | +0.0030 | [+0.0019, +0.0041] | 0.043 | 3/3 |
| transfer-random_forest | covertype | distill-lightgbm.LossHigh | lowest | 5 % | 3 | -0.0002 | [-0.0032, +0.0042] | 0.937 | 1/3 |
| transfer-random_forest | covertype | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0056 | [+0.0008, +0.0138] | 0.307 | 3/3 |
| transfer-random_forest | covertype | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0124 | [+0.0068, +0.0174] | 0.056 | 3/3 |
| transfer-random_forest | covertype | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0051 | [+0.0012, +0.0091] | 0.153 | 3/3 |
| transfer-random_forest | covertype | lightgbm.LOO | lowest | 5 % | 3 | -0.0044 | [-0.0100, -0.0012] | 0.258 | 0/3 |
| transfer-random_forest | covertype | lightgbm.LOO | lowest | 10 % | 3 | +0.0049 | [-0.0018, +0.0144] | 0.425 | 2/3 |
| transfer-random_forest | covertype | lightgbm.LOO | lowest | 20 % | 3 | +0.0071 | [-0.0016, +0.0178] | 0.340 | 2/3 |
| transfer-random_forest | covertype | lightgbm.LOO | lowest | auc | 3 | +0.0025 | [-0.0036, +0.0096] | 0.581 | 2/3 |
| transfer-random_forest | covertype | lightgbm.LossHigh | lowest | 5 % | 3 | -0.0013 | [-0.0050, +0.0032] | 0.635 | 1/3 |
| transfer-random_forest | covertype | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0074 | [+0.0028, +0.0108] | 0.090 | 3/3 |
| transfer-random_forest | covertype | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0082 | [+0.0038, +0.0166] | 0.190 | 3/3 |
| transfer-random_forest | covertype | lightgbm.LossHigh | lowest | auc | 3 | +0.0045 | [+0.0008, +0.0076] | 0.155 | 3/3 |
| transfer-random_forest | covertype | pytorch.Influence | lowest | 5 % | 3 | -0.0009 | [-0.0024, +0.0000] | 0.336 | 0/3 |
| transfer-random_forest | covertype | pytorch.Influence | lowest | 10 % | 3 | +0.0038 | [-0.0026, +0.0098] | 0.400 | 2/3 |
| transfer-random_forest | covertype | pytorch.Influence | lowest | 20 % | 3 | +0.0063 | [-0.0012, +0.0194] | 0.436 | 2/3 |
| transfer-random_forest | covertype | pytorch.Influence | lowest | auc | 3 | +0.0028 | [-0.0019, +0.0085] | 0.459 | 2/3 |
| transfer-random_forest | covertype | pytorch.LOO | lowest | 5 % | 3 | -0.0034 | [-0.0082, +0.0026] | 0.396 | 1/3 |
| transfer-random_forest | covertype | pytorch.LOO | lowest | 10 % | 3 | +0.0040 | [-0.0006, +0.0106] | 0.359 | 2/3 |
| transfer-random_forest | covertype | pytorch.LOO | lowest | 20 % | 3 | +0.0067 | [+0.0038, +0.0126] | 0.149 | 3/3 |
| transfer-random_forest | covertype | pytorch.LOO | lowest | auc | 3 | +0.0023 | [-0.0004, +0.0051] | 0.279 | 2/3 |
| transfer-random_forest | covertype | pytorch.LissaInfluence | lowest | 5 % | 3 | -0.0066 | [-0.0138, +0.0022] | 0.294 | 1/3 |
| transfer-random_forest | covertype | pytorch.LissaInfluence | lowest | 10 % | 3 | -0.0061 | [-0.0192, +0.0020] | 0.456 | 1/3 |
| transfer-random_forest | covertype | pytorch.LissaInfluence | lowest | 20 % | 3 | -0.0136 | [-0.0330, +0.0000] | 0.305 | 0/3 |
| transfer-random_forest | covertype | pytorch.LissaInfluence | lowest | auc | 3 | -0.0073 | [-0.0189, +0.0013] | 0.347 | 1/3 |
| transfer-random_forest | covertype | pytorch.LossHigh | lowest | 5 % | 3 | +0.0032 | [-0.0018, +0.0080] | 0.376 | 2/3 |
| transfer-random_forest | covertype | pytorch.LossHigh | lowest | 10 % | 3 | +0.0074 | [+0.0016, +0.0158] | 0.227 | 3/3 |
| transfer-random_forest | covertype | pytorch.LossHigh | lowest | 20 % | 3 | +0.0093 | [+0.0024, +0.0136] | 0.116 | 3/3 |
| transfer-random_forest | covertype | pytorch.LossHigh | lowest | auc | 3 | +0.0059 | [+0.0021, +0.0089] | 0.100 | 3/3 |
| transfer-random_forest | covertype | random_forest.LOO | lowest | 5 % | 3 | -0.0043 | [-0.0052, -0.0034] | 0.015 | 0/3 |
| transfer-random_forest | covertype | random_forest.LOO | lowest | 10 % | 3 | +0.0028 | [+0.0000, +0.0082] | 0.409 | 2/3 |
| transfer-random_forest | covertype | random_forest.LOO | lowest | 20 % | 3 | +0.0101 | [+0.0032, +0.0214] | 0.220 | 3/3 |
| transfer-random_forest | covertype | random_forest.LOO | lowest | auc | 3 | +0.0025 | [-0.0005, +0.0074] | 0.416 | 2/3 |
| transfer-random_forest | covertype | random_forest.LossHigh | lowest | 5 % | 3 | -0.0011 | [-0.0080, +0.0060] | 0.817 | 1/3 |
| transfer-random_forest | covertype | random_forest.LossHigh | lowest | 10 % | 3 | +0.0073 | [+0.0042, +0.0104] | 0.055 | 3/3 |
| transfer-random_forest | covertype | random_forest.LossHigh | lowest | 20 % | 3 | +0.0069 | [+0.0026, +0.0094] | 0.086 | 3/3 |
| transfer-random_forest | covertype | random_forest.LossHigh | lowest | auc | 3 | +0.0042 | [+0.0031, +0.0053] | 0.021 | 3/3 |
| transfer-random_forest | covertype | xgboost.LOO | lowest | 5 % | 3 | -0.0023 | [-0.0034, -0.0012] | 0.070 | 0/3 |
| transfer-random_forest | covertype | xgboost.LOO | lowest | 10 % | 3 | +0.0025 | [-0.0012, +0.0050] | 0.314 | 2/3 |
| transfer-random_forest | covertype | xgboost.LOO | lowest | 20 % | 3 | +0.0035 | [-0.0042, +0.0126] | 0.553 | 2/3 |
| transfer-random_forest | covertype | xgboost.LOO | lowest | auc | 3 | +0.0012 | [-0.0020, +0.0043] | 0.565 | 2/3 |
| transfer-random_forest | covertype | xgboost.LossHigh | lowest | 5 % | 3 | -0.0013 | [-0.0082, +0.0070] | 0.802 | 1/3 |
| transfer-random_forest | covertype | xgboost.LossHigh | lowest | 10 % | 3 | +0.0050 | [+0.0034, +0.0078] | 0.071 | 3/3 |
| transfer-random_forest | covertype | xgboost.LossHigh | lowest | 20 % | 3 | +0.0078 | [-0.0002, +0.0132] | 0.196 | 2/3 |
| transfer-random_forest | covertype | xgboost.LossHigh | lowest | auc | 3 | +0.0035 | [-0.0007, +0.0073] | 0.267 | 2/3 |
| transfer-random_forest | housing | any.DataOOB | lowest | 5 % | 3 | +1258.1091 | [+724.3347, +1981.0687] | 0.078 | 3/3 |
| transfer-random_forest | housing | any.DataOOB | lowest | 10 % | 3 | +6252.7464 | [+5199.7431, +6819.9581] | 0.007 | 3/3 |
| transfer-random_forest | housing | any.DataOOB | lowest | 20 % | 3 | +6681.5103 | [+4686.1439, +8041.1264] | 0.022 | 3/3 |
| transfer-random_forest | housing | any.DataOOB | lowest | auc | 3 | +4329.6848 | [+3388.6706, +4882.0666] | 0.012 | 3/3 |
| transfer-random_forest | housing | catboost.CatBoostLFC | lowest | 5 % | 3 | -1508.9156 | [-2186.6458, -566.1114] | 0.090 | 0/3 |
| transfer-random_forest | housing | catboost.CatBoostLFC | lowest | 10 % | 3 | -3284.6931 | [-3698.7574, -3004.9084] | 0.004 | 0/3 |
| transfer-random_forest | housing | catboost.CatBoostLFC | lowest | 20 % | 3 | -7553.0956 | [-7776.1750, -7159.4979] | 0.001 | 0/3 |
| transfer-random_forest | housing | catboost.CatBoostLFC | lowest | auc | 3 | -3497.2627 | [-3864.5990, -3212.4123] | 0.003 | 0/3 |
| transfer-random_forest | housing | catboost.LOO | lowest | 5 % | 3 | +632.0207 | [+223.5567, +843.4429] | 0.091 | 3/3 |
| transfer-random_forest | housing | catboost.LOO | lowest | 10 % | 3 | +465.5618 | [-582.1713, +1030.8913] | 0.468 | 2/3 |
| transfer-random_forest | housing | catboost.LOO | lowest | 20 % | 3 | +334.9259 | [-753.6353, +1607.9899] | 0.674 | 2/3 |
| transfer-random_forest | housing | catboost.LOO | lowest | auc | 3 | +416.3223 | [-350.8339, +999.4424] | 0.408 | 2/3 |
| transfer-random_forest | housing | catboost.LossHigh | lowest | 5 % | 3 | +1618.5035 | [+1093.3555, +2305.1020] | 0.046 | 3/3 |
| transfer-random_forest | housing | catboost.LossHigh | lowest | 10 % | 3 | +5599.6565 | [+4477.8552, +6645.9755] | 0.012 | 3/3 |
| transfer-random_forest | housing | catboost.LossHigh | lowest | 20 % | 3 | +5137.5520 | [+4331.8973, +6230.8837] | 0.012 | 3/3 |
| transfer-random_forest | housing | catboost.LossHigh | lowest | auc | 3 | +3788.8851 | [+3126.4333, +4626.2372] | 0.013 | 3/3 |
| transfer-random_forest | housing | distill-lightgbm.Influence | lowest | 5 % | 3 | +1854.8799 | [+417.3374, +3240.0891] | 0.151 | 3/3 |
| transfer-random_forest | housing | distill-lightgbm.Influence | lowest | 10 % | 3 | +1441.4692 | [+693.9962, +2224.5588] | 0.083 | 3/3 |
| transfer-random_forest | housing | distill-lightgbm.Influence | lowest | 20 % | 3 | +446.8987 | [-181.5997, +1033.9997] | 0.331 | 2/3 |
| transfer-random_forest | housing | distill-lightgbm.Influence | lowest | auc | 3 | +1115.9956 | [+319.1830, +1595.7169] | 0.109 | 3/3 |
| transfer-random_forest | housing | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +980.2871 | [+98.2779, +1803.1176] | 0.185 | 3/3 |
| transfer-random_forest | housing | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +6035.2550 | [+5400.7307, +6420.2142] | 0.003 | 3/3 |
| transfer-random_forest | housing | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +5766.7928 | [+4412.5229, +7211.0422] | 0.019 | 3/3 |
| transfer-random_forest | housing | distill-lightgbm.LossHigh | lowest | auc | 3 | +3949.9906 | [+3152.9742, +4419.4346] | 0.010 | 3/3 |
| transfer-random_forest | housing | lightgbm.LOO | lowest | 5 % | 3 | +887.6045 | [+24.4995, +1868.0743] | 0.239 | 3/3 |
| transfer-random_forest | housing | lightgbm.LOO | lowest | 10 % | 3 | +1007.0455 | [+593.4883, +1614.1111] | 0.083 | 3/3 |
| transfer-random_forest | housing | lightgbm.LOO | lowest | 20 % | 3 | +1018.8749 | [+714.9098, +1503.6596] | 0.053 | 3/3 |
| transfer-random_forest | housing | lightgbm.LOO | lowest | auc | 3 | +854.2619 | [+520.7152, +1448.2251] | 0.103 | 3/3 |
| transfer-random_forest | housing | lightgbm.LossHigh | lowest | 5 % | 3 | +1894.5830 | [+1385.9308, +2364.4737] | 0.022 | 3/3 |
| transfer-random_forest | housing | lightgbm.LossHigh | lowest | 10 % | 3 | +5840.4468 | [+5476.4573, +6382.5322] | 0.002 | 3/3 |
| transfer-random_forest | housing | lightgbm.LossHigh | lowest | 20 % | 3 | +6249.1340 | [+5114.7570, +7537.0922] | 0.012 | 3/3 |
| transfer-random_forest | housing | lightgbm.LossHigh | lowest | auc | 3 | +4226.0968 | [+3923.4792, +4400.6739] | 0.001 | 3/3 |
| transfer-random_forest | housing | pytorch.Influence | lowest | 5 % | 3 | +1872.9946 | [+1258.3399, +2602.9151] | 0.041 | 3/3 |
| transfer-random_forest | housing | pytorch.Influence | lowest | 10 % | 3 | +2009.1080 | [+1680.1093, +2659.7287] | 0.025 | 3/3 |
| transfer-random_forest | housing | pytorch.Influence | lowest | 20 % | 3 | +1868.8591 | [+537.8662, +3291.2525] | 0.143 | 3/3 |
| transfer-random_forest | housing | pytorch.Influence | lowest | auc | 3 | +1688.8789 | [+1203.9397, +2134.7964] | 0.025 | 3/3 |
| transfer-random_forest | housing | pytorch.LOO | lowest | 5 % | 3 | +191.8902 | [-104.2457, +450.8557] | 0.356 | 2/3 |
| transfer-random_forest | housing | pytorch.LOO | lowest | 10 % | 3 | -232.1552 | [-733.7572, +586.7361] | 0.631 | 1/3 |
| transfer-random_forest | housing | pytorch.LOO | lowest | 20 % | 3 | +836.7525 | [+516.3771, +1036.1942] | 0.035 | 3/3 |
| transfer-random_forest | housing | pytorch.LOO | lowest | auc | 3 | +170.1025 | [-61.7988, +406.3854] | 0.335 | 2/3 |
| transfer-random_forest | housing | pytorch.LissaInfluence | lowest | 5 % | 3 | +260.8680 | [-1338.5978, +3221.5979] | 0.876 | 1/3 |
| transfer-random_forest | housing | pytorch.LissaInfluence | lowest | 10 % | 3 | -1767.7115 | [-3451.3046, +1336.5822] | 0.373 | 1/3 |
| transfer-random_forest | housing | pytorch.LissaInfluence | lowest | 20 % | 3 | -6927.8945 | [-10072.0875, -1982.4552] | 0.110 | 0/3 |
| transfer-random_forest | housing | pytorch.LissaInfluence | lowest | auc | 3 | -2329.6484 | [-3988.7754, +811.0040] | 0.276 | 1/3 |
| transfer-random_forest | housing | pytorch.LossHigh | lowest | 5 % | 3 | +1393.4473 | [+456.2455, +2148.7171] | 0.107 | 3/3 |
| transfer-random_forest | housing | pytorch.LossHigh | lowest | 10 % | 3 | +5848.2134 | [+5263.2643, +6399.6176] | 0.003 | 3/3 |
| transfer-random_forest | housing | pytorch.LossHigh | lowest | 20 % | 3 | +5899.6401 | [+4345.9105, +7123.1014] | 0.019 | 3/3 |
| transfer-random_forest | housing | pytorch.LossHigh | lowest | auc | 3 | +4016.3519 | [+3174.2631, +4523.6141] | 0.011 | 3/3 |
| transfer-random_forest | housing | random_forest.LOO | lowest | 5 % | 3 | +1361.3380 | [+778.5380, +2133.3118] | 0.077 | 3/3 |
| transfer-random_forest | housing | random_forest.LOO | lowest | 10 % | 3 | +573.5562 | [+254.9021, +1199.2199] | 0.208 | 3/3 |
| transfer-random_forest | housing | random_forest.LOO | lowest | 20 % | 3 | +1248.7082 | [+309.8583, +2197.1147] | 0.149 | 3/3 |
| transfer-random_forest | housing | random_forest.LOO | lowest | auc | 3 | +867.5951 | [+466.0939, +1292.8234] | 0.068 | 3/3 |
| transfer-random_forest | housing | random_forest.LossHigh | lowest | 5 % | 3 | +843.0887 | [+239.6066, +1702.5913] | 0.196 | 3/3 |
| transfer-random_forest | housing | random_forest.LossHigh | lowest | 10 % | 3 | +5707.4811 | [+4287.0395, +7136.0675] | 0.020 | 3/3 |
| transfer-random_forest | housing | random_forest.LossHigh | lowest | 20 % | 3 | +5974.2763 | [+4404.6851, +7071.2955] | 0.018 | 3/3 |
| transfer-random_forest | housing | random_forest.LossHigh | lowest | auc | 3 | +3844.6467 | [+2855.5782, +4713.3852] | 0.019 | 3/3 |
| transfer-random_forest | housing | xgboost.LOO | lowest | 5 % | 3 | +556.6236 | [+1.7316, +1170.7898] | 0.242 | 3/3 |
| transfer-random_forest | housing | xgboost.LOO | lowest | 10 % | 3 | -165.1728 | [-1021.0779, +706.6928] | 0.772 | 1/3 |
| transfer-random_forest | housing | xgboost.LOO | lowest | 20 % | 3 | -149.7704 | [-1312.3187, +1275.2693] | 0.862 | 1/3 |
| transfer-random_forest | housing | xgboost.LOO | lowest | auc | 3 | +39.7735 | [-485.5367, +708.1644] | 0.920 | 1/3 |
| transfer-random_forest | housing | xgboost.LossHigh | lowest | 5 % | 3 | +1888.8570 | [+1530.9046, +2572.9376] | 0.031 | 3/3 |
| transfer-random_forest | housing | xgboost.LossHigh | lowest | 10 % | 3 | +1937.9268 | [+733.1067, +3049.0905] | 0.102 | 3/3 |
| transfer-random_forest | housing | xgboost.LossHigh | lowest | 20 % | 3 | +2773.6666 | [+1745.0776, +3314.0414] | 0.033 | 3/3 |
| transfer-random_forest | housing | xgboost.LossHigh | lowest | auc | 3 | +1892.3535 | [+1101.8666, +2602.1136] | 0.049 | 3/3 |
| transfer-random_forest | wine | any.DataOOB | lowest | 5 % | 3 | +0.0172 | [-0.0138, +0.0388] | 0.393 | 2/3 |
| transfer-random_forest | wine | any.DataOOB | lowest | 10 % | 3 | +0.0445 | [-0.0000, +0.0863] | 0.217 | 2/3 |
| transfer-random_forest | wine | any.DataOOB | lowest | 20 % | 3 | +0.0396 | [+0.0131, +0.0564] | 0.098 | 3/3 |
| transfer-random_forest | wine | any.DataOOB | lowest | auc | 3 | +0.0308 | [+0.0099, +0.0544] | 0.139 | 3/3 |
| transfer-random_forest | wine | catboost.CatBoostLFC | lowest | 5 % | 3 | +0.0027 | [-0.0152, +0.0154] | 0.797 | 2/3 |
| transfer-random_forest | wine | catboost.CatBoostLFC | lowest | 10 % | 3 | -0.0108 | [-0.0416, +0.0114] | 0.568 | 1/3 |
| transfer-random_forest | wine | catboost.CatBoostLFC | lowest | 20 % | 3 | -0.0391 | [-0.0615, -0.0126] | 0.111 | 0/3 |
| transfer-random_forest | wine | catboost.CatBoostLFC | lowest | auc | 3 | -0.0132 | [-0.0226, -0.0078] | 0.109 | 0/3 |
| transfer-random_forest | wine | catboost.LOO | lowest | 5 % | 3 | -0.0024 | [-0.0296, +0.0177] | 0.879 | 2/3 |
| transfer-random_forest | wine | catboost.LOO | lowest | 10 % | 3 | -0.0111 | [-0.0514, +0.0254] | 0.669 | 1/3 |
| transfer-random_forest | wine | catboost.LOO | lowest | 20 % | 3 | -0.0100 | [-0.0325, +0.0289] | 0.660 | 1/3 |
| transfer-random_forest | wine | catboost.LOO | lowest | auc | 3 | -0.0072 | [-0.0263, +0.0212] | 0.667 | 1/3 |
| transfer-random_forest | wine | catboost.LossHigh | lowest | 5 % | 3 | +0.0027 | [-0.0299, +0.0307] | 0.894 | 2/3 |
| transfer-random_forest | wine | catboost.LossHigh | lowest | 10 % | 3 | +0.0392 | [+0.0167, +0.0686] | 0.125 | 3/3 |
| transfer-random_forest | wine | catboost.LossHigh | lowest | 20 % | 3 | +0.0225 | [-0.0065, +0.0494] | 0.299 | 2/3 |
| transfer-random_forest | wine | catboost.LossHigh | lowest | auc | 3 | +0.0210 | [+0.0107, +0.0399] | 0.157 | 3/3 |
| transfer-random_forest | wine | distill-lightgbm.Influence | lowest | 5 % | 3 | +0.0119 | [-0.0064, +0.0290] | 0.366 | 2/3 |
| transfer-random_forest | wine | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0024 | [-0.0255, +0.0397] | 0.912 | 1/3 |
| transfer-random_forest | wine | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0023 | [+0.0010, +0.0039] | 0.110 | 3/3 |
| transfer-random_forest | wine | distill-lightgbm.Influence | lowest | auc | 3 | +0.0045 | [-0.0040, +0.0191] | 0.606 | 1/3 |
| transfer-random_forest | wine | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0114 | [-0.0132, +0.0310] | 0.474 | 2/3 |
| transfer-random_forest | wine | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0426 | [-0.0014, +0.0798] | 0.214 | 2/3 |
| transfer-random_forest | wine | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0309 | [-0.0075, +0.0534] | 0.250 | 2/3 |
| transfer-random_forest | wine | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0265 | [+0.0054, +0.0473] | 0.160 | 3/3 |
| transfer-random_forest | wine | lightgbm.LOO | lowest | 5 % | 3 | -0.0017 | [-0.0407, +0.0192] | 0.940 | 2/3 |
| transfer-random_forest | wine | lightgbm.LOO | lowest | 10 % | 3 | +0.0159 | [+0.0046, +0.0353] | 0.244 | 3/3 |
| transfer-random_forest | wine | lightgbm.LOO | lowest | 20 % | 3 | +0.0095 | [+0.0005, +0.0189] | 0.215 | 3/3 |
| transfer-random_forest | wine | lightgbm.LOO | lowest | auc | 3 | +0.0079 | [-0.0050, +0.0182] | 0.365 | 2/3 |
| transfer-random_forest | wine | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0205 | [-0.0161, +0.0421] | 0.381 | 2/3 |
| transfer-random_forest | wine | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0335 | [-0.0003, +0.0757] | 0.272 | 2/3 |
| transfer-random_forest | wine | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0401 | [+0.0150, +0.0598] | 0.094 | 3/3 |
| transfer-random_forest | wine | lightgbm.LossHigh | lowest | auc | 3 | +0.0277 | [+0.0142, +0.0522] | 0.152 | 3/3 |
| transfer-random_forest | wine | pytorch.Influence | lowest | 5 % | 3 | -0.0052 | [-0.0341, +0.0151] | 0.758 | 2/3 |
| transfer-random_forest | wine | pytorch.Influence | lowest | 10 % | 3 | -0.0096 | [-0.0424, +0.0325] | 0.708 | 1/3 |
| transfer-random_forest | wine | pytorch.Influence | lowest | 20 % | 3 | -0.0055 | [-0.0519, +0.0297] | 0.840 | 2/3 |
| transfer-random_forest | wine | pytorch.Influence | lowest | auc | 3 | -0.0063 | [-0.0374, +0.0204] | 0.745 | 1/3 |
| transfer-random_forest | wine | pytorch.LOO | lowest | 5 % | 3 | +0.0011 | [-0.0095, +0.0088] | 0.865 | 2/3 |
| transfer-random_forest | wine | pytorch.LOO | lowest | 10 % | 3 | +0.0095 | [-0.0113, +0.0383] | 0.588 | 2/3 |
| transfer-random_forest | wine | pytorch.LOO | lowest | 20 % | 3 | +0.0104 | [-0.0018, +0.0279] | 0.366 | 2/3 |
| transfer-random_forest | wine | pytorch.LOO | lowest | auc | 3 | +0.0064 | [-0.0037, +0.0179] | 0.413 | 2/3 |
| transfer-random_forest | wine | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0222 | [-0.0103, +0.0561] | 0.366 | 2/3 |
| transfer-random_forest | wine | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0095 | [-0.0400, +0.0605] | 0.774 | 2/3 |
| transfer-random_forest | wine | pytorch.LissaInfluence | lowest | 20 % | 3 | +0.0064 | [-0.0250, +0.0584] | 0.829 | 1/3 |
| transfer-random_forest | wine | pytorch.LissaInfluence | lowest | auc | 3 | +0.0107 | [-0.0161, +0.0513] | 0.655 | 1/3 |
| transfer-random_forest | wine | pytorch.LossHigh | lowest | 5 % | 3 | +0.0154 | [-0.0109, +0.0373] | 0.388 | 2/3 |
| transfer-random_forest | wine | pytorch.LossHigh | lowest | 10 % | 3 | +0.0445 | [+0.0080, +0.0791] | 0.163 | 3/3 |
| transfer-random_forest | wine | pytorch.LossHigh | lowest | 20 % | 3 | +0.0340 | [-0.0094, +0.0590] | 0.259 | 2/3 |
| transfer-random_forest | wine | pytorch.LossHigh | lowest | auc | 3 | +0.0290 | [+0.0056, +0.0520] | 0.163 | 3/3 |
| transfer-random_forest | wine | random_forest.LOO | lowest | 5 % | 3 | +0.0006 | [-0.0195, +0.0165] | 0.961 | 2/3 |
| transfer-random_forest | wine | random_forest.LOO | lowest | 10 % | 3 | -0.0013 | [-0.0500, +0.0398] | 0.965 | 2/3 |
| transfer-random_forest | wine | random_forest.LOO | lowest | 20 % | 3 | +0.0135 | [-0.0278, +0.0426] | 0.590 | 2/3 |
| transfer-random_forest | wine | random_forest.LOO | lowest | auc | 3 | +0.0030 | [-0.0245, +0.0297] | 0.864 | 2/3 |
| transfer-random_forest | wine | random_forest.LossHigh | lowest | 5 % | 3 | +0.0202 | [-0.0158, +0.0385] | 0.378 | 2/3 |
| transfer-random_forest | wine | random_forest.LossHigh | lowest | 10 % | 3 | +0.0299 | [+0.0138, +0.0522] | 0.122 | 3/3 |
| transfer-random_forest | wine | random_forest.LossHigh | lowest | 20 % | 3 | +0.0398 | [+0.0167, +0.0526] | 0.075 | 3/3 |
| transfer-random_forest | wine | random_forest.LossHigh | lowest | auc | 3 | +0.0262 | [+0.0175, +0.0422] | 0.082 | 3/3 |
| transfer-random_forest | wine | xgboost.LOO | lowest | 5 % | 3 | -0.0134 | [-0.0201, -0.0044] | 0.104 | 0/3 |
| transfer-random_forest | wine | xgboost.LOO | lowest | 10 % | 3 | +0.0059 | [-0.0172, +0.0330] | 0.727 | 2/3 |
| transfer-random_forest | wine | xgboost.LOO | lowest | 20 % | 3 | +0.0097 | [+0.0005, +0.0149] | 0.170 | 3/3 |
| transfer-random_forest | wine | xgboost.LOO | lowest | auc | 3 | +0.0013 | [-0.0113, +0.0150] | 0.883 | 2/3 |
| transfer-random_forest | wine | xgboost.LossHigh | lowest | 5 % | 3 | +0.0073 | [-0.0146, +0.0323] | 0.645 | 2/3 |
| transfer-random_forest | wine | xgboost.LossHigh | lowest | 10 % | 3 | +0.0126 | [+0.0059, +0.0231] | 0.140 | 3/3 |
| transfer-random_forest | wine | xgboost.LossHigh | lowest | 20 % | 3 | -0.0166 | [-0.0266, -0.0095] | 0.084 | 0/3 |
| transfer-random_forest | wine | xgboost.LossHigh | lowest | auc | 3 | +0.0024 | [-0.0081, +0.0090] | 0.694 | 2/3 |
| transfer-xgboost | adult | any.DataOOB | lowest | 5 % | 3 | +0.0425 | [+0.0375, +0.0523] | 0.013 | 3/3 |
| transfer-xgboost | adult | any.DataOOB | lowest | 10 % | 3 | +0.0609 | [+0.0497, +0.0749] | 0.014 | 3/3 |
| transfer-xgboost | adult | any.DataOOB | lowest | 20 % | 3 | +0.0703 | [+0.0616, +0.0849] | 0.011 | 3/3 |
| transfer-xgboost | adult | any.DataOOB | lowest | auc | 3 | +0.0510 | [+0.0441, +0.0566] | 0.005 | 3/3 |
| transfer-xgboost | adult | any.KNNShapley | lowest | 5 % | 3 | +0.0483 | [+0.0369, +0.0598] | 0.018 | 3/3 |
| transfer-xgboost | adult | any.KNNShapley | lowest | 10 % | 3 | +0.0670 | [+0.0579, +0.0779] | 0.008 | 3/3 |
| transfer-xgboost | adult | any.KNNShapley | lowest | 20 % | 3 | +0.0615 | [+0.0565, +0.0693] | 0.004 | 3/3 |
| transfer-xgboost | adult | any.KNNShapley | lowest | auc | 3 | +0.0525 | [+0.0483, +0.0583] | 0.003 | 3/3 |
| transfer-xgboost | adult | catboost.CatBoostLFC | lowest | 5 % | 3 | +0.0340 | [+0.0240, +0.0455] | 0.032 | 3/3 |
| transfer-xgboost | adult | catboost.CatBoostLFC | lowest | 10 % | 3 | +0.0449 | [+0.0294, +0.0593] | 0.035 | 3/3 |
| transfer-xgboost | adult | catboost.CatBoostLFC | lowest | 20 % | 3 | +0.0467 | [+0.0404, +0.0502] | 0.004 | 3/3 |
| transfer-xgboost | adult | catboost.CatBoostLFC | lowest | auc | 3 | +0.0370 | [+0.0292, +0.0462] | 0.017 | 3/3 |
| transfer-xgboost | adult | catboost.LOO | lowest | 5 % | 3 | +0.0015 | [-0.0138, +0.0261] | 0.915 | 1/3 |
| transfer-xgboost | adult | catboost.LOO | lowest | 10 % | 3 | +0.0032 | [-0.0196, +0.0244] | 0.827 | 2/3 |
| transfer-xgboost | adult | catboost.LOO | lowest | 20 % | 3 | -0.0003 | [-0.0063, +0.0070] | 0.938 | 1/3 |
| transfer-xgboost | adult | catboost.LOO | lowest | auc | 3 | +0.0015 | [-0.0124, +0.0174] | 0.881 | 1/3 |
| transfer-xgboost | adult | catboost.LossHigh | lowest | 5 % | 3 | +0.0484 | [+0.0419, +0.0579] | 0.010 | 3/3 |
| transfer-xgboost | adult | catboost.LossHigh | lowest | 10 % | 3 | +0.0804 | [+0.0647, +0.0997] | 0.016 | 3/3 |
| transfer-xgboost | adult | catboost.LossHigh | lowest | 20 % | 3 | +0.0826 | [+0.0773, +0.0861] | 0.001 | 3/3 |
| transfer-xgboost | adult | catboost.LossHigh | lowest | auc | 3 | +0.0629 | [+0.0558, +0.0712] | 0.005 | 3/3 |
| transfer-xgboost | adult | distill-lightgbm.Influence | lowest | 5 % | 3 | +0.0222 | [+0.0071, +0.0399] | 0.146 | 3/3 |
| transfer-xgboost | adult | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0392 | [+0.0296, +0.0562] | 0.044 | 3/3 |
| transfer-xgboost | adult | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0331 | [+0.0309, +0.0350] | 0.001 | 3/3 |
| transfer-xgboost | adult | distill-lightgbm.Influence | lowest | auc | 3 | +0.0285 | [+0.0212, +0.0388] | 0.033 | 3/3 |
| transfer-xgboost | adult | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0530 | [+0.0477, +0.0560] | 0.002 | 3/3 |
| transfer-xgboost | adult | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0647 | [+0.0551, +0.0776] | 0.011 | 3/3 |
| transfer-xgboost | adult | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0769 | [+0.0719, +0.0865] | 0.004 | 3/3 |
| transfer-xgboost | adult | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0567 | [+0.0542, +0.0612] | 0.002 | 3/3 |
| transfer-xgboost | adult | lightgbm.LOO | lowest | 5 % | 3 | +0.0002 | [-0.0089, +0.0122] | 0.976 | 1/3 |
| transfer-xgboost | adult | lightgbm.LOO | lowest | 10 % | 3 | +0.0130 | [+0.0016, +0.0282] | 0.242 | 3/3 |
| transfer-xgboost | adult | lightgbm.LOO | lowest | 20 % | 3 | +0.0156 | [+0.0124, +0.0217] | 0.037 | 3/3 |
| transfer-xgboost | adult | lightgbm.LOO | lowest | auc | 3 | +0.0088 | [+0.0015, +0.0191] | 0.237 | 3/3 |
| transfer-xgboost | adult | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0347 | [+0.0223, +0.0561] | 0.084 | 3/3 |
| transfer-xgboost | adult | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0569 | [+0.0362, +0.0802] | 0.047 | 3/3 |
| transfer-xgboost | adult | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0674 | [+0.0622, +0.0762] | 0.004 | 3/3 |
| transfer-xgboost | adult | lightgbm.LossHigh | lowest | auc | 3 | +0.0469 | [+0.0382, +0.0601] | 0.020 | 3/3 |
| transfer-xgboost | adult | pytorch.Influence | lowest | 5 % | 3 | +0.0249 | [+0.0116, +0.0399] | 0.094 | 3/3 |
| transfer-xgboost | adult | pytorch.Influence | lowest | 10 % | 3 | +0.0442 | [+0.0230, +0.0705] | 0.087 | 3/3 |
| transfer-xgboost | adult | pytorch.Influence | lowest | 20 % | 3 | +0.0428 | [+0.0230, +0.0534] | 0.050 | 3/3 |
| transfer-xgboost | adult | pytorch.Influence | lowest | auc | 3 | +0.0335 | [+0.0201, +0.0497] | 0.061 | 3/3 |
| transfer-xgboost | adult | pytorch.LOO | lowest | 5 % | 3 | +0.0009 | [-0.0162, +0.0240] | 0.947 | 1/3 |
| transfer-xgboost | adult | pytorch.LOO | lowest | 10 % | 3 | +0.0120 | [-0.0018, +0.0327] | 0.371 | 2/3 |
| transfer-xgboost | adult | pytorch.LOO | lowest | 20 % | 3 | +0.0006 | [-0.0114, +0.0147] | 0.940 | 1/3 |
| transfer-xgboost | adult | pytorch.LOO | lowest | auc | 3 | +0.0049 | [-0.0049, +0.0219] | 0.624 | 1/3 |
| transfer-xgboost | adult | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0455 | [+0.0261, +0.0663] | 0.060 | 3/3 |
| transfer-xgboost | adult | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0660 | [+0.0465, +0.0920] | 0.040 | 3/3 |
| transfer-xgboost | adult | pytorch.LissaInfluence | lowest | 20 % | 3 | +0.0777 | [+0.0748, +0.0829] | 0.001 | 3/3 |
| transfer-xgboost | adult | pytorch.LissaInfluence | lowest | auc | 3 | +0.0555 | [+0.0447, +0.0699] | 0.018 | 3/3 |
| transfer-xgboost | adult | pytorch.LossHigh | lowest | 5 % | 3 | +0.0461 | [+0.0405, +0.0555] | 0.010 | 3/3 |
| transfer-xgboost | adult | pytorch.LossHigh | lowest | 10 % | 3 | +0.0672 | [+0.0584, +0.0795] | 0.009 | 3/3 |
| transfer-xgboost | adult | pytorch.LossHigh | lowest | 20 % | 3 | +0.0860 | [+0.0812, +0.0910] | 0.001 | 3/3 |
| transfer-xgboost | adult | pytorch.LossHigh | lowest | auc | 3 | +0.0582 | [+0.0548, +0.0640] | 0.002 | 3/3 |
| transfer-xgboost | adult | random_forest.LOO | lowest | 5 % | 3 | +0.0034 | [-0.0039, +0.0150] | 0.617 | 1/3 |
| transfer-xgboost | adult | random_forest.LOO | lowest | 10 % | 3 | +0.0031 | [-0.0107, +0.0185] | 0.746 | 2/3 |
| transfer-xgboost | adult | random_forest.LOO | lowest | 20 % | 3 | -0.0056 | [-0.0143, +0.0081] | 0.505 | 1/3 |
| transfer-xgboost | adult | random_forest.LOO | lowest | auc | 3 | +0.0006 | [-0.0078, +0.0080] | 0.902 | 2/3 |
| transfer-xgboost | adult | random_forest.LossHigh | lowest | 5 % | 3 | +0.0509 | [+0.0431, +0.0661] | 0.022 | 3/3 |
| transfer-xgboost | adult | random_forest.LossHigh | lowest | 10 % | 3 | +0.0759 | [+0.0653, +0.0956] | 0.017 | 3/3 |
| transfer-xgboost | adult | random_forest.LossHigh | lowest | 20 % | 3 | +0.0832 | [+0.0662, +0.0956] | 0.011 | 3/3 |
| transfer-xgboost | adult | random_forest.LossHigh | lowest | auc | 3 | +0.0620 | [+0.0577, +0.0689] | 0.003 | 3/3 |
| transfer-xgboost | adult | xgboost.LOO | lowest | 5 % | 3 | +0.0133 | [+0.0063, +0.0258] | 0.168 | 3/3 |
| transfer-xgboost | adult | xgboost.LOO | lowest | 10 % | 3 | +0.0193 | [-0.0018, +0.0489] | 0.334 | 2/3 |
| transfer-xgboost | adult | xgboost.LOO | lowest | 20 % | 3 | +0.0065 | [-0.0161, +0.0224] | 0.631 | 2/3 |
| transfer-xgboost | adult | xgboost.LOO | lowest | auc | 3 | +0.0122 | [-0.0028, +0.0304] | 0.336 | 2/3 |
| transfer-xgboost | adult | xgboost.LossHigh | lowest | 5 % | 3 | +0.0178 | [+0.0092, +0.0275] | 0.078 | 3/3 |
| transfer-xgboost | adult | xgboost.LossHigh | lowest | 10 % | 3 | +0.0379 | [+0.0261, +0.0547] | 0.048 | 3/3 |
| transfer-xgboost | adult | xgboost.LossHigh | lowest | 20 % | 3 | +0.0484 | [+0.0417, +0.0529] | 0.005 | 3/3 |
| transfer-xgboost | adult | xgboost.LossHigh | lowest | auc | 3 | +0.0308 | [+0.0244, +0.0406] | 0.025 | 3/3 |
| transfer-xgboost | covertype | any.DataOOB | lowest | 5 % | 3 | +0.0065 | [+0.0008, +0.0098] | 0.151 | 3/3 |
| transfer-xgboost | covertype | any.DataOOB | lowest | 10 % | 3 | +0.0158 | [+0.0074, +0.0310] | 0.174 | 3/3 |
| transfer-xgboost | covertype | any.DataOOB | lowest | 20 % | 3 | +0.0153 | [+0.0064, +0.0298] | 0.170 | 3/3 |
| transfer-xgboost | covertype | any.DataOOB | lowest | auc | 3 | +0.0114 | [+0.0054, +0.0215] | 0.155 | 3/3 |
| transfer-xgboost | covertype | any.KNNShapley | lowest | 5 % | 3 | +0.0035 | [+0.0020, +0.0052] | 0.065 | 3/3 |
| transfer-xgboost | covertype | any.KNNShapley | lowest | 10 % | 3 | +0.0091 | [+0.0032, +0.0172] | 0.160 | 3/3 |
| transfer-xgboost | covertype | any.KNNShapley | lowest | 20 % | 3 | +0.0127 | [+0.0054, +0.0172] | 0.075 | 3/3 |
| transfer-xgboost | covertype | any.KNNShapley | lowest | auc | 3 | +0.0075 | [+0.0048, +0.0120] | 0.083 | 3/3 |
| transfer-xgboost | covertype | catboost.LOO | lowest | 5 % | 3 | -0.0112 | [-0.0144, -0.0070] | 0.036 | 0/3 |
| transfer-xgboost | covertype | catboost.LOO | lowest | 10 % | 3 | +0.0014 | [+0.0000, +0.0036] | 0.336 | 2/3 |
| transfer-xgboost | covertype | catboost.LOO | lowest | 20 % | 3 | -0.0040 | [-0.0094, +0.0028] | 0.381 | 1/3 |
| transfer-xgboost | covertype | catboost.LOO | lowest | auc | 3 | -0.0033 | [-0.0052, -0.0018] | 0.083 | 0/3 |
| transfer-xgboost | covertype | catboost.LossHigh | lowest | 5 % | 3 | +0.0021 | [-0.0018, +0.0062] | 0.453 | 2/3 |
| transfer-xgboost | covertype | catboost.LossHigh | lowest | 10 % | 3 | +0.0128 | [+0.0074, +0.0200] | 0.076 | 3/3 |
| transfer-xgboost | covertype | catboost.LossHigh | lowest | 20 % | 3 | +0.0155 | [+0.0088, +0.0266] | 0.108 | 3/3 |
| transfer-xgboost | covertype | catboost.LossHigh | lowest | auc | 3 | +0.0092 | [+0.0055, +0.0157] | 0.105 | 3/3 |
| transfer-xgboost | covertype | distill-lightgbm.Influence | lowest | 5 % | 3 | -0.0019 | [-0.0040, +0.0016] | 0.390 | 1/3 |
| transfer-xgboost | covertype | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0019 | [-0.0060, +0.0084] | 0.701 | 2/3 |
| transfer-xgboost | covertype | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0023 | [-0.0018, +0.0066] | 0.438 | 2/3 |
| transfer-xgboost | covertype | distill-lightgbm.Influence | lowest | auc | 3 | +0.0008 | [-0.0037, +0.0041] | 0.764 | 2/3 |
| transfer-xgboost | covertype | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0019 | [-0.0024, +0.0056] | 0.506 | 2/3 |
| transfer-xgboost | covertype | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.0164 | [+0.0126, +0.0232] | 0.041 | 3/3 |
| transfer-xgboost | covertype | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.0233 | [+0.0168, +0.0350] | 0.057 | 3/3 |
| transfer-xgboost | covertype | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.0125 | [+0.0087, +0.0188] | 0.061 | 3/3 |
| transfer-xgboost | covertype | lightgbm.LOO | lowest | 5 % | 3 | -0.0024 | [-0.0040, +0.0004] | 0.230 | 1/3 |
| transfer-xgboost | covertype | lightgbm.LOO | lowest | 10 % | 3 | -0.0024 | [-0.0082, +0.0044] | 0.580 | 1/3 |
| transfer-xgboost | covertype | lightgbm.LOO | lowest | 20 % | 3 | -0.0032 | [-0.0102, +0.0040] | 0.517 | 1/3 |
| transfer-xgboost | covertype | lightgbm.LOO | lowest | auc | 3 | -0.0023 | [-0.0065, -0.0002] | 0.390 | 0/3 |
| transfer-xgboost | covertype | lightgbm.LossHigh | lowest | 5 % | 3 | -0.0020 | [-0.0070, +0.0036] | 0.582 | 1/3 |
| transfer-xgboost | covertype | lightgbm.LossHigh | lowest | 10 % | 3 | +0.0060 | [+0.0000, +0.0100] | 0.188 | 2/3 |
| transfer-xgboost | covertype | lightgbm.LossHigh | lowest | 20 % | 3 | +0.0089 | [+0.0022, +0.0224] | 0.316 | 3/3 |
| transfer-xgboost | covertype | lightgbm.LossHigh | lowest | auc | 3 | +0.0040 | [-0.0012, +0.0102] | 0.356 | 2/3 |
| transfer-xgboost | covertype | pytorch.Influence | lowest | 5 % | 3 | +0.0019 | [-0.0014, +0.0066] | 0.506 | 2/3 |
| transfer-xgboost | covertype | pytorch.Influence | lowest | 10 % | 3 | +0.0086 | [+0.0026, +0.0138] | 0.119 | 3/3 |
| transfer-xgboost | covertype | pytorch.Influence | lowest | 20 % | 3 | +0.0053 | [-0.0062, +0.0152] | 0.487 | 2/3 |
| transfer-xgboost | covertype | pytorch.Influence | lowest | auc | 3 | +0.0050 | [-0.0009, +0.0091] | 0.241 | 2/3 |
| transfer-xgboost | covertype | pytorch.LOO | lowest | 5 % | 3 | -0.0027 | [-0.0058, +0.0004] | 0.266 | 1/3 |
| transfer-xgboost | covertype | pytorch.LOO | lowest | 10 % | 3 | -0.0001 | [-0.0028, +0.0044] | 0.959 | 1/3 |
| transfer-xgboost | covertype | pytorch.LOO | lowest | 20 % | 3 | -0.0042 | [-0.0104, +0.0032] | 0.401 | 1/3 |
| transfer-xgboost | covertype | pytorch.LOO | lowest | auc | 3 | -0.0018 | [-0.0040, +0.0010] | 0.352 | 1/3 |
| transfer-xgboost | covertype | pytorch.LissaInfluence | lowest | 5 % | 3 | -0.0010 | [-0.0086, +0.0046] | 0.823 | 2/3 |
| transfer-xgboost | covertype | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0081 | [-0.0006, +0.0160] | 0.233 | 2/3 |
| transfer-xgboost | covertype | pytorch.LissaInfluence | lowest | 20 % | 3 | +0.0066 | [-0.0080, +0.0190] | 0.490 | 2/3 |
| transfer-xgboost | covertype | pytorch.LissaInfluence | lowest | auc | 3 | +0.0045 | [-0.0044, +0.0119] | 0.448 | 2/3 |
| transfer-xgboost | covertype | pytorch.LossHigh | lowest | 5 % | 3 | +0.0079 | [+0.0074, +0.0088] | 0.003 | 3/3 |
| transfer-xgboost | covertype | pytorch.LossHigh | lowest | 10 % | 3 | +0.0203 | [+0.0122, +0.0256] | 0.039 | 3/3 |
| transfer-xgboost | covertype | pytorch.LossHigh | lowest | 20 % | 3 | +0.0236 | [+0.0180, +0.0320] | 0.031 | 3/3 |
| transfer-xgboost | covertype | pytorch.LossHigh | lowest | auc | 3 | +0.0155 | [+0.0116, +0.0198] | 0.023 | 3/3 |
| transfer-xgboost | covertype | random_forest.LOO | lowest | 5 % | 3 | -0.0020 | [-0.0078, +0.0026] | 0.581 | 1/3 |
| transfer-xgboost | covertype | random_forest.LOO | lowest | 10 % | 3 | -0.0014 | [-0.0116, +0.0078] | 0.827 | 1/3 |
| transfer-xgboost | covertype | random_forest.LOO | lowest | 20 % | 3 | -0.0054 | [-0.0074, -0.0018] | 0.096 | 0/3 |
| transfer-xgboost | covertype | random_forest.LOO | lowest | auc | 3 | -0.0024 | [-0.0081, +0.0023] | 0.519 | 1/3 |
| transfer-xgboost | covertype | random_forest.LossHigh | lowest | 5 % | 3 | -0.0039 | [-0.0052, -0.0014] | 0.089 | 0/3 |
| transfer-xgboost | covertype | random_forest.LossHigh | lowest | 10 % | 3 | +0.0073 | [+0.0042, +0.0110] | 0.066 | 3/3 |
| transfer-xgboost | covertype | random_forest.LossHigh | lowest | 20 % | 3 | +0.0076 | [+0.0016, +0.0154] | 0.204 | 3/3 |
| transfer-xgboost | covertype | random_forest.LossHigh | lowest | auc | 3 | +0.0037 | [+0.0007, +0.0061] | 0.143 | 3/3 |
| transfer-xgboost | covertype | xgboost.LOO | lowest | 5 % | 3 | -0.0044 | [-0.0086, -0.0012] | 0.183 | 0/3 |
| transfer-xgboost | covertype | xgboost.LOO | lowest | 10 % | 3 | -0.0035 | [-0.0052, -0.0022] | 0.061 | 0/3 |
| transfer-xgboost | covertype | xgboost.LOO | lowest | 20 % | 3 | -0.0031 | [-0.0086, +0.0014] | 0.406 | 1/3 |
| transfer-xgboost | covertype | xgboost.LOO | lowest | auc | 3 | -0.0032 | [-0.0062, -0.0011] | 0.182 | 0/3 |
| transfer-xgboost | covertype | xgboost.LossHigh | lowest | 5 % | 3 | -0.0029 | [-0.0032, -0.0026] | 0.004 | 0/3 |
| transfer-xgboost | covertype | xgboost.LossHigh | lowest | 10 % | 3 | +0.0071 | [+0.0056, +0.0082] | 0.012 | 3/3 |
| transfer-xgboost | covertype | xgboost.LossHigh | lowest | 20 % | 3 | +0.0022 | [-0.0068, +0.0106] | 0.705 | 2/3 |
| transfer-xgboost | covertype | xgboost.LossHigh | lowest | auc | 3 | +0.0025 | [-0.0003, +0.0050] | 0.245 | 2/3 |
| transfer-xgboost | housing | any.DataOOB | lowest | 5 % | 3 | +10396.1133 | [+8207.9602, +11573.3843] | 0.011 | 3/3 |
| transfer-xgboost | housing | any.DataOOB | lowest | 10 % | 3 | +24639.3921 | [+23370.9966, +26435.8101] | 0.001 | 3/3 |
| transfer-xgboost | housing | any.DataOOB | lowest | 20 % | 3 | +25014.5229 | [+24210.4227, +26454.4031] | 0.001 | 3/3 |
| transfer-xgboost | housing | any.DataOOB | lowest | auc | 3 | +18092.4311 | [+17188.4393, +19378.7784] | 0.001 | 3/3 |
| transfer-xgboost | housing | catboost.CatBoostLFC | lowest | 5 % | 3 | +1969.5935 | [-23.5404, +3480.1752] | 0.199 | 2/3 |
| transfer-xgboost | housing | catboost.CatBoostLFC | lowest | 10 % | 3 | +1105.0554 | [-104.0581, +2521.9251] | 0.286 | 2/3 |
| transfer-xgboost | housing | catboost.CatBoostLFC | lowest | 20 % | 3 | -2212.9835 | [-2638.9287, -1776.8886] | 0.012 | 0/3 |
| transfer-xgboost | housing | catboost.CatBoostLFC | lowest | auc | 3 | +353.5483 | [-600.6902, +1371.5436] | 0.598 | 2/3 |
| transfer-xgboost | housing | catboost.LOO | lowest | 5 % | 3 | +1030.3156 | [-2080.8660, +3073.2346] | 0.581 | 2/3 |
| transfer-xgboost | housing | catboost.LOO | lowest | 10 % | 3 | -108.6379 | [-649.2011, +243.5339] | 0.730 | 2/3 |
| transfer-xgboost | housing | catboost.LOO | lowest | 20 % | 3 | -653.3998 | [-1755.8811, +62.4795] | 0.363 | 1/3 |
| transfer-xgboost | housing | catboost.LOO | lowest | auc | 3 | +53.4897 | [-1202.6372, +792.9344] | 0.940 | 2/3 |
| transfer-xgboost | housing | catboost.LossHigh | lowest | 5 % | 3 | +11040.2761 | [+9687.2648, +12316.1961] | 0.005 | 3/3 |
| transfer-xgboost | housing | catboost.LossHigh | lowest | 10 % | 3 | +23813.1159 | [+21500.3971, +26398.2735] | 0.004 | 3/3 |
| transfer-xgboost | housing | catboost.LossHigh | lowest | 20 % | 3 | +23855.4802 | [+21647.1607, +26267.9633] | 0.003 | 3/3 |
| transfer-xgboost | housing | catboost.LossHigh | lowest | auc | 3 | +17653.8576 | [+15896.2553, +19545.3924] | 0.004 | 3/3 |
| transfer-xgboost | housing | distill-lightgbm.Influence | lowest | 5 % | 3 | +4108.8055 | [+2688.0308, +5323.9950] | 0.033 | 3/3 |
| transfer-xgboost | housing | distill-lightgbm.Influence | lowest | 10 % | 3 | +7526.6522 | [+6157.1144, +8636.7370] | 0.009 | 3/3 |
| transfer-xgboost | housing | distill-lightgbm.Influence | lowest | 20 % | 3 | +4670.0991 | [+3168.2315, +5655.9643] | 0.026 | 3/3 |
| transfer-xgboost | housing | distill-lightgbm.Influence | lowest | auc | 3 | +5017.2207 | [+4179.5734, +5547.3136] | 0.007 | 3/3 |
| transfer-xgboost | housing | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +10628.6430 | [+9795.5232, +12103.1633] | 0.005 | 3/3 |
| transfer-xgboost | housing | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +24402.1758 | [+23085.8035, +26303.1412] | 0.002 | 3/3 |
| transfer-xgboost | housing | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +25296.9313 | [+22946.5681, +27855.6110] | 0.003 | 3/3 |
| transfer-xgboost | housing | distill-lightgbm.LossHigh | lowest | auc | 3 | +18132.2095 | [+17117.1164, +19324.3913] | 0.001 | 3/3 |
| transfer-xgboost | housing | lightgbm.LOO | lowest | 5 % | 3 | +1023.1690 | [-537.5847, +2830.7260] | 0.406 | 2/3 |
| transfer-xgboost | housing | lightgbm.LOO | lowest | 10 % | 3 | +1764.6497 | [+1054.8312, +3127.2988] | 0.122 | 3/3 |
| transfer-xgboost | housing | lightgbm.LOO | lowest | 20 % | 3 | +1849.6260 | [+588.6792, +3463.9533] | 0.161 | 3/3 |
| transfer-xgboost | housing | lightgbm.LOO | lowest | auc | 3 | +1379.9424 | [+408.3353, +1990.6020] | 0.107 | 3/3 |
| transfer-xgboost | housing | lightgbm.LossHigh | lowest | 5 % | 3 | +11356.4866 | [+10357.7332, +12383.7500] | 0.003 | 3/3 |
| transfer-xgboost | housing | lightgbm.LossHigh | lowest | 10 % | 3 | +24587.8226 | [+23561.3141, +26320.1485] | 0.001 | 3/3 |
| transfer-xgboost | housing | lightgbm.LossHigh | lowest | 20 % | 3 | +25364.7526 | [+23466.9860, +26974.7705] | 0.002 | 3/3 |
| transfer-xgboost | housing | lightgbm.LossHigh | lowest | auc | 3 | +18400.7433 | [+17411.9317, +19445.7425] | 0.001 | 3/3 |
| transfer-xgboost | housing | pytorch.Influence | lowest | 5 % | 3 | +6401.3915 | [+5668.7540, +7478.0075] | 0.007 | 3/3 |
| transfer-xgboost | housing | pytorch.Influence | lowest | 10 % | 3 | +8689.1093 | [+8053.4358, +9745.1171] | 0.004 | 3/3 |
| transfer-xgboost | housing | pytorch.Influence | lowest | 20 % | 3 | +8630.9044 | [+6164.8931, +10723.6470] | 0.023 | 3/3 |
| transfer-xgboost | housing | pytorch.Influence | lowest | auc | 3 | +7016.4900 | [+6075.6150, +8204.8325] | 0.008 | 3/3 |
| transfer-xgboost | housing | pytorch.LOO | lowest | 5 % | 3 | -104.5630 | [-764.7462, +482.3917] | 0.800 | 1/3 |
| transfer-xgboost | housing | pytorch.LOO | lowest | 10 % | 3 | -392.5662 | [-1448.0823, +1628.7428] | 0.735 | 1/3 |
| transfer-xgboost | housing | pytorch.LOO | lowest | 20 % | 3 | -286.0416 | [-1885.3506, +2044.0567] | 0.833 | 1/3 |
| transfer-xgboost | housing | pytorch.LOO | lowest | auc | 3 | -244.8635 | [-1205.5551, +477.1687] | 0.673 | 1/3 |
| transfer-xgboost | housing | pytorch.LissaInfluence | lowest | 5 % | 3 | +6442.2127 | [+5110.2854, +8005.7489] | 0.017 | 3/3 |
| transfer-xgboost | housing | pytorch.LissaInfluence | lowest | 10 % | 3 | +8194.2081 | [+5620.7156, +10937.2745] | 0.033 | 3/3 |
| transfer-xgboost | housing | pytorch.LissaInfluence | lowest | 20 % | 3 | +3988.5348 | [+1348.7160, +8340.0268] | 0.210 | 3/3 |
| transfer-xgboost | housing | pytorch.LissaInfluence | lowest | auc | 3 | +5680.5149 | [+3722.5187, +8187.9219] | 0.050 | 3/3 |
| transfer-xgboost | housing | pytorch.LossHigh | lowest | 5 % | 3 | +10366.0794 | [+9087.9250, +11383.3297] | 0.004 | 3/3 |
| transfer-xgboost | housing | pytorch.LossHigh | lowest | 10 % | 3 | +24017.3191 | [+23296.3376, +25258.0267] | 0.001 | 3/3 |
| transfer-xgboost | housing | pytorch.LossHigh | lowest | 20 % | 3 | +24676.5239 | [+23195.3685, +27553.8301] | 0.003 | 3/3 |
| transfer-xgboost | housing | pytorch.LossHigh | lowest | auc | 3 | +17767.1455 | [+16882.4208, +19206.0500] | 0.002 | 3/3 |
| transfer-xgboost | housing | random_forest.LOO | lowest | 5 % | 3 | -222.7606 | [-2388.7524, +920.5875] | 0.856 | 2/3 |
| transfer-xgboost | housing | random_forest.LOO | lowest | 10 % | 3 | -450.0749 | [-2055.2446, +1117.5377] | 0.672 | 1/3 |
| transfer-xgboost | housing | random_forest.LOO | lowest | 20 % | 3 | +115.1648 | [-1916.2482, +1499.4547] | 0.922 | 2/3 |
| transfer-xgboost | housing | random_forest.LOO | lowest | auc | 3 | -195.6771 | [-1230.9443, +1024.0872] | 0.794 | 1/3 |
| transfer-xgboost | housing | random_forest.LossHigh | lowest | 5 % | 3 | +11393.0782 | [+11071.7016, +11686.0140] | 0.000 | 3/3 |
| transfer-xgboost | housing | random_forest.LossHigh | lowest | 10 % | 3 | +24208.2212 | [+23369.5296, +25877.5290] | 0.001 | 3/3 |
| transfer-xgboost | housing | random_forest.LossHigh | lowest | 20 % | 3 | +24555.1837 | [+23509.4504, +26525.8179] | 0.002 | 3/3 |
| transfer-xgboost | housing | random_forest.LossHigh | lowest | auc | 3 | +18065.1484 | [+17439.0697, +19257.0313] | 0.001 | 3/3 |
| transfer-xgboost | housing | xgboost.LOO | lowest | 5 % | 3 | -505.4736 | [-3015.7656, +1943.8904] | 0.758 | 1/3 |
| transfer-xgboost | housing | xgboost.LOO | lowest | 10 % | 3 | +161.4626 | [-322.7033, +785.9955] | 0.671 | 2/3 |
| transfer-xgboost | housing | xgboost.LOO | lowest | 20 % | 3 | -934.1572 | [-1690.8997, -343.1050] | 0.143 | 0/3 |
| transfer-xgboost | housing | xgboost.LOO | lowest | auc | 3 | -299.3592 | [-1168.7554, +694.9447] | 0.636 | 1/3 |
| transfer-xgboost | housing | xgboost.LossHigh | lowest | 5 % | 3 | +7127.1924 | [+6127.4321, +8505.1989] | 0.010 | 3/3 |
| transfer-xgboost | housing | xgboost.LossHigh | lowest | 10 % | 3 | +10114.1414 | [+9401.5268, +10558.7768] | 0.001 | 3/3 |
| transfer-xgboost | housing | xgboost.LossHigh | lowest | 20 % | 3 | +13951.5979 | [+12373.4049, +15079.9796] | 0.003 | 3/3 |
| transfer-xgboost | housing | xgboost.LossHigh | lowest | auc | 3 | +9062.5006 | [+8518.5045, +9686.1933] | 0.001 | 3/3 |
| transfer-xgboost | wine | any.DataOOB | lowest | 5 % | 3 | +0.0779 | [+0.0109, +0.1310] | 0.158 | 3/3 |
| transfer-xgboost | wine | any.DataOOB | lowest | 10 % | 3 | +0.1320 | [+0.0923, +0.1904] | 0.047 | 3/3 |
| transfer-xgboost | wine | any.DataOOB | lowest | 20 % | 3 | +0.1531 | [+0.1437, +0.1652] | 0.002 | 3/3 |
| transfer-xgboost | wine | any.DataOOB | lowest | auc | 3 | +0.1072 | [+0.0865, +0.1319] | 0.015 | 3/3 |
| transfer-xgboost | wine | catboost.CatBoostLFC | lowest | 5 % | 3 | +0.0253 | [+0.0019, +0.0618] | 0.305 | 3/3 |
| transfer-xgboost | wine | catboost.CatBoostLFC | lowest | 10 % | 3 | +0.0071 | [-0.0418, +0.0747] | 0.858 | 1/3 |
| transfer-xgboost | wine | catboost.CatBoostLFC | lowest | 20 % | 3 | +0.0213 | [-0.0260, +0.0610] | 0.489 | 2/3 |
| transfer-xgboost | wine | catboost.CatBoostLFC | lowest | auc | 3 | +0.0143 | [-0.0067, +0.0463] | 0.472 | 2/3 |
| transfer-xgboost | wine | catboost.LOO | lowest | 5 % | 3 | +0.0156 | [-0.0406, +0.0519] | 0.639 | 2/3 |
| transfer-xgboost | wine | catboost.LOO | lowest | 10 % | 3 | +0.0210 | [-0.0080, +0.0697] | 0.481 | 2/3 |
| transfer-xgboost | wine | catboost.LOO | lowest | 20 % | 3 | +0.0070 | [-0.0150, +0.0374] | 0.699 | 1/3 |
| transfer-xgboost | wine | catboost.LOO | lowest | auc | 3 | +0.0135 | [+0.0056, +0.0193] | 0.080 | 3/3 |
| transfer-xgboost | wine | catboost.LossHigh | lowest | 5 % | 3 | +0.0585 | [+0.0441, +0.0749] | 0.022 | 3/3 |
| transfer-xgboost | wine | catboost.LossHigh | lowest | 10 % | 3 | +0.1600 | [+0.1330, +0.1927] | 0.012 | 3/3 |
| transfer-xgboost | wine | catboost.LossHigh | lowest | 20 % | 3 | +0.1314 | [+0.1053, +0.1599] | 0.014 | 3/3 |
| transfer-xgboost | wine | catboost.LossHigh | lowest | auc | 3 | +0.1075 | [+0.0963, +0.1173] | 0.003 | 3/3 |
| transfer-xgboost | wine | distill-lightgbm.Influence | lowest | 5 % | 3 | +0.0624 | [+0.0510, +0.0699] | 0.008 | 3/3 |
| transfer-xgboost | wine | distill-lightgbm.Influence | lowest | 10 % | 3 | +0.0600 | [+0.0085, +0.0859] | 0.145 | 3/3 |
| transfer-xgboost | wine | distill-lightgbm.Influence | lowest | 20 % | 3 | +0.0543 | [+0.0057, +0.1078] | 0.208 | 3/3 |
| transfer-xgboost | wine | distill-lightgbm.Influence | lowest | auc | 3 | +0.0517 | [+0.0174, +0.0765] | 0.100 | 3/3 |
| transfer-xgboost | wine | distill-lightgbm.LossHigh | lowest | 5 % | 3 | +0.0949 | [+0.0551, +0.1561] | 0.093 | 3/3 |
| transfer-xgboost | wine | distill-lightgbm.LossHigh | lowest | 10 % | 3 | +0.1354 | [+0.0962, +0.1835] | 0.034 | 3/3 |
| transfer-xgboost | wine | distill-lightgbm.LossHigh | lowest | 20 % | 3 | +0.1532 | [+0.1356, +0.1750] | 0.006 | 3/3 |
| transfer-xgboost | wine | distill-lightgbm.LossHigh | lowest | auc | 3 | +0.1128 | [+0.0917, +0.1302] | 0.010 | 3/3 |
| transfer-xgboost | wine | lightgbm.LOO | lowest | 5 % | 3 | +0.0029 | [-0.0182, +0.0274] | 0.845 | 1/3 |
| transfer-xgboost | wine | lightgbm.LOO | lowest | 10 % | 3 | +0.0173 | [+0.0120, +0.0221] | 0.028 | 3/3 |
| transfer-xgboost | wine | lightgbm.LOO | lowest | 20 % | 3 | +0.0487 | [-0.0223, +0.1423] | 0.424 | 2/3 |
| transfer-xgboost | wine | lightgbm.LOO | lowest | auc | 3 | +0.0194 | [-0.0034, +0.0507] | 0.353 | 2/3 |
| transfer-xgboost | wine | lightgbm.LossHigh | lowest | 5 % | 3 | +0.0992 | [+0.0666, +0.1213] | 0.027 | 3/3 |
| transfer-xgboost | wine | lightgbm.LossHigh | lowest | 10 % | 3 | +0.1424 | [+0.1232, +0.1673] | 0.008 | 3/3 |
| transfer-xgboost | wine | lightgbm.LossHigh | lowest | 20 % | 3 | +0.1420 | [+0.1176, +0.1570] | 0.007 | 3/3 |
| transfer-xgboost | wine | lightgbm.LossHigh | lowest | auc | 3 | +0.1137 | [+0.1088, +0.1194] | 0.001 | 3/3 |
| transfer-xgboost | wine | pytorch.Influence | lowest | 5 % | 3 | +0.0573 | [+0.0361, +0.0807] | 0.047 | 3/3 |
| transfer-xgboost | wine | pytorch.Influence | lowest | 10 % | 3 | +0.0484 | [+0.0445, +0.0522] | 0.002 | 3/3 |
| transfer-xgboost | wine | pytorch.Influence | lowest | 20 % | 3 | +0.0122 | [-0.0102, +0.0297] | 0.408 | 2/3 |
| transfer-xgboost | wine | pytorch.Influence | lowest | auc | 3 | +0.0356 | [+0.0294, +0.0412] | 0.009 | 3/3 |
| transfer-xgboost | wine | pytorch.LOO | lowest | 5 % | 3 | -0.0001 | [-0.0577, +0.0476] | 0.998 | 2/3 |
| transfer-xgboost | wine | pytorch.LOO | lowest | 10 % | 3 | +0.0211 | [+0.0042, +0.0380] | 0.163 | 3/3 |
| transfer-xgboost | wine | pytorch.LOO | lowest | 20 % | 3 | +0.0141 | [-0.0272, +0.0611] | 0.637 | 2/3 |
| transfer-xgboost | wine | pytorch.LOO | lowest | auc | 3 | +0.0114 | [-0.0133, +0.0320] | 0.479 | 2/3 |
| transfer-xgboost | wine | pytorch.LissaInfluence | lowest | 5 % | 3 | +0.0634 | [+0.0222, +0.1395] | 0.238 | 3/3 |
| transfer-xgboost | wine | pytorch.LissaInfluence | lowest | 10 % | 3 | +0.0612 | [-0.0435, +0.1408] | 0.379 | 2/3 |
| transfer-xgboost | wine | pytorch.LissaInfluence | lowest | 20 % | 3 | +0.0872 | [+0.0527, +0.1519] | 0.115 | 3/3 |
| transfer-xgboost | wine | pytorch.LissaInfluence | lowest | auc | 3 | +0.0606 | [+0.0040, +0.1052] | 0.179 | 3/3 |
| transfer-xgboost | wine | pytorch.LossHigh | lowest | 5 % | 3 | +0.0784 | [+0.0394, +0.1367] | 0.119 | 3/3 |
| transfer-xgboost | wine | pytorch.LossHigh | lowest | 10 % | 3 | +0.1340 | [+0.1220, +0.1417] | 0.002 | 3/3 |
| transfer-xgboost | wine | pytorch.LossHigh | lowest | 20 % | 3 | +0.1586 | [+0.1494, +0.1663] | 0.001 | 3/3 |
| transfer-xgboost | wine | pytorch.LossHigh | lowest | auc | 3 | +0.1095 | [+0.0991, +0.1215] | 0.004 | 3/3 |
| transfer-xgboost | wine | random_forest.LOO | lowest | 5 % | 3 | +0.0324 | [+0.0095, +0.0726] | 0.250 | 3/3 |
| transfer-xgboost | wine | random_forest.LOO | lowest | 10 % | 3 | +0.0220 | [-0.0478, +0.0800] | 0.615 | 2/3 |
| transfer-xgboost | wine | random_forest.LOO | lowest | 20 % | 3 | +0.0197 | [-0.0063, +0.0402] | 0.287 | 2/3 |
| transfer-xgboost | wine | random_forest.LOO | lowest | auc | 3 | +0.0213 | [-0.0055, +0.0545] | 0.350 | 2/3 |
| transfer-xgboost | wine | random_forest.LossHigh | lowest | 5 % | 3 | +0.1156 | [+0.1128, +0.1186] | 0.000 | 3/3 |
| transfer-xgboost | wine | random_forest.LossHigh | lowest | 10 % | 3 | +0.1268 | [+0.0919, +0.1932] | 0.062 | 3/3 |
| transfer-xgboost | wine | random_forest.LossHigh | lowest | 20 % | 3 | +0.1734 | [+0.1726, +0.1751] | 0.000 | 3/3 |
| transfer-xgboost | wine | random_forest.LossHigh | lowest | auc | 3 | +0.1198 | [+0.1058, +0.1451] | 0.011 | 3/3 |
| transfer-xgboost | wine | xgboost.LOO | lowest | 5 % | 3 | -0.0179 | [-0.0268, -0.0040] | 0.126 | 0/3 |
| transfer-xgboost | wine | xgboost.LOO | lowest | 10 % | 3 | -0.0079 | [-0.0512, +0.0195] | 0.754 | 2/3 |
| transfer-xgboost | wine | xgboost.LOO | lowest | 20 % | 3 | +0.0242 | [-0.0195, +0.0884] | 0.538 | 2/3 |
| transfer-xgboost | wine | xgboost.LOO | lowest | auc | 3 | -0.0014 | [-0.0076, +0.0019] | 0.699 | 2/3 |
| transfer-xgboost | wine | xgboost.LossHigh | lowest | 5 % | 3 | +0.0615 | [+0.0197, +0.0942] | 0.108 | 3/3 |
| transfer-xgboost | wine | xgboost.LossHigh | lowest | 10 % | 3 | +0.0393 | [-0.0337, +0.1127] | 0.450 | 2/3 |
| transfer-xgboost | wine | xgboost.LossHigh | lowest | 20 % | 3 | +0.0359 | [-0.0102, +0.0834] | 0.315 | 2/3 |
| transfer-xgboost | wine | xgboost.LossHigh | lowest | auc | 3 | +0.0391 | [+0.0084, +0.0558] | 0.126 | 3/3 |

# Detection of corrupted points

| study | dataset | method | n | AUC | AUC − 0.5, 95 % CI | p (vs 0.5) |
|---|---|---|---|---|---|---|
| damp-linear-0.0001 | adult | Influence | 3 | 0.786 | [+0.241, +0.317] | 0.006 |
| damp-linear-0.0001 | adult | LissaInfluence | 3 | 0.854 | [+0.311, +0.399] | 0.005 |
| damp-linear-0.0001 | adult | LossHigh | 3 | 0.917 | [+0.403, +0.430] | 0.000 |
| damp-linear-0.0001 | covertype | Influence | 3 | 0.862 | [+0.331, +0.393] | 0.002 |
| damp-linear-0.0001 | covertype | LissaInfluence | 3 | 0.835 | [+0.301, +0.378] | 0.005 |
| damp-linear-0.0001 | covertype | LossHigh | 3 | 0.921 | [+0.408, +0.427] | 0.000 |
| damp-linear-0.0001 | housing | Influence | 3 | 0.532 | [-0.038, +0.074] | 0.461 |
| damp-linear-0.0001 | housing | LissaInfluence | 3 | 0.548 | [+0.009, +0.073] | 0.138 |
| damp-linear-0.0001 | housing | LossHigh | 3 | 0.995 | [+0.492, +0.497] | 0.000 |
| damp-linear-0.0001 | wine | Influence | 3 | 0.577 | [+0.040, +0.106] | 0.059 |
| damp-linear-0.0001 | wine | LissaInfluence | 3 | 0.592 | [+0.052, +0.140] | 0.070 |
| damp-linear-0.0001 | wine | LossHigh | 3 | 0.982 | [+0.475, +0.494] | 0.000 |
| damp-linear-0.01 | adult | Influence | 3 | 0.833 | [+0.271, +0.380] | 0.009 |
| damp-linear-0.01 | adult | LissaInfluence | 3 | 0.854 | [+0.311, +0.399] | 0.005 |
| damp-linear-0.01 | adult | LossHigh | 3 | 0.917 | [+0.403, +0.430] | 0.000 |
| damp-linear-0.01 | covertype | Influence | 3 | 0.862 | [+0.336, +0.389] | 0.002 |
| damp-linear-0.01 | covertype | LissaInfluence | 3 | 0.835 | [+0.300, +0.378] | 0.005 |
| damp-linear-0.01 | covertype | LossHigh | 3 | 0.921 | [+0.408, +0.427] | 0.000 |
| damp-linear-0.01 | housing | Influence | 3 | 0.532 | [-0.036, +0.075] | 0.450 |
| damp-linear-0.01 | housing | LissaInfluence | 3 | 0.549 | [+0.009, +0.074] | 0.138 |
| damp-linear-0.01 | housing | LossHigh | 3 | 0.995 | [+0.492, +0.497] | 0.000 |
| damp-linear-0.01 | wine | Influence | 3 | 0.579 | [+0.040, +0.110] | 0.062 |
| damp-linear-0.01 | wine | LissaInfluence | 3 | 0.592 | [+0.052, +0.140] | 0.070 |
| damp-linear-0.01 | wine | LossHigh | 3 | 0.982 | [+0.475, +0.494] | 0.000 |
| damp-linear-1 | adult | Influence | 3 | 0.841 | [+0.291, +0.390] | 0.007 |
| damp-linear-1 | adult | LissaInfluence | 3 | 0.841 | [+0.287, +0.389] | 0.007 |
| damp-linear-1 | adult | LossHigh | 3 | 0.917 | [+0.403, +0.430] | 0.000 |
| damp-linear-1 | covertype | Influence | 3 | 0.793 | [+0.238, +0.356] | 0.013 |
| damp-linear-1 | covertype | LissaInfluence | 3 | 0.790 | [+0.235, +0.352] | 0.014 |
| damp-linear-1 | covertype | LossHigh | 3 | 0.921 | [+0.408, +0.427] | 0.000 |
| damp-linear-1 | housing | Influence | 3 | 0.551 | [+0.007, +0.075] | 0.147 |
| damp-linear-1 | housing | LissaInfluence | 3 | 0.545 | [+0.001, +0.073] | 0.180 |
| damp-linear-1 | housing | LossHigh | 3 | 0.995 | [+0.492, +0.497] | 0.000 |
| damp-linear-1 | wine | Influence | 3 | 0.588 | [+0.038, +0.151] | 0.119 |
| damp-linear-1 | wine | LissaInfluence | 3 | 0.592 | [+0.048, +0.146] | 0.086 |
| damp-linear-1 | wine | LossHigh | 3 | 0.982 | [+0.475, +0.494] | 0.000 |
| damp-linear-1e-06 | adult | Influence | 3 | 0.781 | [+0.238, +0.309] | 0.006 |
| damp-linear-1e-06 | adult | LissaInfluence | 3 | 0.854 | [+0.311, +0.399] | 0.005 |
| damp-linear-1e-06 | adult | LossHigh | 3 | 0.917 | [+0.403, +0.430] | 0.000 |
| damp-linear-1e-06 | covertype | Influence | 3 | 0.856 | [+0.319, +0.393] | 0.004 |
| damp-linear-1e-06 | covertype | LissaInfluence | 3 | 0.835 | [+0.301, +0.378] | 0.005 |
| damp-linear-1e-06 | covertype | LossHigh | 3 | 0.921 | [+0.408, +0.427] | 0.000 |
| damp-linear-1e-06 | housing | Influence | 3 | 0.532 | [-0.038, +0.074] | 0.460 |
| damp-linear-1e-06 | housing | LissaInfluence | 3 | 0.548 | [+0.009, +0.073] | 0.138 |
| damp-linear-1e-06 | housing | LossHigh | 3 | 0.995 | [+0.492, +0.497] | 0.000 |
| damp-linear-1e-06 | wine | Influence | 3 | 0.577 | [+0.040, +0.106] | 0.059 |
| damp-linear-1e-06 | wine | LissaInfluence | 3 | 0.592 | [+0.052, +0.140] | 0.070 |
| damp-linear-1e-06 | wine | LossHigh | 3 | 0.982 | [+0.475, +0.494] | 0.000 |
| damp-mlp-0.0001 | adult | Influence | 3 | 0.498 | [-0.010, +0.004] | 0.707 |
| damp-mlp-0.0001 | adult | LissaInfluence | 3 | 0.852 | [+0.301, +0.397] | 0.006 |
| damp-mlp-0.0001 | adult | LossHigh | 3 | 0.925 | [+0.415, +0.433] | 0.000 |
| damp-mlp-0.0001 | housing | Influence | 3 | 0.530 | [-0.016, +0.055] | 0.323 |
| damp-mlp-0.0001 | housing | LissaInfluence | 3 | 0.541 | [+0.015, +0.066] | 0.108 |
| damp-mlp-0.0001 | housing | LossHigh | 3 | 0.998 | [+0.497, +0.498] | 0.000 |
| damp-mlp-0.0001 | wine | Influence | 3 | 0.532 | [-0.018, +0.106] | 0.483 |
| damp-mlp-0.0001 | wine | LissaInfluence | 3 | 0.620 | [+0.010, +0.203] | 0.171 |
| damp-mlp-0.0001 | wine | LossHigh | 3 | 0.984 | [+0.476, +0.495] | 0.000 |
| damp-mlp-0.01 | adult | Influence | 3 | 0.696 | [+0.151, +0.224] | 0.013 |
| damp-mlp-0.01 | adult | LissaInfluence | 3 | 0.853 | [+0.301, +0.399] | 0.006 |
| damp-mlp-0.01 | adult | LossHigh | 3 | 0.925 | [+0.415, +0.433] | 0.000 |
| damp-mlp-0.01 | housing | Influence | 3 | 0.505 | [-0.044, +0.057] | 0.882 |
| damp-mlp-0.01 | housing | LissaInfluence | 3 | 0.541 | [+0.015, +0.065] | 0.108 |
| damp-mlp-0.01 | housing | LossHigh | 3 | 0.998 | [+0.497, +0.498] | 0.000 |
| damp-mlp-0.01 | wine | Influence | 3 | 0.498 | [-0.031, +0.052] | 0.943 |
| damp-mlp-0.01 | wine | LissaInfluence | 3 | 0.620 | [+0.010, +0.203] | 0.172 |
| damp-mlp-0.01 | wine | LossHigh | 3 | 0.984 | [+0.476, +0.495] | 0.000 |
| damp-mlp-0.1 | adult | Influence | 3 | 0.852 | [+0.326, +0.380] | 0.002 |
| damp-mlp-0.1 | covertype | Influence | 3 | 0.818 | [+0.269, +0.354] | 0.006 |
| damp-mlp-0.1 | housing | Influence | 3 | 0.546 | [-0.012, +0.102] | 0.296 |
| damp-mlp-0.1 | wine | Influence | 3 | 0.599 | [+0.015, +0.179] | 0.170 |
| damp-mlp-1 | adult | Influence | 3 | 0.892 | [+0.373, +0.419] | 0.001 |
| damp-mlp-1 | adult | LissaInfluence | 3 | 0.877 | [+0.360, +0.397] | 0.001 |
| damp-mlp-1 | adult | LossHigh | 3 | 0.925 | [+0.415, +0.433] | 0.000 |
| damp-mlp-1 | covertype | Influence | 3 | 0.861 | [+0.291, +0.419] | 0.011 |
| damp-mlp-1 | housing | Influence | 3 | 0.538 | [-0.005, +0.067] | 0.227 |
| damp-mlp-1 | housing | LissaInfluence | 3 | 0.540 | [+0.010, +0.063] | 0.126 |
| damp-mlp-1 | housing | LossHigh | 3 | 0.998 | [+0.497, +0.498] | 0.000 |
| damp-mlp-1 | wine | Influence | 3 | 0.621 | [+0.009, +0.186] | 0.164 |
| damp-mlp-1 | wine | LissaInfluence | 3 | 0.619 | [-0.006, +0.192] | 0.198 |
| damp-mlp-1 | wine | LossHigh | 3 | 0.984 | [+0.476, +0.495] | 0.000 |
| damp-mlp-1e-06 | adult | Influence | 3 | 0.543 | [+0.025, +0.075] | 0.115 |
| damp-mlp-1e-06 | adult | LissaInfluence | 3 | 0.852 | [+0.301, +0.397] | 0.006 |
| damp-mlp-1e-06 | adult | LossHigh | 3 | 0.925 | [+0.415, +0.433] | 0.000 |
| damp-mlp-1e-06 | housing | Influence | 3 | 0.521 | [-0.001, +0.048] | 0.281 |
| damp-mlp-1e-06 | housing | LissaInfluence | 3 | 0.541 | [+0.015, +0.066] | 0.108 |
| damp-mlp-1e-06 | housing | LossHigh | 3 | 0.998 | [+0.497, +0.498] | 0.000 |
| damp-mlp-1e-06 | wine | Influence | 3 | 0.517 | [-0.041, +0.065] | 0.633 |
| damp-mlp-1e-06 | wine | LissaInfluence | 3 | 0.620 | [+0.010, +0.203] | 0.171 |
| damp-mlp-1e-06 | wine | LossHigh | 3 | 0.984 | [+0.476, +0.495] | 0.000 |
| distill-catboost-noise10 | adult | CatBoostLFC | 3 | 0.748 | [+0.220, +0.305] | 0.013 |
| distill-catboost-noise10 | adult | DataOOB | 3 | 0.896 | [+0.389, +0.405] | 0.000 |
| distill-catboost-noise10 | adult | Influence | 3 | 0.537 | [+0.006, +0.070] | 0.179 |
| distill-catboost-noise10 | adult | LissaInfluence | 3 | 0.764 | [+0.252, +0.277] | 0.001 |
| distill-catboost-noise10 | adult | LossHigh | 3 | 0.870 | [+0.352, +0.384] | 0.001 |
| distill-catboost-noise10 | covertype | DataOOB | 3 | 0.950 | [+0.442, +0.459] | 0.000 |
| distill-catboost-noise10 | covertype | Influence | 3 | 0.501 | [-0.055, +0.051] | 0.978 |
| distill-catboost-noise10 | covertype | LissaInfluence | 3 | 0.878 | [+0.355, +0.398] | 0.001 |
| distill-catboost-noise10 | covertype | LossHigh | 3 | 0.939 | [+0.425, +0.446] | 0.000 |
| distill-catboost-noise10 | housing | DataOOB | 3 | 0.998 | [+0.497, +0.499] | 0.000 |
| distill-catboost-noise10 | housing | Influence | 3 | 0.535 | [-0.001, +0.056] | 0.190 |
| distill-catboost-noise10 | housing | LissaInfluence | 3 | 0.546 | [+0.008, +0.074] | 0.143 |
| distill-catboost-noise10 | housing | LossHigh | 3 | 0.995 | [+0.493, +0.496] | 0.000 |
| distill-catboost-noise10 | wine | DataOOB | 3 | 0.984 | [+0.477, +0.494] | 0.000 |
| distill-catboost-noise10 | wine | Influence | 3 | 0.446 | [-0.098, +0.001] | 0.204 |
| distill-catboost-noise10 | wine | LissaInfluence | 3 | 0.586 | [+0.040, +0.176] | 0.198 |
| distill-catboost-noise10 | wine | LossHigh | 3 | 0.978 | [+0.474, +0.485] | 0.000 |
| distill-catboost-noise10-tgtteacher | adult | Influence | 3 | 0.503 | [-0.017, +0.032] | 0.845 |
| distill-catboost-noise10-tgtteacher | adult | LissaInfluence | 3 | 0.767 | [+0.239, +0.287] | 0.003 |
| distill-catboost-noise10-tgtteacher | covertype | Influence | 3 | 0.563 | [+0.046, +0.087] | 0.037 |
| distill-catboost-noise10-tgtteacher | covertype | LissaInfluence | 3 | 0.911 | [+0.399, +0.418] | 0.000 |
| distill-catboost-noise10-tgtteacher | housing | Influence | 3 | 0.503 | [-0.011, +0.014] | 0.739 |
| distill-catboost-noise10-tgtteacher | housing | LissaInfluence | 3 | 0.503 | [-0.000, +0.010] | 0.394 |
| distill-catboost-noise10-tgtteacher | wine | Influence | 3 | 0.500 | [-0.035, +0.050] | 0.993 |
| distill-catboost-noise10-tgtteacher | wine | LissaInfluence | 3 | 0.511 | [-0.056, +0.064] | 0.780 |
| distill-lightgbm-noise10 | adult | BoostIn | 3 | 0.829 | [+0.297, +0.350] | 0.002 |
| distill-lightgbm-noise10 | adult | DataOOB | 3 | 0.896 | [+0.389, +0.405] | 0.000 |
| distill-lightgbm-noise10 | adult | Influence | 3 | 0.532 | [+0.008, +0.055] | 0.143 |
| distill-lightgbm-noise10 | adult | LissaInfluence | 3 | 0.760 | [+0.242, +0.277] | 0.002 |
| distill-lightgbm-noise10 | adult | LossHigh | 3 | 0.878 | [+0.362, +0.389] | 0.000 |
| distill-lightgbm-noise10 | covertype | BoostIn | 3 | 0.908 | [+0.394, +0.430] | 0.001 |
| distill-lightgbm-noise10 | covertype | DataOOB | 3 | 0.950 | [+0.442, +0.459] | 0.000 |
| distill-lightgbm-noise10 | covertype | Influence | 3 | 0.517 | [-0.064, +0.075] | 0.729 |
| distill-lightgbm-noise10 | covertype | LissaInfluence | 3 | 0.788 | [+0.200, +0.371] | 0.028 |
| distill-lightgbm-noise10 | covertype | LossHigh | 3 | 0.944 | [+0.435, +0.457] | 0.000 |
| distill-lightgbm-noise10 | housing | BoostIn | 3 | 0.529 | [+0.007, +0.057] | 0.182 |
| distill-lightgbm-noise10 | housing | DataOOB | 3 | 0.998 | [+0.497, +0.499] | 0.000 |
| distill-lightgbm-noise10 | housing | Influence | 3 | 0.474 | [-0.048, +0.006] | 0.249 |
| distill-lightgbm-noise10 | housing | LissaInfluence | 3 | 0.507 | [-0.003, +0.018] | 0.358 |
| distill-lightgbm-noise10 | housing | LossHigh | 3 | 0.998 | [+0.498, +0.499] | 0.000 |
| distill-lightgbm-noise10 | wine | BoostIn | 3 | 0.568 | [+0.004, +0.174] | 0.330 |
| distill-lightgbm-noise10 | wine | DataOOB | 3 | 0.984 | [+0.477, +0.494] | 0.000 |
| distill-lightgbm-noise10 | wine | Influence | 3 | 0.463 | [-0.052, -0.018] | 0.064 |
| distill-lightgbm-noise10 | wine | LissaInfluence | 3 | 0.555 | [-0.052, +0.170] | 0.483 |
| distill-lightgbm-noise10 | wine | LossHigh | 3 | 0.984 | [+0.477, +0.494] | 0.000 |
| distill-lightgbm-noise10-tgtteacher | adult | Influence | 3 | 0.448 | [-0.074, -0.038] | 0.044 |
| distill-lightgbm-noise10-tgtteacher | adult | LissaInfluence | 3 | 0.747 | [+0.202, +0.284] | 0.009 |
| distill-lightgbm-noise10-tgtteacher | covertype | Influence | 3 | 0.523 | [-0.027, +0.086] | 0.560 |
| distill-lightgbm-noise10-tgtteacher | covertype | LissaInfluence | 3 | 0.924 | [+0.416, +0.434] | 0.000 |
| distill-lightgbm-noise10-tgtteacher | housing | Influence | 3 | 0.509 | [-0.020, +0.051] | 0.725 |
| distill-lightgbm-noise10-tgtteacher | housing | LissaInfluence | 3 | 0.506 | [-0.006, +0.020] | 0.511 |
| distill-lightgbm-noise10-tgtteacher | wine | Influence | 3 | 0.473 | [-0.101, +0.013] | 0.550 |
| distill-lightgbm-noise10-tgtteacher | wine | LissaInfluence | 3 | 0.533 | [-0.049, +0.149] | 0.639 |
| models-catboost-noise10 | adult | CatBoostLFC | 3 | 0.748 | [+0.220, +0.305] | 0.013 |
| models-catboost-noise10 | adult | DataOOB | 3 | 0.896 | [+0.389, +0.405] | 0.000 |
| models-catboost-noise10 | adult | KNNShapley | 3 | 0.878 | [+0.368, +0.399] | 0.001 |
| models-catboost-noise10 | adult | LOO | 3 | 0.524 | [+0.000, +0.051] | 0.256 |
| models-catboost-noise10 | adult | LossHigh | 3 | 0.917 | [+0.415, +0.419] | 0.000 |
| models-catboost-noise10 | covertype | DataOOB | 3 | 0.950 | [+0.442, +0.459] | 0.000 |
| models-catboost-noise10 | covertype | KNNShapley | 3 | 0.913 | [+0.409, +0.417] | 0.000 |
| models-catboost-noise10 | covertype | LOO | 3 | 0.527 | [+0.021, +0.031] | 0.013 |
| models-catboost-noise10 | covertype | LossHigh | 3 | 0.905 | [+0.390, +0.417] | 0.000 |
| models-catboost-noise10 | housing | CatBoostLFC | 3 | 0.505 | [-0.002, +0.015] | 0.467 |
| models-catboost-noise10 | housing | DataOOB | 3 | 0.998 | [+0.497, +0.499] | 0.000 |
| models-catboost-noise10 | housing | LOO | 3 | 0.517 | [+0.013, +0.020] | 0.015 |
| models-catboost-noise10 | housing | LossHigh | 3 | 0.996 | [+0.495, +0.497] | 0.000 |
| models-catboost-noise10 | wine | CatBoostLFC | 3 | 0.524 | [-0.020, +0.064] | 0.426 |
| models-catboost-noise10 | wine | DataOOB | 3 | 0.984 | [+0.477, +0.494] | 0.000 |
| models-catboost-noise10 | wine | LOO | 3 | 0.508 | [-0.015, +0.029] | 0.608 |
| models-catboost-noise10 | wine | LossHigh | 3 | 0.978 | [+0.474, +0.485] | 0.000 |
| models-lightgbm-noise10 | adult | BoostIn | 3 | 0.829 | [+0.297, +0.350] | 0.002 |
| models-lightgbm-noise10 | adult | DataOOB | 3 | 0.896 | [+0.389, +0.405] | 0.000 |
| models-lightgbm-noise10 | adult | KNNShapley | 3 | 0.878 | [+0.368, +0.399] | 0.001 |
| models-lightgbm-noise10 | adult | LOO | 3 | 0.508 | [-0.001, +0.024] | 0.465 |
| models-lightgbm-noise10 | adult | LossHigh | 3 | 0.889 | [+0.377, +0.410] | 0.001 |
| models-lightgbm-noise10 | covertype | BoostIn | 3 | 0.908 | [+0.394, +0.430] | 0.001 |
| models-lightgbm-noise10 | covertype | DataOOB | 3 | 0.950 | [+0.442, +0.459] | 0.000 |
| models-lightgbm-noise10 | covertype | KNNShapley | 3 | 0.913 | [+0.409, +0.417] | 0.000 |
| models-lightgbm-noise10 | covertype | LOO | 3 | 0.489 | [-0.018, -0.001] | 0.157 |
| models-lightgbm-noise10 | covertype | LossHigh | 3 | 0.826 | [+0.288, +0.358] | 0.004 |
| models-lightgbm-noise10 | housing | BoostIn | 3 | 0.553 | [+0.037, +0.064] | 0.023 |
| models-lightgbm-noise10 | housing | DataOOB | 3 | 0.998 | [+0.497, +0.499] | 0.000 |
| models-lightgbm-noise10 | housing | LOO | 3 | 0.558 | [+0.050, +0.066] | 0.006 |
| models-lightgbm-noise10 | housing | LossHigh | 3 | 0.997 | [+0.497, +0.498] | 0.000 |
| models-lightgbm-noise10 | wine | BoostIn | 3 | 0.547 | [-0.060, +0.170] | 0.557 |
| models-lightgbm-noise10 | wine | DataOOB | 3 | 0.984 | [+0.477, +0.494] | 0.000 |
| models-lightgbm-noise10 | wine | LOO | 3 | 0.536 | [-0.008, +0.068] | 0.258 |
| models-lightgbm-noise10 | wine | LossHigh | 3 | 0.983 | [+0.476, +0.491] | 0.000 |
| models-random_forest-noise10 | adult | DataOOB | 3 | 0.896 | [+0.389, +0.405] | 0.000 |
| models-random_forest-noise10 | adult | KNNShapley | 3 | 0.878 | [+0.368, +0.399] | 0.001 |
| models-random_forest-noise10 | adult | LOO | 3 | 0.494 | [-0.034, +0.014] | 0.724 |
| models-random_forest-noise10 | adult | LossHigh | 3 | 0.930 | [+0.426, +0.433] | 0.000 |
| models-random_forest-noise10 | covertype | DataOOB | 3 | 0.950 | [+0.442, +0.459] | 0.000 |
| models-random_forest-noise10 | covertype | KNNShapley | 3 | 0.913 | [+0.409, +0.417] | 0.000 |
| models-random_forest-noise10 | covertype | LOO | 3 | 0.471 | [-0.058, -0.014] | 0.186 |
| models-random_forest-noise10 | covertype | LossHigh | 3 | 0.933 | [+0.423, +0.440] | 0.000 |
| models-random_forest-noise10 | housing | DataOOB | 3 | 0.998 | [+0.497, +0.499] | 0.000 |
| models-random_forest-noise10 | housing | LOO | 3 | 0.531 | [+0.025, +0.041] | 0.025 |
| models-random_forest-noise10 | housing | LossHigh | 3 | 0.996 | [+0.495, +0.497] | 0.000 |
| models-random_forest-noise10 | wine | DataOOB | 3 | 0.984 | [+0.477, +0.494] | 0.000 |
| models-random_forest-noise10 | wine | LOO | 3 | 0.541 | [+0.009, +0.069] | 0.145 |
| models-random_forest-noise10 | wine | LossHigh | 3 | 0.975 | [+0.463, +0.492] | 0.000 |
| models-xgboost-noise10 | adult | DataOOB | 3 | 0.896 | [+0.389, +0.405] | 0.000 |
| models-xgboost-noise10 | adult | KNNShapley | 3 | 0.878 | [+0.368, +0.399] | 0.001 |
| models-xgboost-noise10 | adult | LOO | 3 | 0.508 | [-0.018, +0.034] | 0.636 |
| models-xgboost-noise10 | adult | LossHigh | 3 | 0.827 | [+0.315, +0.334] | 0.000 |
| models-xgboost-noise10 | covertype | DataOOB | 3 | 0.950 | [+0.442, +0.459] | 0.000 |
| models-xgboost-noise10 | covertype | KNNShapley | 3 | 0.913 | [+0.409, +0.417] | 0.000 |
| models-xgboost-noise10 | covertype | LOO | 3 | 0.502 | [-0.043, +0.042] | 0.937 |
| models-xgboost-noise10 | covertype | LossHigh | 3 | 0.919 | [+0.402, +0.429] | 0.000 |
| models-xgboost-noise10 | housing | DataOOB | 3 | 0.998 | [+0.497, +0.499] | 0.000 |
| models-xgboost-noise10 | housing | LOO | 3 | 0.527 | [+0.015, +0.036] | 0.046 |
| models-xgboost-noise10 | housing | LossHigh | 3 | 0.807 | [+0.302, +0.310] | 0.000 |
| models-xgboost-noise10 | wine | DataOOB | 3 | 0.984 | [+0.477, +0.494] | 0.000 |
| models-xgboost-noise10 | wine | LOO | 3 | 0.536 | [+0.001, +0.065] | 0.195 |
| models-xgboost-noise10 | wine | LossHigh | 3 | 0.573 | [+0.060, +0.085] | 0.010 |
| noise10 | adult | DataOOB | 5 | 0.888 | [+0.376, +0.398] | 0.000 |
| noise10 | adult | Influence | 5 | 0.519 | [-0.006, +0.044] | 0.266 |
| noise10 | adult | KNNShapley | 5 | 0.881 | [+0.371, +0.391] | 0.000 |
| noise10 | adult | LOO | 5 | 0.512 | [-0.007, +0.030] | 0.352 |
| noise10 | adult | LissaInfluence | 5 | 0.879 | [+0.363, +0.394] | 0.000 |
| noise10 | adult | LossHigh | 5 | 0.915 | [+0.398, +0.428] | 0.000 |
| noise10 | covertype | DataOOB | 5 | 0.950 | [+0.444, +0.456] | 0.000 |
| noise10 | covertype | Influence | 5 | 0.498 | [-0.035, +0.031] | 0.927 |
| noise10 | covertype | KNNShapley | 5 | 0.916 | [+0.411, +0.421] | 0.000 |
| noise10 | covertype | LOO | 5 | 0.498 | [-0.006, +0.003] | 0.497 |
| noise10 | covertype | LissaInfluence | 5 | 0.851 | [+0.296, +0.403] | 0.000 |
| noise10 | covertype | LossHigh | 5 | 0.933 | [+0.415, +0.451] | 0.000 |
| noise10 | housing | DataOOB | 5 | 0.998 | [+0.497, +0.498] | 0.000 |
| noise10 | housing | Influence | 5 | 0.540 | [+0.012, +0.063] | 0.063 |
| noise10 | housing | LOO | 5 | 0.514 | [+0.005, +0.021] | 0.051 |
| noise10 | housing | LissaInfluence | 5 | 0.539 | [+0.013, +0.065] | 0.057 |
| noise10 | housing | LossHigh | 5 | 0.998 | [+0.497, +0.498] | 0.000 |
| noise10 | wine | DataOOB | 5 | 0.985 | [+0.479, +0.491] | 0.000 |
| noise10 | wine | Influence | 5 | 0.519 | [-0.009, +0.063] | 0.431 |
| noise10 | wine | LOO | 5 | 0.566 | [+0.040, +0.091] | 0.010 |
| noise10 | wine | LissaInfluence | 5 | 0.581 | [+0.019, +0.143] | 0.093 |
| noise10 | wine | LossHigh | 5 | 0.987 | [+0.480, +0.493] | 0.000 |
| noise10 | wine | TMCShapley | 5 | 0.573 | [+0.046, +0.099] | 0.009 |
| noise20 | adult | DataOOB | 3 | 0.857 | [+0.342, +0.372] | 0.001 |
| noise20 | adult | Influence | 3 | 0.535 | [-0.003, +0.063] | 0.221 |
| noise20 | adult | KNNShapley | 3 | 0.877 | [+0.368, +0.386] | 0.000 |
| noise20 | adult | LissaInfluence | 3 | 0.845 | [+0.293, +0.408] | 0.009 |
| noise20 | adult | LossHigh | 3 | 0.908 | [+0.387, +0.421] | 0.001 |
| noise20 | covertype | DataOOB | 3 | 0.949 | [+0.447, +0.450] | 0.000 |
| noise20 | covertype | KNNShapley | 3 | 0.925 | [+0.420, +0.433] | 0.000 |
| noise20 | covertype | LissaInfluence | 3 | 0.915 | [+0.408, +0.423] | 0.000 |
| noise20 | covertype | LossHigh | 3 | 0.947 | [+0.438, +0.454] | 0.000 |
| noise20 | housing | DataOOB | 3 | 0.996 | [+0.496, +0.497] | 0.000 |
| noise20 | housing | Influence | 3 | 0.495 | [-0.020, +0.013] | 0.629 |
| noise20 | housing | LissaInfluence | 3 | 0.528 | [-0.007, +0.078] | 0.385 |
| noise20 | housing | LossHigh | 3 | 0.997 | [+0.495, +0.498] | 0.000 |
| noise20 | wine | DataOOB | 3 | 0.973 | [+0.468, +0.479] | 0.000 |
| noise20 | wine | Influence | 3 | 0.496 | [-0.033, +0.012] | 0.812 |
| noise20 | wine | LissaInfluence | 3 | 0.558 | [+0.025, +0.078] | 0.072 |
| noise20 | wine | LossHigh | 3 | 0.980 | [+0.472, +0.486] | 0.000 |
| noise5 | adult | DataOOB | 3 | 0.918 | [+0.408, +0.438] | 0.001 |
| noise5 | adult | Influence | 3 | 0.506 | [-0.025, +0.045] | 0.799 |
| noise5 | adult | KNNShapley | 3 | 0.871 | [+0.360, +0.381] | 0.000 |
| noise5 | adult | LissaInfluence | 3 | 0.838 | [+0.269, +0.402] | 0.013 |
| noise5 | adult | LossHigh | 3 | 0.928 | [+0.426, +0.431] | 0.000 |
| noise5 | covertype | DataOOB | 3 | 0.959 | [+0.443, +0.471] | 0.000 |
| noise5 | covertype | KNNShapley | 3 | 0.927 | [+0.417, +0.443] | 0.000 |
| noise5 | covertype | LissaInfluence | 3 | 0.792 | [+0.188, +0.393] | 0.039 |
| noise5 | covertype | LossHigh | 3 | 0.952 | [+0.442, +0.462] | 0.000 |
| noise5 | housing | DataOOB | 3 | 0.998 | [+0.497, +0.499] | 0.000 |
| noise5 | housing | Influence | 3 | 0.508 | [-0.021, +0.035] | 0.658 |
| noise5 | housing | LissaInfluence | 3 | 0.582 | [+0.012, +0.130] | 0.149 |
| noise5 | housing | LossHigh | 3 | 0.998 | [+0.497, +0.499] | 0.000 |
| noise5 | wine | DataOOB | 3 | 0.982 | [+0.463, +0.492] | 0.000 |
| noise5 | wine | Influence | 3 | 0.535 | [+0.017, +0.054] | 0.080 |
| noise5 | wine | LissaInfluence | 3 | 0.575 | [-0.027, +0.161] | 0.304 |
| noise5 | wine | LossHigh | 3 | 0.980 | [+0.464, +0.492] | 0.000 |
| sweep-base | adult | DataOOB | 3 | 0.896 | [+0.389, +0.405] | 0.000 |
| sweep-base | adult | Influence | 3 | 0.524 | [-0.019, +0.055] | 0.386 |
| sweep-base | adult | KNNShapley | 3 | 0.878 | [+0.368, +0.399] | 0.001 |
| sweep-base | adult | LOO | 3 | 0.527 | [+0.011, +0.043] | 0.100 |
| sweep-base | adult | LissaInfluence | 3 | 0.880 | [+0.366, +0.398] | 0.001 |
| sweep-base | adult | LossHigh | 3 | 0.925 | [+0.415, +0.433] | 0.000 |
| sweep-batch_size-0 | adult | DataOOB | 3 | 0.896 | [+0.389, +0.405] | 0.000 |
| sweep-batch_size-0 | adult | Influence | 3 | 0.547 | [+0.005, +0.089] | 0.193 |
| sweep-batch_size-0 | adult | KNNShapley | 3 | 0.878 | [+0.368, +0.399] | 0.001 |
| sweep-batch_size-0 | adult | LOO | 3 | 0.549 | [+0.026, +0.083] | 0.101 |
| sweep-batch_size-0 | adult | LissaInfluence | 3 | 0.920 | [+0.412, +0.434] | 0.000 |
| sweep-batch_size-0 | adult | LossHigh | 3 | 0.922 | [+0.414, +0.435] | 0.000 |
| sweep-fit_mode-overfit | adult | DataOOB | 3 | 0.896 | [+0.389, +0.405] | 0.000 |
| sweep-fit_mode-overfit | adult | KNNShapley | 3 | 0.878 | [+0.368, +0.399] | 0.001 |
| sweep-fit_mode-overfit | adult | LOO | 3 | 0.517 | [-0.012, +0.033] | 0.357 |
| sweep-fit_mode-overfit | adult | LissaInfluence | 3 | 0.793 | [+0.252, +0.329] | 0.006 |
| sweep-fit_mode-overfit | adult | LossHigh | 3 | 0.891 | [+0.376, +0.400] | 0.000 |
| sweep-fit_mode-underfit | adult | DataOOB | 3 | 0.896 | [+0.389, +0.405] | 0.000 |
| sweep-fit_mode-underfit | adult | Influence | 3 | 0.693 | [+0.153, +0.218] | 0.011 |
| sweep-fit_mode-underfit | adult | KNNShapley | 3 | 0.878 | [+0.368, +0.399] | 0.001 |
| sweep-fit_mode-underfit | adult | LOO | 3 | 0.518 | [+0.000, +0.045] | 0.324 |
| sweep-fit_mode-underfit | adult | LissaInfluence | 3 | 0.834 | [+0.272, +0.390] | 0.010 |
| sweep-fit_mode-underfit | adult | LossHigh | 3 | 0.796 | [+0.248, +0.340] | 0.008 |
| sweep-sample_scale-0.1 | adult | DataOOB | 3 | 0.857 | [+0.336, +0.373] | 0.001 |
| sweep-sample_scale-0.1 | adult | Influence | 3 | 0.528 | [-0.132, +0.176] | 0.780 |
| sweep-sample_scale-0.1 | adult | KNNShapley | 3 | 0.816 | [+0.272, +0.368] | 0.008 |
| sweep-sample_scale-0.1 | adult | LOO | 3 | 0.617 | [+0.031, +0.243] | 0.209 |
| sweep-sample_scale-0.1 | adult | LissaInfluence | 3 | 0.860 | [+0.287, +0.419] | 0.011 |
| sweep-sample_scale-0.1 | adult | LossHigh | 3 | 0.885 | [+0.356, +0.431] | 0.004 |
| sweep-sample_scale-0.3 | adult | DataOOB | 3 | 0.900 | [+0.378, +0.423] | 0.001 |
| sweep-sample_scale-0.3 | adult | Influence | 3 | 0.509 | [-0.058, +0.109] | 0.875 |
| sweep-sample_scale-0.3 | adult | KNNShapley | 3 | 0.861 | [+0.348, +0.375] | 0.000 |
| sweep-sample_scale-0.3 | adult | LOO | 3 | 0.530 | [-0.061, +0.124] | 0.631 |
| sweep-sample_scale-0.3 | adult | LissaInfluence | 3 | 0.857 | [+0.269, +0.407] | 0.015 |
| sweep-sample_scale-0.3 | adult | LossHigh | 3 | 0.911 | [+0.404, +0.418] | 0.000 |
| sweep-valuation_epochs-10 | adult | LOO | 3 | 0.502 | [-0.022, +0.044] | 0.947 |
| sweep-valuation_epochs-60 | adult | LOO | 3 | 0.494 | [-0.025, +0.032] | 0.785 |
| sysnoise10 | adult | DataOOB | 3 | 0.902 | [+0.395, +0.409] | 0.000 |
| sysnoise10 | adult | Influence | 3 | 0.512 | [-0.006, +0.041] | 0.503 |
| sysnoise10 | adult | KNNShapley | 3 | 0.947 | [+0.445, +0.451] | 0.000 |
| sysnoise10 | adult | LissaInfluence | 3 | 0.964 | [+0.459, +0.467] | 0.000 |
| sysnoise10 | adult | LossHigh | 3 | 0.922 | [+0.411, +0.429] | 0.000 |
| sysnoise10 | covertype | DataOOB | 3 | 0.729 | [+0.217, +0.245] | 0.001 |
| sysnoise10 | covertype | KNNShapley | 3 | 0.778 | [+0.257, +0.292] | 0.001 |
| sysnoise10 | covertype | LissaInfluence | 3 | 0.613 | [-0.397, +0.424] | 0.703 |
| sysnoise10 | covertype | LossHigh | 3 | 0.773 | [+0.248, +0.292] | 0.002 |
| sysnoise10 | housing | DataOOB | 3 | 0.582 | [+0.054, +0.126] | 0.067 |
| sysnoise10 | housing | Influence | 3 | 0.615 | [+0.048, +0.184] | 0.099 |
| sysnoise10 | housing | LissaInfluence | 3 | 0.928 | [+0.412, +0.439] | 0.000 |
| sysnoise10 | housing | LossHigh | 3 | 0.859 | [+0.346, +0.370] | 0.000 |
| sysnoise10 | wine | DataOOB | 3 | 0.635 | [+0.113, +0.150] | 0.007 |
| sysnoise10 | wine | Influence | 3 | 0.518 | [-0.182, +0.182] | 0.880 |
| sysnoise10 | wine | LissaInfluence | 3 | 0.899 | [+0.366, +0.454] | 0.005 |
| sysnoise10 | wine | LossHigh | 3 | 0.835 | [+0.291, +0.418] | 0.015 |
| sysnoise20 | adult | DataOOB | 3 | 0.804 | [+0.296, +0.308] | 0.000 |
| sysnoise20 | adult | Influence | 3 | 0.546 | [+0.008, +0.092] | 0.204 |
| sysnoise20 | adult | KNNShapley | 3 | 0.940 | [+0.436, +0.444] | 0.000 |
| sysnoise20 | adult | LissaInfluence | 3 | 0.929 | [+0.373, +0.466] | 0.004 |
| sysnoise20 | adult | LossHigh | 3 | 0.850 | [+0.333, +0.365] | 0.001 |
| sysnoise20 | covertype | DataOOB | 3 | 0.557 | [+0.048, +0.070] | 0.014 |
| sysnoise20 | covertype | KNNShapley | 3 | 0.752 | [+0.234, +0.265] | 0.001 |
| sysnoise20 | covertype | LissaInfluence | 3 | 0.895 | [+0.388, +0.399] | 0.000 |
| sysnoise20 | covertype | LossHigh | 3 | 0.687 | [+0.154, +0.247] | 0.025 |
| sysnoise20 | housing | DataOOB | 3 | 0.667 | [+0.127, +0.208] | 0.019 |
| sysnoise20 | housing | Influence | 3 | 0.607 | [+0.010, +0.207] | 0.203 |
| sysnoise20 | housing | LissaInfluence | 3 | 0.906 | [+0.320, +0.476] | 0.013 |
| sysnoise20 | housing | LossHigh | 3 | 0.776 | [+0.162, +0.392] | 0.053 |
| sysnoise20 | wine | DataOOB | 3 | 0.587 | [+0.040, +0.121] | 0.069 |
| sysnoise20 | wine | Influence | 3 | 0.654 | [-0.065, +0.322] | 0.311 |
| sysnoise20 | wine | LissaInfluence | 3 | 0.957 | [+0.442, +0.478] | 0.001 |
| sysnoise20 | wine | LossHigh | 3 | 0.849 | [+0.314, +0.384] | 0.003 |
| sysnoise5 | adult | DataOOB | 3 | 0.919 | [+0.406, +0.426] | 0.000 |
| sysnoise5 | adult | Influence | 3 | 0.519 | [-0.011, +0.041] | 0.343 |
| sysnoise5 | adult | KNNShapley | 3 | 0.943 | [+0.438, +0.448] | 0.000 |
| sysnoise5 | adult | LissaInfluence | 3 | 0.939 | [+0.407, +0.474] | 0.002 |
| sysnoise5 | adult | LossHigh | 3 | 0.930 | [+0.420, +0.446] | 0.000 |
| sysnoise5 | covertype | DataOOB | 3 | 0.818 | [+0.295, +0.341] | 0.002 |
| sysnoise5 | covertype | KNNShapley | 3 | 0.793 | [+0.260, +0.316] | 0.003 |
| sysnoise5 | covertype | LissaInfluence | 3 | 0.724 | [-0.130, +0.416] | 0.334 |
| sysnoise5 | covertype | LossHigh | 3 | 0.824 | [+0.289, +0.350] | 0.003 |
| sysnoise5 | housing | DataOOB | 3 | 0.486 | [-0.080, +0.025] | 0.710 |
| sysnoise5 | housing | Influence | 3 | 0.651 | [+0.065, +0.267] | 0.129 |
| sysnoise5 | housing | LissaInfluence | 3 | 0.927 | [+0.390, +0.446] | 0.002 |
| sysnoise5 | housing | LossHigh | 3 | 0.913 | [+0.402, +0.429] | 0.000 |
| sysnoise5 | wine | DataOOB | 3 | 0.676 | [+0.077, +0.277] | 0.093 |
| sysnoise5 | wine | Influence | 3 | 0.604 | [+0.082, +0.148] | 0.041 |
| sysnoise5 | wine | LissaInfluence | 3 | 0.822 | [+0.267, +0.424] | 0.024 |
| sysnoise5 | wine | LossHigh | 3 | 0.784 | [+0.256, +0.330] | 0.006 |

# Cross-study comparisons (detection AUC, paired by seed)

| comparison | dataset | method | n | AUC A | AUC B | A − B, 95 % CI | p |
|---|---|---|---|---|---|---|---|
| lightgbm - MLP | adult | LOO | 3 | 0.508 | 0.527 | -0.020 [-0.043, +0.014] | 0.372 |
| lightgbm - MLP | adult | LossHigh | 3 | 0.889 | 0.925 | -0.036 [-0.057, -0.005] | 0.150 |
| lightgbm - MLP | covertype | LOO | 3 | 0.489 | 0.496 | -0.007 [-0.012, -0.000] | 0.180 |
| lightgbm - MLP | covertype | LossHigh | 3 | 0.826 | 0.934 | -0.108 [-0.144, -0.059] | 0.051 |
| lightgbm - MLP | housing | LOO | 3 | 0.558 | 0.511 | +0.047 [+0.034, +0.054] | 0.018 |
| lightgbm - MLP | housing | LossHigh | 3 | 0.997 | 0.998 | -0.000 [-0.000, +0.000] | 0.575 |
| lightgbm - MLP | wine | LOO | 3 | 0.536 | 0.564 | -0.029 [-0.105, +0.048] | 0.584 |
| lightgbm - MLP | wine | LossHigh | 3 | 0.983 | 0.984 | -0.001 [-0.004, +0.001] | 0.521 |
| xgboost - MLP | adult | LOO | 3 | 0.508 | 0.527 | -0.019 [-0.046, -0.002] | 0.304 |
| xgboost - MLP | adult | LossHigh | 3 | 0.827 | 0.925 | -0.098 [-0.118, -0.082] | 0.011 |
| xgboost - MLP | covertype | LOO | 3 | 0.502 | 0.496 | +0.006 [-0.037, +0.044] | 0.826 |
| xgboost - MLP | covertype | LossHigh | 3 | 0.919 | 0.934 | -0.015 [-0.029, +0.009] | 0.334 |
| xgboost - MLP | housing | LOO | 3 | 0.527 | 0.511 | +0.015 [+0.001, +0.033] | 0.247 |
| xgboost - MLP | housing | LossHigh | 3 | 0.807 | 0.998 | -0.191 [-0.196, -0.187] | 0.000 |
| xgboost - MLP | wine | LOO | 3 | 0.536 | 0.564 | -0.028 [-0.076, +0.024] | 0.434 |
| xgboost - MLP | wine | LossHigh | 3 | 0.573 | 0.984 | -0.412 [-0.435, -0.391] | 0.001 |
| catboost - MLP | adult | LOO | 3 | 0.524 | 0.527 | -0.004 [-0.043, +0.041] | 0.895 |
| catboost - MLP | adult | LossHigh | 3 | 0.917 | 0.925 | -0.008 [-0.016, +0.004] | 0.313 |
| catboost - MLP | covertype | LOO | 3 | 0.527 | 0.496 | +0.031 [+0.022, +0.037] | 0.020 |
| catboost - MLP | covertype | LossHigh | 3 | 0.905 | 0.934 | -0.029 [-0.042, -0.009] | 0.104 |
| catboost - MLP | housing | LOO | 3 | 0.517 | 0.511 | +0.005 [-0.011, +0.024] | 0.661 |
| catboost - MLP | housing | LossHigh | 3 | 0.996 | 0.998 | -0.001 [-0.002, -0.000] | 0.114 |
| catboost - MLP | wine | LOO | 3 | 0.508 | 0.564 | -0.056 [-0.112, -0.010] | 0.197 |
| catboost - MLP | wine | LossHigh | 3 | 0.978 | 0.984 | -0.006 [-0.010, -0.001] | 0.146 |
| random_forest - MLP | adult | LOO | 3 | 0.494 | 0.527 | -0.033 [-0.077, +0.004] | 0.296 |
| random_forest - MLP | adult | LossHigh | 3 | 0.930 | 0.925 | +0.005 [-0.001, +0.011] | 0.254 |
| random_forest - MLP | covertype | LOO | 3 | 0.471 | 0.496 | -0.025 [-0.055, -0.009] | 0.224 |
| random_forest - MLP | covertype | LossHigh | 3 | 0.933 | 0.934 | -0.002 [-0.013, +0.018] | 0.890 |
| random_forest - MLP | housing | LOO | 3 | 0.531 | 0.511 | +0.019 [+0.002, +0.030] | 0.160 |
| random_forest - MLP | housing | LossHigh | 3 | 0.996 | 0.998 | -0.001 [-0.002, -0.000] | 0.187 |
| random_forest - MLP | wine | LOO | 3 | 0.541 | 0.564 | -0.023 [-0.068, +0.050] | 0.592 |
| random_forest - MLP | wine | LossHigh | 3 | 0.975 | 0.984 | -0.009 [-0.013, -0.003] | 0.086 |
| student of lightgbm - MLP direct | adult | Influence | 3 | 0.532 | 0.524 | +0.008 [-0.030, +0.074] | 0.837 |
| student of lightgbm - MLP direct | adult | LissaInfluence | 3 | 0.760 | 0.880 | -0.120 [-0.155, -0.098] | 0.021 |
| student of lightgbm - MLP direct | adult | LossHigh | 3 | 0.878 | 0.925 | -0.047 [-0.053, -0.044] | 0.004 |
| student of lightgbm - MLP direct | covertype | Influence | 3 | 0.517 | 0.496 | +0.020 [-0.054, +0.065] | 0.640 |
| student of lightgbm - MLP direct | covertype | LissaInfluence | 3 | 0.788 | 0.855 | -0.067 [-0.222, +0.025] | 0.477 |
| student of lightgbm - MLP direct | covertype | LossHigh | 3 | 0.944 | 0.934 | +0.010 [-0.014, +0.040] | 0.606 |
| student of lightgbm - MLP direct | housing | Influence | 3 | 0.474 | 0.530 | -0.056 [-0.103, -0.020] | 0.149 |
| student of lightgbm - MLP direct | housing | LissaInfluence | 3 | 0.507 | 0.561 | -0.054 [-0.076, -0.028] | 0.063 |
| student of lightgbm - MLP direct | housing | LossHigh | 3 | 0.998 | 0.998 | +0.001 [+0.000, +0.001] | 0.007 |
| student of lightgbm - MLP direct | wine | Influence | 3 | 0.463 | 0.532 | -0.069 [-0.124, -0.034] | 0.129 |
| student of lightgbm - MLP direct | wine | LissaInfluence | 3 | 0.555 | 0.606 | -0.051 [-0.119, +0.001] | 0.287 |
| student of lightgbm - MLP direct | wine | LossHigh | 3 | 0.984 | 0.984 | -0.000 [-0.001, +0.001] | 0.754 |
| student of catboost - MLP direct | adult | Influence | 3 | 0.537 | 0.524 | +0.013 [-0.049, +0.089] | 0.778 |
| student of catboost - MLP direct | adult | LissaInfluence | 3 | 0.764 | 0.880 | -0.116 [-0.136, -0.098] | 0.009 |
| student of catboost - MLP direct | adult | LossHigh | 3 | 0.870 | 0.925 | -0.055 [-0.063, -0.049] | 0.006 |
| student of catboost - MLP direct | covertype | Influence | 3 | 0.501 | 0.496 | +0.005 [-0.029, +0.027] | 0.805 |
| student of catboost - MLP direct | covertype | LissaInfluence | 3 | 0.878 | 0.855 | +0.023 [-0.023, +0.087] | 0.560 |
| student of catboost - MLP direct | covertype | LossHigh | 3 | 0.939 | 0.934 | +0.005 [-0.007, +0.028] | 0.732 |
| student of catboost - MLP direct | housing | Influence | 3 | 0.535 | 0.530 | +0.005 [-0.005, +0.016] | 0.483 |
| student of catboost - MLP direct | housing | LissaInfluence | 3 | 0.546 | 0.561 | -0.015 [-0.064, +0.010] | 0.596 |
| student of catboost - MLP direct | housing | LossHigh | 3 | 0.995 | 0.998 | -0.003 [-0.004, -0.001] | 0.130 |
| student of catboost - MLP direct | wine | Influence | 3 | 0.446 | 0.532 | -0.086 [-0.107, -0.047] | 0.048 |
| student of catboost - MLP direct | wine | LissaInfluence | 3 | 0.586 | 0.606 | -0.020 [-0.125, +0.058] | 0.746 |
| student of catboost - MLP direct | wine | LossHigh | 3 | 0.978 | 0.984 | -0.006 [-0.011, -0.002] | 0.123 |
| linear - MLP (damping 1e-06) | adult | Influence | 3 | 0.781 | 0.543 | +0.238 [+0.163, +0.280] | 0.024 |
| linear - MLP (damping 1e-06) | adult | LissaInfluence | 3 | 0.854 | 0.852 | +0.002 [-0.046, +0.051] | 0.945 |
| linear - MLP (damping 1e-06) | housing | Influence | 3 | 0.532 | 0.521 | +0.011 [-0.085, +0.060] | 0.842 |
| linear - MLP (damping 1e-06) | housing | LissaInfluence | 3 | 0.548 | 0.541 | +0.007 [-0.007, +0.032] | 0.607 |
| linear - MLP (damping 1e-06) | wine | Influence | 3 | 0.577 | 0.517 | +0.060 [-0.025, +0.147] | 0.350 |
| linear - MLP (damping 1e-06) | wine | LissaInfluence | 3 | 0.592 | 0.620 | -0.028 [-0.119, +0.042] | 0.613 |
| linear - MLP (damping 0.0001) | adult | Influence | 3 | 0.786 | 0.498 | +0.288 [+0.251, +0.313] | 0.004 |
| linear - MLP (damping 0.0001) | adult | LissaInfluence | 3 | 0.854 | 0.852 | +0.002 [-0.046, +0.051] | 0.946 |
| linear - MLP (damping 0.0001) | housing | Influence | 3 | 0.532 | 0.530 | +0.001 [-0.021, +0.018] | 0.930 |
| linear - MLP (damping 0.0001) | housing | LissaInfluence | 3 | 0.548 | 0.541 | +0.007 [-0.007, +0.032] | 0.607 |
| linear - MLP (damping 0.0001) | wine | Influence | 3 | 0.577 | 0.532 | +0.045 [-0.019, +0.124] | 0.391 |
| linear - MLP (damping 0.0001) | wine | LissaInfluence | 3 | 0.592 | 0.620 | -0.028 [-0.119, +0.042] | 0.613 |
| linear - MLP (damping 0.01) | adult | Influence | 3 | 0.833 | 0.696 | +0.137 [+0.120, +0.156] | 0.006 |
| linear - MLP (damping 0.01) | adult | LissaInfluence | 3 | 0.854 | 0.853 | +0.001 [-0.047, +0.051] | 0.964 |
| linear - MLP (damping 0.01) | housing | Influence | 3 | 0.532 | 0.505 | +0.027 [+0.001, +0.074] | 0.362 |
| linear - MLP (damping 0.01) | housing | LissaInfluence | 3 | 0.549 | 0.541 | +0.008 [-0.006, +0.032] | 0.575 |
| linear - MLP (damping 0.01) | wine | Influence | 3 | 0.579 | 0.498 | +0.081 [-0.012, +0.138] | 0.228 |
| linear - MLP (damping 0.01) | wine | LissaInfluence | 3 | 0.592 | 0.620 | -0.028 [-0.118, +0.042] | 0.611 |
| linear - MLP (damping 1) | adult | Influence | 3 | 0.841 | 0.892 | -0.050 [-0.083, -0.028] | 0.092 |
| linear - MLP (damping 1) | adult | LissaInfluence | 3 | 0.841 | 0.877 | -0.035 [-0.086, -0.008] | 0.301 |
| linear - MLP (damping 1) | covertype | Influence | 3 | 0.793 | 0.861 | -0.068 [-0.135, -0.006] | 0.210 |
| linear - MLP (damping 1) | housing | Influence | 3 | 0.551 | 0.538 | +0.013 [+0.008, +0.018] | 0.044 |
| linear - MLP (damping 1) | housing | LissaInfluence | 3 | 0.545 | 0.540 | +0.005 [-0.009, +0.025] | 0.675 |
| linear - MLP (damping 1) | wine | Influence | 3 | 0.588 | 0.621 | -0.033 [-0.112, +0.029] | 0.507 |
| linear - MLP (damping 1) | wine | LissaInfluence | 3 | 0.592 | 0.619 | -0.027 [-0.111, +0.053] | 0.620 |
| systematic - random noise 5 % | adult | KNNShapley | 3 | 0.943 | 0.871 | +0.071 [+0.066, +0.082] | 0.006 |
| systematic - random noise 5 % | adult | DataOOB | 3 | 0.919 | 0.918 | +0.000 [-0.014, +0.018] | 0.965 |
| systematic - random noise 5 % | adult | Influence | 3 | 0.519 | 0.506 | +0.013 [-0.005, +0.030] | 0.321 |
| systematic - random noise 5 % | adult | LissaInfluence | 3 | 0.939 | 0.838 | +0.101 [+0.072, +0.138] | 0.035 |
| systematic - random noise 5 % | adult | LossHigh | 3 | 0.930 | 0.928 | +0.002 [-0.007, +0.019] | 0.819 |
| systematic - random noise 5 % | covertype | KNNShapley | 3 | 0.793 | 0.927 | -0.134 [-0.157, -0.117] | 0.008 |
| systematic - random noise 5 % | covertype | DataOOB | 3 | 0.818 | 0.959 | -0.141 [-0.167, -0.125] | 0.009 |
| systematic - random noise 5 % | covertype | LissaInfluence | 3 | 0.724 | 0.792 | -0.068 [-0.523, +0.228] | 0.795 |
| systematic - random noise 5 % | covertype | LossHigh | 3 | 0.824 | 0.952 | -0.128 [-0.163, -0.092] | 0.025 |
| systematic - random noise 5 % | housing | DataOOB | 3 | 0.486 | 0.998 | -0.512 [-0.579, -0.472] | 0.004 |
| systematic - random noise 5 % | housing | Influence | 3 | 0.651 | 0.508 | +0.142 [+0.085, +0.255] | 0.128 |
| systematic - random noise 5 % | housing | LissaInfluence | 3 | 0.927 | 0.582 | +0.345 [+0.316, +0.378] | 0.003 |
| systematic - random noise 5 % | housing | LossHigh | 3 | 0.913 | 0.998 | -0.085 [-0.095, -0.070] | 0.008 |
| systematic - random noise 5 % | wine | DataOOB | 3 | 0.676 | 0.982 | -0.306 [-0.414, -0.215] | 0.034 |
| systematic - random noise 5 % | wine | Influence | 3 | 0.604 | 0.535 | +0.070 [+0.048, +0.095] | 0.036 |
| systematic - random noise 5 % | wine | LissaInfluence | 3 | 0.822 | 0.575 | +0.247 [+0.114, +0.333] | 0.067 |
| systematic - random noise 5 % | wine | LossHigh | 3 | 0.784 | 0.980 | -0.196 [-0.229, -0.134] | 0.024 |
| systematic - random noise 10 % | adult | KNNShapley | 3 | 0.947 | 0.878 | +0.069 [+0.052, +0.077] | 0.014 |
| systematic - random noise 10 % | adult | DataOOB | 3 | 0.902 | 0.896 | +0.006 [+0.001, +0.012] | 0.216 |
| systematic - random noise 10 % | adult | Influence | 3 | 0.512 | 0.524 | -0.013 [-0.043, +0.019] | 0.553 |
| systematic - random noise 10 % | adult | LissaInfluence | 3 | 0.964 | 0.880 | +0.084 [+0.061, +0.101] | 0.019 |
| systematic - random noise 10 % | adult | LossHigh | 3 | 0.922 | 0.925 | -0.003 [-0.016, +0.014] | 0.744 |
| systematic - random noise 10 % | covertype | KNNShapley | 3 | 0.778 | 0.913 | -0.136 [-0.157, -0.118] | 0.007 |
| systematic - random noise 10 % | covertype | DataOOB | 3 | 0.729 | 0.950 | -0.221 [-0.225, -0.214] | 0.000 |
| systematic - random noise 10 % | covertype | LissaInfluence | 3 | 0.613 | 0.855 | -0.243 [-0.773, +0.043] | 0.457 |
| systematic - random noise 10 % | covertype | LossHigh | 3 | 0.773 | 0.934 | -0.161 [-0.184, -0.138] | 0.007 |
| systematic - random noise 10 % | housing | DataOOB | 3 | 0.582 | 0.998 | -0.416 [-0.444, -0.371] | 0.003 |
| systematic - random noise 10 % | housing | Influence | 3 | 0.615 | 0.530 | +0.085 [-0.007, +0.132] | 0.206 |
| systematic - random noise 10 % | housing | LissaInfluence | 3 | 0.928 | 0.561 | +0.367 [+0.339, +0.393] | 0.002 |
| systematic - random noise 10 % | housing | LossHigh | 3 | 0.859 | 0.998 | -0.138 [-0.151, -0.129] | 0.002 |
| systematic - random noise 10 % | wine | DataOOB | 3 | 0.635 | 0.984 | -0.349 [-0.381, -0.330] | 0.002 |
| systematic - random noise 10 % | wine | Influence | 3 | 0.518 | 0.532 | -0.014 [-0.288, +0.200] | 0.932 |
| systematic - random noise 10 % | wine | LissaInfluence | 3 | 0.899 | 0.606 | +0.293 [+0.207, +0.383] | 0.029 |
| systematic - random noise 10 % | wine | LossHigh | 3 | 0.835 | 0.984 | -0.149 [-0.204, -0.063] | 0.076 |
| systematic - random noise 20 % | adult | KNNShapley | 3 | 0.940 | 0.877 | +0.062 [+0.051, +0.076] | 0.015 |
| systematic - random noise 20 % | adult | DataOOB | 3 | 0.804 | 0.857 | -0.054 [-0.064, -0.046] | 0.009 |
| systematic - random noise 20 % | adult | Influence | 3 | 0.546 | 0.535 | +0.011 [-0.006, +0.028] | 0.388 |
| systematic - random noise 20 % | adult | LissaInfluence | 3 | 0.929 | 0.845 | +0.084 [+0.058, +0.114] | 0.035 |
| systematic - random noise 20 % | adult | LossHigh | 3 | 0.850 | 0.908 | -0.058 [-0.065, -0.054] | 0.003 |
| systematic - random noise 20 % | covertype | KNNShapley | 3 | 0.752 | 0.925 | -0.173 [-0.200, -0.157] | 0.006 |
| systematic - random noise 20 % | covertype | DataOOB | 3 | 0.557 | 0.949 | -0.392 [-0.402, -0.377] | 0.000 |
| systematic - random noise 20 % | covertype | LissaInfluence | 3 | 0.895 | 0.915 | -0.020 [-0.025, -0.012] | 0.041 |
| systematic - random noise 20 % | covertype | LossHigh | 3 | 0.687 | 0.947 | -0.260 [-0.288, -0.207] | 0.010 |
| systematic - random noise 20 % | housing | DataOOB | 3 | 0.667 | 0.996 | -0.329 [-0.369, -0.288] | 0.005 |
| systematic - random noise 20 % | housing | Influence | 3 | 0.607 | 0.495 | +0.112 [+0.029, +0.217] | 0.180 |
| systematic - random noise 20 % | housing | LissaInfluence | 3 | 0.906 | 0.528 | +0.378 [+0.241, +0.463] | 0.032 |
| systematic - random noise 20 % | housing | LossHigh | 3 | 0.776 | 0.997 | -0.221 [-0.335, -0.104] | 0.081 |
| systematic - random noise 20 % | wine | DataOOB | 3 | 0.587 | 0.973 | -0.386 [-0.433, -0.358] | 0.004 |
| systematic - random noise 20 % | wine | Influence | 3 | 0.654 | 0.496 | +0.158 [-0.074, +0.355] | 0.335 |
| systematic - random noise 20 % | wine | LissaInfluence | 3 | 0.957 | 0.558 | +0.399 [+0.365, +0.425] | 0.002 |
| systematic - random noise 20 % | wine | LossHigh | 3 | 0.849 | 0.980 | -0.131 [-0.168, -0.088] | 0.030 |
