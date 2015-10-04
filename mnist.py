import array
import gzip
import os
import struct
import numpy as np

images_file_magic = 2051
labels_file_magic = 2049

train_images_filename = 'data/train-images-idx3-ubyte.gz'
train_labels_filename = 'data/train-labels-idx1-ubyte.gz'
test_images_filename  = 'data/t10k-images-idx3-ubyte.gz'
test_labels_filename  = 'data/t10k-labels-idx1-ubyte.gz'

def read_uint32(io):
    return struct.unpack('!I', io.read(4))[0]

def read_count(io):
    return read_uint32(io)

def read_image_size(io):
    nrows = read_uint32(io)
    ncols = read_uint32(io)
    return nrows, ncols

def read_magic(io):
    return read_uint32(io)

def check_magic(io, magic):
    file_magic = read_magic(io)
    if magic != file_magic:
        print magic
        print file_magic
        raise RuntimeError("Error: invalid magic")

def load_mnist(images_path, labels_path):
    with gzip.open(images_path, 'rb') as io_images:
        check_magic(io_images, images_file_magic)
        images_count = read_count(io_images)
        nrows, ncols = read_image_size(io_images)

        with gzip.open(labels_path, 'rb') as io_labels:
            check_magic(io_labels, labels_file_magic)
            labels_count = read_count(io_labels)

            if images_count != labels_count:
                raise RuntimeError("Error: images_count != labels_count")

            count = images_count
            dimension = nrows * ncols
            images = np.zeros(count * dimension, dtype=np.uint8).reshape((count, dimension))
            labels = np.zeros(count, dtype=np.uint8).reshape((count, ))

            for i in range(count):
                labels[i] = ord(io_labels.read(1))
                images[i, :] = array.array('B', io_images.read(dimension))

            return images, labels, count

def load_data():
    train_images, train_labels, train_count = load_mnist(train_images_filename, train_labels_filename)
    test_images, test_labels, test_count   = load_mnist(test_images_filename, test_labels_filename)

    mnist = {}
    mnist['images'] = np.append(train_images, test_images, axis=0)
    mnist['labels'] = np.append(train_labels, test_labels, axis=0)
    mnist['train_count'] = train_count
    mnist['test_count'] = test_count

    return mnist
