# #   这部分主要写从UV位置图获得3D人脸，并不包括如何产生UV位置图。 2020-03-23

### 1.  裁剪后人脸图像 以及 对应的 UV位置图
![人脸图片](https://github.com/DongPoLI/Face-3D-Study/blob/master/generate_position_map/datas/image00050.jpg?raw=true)
![UV Position map](https://github.com/DongPoLI/Face-3D-Study/blob/master/generate_position_map/datas/image00050_posmap.jpg?raw=true)
![UV texture map](https://github.com/DongPoLI/Face-3D-Study/blob/master/generate_position_map/datas/image00050_tex.jpg)

### 2.  从UV位置图 产生的 3D人脸模型效果
1. ply 文件效果 （不带纹理，形状）
![ply](https://github.com/DongPoLI/Face-3D-Study/blob/master/generate_position_map/results/image00050.png)
2. obj 文件效果（带纹理）
![obj](https://github.com/DongPoLI/Face-3D-Study/blob/master/generate_position_map/results/image0050_with_colors.png)

代码在 generate_position_map文件夹中
链接： https://blog.csdn.net/qq_23944915/article/details/105046742
