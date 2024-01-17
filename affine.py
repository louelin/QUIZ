import torch 
import torch.nn.functional as F
import numpy as np 
import math 

def get_affine(rotate_params,translate_params,scale_params):
    '''
    @ params :
    rotate_params : list -> (0,0,0) 
                    this version can`t support the rotate augment
    translate_params : list[float] -> (0.1,0.2,0.3)
                    the params in translate_params must be normalized by the Image shape 
    scale_params : list[float] -> (0.9,1.1,0.5)
                    the params in the scale_params must be centered by 1
    
    @ return :
        final_matrix : which has 4*4 shape 
    '''
    
    tx ,ty ,tz = translate_params
    tx ,ty ,tz = torch.Tensor([tx]), torch.Tensor([ty]),torch.Tensor([tz])

    # 输入旋转角度（弧度制）和旋转轴
    theta_x ,theta_y ,theta_z  =rotate_params
    theta_x ,theta_y ,theta_z = torch.Tensor([theta_x]), torch.Tensor([theta_y]),torch.Tensor([theta_z])

    # 构建旋转矩阵
    rot_x = torch.tensor([[1, 0, 0, 0],
                        [0, torch.cos(theta_x), -torch.sin(theta_x), 0],
                        [0, torch.sin(theta_x), torch.cos(theta_x), 0],
                        [0, 0, 0, 1]])
    rot_y = torch.tensor([[torch.cos(theta_y), 0, torch.sin(theta_y), 0],
                        [0, 1, 0, 0],
                        [-torch.sin(theta_y), 0, torch.cos(theta_y), 0],
                        [0, 0, 0, 1]])
    rot_z = torch.tensor([[torch.cos(theta_z), -torch.sin(theta_z), 0, 0],
                        [torch.sin(theta_z), torch.cos(theta_z), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

    # 构建伸缩因子
    sx ,sy ,sz = scale_params
    sx ,sy ,sz = torch.Tensor([sx]), torch.Tensor([sy]),torch.Tensor([sz])
    # 构建仿射矩阵
    affine_matrix = torch.tensor([[sx, 0, 0, tx],
                                [0, sy, 0, ty],
                                [0, 0, sz, tz],
                                [0, 0, 0, 1]])

    # 组合旋转矩阵和仿射矩阵
    final_matrix = torch.matmul(rot_z, torch.matmul(rot_y, torch.matmul(rot_x, affine_matrix)))

    return final_matrix

def random_affine(img,points):
    '''
    @ params 

    img -> torch.FloteTensor : which shape is (1,H,W,D),
    points -> list[float] | np.array : which shape is (N,3) and has been normalized into [0,1]
    '''

    rotate_params = [0,0,0]
    translate_params = np.random.uniform(low=-0.2,high =0.2 , size=(3)).tolist()
    scale_params = np.random.uniform(low=0.5,high = 1.5 , size=(3)).tolist()
    # translate_params = [0.1,0.1,0.1]
    # scale_params = [0.9,0.9,0.9]
    affine_matrix = get_affine(rotate_params,translate_params,scale_params)
    
    affine_matrix.unsqueeze(0)[:,:3]
    grid = F.affine_grid(affine_matrix.unsqueeze(0)[:,:3],size = img.unsqueeze(0).shape, align_corners=False)
    trans_image = F.grid_sample(img.unsqueeze(0), grid, padding_mode="zeros",align_corners=False)[0]

    # the center of pytorch affine grid is the image center ,which is not like to CV2 
    point1_center = np.zeros_like(points)
    for i in range(points.shape[0]):
        x , y ,z = points[i]
        point1_center[i] = z-0.5,y-0.5,x-0.5
    

    point1_center_new = ((torch.inverse(affine_matrix[:3,:3])@torch.Tensor(point1_center).T).T - affine_matrix[:3,-1]/2 ) +0.5

    # exchange x and z
    point1_center_new_change = np.zeros_like(point1_center_new)
    for i in range(point1_center_new.shape[0]):
        x , y ,z = point1_center_new[i]
        point1_center_new_change[i] = z,y,x
    
    return trans_image , point1_center_new_change

def random_permute(img,points,index):
    if index == 1 :
        img = img.clone().permute(0,1,3,2)
        new_point1 = np.copy(np.array(points))
        new_point1[:,[1,2]] = new_point1[:,[2,1]]
    elif index == 2:
        img = img.clone().permute(0,2,1,3)
        new_point1 = np.copy(np.array(points))
        new_point1[:,[0,1]] = new_point1[:,[1,0]]
    elif index == 3:
        img = img.clone().permute(0,3,2,1)
        new_point1 = np.copy(np.array(points))
        new_point1[:,[0,2]] = new_point1[:,[2,0]]
    else :
        return img , points

    return img , new_point1

def random_flip(img,points, index):
    flip_img = torch.flip(img.clone(),dims=[index])
    new_point1 = np.copy(np.array(points))
    new_point1[:,index-1] = 1 - new_point1[:,index-1]

    return flip_img , new_point1