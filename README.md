# acc_ass
## Accuracy assessment tools
A number of tools to help with accuracy assessment of classification of remote sensing imagery.

<b>[strat_rnd_sampling.py](https://github.com/timwh/acc_ass/blob/main/strat_rnd_sampling.py)</b>  - Stratified random point sampling for creating a reference data set. Number of points is per class area. <br>
  | | Class_name | Area_Pxl	| samples |
  |:-:|:---------|:--------:|:-------:|
  | 0 |	emergent |	440505.0	| 109 |
  | 1	| floating	| 109400.0	| 27 |
  | 2	| submerged	| 167093.0	| 41 |
  | 3	| water	| 314130.0 |	78 |

<img src="https://github.com/timwh/acc_ass/blob/main/images/Screenshot%202025-03-31093809.png" width="350" height="350" />

<b>[add_class2ref.py](https://github.com/timwh/acc_ass/blob/main/add_class2ref.py)</b> - Add the class name from the classified shapefile to the reference point set. <br>
<b>[conf_matrix.py](https://github.com/timwh/acc_ass/blob/main/conf_matrix.py)</b> - Create confusion matrix with overall, user's and producer's accuracies, and Kappa statistic

<img src="https://github.com/timwh/acc_ass/blob/main/images/Screenshot2025-03-28160534.png" width="400" height="400" /><br>
<b>[mcnemar_test.py](https://github.com/timwh/acc_ass/blob/main/mcnemar_test.py)</b> - Conduct a McNemar test to describe difference between two classifications using same reference

|||Classification|1|
|:-:|:-:|:------:|:-------:|
|||Correct|Wrong|
|<b>Classification</b>|Correct|168|10|
|2|Wrong|3|24|

statistic: 3.0000, p-value: 0.0923
