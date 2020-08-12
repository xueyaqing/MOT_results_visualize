from __future__ import print_function
import matplotlib; matplotlib.use('Agg')
import os.path, copy, numpy as np, time, sys
from numba import jit
from scipy.optimize import linear_sum_assignment
from filterpy.kalman import KalmanFilter
from utils_vis import load_list_from_folder, fileparts, mkdir_if_missing
# from scipy.spatial import ConvexHull
import open3d as o3d
import numpy as np
import time
import os
from alfred.fusion.common import draw_3d_box, compute_3d_box_lidar_coords
from alfred.fusion.kitti_fusion import load_pc_from_file
import random

# generate random color to seperate diff cars
def random_colors(max_num):
    res = []
    for index in range(0,max_num):
        color = []
        for i in range(3):
            color.append(random.random())
        res.append(color)
    return res

# open3d generate tool
def visual_option():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    opt.point_size = 1
    opt.line_width = 100
    opt.show_coordinate_frame = False
    return vis

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python main.py result_sha(e.g., 20200728_inno_01000008_device3_Car.txt) type fids/trkids/fnum')
        sys.exit(1)

    # filename
    result_sha = sys.argv[1]
    # visualize type, look up README.md for more details
    type = sys.argv[2]
    if(type == '0'):
        fids = []
        fid_num_statistic = {}
        for i in range(3,len(sys.argv)):
            fids.append(int(sys.argv[i]))
    elif (type == '1'):
        trkids = []
        trkid_num_statistic = {}
        for i in range(3,len(sys.argv)):
            trkids.append(int(sys.argv[i]))
    elif (type == '2'):
        if(len(sys.argv) > 4):
            print("too many argv")
            sys.exit(1)
        fnum = int(sys.argv[3])
        tkid_num_statistic = {}
    else:
        print('Wrong type')
        sys.exit(1)

    # ====================================Visual Preparation======================================
    vis = visual_option()
    line_set = [o3d.geometry.LineSet() for _ in range(1000)]
    # pcobj = o3d.geometry.PointCloud()
    
    # generate 300 colors
    max_color = 300
    colors = random_colors(max_color)

    trackers = []
    # filedir change to your data dir
    root_path = 'your filedir'
    filename = os.path.join(root_path, result_sha)
    with open(filename , 'r') as f:
        trackers_all = np.loadtxt(filename, delimiter=' ')
        for tracker in trackers_all:
            # load tracking results from file
            if(type == '0'):
                if(int(tracker[0]) in fids):
                    trackers.append(tracker)
            elif (type == '1'):
                if(int(tracker[1]) in trkids):
                    trackers.append(tracker)
            elif (type == '2'):
                if(int(tracker[0]) <= fnum):
                    trackers.append(tracker)

    f.close()

    for index, d in enumerate(trackers):
    	# get x y z w h l thata to draw lines,change the index by your file
        xyz = np.array([d[13: 16]])
        h = np.array([d[11]])
        w = np.array([d[10]])
        l = np.array([d[12]])
        hwl_tmp = np.concatenate((h,w,l),axis=0)
        hwl = np.array([hwl_tmp])
        r_y = [d[6]]
        pts3d = compute_3d_box_lidar_coords(xyz, hwl, angles=r_y, origin=(0.5, 0.5, 0.5), axis=2)
        lines = [[0, 1], [1, 2], [2, 3], [3, 0],
                [4, 5], [5, 6], [6, 7], [7, 4],
                [0, 4], [1, 5], [2, 6], [3, 7]]

        
        tkid = int(d[1])

        # one color for one car
        color = colors[tkid % max_color]
        
        line_colors = [color for i in range(len(lines))]

        line_set_tmp = o3d.geometry.LineSet()
        line_set_tmp.points = o3d.utility.Vector3dVector(pts3d[0])
        line_set_tmp.lines = o3d.utility.Vector2iVector(lines)
        line_set_tmp.colors = o3d.utility.Vector3dVector(line_colors)
        vis.add_geometry(line_set_tmp)

        # information statistic
        if(type == '2'):
            if tkid not in tkid_num_statistic:
                tkid_num_statistic[tkid] = 1
            else:
                tkid_num_statistic[tkid] +=1
        elif (type == '1'):
            if tkid not in trkid_num_statistic:
                trkid_num_statistic[tkid] = 1
            else:
                trkid_num_statistic[tkid] +=1
        elif (type == '0'):
            if int(d[0]) not in fid_num_statistic:
                fid_num_statistic[int(d[0])] = 1
            else:
                fid_num_statistic[int(d[0])] +=1

    if(type == '0'):
        print("The detections numbers of frame(s) is" ,fid_num_statistic)
    elif (type == '1'):
        print("The tracklet length statistic is", trkid_num_statistic)
    elif (type == '2'):
        print("The statistic information is",tkid_num_statistic)
    
    # draw
    vis.poll_events()
    vis.update_renderer()
    vis.run()