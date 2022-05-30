import aiofiles
import cv2
import numpy
import uuid
import os
from os import listdir
from os.path import isfile, join

from typing import Optional
from fastapi import UploadFile
from services import image_enhance


def remove_dot(invertThin):
    temp0 = numpy.array(invertThin[:])
    temp0 = numpy.array(temp0)
    temp1 = temp0 / 255
    temp2 = numpy.array(temp1)

    W, H = temp0.shape[:2]
    filtersize = 6

    for i in range(W - filtersize):
        for j in range(H - filtersize):
            filter0 = temp1[i:i + filtersize, j:j + filtersize]

            flag = 0
            if sum(filter0[:, 0]) == 0:
                flag += 1
            if sum(filter0[:, filtersize - 1]) == 0:
                flag += 1
            if sum(filter0[0, :]) == 0:
                flag += 1
            if sum(filter0[filtersize - 1, :]) == 0:
                flag += 1
            if flag > 3:
                temp2[i:i + filtersize, j:j + filtersize] = numpy.zeros((filtersize, filtersize))

    return temp2


def get_descriptors(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img = clahe.apply(img)
    img = image_enhance.image_enhance(img)
    img = numpy.array(img, dtype=numpy.uint8)
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    img[img == 255] = 1

    harris_corners = cv2.cornerHarris(img, 3, 3, 0.04)
    harris_normalized = cv2.normalize(harris_corners, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
    threshold_harris = 125
    keypoints = []
    for x in range(0, harris_normalized.shape[0]):
        for y in range(0, harris_normalized.shape[1]):
            if harris_normalized[x][y] > threshold_harris:
                keypoints.append(cv2.KeyPoint(y, x, 1))
    orb = cv2.ORB_create()
    _, des = orb.compute(img, keypoints)
    return (keypoints, des)


def calculate_descriptions(image_path: str):
    img2 = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return get_descriptors(img2)[1]


def compare_fingerprints(image1_path: str, image2_path: str) -> float:
    des1 = calculate_descriptions(image1_path)

    des2 = calculate_descriptions(image2_path)

    return compare_fingerprints_pre_counted(des1, des2)


def compare_fingerprints_pre_counted(des1, des2) -> float:
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = sorted(bf.match(des1, des2), key=lambda match: match.distance)

    score = 0
    for match in matches:
        score += match.distance

    return score / float(len(matches))


def check_if_fingerprint_match(des1, des2) -> bool:
    score = compare_fingerprints_pre_counted(des1, des2)
    # score_threshold = 33
    score_threshold = 22.5
    if score < score_threshold:
        return True
    else:
        return False


def compare_with_user(username: str, uploaded_filepath: str) -> bool:
    # TODO handle if username exist
    base_dir = f"/database/{username}"
    users_file = [f"{base_dir}/{file}" for file in listdir(base_dir) if isfile(join(base_dir, file))]
    des_uploaded_file = calculate_descriptions(uploaded_filepath)
    for user_file in users_file:
        des_user_file = calculate_descriptions(user_file)
        if check_if_fingerprint_match(des_user_file, des_uploaded_file):
            return True
    return False


async def save_file(upload_file: UploadFile, base_directory: Optional[str] = "temp") -> str:
    file_extension = upload_file.filename.split('.')[-1]
    out_file_path = f"/database/{base_directory}/{uuid.uuid4()}.{file_extension}"

    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await upload_file.read(1024):
            await out_file.write(content)

    return out_file_path


async def remove_file(file_path: str):
    os.remove(file_path)

