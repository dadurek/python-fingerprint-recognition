import os
import uuid
from os import listdir
from os.path import isfile, join
from pathlib import Path
from typing import Optional

import aiofiles
import cv2
import numpy as np
from fastapi import UploadFile

DATABASE_DIRECTORY = "../database"
DATABASE_USERS_SUBDIRECTORY = "users"


def calculate_descriptions(image_path: str):
    img2 = cv2.imread(image_path)
    sift = cv2.SIFT_create()
    key_points, desc = sift.detectAndCompute(img2, None)
    return key_points, desc


def compare_fingerprints(image1_path: str, image2_path: str) -> float:
    key_points1, des1 = calculate_descriptions(image1_path)
    key_points2, des2 = calculate_descriptions(image2_path)

    return compare_fingerprints_pre_counted(key_points1, des1, key_points2, des2)


def compare_fingerprints_pre_counted(key_points1, des1, key_points2, des2) -> float:
    matches = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(np.float32(des1), np.float32(des2), k=2)
    match_points = []

    for p, q in matches:
        if p.distance < 0.7 * q.distance:
            match_points.append(p)

    key_points = min([len(key_points1), len(key_points2)])
    return (len(match_points) / key_points) * 100


def check_if_fingerprint_match(key_points1, des1, key_points2, des2) -> bool:
    score = compare_fingerprints_pre_counted(key_points1, des1, key_points2, des2)
    score_threshold = 25
    if score > score_threshold:
        return True
    else:
        return False


def compare_with_user(username: str, uploaded_filepath: str) -> bool:
    # TODO handle if username exist
    base_dir = f"{DATABASE_DIRECTORY}/{DATABASE_USERS_SUBDIRECTORY}/{username}"
    users_file = [f"{base_dir}/{file}" for file in listdir(base_dir) if isfile(join(base_dir, file))]
    key_points1, des1 = calculate_descriptions(uploaded_filepath)
    for user_file in users_file:
        key_points2, des2 = calculate_descriptions(user_file)
        if check_if_fingerprint_match(key_points1, des1, key_points2, des2):
            return True
    return False


async def save_file(upload_file: UploadFile, username: Optional[str]) -> str:
    file_extension = upload_file.filename.split('.')[-1]
    if not username:
        base_dir = f"{DATABASE_DIRECTORY}/temp"
    else:
        base_dir = f"{DATABASE_DIRECTORY}/{DATABASE_USERS_SUBDIRECTORY}/{username}"
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    out_file_path = f"{base_dir}/{uuid.uuid4()}.{file_extension}"

    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await upload_file.read(1024):
            await out_file.write(content)

    return out_file_path


async def remove_file(file_path: str):
    os.remove(file_path)
