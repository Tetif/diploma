| study | dataset | method | seeds | full data | metric @10 % removed | detection AUC | values, s |
|---|---|---|---|---|---|---|---|
| clean | wine | LOO | 5 | 0.4782 | 0.4700 ± 0.0258 | — | 211.1 |
| clean | wine | TMC-Shapley | 5 | 0.4782 | 0.4798 ± 0.0295 | — | 603.1 |
| clean | wine | Data-OOB | 5 | 0.4782 | 0.4874 ± 0.0221 | — | 1.0 |
| clean | wine | Influence | 5 | 0.4782 | 0.4819 ± 0.0275 | — | 0.6 |
| clean | wine | LiSSA | 5 | 0.4782 | 0.4767 ± 0.0266 | — | 0.8 |
| clean | wine | high loss | 5 | 0.4782 | 0.4862 ± 0.0255 | — | 0.0 |
| clean | wine | random | 5 | 0.4782 | 0.4761 ± 0.0274 | — | 0.0 |
| clean | housing | LOO | 5 | 44382.0854 | 44662.4793 ± 872.1531 | — | 840.5 |
| clean | housing | Data-OOB | 5 | 44382.0854 | 44834.5405 ± 669.4803 | — | 1.4 |
| clean | housing | Influence | 5 | 44382.0854 | 44739.1882 ± 1017.2091 | — | 2.5 |
| clean | housing | LiSSA | 5 | 44382.0854 | 44527.4293 ± 766.2451 | — | 1.4 |
| clean | housing | high loss | 5 | 44382.0854 | 44402.2262 ± 1211.6787 | — | 0.0 |
| clean | housing | random | 5 | 44382.0854 | 44747.8363 ± 841.4237 | — | 0.0 |
| clean | adult | LOO | 5 | 0.6744 | 0.6761 ± 0.0095 | — | 1127.2 |
| clean | adult | KNN-Shapley | 5 | 0.6744 | 0.6747 ± 0.0104 | — | 1.1 |
| clean | adult | Data-OOB | 5 | 0.6744 | 0.6713 ± 0.0104 | — | 1.3 |
| clean | adult | Influence | 5 | 0.6744 | 0.6731 ± 0.0087 | — | 149.1 |
| clean | adult | LiSSA | 5 | 0.6744 | 0.6586 ± 0.0182 | — | 4.8 |
| clean | adult | high loss | 5 | 0.6744 | 0.6802 ± 0.0110 | — | 0.0 |
| clean | adult | random | 5 | 0.6744 | 0.6727 ± 0.0084 | — | 0.0 |
| clean | covertype | LOO | 5 | 0.7192 | 0.7215 ± 0.0070 | — | 1072.6 |
| clean | covertype | KNN-Shapley | 5 | 0.7192 | 0.7158 ± 0.0101 | — | 1.1 |
| clean | covertype | Data-OOB | 5 | 0.7192 | 0.7221 ± 0.0123 | — | 1.7 |
| clean | covertype | Influence | 5 | 0.7192 | 0.7184 ± 0.0038 | — | 503.4 |
| clean | covertype | LiSSA | 5 | 0.7192 | 0.7101 ± 0.0078 | — | 6.8 |
| clean | covertype | high loss | 5 | 0.7192 | 0.7195 ± 0.0102 | — | 0.0 |
| clean | covertype | random | 5 | 0.7192 | 0.7198 ± 0.0071 | — | 0.0 |
| noise10 | wine | LOO | 5 | 0.4850 | 0.4702 ± 0.0215 | 0.5665 ± 0.0326 | 212.0 |
| noise10 | wine | TMC-Shapley | 5 | 0.4850 | 0.4698 ± 0.0278 | 0.5733 ± 0.0343 | 851.3 |
| noise10 | wine | Data-OOB | 5 | 0.4850 | 0.4827 ± 0.0221 | 0.9849 ± 0.0073 | 0.9 |
| noise10 | wine | Influence | 5 | 0.4850 | 0.4863 ± 0.0203 | 0.5193 ± 0.0493 | 0.7 |
| noise10 | wine | LiSSA | 5 | 0.4850 | 0.4919 ± 0.0269 | 0.5811 ± 0.0824 | 0.7 |
| noise10 | wine | high loss | 5 | 0.4850 | 0.4803 ± 0.0289 | 0.9870 ± 0.0081 | 0.0 |
| noise10 | wine | random | 5 | 0.4850 | 0.4841 ± 0.0201 | 0.4705 ± 0.0333 | 0.0 |
| noise10 | housing | LOO | 5 | 46630.4654 | 46494.4817 ± 1525.8061 | 0.5136 ± 0.0111 | 830.9 |
| noise10 | housing | Data-OOB | 5 | 46630.4654 | 44993.3382 ± 1325.8103 | 0.9977 ± 0.0011 | 1.5 |
| noise10 | housing | Influence | 5 | 46630.4654 | 46699.2404 ± 1354.8244 | 0.5397 ± 0.0348 | 3.2 |
| noise10 | housing | LiSSA | 5 | 46630.4654 | 47944.5911 ± 3061.4963 | 0.5394 ± 0.0333 | 1.1 |
| noise10 | housing | high loss | 5 | 46630.4654 | 45151.5881 ± 1287.5639 | 0.9977 ± 0.0007 | 0.0 |
| noise10 | housing | random | 5 | 46630.4654 | 47801.9504 ± 1166.7801 | 0.4973 ± 0.0315 | 0.0 |
| noise10 | adult | LOO | 5 | 0.6668 | 0.6559 ± 0.0132 | 0.5117 ± 0.0247 | 1127.4 |
| noise10 | adult | KNN-Shapley | 5 | 0.6668 | 0.6590 ± 0.0092 | 0.8809 ± 0.0133 | 1.3 |
| noise10 | adult | Data-OOB | 5 | 0.6668 | 0.6625 ± 0.0146 | 0.8877 ± 0.0143 | 1.7 |
| noise10 | adult | Influence | 5 | 0.6668 | 0.6618 ± 0.0139 | 0.5189 ± 0.0327 | 132.6 |
| noise10 | adult | LiSSA | 5 | 0.6668 | 0.6608 ± 0.0047 | 0.8787 ± 0.0202 | 6.2 |
| noise10 | adult | high loss | 5 | 0.6668 | 0.6603 ± 0.0118 | 0.9151 ± 0.0201 | 0.0 |
| noise10 | adult | random | 5 | 0.6668 | 0.6634 ± 0.0115 | 0.4973 ± 0.0315 | 0.0 |
| noise10 | covertype | LOO | 5 | 0.7118 | 0.7115 ± 0.0035 | 0.4979 ± 0.0063 | 1067.6 |
| noise10 | covertype | KNN-Shapley | 5 | 0.7118 | 0.7067 ± 0.0047 | 0.9159 ± 0.0066 | 1.0 |
| noise10 | covertype | Data-OOB | 5 | 0.7118 | 0.7101 ± 0.0130 | 0.9504 ± 0.0077 | 1.8 |
| noise10 | covertype | Influence | 5 | 0.7118 | 0.7026 ± 0.0088 | 0.4981 ± 0.0444 | 379.0 |
| noise10 | covertype | LiSSA | 5 | 0.7118 | 0.6944 ± 0.0069 | 0.8508 ± 0.0703 | 7.6 |
| noise10 | covertype | high loss | 5 | 0.7118 | 0.7116 ± 0.0055 | 0.9327 ± 0.0233 | 0.0 |
| noise10 | covertype | random | 5 | 0.7118 | 0.7110 ± 0.0058 | 0.4973 ± 0.0315 | 0.0 |
| damp-linear-0.0001 | wine | Influence | 3 | 0.4756 | 0.4749 ± 0.0132 | 0.5774 ± 0.0340 | 0.3 |
| damp-linear-0.0001 | wine | LiSSA | 3 | 0.4756 | 0.4731 ± 0.0199 | 0.5919 ± 0.0444 | 0.2 |
| damp-linear-0.0001 | wine | high loss | 3 | 0.4756 | 0.4721 ± 0.0221 | 0.9823 ± 0.0100 | 0.0 |
| damp-linear-0.0001 | wine | random | 3 | 0.4756 | 0.4754 ± 0.0285 | 0.4761 ± 0.0454 | 0.0 |
| damp-linear-0.0001 | housing | Influence | 3 | 50005.8605 | 52866.4848 ± 2657.2929 | 0.5316 ± 0.0604 | 0.5 |
| damp-linear-0.0001 | housing | LiSSA | 3 | 50005.8605 | 53542.4987 ± 1702.2360 | 0.5484 ± 0.0349 | 0.2 |
| damp-linear-0.0001 | housing | high loss | 3 | 50005.8605 | 49460.8035 ± 776.6884 | 0.9950 ± 0.0027 | 0.0 |
| damp-linear-0.0001 | housing | random | 3 | 50005.8605 | 50317.2133 ± 336.9874 | 0.4892 ± 0.0417 | 0.0 |
| damp-linear-0.0001 | adult | Influence | 3 | 0.6293 | 0.6404 ± 0.0062 | 0.7860 ± 0.0397 | 0.5 |
| damp-linear-0.0001 | adult | LiSSA | 3 | 0.6293 | 0.6415 ± 0.0099 | 0.8537 ± 0.0440 | 0.5 |
| damp-linear-0.0001 | adult | high loss | 3 | 0.6293 | 0.6431 ± 0.0083 | 0.9168 ± 0.0134 | 0.0 |
| damp-linear-0.0001 | adult | random | 3 | 0.6293 | 0.6342 ± 0.0090 | 0.4892 ± 0.0417 | 0.0 |
| damp-linear-0.0001 | covertype | Influence | 3 | 0.6930 | 0.6889 ± 0.0110 | 0.8616 ± 0.0307 | 0.8 |
| damp-linear-0.0001 | covertype | LiSSA | 3 | 0.6930 | 0.6806 ± 0.0097 | 0.8352 ± 0.0391 | 0.6 |
| damp-linear-0.0001 | covertype | high loss | 3 | 0.6930 | 0.6999 ± 0.0075 | 0.9205 ± 0.0105 | 0.0 |
| damp-linear-0.0001 | covertype | random | 3 | 0.6930 | 0.6922 ± 0.0155 | 0.4892 ± 0.0417 | 0.0 |
| damp-linear-0.01 | wine | Influence | 3 | 0.4756 | 0.4757 ± 0.0139 | 0.5786 ± 0.0355 | 0.2 |
| damp-linear-0.01 | wine | LiSSA | 3 | 0.4756 | 0.4729 ± 0.0196 | 0.5919 ± 0.0446 | 0.3 |
| damp-linear-0.01 | wine | high loss | 3 | 0.4756 | 0.4721 ± 0.0221 | 0.9823 ± 0.0100 | 0.0 |
| damp-linear-0.01 | wine | random | 3 | 0.4756 | 0.4754 ± 0.0285 | 0.4761 ± 0.0454 | 0.0 |
| damp-linear-0.01 | housing | Influence | 3 | 50005.8605 | 52824.9754 ± 2216.7878 | 0.5321 ± 0.0597 | 0.6 |
| damp-linear-0.01 | housing | LiSSA | 3 | 50005.8605 | 53837.1390 ± 2024.2982 | 0.5487 ± 0.0350 | 0.2 |
| damp-linear-0.01 | housing | high loss | 3 | 50005.8605 | 49460.8035 ± 776.6884 | 0.9950 ± 0.0027 | 0.0 |
| damp-linear-0.01 | housing | random | 3 | 50005.8605 | 50317.2133 ± 336.9874 | 0.4892 ± 0.0417 | 0.0 |
| damp-linear-0.01 | adult | Influence | 3 | 0.6293 | 0.6461 ± 0.0056 | 0.8331 ± 0.0560 | 0.5 |
| damp-linear-0.01 | adult | LiSSA | 3 | 0.6293 | 0.6415 ± 0.0099 | 0.8542 ± 0.0443 | 0.6 |
| damp-linear-0.01 | adult | high loss | 3 | 0.6293 | 0.6431 ± 0.0083 | 0.9168 ± 0.0134 | 0.0 |
| damp-linear-0.01 | adult | random | 3 | 0.6293 | 0.6342 ± 0.0090 | 0.4892 ± 0.0417 | 0.0 |
| damp-linear-0.01 | covertype | Influence | 3 | 0.6930 | 0.6806 ± 0.0037 | 0.8616 ± 0.0264 | 0.7 |
| damp-linear-0.01 | covertype | LiSSA | 3 | 0.6930 | 0.6820 ± 0.0098 | 0.8346 ± 0.0394 | 0.6 |
| damp-linear-0.01 | covertype | high loss | 3 | 0.6930 | 0.6999 ± 0.0075 | 0.9205 ± 0.0105 | 0.0 |
| damp-linear-0.01 | covertype | random | 3 | 0.6930 | 0.6922 ± 0.0155 | 0.4892 ± 0.0417 | 0.0 |
| damp-linear-1 | wine | Influence | 3 | 0.4756 | 0.4775 ± 0.0216 | 0.5876 ± 0.0576 | 0.3 |
| damp-linear-1 | wine | LiSSA | 3 | 0.4756 | 0.4758 ± 0.0194 | 0.5915 ± 0.0497 | 0.3 |
| damp-linear-1 | wine | high loss | 3 | 0.4756 | 0.4721 ± 0.0221 | 0.9823 ± 0.0100 | 0.0 |
| damp-linear-1 | wine | random | 3 | 0.4756 | 0.4754 ± 0.0285 | 0.4761 ± 0.0454 | 0.0 |
| damp-linear-1 | housing | Influence | 3 | 50005.8605 | 53499.1910 ± 2208.5407 | 0.5509 ± 0.0381 | 0.6 |
| damp-linear-1 | housing | LiSSA | 3 | 50005.8605 | 54205.5404 ± 2761.7786 | 0.5454 ± 0.0388 | 0.2 |
| damp-linear-1 | housing | high loss | 3 | 50005.8605 | 49460.8035 ± 776.6884 | 0.9950 ± 0.0027 | 0.0 |
| damp-linear-1 | housing | random | 3 | 50005.8605 | 50317.2133 ± 336.9874 | 0.4892 ± 0.0417 | 0.0 |
| damp-linear-1 | adult | Influence | 3 | 0.6293 | 0.6433 ± 0.0075 | 0.8415 ± 0.0498 | 0.5 |
| damp-linear-1 | adult | LiSSA | 3 | 0.6293 | 0.6451 ± 0.0115 | 0.8413 ± 0.0513 | 0.5 |
| damp-linear-1 | adult | high loss | 3 | 0.6293 | 0.6431 ± 0.0083 | 0.9168 ± 0.0134 | 0.0 |
| damp-linear-1 | adult | random | 3 | 0.6293 | 0.6342 ± 0.0090 | 0.4892 ± 0.0417 | 0.0 |
| damp-linear-1 | covertype | Influence | 3 | 0.6930 | 0.6785 ± 0.0055 | 0.7927 ± 0.0595 | 0.7 |
| damp-linear-1 | covertype | LiSSA | 3 | 0.6930 | 0.6779 ± 0.0042 | 0.7897 ± 0.0590 | 0.6 |
| damp-linear-1 | covertype | high loss | 3 | 0.6930 | 0.6999 ± 0.0075 | 0.9205 ± 0.0105 | 0.0 |
| damp-linear-1 | covertype | random | 3 | 0.6930 | 0.6922 ± 0.0155 | 0.4892 ± 0.0417 | 0.0 |
| damp-linear-1e-06 | wine | Influence | 3 | 0.4756 | 0.4749 ± 0.0132 | 0.5774 ± 0.0340 | 0.2 |
| damp-linear-1e-06 | wine | LiSSA | 3 | 0.4756 | 0.4731 ± 0.0199 | 0.5918 ± 0.0444 | 0.3 |
| damp-linear-1e-06 | wine | high loss | 3 | 0.4756 | 0.4721 ± 0.0221 | 0.9823 ± 0.0100 | 0.0 |
| damp-linear-1e-06 | wine | random | 3 | 0.4756 | 0.4754 ± 0.0285 | 0.4761 ± 0.0454 | 0.0 |
| damp-linear-1e-06 | housing | Influence | 3 | 50005.8605 | 52866.4848 ± 2657.2929 | 0.5316 ± 0.0604 | 0.6 |
| damp-linear-1e-06 | housing | LiSSA | 3 | 50005.8605 | 53542.4987 ± 1702.2360 | 0.5484 ± 0.0349 | 0.3 |
| damp-linear-1e-06 | housing | high loss | 3 | 50005.8605 | 49460.8035 ± 776.6884 | 0.9950 ± 0.0027 | 0.0 |
| damp-linear-1e-06 | housing | random | 3 | 50005.8605 | 50317.2133 ± 336.9874 | 0.4892 ± 0.0417 | 0.0 |
| damp-linear-1e-06 | adult | Influence | 3 | 0.6293 | 0.6456 ± 0.0061 | 0.7806 ± 0.0376 | 0.5 |
| damp-linear-1e-06 | adult | LiSSA | 3 | 0.6293 | 0.6415 ± 0.0099 | 0.8537 ± 0.0440 | 0.5 |
| damp-linear-1e-06 | adult | high loss | 3 | 0.6293 | 0.6431 ± 0.0083 | 0.9168 ± 0.0134 | 0.0 |
| damp-linear-1e-06 | adult | random | 3 | 0.6293 | 0.6342 ± 0.0090 | 0.4892 ± 0.0417 | 0.0 |
| damp-linear-1e-06 | covertype | Influence | 3 | 0.6930 | 0.6863 ± 0.0085 | 0.8564 ± 0.0370 | 0.8 |
| damp-linear-1e-06 | covertype | LiSSA | 3 | 0.6930 | 0.6806 ± 0.0097 | 0.8352 ± 0.0391 | 0.6 |
| damp-linear-1e-06 | covertype | high loss | 3 | 0.6930 | 0.6999 ± 0.0075 | 0.9205 ± 0.0105 | 0.0 |
| damp-linear-1e-06 | covertype | random | 3 | 0.6930 | 0.6922 ± 0.0155 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-0.0001 | wine | Influence | 3 | 0.4833 | 0.4897 ± 0.0279 | 0.5321 ± 0.0651 | 0.7 |
| damp-mlp-0.0001 | wine | LiSSA | 3 | 0.4833 | 0.4823 ± 0.0280 | 0.6200 ± 0.0992 | 0.8 |
| damp-mlp-0.0001 | wine | high loss | 3 | 0.4833 | 0.4766 ± 0.0369 | 0.9841 ± 0.0099 | 0.0 |
| damp-mlp-0.0001 | wine | random | 3 | 0.4833 | 0.4828 ± 0.0254 | 0.4761 ± 0.0454 | 0.0 |
| damp-mlp-0.0001 | housing | Influence | 3 | 46691.2572 | 46493.7737 ± 1597.9133 | 0.5304 ± 0.0405 | 5.3 |
| damp-mlp-0.0001 | housing | LiSSA | 3 | 46691.2572 | 47128.9788 ± 625.9011 | 0.5411 ± 0.0255 | 1.3 |
| damp-mlp-0.0001 | housing | high loss | 3 | 46691.2572 | 44544.6783 ± 1213.8324 | 0.9976 ± 0.0007 | 0.0 |
| damp-mlp-0.0001 | housing | random | 3 | 46691.2572 | 47887.7516 ± 923.4232 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-0.0001 | adult | Influence | 3 | 0.6660 | 0.6540 ± 0.0126 | 0.4982 ± 0.0073 | 174.3 |
| damp-mlp-0.0001 | adult | LiSSA | 3 | 0.6660 | 0.6567 ± 0.0125 | 0.8516 ± 0.0483 | 9.3 |
| damp-mlp-0.0001 | adult | high loss | 3 | 0.6660 | 0.6565 ± 0.0148 | 0.9251 ± 0.0093 | 0.0 |
| damp-mlp-0.0001 | adult | random | 3 | 0.6660 | 0.6610 ± 0.0149 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-0.01 | wine | Influence | 3 | 0.4833 | 0.4828 ± 0.0240 | 0.4978 ± 0.0473 | 0.7 |
| damp-mlp-0.01 | wine | LiSSA | 3 | 0.4833 | 0.4834 ± 0.0287 | 0.6202 ± 0.0995 | 0.7 |
| damp-mlp-0.01 | wine | high loss | 3 | 0.4833 | 0.4766 ± 0.0369 | 0.9841 ± 0.0099 | 0.0 |
| damp-mlp-0.01 | wine | random | 3 | 0.4833 | 0.4828 ± 0.0254 | 0.4761 ± 0.0454 | 0.0 |
| damp-mlp-0.01 | housing | Influence | 3 | 46691.2572 | 46730.9886 ± 1652.1578 | 0.5048 ± 0.0501 | 4.6 |
| damp-mlp-0.01 | housing | LiSSA | 3 | 46691.2572 | 47043.4172 ± 886.1716 | 0.5407 ± 0.0253 | 1.3 |
| damp-mlp-0.01 | housing | high loss | 3 | 46691.2572 | 44544.6783 ± 1213.8324 | 0.9976 ± 0.0007 | 0.0 |
| damp-mlp-0.01 | housing | random | 3 | 46691.2572 | 47887.7516 ± 923.4232 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-0.01 | adult | Influence | 3 | 0.6660 | 0.6649 ± 0.0037 | 0.6963 ± 0.0393 | 167.2 |
| damp-mlp-0.01 | adult | LiSSA | 3 | 0.6660 | 0.6561 ± 0.0115 | 0.8528 ± 0.0488 | 7.1 |
| damp-mlp-0.01 | adult | high loss | 3 | 0.6660 | 0.6565 ± 0.0148 | 0.9251 ± 0.0093 | 0.0 |
| damp-mlp-0.01 | adult | random | 3 | 0.6660 | 0.6610 ± 0.0149 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-0.1 | wine | Influence | 3 | 0.4833 | 0.4823 ± 0.0268 | 0.5994 ± 0.0819 | 0.5 |
| damp-mlp-0.1 | wine | random | 3 | 0.4833 | 0.4828 ± 0.0254 | 0.4761 ± 0.0454 | 0.0 |
| damp-mlp-0.1 | housing | Influence | 3 | 46691.2572 | 46002.1941 ± 1133.5462 | 0.5461 ± 0.0571 | 2.9 |
| damp-mlp-0.1 | housing | random | 3 | 46691.2572 | 47887.7516 ± 923.4232 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-0.1 | adult | Influence | 3 | 0.6660 | 0.6624 ± 0.0071 | 0.8516 ± 0.0270 | 139.8 |
| damp-mlp-0.1 | adult | random | 3 | 0.6660 | 0.6610 ± 0.0149 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-0.1 | covertype | Influence | 3 | 0.7124 | 0.7081 ± 0.0048 | 0.8178 ± 0.0438 | 415.3 |
| damp-mlp-0.1 | covertype | random | 3 | 0.7124 | 0.7091 ± 0.0045 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-1 | wine | Influence | 3 | 0.4833 | 0.4811 ± 0.0273 | 0.6209 ± 0.0972 | 0.6 |
| damp-mlp-1 | wine | LiSSA | 3 | 0.4833 | 0.4776 ± 0.0274 | 0.6190 ± 0.1085 | 0.7 |
| damp-mlp-1 | wine | high loss | 3 | 0.4833 | 0.4766 ± 0.0369 | 0.9841 ± 0.0099 | 0.0 |
| damp-mlp-1 | wine | random | 3 | 0.4833 | 0.4828 ± 0.0254 | 0.4761 ± 0.0454 | 0.0 |
| damp-mlp-1 | housing | Influence | 3 | 46691.2572 | 47807.6699 ± 2035.2280 | 0.5381 ± 0.0382 | 3.6 |
| damp-mlp-1 | housing | LiSSA | 3 | 46691.2572 | 48269.6332 ± 1865.5407 | 0.5404 ± 0.0276 | 1.3 |
| damp-mlp-1 | housing | high loss | 3 | 46691.2572 | 44544.6783 ± 1213.8324 | 0.9976 ± 0.0007 | 0.0 |
| damp-mlp-1 | housing | random | 3 | 46691.2572 | 47887.7516 ± 923.4232 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-1 | adult | Influence | 3 | 0.6660 | 0.6554 ± 0.0093 | 0.8919 ± 0.0238 | 139.3 |
| damp-mlp-1 | adult | LiSSA | 3 | 0.6660 | 0.6598 ± 0.0103 | 0.8767 ± 0.0185 | 5.5 |
| damp-mlp-1 | adult | high loss | 3 | 0.6660 | 0.6565 ± 0.0148 | 0.9251 ± 0.0093 | 0.0 |
| damp-mlp-1 | adult | random | 3 | 0.6660 | 0.6610 ± 0.0149 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-1 | covertype | Influence | 3 | 0.7124 | 0.6997 ± 0.0063 | 0.8606 ± 0.0652 | 383.0 |
| damp-mlp-1 | covertype | random | 3 | 0.7124 | 0.7091 ± 0.0045 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-1e-06 | wine | Influence | 3 | 0.4833 | 0.4769 ± 0.0237 | 0.5174 ± 0.0538 | 0.6 |
| damp-mlp-1e-06 | wine | LiSSA | 3 | 0.4833 | 0.4823 ± 0.0280 | 0.6200 ± 0.0992 | 0.7 |
| damp-mlp-1e-06 | wine | high loss | 3 | 0.4833 | 0.4766 ± 0.0369 | 0.9841 ± 0.0099 | 0.0 |
| damp-mlp-1e-06 | wine | random | 3 | 0.4833 | 0.4828 ± 0.0254 | 0.4761 ± 0.0454 | 0.0 |
| damp-mlp-1e-06 | housing | Influence | 3 | 46691.2572 | 46766.6283 ± 1583.9464 | 0.5208 ± 0.0246 | 3.4 |
| damp-mlp-1e-06 | housing | LiSSA | 3 | 46691.2572 | 47128.9788 ± 625.9011 | 0.5411 ± 0.0255 | 1.4 |
| damp-mlp-1e-06 | housing | high loss | 3 | 46691.2572 | 44544.6783 ± 1213.8324 | 0.9976 ± 0.0007 | 0.0 |
| damp-mlp-1e-06 | housing | random | 3 | 46691.2572 | 47887.7516 ± 923.4232 | 0.4892 ± 0.0417 | 0.0 |
| damp-mlp-1e-06 | adult | Influence | 3 | 0.6660 | 0.6650 ± 0.0122 | 0.5429 ± 0.0276 | 136.1 |
| damp-mlp-1e-06 | adult | LiSSA | 3 | 0.6660 | 0.6567 ± 0.0125 | 0.8515 ± 0.0483 | 5.4 |
| damp-mlp-1e-06 | adult | high loss | 3 | 0.6660 | 0.6565 ± 0.0148 | 0.9251 ± 0.0093 | 0.0 |
| damp-mlp-1e-06 | adult | random | 3 | 0.6660 | 0.6610 ± 0.0149 | 0.4892 ± 0.0417 | 0.0 |
| distill-catboost-noise10 | wine | Data-OOB | 3 | 0.5076 | 0.4991 ± 0.0154 | 0.9836 ± 0.0090 | 0.8 |
| distill-catboost-noise10 | wine | Influence | 3 | 0.5076 | 0.5004 ± 0.0176 | 0.4459 ± 0.0505 | 1.3 |
| distill-catboost-noise10 | wine | LiSSA | 3 | 0.5076 | 0.4898 ± 0.0194 | 0.5856 ± 0.0782 | 0.8 |
| distill-catboost-noise10 | wine | high loss | 3 | 0.5076 | 0.4990 ± 0.0189 | 0.9777 ± 0.0059 | 0.0 |
| distill-catboost-noise10 | wine | random | 3 | 0.5076 | 0.5044 ± 0.0189 | 0.4761 ± 0.0454 | 0.0 |
| distill-catboost-noise10 | housing | Data-OOB | 3 | 49457.3421 | 49062.1385 ± 1161.0737 | 0.9980 ± 0.0007 | 1.2 |
| distill-catboost-noise10 | housing | Influence | 3 | 49457.3421 | 50128.3599 ± 1041.9861 | 0.5355 ± 0.0314 | 2.5 |
| distill-catboost-noise10 | housing | LiSSA | 3 | 49457.3421 | 49506.9038 ± 275.5503 | 0.5460 ± 0.0339 | 1.1 |
| distill-catboost-noise10 | housing | high loss | 3 | 49457.3421 | 49666.0046 ± 795.4332 | 0.9950 ± 0.0017 | 0.0 |
| distill-catboost-noise10 | housing | random | 3 | 49457.3421 | 49693.3967 ± 845.9302 | 0.4892 ± 0.0417 | 0.0 |
| distill-catboost-noise10 | adult | Data-OOB | 3 | 0.6577 | 0.6632 ± 0.0124 | 0.8960 ± 0.0080 | 1.7 |
| distill-catboost-noise10 | adult | Influence | 3 | 0.6577 | 0.6536 ± 0.0030 | 0.5375 ± 0.0319 | 30.6 |
| distill-catboost-noise10 | adult | LiSSA | 3 | 0.6577 | 0.6511 ± 0.0083 | 0.7637 ± 0.0129 | 1.9 |
| distill-catboost-noise10 | adult | high loss | 3 | 0.6577 | 0.6586 ± 0.0103 | 0.8699 ± 0.0165 | 0.0 |
| distill-catboost-noise10 | adult | CatBoost LFC | 3 | 0.6577 | 0.6626 ± 0.0048 | 0.7484 ± 0.0487 | 1.5 |
| distill-catboost-noise10 | adult | random | 3 | 0.6577 | 0.6562 ± 0.0010 | 0.4892 ± 0.0417 | 0.0 |
| distill-catboost-noise10 | covertype | Data-OOB | 3 | 0.7137 | 0.7133 ± 0.0121 | 0.9503 ± 0.0082 | 1.8 |
| distill-catboost-noise10 | covertype | Influence | 3 | 0.7137 | 0.7106 ± 0.0091 | 0.5010 ± 0.0532 | 17.8 |
| distill-catboost-noise10 | covertype | LiSSA | 3 | 0.7137 | 0.7119 ± 0.0051 | 0.8782 ± 0.0216 | 1.6 |
| distill-catboost-noise10 | covertype | high loss | 3 | 0.7137 | 0.7087 ± 0.0098 | 0.9389 ± 0.0124 | 0.0 |
| distill-catboost-noise10 | covertype | random | 3 | 0.7137 | 0.7085 ± 0.0073 | 0.4892 ± 0.0417 | 0.0 |
| distill-catboost-noise10-tgtteacher | wine | Influence | 3 | 0.5076 | 0.4991 ± 0.0191 | 0.5002 ± 0.0446 | 1.8 |
| distill-catboost-noise10-tgtteacher | wine | LiSSA | 3 | 0.5076 | 0.4976 ± 0.0223 | 0.5112 ± 0.0609 | 0.8 |
| distill-catboost-noise10-tgtteacher | housing | Influence | 3 | 49457.3421 | 50187.5524 ± 1079.9658 | 0.5028 ± 0.0128 | 2.4 |
| distill-catboost-noise10-tgtteacher | housing | LiSSA | 3 | 49457.3421 | 49274.7304 ± 384.2481 | 0.5034 ± 0.0055 | 1.2 |
| distill-catboost-noise10-tgtteacher | adult | Influence | 3 | 0.6577 | 0.6582 ± 0.0085 | 0.5033 ± 0.0254 | 31.3 |
| distill-catboost-noise10-tgtteacher | adult | LiSSA | 3 | 0.6577 | 0.6586 ± 0.0110 | 0.7671 ± 0.0251 | 2.0 |
| distill-catboost-noise10-tgtteacher | covertype | Influence | 3 | 0.7137 | 0.7163 ± 0.0040 | 0.5627 ± 0.0216 | 19.9 |
| distill-catboost-noise10-tgtteacher | covertype | LiSSA | 3 | 0.7137 | 0.7141 ± 0.0021 | 0.9114 ± 0.0105 | 1.8 |
| distill-lightgbm-noise10 | wine | Data-OOB | 3 | 0.4810 | 0.4755 ± 0.0226 | 0.9836 ± 0.0090 | 0.8 |
| distill-lightgbm-noise10 | wine | Influence | 3 | 0.4810 | 0.4868 ± 0.0186 | 0.4627 ± 0.0172 | 1.8 |
| distill-lightgbm-noise10 | wine | LiSSA | 3 | 0.4810 | 0.4780 ± 0.0203 | 0.5550 ± 0.1115 | 0.9 |
| distill-lightgbm-noise10 | wine | high loss | 3 | 0.4810 | 0.4740 ± 0.0250 | 0.9840 ± 0.0092 | 0.0 |
| distill-lightgbm-noise10 | wine | BoostIn | 3 | 0.4810 | 0.4797 ± 0.0182 | 0.5681 ± 0.0925 | 0.2 |
| distill-lightgbm-noise10 | wine | random | 3 | 0.4810 | 0.4710 ± 0.0231 | 0.4761 ± 0.0454 | 0.0 |
| distill-lightgbm-noise10 | housing | Data-OOB | 3 | 47517.2028 | 43210.6704 ± 1255.4420 | 0.9980 ± 0.0007 | 1.4 |
| distill-lightgbm-noise10 | housing | Influence | 3 | 47517.2028 | 46505.0418 ± 1052.8192 | 0.4739 ± 0.0280 | 2.7 |
| distill-lightgbm-noise10 | housing | LiSSA | 3 | 47517.2028 | 47912.0113 ± 575.5569 | 0.5073 ± 0.0106 | 1.5 |
| distill-lightgbm-noise10 | housing | high loss | 3 | 47517.2028 | 43850.1851 ± 648.8749 | 0.9981 ± 0.0007 | 0.0 |
| distill-lightgbm-noise10 | housing | BoostIn | 3 | 47517.2028 | 46775.8655 ± 914.2568 | 0.5293 ± 0.0252 | 0.3 |
| distill-lightgbm-noise10 | housing | random | 3 | 47517.2028 | 48764.5601 ± 414.3844 | 0.4892 ± 0.0417 | 0.0 |
| distill-lightgbm-noise10 | adult | Data-OOB | 3 | 0.6546 | 0.6567 ± 0.0077 | 0.8960 ± 0.0080 | 1.6 |
| distill-lightgbm-noise10 | adult | Influence | 3 | 0.6546 | 0.6539 ± 0.0024 | 0.5323 ± 0.0238 | 42.0 |
| distill-lightgbm-noise10 | adult | LiSSA | 3 | 0.6546 | 0.6578 ± 0.0079 | 0.7596 ± 0.0175 | 2.5 |
| distill-lightgbm-noise10 | adult | high loss | 3 | 0.6546 | 0.6627 ± 0.0101 | 0.8782 ± 0.0142 | 0.0 |
| distill-lightgbm-noise10 | adult | BoostIn | 3 | 0.6546 | 0.6581 ± 0.0027 | 0.8291 ± 0.0284 | 1.2 |
| distill-lightgbm-noise10 | adult | random | 3 | 0.6546 | 0.6566 ± 0.0115 | 0.4892 ± 0.0417 | 0.0 |
| distill-lightgbm-noise10 | covertype | Data-OOB | 3 | 0.7166 | 0.7151 ± 0.0129 | 0.9503 ± 0.0082 | 1.8 |
| distill-lightgbm-noise10 | covertype | Influence | 3 | 0.7166 | 0.7107 ± 0.0108 | 0.5165 ± 0.0719 | 11.6 |
| distill-lightgbm-noise10 | covertype | LiSSA | 3 | 0.7166 | 0.7112 ± 0.0063 | 0.7880 ± 0.0859 | 1.7 |
| distill-lightgbm-noise10 | covertype | high loss | 3 | 0.7166 | 0.7133 ± 0.0090 | 0.9440 ± 0.0119 | 0.0 |
| distill-lightgbm-noise10 | covertype | BoostIn | 3 | 0.7166 | 0.7117 ± 0.0112 | 0.9079 ± 0.0194 | 7.5 |
| distill-lightgbm-noise10 | covertype | random | 3 | 0.7166 | 0.7155 ± 0.0085 | 0.4892 ± 0.0417 | 0.0 |
| distill-lightgbm-noise10-tgtteacher | wine | Influence | 3 | 0.4810 | 0.4955 ± 0.0264 | 0.4734 ± 0.0648 | 2.0 |
| distill-lightgbm-noise10-tgtteacher | wine | LiSSA | 3 | 0.4810 | 0.4700 ± 0.0213 | 0.5327 ± 0.1035 | 0.9 |
| distill-lightgbm-noise10-tgtteacher | housing | Influence | 3 | 47517.2028 | 48039.9602 ± 246.3170 | 0.5087 ± 0.0372 | 3.0 |
| distill-lightgbm-noise10-tgtteacher | housing | LiSSA | 3 | 47517.2028 | 47677.2473 ± 669.4658 | 0.5059 ± 0.0129 | 1.5 |
| distill-lightgbm-noise10-tgtteacher | adult | Influence | 3 | 0.6546 | 0.6483 ± 0.0104 | 0.4484 ± 0.0195 | 41.0 |
| distill-lightgbm-noise10-tgtteacher | adult | LiSSA | 3 | 0.6546 | 0.6631 ± 0.0047 | 0.7473 ± 0.0416 | 2.3 |
| distill-lightgbm-noise10-tgtteacher | covertype | Influence | 3 | 0.7166 | 0.7134 ± 0.0060 | 0.5231 ± 0.0578 | 11.7 |
| distill-lightgbm-noise10-tgtteacher | covertype | LiSSA | 3 | 0.7166 | 0.7173 ± 0.0060 | 0.9244 ± 0.0092 | 2.0 |
| models-catboost-clean | wine | LOO | 3 | 0.4949 | 0.4946 ± 0.0273 | — | 37.8 |
| models-catboost-clean | wine | Data-OOB | 3 | 0.4949 | 0.4899 ± 0.0179 | — | 0.8 |
| models-catboost-clean | wine | high loss | 3 | 0.4949 | 0.4957 ± 0.0227 | — | 0.0 |
| models-catboost-clean | wine | CatBoost LFC | 3 | 0.4949 | 0.4957 ± 0.0206 | — | 0.0 |
| models-catboost-clean | wine | random | 3 | 0.4949 | 0.4919 ± 0.0200 | — | 0.0 |
| models-catboost-clean | housing | LOO | 3 | 46615.9061 | 46815.9514 ± 839.5180 | — | 386.2 |
| models-catboost-clean | housing | Data-OOB | 3 | 46615.9061 | 47546.7765 ± 1063.3424 | — | 1.1 |
| models-catboost-clean | housing | high loss | 3 | 46615.9061 | 48697.2180 ± 1128.4273 | — | 0.0 |
| models-catboost-clean | housing | CatBoost LFC | 3 | 46615.9061 | 47586.3805 ± 1569.4473 | — | 0.1 |
| models-catboost-clean | housing | random | 3 | 46615.9061 | 46812.3114 ± 1027.2540 | — | 0.0 |
| models-catboost-clean | adult | LOO | 3 | 0.6881 | 0.6815 ± 0.0044 | — | 389.9 |
| models-catboost-clean | adult | KNN-Shapley | 3 | 0.6881 | 0.6746 ± 0.0133 | — | 1.3 |
| models-catboost-clean | adult | Data-OOB | 3 | 0.6881 | 0.6774 ± 0.0079 | — | 1.4 |
| models-catboost-clean | adult | high loss | 3 | 0.6881 | 0.6779 ± 0.0082 | — | 0.0 |
| models-catboost-clean | adult | CatBoost LFC | 3 | 0.6881 | 0.6800 ± 0.0148 | — | 1.5 |
| models-catboost-clean | adult | random | 3 | 0.6881 | 0.6802 ± 0.0030 | — | 0.0 |
| models-catboost-clean | covertype | LOO | 3 | 0.7105 | 0.7164 ± 0.0085 | — | 5120.6 |
| models-catboost-clean | covertype | KNN-Shapley | 3 | 0.7105 | 0.7163 ± 0.0173 | — | 1.4 |
| models-catboost-clean | covertype | Data-OOB | 3 | 0.7105 | 0.7154 ± 0.0121 | — | 1.7 |
| models-catboost-clean | covertype | high loss | 3 | 0.7105 | 0.7147 ± 0.0132 | — | 0.0 |
| models-catboost-clean | covertype | random | 3 | 0.7105 | 0.7186 ± 0.0123 | — | 0.0 |
| models-catboost-noise10 | wine | LOO | 3 | 0.5037 | 0.5199 ± 0.0280 | 0.5077 ± 0.0222 | 38.6 |
| models-catboost-noise10 | wine | Data-OOB | 3 | 0.5037 | 0.4959 ± 0.0178 | 0.9836 ± 0.0090 | 1.2 |
| models-catboost-noise10 | wine | high loss | 3 | 0.5037 | 0.4937 ± 0.0162 | 0.9777 ± 0.0061 | 0.0 |
| models-catboost-noise10 | wine | CatBoost LFC | 3 | 0.5037 | 0.4966 ± 0.0225 | 0.5243 ± 0.0425 | 0.1 |
| models-catboost-noise10 | wine | random | 3 | 0.5037 | 0.4993 ± 0.0180 | 0.4761 ± 0.0454 | 0.0 |
| models-catboost-noise10 | housing | LOO | 3 | 47002.3729 | 47301.4437 ± 603.6063 | 0.5167 ± 0.0036 | 418.0 |
| models-catboost-noise10 | housing | Data-OOB | 3 | 47002.3729 | 47061.7218 ± 970.4177 | 0.9980 ± 0.0007 | 1.1 |
| models-catboost-noise10 | housing | high loss | 3 | 47002.3729 | 47135.9689 ± 993.2007 | 0.9962 ± 0.0010 | 0.0 |
| models-catboost-noise10 | housing | CatBoost LFC | 3 | 47002.3729 | 47923.3371 ± 739.6269 | 0.5048 ± 0.0094 | 0.1 |
| models-catboost-noise10 | housing | random | 3 | 47002.3729 | 47689.9675 ± 1417.9551 | 0.4892 ± 0.0417 | 0.0 |
| models-catboost-noise10 | adult | LOO | 3 | 0.6643 | 0.6598 ± 0.0091 | 0.5235 ± 0.0259 | 361.7 |
| models-catboost-noise10 | adult | KNN-Shapley | 3 | 0.6643 | 0.6558 ± 0.0094 | 0.8784 ± 0.0176 | 1.5 |
| models-catboost-noise10 | adult | Data-OOB | 3 | 0.6643 | 0.6600 ± 0.0046 | 0.8960 ± 0.0080 | 1.5 |
| models-catboost-noise10 | adult | high loss | 3 | 0.6643 | 0.6619 ± 0.0056 | 0.9170 ± 0.0017 | 0.0 |
| models-catboost-noise10 | adult | CatBoost LFC | 3 | 0.6643 | 0.6672 ± 0.0070 | 0.7484 ± 0.0487 | 1.7 |
| models-catboost-noise10 | adult | random | 3 | 0.6643 | 0.6621 ± 0.0011 | 0.4892 ± 0.0417 | 0.0 |
| models-catboost-noise10 | covertype | LOO | 3 | 0.6827 | 0.6832 ± 0.0095 | 0.5272 ± 0.0053 | 5186.5 |
| models-catboost-noise10 | covertype | KNN-Shapley | 3 | 0.6827 | 0.6887 ± 0.0151 | 0.9135 ± 0.0041 | 1.4 |
| models-catboost-noise10 | covertype | Data-OOB | 3 | 0.6827 | 0.6920 ± 0.0151 | 0.9503 ± 0.0082 | 2.1 |
| models-catboost-noise10 | covertype | high loss | 3 | 0.6827 | 0.6885 ± 0.0123 | 0.9053 ± 0.0137 | 0.0 |
| models-catboost-noise10 | covertype | random | 3 | 0.6827 | 0.6815 ± 0.0078 | 0.4892 ± 0.0417 | 0.0 |
| models-lightgbm-clean | wine | LOO | 3 | 0.4349 | 0.4377 ± 0.0191 | — | 72.9 |
| models-lightgbm-clean | wine | Data-OOB | 3 | 0.4349 | 0.4477 ± 0.0261 | — | 0.8 |
| models-lightgbm-clean | wine | high loss | 3 | 0.4349 | 0.4487 ± 0.0406 | — | 0.0 |
| models-lightgbm-clean | wine | BoostIn | 3 | 0.4349 | 0.4501 ± 0.0248 | — | 0.5 |
| models-lightgbm-clean | wine | random | 3 | 0.4349 | 0.4423 ± 0.0284 | — | 0.0 |
| models-lightgbm-clean | housing | LOO | 3 | 37837.0841 | 38879.8646 ± 626.2099 | — | 308.6 |
| models-lightgbm-clean | housing | Data-OOB | 3 | 37837.0841 | 38504.3585 ± 629.5080 | — | 1.2 |
| models-lightgbm-clean | housing | high loss | 3 | 37837.0841 | 37857.6206 ± 841.5739 | — | 0.0 |
| models-lightgbm-clean | housing | BoostIn | 3 | 37837.0841 | 40707.9703 ± 711.5348 | — | 1.7 |
| models-lightgbm-clean | housing | random | 3 | 37837.0841 | 38913.5488 ± 752.8004 | — | 0.0 |
| models-lightgbm-clean | adult | LOO | 3 | 0.6747 | 0.6787 ± 0.0085 | — | 216.4 |
| models-lightgbm-clean | adult | KNN-Shapley | 3 | 0.6747 | 0.6683 ± 0.0133 | — | 1.1 |
| models-lightgbm-clean | adult | Data-OOB | 3 | 0.6747 | 0.6596 ± 0.0118 | — | 1.3 |
| models-lightgbm-clean | adult | high loss | 3 | 0.6747 | 0.6561 ± 0.0053 | — | 0.0 |
| models-lightgbm-clean | adult | BoostIn | 3 | 0.6747 | 0.6720 ± 0.0177 | — | 0.4 |
| models-lightgbm-clean | adult | random | 3 | 0.6747 | 0.6786 ± 0.0092 | — | 0.0 |
| models-lightgbm-clean | covertype | LOO | 3 | 0.7088 | 0.7093 ± 0.0143 | — | 1581.7 |
| models-lightgbm-clean | covertype | KNN-Shapley | 3 | 0.7088 | 0.7037 ± 0.0040 | — | 1.0 |
| models-lightgbm-clean | covertype | Data-OOB | 3 | 0.7088 | 0.6999 ± 0.0126 | — | 1.7 |
| models-lightgbm-clean | covertype | high loss | 3 | 0.7088 | 0.6995 ± 0.0142 | — | 0.0 |
| models-lightgbm-clean | covertype | BoostIn | 3 | 0.7088 | 0.7013 ± 0.0083 | — | 5.6 |
| models-lightgbm-clean | covertype | random | 3 | 0.7088 | 0.7053 ± 0.0134 | — | 0.0 |
| models-lightgbm-noise10 | wine | LOO | 3 | 0.4998 | 0.4917 ± 0.0149 | 0.5356 ± 0.0393 | 72.8 |
| models-lightgbm-noise10 | wine | Data-OOB | 3 | 0.4998 | 0.4583 ± 0.0337 | 0.9836 ± 0.0090 | 0.8 |
| models-lightgbm-noise10 | wine | high loss | 3 | 0.4998 | 0.4513 ± 0.0328 | 0.9829 ± 0.0074 | 0.0 |
| models-lightgbm-noise10 | wine | BoostIn | 3 | 0.4998 | 0.5192 ± 0.0216 | 0.5467 ± 0.1158 | 0.1 |
| models-lightgbm-noise10 | wine | random | 3 | 0.4998 | 0.4791 ± 0.0289 | 0.4761 ± 0.0454 | 0.0 |
| models-lightgbm-noise10 | housing | LOO | 3 | 49157.8074 | 49754.5781 ± 985.4220 | 0.5582 ± 0.0081 | 295.8 |
| models-lightgbm-noise10 | housing | Data-OOB | 3 | 49157.8074 | 39021.8209 ± 353.1227 | 0.9980 ± 0.0007 | 1.4 |
| models-lightgbm-noise10 | housing | high loss | 3 | 49157.8074 | 40419.6462 ± 729.7573 | 0.9974 ± 0.0005 | 0.0 |
| models-lightgbm-noise10 | housing | BoostIn | 3 | 49157.8074 | 54032.1055 ± 1864.9020 | 0.5531 ± 0.0141 | 0.3 |
| models-lightgbm-noise10 | housing | random | 3 | 49157.8074 | 50179.8604 ± 614.8884 | 0.4892 ± 0.0417 | 0.0 |
| models-lightgbm-noise10 | adult | LOO | 3 | 0.6367 | 0.6419 ± 0.0108 | 0.5076 ± 0.0146 | 207.6 |
| models-lightgbm-noise10 | adult | KNN-Shapley | 3 | 0.6367 | 0.6598 ± 0.0154 | 0.8784 ± 0.0176 | 1.4 |
| models-lightgbm-noise10 | adult | Data-OOB | 3 | 0.6367 | 0.6513 ± 0.0107 | 0.8960 ± 0.0080 | 1.8 |
| models-lightgbm-noise10 | adult | high loss | 3 | 0.6367 | 0.6610 ± 0.0067 | 0.8893 ± 0.0180 | 0.0 |
| models-lightgbm-noise10 | adult | BoostIn | 3 | 0.6367 | 0.6572 ± 0.0094 | 0.8291 ± 0.0284 | 1.4 |
| models-lightgbm-noise10 | adult | random | 3 | 0.6367 | 0.6408 ± 0.0135 | 0.4892 ± 0.0417 | 0.0 |
| models-lightgbm-noise10 | covertype | LOO | 3 | 0.6955 | 0.6901 ± 0.0153 | 0.4891 ± 0.0086 | 1805.1 |
| models-lightgbm-noise10 | covertype | KNN-Shapley | 3 | 0.6955 | 0.6973 ± 0.0150 | 0.9135 ± 0.0041 | 1.0 |
| models-lightgbm-noise10 | covertype | Data-OOB | 3 | 0.6955 | 0.7004 ± 0.0151 | 0.9503 ± 0.0082 | 1.9 |
| models-lightgbm-noise10 | covertype | high loss | 3 | 0.6955 | 0.6942 ± 0.0117 | 0.8260 ± 0.0357 | 0.0 |
| models-lightgbm-noise10 | covertype | BoostIn | 3 | 0.6955 | 0.6945 ± 0.0135 | 0.9079 ± 0.0194 | 7.2 |
| models-lightgbm-noise10 | covertype | random | 3 | 0.6955 | 0.6903 ± 0.0116 | 0.4892 ± 0.0417 | 0.0 |
| models-random_forest-clean | wine | LOO | 3 | 0.4366 | 0.4450 ± 0.0135 | — | 101.0 |
| models-random_forest-clean | wine | Data-OOB | 3 | 0.4366 | 0.4579 ± 0.0134 | — | 0.9 |
| models-random_forest-clean | wine | high loss | 3 | 0.4366 | 0.4505 ± 0.0221 | — | 0.0 |
| models-random_forest-clean | wine | random | 3 | 0.4366 | 0.4435 ± 0.0086 | — | 0.0 |
| models-random_forest-clean | housing | LOO | 3 | 41593.0207 | 41910.4177 ± 562.9694 | — | 650.2 |
| models-random_forest-clean | housing | Data-OOB | 3 | 41593.0207 | 42619.1964 ± 504.4043 | — | 1.2 |
| models-random_forest-clean | housing | high loss | 3 | 41593.0207 | 42370.5747 ± 522.7760 | — | 0.0 |
| models-random_forest-clean | housing | random | 3 | 41593.0207 | 42381.1282 ± 640.3464 | — | 0.0 |
| models-random_forest-clean | adult | LOO | 3 | 0.6673 | 0.6685 ± 0.0047 | — | 283.6 |
| models-random_forest-clean | adult | KNN-Shapley | 3 | 0.6673 | 0.6669 ± 0.0047 | — | 1.0 |
| models-random_forest-clean | adult | Data-OOB | 3 | 0.6673 | 0.6664 ± 0.0043 | — | 1.3 |
| models-random_forest-clean | adult | high loss | 3 | 0.6673 | 0.6610 ± 0.0089 | — | 0.0 |
| models-random_forest-clean | adult | random | 3 | 0.6673 | 0.6676 ± 0.0058 | — | 0.0 |
| models-random_forest-clean | covertype | LOO | 3 | 0.7335 | 0.7336 ± 0.0133 | — | 395.6 |
| models-random_forest-clean | covertype | KNN-Shapley | 3 | 0.7335 | 0.7314 ± 0.0124 | — | 1.6 |
| models-random_forest-clean | covertype | Data-OOB | 3 | 0.7335 | 0.7304 ± 0.0140 | — | 2.4 |
| models-random_forest-clean | covertype | high loss | 3 | 0.7335 | 0.7285 ± 0.0134 | — | 0.0 |
| models-random_forest-clean | covertype | random | 3 | 0.7335 | 0.7300 ± 0.0144 | — | 0.0 |
| models-random_forest-noise10 | wine | LOO | 3 | 0.4847 | 0.4879 ± 0.0217 | 0.5409 ± 0.0304 | 101.7 |
| models-random_forest-noise10 | wine | Data-OOB | 3 | 0.4847 | 0.4421 ± 0.0200 | 0.9836 ± 0.0090 | 0.9 |
| models-random_forest-noise10 | wine | high loss | 3 | 0.4847 | 0.4567 ± 0.0107 | 0.9753 ± 0.0147 | 0.0 |
| models-random_forest-noise10 | wine | random | 3 | 0.4847 | 0.4866 ± 0.0237 | 0.4761 ± 0.0454 | 0.0 |
| models-random_forest-noise10 | housing | LOO | 3 | 48792.6941 | 48627.0874 ± 426.0847 | 0.5308 ± 0.0086 | 665.7 |
| models-random_forest-noise10 | housing | Data-OOB | 3 | 48792.6941 | 42947.8972 ± 664.7835 | 0.9980 ± 0.0007 | 1.3 |
| models-random_forest-noise10 | housing | high loss | 3 | 48792.6941 | 43493.1624 ± 1411.9654 | 0.9963 ± 0.0014 | 0.0 |
| models-random_forest-noise10 | housing | random | 3 | 48792.6941 | 49200.6435 ± 900.6435 | 0.4892 ± 0.0417 | 0.0 |
| models-random_forest-noise10 | adult | LOO | 3 | 0.6671 | 0.6632 ± 0.0069 | 0.4941 ± 0.0252 | 282.3 |
| models-random_forest-noise10 | adult | KNN-Shapley | 3 | 0.6671 | 0.6655 ± 0.0065 | 0.8784 ± 0.0176 | 1.2 |
| models-random_forest-noise10 | adult | Data-OOB | 3 | 0.6671 | 0.6617 ± 0.0020 | 0.8960 ± 0.0080 | 1.5 |
| models-random_forest-noise10 | adult | high loss | 3 | 0.6671 | 0.6553 ± 0.0083 | 0.9305 ± 0.0042 | 0.0 |
| models-random_forest-noise10 | adult | random | 3 | 0.6671 | 0.6668 ± 0.0052 | 0.4892 ± 0.0417 | 0.0 |
| models-random_forest-noise10 | covertype | LOO | 3 | 0.7226 | 0.7177 ± 0.0119 | 0.4709 ± 0.0254 | 396.8 |
| models-random_forest-noise10 | covertype | KNN-Shapley | 3 | 0.7226 | 0.7184 ± 0.0104 | 0.9135 ± 0.0041 | 1.1 |
| models-random_forest-noise10 | covertype | Data-OOB | 3 | 0.7226 | 0.7217 ± 0.0163 | 0.9503 ± 0.0082 | 1.9 |
| models-random_forest-noise10 | covertype | high loss | 3 | 0.7226 | 0.7223 ± 0.0146 | 0.9328 ± 0.0091 | 0.0 |
| models-random_forest-noise10 | covertype | random | 3 | 0.7226 | 0.7149 ± 0.0161 | 0.4892 ± 0.0417 | 0.0 |
| models-xgboost-clean | wine | LOO | 3 | 0.4225 | 0.4059 ± 0.0139 | — | 199.2 |
| models-xgboost-clean | wine | Data-OOB | 3 | 0.4225 | 0.4261 ± 0.0331 | — | 1.0 |
| models-xgboost-clean | wine | high loss | 3 | 0.4225 | 0.4414 ± 0.0422 | — | 0.0 |
| models-xgboost-clean | wine | random | 3 | 0.4225 | 0.4221 ± 0.0239 | — | 0.0 |
| models-xgboost-clean | housing | LOO | 3 | 40226.0936 | 40728.0214 ± 946.4034 | — | 167.8 |
| models-xgboost-clean | housing | Data-OOB | 3 | 40226.0936 | 39670.3992 ± 575.4871 | — | 1.4 |
| models-xgboost-clean | housing | high loss | 3 | 40226.0936 | 40037.4435 ± 195.6966 | — | 0.0 |
| models-xgboost-clean | housing | random | 3 | 40226.0936 | 41589.0816 ± 393.3806 | — | 0.0 |
| models-xgboost-clean | adult | LOO | 3 | 0.6487 | 0.6469 ± 0.0069 | — | 163.1 |
| models-xgboost-clean | adult | KNN-Shapley | 3 | 0.6487 | 0.6637 ± 0.0156 | — | 1.1 |
| models-xgboost-clean | adult | Data-OOB | 3 | 0.6487 | 0.6657 ± 0.0044 | — | 1.3 |
| models-xgboost-clean | adult | high loss | 3 | 0.6487 | 0.6717 ± 0.0125 | — | 0.0 |
| models-xgboost-clean | adult | random | 3 | 0.6487 | 0.6491 ± 0.0156 | — | 0.0 |
| models-xgboost-clean | covertype | LOO | 3 | 0.6983 | 0.6959 ± 0.0072 | — | 626.2 |
| models-xgboost-clean | covertype | KNN-Shapley | 3 | 0.6983 | 0.7075 ± 0.0127 | — | 1.0 |
| models-xgboost-clean | covertype | Data-OOB | 3 | 0.6983 | 0.7021 ± 0.0156 | — | 1.6 |
| models-xgboost-clean | covertype | high loss | 3 | 0.6983 | 0.7007 ± 0.0132 | — | 0.0 |
| models-xgboost-clean | covertype | random | 3 | 0.6983 | 0.6939 ± 0.0124 | — | 0.0 |
| models-xgboost-noise10 | wine | LOO | 3 | 0.5612 | 0.5809 ± 0.0305 | 0.5362 ± 0.0327 | 383.8 |
| models-xgboost-noise10 | wine | Data-OOB | 3 | 0.5612 | 0.4410 ± 0.0152 | 0.9836 ± 0.0090 | 0.8 |
| models-xgboost-noise10 | wine | high loss | 3 | 0.5612 | 0.5336 ± 0.0353 | 0.5726 ± 0.0125 | 0.0 |
| models-xgboost-noise10 | wine | random | 3 | 0.5612 | 0.5730 ± 0.0387 | 0.4761 ± 0.0454 | 0.0 |
| models-xgboost-noise10 | housing | LOO | 3 | 66237.2478 | 66320.7728 ± 775.3525 | 0.5267 ± 0.0103 | 162.9 |
| models-xgboost-noise10 | housing | Data-OOB | 3 | 66237.2478 | 41842.8434 ± 521.5901 | 0.9980 ± 0.0007 | 1.4 |
| models-xgboost-noise10 | housing | high loss | 3 | 66237.2478 | 56368.0941 ± 1053.9627 | 0.8067 ± 0.0044 | 0.0 |
| models-xgboost-noise10 | housing | random | 3 | 66237.2478 | 66482.2355 ± 1279.2035 | 0.4892 ± 0.0417 | 0.0 |
| models-xgboost-noise10 | adult | LOO | 3 | 0.5817 | 0.5927 ± 0.0210 | 0.5083 ± 0.0261 | 170.5 |
| models-xgboost-noise10 | adult | KNN-Shapley | 3 | 0.5817 | 0.6404 ± 0.0061 | 0.8784 ± 0.0176 | 1.4 |
| models-xgboost-noise10 | adult | Data-OOB | 3 | 0.5817 | 0.6343 ± 0.0065 | 0.8960 ± 0.0080 | 1.7 |
| models-xgboost-noise10 | adult | high loss | 3 | 0.5817 | 0.6113 ± 0.0097 | 0.8272 ± 0.0104 | 0.0 |
| models-xgboost-noise10 | adult | random | 3 | 0.5817 | 0.5734 ± 0.0064 | 0.4892 ± 0.0417 | 0.0 |
| models-xgboost-noise10 | covertype | LOO | 3 | 0.6728 | 0.6659 ± 0.0087 | 0.5022 ± 0.0431 | 810.2 |
| models-xgboost-noise10 | covertype | KNN-Shapley | 3 | 0.6728 | 0.6785 ± 0.0147 | 0.9135 ± 0.0041 | 1.3 |
| models-xgboost-noise10 | covertype | Data-OOB | 3 | 0.6728 | 0.6811 ± 0.0147 | 0.9503 ± 0.0082 | 1.8 |
| models-xgboost-noise10 | covertype | high loss | 3 | 0.6728 | 0.6765 ± 0.0105 | 0.9191 ± 0.0146 | 0.0 |
| models-xgboost-noise10 | covertype | random | 3 | 0.6728 | 0.6694 ± 0.0092 | 0.4892 ± 0.0417 | 0.0 |
| noise20 | wine | Data-OOB | 3 | 0.5056 | 0.4935 ± 0.0419 | 0.9732 ± 0.0058 | 1.0 |
| noise20 | wine | Influence | 3 | 0.5056 | 0.4961 ± 0.0121 | 0.4961 ± 0.0252 | 0.6 |
| noise20 | wine | LiSSA | 3 | 0.5056 | 0.5141 ± 0.0229 | 0.5575 ± 0.0283 | 0.7 |
| noise20 | wine | high loss | 3 | 0.5056 | 0.5155 ± 0.0436 | 0.9802 ± 0.0070 | 0.0 |
| noise20 | wine | random | 3 | 0.5056 | 0.5160 ± 0.0104 | 0.4794 ± 0.0506 | 0.0 |
| noise20 | housing | Data-OOB | 3 | 50550.5692 | 51294.8265 ± 1133.1768 | 0.9962 ± 0.0003 | 1.5 |
| noise20 | housing | Influence | 3 | 50550.5692 | 48253.3746 ± 1480.8516 | 0.4946 ± 0.0167 | 3.4 |
| noise20 | housing | LiSSA | 3 | 50550.5692 | 53937.6870 ± 6455.2739 | 0.5283 ± 0.0444 | 1.4 |
| noise20 | housing | high loss | 3 | 50550.5692 | 54014.7546 ± 1291.1017 | 0.9969 ± 0.0013 | 0.0 |
| noise20 | housing | random | 3 | 50550.5692 | 49946.4273 ± 1183.8159 | 0.4947 ± 0.0238 | 0.0 |
| noise20 | adult | KNN-Shapley | 3 | 0.6620 | 0.6412 ± 0.0073 | 0.8774 ± 0.0091 | 1.2 |
| noise20 | adult | Data-OOB | 3 | 0.6620 | 0.6482 ± 0.0191 | 0.8575 ± 0.0149 | 1.6 |
| noise20 | adult | Influence | 3 | 0.6620 | 0.6526 ± 0.0043 | 0.5345 ± 0.0340 | 142.5 |
| noise20 | adult | LiSSA | 3 | 0.6620 | 0.6540 ± 0.0169 | 0.8450 ± 0.0584 | 7.5 |
| noise20 | adult | high loss | 3 | 0.6620 | 0.6595 ± 0.0175 | 0.9081 ± 0.0185 | 0.0 |
| noise20 | adult | random | 3 | 0.6620 | 0.6494 ± 0.0091 | 0.4947 ± 0.0238 | 0.0 |
| noise20 | covertype | KNN-Shapley | 3 | 0.6987 | 0.6997 ± 0.0150 | 0.9251 ± 0.0073 | 1.0 |
| noise20 | covertype | Data-OOB | 3 | 0.6987 | 0.7067 ± 0.0153 | 0.9487 ± 0.0018 | 1.8 |
| noise20 | covertype | LiSSA | 3 | 0.6987 | 0.6941 ± 0.0191 | 0.9150 ± 0.0075 | 12.5 |
| noise20 | covertype | high loss | 3 | 0.6987 | 0.6993 ± 0.0188 | 0.9466 ± 0.0077 | 0.0 |
| noise20 | covertype | random | 3 | 0.6987 | 0.6942 ± 0.0095 | 0.4947 ± 0.0238 | 0.0 |
| noise5 | wine | Data-OOB | 3 | 0.4813 | 0.4867 ± 0.0259 | 0.9821 ± 0.0164 | 1.0 |
| noise5 | wine | Influence | 3 | 0.4813 | 0.4793 ± 0.0378 | 0.5349 ± 0.0182 | 0.6 |
| noise5 | wine | LiSSA | 3 | 0.4813 | 0.4941 ± 0.0224 | 0.5750 ± 0.0948 | 0.7 |
| noise5 | wine | high loss | 3 | 0.4813 | 0.4853 ± 0.0294 | 0.9802 ± 0.0147 | 0.0 |
| noise5 | wine | random | 3 | 0.4813 | 0.4784 ± 0.0489 | 0.5127 ± 0.0338 | 0.0 |
| noise5 | housing | Data-OOB | 3 | 45068.6262 | 44625.1134 ± 1240.5624 | 0.9982 ± 0.0014 | 1.3 |
| noise5 | housing | Influence | 3 | 45068.6262 | 45579.4030 ± 977.5264 | 0.5083 ± 0.0281 | 4.5 |
| noise5 | housing | LiSSA | 3 | 45068.6262 | 45770.4993 ± 2368.8730 | 0.5822 ± 0.0622 | 1.3 |
| noise5 | housing | high loss | 3 | 45068.6262 | 44212.9648 ± 1384.0100 | 0.9984 ± 0.0013 | 0.0 |
| noise5 | housing | random | 3 | 45068.6262 | 46783.3902 ± 400.5950 | 0.5266 ± 0.0503 | 0.0 |
| noise5 | adult | KNN-Shapley | 3 | 0.6730 | 0.6575 ± 0.0156 | 0.8711 ± 0.0108 | 1.2 |
| noise5 | adult | Data-OOB | 3 | 0.6730 | 0.6662 ± 0.0042 | 0.9184 ± 0.0172 | 1.5 |
| noise5 | adult | Influence | 3 | 0.6730 | 0.6689 ± 0.0080 | 0.5060 ± 0.0359 | 168.9 |
| noise5 | adult | LiSSA | 3 | 0.6730 | 0.6599 ± 0.0052 | 0.8381 ± 0.0666 | 7.0 |
| noise5 | adult | high loss | 3 | 0.6730 | 0.6688 ± 0.0077 | 0.9281 ± 0.0026 | 0.0 |
| noise5 | adult | random | 3 | 0.6730 | 0.6750 ± 0.0157 | 0.5266 ± 0.0503 | 0.0 |
| noise5 | covertype | KNN-Shapley | 3 | 0.7113 | 0.7119 ± 0.0089 | 0.9266 ± 0.0143 | 1.0 |
| noise5 | covertype | Data-OOB | 3 | 0.7113 | 0.7185 ± 0.0106 | 0.9587 ± 0.0146 | 1.8 |
| noise5 | covertype | LiSSA | 3 | 0.7113 | 0.7089 ± 0.0075 | 0.7922 ± 0.1027 | 13.2 |
| noise5 | covertype | high loss | 3 | 0.7113 | 0.7125 ± 0.0074 | 0.9521 ± 0.0101 | 0.0 |
| noise5 | covertype | random | 3 | 0.7113 | 0.7123 ± 0.0067 | 0.5266 ± 0.0503 | 0.0 |
| sysnoise10 | wine | Data-OOB | 3 | 0.5540 | 0.5462 ± 0.0231 | 0.6346 ± 0.0192 | 0.9 |
| sysnoise10 | wine | Influence | 3 | 0.5540 | 0.5278 ± 0.0176 | 0.5183 ± 0.1847 | 0.6 |
| sysnoise10 | wine | LiSSA | 3 | 0.5540 | 0.4813 ± 0.0298 | 0.8988 ± 0.0481 | 0.7 |
| sysnoise10 | wine | high loss | 3 | 0.5540 | 0.5325 ± 0.0099 | 0.8350 ± 0.0723 | 0.0 |
| sysnoise10 | wine | random | 3 | 0.5540 | 0.5563 ± 0.0070 | 0.5139 ± 0.0139 | 0.0 |
| sysnoise10 | housing | Data-OOB | 3 | 56041.0214 | 57535.1055 ± 2387.9255 | 0.5819 ± 0.0385 | 1.4 |
| sysnoise10 | housing | Influence | 3 | 56041.0214 | 54389.5176 ± 2155.9350 | 0.6153 ± 0.0681 | 3.7 |
| sysnoise10 | housing | LiSSA | 3 | 56041.0214 | 45475.4913 ± 155.4617 | 0.9285 ± 0.0144 | 1.4 |
| sysnoise10 | housing | high loss | 3 | 56041.0214 | 52888.0665 ± 2771.4010 | 0.8591 ± 0.0121 | 0.0 |
| sysnoise10 | housing | random | 3 | 56041.0214 | 56796.3272 ± 2548.1254 | 0.5012 ± 0.0167 | 0.0 |
| sysnoise10 | adult | KNN-Shapley | 3 | 0.6626 | 0.6581 ± 0.0199 | 0.9472 ± 0.0033 | 1.2 |
| sysnoise10 | adult | Data-OOB | 3 | 0.6626 | 0.6570 ± 0.0154 | 0.9020 ± 0.0070 | 1.4 |
| sysnoise10 | adult | Influence | 3 | 0.6626 | 0.6621 ± 0.0081 | 0.5119 ± 0.0254 | 165.4 |
| sysnoise10 | adult | LiSSA | 3 | 0.6626 | 0.6654 ± 0.0009 | 0.9641 ± 0.0044 | 7.3 |
| sysnoise10 | adult | high loss | 3 | 0.6626 | 0.6516 ± 0.0255 | 0.9217 ± 0.0096 | 0.0 |
| sysnoise10 | adult | random | 3 | 0.6626 | 0.6586 ± 0.0188 | 0.5092 ± 0.0339 | 0.0 |
| sysnoise10 | covertype | KNN-Shapley | 3 | 0.7076 | 0.7090 ± 0.0138 | 0.7775 ± 0.0179 | 1.1 |
| sysnoise10 | covertype | Data-OOB | 3 | 0.7076 | 0.7081 ± 0.0108 | 0.7289 ± 0.0142 | 1.8 |
| sysnoise10 | covertype | LiSSA | 3 | 0.7076 | 0.7009 ± 0.0135 | 0.6129 ± 0.4449 | 9.7 |
| sysnoise10 | covertype | high loss | 3 | 0.7076 | 0.7074 ± 0.0133 | 0.7735 ± 0.0231 | 0.0 |
| sysnoise10 | covertype | random | 3 | 0.7076 | 0.6941 ± 0.0188 | 0.4946 ± 0.0383 | 0.0 |
| sysnoise20 | wine | Data-OOB | 3 | 0.5767 | 0.5820 ± 0.0298 | 0.5870 ± 0.0418 | 0.9 |
| sysnoise20 | wine | Influence | 3 | 0.5767 | 0.5568 ± 0.0086 | 0.6537 ± 0.1981 | 0.6 |
| sysnoise20 | wine | LiSSA | 3 | 0.5767 | 0.5321 ± 0.0091 | 0.9567 ± 0.0185 | 0.7 |
| sysnoise20 | wine | high loss | 3 | 0.5767 | 0.5434 ± 0.0120 | 0.8492 ± 0.0351 | 0.0 |
| sysnoise20 | wine | random | 3 | 0.5767 | 0.5757 ± 0.0168 | 0.5047 ± 0.0093 | 0.0 |
| sysnoise20 | housing | Data-OOB | 3 | 70847.7558 | 67374.9094 ± 987.2716 | 0.6667 ± 0.0409 | 1.4 |
| sysnoise20 | housing | Influence | 3 | 70847.7558 | 67979.8437 ± 1420.1666 | 0.6066 ± 0.0988 | 4.0 |
| sysnoise20 | housing | LiSSA | 3 | 70847.7558 | 59445.2091 ± 766.8292 | 0.9059 ± 0.0795 | 1.4 |
| sysnoise20 | housing | high loss | 3 | 70847.7558 | 63163.9810 ± 2567.4328 | 0.7764 ± 0.1149 | 0.0 |
| sysnoise20 | housing | random | 3 | 70847.7558 | 72485.4130 ± 1506.6502 | 0.5024 ± 0.0073 | 0.0 |
| sysnoise20 | adult | KNN-Shapley | 3 | 0.6495 | 0.6472 ± 0.0037 | 0.9395 ± 0.0041 | 1.1 |
| sysnoise20 | adult | Data-OOB | 3 | 0.6495 | 0.6535 ± 0.0011 | 0.8035 ± 0.0064 | 1.6 |
| sysnoise20 | adult | Influence | 3 | 0.6495 | 0.6525 ± 0.0038 | 0.5456 ± 0.0425 | 149.8 |
| sysnoise20 | adult | LiSSA | 3 | 0.6495 | 0.6438 ± 0.0102 | 0.9291 ± 0.0495 | 8.0 |
| sysnoise20 | adult | high loss | 3 | 0.6495 | 0.6463 ± 0.0056 | 0.8498 ± 0.0161 | 0.0 |
| sysnoise20 | adult | random | 3 | 0.6495 | 0.6555 ± 0.0039 | 0.5044 ± 0.0180 | 0.0 |
| sysnoise20 | covertype | KNN-Shapley | 3 | 0.6627 | 0.6620 ± 0.0039 | 0.7519 ± 0.0164 | 1.0 |
| sysnoise20 | covertype | Data-OOB | 3 | 0.6627 | 0.6669 ± 0.0073 | 0.5567 ± 0.0116 | 1.7 |
| sysnoise20 | covertype | LiSSA | 3 | 0.6627 | 0.6511 ± 0.0212 | 0.8945 ± 0.0054 | 9.5 |
| sysnoise20 | covertype | high loss | 3 | 0.6627 | 0.6607 ± 0.0116 | 0.6868 ± 0.0524 | 0.0 |
| sysnoise20 | covertype | random | 3 | 0.6627 | 0.6101 ± 0.0059 | 0.4793 ± 0.0091 | 0.0 |
| sysnoise5 | wine | Data-OOB | 3 | 0.5142 | 0.5260 ± 0.0260 | 0.6761 ± 0.1000 | 0.9 |
| sysnoise5 | wine | Influence | 3 | 0.5142 | 0.5092 ± 0.0338 | 0.6044 ± 0.0380 | 0.6 |
| sysnoise5 | wine | LiSSA | 3 | 0.5142 | 0.4807 ± 0.0265 | 0.8218 ± 0.0884 | 0.6 |
| sysnoise5 | wine | high loss | 3 | 0.5142 | 0.5136 ± 0.0257 | 0.7844 ± 0.0396 | 0.0 |
| sysnoise5 | wine | random | 3 | 0.5142 | 0.5156 ± 0.0277 | 0.5519 ± 0.0157 | 0.0 |
| sysnoise5 | housing | Data-OOB | 3 | 49587.5445 | 49801.3655 ± 2088.9499 | 0.4858 ± 0.0572 | 1.3 |
| sysnoise5 | housing | Influence | 3 | 49587.5445 | 47398.0389 ± 1154.1796 | 0.6505 ± 0.1042 | 3.6 |
| sysnoise5 | housing | LiSSA | 3 | 49587.5445 | 45378.9372 ± 589.2520 | 0.9268 ± 0.0319 | 1.4 |
| sysnoise5 | housing | high loss | 3 | 49587.5445 | 46160.8283 ± 1356.8631 | 0.9133 ± 0.0140 | 0.0 |
| sysnoise5 | housing | random | 3 | 49587.5445 | 49444.6810 ± 2112.4467 | 0.5031 ± 0.0200 | 0.0 |
| sysnoise5 | adult | KNN-Shapley | 3 | 0.6738 | 0.6627 ± 0.0139 | 0.9426 ± 0.0048 | 1.3 |
| sysnoise5 | adult | Data-OOB | 3 | 0.6738 | 0.6703 ± 0.0089 | 0.9189 ± 0.0108 | 1.6 |
| sysnoise5 | adult | Influence | 3 | 0.6738 | 0.6676 ± 0.0151 | 0.5193 ± 0.0271 | 133.0 |
| sysnoise5 | adult | LiSSA | 3 | 0.6738 | 0.6565 ± 0.0049 | 0.9386 ± 0.0338 | 6.6 |
| sysnoise5 | adult | high loss | 3 | 0.6738 | 0.6694 ± 0.0086 | 0.9303 ± 0.0139 | 0.0 |
| sysnoise5 | adult | random | 3 | 0.6738 | 0.6703 ± 0.0201 | 0.4846 ± 0.0238 | 0.0 |
| sysnoise5 | covertype | KNN-Shapley | 3 | 0.7087 | 0.7094 ± 0.0112 | 0.7929 ± 0.0293 | 1.1 |
| sysnoise5 | covertype | Data-OOB | 3 | 0.7087 | 0.7209 ± 0.0143 | 0.8181 ± 0.0227 | 1.7 |
| sysnoise5 | covertype | LiSSA | 3 | 0.7087 | 0.7001 ± 0.0065 | 0.7237 ± 0.3067 | 8.5 |
| sysnoise5 | covertype | high loss | 3 | 0.7087 | 0.7159 ± 0.0144 | 0.8243 ± 0.0319 | 0.0 |
| sysnoise5 | covertype | random | 3 | 0.7087 | 0.7137 ± 0.0061 | 0.5153 ± 0.0331 | 0.0 |
| transfer-catboost | wine | any.DataOOB | 3 | 0.5037 | 0.4959 ± 0.0178 | — | 0.0 |
| transfer-catboost | wine | catboost.CatBoostLFC | 3 | 0.5037 | 0.4966 ± 0.0225 | — | 0.0 |
| transfer-catboost | wine | catboost.LOO | 3 | 0.5037 | 0.5199 ± 0.0280 | — | 0.0 |
| transfer-catboost | wine | catboost.LossHigh | 3 | 0.5037 | 0.4937 ± 0.0162 | — | 0.0 |
| transfer-catboost | wine | distill-lightgbm.Influence | 3 | 0.5037 | 0.5064 ± 0.0166 | — | 0.0 |
| transfer-catboost | wine | distill-lightgbm.LossHigh | 3 | 0.5037 | 0.4980 ± 0.0200 | — | 0.0 |
| transfer-catboost | wine | lightgbm.LOO | 3 | 0.5037 | 0.4976 ± 0.0241 | — | 0.0 |
| transfer-catboost | wine | lightgbm.LossHigh | 3 | 0.5037 | 0.4974 ± 0.0206 | — | 0.0 |
| transfer-catboost | wine | pytorch.Influence | 3 | 0.5037 | 0.5008 ± 0.0166 | — | 0.0 |
| transfer-catboost | wine | pytorch.LOO | 3 | 0.5037 | 0.4951 ± 0.0224 | — | 0.0 |
| transfer-catboost | wine | pytorch.LissaInfluence | 3 | 0.5037 | 0.4878 ± 0.0199 | — | 0.0 |
| transfer-catboost | wine | pytorch.LossHigh | 3 | 0.5037 | 0.4964 ± 0.0239 | — | 0.0 |
| transfer-catboost | wine | random_forest.LOO | 3 | 0.5037 | 0.4976 ± 0.0211 | — | 0.0 |
| transfer-catboost | wine | random_forest.LossHigh | 3 | 0.5037 | 0.4975 ± 0.0226 | — | 0.0 |
| transfer-catboost | wine | xgboost.LOO | 3 | 0.5037 | 0.4975 ± 0.0296 | — | 0.0 |
| transfer-catboost | wine | xgboost.LossHigh | 3 | 0.5037 | 0.5125 ± 0.0172 | — | 0.0 |
| transfer-catboost | wine | random | 3 | 0.5037 | 0.4993 ± 0.0180 | — | 0.0 |
| transfer-catboost | housing | any.DataOOB | 3 | 47002.3729 | 47061.7218 ± 970.4177 | — | 0.0 |
| transfer-catboost | housing | catboost.CatBoostLFC | 3 | 47002.3729 | 47923.3371 ± 739.6269 | — | 0.0 |
| transfer-catboost | housing | catboost.LOO | 3 | 47002.3729 | 47301.4437 ± 603.6063 | — | 0.0 |
| transfer-catboost | housing | catboost.LossHigh | 3 | 47002.3729 | 47135.9689 ± 993.2007 | — | 0.0 |
| transfer-catboost | housing | distill-lightgbm.Influence | 3 | 47002.3729 | 47953.8944 ± 834.0656 | — | 0.0 |
| transfer-catboost | housing | distill-lightgbm.LossHigh | 3 | 47002.3729 | 47038.0384 ± 985.9623 | — | 0.0 |
| transfer-catboost | housing | lightgbm.LOO | 3 | 47002.3729 | 47429.5772 ± 1047.7461 | — | 0.0 |
| transfer-catboost | housing | lightgbm.LossHigh | 3 | 47002.3729 | 47014.3580 ± 964.2764 | — | 0.0 |
| transfer-catboost | housing | pytorch.Influence | 3 | 47002.3729 | 47609.5063 ± 810.7341 | — | 0.0 |
| transfer-catboost | housing | pytorch.LOO | 3 | 47002.3729 | 47593.4375 ± 1050.9735 | — | 0.0 |
| transfer-catboost | housing | pytorch.LissaInfluence | 3 | 47002.3729 | 46889.5633 ± 765.9915 | — | 0.0 |
| transfer-catboost | housing | pytorch.LossHigh | 3 | 47002.3729 | 46948.4976 ± 973.7563 | — | 0.0 |
| transfer-catboost | housing | random_forest.LOO | 3 | 47002.3729 | 47349.3558 ± 1020.3987 | — | 0.0 |
| transfer-catboost | housing | random_forest.LossHigh | 3 | 47002.3729 | 47084.0136 ± 923.3662 | — | 0.0 |
| transfer-catboost | housing | xgboost.LOO | 3 | 47002.3729 | 47691.4764 ± 1143.0695 | — | 0.0 |
| transfer-catboost | housing | xgboost.LossHigh | 3 | 47002.3729 | 47702.6913 ± 944.7530 | — | 0.0 |
| transfer-catboost | housing | random | 3 | 47002.3729 | 47689.9675 ± 1417.9551 | — | 0.0 |
| transfer-catboost | adult | any.DataOOB | 3 | 0.6643 | 0.6600 ± 0.0046 | — | 0.0 |
| transfer-catboost | adult | any.KNNShapley | 3 | 0.6643 | 0.6558 ± 0.0094 | — | 0.0 |
| transfer-catboost | adult | catboost.CatBoostLFC | 3 | 0.6643 | 0.6672 ± 0.0070 | — | 0.0 |
| transfer-catboost | adult | catboost.LOO | 3 | 0.6643 | 0.6598 ± 0.0091 | — | 0.0 |
| transfer-catboost | adult | catboost.LossHigh | 3 | 0.6643 | 0.6619 ± 0.0056 | — | 0.0 |
| transfer-catboost | adult | distill-lightgbm.Influence | 3 | 0.6643 | 0.6631 ± 0.0048 | — | 0.0 |
| transfer-catboost | adult | distill-lightgbm.LossHigh | 3 | 0.6643 | 0.6613 ± 0.0021 | — | 0.0 |
| transfer-catboost | adult | lightgbm.LOO | 3 | 0.6643 | 0.6607 ± 0.0117 | — | 0.0 |
| transfer-catboost | adult | lightgbm.LossHigh | 3 | 0.6643 | 0.6634 ± 0.0049 | — | 0.0 |
| transfer-catboost | adult | pytorch.Influence | 3 | 0.6643 | 0.6686 ± 0.0121 | — | 0.0 |
| transfer-catboost | adult | pytorch.LOO | 3 | 0.6643 | 0.6593 ± 0.0059 | — | 0.0 |
| transfer-catboost | adult | pytorch.LissaInfluence | 3 | 0.6643 | 0.6656 ± 0.0090 | — | 0.0 |
| transfer-catboost | adult | pytorch.LossHigh | 3 | 0.6643 | 0.6588 ± 0.0016 | — | 0.0 |
| transfer-catboost | adult | random_forest.LOO | 3 | 0.6643 | 0.6639 ± 0.0092 | — | 0.0 |
| transfer-catboost | adult | random_forest.LossHigh | 3 | 0.6643 | 0.6584 ± 0.0045 | — | 0.0 |
| transfer-catboost | adult | xgboost.LOO | 3 | 0.6643 | 0.6606 ± 0.0066 | — | 0.0 |
| transfer-catboost | adult | xgboost.LossHigh | 3 | 0.6643 | 0.6634 ± 0.0061 | — | 0.0 |
| transfer-catboost | adult | random | 3 | 0.6643 | 0.6621 ± 0.0011 | — | 0.0 |
| transfer-catboost | covertype | any.DataOOB | 3 | 0.6827 | 0.6892 ± 0.0108 | — | 0.0 |
| transfer-catboost | covertype | any.KNNShapley | 3 | 0.6827 | 0.6887 ± 0.0151 | — | 0.0 |
| transfer-catboost | covertype | catboost.LOO | 3 | 0.6827 | 0.6832 ± 0.0095 | — | 0.0 |
| transfer-catboost | covertype | catboost.LossHigh | 3 | 0.6827 | 0.6885 ± 0.0123 | — | 0.0 |
| transfer-catboost | covertype | distill-lightgbm.Influence | 3 | 0.6827 | 0.6877 ± 0.0140 | — | 0.0 |
| transfer-catboost | covertype | distill-lightgbm.LossHigh | 3 | 0.6827 | 0.6921 ± 0.0082 | — | 0.0 |
| transfer-catboost | covertype | lightgbm.LOO | 3 | 0.6827 | 0.6741 ± 0.0088 | — | 0.0 |
| transfer-catboost | covertype | lightgbm.LossHigh | 3 | 0.6827 | 0.6879 ± 0.0085 | — | 0.0 |
| transfer-catboost | covertype | pytorch.Influence | 3 | 0.6827 | 0.6838 ± 0.0053 | — | 0.0 |
| transfer-catboost | covertype | pytorch.LOO | 3 | 0.6827 | 0.6843 ± 0.0108 | — | 0.0 |
| transfer-catboost | covertype | pytorch.LissaInfluence | 3 | 0.6827 | 0.6859 ± 0.0232 | — | 0.0 |
| transfer-catboost | covertype | pytorch.LossHigh | 3 | 0.6827 | 0.6929 ± 0.0158 | — | 0.0 |
| transfer-catboost | covertype | random_forest.LOO | 3 | 0.6827 | 0.6851 ± 0.0103 | — | 0.0 |
| transfer-catboost | covertype | random_forest.LossHigh | 3 | 0.6827 | 0.6851 ± 0.0103 | — | 0.0 |
| transfer-catboost | covertype | xgboost.LOO | 3 | 0.6827 | 0.6812 ± 0.0110 | — | 0.0 |
| transfer-catboost | covertype | xgboost.LossHigh | 3 | 0.6827 | 0.6853 ± 0.0070 | — | 0.0 |
| transfer-catboost | covertype | random | 3 | 0.6827 | 0.6815 ± 0.0078 | — | 0.0 |
| transfer-distill-lightgbm | wine | any.DataOOB | 3 | 0.4810 | 0.4755 ± 0.0226 | — | 0.0 |
| transfer-distill-lightgbm | wine | catboost.CatBoostLFC | 3 | 0.4810 | 0.4912 ± 0.0214 | — | 0.0 |
| transfer-distill-lightgbm | wine | catboost.LOO | 3 | 0.4810 | 0.4934 ± 0.0289 | — | 0.0 |
| transfer-distill-lightgbm | wine | catboost.LossHigh | 3 | 0.4810 | 0.4809 ± 0.0251 | — | 0.0 |
| transfer-distill-lightgbm | wine | distill-lightgbm.Influence | 3 | 0.4810 | 0.4868 ± 0.0186 | — | 0.0 |
| transfer-distill-lightgbm | wine | distill-lightgbm.LossHigh | 3 | 0.4810 | 0.4740 ± 0.0250 | — | 0.0 |
| transfer-distill-lightgbm | wine | lightgbm.LOO | 3 | 0.4810 | 0.4991 ± 0.0145 | — | 0.0 |
| transfer-distill-lightgbm | wine | lightgbm.LossHigh | 3 | 0.4810 | 0.4714 ± 0.0201 | — | 0.0 |
| transfer-distill-lightgbm | wine | pytorch.Influence | 3 | 0.4810 | 0.4910 ± 0.0230 | — | 0.0 |
| transfer-distill-lightgbm | wine | pytorch.LOO | 3 | 0.4810 | 0.4748 ± 0.0282 | — | 0.0 |
| transfer-distill-lightgbm | wine | pytorch.LissaInfluence | 3 | 0.4810 | 0.4779 ± 0.0223 | — | 0.0 |
| transfer-distill-lightgbm | wine | pytorch.LossHigh | 3 | 0.4810 | 0.4670 ± 0.0320 | — | 0.0 |
| transfer-distill-lightgbm | wine | random_forest.LOO | 3 | 0.4810 | 0.4809 ± 0.0148 | — | 0.0 |
| transfer-distill-lightgbm | wine | random_forest.LossHigh | 3 | 0.4810 | 0.4773 ± 0.0116 | — | 0.0 |
| transfer-distill-lightgbm | wine | xgboost.LOO | 3 | 0.4810 | 0.4894 ± 0.0373 | — | 0.0 |
| transfer-distill-lightgbm | wine | xgboost.LossHigh | 3 | 0.4810 | 0.4739 ± 0.0148 | — | 0.0 |
| transfer-distill-lightgbm | wine | random | 3 | 0.4810 | 0.4710 ± 0.0231 | — | 0.0 |
| transfer-distill-lightgbm | housing | any.DataOOB | 3 | 47517.2028 | 43210.6704 ± 1255.4420 | — | 0.0 |
| transfer-distill-lightgbm | housing | catboost.CatBoostLFC | 3 | 47517.2028 | 50474.0172 ± 830.8795 | — | 0.0 |
| transfer-distill-lightgbm | housing | catboost.LOO | 3 | 47517.2028 | 47586.5729 ± 1547.1949 | — | 0.0 |
| transfer-distill-lightgbm | housing | catboost.LossHigh | 3 | 47517.2028 | 44401.6377 ± 1033.7425 | — | 0.0 |
| transfer-distill-lightgbm | housing | distill-lightgbm.Influence | 3 | 47517.2028 | 46505.0418 ± 1052.8192 | — | 0.0 |
| transfer-distill-lightgbm | housing | distill-lightgbm.LossHigh | 3 | 47517.2028 | 43850.1851 ± 648.8749 | — | 0.0 |
| transfer-distill-lightgbm | housing | lightgbm.LOO | 3 | 47517.2028 | 47955.2113 ± 1590.5166 | — | 0.0 |
| transfer-distill-lightgbm | housing | lightgbm.LossHigh | 3 | 47517.2028 | 44363.0522 ± 792.9426 | — | 0.0 |
| transfer-distill-lightgbm | housing | pytorch.Influence | 3 | 47517.2028 | 47918.4097 ± 698.9683 | — | 0.0 |
| transfer-distill-lightgbm | housing | pytorch.LOO | 3 | 47517.2028 | 47484.5702 ± 593.4444 | — | 0.0 |
| transfer-distill-lightgbm | housing | pytorch.LissaInfluence | 3 | 47517.2028 | 49647.8706 ± 2887.3722 | — | 0.0 |
| transfer-distill-lightgbm | housing | pytorch.LossHigh | 3 | 47517.2028 | 43807.6099 ± 829.0554 | — | 0.0 |
| transfer-distill-lightgbm | housing | random_forest.LOO | 3 | 47517.2028 | 47179.2001 ± 767.2284 | — | 0.0 |
| transfer-distill-lightgbm | housing | random_forest.LossHigh | 3 | 47517.2028 | 44297.3165 ± 567.0238 | — | 0.0 |
| transfer-distill-lightgbm | housing | xgboost.LOO | 3 | 47517.2028 | 48228.6030 ± 1341.2741 | — | 0.0 |
| transfer-distill-lightgbm | housing | xgboost.LossHigh | 3 | 47517.2028 | 46675.0029 ± 707.8909 | — | 0.0 |
| transfer-distill-lightgbm | housing | random | 3 | 47517.2028 | 48764.5601 ± 414.3844 | — | 0.0 |
| transfer-distill-lightgbm | adult | any.DataOOB | 3 | 0.6546 | 0.6567 ± 0.0077 | — | 0.0 |
| transfer-distill-lightgbm | adult | any.KNNShapley | 3 | 0.6546 | 0.6570 ± 0.0123 | — | 0.0 |
| transfer-distill-lightgbm | adult | catboost.CatBoostLFC | 3 | 0.6546 | 0.6647 ± 0.0099 | — | 0.0 |
| transfer-distill-lightgbm | adult | catboost.LOO | 3 | 0.6546 | 0.6508 ± 0.0086 | — | 0.0 |
| transfer-distill-lightgbm | adult | catboost.LossHigh | 3 | 0.6546 | 0.6641 ± 0.0054 | — | 0.0 |
| transfer-distill-lightgbm | adult | distill-lightgbm.Influence | 3 | 0.6546 | 0.6539 ± 0.0024 | — | 0.0 |
| transfer-distill-lightgbm | adult | distill-lightgbm.LossHigh | 3 | 0.6546 | 0.6627 ± 0.0101 | — | 0.0 |
| transfer-distill-lightgbm | adult | lightgbm.LOO | 3 | 0.6546 | 0.6581 ± 0.0060 | — | 0.0 |
| transfer-distill-lightgbm | adult | lightgbm.LossHigh | 3 | 0.6546 | 0.6567 ± 0.0068 | — | 0.0 |
| transfer-distill-lightgbm | adult | pytorch.Influence | 3 | 0.6546 | 0.6675 ± 0.0081 | — | 0.0 |
| transfer-distill-lightgbm | adult | pytorch.LOO | 3 | 0.6546 | 0.6494 ± 0.0122 | — | 0.0 |
| transfer-distill-lightgbm | adult | pytorch.LissaInfluence | 3 | 0.6546 | 0.6586 ± 0.0091 | — | 0.0 |
| transfer-distill-lightgbm | adult | pytorch.LossHigh | 3 | 0.6546 | 0.6624 ± 0.0101 | — | 0.0 |
| transfer-distill-lightgbm | adult | random_forest.LOO | 3 | 0.6546 | 0.6534 ± 0.0109 | — | 0.0 |
| transfer-distill-lightgbm | adult | random_forest.LossHigh | 3 | 0.6546 | 0.6604 ± 0.0146 | — | 0.0 |
| transfer-distill-lightgbm | adult | xgboost.LOO | 3 | 0.6546 | 0.6459 ± 0.0166 | — | 0.0 |
| transfer-distill-lightgbm | adult | xgboost.LossHigh | 3 | 0.6546 | 0.6603 ± 0.0082 | — | 0.0 |
| transfer-distill-lightgbm | adult | random | 3 | 0.6546 | 0.6566 ± 0.0115 | — | 0.0 |
| transfer-distill-lightgbm | covertype | any.DataOOB | 3 | 0.7166 | 0.7168 ± 0.0142 | — | 0.0 |
| transfer-distill-lightgbm | covertype | any.KNNShapley | 3 | 0.7166 | 0.7101 ± 0.0129 | — | 0.0 |
| transfer-distill-lightgbm | covertype | catboost.LOO | 3 | 0.7166 | 0.7135 ± 0.0080 | — | 0.0 |
| transfer-distill-lightgbm | covertype | catboost.LossHigh | 3 | 0.7166 | 0.7175 ± 0.0138 | — | 0.0 |
| transfer-distill-lightgbm | covertype | distill-lightgbm.Influence | 3 | 0.7166 | 0.7107 ± 0.0108 | — | 0.0 |
| transfer-distill-lightgbm | covertype | distill-lightgbm.LossHigh | 3 | 0.7166 | 0.7133 ± 0.0090 | — | 0.0 |
| transfer-distill-lightgbm | covertype | lightgbm.LOO | 3 | 0.7166 | 0.7129 ± 0.0130 | — | 0.0 |
| transfer-distill-lightgbm | covertype | lightgbm.LossHigh | 3 | 0.7166 | 0.7126 ± 0.0157 | — | 0.0 |
| transfer-distill-lightgbm | covertype | pytorch.Influence | 3 | 0.7166 | 0.7050 ± 0.0098 | — | 0.0 |
| transfer-distill-lightgbm | covertype | pytorch.LOO | 3 | 0.7166 | 0.7117 ± 0.0050 | — | 0.0 |
| transfer-distill-lightgbm | covertype | pytorch.LissaInfluence | 3 | 0.7166 | 0.7009 ± 0.0072 | — | 0.0 |
| transfer-distill-lightgbm | covertype | pytorch.LossHigh | 3 | 0.7166 | 0.7193 ± 0.0090 | — | 0.0 |
| transfer-distill-lightgbm | covertype | random_forest.LOO | 3 | 0.7166 | 0.7151 ± 0.0077 | — | 0.0 |
| transfer-distill-lightgbm | covertype | random_forest.LossHigh | 3 | 0.7166 | 0.7125 ± 0.0073 | — | 0.0 |
| transfer-distill-lightgbm | covertype | xgboost.LOO | 3 | 0.7166 | 0.7189 ± 0.0054 | — | 0.0 |
| transfer-distill-lightgbm | covertype | xgboost.LossHigh | 3 | 0.7166 | 0.7147 ± 0.0126 | — | 0.0 |
| transfer-distill-lightgbm | covertype | random | 3 | 0.7166 | 0.7155 ± 0.0085 | — | 0.0 |
| transfer-lightgbm | wine | any.DataOOB | 3 | 0.4998 | 0.4583 ± 0.0337 | — | 0.0 |
| transfer-lightgbm | wine | catboost.CatBoostLFC | 3 | 0.4998 | 0.4963 ± 0.0165 | — | 0.0 |
| transfer-lightgbm | wine | catboost.LOO | 3 | 0.4998 | 0.5096 ± 0.0286 | — | 0.0 |
| transfer-lightgbm | wine | catboost.LossHigh | 3 | 0.4998 | 0.4498 ± 0.0128 | — | 0.0 |
| transfer-lightgbm | wine | distill-lightgbm.Influence | 3 | 0.4998 | 0.4867 ± 0.0213 | — | 0.0 |
| transfer-lightgbm | wine | distill-lightgbm.LossHigh | 3 | 0.4998 | 0.4444 ± 0.0485 | — | 0.0 |
| transfer-lightgbm | wine | lightgbm.LOO | 3 | 0.4998 | 0.4917 ± 0.0149 | — | 0.0 |
| transfer-lightgbm | wine | lightgbm.LossHigh | 3 | 0.4998 | 0.4513 ± 0.0328 | — | 0.0 |
| transfer-lightgbm | wine | pytorch.Influence | 3 | 0.4998 | 0.4923 ± 0.0373 | — | 0.0 |
| transfer-lightgbm | wine | pytorch.LOO | 3 | 0.4998 | 0.4909 ± 0.0081 | — | 0.0 |
| transfer-lightgbm | wine | pytorch.LissaInfluence | 3 | 0.4998 | 0.4704 ± 0.0247 | — | 0.0 |
| transfer-lightgbm | wine | pytorch.LossHigh | 3 | 0.4998 | 0.4291 ± 0.0334 | — | 0.0 |
| transfer-lightgbm | wine | random_forest.LOO | 3 | 0.4998 | 0.5072 ± 0.0253 | — | 0.0 |
| transfer-lightgbm | wine | random_forest.LossHigh | 3 | 0.4998 | 0.4674 ± 0.0170 | — | 0.0 |
| transfer-lightgbm | wine | xgboost.LOO | 3 | 0.4998 | 0.4891 ± 0.0182 | — | 0.0 |
| transfer-lightgbm | wine | xgboost.LossHigh | 3 | 0.4998 | 0.4844 ± 0.0223 | — | 0.0 |
| transfer-lightgbm | wine | random | 3 | 0.4998 | 0.4791 ± 0.0289 | — | 0.0 |
| transfer-lightgbm | housing | any.DataOOB | 3 | 49157.8074 | 39021.8209 ± 353.1227 | — | 0.0 |
| transfer-lightgbm | housing | catboost.CatBoostLFC | 3 | 49157.8074 | 52292.2729 ± 1275.4065 | — | 0.0 |
| transfer-lightgbm | housing | catboost.LOO | 3 | 49157.8074 | 49909.7770 ± 1729.9040 | — | 0.0 |
| transfer-lightgbm | housing | catboost.LossHigh | 3 | 49157.8074 | 40371.0207 ± 971.1057 | — | 0.0 |
| transfer-lightgbm | housing | distill-lightgbm.Influence | 3 | 49157.8074 | 48477.0472 ± 1082.7413 | — | 0.0 |
| transfer-lightgbm | housing | distill-lightgbm.LossHigh | 3 | 49157.8074 | 39664.0599 ± 413.2934 | — | 0.0 |
| transfer-lightgbm | housing | lightgbm.LOO | 3 | 49157.8074 | 49754.5781 ± 985.4220 | — | 0.0 |
| transfer-lightgbm | housing | lightgbm.LossHigh | 3 | 49157.8074 | 40419.6462 ± 729.7573 | — | 0.0 |
| transfer-lightgbm | housing | pytorch.Influence | 3 | 49157.8074 | 47741.3505 ± 1368.8414 | — | 0.0 |
| transfer-lightgbm | housing | pytorch.LOO | 3 | 49157.8074 | 49754.8275 ± 621.3275 | — | 0.0 |
| transfer-lightgbm | housing | pytorch.LissaInfluence | 3 | 49157.8074 | 50363.1396 ± 3613.3507 | — | 0.0 |
| transfer-lightgbm | housing | pytorch.LossHigh | 3 | 49157.8074 | 39746.1093 ± 445.7033 | — | 0.0 |
| transfer-lightgbm | housing | random_forest.LOO | 3 | 49157.8074 | 49997.4191 ± 547.4186 | — | 0.0 |
| transfer-lightgbm | housing | random_forest.LossHigh | 3 | 49157.8074 | 40139.9964 ± 419.9221 | — | 0.0 |
| transfer-lightgbm | housing | xgboost.LOO | 3 | 49157.8074 | 50092.1013 ± 1042.6107 | — | 0.0 |
| transfer-lightgbm | housing | xgboost.LossHigh | 3 | 49157.8074 | 47982.2690 ± 535.2837 | — | 0.0 |
| transfer-lightgbm | housing | random | 3 | 49157.8074 | 50179.8604 ± 614.8884 | — | 0.0 |
| transfer-lightgbm | adult | any.DataOOB | 3 | 0.6367 | 0.6513 ± 0.0107 | — | 0.0 |
| transfer-lightgbm | adult | any.KNNShapley | 3 | 0.6367 | 0.6598 ± 0.0154 | — | 0.0 |
| transfer-lightgbm | adult | catboost.CatBoostLFC | 3 | 0.6367 | 0.6363 ± 0.0173 | — | 0.0 |
| transfer-lightgbm | adult | catboost.LOO | 3 | 0.6367 | 0.6499 ± 0.0137 | — | 0.0 |
| transfer-lightgbm | adult | catboost.LossHigh | 3 | 0.6367 | 0.6581 ± 0.0050 | — | 0.0 |
| transfer-lightgbm | adult | distill-lightgbm.Influence | 3 | 0.6367 | 0.6528 ± 0.0097 | — | 0.0 |
| transfer-lightgbm | adult | distill-lightgbm.LossHigh | 3 | 0.6367 | 0.6559 ± 0.0050 | — | 0.0 |
| transfer-lightgbm | adult | lightgbm.LOO | 3 | 0.6367 | 0.6419 ± 0.0108 | — | 0.0 |
| transfer-lightgbm | adult | lightgbm.LossHigh | 3 | 0.6367 | 0.6610 ± 0.0067 | — | 0.0 |
| transfer-lightgbm | adult | pytorch.Influence | 3 | 0.6367 | 0.6576 ± 0.0181 | — | 0.0 |
| transfer-lightgbm | adult | pytorch.LOO | 3 | 0.6367 | 0.6315 ± 0.0111 | — | 0.0 |
| transfer-lightgbm | adult | pytorch.LissaInfluence | 3 | 0.6367 | 0.6561 ± 0.0109 | — | 0.0 |
| transfer-lightgbm | adult | pytorch.LossHigh | 3 | 0.6367 | 0.6568 ± 0.0081 | — | 0.0 |
| transfer-lightgbm | adult | random_forest.LOO | 3 | 0.6367 | 0.6404 ± 0.0044 | — | 0.0 |
| transfer-lightgbm | adult | random_forest.LossHigh | 3 | 0.6367 | 0.6577 ± 0.0080 | — | 0.0 |
| transfer-lightgbm | adult | xgboost.LOO | 3 | 0.6367 | 0.6328 ± 0.0138 | — | 0.0 |
| transfer-lightgbm | adult | xgboost.LossHigh | 3 | 0.6367 | 0.6509 ± 0.0081 | — | 0.0 |
| transfer-lightgbm | adult | random | 3 | 0.6367 | 0.6408 ± 0.0135 | — | 0.0 |
| transfer-lightgbm | covertype | any.DataOOB | 3 | 0.6955 | 0.6991 ± 0.0128 | — | 0.0 |
| transfer-lightgbm | covertype | any.KNNShapley | 3 | 0.6955 | 0.6973 ± 0.0150 | — | 0.0 |
| transfer-lightgbm | covertype | catboost.LOO | 3 | 0.6955 | 0.6885 ± 0.0068 | — | 0.0 |
| transfer-lightgbm | covertype | catboost.LossHigh | 3 | 0.6955 | 0.6935 ± 0.0139 | — | 0.0 |
| transfer-lightgbm | covertype | distill-lightgbm.Influence | 3 | 0.6955 | 0.6890 ± 0.0139 | — | 0.0 |
| transfer-lightgbm | covertype | distill-lightgbm.LossHigh | 3 | 0.6955 | 0.6997 ± 0.0131 | — | 0.0 |
| transfer-lightgbm | covertype | lightgbm.LOO | 3 | 0.6955 | 0.6901 ± 0.0153 | — | 0.0 |
| transfer-lightgbm | covertype | lightgbm.LossHigh | 3 | 0.6955 | 0.6942 ± 0.0117 | — | 0.0 |
| transfer-lightgbm | covertype | pytorch.Influence | 3 | 0.6955 | 0.6972 ± 0.0125 | — | 0.0 |
| transfer-lightgbm | covertype | pytorch.LOO | 3 | 0.6955 | 0.6856 ± 0.0141 | — | 0.0 |
| transfer-lightgbm | covertype | pytorch.LissaInfluence | 3 | 0.6955 | 0.6941 ± 0.0142 | — | 0.0 |
| transfer-lightgbm | covertype | pytorch.LossHigh | 3 | 0.6955 | 0.7060 ± 0.0238 | — | 0.0 |
| transfer-lightgbm | covertype | random_forest.LOO | 3 | 0.6955 | 0.6868 ± 0.0145 | — | 0.0 |
| transfer-lightgbm | covertype | random_forest.LossHigh | 3 | 0.6955 | 0.6923 ± 0.0188 | — | 0.0 |
| transfer-lightgbm | covertype | xgboost.LOO | 3 | 0.6955 | 0.6906 ± 0.0144 | — | 0.0 |
| transfer-lightgbm | covertype | xgboost.LossHigh | 3 | 0.6955 | 0.6971 ± 0.0137 | — | 0.0 |
| transfer-lightgbm | covertype | random | 3 | 0.6955 | 0.6903 ± 0.0116 | — | 0.0 |
| transfer-pytorch | wine | any.DataOOB | 3 | 0.4833 | 0.4792 ± 0.0258 | — | 0.0 |
| transfer-pytorch | wine | catboost.CatBoostLFC | 3 | 0.4833 | 0.4986 ± 0.0329 | — | 0.0 |
| transfer-pytorch | wine | catboost.LOO | 3 | 0.4833 | 0.4877 ± 0.0267 | — | 0.0 |
| transfer-pytorch | wine | catboost.LossHigh | 3 | 0.4833 | 0.4754 ± 0.0252 | — | 0.0 |
| transfer-pytorch | wine | distill-lightgbm.Influence | 3 | 0.4833 | 0.4823 ± 0.0168 | — | 0.0 |
| transfer-pytorch | wine | distill-lightgbm.LossHigh | 3 | 0.4833 | 0.4794 ± 0.0264 | — | 0.0 |
| transfer-pytorch | wine | lightgbm.LOO | 3 | 0.4833 | 0.4836 ± 0.0233 | — | 0.0 |
| transfer-pytorch | wine | lightgbm.LossHigh | 3 | 0.4833 | 0.4812 ± 0.0366 | — | 0.0 |
| transfer-pytorch | wine | pytorch.Influence | 3 | 0.4833 | 0.4897 ± 0.0279 | — | 0.0 |
| transfer-pytorch | wine | pytorch.LOO | 3 | 0.4833 | 0.4714 ± 0.0263 | — | 0.0 |
| transfer-pytorch | wine | pytorch.LissaInfluence | 3 | 0.4833 | 0.4801 ± 0.0280 | — | 0.0 |
| transfer-pytorch | wine | pytorch.LossHigh | 3 | 0.4833 | 0.4766 ± 0.0369 | — | 0.0 |
| transfer-pytorch | wine | random_forest.LOO | 3 | 0.4833 | 0.4795 ± 0.0267 | — | 0.0 |
| transfer-pytorch | wine | random_forest.LossHigh | 3 | 0.4833 | 0.4834 ± 0.0281 | — | 0.0 |
| transfer-pytorch | wine | xgboost.LOO | 3 | 0.4833 | 0.4747 ± 0.0373 | — | 0.0 |
| transfer-pytorch | wine | xgboost.LossHigh | 3 | 0.4833 | 0.4764 ± 0.0288 | — | 0.0 |
| transfer-pytorch | wine | random | 3 | 0.4833 | 0.4828 ± 0.0254 | — | 0.0 |
| transfer-pytorch | housing | any.DataOOB | 3 | 46691.2572 | 44287.6587 ± 1126.8958 | — | 0.0 |
| transfer-pytorch | housing | catboost.CatBoostLFC | 3 | 46691.2572 | 49284.9705 ± 925.4028 | — | 0.0 |
| transfer-pytorch | housing | catboost.LOO | 3 | 46691.2572 | 47390.8219 ± 1226.1044 | — | 0.0 |
| transfer-pytorch | housing | catboost.LossHigh | 3 | 46691.2572 | 44894.4443 ± 1499.9724 | — | 0.0 |
| transfer-pytorch | housing | distill-lightgbm.Influence | 3 | 46691.2572 | 46607.8187 ± 1517.8588 | — | 0.0 |
| transfer-pytorch | housing | distill-lightgbm.LossHigh | 3 | 46691.2572 | 44733.2299 ± 1099.4473 | — | 0.0 |
| transfer-pytorch | housing | lightgbm.LOO | 3 | 46691.2572 | 46406.5742 ± 797.7943 | — | 0.0 |
| transfer-pytorch | housing | lightgbm.LossHigh | 3 | 46691.2572 | 44733.5082 ± 1106.5793 | — | 0.0 |
| transfer-pytorch | housing | pytorch.Influence | 3 | 46691.2572 | 46493.7737 ± 1597.9133 | — | 0.0 |
| transfer-pytorch | housing | pytorch.LOO | 3 | 46691.2572 | 46819.7445 ± 1047.3674 | — | 0.0 |
| transfer-pytorch | housing | pytorch.LissaInfluence | 3 | 46691.2572 | 48387.0658 ± 2501.0700 | — | 0.0 |
| transfer-pytorch | housing | pytorch.LossHigh | 3 | 46691.2572 | 44544.6783 ± 1213.8324 | — | 0.0 |
| transfer-pytorch | housing | random_forest.LOO | 3 | 46691.2572 | 46969.6220 ± 233.1266 | — | 0.0 |
| transfer-pytorch | housing | random_forest.LossHigh | 3 | 46691.2572 | 44530.1350 ± 971.6263 | — | 0.0 |
| transfer-pytorch | housing | xgboost.LOO | 3 | 46691.2572 | 47861.8925 ± 1344.1208 | — | 0.0 |
| transfer-pytorch | housing | xgboost.LossHigh | 3 | 46691.2572 | 47509.5523 ± 1940.7773 | — | 0.0 |
| transfer-pytorch | housing | random | 3 | 46691.2572 | 47887.7516 ± 923.4232 | — | 0.0 |
| transfer-pytorch | adult | any.DataOOB | 3 | 0.6660 | 0.6603 ± 0.0179 | — | 0.0 |
| transfer-pytorch | adult | any.KNNShapley | 3 | 0.6660 | 0.6532 ± 0.0053 | — | 0.0 |
| transfer-pytorch | adult | catboost.CatBoostLFC | 3 | 0.6660 | 0.6606 ± 0.0099 | — | 0.0 |
| transfer-pytorch | adult | catboost.LOO | 3 | 0.6660 | 0.6551 ± 0.0222 | — | 0.0 |
| transfer-pytorch | adult | catboost.LossHigh | 3 | 0.6660 | 0.6639 ± 0.0113 | — | 0.0 |
| transfer-pytorch | adult | distill-lightgbm.Influence | 3 | 0.6660 | 0.6613 ± 0.0059 | — | 0.0 |
| transfer-pytorch | adult | distill-lightgbm.LossHigh | 3 | 0.6660 | 0.6644 ± 0.0087 | — | 0.0 |
| transfer-pytorch | adult | lightgbm.LOO | 3 | 0.6660 | 0.6596 ± 0.0110 | — | 0.0 |
| transfer-pytorch | adult | lightgbm.LossHigh | 3 | 0.6660 | 0.6622 ± 0.0101 | — | 0.0 |
| transfer-pytorch | adult | pytorch.Influence | 3 | 0.6660 | 0.6667 ± 0.0157 | — | 0.0 |
| transfer-pytorch | adult | pytorch.LOO | 3 | 0.6660 | 0.6504 ± 0.0152 | — | 0.0 |
| transfer-pytorch | adult | pytorch.LissaInfluence | 3 | 0.6660 | 0.6619 ± 0.0062 | — | 0.0 |
| transfer-pytorch | adult | pytorch.LossHigh | 3 | 0.6660 | 0.6565 ± 0.0148 | — | 0.0 |
| transfer-pytorch | adult | random_forest.LOO | 3 | 0.6660 | 0.6674 ± 0.0105 | — | 0.0 |
| transfer-pytorch | adult | random_forest.LossHigh | 3 | 0.6660 | 0.6600 ± 0.0114 | — | 0.0 |
| transfer-pytorch | adult | xgboost.LOO | 3 | 0.6660 | 0.6644 ± 0.0094 | — | 0.0 |
| transfer-pytorch | adult | xgboost.LossHigh | 3 | 0.6660 | 0.6630 ± 0.0139 | — | 0.0 |
| transfer-pytorch | adult | random | 3 | 0.6660 | 0.6610 ± 0.0149 | — | 0.0 |
| transfer-pytorch | covertype | any.DataOOB | 3 | 0.7124 | 0.7060 ± 0.0163 | — | 0.0 |
| transfer-pytorch | covertype | any.KNNShapley | 3 | 0.7124 | 0.7065 ± 0.0025 | — | 0.0 |
| transfer-pytorch | covertype | catboost.LOO | 3 | 0.7124 | 0.7111 ± 0.0033 | — | 0.0 |
| transfer-pytorch | covertype | catboost.LossHigh | 3 | 0.7124 | 0.7100 ± 0.0071 | — | 0.0 |
| transfer-pytorch | covertype | distill-lightgbm.Influence | 3 | 0.7124 | 0.7117 ± 0.0056 | — | 0.0 |
| transfer-pytorch | covertype | distill-lightgbm.LossHigh | 3 | 0.7124 | 0.7110 ± 0.0104 | — | 0.0 |
| transfer-pytorch | covertype | lightgbm.LOO | 3 | 0.7124 | 0.7067 ± 0.0097 | — | 0.0 |
| transfer-pytorch | covertype | lightgbm.LossHigh | 3 | 0.7124 | 0.7145 ± 0.0064 | — | 0.0 |
| transfer-pytorch | covertype | pytorch.Influence | 3 | 0.7124 | 0.6995 ± 0.0108 | — | 0.0 |
| transfer-pytorch | covertype | pytorch.LOO | 3 | 0.7124 | 0.7133 ± 0.0033 | — | 0.0 |
| transfer-pytorch | covertype | pytorch.LissaInfluence | 3 | 0.7124 | 0.6901 ± 0.0045 | — | 0.0 |
| transfer-pytorch | covertype | pytorch.LossHigh | 3 | 0.7124 | 0.7096 ± 0.0064 | — | 0.0 |
| transfer-pytorch | covertype | random_forest.LOO | 3 | 0.7124 | 0.7080 ± 0.0065 | — | 0.0 |
| transfer-pytorch | covertype | random_forest.LossHigh | 3 | 0.7124 | 0.7054 ± 0.0043 | — | 0.0 |
| transfer-pytorch | covertype | xgboost.LOO | 3 | 0.7124 | 0.7061 ± 0.0041 | — | 0.0 |
| transfer-pytorch | covertype | xgboost.LossHigh | 3 | 0.7124 | 0.7103 ± 0.0111 | — | 0.0 |
| transfer-pytorch | covertype | random | 3 | 0.7124 | 0.7091 ± 0.0045 | — | 0.0 |
| transfer-random_forest | wine | any.DataOOB | 3 | 0.4847 | 0.4421 ± 0.0200 | — | 0.0 |
| transfer-random_forest | wine | catboost.CatBoostLFC | 3 | 0.4847 | 0.4974 ± 0.0044 | — | 0.0 |
| transfer-random_forest | wine | catboost.LOO | 3 | 0.4847 | 0.4976 ± 0.0152 | — | 0.0 |
| transfer-random_forest | wine | catboost.LossHigh | 3 | 0.4847 | 0.4474 ± 0.0108 | — | 0.0 |
| transfer-random_forest | wine | distill-lightgbm.Influence | 3 | 0.4847 | 0.4842 ± 0.0157 | — | 0.0 |
| transfer-random_forest | wine | distill-lightgbm.LossHigh | 3 | 0.4847 | 0.4440 ± 0.0174 | — | 0.0 |
| transfer-random_forest | wine | lightgbm.LOO | 3 | 0.4847 | 0.4707 ± 0.0140 | — | 0.0 |
| transfer-random_forest | wine | lightgbm.LossHigh | 3 | 0.4847 | 0.4531 ± 0.0188 | — | 0.0 |
| transfer-random_forest | wine | pytorch.Influence | 3 | 0.4847 | 0.4961 ± 0.0331 | — | 0.0 |
| transfer-random_forest | wine | pytorch.LOO | 3 | 0.4847 | 0.4771 ± 0.0115 | — | 0.0 |
| transfer-random_forest | wine | pytorch.LissaInfluence | 3 | 0.4847 | 0.4770 ± 0.0276 | — | 0.0 |
| transfer-random_forest | wine | pytorch.LossHigh | 3 | 0.4847 | 0.4421 ± 0.0126 | — | 0.0 |
| transfer-random_forest | wine | random_forest.LOO | 3 | 0.4847 | 0.4879 ± 0.0217 | — | 0.0 |
| transfer-random_forest | wine | random_forest.LossHigh | 3 | 0.4847 | 0.4567 ± 0.0107 | — | 0.0 |
| transfer-random_forest | wine | xgboost.LOO | 3 | 0.4847 | 0.4807 ± 0.0083 | — | 0.0 |
| transfer-random_forest | wine | xgboost.LossHigh | 3 | 0.4847 | 0.4740 ± 0.0192 | — | 0.0 |
| transfer-random_forest | wine | random | 3 | 0.4847 | 0.4866 ± 0.0237 | — | 0.0 |
| transfer-random_forest | housing | any.DataOOB | 3 | 48792.6941 | 42947.8972 ± 664.7835 | — | 0.0 |
| transfer-random_forest | housing | catboost.CatBoostLFC | 3 | 48792.6941 | 52485.3366 ± 607.0166 | — | 0.0 |
| transfer-random_forest | housing | catboost.LOO | 3 | 48792.6941 | 48735.0818 ± 1775.2065 | — | 0.0 |
| transfer-random_forest | housing | catboost.LossHigh | 3 | 48792.6941 | 43600.9870 ± 302.7128 | — | 0.0 |
| transfer-random_forest | housing | distill-lightgbm.Influence | 3 | 48792.6941 | 47759.1744 ± 994.3684 | — | 0.0 |
| transfer-random_forest | housing | distill-lightgbm.LossHigh | 3 | 48792.6941 | 43165.3885 ± 665.9927 | — | 0.0 |
| transfer-random_forest | housing | lightgbm.LOO | 3 | 48792.6941 | 48193.5981 ± 375.4268 | — | 0.0 |
| transfer-random_forest | housing | lightgbm.LossHigh | 3 | 48792.6941 | 43360.1967 ± 1014.3350 | — | 0.0 |
| transfer-random_forest | housing | pytorch.Influence | 3 | 48792.6941 | 47191.5355 ± 1142.8705 | — | 0.0 |
| transfer-random_forest | housing | pytorch.LOO | 3 | 48792.6941 | 49432.7988 ± 1179.3945 | — | 0.0 |
| transfer-random_forest | housing | pytorch.LissaInfluence | 3 | 48792.6941 | 50968.3550 ± 1889.9330 | — | 0.0 |
| transfer-random_forest | housing | pytorch.LossHigh | 3 | 48792.6941 | 43352.4301 ± 861.9676 | — | 0.0 |
| transfer-random_forest | housing | random_forest.LOO | 3 | 48792.6941 | 48627.0874 ± 426.0847 | — | 0.0 |
| transfer-random_forest | housing | random_forest.LossHigh | 3 | 48792.6941 | 43493.1624 ± 1411.9654 | — | 0.0 |
| transfer-random_forest | housing | xgboost.LOO | 3 | 48792.6941 | 49365.8163 ± 1029.7146 | — | 0.0 |
| transfer-random_forest | housing | xgboost.LossHigh | 3 | 48792.6941 | 47262.7167 ± 2058.2694 | — | 0.0 |
| transfer-random_forest | housing | random | 3 | 48792.6941 | 49200.6435 ± 900.6435 | — | 0.0 |
| transfer-random_forest | adult | any.DataOOB | 3 | 0.6671 | 0.6617 ± 0.0020 | — | 0.0 |
| transfer-random_forest | adult | any.KNNShapley | 3 | 0.6671 | 0.6655 ± 0.0065 | — | 0.0 |
| transfer-random_forest | adult | catboost.CatBoostLFC | 3 | 0.6671 | 0.6662 ± 0.0085 | — | 0.0 |
| transfer-random_forest | adult | catboost.LOO | 3 | 0.6671 | 0.6657 ± 0.0116 | — | 0.0 |
| transfer-random_forest | adult | catboost.LossHigh | 3 | 0.6671 | 0.6556 ± 0.0085 | — | 0.0 |
| transfer-random_forest | adult | distill-lightgbm.Influence | 3 | 0.6671 | 0.6675 ± 0.0090 | — | 0.0 |
| transfer-random_forest | adult | distill-lightgbm.LossHigh | 3 | 0.6671 | 0.6599 ± 0.0032 | — | 0.0 |
| transfer-random_forest | adult | lightgbm.LOO | 3 | 0.6671 | 0.6657 ± 0.0075 | — | 0.0 |
| transfer-random_forest | adult | lightgbm.LossHigh | 3 | 0.6671 | 0.6607 ± 0.0033 | — | 0.0 |
| transfer-random_forest | adult | pytorch.Influence | 3 | 0.6671 | 0.6683 ± 0.0049 | — | 0.0 |
| transfer-random_forest | adult | pytorch.LOO | 3 | 0.6671 | 0.6672 ± 0.0076 | — | 0.0 |
| transfer-random_forest | adult | pytorch.LissaInfluence | 3 | 0.6671 | 0.6594 ± 0.0106 | — | 0.0 |
| transfer-random_forest | adult | pytorch.LossHigh | 3 | 0.6671 | 0.6596 ± 0.0052 | — | 0.0 |
| transfer-random_forest | adult | random_forest.LOO | 3 | 0.6671 | 0.6632 ± 0.0069 | — | 0.0 |
| transfer-random_forest | adult | random_forest.LossHigh | 3 | 0.6671 | 0.6553 ± 0.0083 | — | 0.0 |
| transfer-random_forest | adult | xgboost.LOO | 3 | 0.6671 | 0.6603 ± 0.0086 | — | 0.0 |
| transfer-random_forest | adult | xgboost.LossHigh | 3 | 0.6671 | 0.6642 ± 0.0072 | — | 0.0 |
| transfer-random_forest | adult | random | 3 | 0.6671 | 0.6668 ± 0.0052 | — | 0.0 |
| transfer-random_forest | covertype | any.DataOOB | 3 | 0.7226 | 0.7208 ± 0.0148 | — | 0.0 |
| transfer-random_forest | covertype | any.KNNShapley | 3 | 0.7226 | 0.7184 ± 0.0104 | — | 0.0 |
| transfer-random_forest | covertype | catboost.LOO | 3 | 0.7226 | 0.7197 ± 0.0118 | — | 0.0 |
| transfer-random_forest | covertype | catboost.LossHigh | 3 | 0.7226 | 0.7209 ± 0.0144 | — | 0.0 |
| transfer-random_forest | covertype | distill-lightgbm.Influence | 3 | 0.7226 | 0.7193 ± 0.0136 | — | 0.0 |
| transfer-random_forest | covertype | distill-lightgbm.LossHigh | 3 | 0.7226 | 0.7205 ± 0.0096 | — | 0.0 |
| transfer-random_forest | covertype | lightgbm.LOO | 3 | 0.7226 | 0.7198 ± 0.0080 | — | 0.0 |
| transfer-random_forest | covertype | lightgbm.LossHigh | 3 | 0.7226 | 0.7223 ± 0.0122 | — | 0.0 |
| transfer-random_forest | covertype | pytorch.Influence | 3 | 0.7226 | 0.7187 ± 0.0099 | — | 0.0 |
| transfer-random_forest | covertype | pytorch.LOO | 3 | 0.7226 | 0.7189 ± 0.0104 | — | 0.0 |
| transfer-random_forest | covertype | pytorch.LissaInfluence | 3 | 0.7226 | 0.7089 ± 0.0108 | — | 0.0 |
| transfer-random_forest | covertype | pytorch.LossHigh | 3 | 0.7226 | 0.7223 ± 0.0090 | — | 0.0 |
| transfer-random_forest | covertype | random_forest.LOO | 3 | 0.7226 | 0.7177 ± 0.0119 | — | 0.0 |
| transfer-random_forest | covertype | random_forest.LossHigh | 3 | 0.7226 | 0.7223 ± 0.0146 | — | 0.0 |
| transfer-random_forest | covertype | xgboost.LOO | 3 | 0.7226 | 0.7175 ± 0.0139 | — | 0.0 |
| transfer-random_forest | covertype | xgboost.LossHigh | 3 | 0.7226 | 0.7199 ± 0.0166 | — | 0.0 |
| transfer-random_forest | covertype | random | 3 | 0.7226 | 0.7149 ± 0.0161 | — | 0.0 |
| transfer-xgboost | wine | any.DataOOB | 3 | 0.5612 | 0.4410 ± 0.0152 | — | 0.0 |
| transfer-xgboost | wine | catboost.CatBoostLFC | 3 | 0.5612 | 0.5659 ± 0.0227 | — | 0.0 |
| transfer-xgboost | wine | catboost.LOO | 3 | 0.5612 | 0.5519 ± 0.0115 | — | 0.0 |
| transfer-xgboost | wine | catboost.LossHigh | 3 | 0.5612 | 0.4130 ± 0.0262 | — | 0.0 |
| transfer-xgboost | wine | distill-lightgbm.Influence | 3 | 0.5612 | 0.5130 ± 0.0277 | — | 0.0 |
| transfer-xgboost | wine | distill-lightgbm.LossHigh | 3 | 0.5612 | 0.4376 ± 0.0301 | — | 0.0 |
| transfer-xgboost | wine | lightgbm.LOO | 3 | 0.5612 | 0.5556 ± 0.0424 | — | 0.0 |
| transfer-xgboost | wine | lightgbm.LossHigh | 3 | 0.5612 | 0.4306 ± 0.0162 | — | 0.0 |
| transfer-xgboost | wine | pytorch.Influence | 3 | 0.5612 | 0.5245 ± 0.0373 | — | 0.0 |
| transfer-xgboost | wine | pytorch.LOO | 3 | 0.5612 | 0.5519 ± 0.0360 | — | 0.0 |
| transfer-xgboost | wine | pytorch.LissaInfluence | 3 | 0.5612 | 0.5118 ± 0.0859 | — | 0.0 |
| transfer-xgboost | wine | pytorch.LossHigh | 3 | 0.5612 | 0.4390 ± 0.0324 | — | 0.0 |
| transfer-xgboost | wine | random_forest.LOO | 3 | 0.5612 | 0.5509 ± 0.0824 | — | 0.0 |
| transfer-xgboost | wine | random_forest.LossHigh | 3 | 0.5612 | 0.4462 ± 0.0251 | — | 0.0 |
| transfer-xgboost | wine | xgboost.LOO | 3 | 0.5612 | 0.5809 ± 0.0305 | — | 0.0 |
| transfer-xgboost | wine | xgboost.LossHigh | 3 | 0.5612 | 0.5336 ± 0.0353 | — | 0.0 |
| transfer-xgboost | wine | random | 3 | 0.5612 | 0.5730 ± 0.0387 | — | 0.0 |
| transfer-xgboost | housing | any.DataOOB | 3 | 66237.2478 | 41842.8434 ± 521.5901 | — | 0.0 |
| transfer-xgboost | housing | catboost.CatBoostLFC | 3 | 66237.2478 | 65377.1801 ± 432.7727 | — | 0.0 |
| transfer-xgboost | housing | catboost.LOO | 3 | 66237.2478 | 66590.8734 ± 1175.6812 | — | 0.0 |
| transfer-xgboost | housing | catboost.LossHigh | 3 | 66237.2478 | 42669.1196 ± 1351.2269 | — | 0.0 |
| transfer-xgboost | housing | distill-lightgbm.Influence | 3 | 66237.2478 | 58955.5833 ± 1573.0171 | — | 0.0 |
| transfer-xgboost | housing | distill-lightgbm.LossHigh | 3 | 66237.2478 | 42080.0597 ± 571.7640 | — | 0.0 |
| transfer-xgboost | housing | lightgbm.LOO | 3 | 66237.2478 | 64717.5858 ± 105.9749 | — | 0.0 |
| transfer-xgboost | housing | lightgbm.LossHigh | 3 | 66237.2478 | 41894.4129 ± 321.1983 | — | 0.0 |
| transfer-xgboost | housing | pytorch.Influence | 3 | 66237.2478 | 57793.1262 ± 364.5780 | — | 0.0 |
| transfer-xgboost | housing | pytorch.LOO | 3 | 66237.2478 | 66874.8017 ± 487.1985 | — | 0.0 |
| transfer-xgboost | housing | pytorch.LissaInfluence | 3 | 66237.2478 | 58288.0274 ± 1576.6344 | — | 0.0 |
| transfer-xgboost | housing | pytorch.LossHigh | 3 | 66237.2478 | 42464.9163 ± 265.5316 | — | 0.0 |
| transfer-xgboost | housing | random_forest.LOO | 3 | 66237.2478 | 66932.3104 ± 895.8011 | — | 0.0 |
| transfer-xgboost | housing | random_forest.LossHigh | 3 | 66237.2478 | 42274.0143 ± 181.1812 | — | 0.0 |
| transfer-xgboost | housing | xgboost.LOO | 3 | 66237.2478 | 66320.7728 ± 775.3525 | — | 0.0 |
| transfer-xgboost | housing | xgboost.LossHigh | 3 | 66237.2478 | 56368.0941 ± 1053.9627 | — | 0.0 |
| transfer-xgboost | housing | random | 3 | 66237.2478 | 66482.2355 ± 1279.2035 | — | 0.0 |
| transfer-xgboost | adult | any.DataOOB | 3 | 0.5817 | 0.6343 ± 0.0065 | — | 0.0 |
| transfer-xgboost | adult | any.KNNShapley | 3 | 0.5817 | 0.6404 ± 0.0061 | — | 0.0 |
| transfer-xgboost | adult | catboost.CatBoostLFC | 3 | 0.5817 | 0.6183 ± 0.0093 | — | 0.0 |
| transfer-xgboost | adult | catboost.LOO | 3 | 0.5817 | 0.5766 ± 0.0182 | — | 0.0 |
| transfer-xgboost | adult | catboost.LossHigh | 3 | 0.5817 | 0.6538 ± 0.0114 | — | 0.0 |
| transfer-xgboost | adult | distill-lightgbm.Influence | 3 | 0.5817 | 0.6126 ± 0.0089 | — | 0.0 |
| transfer-xgboost | adult | distill-lightgbm.LossHigh | 3 | 0.5817 | 0.6381 ± 0.0068 | — | 0.0 |
| transfer-xgboost | adult | lightgbm.LOO | 3 | 0.5817 | 0.5864 ± 0.0087 | — | 0.0 |
| transfer-xgboost | adult | lightgbm.LossHigh | 3 | 0.5817 | 0.6303 ± 0.0175 | — | 0.0 |
| transfer-xgboost | adult | pytorch.Influence | 3 | 0.5817 | 0.6176 ± 0.0191 | — | 0.0 |
| transfer-xgboost | adult | pytorch.LOO | 3 | 0.5817 | 0.5855 ± 0.0119 | — | 0.0 |
| transfer-xgboost | adult | pytorch.LissaInfluence | 3 | 0.5817 | 0.6394 ± 0.0171 | — | 0.0 |
| transfer-xgboost | adult | pytorch.LossHigh | 3 | 0.5817 | 0.6407 ± 0.0061 | — | 0.0 |
| transfer-xgboost | adult | random_forest.LOO | 3 | 0.5817 | 0.5766 ± 0.0104 | — | 0.0 |
| transfer-xgboost | adult | random_forest.LossHigh | 3 | 0.5817 | 0.6493 ± 0.0111 | — | 0.0 |
| transfer-xgboost | adult | xgboost.LOO | 3 | 0.5817 | 0.5927 ± 0.0210 | — | 0.0 |
| transfer-xgboost | adult | xgboost.LossHigh | 3 | 0.5817 | 0.6113 ± 0.0097 | — | 0.0 |
| transfer-xgboost | adult | random | 3 | 0.5817 | 0.5734 ± 0.0064 | — | 0.0 |
| transfer-xgboost | covertype | any.DataOOB | 3 | 0.6728 | 0.6852 ± 0.0214 | — | 0.0 |
| transfer-xgboost | covertype | any.KNNShapley | 3 | 0.6728 | 0.6785 ± 0.0147 | — | 0.0 |
| transfer-xgboost | covertype | catboost.LOO | 3 | 0.6728 | 0.6708 ± 0.0073 | — | 0.0 |
| transfer-xgboost | covertype | catboost.LossHigh | 3 | 0.6728 | 0.6822 ± 0.0154 | — | 0.0 |
| transfer-xgboost | covertype | distill-lightgbm.Influence | 3 | 0.6728 | 0.6713 ± 0.0165 | — | 0.0 |
| transfer-xgboost | covertype | distill-lightgbm.LossHigh | 3 | 0.6728 | 0.6858 ± 0.0145 | — | 0.0 |
| transfer-xgboost | covertype | lightgbm.LOO | 3 | 0.6728 | 0.6670 ± 0.0135 | — | 0.0 |
| transfer-xgboost | covertype | lightgbm.LossHigh | 3 | 0.6728 | 0.6754 ± 0.0144 | — | 0.0 |
| transfer-xgboost | covertype | pytorch.Influence | 3 | 0.6728 | 0.6780 ± 0.0120 | — | 0.0 |
| transfer-xgboost | covertype | pytorch.LOO | 3 | 0.6728 | 0.6693 ± 0.0127 | — | 0.0 |
| transfer-xgboost | covertype | pytorch.LissaInfluence | 3 | 0.6728 | 0.6775 ± 0.0161 | — | 0.0 |
| transfer-xgboost | covertype | pytorch.LossHigh | 3 | 0.6728 | 0.6897 ± 0.0162 | — | 0.0 |
| transfer-xgboost | covertype | random_forest.LOO | 3 | 0.6728 | 0.6680 ± 0.0152 | — | 0.0 |
| transfer-xgboost | covertype | random_forest.LossHigh | 3 | 0.6728 | 0.6767 ± 0.0113 | — | 0.0 |
| transfer-xgboost | covertype | xgboost.LOO | 3 | 0.6728 | 0.6659 ± 0.0087 | — | 0.0 |
| transfer-xgboost | covertype | xgboost.LossHigh | 3 | 0.6728 | 0.6765 ± 0.0105 | — | 0.0 |
| transfer-xgboost | covertype | random | 3 | 0.6728 | 0.6694 ± 0.0092 | — | 0.0 |

Paired vs random removal at 10 % (lowest first; > 0 = better than random):

| data | dataset | method | n | Δ mean | 95 % bootstrap CI | p (t-test) | seeds better |
|---|---|---|---|---|---|---|---|
| clean data | wine | LOO | 5 | +0.0061 | [-0.0016, +0.0167] | 0.326 | 3/5 |
| clean data | wine | TMC-Shapley | 5 | -0.0037 | [-0.0114, +0.0038] | 0.433 | 1/5 |
| clean data | wine | Data-OOB | 5 | -0.0112 | [-0.0161, -0.0063] | 0.019 | 0/5 |
| clean data | wine | Influence | 5 | -0.0057 | [-0.0106, -0.0007] | 0.115 | 1/5 |
| clean data | wine | LiSSA | 5 | -0.0005 | [-0.0106, +0.0095] | 0.931 | 2/5 |
| clean data | wine | high loss | 5 | -0.0101 | [-0.0158, -0.0052] | 0.033 | 0/5 |
| clean data | housing | LOO | 5 | +85.3570 | [-263.4151, +445.9425] | 0.678 | 4/5 |
| clean data | housing | Data-OOB | 5 | -86.7043 | [-750.2040, +576.7955] | 0.832 | 2/5 |
| clean data | housing | Influence | 5 | +8.6481 | [-1060.8838, +1064.5115] | 0.989 | 2/5 |
| clean data | housing | LiSSA | 5 | +220.4069 | [-460.1687, +1075.7626] | 0.648 | 2/5 |
| clean data | housing | high loss | 5 | +345.6100 | [-391.8732, +1033.2760] | 0.450 | 3/5 |
| clean data | adult | LOO | 5 | +0.0035 | [-0.0007, +0.0070] | 0.191 | 4/5 |
| clean data | adult | KNN-Shapley | 5 | +0.0020 | [-0.0051, +0.0116] | 0.705 | 2/5 |
| clean data | adult | Data-OOB | 5 | -0.0014 | [-0.0047, +0.0022] | 0.513 | 2/5 |
| clean data | adult | Influence | 5 | +0.0004 | [-0.0028, +0.0036] | 0.827 | 3/5 |
| clean data | adult | LiSSA | 5 | -0.0140 | [-0.0294, -0.0007] | 0.159 | 1/5 |
| clean data | adult | high loss | 5 | +0.0075 | [+0.0032, +0.0120] | 0.041 | 5/5 |
| clean data | covertype | LOO | 5 | +0.0017 | [-0.0020, +0.0066] | 0.516 | 2/5 |
| clean data | covertype | KNN-Shapley | 5 | -0.0040 | [-0.0090, +0.0001] | 0.184 | 1/5 |
| clean data | covertype | Data-OOB | 5 | +0.0024 | [-0.0037, +0.0082] | 0.535 | 3/5 |
| clean data | covertype | Influence | 5 | -0.0013 | [-0.0037, +0.0016] | 0.434 | 1/5 |
| clean data | covertype | LiSSA | 5 | -0.0096 | [-0.0148, -0.0046] | 0.036 | 0/5 |
| clean data | covertype | high loss | 5 | -0.0003 | [-0.0049, +0.0043] | 0.923 | 2/5 |
| corrupted labels | wine | LOO | 5 | +0.0139 | [+0.0078, +0.0199] | 0.016 | 5/5 |
| corrupted labels | wine | TMC-Shapley | 5 | +0.0143 | [+0.0067, +0.0218] | 0.032 | 5/5 |
| corrupted labels | wine | Data-OOB | 5 | +0.0014 | [-0.0020, +0.0040] | 0.474 | 4/5 |
| corrupted labels | wine | Influence | 5 | -0.0022 | [-0.0224, +0.0152] | 0.851 | 3/5 |
| corrupted labels | wine | LiSSA | 5 | -0.0078 | [-0.0224, +0.0099] | 0.438 | 2/5 |
| corrupted labels | wine | high loss | 5 | +0.0038 | [-0.0038, +0.0115] | 0.440 | 3/5 |
| corrupted labels | housing | LOO | 5 | +1307.4687 | [+678.4053, +1804.0815] | 0.014 | 5/5 |
| corrupted labels | housing | Data-OOB | 5 | +2808.6122 | [+1800.4945, +3769.9845] | 0.009 | 5/5 |
| corrupted labels | housing | Influence | 5 | +1102.7100 | [+557.9677, +1780.9219] | 0.035 | 5/5 |
| corrupted labels | housing | LiSSA | 5 | -142.6407 | [-2246.1782, +2035.6313] | 0.914 | 2/5 |
| corrupted labels | housing | high loss | 5 | +2650.3623 | [+1650.8477, +3697.2012] | 0.011 | 5/5 |
| corrupted labels | adult | LOO | 5 | -0.0075 | [-0.0251, +0.0052] | 0.445 | 2/5 |
| corrupted labels | adult | KNN-Shapley | 5 | -0.0044 | [-0.0137, +0.0022] | 0.406 | 2/5 |
| corrupted labels | adult | Data-OOB | 5 | -0.0009 | [-0.0047, +0.0029] | 0.702 | 2/5 |
| corrupted labels | adult | Influence | 5 | -0.0016 | [-0.0099, +0.0058] | 0.744 | 3/5 |
| corrupted labels | adult | LiSSA | 5 | -0.0026 | [-0.0087, +0.0044] | 0.525 | 2/5 |
| corrupted labels | adult | high loss | 5 | -0.0031 | [-0.0059, -0.0004] | 0.131 | 1/5 |
| corrupted labels | covertype | LOO | 5 | +0.0005 | [-0.0046, +0.0048] | 0.872 | 3/5 |
| corrupted labels | covertype | KNN-Shapley | 5 | -0.0044 | [-0.0068, -0.0010] | 0.065 | 1/5 |
| corrupted labels | covertype | Data-OOB | 5 | -0.0009 | [-0.0128, +0.0077] | 0.884 | 4/5 |
| corrupted labels | covertype | Influence | 5 | -0.0084 | [-0.0178, -0.0006] | 0.161 | 1/5 |
| corrupted labels | covertype | LiSSA | 5 | -0.0166 | [-0.0213, -0.0120] | 0.004 | 0/5 |
| corrupted labels | covertype | high loss | 5 | +0.0006 | [-0.0038, +0.0049] | 0.840 | 3/5 |
