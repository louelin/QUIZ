import os 
from glob import glob
import torch, sys
from torch.utils.data import Dataset
import random
import nibabel as nib
import numpy as np
from scipy.io import loadmat
from monai.transforms import Resize
from tqdm import tqdm
import json
import SimpleITK as sitk
from .affine import random_affine , random_flip ,random_permute 




class Plevic_Dataset(Dataset):
    def __init__(self,Json_path = "./train_pairs.json", transforms=None):
        with open(Json_path,'r') as f :
            self.data = json.load(f)

        self.transforms = transforms
        self.R = Resize(spatial_size=(128,128,128))

    def load_nii(self, path):
        image = nib.load(path).get_fdata()
        return image
    def load_query(self,path,index):
        single_query_path = path[index]
        matrix = loadmat(single_query_path)
        queries = (matrix['queries'] / 128).astype(np.float32)
        # print("queries:", queries.type)
        # queries = queries[None, ...]
        return queries


    
    def Normal(self,x):
        x = (x-x.min())/(x.max() - x.min())
        return x

    def two_images_side_by_side(self,img_a, img_b):
        assert img_a.shape == img_b.shape, f'{img_a.shape} vs {img_b.shape}'
        assert img_a.dtype == img_b.dtype
        n, h, w, d = img_a.shape
        canvas = np.zeros((n, h, w, 2*d), dtype=np.float64)
        canvas[:, :, :, 0:1 * d] = img_a
        canvas[:, :, :, 1 * d:2 * d] = img_b
        return canvas
    

    def __getitem__(self, index):
        data = self.data[index]
        
        ct_path , cbct_path , ref_data = data['ct'] , data['cbct'] , data['ref']

        ct = sitk.GetArrayFromImage(sitk.ReadImage(ct_path))
        cbct = sitk.GetArrayFromImage(sitk.ReadImage(cbct_path))
        ref = np.load(ref_data,allow_pickle=True)
        random_index = np.random.randint(0,ref.shape[0],size=(40))
        if self.transforms:
            ref = ref[random_index]
        targets = ref[:,:3]
        queries = ref[:,3:]

        queries = (queries / cbct.shape).astype(np.float32)
        targets = (targets / ct.shape).astype(np.float32)



        fix_img, mov_img = self.R(torch.from_numpy(ct[None, ...])), self.R(torch.from_numpy(cbct[None, ...]))
        
        fix_img,mov_img = self.Normal(fix_img), self.Normal(mov_img)

        if self.transforms:
            affine_prob = random.random()
            if affine_prob > 0.8:
                fix_img , targets = random_affine(fix_img , targets)
            affine_prob = random.random()
            if affine_prob > 0.8:
                mov_img , queries = random_affine(mov_img , queries)
            
            permute_prob = random.randint(0,3)
            fix_img , targets = random_permute(fix_img , targets , permute_prob)
            mov_img , queries = random_permute(mov_img , queries , permute_prob)
            
            flip_prob = random.random()
            if flip_prob > 0.8 :
                flip_prob = random.randint(1,3)
                fix_img , targets = random_flip(fix_img , targets , flip_prob)
                mov_img , queries = random_flip(mov_img , queries , flip_prob)
            
            fix_img , mov_img = self.transforms(fix_img) , self.transforms(mov_img)


        cat_img = torch.FloatTensor(self.two_images_side_by_side(fix_img, mov_img))

        out = {
            'image': cat_img,
            'queries': queries,
            'targets': targets,
            'fixed_path' : ct_path  ,
            'mov_path' : cbct_path,
        }

        return out
   
    def __len__(self):
        return len(self.data)



if __name__ == "__main__":
    test_set =Plevic_Dataset(Json_path = "./val_pairs.json")
    

    for i in range(4):
        item = test_set.__getitem__(i)
        
