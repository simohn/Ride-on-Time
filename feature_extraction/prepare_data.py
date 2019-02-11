import os
import re
import shutil
from glob import glob
import ntpath


def split_data_into_train_test_set():
    base_path = "data/rider_images/"
    data_folder = "all_v2/"

    version = int(re.search(r'\d+', data_folder).group())

    if os.path.exists(base_path + "train_v" + str(version)):
        shutil.rmtree(base_path + "train_v" + str(version), ignore_errors=True)

    shutil.copytree(base_path+data_folder, base_path + "train_v" + str(version))

    if os.path.exists(base_path + "test_v" + str(version)):
        shutil.rmtree(base_path + "test_v" + str(version), ignore_errors=True)

    os.makedirs(base_path + "test_v" + str(version))

    img_name_list = glob(base_path + "train_v" + str(version) + "/*.jpg")
    img_name_list.sort()

    eval_done = False
    test_done = False

    code_old = "-1"

    for index, path_and_name in enumerate(img_name_list):
        img_name_only = ntpath.basename(path_and_name)
        code = img_name_only.split('_')

        if code[0] != code_old:
            eval_done = False
            test_done = False

        if not eval_done:
            shutil.copy(base_path + "train_v" + str(version) + "/" + img_name_only, base_path + "test_v" +
                        str(version) + "/" + code[0] + "_0.jpg")
            eval_done = True
        elif not test_done:
            shutil.move(base_path + "train_v" + str(version) + "/" + img_name_only, base_path + "test_v" +
                        str(version) + "/" + code[0] + "_1.jpg")
            test_done = True

        code_old = code[0]


if __name__ == "__main__":
    split_data_into_train_test_set()