import shutil
import os 
from glob import glob

# /home/liulin/Pelvic_nii/Pelvic-Ref-002

strings = []
for i in range(2,59):
    string = "0" + str(i) if len(str(i)) == 2 else "00" + str(i)
    strings.append(string)

Data_path = "/home/liulin/Pelvic_nii/Pelvic-Ref-"
Save_path = "/media/liulin/Elements SE/liulin_Ubuntu_temp/Quiz/github_Quiz/keypoints/"
for i in range(len(strings)):
    path = Data_path + strings[i]
    keypoint_path = os.path.join(path , "keypoints.npy")
    if os.path.exists(keypoint_path):

        save_path = os.path.join(Save_path , "Pelvic-Ref-" + strings[i] + "_keypoints.npy")
        shutil.copy(keypoint_path , save_path)
print("Finish")