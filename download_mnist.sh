#! /bin/bash

function download() {
  local url="$1"
  local filename="$(basename $url)"

  echo Downloading "$filename"
  curl "${url}" -o "data/${filename}"
}

download http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
download http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
download http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
download http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
