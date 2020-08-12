## 可视化部分的代码运行

### 介绍

**使用的工具是Open3D**

pip install open3d==0.10.0

**此外还需要安装的包**

- 1.scikit-learn==0.19.2 2. filterpy==1.4.5 3. numba==0.43.1 4. matplotlib==2.2.3 5. pillow==6.2.2 6. opencv-python==3.4.3.18 7. glob2==0.6 8. llvmlite==0.32.1 (for python 3.6) or llvmlite==0.31.0 (for python 2.7)
- 运行$ pip install -r requirements.txt即可

**此外还需要作者自己编写的工具包**

- 在'utils.py'中，放入可视化文件的同级目录即可，或者export到PYTHONPATH中

**文件结构**

我使用的结果文件结构，可视化过程中需要用到的有 x yz w h l thata，根据自己的文件结构进行调整即可

| fid  | tid  | tid_gt | timestamp          | d_type | lo la                | speed | thata    | cred | h w l                      | x y z                         |
| ---- | ---- | ------ | ------------------ | ------ | -------------------- | ----- | -------- | ---- | -------------------------- | ----------------------------- |
| 0    | 1    | 1      | 20200728160000.062 | 2      | 1202527315 302370121 | 0     | 0.542797 | 100  | 1.857000 1.582000 4.259000 | -2.718000 -3.318000 24.092000 |

部分代码借鉴：https://blog.csdn.net/Oreooooo/article/details/107281003?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~first_rank_v2~rank_v25-1-107281003.nonecase



### 可视化文件

可视化文件**visualize.py**，可以实现输出某一帧的识别结果、输出若干辆车辆的完整追踪轨迹、输出前n帧所有车辆的追踪轨迹三个功能

**usage**

**python visualize.py filename type fids/trkids/fnum**

- filename是文件名，文件目录需要在源码中手动给出
- type取值范围是0,1,2
  - 0：输出某一帧的识别结果，其后面的参数可以有多个，表示不同的帧序号fids，输出结果中相同车辆用相同的颜色表示
  - 1：输出指定轨迹编号的追踪结果，其后面可以有多个参数，表示不同轨迹ID trkids，输出指定车辆的完整追踪轨迹
  - 2：输出前fnum帧所有车辆的追踪结果，其后面有一个参数，用于限定帧序号，输出在该帧之前的所有帧的所有车辆的追踪结果

**输出某些帧的追踪结果**

- 输出filename中第1帧的追踪结果

  python visualize.py filename 0 1

- 输出filename中第1帧、第5帧、第10帧的追踪结果

  python visualize.py filename 0 1 5 10

**输出某些车辆的追踪结果**

- 输出filename中tracking ID为1的轨迹的追踪结果

  python visualize.py filename 1 1

- 输出filename中tracking ID为1、81、126的轨迹的追踪结果

  python visualize.py filename 1 1 81 126

**输出前fnum帧所有车辆的追踪结果**

- 输出filename中帧序号<=30的轨迹追踪结果
- python visualize.py filename 2 30 
