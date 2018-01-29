# Online Contactless Palmprint Identification using Deep Learning (Matching Part)

This is a Pytorch implementation for matching part of Online Contactless Palmprint Identification using Deep Learning.

## Setup

* [Pytorch](http://pytorch.org/)
* [Numpy](www.numpy.org/)
* [Pillow](https://pypi.python.org/pypi/Pillow/)
* [Scipy](https://www.scipy.org/)

***It is recommended to use [Anaconda Python2.7](https://www.continuum.io/anaconda-overview), since you only need to install Pytorch manually.***

## Usage

You need to specify the path of training dataset path, shifting size (***default is 5***) and triplet alpha (***default is 10***) and then run the command for easy training.

```
python main.py --dp_prefix IITD --train_path ./path-to-iitd-folder/ --model RFN-128 --batch_size 10
```

### Other Options

`--checkpoint_dir` allows you to specifically set the saving directory of your model, which by default is './checkpoint/'
`--start_ckpt` allows you to train on dataset based on the chosen the checkpoint model
`--epoch` specifies the maximum epoch number during training.
`--log_interval` specifies the **frequency** to logging the training loss

***please see more by running python main.py -h to see a list of all options***

## Protocols

There are four pretty designed protocols for the testing dataset under protocol folder. It is worth to mentioned that `polyu_roc.py` is specially designed for PolyU 2D/3D Contactless dataset due to its special data formating. You can also use `twos_roc.py` if you have formatted the dataset correctly (first 5 in session1, second 5 in session2).

For all the protocol files, **you need to specify the path to thetesting dataset**, please use `python ./protocols/XXX.py -h` for more details.

**`twos_roc.py`**: two-session work (**300 Subject, 35 Subject**)
**`iitdlike_roc.py`**: IITD-like protocol (**600 Subject, IITD Right**)
**`nfolds_roc.py`**: All-to-All protocol (**CASIA**)

*Example:*

```
python protocols/XXX.py --test_path ./path-to-testset/ --model_path ./path-to-model/ --out_path ./dest-to-store-npy
```

## Plot

For each of the targeting dataset, we prepare a plot function for each of the test dataset(*specifies the x,y coordinates*).

*Example Usage:*

```
python plot/roc_iitd.py --src_npy ./path-to-your-stored-npy/ --dest ./path-to-target-pdf --label RFN-128
```

## Put It Together

It would be nice if we put all the procedure together. So let's take training with **IITD Left** and testing on **IITD Right** as an example.

* Change directory to code folder

```
cd /palmprint-recog/code/
```

* Training with prepared dataset

Please make sure there are `IITD5` under `/palmprint-recog/dataset/` folder

```
python main.py --db_prefix IITD-Left --train_path ../dataset/IITD5/IITD\ Left --epochs 500 --alpha 10 --model RFN-128 --shifted_size 5
```

There will be a folder name `IITD-Left_a10s5mRFN-128_XXX` in the `./checkpoint/` folder, which `XXX` is the datetime.

* Use training checkpoint to test on IITD Right with IITD-like protocol

Let's take epoch 300 as an example, `--save_mmat` is used when plotting CMC

```
python protocols/iitdlike_roc.py --test_path ../dataset/IITD5/IITD\ Right --model_path ./checkpoint/IITD-Left_a10s5mRFN-128_XXX/ckpt_epoch_300.pth --out_path ./output/IITD-Right-test.npy --shift_size 5 --save_mmat True
```

* Using the generated .npy file to plot ROC and CMC

*ROC:*

```
python plot/roc_iitd.py --src_npy ./output/IITD-Right-test.npy --dest ./output/IITD-Right-test.pdf --label RFN-128
```

*CMC:*

```
python plot/cmc_iitd.py --src_npy ./output/IITD-Right-test.npy --dest ./output/IITD-Right-test_cmc.pdf --label RFN-128
```

## Best Trained Model

We have provided the best trained model for each dataset, please check the files under `./checkpoint/selected-best-ckpt/` for details.