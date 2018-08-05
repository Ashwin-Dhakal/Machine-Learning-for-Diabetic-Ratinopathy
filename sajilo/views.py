from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

def index(request):
    return render(request,'sajilo/index.html')

def searchlist(request):
    image= request.GET.get('img')

    img_name= image.split('-')[0]

    import glob
    import shutil
    import os
    import cv2  # working with, mainly resizing, images
    import numpy as np  # dealing with arrays
    from random import shuffle  # mixing up or currently ordered data that might lead our network astray in training.
    from tqdm import tqdm  # a nice pretty percentage bar for tasks. Thanks to viewer Daniel BA1/4hler for this suggestion
    if img_name == 'd':
        verify_dir = 'testpicture/0'
    elif img_name == 'm':
        verify_dir = 'testpicture/1'
    elif img_name == 'a':
        verify_dir = 'testpicture/2'
    else:
        verify_dir = 'testpicture/4'
    IMG_SIZE = 50
    LR = 1e-3
    MODEL_NAME = 'diabetic-{}-{}.model'.format(LR, '2conv-basic')

    def process_verify_data():
        verifying_data = []
        for img in tqdm(os.listdir(verify_dir)):
            path = os.path.join(verify_dir, img)
            img_num = img.split('.')[0]
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            verifying_data.append([np.array(img), img_num])
        np.save('verify_data.npy', verifying_data)
        return verifying_data

    verify_data = process_verify_data()
    # verify_data = np.load('verify_data.npy')

    import tflearn
    from tflearn.layers.conv import conv_2d, max_pool_2d
    from tflearn.layers.core import input_data, dropout, fully_connected
    from tflearn.layers.estimator import regression
    import tensorflow as tf

    tf.reset_default_graph()

    convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 128, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)

    convnet = fully_connected(convnet, 4, activation='softmax')
    convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(convnet, tensorboard_dir='log')

    if os.path.exists('{}.meta'.format(MODEL_NAME)):
        model.load(MODEL_NAME)
        print('model loaded!')

    import matplotlib.pyplot as plt

    fig = plt.figure()
    for num, data in enumerate(verify_data):

        img_num = data[1]
        img_data = data[0]

        y = fig.add_subplot(3, 4, num + 1)
        orig = img_data
        data = img_data.reshape(IMG_SIZE, IMG_SIZE, 3)
        # model_out = model.predict([data])[0]
        model_out = model.predict([data])[0]

        if np.argmax(model_out) == 0:
            str_label = 'No Diabetic Retinopathy !'
            rating= '0'
        elif np.argmax(model_out) == 1:
            str_label = 'Mild Diabetic Retinopathy !'
            rating = '1'
        elif np.argmax(model_out) == 2:
            str_label = 'Moderate Diabetic Retinopathy!'
            rating = '2'

        elif np.argmax(model_out) == 3:
            str_label = 'Proliferative Diabetic Retinopathy !'
            rating = '3'


        image_url = '/images/' + image
        context = {
            "image" : image,
            "url": image_url,
            "str_label" : str_label,
            "rating" : rating,
        }



        return render(request, 'sajilo/searchlist.html', context)





