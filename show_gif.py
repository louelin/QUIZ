import nibabel as nib 
import numpy as np 
import os 
import torch 
import matplotlib.pyplot as plt 
import SimpleITK as sitk

from tqdm import tqdm
from PIL import Image
import glob

def show_keypoints(cbct,ct,cbct_key,ct_keypoints):
    x ,y ,z = map(int , cbct_key)
    ct_x,ct_y,ct_z = map(int, ct_keypoints)

    
    ct = (ct - ct.min())/(ct.max() - ct.min()) * 255
    cbct = (cbct - cbct.min())/(cbct.max() - cbct.min()) * 255

    
    cbct[0,x-5:x+5 , y-5:y+5,z-5:z+5] = 255
    ct[:,ct_x-5:ct_x+5 , ct_y-5:ct_y+5,ct_z-5:ct_z+5] = 255
    fig = plt.figure()
    plt.subplot(231)
    plt.imshow(cbct[0,x,:,:],"gray")
    plt.subplot(232)
    plt.imshow(cbct[0,:,y,:],"gray")
    plt.subplot(233)
    plt.imshow(cbct[0,:,:,z],"gray")

    plt.subplot(234)
    plt.imshow(ct[0,ct_x,:,:],"gray")
    plt.subplot(235)
    plt.imshow(ct[0,:,ct_y,:],"gray")
    plt.subplot(236)
    plt.imshow(ct[0,:,:,ct_z],"gray")

    # plt.show()
    # plt.close()
    return fig

keypoints_files = glob.glob("/media/liulin/Elements SE/liulin_Ubuntu_temp/Quiz/github_Quiz/keypoints/*.npy")
nii_path = "/home/liulin/Pelvic_nii/"
png_save_path = "/media/liulin/Elements SE/liulin_Ubuntu_temp/Quiz/github_Quiz/landmark_gif/"
gif_save_path = "/media/liulin/Elements SE/liulin_Ubuntu_temp/Quiz/github_Quiz/gif_dir"
# with open(Json_path,'r') as f :
#     self.data = json.load(f)

for j in tqdm(range(len(keypoints_files))):

    subject_name = keypoints_files[j].split("/")[-1][:14]

    if os.path.exists(gif_save_path + "/" + subject_name+ ".gif"):
        continue
    
    try :
        print(subject_name)
        cbct_path = glob.glob(os.path.join(nii_path,subject_name) + "/*newcbct.nii.gz")[0]
        ct_path = glob.glob(os.path.join(nii_path,subject_name) + "/*simct.nii.gz")[0]


        cbct = nib.load(cbct_path)
        ct = nib.load(ct_path)
        affine = cbct.affine 
        cbct = cbct.get_fdata()
        ct = ct.get_fdata()
        keypoints = np.load( keypoints_files[j],allow_pickle=True)
        keypoints ,ct_keypoints= keypoints[:,3:] ,keypoints[:,:3]


        for i in range(keypoints.shape[0]):
            # try : 
            fig = show_keypoints(cbct.copy()[None,...],ct.copy()[None,...],keypoints[i][::-1],ct_keypoints[i][::-1])
            if not os.path.exists(png_save_path + subject_name):
                os.makedirs(png_save_path + subject_name)
            fig.savefig(png_save_path + subject_name + f"/keypoints_{i}.png")
            plt.close(fig)
            # except :
                # Sometimes integer conversions go beyond array boundaries
                # continue

        png_files = sorted(glob.glob(png_save_path + subject_name+"/*.png"))

        images = []
        for png_file in png_files :
            img = Image.open(png_file)
            images.append(img)

        
        # if not os.path.exists(save_path + "/" + subject_name):
        #     os.makedirs(save_path + "/" + subject_name)

        images[0].save(gif_save_path + "/" + subject_name+ ".gif" , save_all =True ,append_images = images[1:] , duration=500 , loop = 0)
    except :
        print(f"{subject_name} have Error!!!")
        