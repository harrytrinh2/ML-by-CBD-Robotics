#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, request, redirect, url_for, render_template
import os
import json
import glob
import numpy as np
import pandas as pd
from uuid import uuid4
import SimpleITK as sitk
import pdb
import sys
import argparse
import  cv2
from  collections  import Counter
from scipy.misc import imsave
import matplotlib.pyplot as plt
import keras
from keras.models import load_model
import tensorflow as tf
import tensorflow as tf
global graph,model
graph = tf.get_default_graph()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())
    upload_key = str(upload_key).replace("-","_")
    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = "D:\\npy\\uploads\\{}".format(upload_key)
    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False, "Couldn't create upload directory: {}".format(target))
        else:
            return "Couldn't create upload directory: {}".format(target)
    print("=== Form Data ===")
    for key, value in list(form.items()):
        print(key, "=>", value)

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return redirect(url_for("generate_imgs", uuid=upload_key))

def load_itk_image(filename):
    itkimage = sitk.ReadImage(filename)
    numpyImage = sitk.GetArrayFromImage(itkimage)
    numpyOrigin = np.array(list(reversed(itkimage.GetOrigin())))
    numpySpacing = np.array(list(reversed(itkimage.GetSpacing())))
    return numpyImage, numpyOrigin, numpySpacing

def getdata(nodule_info):
    mhd_file = nodule_info[5]
    itk_img = sitk.ReadImage(mhd_file)
    img_array = sitk.GetArrayFromImage(itk_img)  # z,y,x ordering
    origin_xyz = np.array(itk_img.GetOrigin())   # x,y,z  Origin in world coordinates (mm)
    spacing_xyz = np.array(itk_img.GetSpacing()) # spacing of voxels in world coor. (mm)
    center_xyz = (nodule_info[1], nodule_info[2], nodule_info[3])
    nodule_xyz = ((center_xyz - origin_xyz) // spacing_xyz).astype(np.int16)
    nodule = img_array[nodule_xyz[2], nodule_xyz[1] - 16:nodule_xyz[1]+16, nodule_xyz[0] - 16:nodule_xyz[0]+16]
    nodule = np.array(nodule)
    return nodule

@app.route("/files/<uuid>")
def upload_complete(uuid):
    """The location we send them to at the end of the upload."""

    #get the files
    root = "D:\\npy\\uploads\\{}".format(uuid)
    if not os.path.isdir(root):
        return "Error: UUID not found :("
    for file in glob.glob("{}\\*.*".format(root)):
        _link = (file)
        #"C:/Users/PhucCoi/PycharmProjects/flask-multi-upload-master/"+str(file).split("\\")[0]+"/"+str(file).split("\\")[1]
        #_link = (_link.replace("-","_")).replace(".","_")
        print("link = ",_link)
        saving_npy("D:\\subset6\\1.3.6.1.4.1.14519.5.2.1.6279.6001.106630482085576298661469304872.mhd")
        #numpyImage, numpyOrigin, numpySpacing = load_itk_image("D:\\subset6\\1.3.6.1.4.1.14519.5.2.1.6279.6001.106630482085576298661469304872.mhd")
def getsuid(filename):
    file = filename.split('\\')[-1]
    file = file.split('.mhd')[0]
    return file
def saving_npy(direction):
    filename = getsuid(direction)
    datasub = candidates[0:0]
    for j in range(candidates.shape[0]):
        if (candidates.seriesuid[j] == filename):
            datasub = datasub.append(candidates.loc[j])
    print(datasub)
    datasub['file'] = "D:\\subset6\\" + datasub.seriesuid + ".mhd"
    datapos = datasub[datasub['class']==1]
    dataneg = datasub[datasub['class']==0]
    dataneg = dataneg.sample(n = datapos.shape[0], random_state = 42)
    for j in range(datapos.shape[0]):
        ineed = getdata(datapos.iloc[j])
        path = "D:\\npy\\uploads\\save_npy\\1" + "\\" + "\\" +datapos.iloc[j][0]+str(datapos.iloc[j][1])+str(datapos.iloc[j][1])+str(datapos.iloc[j][2])+str(datapos.iloc[j][3])+".npy"
        np.save(path,ineed)
    for j in range(datapos.shape[0]):
        ineed = getdata(dataneg.iloc[j])
        path = "D:\\npy\\uploads\\save_npy\\0" + "\\" + "\\" +dataneg.iloc[j][0]+str(dataneg.iloc[j][1])+str(dataneg.iloc[j][1])+str(dataneg.iloc[j][2])+str(dataneg.iloc[j][3])+".npy"
        np.save(path,ineed)
    return render_template("print.html",calculate_diameter=calculate_diameter(path),prediction=prediction(path))
def calculate_diameter(filename):
    a = np.load(filename)
    plt.imshow(a, cmap=plt.cm.gray)
    imsave(filename.replace(".npy",".png"), a)
    img = cv2.imread(filename.replace(".npy",".png"))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=1)
    plt.imshow(sure_bg)
    sum=0
    for i in range(32):
        if Counter( sure_bg[i])[0] !=0:
            sum+=Counter( sure_bg[i])[0]
    _diameter_mm = sum *0.264583 * 0.65
    return _diameter_mm

# @app.route("/npy/<uuid>", methods = ['POST'])
# def generate_imgs(uuid):
#     #get the files
#     root = "uploadr/static/uploads/{}".format(uuid)
#     if not os.path.isdir(root):
#         return "Error: UUID not found :("
#     for file in glob.glob("{}/*.*".format(root)):
#         numpyImage, numpyOrigin, numpySpacing = load_itk_image(file)
#         numpy_image = numpyImage.shape
#         print(numpy_image)
#     return render_template("print.html")

def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))

parser = argparse.ArgumentParser(description="Uploadr")
parser.add_argument(
    "--port", "-p",
    type=int,
    help="Port to listen on",
    default=1996,
)
args = parser.parse_args()
def prediction(file):
    _img=[]
    _img.append(np.load(file))
    img = np.array(_img)
    img = img.astype('float32')
    print(img.shape)
    img = img.reshape(img.shape[0], 32, 32, 1)
    print(img.shape)
    with graph.as_default():
        y = model.predict_classes(img)
    return y
if __name__ == '__main__':
    flask_options = dict(
        debug=True,
        port=args.port,
        threaded=True,
    )
    candidates = pd.read_csv('F:\data\Luna Analysis\CSVFILES\candidates_V2.csv')
    model = load_model("C:\\Users\\PhucCoi\\Documents\\ML-by-CBD-Robotics\\Deep Learning\\Week5 Lung cancer part 2\\CNN_model.h5")
    app.run(**flask_options)

