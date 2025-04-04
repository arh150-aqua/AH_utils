import pandas as pd
import multiprocessing as mp
import boto3
import cv2
import numpy as np


def get_img_from_s3(image_url, bucket = "aquabyte-datasets-images"):
    s3_resource = boto3.resource('s3')
    bucket_crops = s3_resource.Bucket(bucket)
    key=image_url.split("s3://aquabyte-datasets-images/")[1]
    try:
        img = bucket_crops.Object(key).get().get('Body').read()
    except:
        print("failed to get;", key)
        return
    ima = cv2.imdecode(np.asarray(bytearray(img)), cv2.IMREAD_COLOR)
    
    return ima


# df = pd.read_csv('data/annotations.csv')
# unique_image_urls = df['image_url'].unique()
# img = get_img_from_s3(unique_image_urls[0])
# cv2.imshow('first image', img)
# cv2.waitKey(20000)
