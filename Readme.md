# QUIZ: An Arbitrary Volumetric Point Matching Method for Medical Image Registration

This repo open-sources the [TCIA Pelvic data](https://wiki.cancerimagingarchive.net/display/Public/Pelvic-Reference-Data) we have calibrated and provides programmable code. You can find the raw data (with image data) at this https://wiki.cancerimagingarchive.net/display/Public/Pelvic-Reference-Data link. This repo only provides the corrected landmark file.

## Publication
You can find out how we used the altered dataset in our article. [QUIZ: An Arbitrary Volumetric Point Matching Method for Medical Image Registration](https://www.sciencedirect.com/science/article/abs/pii/S0895611124000132)

##  How to use this Dataset
All landmarks are stored in the keypoints folder with patient names and in .npy format

You can visualize all point pairs by executing the show_gif.py file or in gif_dir
```cmd
python show_gif.py
```
It is worth noting that we discarded point pair information for several samples, among them 'Pelvic-Ref-001' and 'Pelvic-Ref-016' and 'Pelvic-Ref-051'

If you want to apply this dataset to your own dataset, you can refer to dataset.py

## Citation
If you use the data we provide, please cite our articles and follow TCIA's licenses!

```
@article{LIU2024102336,
title = {QUIZ: An arbitrary volumetric point matching method for medical image registration},
journal = {Computerized Medical Imaging and Graphics},
pages = {102336},
year = {2024},
issn = {0895-6111},
doi = {https://doi.org/10.1016/j.compmedimag.2024.102336},
url = {https://www.sciencedirect.com/science/article/pii/S0895611124000132},
author = {Lin Liu and Xinxin Fan and Haoyang Liu and Chulong Zhang and Weibin Kong and Jingjing Dai and Yuming Jiang and Yaoqin Xie and Xiaokun Liang},
}
```


## Acknowledgements
Yorke, A. A., McDonald, G. C., Solis, D., & Guerrero, T. (2019). Pelvic Reference Data (Version 1) [Data set]. The Cancer Imaging Archive. https://doi.org/10.7937/TCIA.2019.WOSKQ5OO

A. Yorke, A., McDonald, G. C., Solis, D., & Guerrero, T.  (2021) Quality Assurance of Image Registration Using Combinatorial Rigid Registration Optimization (CORRO). J. Cancer Research and Cellular Therapeutics. 5(2). DOI: https://doi.org/10.31579/2640-1053/076

Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., Moore, S., Phillips, S., Maffitt, D., Pringle, M., Tarbox, L., & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository. In Journal of Digital Imaging (Vol. 26, Issue 6, pp. 1045–1057). Springer Science and Business Media LLC. https://doi.org/10.1007/s10278-013-9622-7

orke, A, Solis, D., Jr. and Guerrero, T. (2020), A feasibility study to estimate optimal rigid‐body registration using combinatorial rigid registration optimization (CORRO). J. Appl. Clin. Med. Phys., 21: 14-22. https://doi.org/10.1002/acm2.12965