# import numpy as np
import torchvision.transforms as transforms
import torchvision.datasets as dset
# from PIL import Image
import os.path as osp
from .dataset_const import Dataset2Class, imagenet_pca


# class Lighting(object):
#     def __init__(self, alphastd,
#                  eigval=dc.imagenet_pca['eigval'],
#                  eigvec=dc.imagenet_pca['eigvec']):
#         self.alphastd = alphastd
#         assert eigval.shape == (3,)
#         assert eigvec.shape == (3, 3)
#         self.eigval = eigval
#         self.eigvec = eigvec
#
#     def __call__(self, img):
#         if self.alphastd == 0.:
#             return img
#         rnd = np.random.randn(3) * self.alphastd
#         rnd = rnd.astype('float32')
#         v = rnd
#         old_dtype = np.asarray(img).dtype
#         v = v * self.eigval
#         v = v.reshape((3, 1))
#         inc = np.dot(self.eigvec, v).reshape((3,))
#         img = np.add(img, inc)
#         if old_dtype == np.uint8:
#             img = np.clip(img, 0, 255)
#         img = Image.fromarray(img.astype(old_dtype), 'RGB')
#         return img
#
#     def __repr__(self):
#         return self.__class__.__name__ + '()'


def get_datasets(name, root, cutout):
    if name == 'cifar10':
        mean = [x / 255 for x in [125.3, 123.0, 113.9]]
        std = [x / 255 for x in [63.0, 62.1, 66.7]]
    elif name == 'cifar100':
        mean = [x / 255 for x in [129.3, 124.1, 112.4]]
        std = [x / 255 for x in [68.2, 65.4, 70.4]]
    elif name == 'fake':
        mean = [x / 255 for x in [129.3, 124.1, 112.4]]
        std = [x / 255 for x in [68.2, 65.4, 70.4]]
    elif name.startswith('imagenet-1k'):
        mean, std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
    elif name.startswith('imagenette'):
        mean, std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
    elif name.startswith('ImageNet16'):
        mean = [x / 255 for x in [122.68, 116.66, 104.01]]
        std = [x / 255 for x in [63.22, 61.26, 65.09]]
    else:
        raise TypeError("Unknow dataset : {:}".format(name))

    # Data Argumentation
    if name == 'cifar10' or name == 'cifar100':
        lists = [transforms.RandomHorizontalFlip(), transforms.RandomCrop(32, padding=4), transforms.ToTensor(),
                 transforms.Normalize(mean, std)]
        # if cutout > 0: lists += [CUTOUT(cutout)]
        train_transform = transforms.Compose(lists)
        test_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean, std)])
        xshape = (1, 3, 32, 32)
    elif name == 'fake':
        lists = [transforms.RandomHorizontalFlip(), transforms.RandomCrop(32, padding=4), transforms.ToTensor(),
                 transforms.Normalize(mean, std)]
        # if cutout > 0: lists += [CUTOUT(cutout)]
        train_transform = transforms.Compose(lists)
        test_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean, std)])
        xshape = (1, 3, 32, 32)
    # elif name.startswith('ImageNet16'):
    #     lists = [transforms.RandomHorizontalFlip(), transforms.RandomCrop(16, padding=2), transforms.ToTensor(),
    #              transforms.Normalize(mean, std)]
    #     # if cutout > 0: lists += [CUTOUT(cutout)]
    #     train_transform = transforms.Compose(lists)
    #     test_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean, std)])
    #     xshape = (1, 3, 16, 16)
    # elif name == 'tiered':
    #     lists = [transforms.RandomHorizontalFlip(), transforms.RandomCrop(80, padding=4), transforms.ToTensor(),
    #              transforms.Normalize(mean, std)]
    #     # if cutout > 0: lists += [CUTOUT(cutout)]
    #     train_transform = transforms.Compose(lists)
    #     test_transform = transforms.Compose(
    #         [transforms.CenterCrop(80), transforms.ToTensor(), transforms.Normalize(mean, std)])
    #     xshape = (1, 3, 32, 32)
    # elif name.startswith('imagenette'):
    #     normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    #     xlists = []
    #     xlists.append(transforms.ToTensor())
    #     xlists.append(normalize)
    #     # train_transform = transforms.Compose(xlists)
    #     train_transform = transforms.Compose(
    #         [normalize, normalize, transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(),
    #          normalize])
    #     test_transform = transforms.Compose(
    #         [normalize, normalize, transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(),
    #          normalize])
    #     xshape = (1, 3, 224, 224)
    # elif name.startswith('imagenet-1k'):
    #     normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    #     if name == 'imagenet-1k':
    #         xlists = [transforms.RandomResizedCrop(224), transforms.ColorJitter(
    #             brightness=0.4,
    #             contrast=0.4,
    #             saturation=0.4,
    #             hue=0.2), Lighting(0.1)]
    #     elif name == 'imagenet-1k-s':
    #         xlists = [transforms.RandomResizedCrop(224, scale=(0.2, 1.0))]
    #     else:
    #         raise ValueError('invalid name : {:}'.format(name))
    #     xlists.append(transforms.RandomHorizontalFlip(p=0.5))
    #     xlists.append(transforms.ToTensor())
    #     xlists.append(normalize)
    #     train_transform = transforms.Compose(xlists)
    #     test_transform = transforms.Compose(
    #         [transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), normalize])
    #     xshape = (1, 3, 224, 224)
    else:
        raise TypeError("Unknow dataset : {:}".format(name))

    if name == 'cifar10':
        train_data = dset.CIFAR10(root, train=True, transform=train_transform, download=False)
        test_data = dset.CIFAR10(root, train=False, transform=test_transform, download=True)
        assert len(train_data) == 50000 and len(test_data) == 10000
    elif name == 'cifar100':
        train_data = dset.CIFAR100(root, train=True, transform=train_transform, download=True)
        test_data = dset.CIFAR100(root, train=False, transform=test_transform, download=True)
        assert len(train_data) == 50000 and len(test_data) == 10000
    elif name == 'fake':
        train_data = dset.FakeData(size=50000, image_size=(3, 32, 32), transform=train_transform)
        test_data = dset.FakeData(size=10000, image_size=(3, 32, 32), transform=test_transform)
    elif name.startswith('imagenette2'):
        train_data = dset.ImageFolder(osp.join(root, 'train'), train_transform)
        test_data = dset.ImageFolder(osp.join(root, 'val'), test_transform)
    elif name.startswith('imagenet-1k'):
        train_data = dset.ImageFolder(osp.join(root, 'train'), train_transform)
        test_data = dset.ImageFolder(osp.join(root, 'val'), test_transform)
        assert len(train_data) == 1281167 and len(
            test_data) == 50000, 'invalid number of images : {:} & {:} vs {:} & {:}'.format(len(train_data),
                                                                                            len(test_data), 1281167,
                                                                                            50000)
    # elif name == 'ImageNet16':
    #     train_data = ImageNet16(root, True, train_transform)
    #     test_data = ImageNet16(root, False, test_transform)
    #     assert len(train_data) == 1281167 and len(test_data) == 50000
    # elif name == 'ImageNet16-120':
    #     train_data = ImageNet16(root, True, train_transform, 120)
    #     test_data = ImageNet16(root, False, test_transform, 120)
    #     assert len(train_data) == 151700 and len(test_data) == 6000
    # elif name == 'ImageNet16-150':
    #     train_data = ImageNet16(root, True, train_transform, 150)
    #     test_data = ImageNet16(root, False, test_transform, 150)
    #     assert len(train_data) == 190272 and len(test_data) == 7500
    # elif name == 'ImageNet16-200':
    #     train_data = ImageNet16(root, True, train_transform, 200)
    #     test_data = ImageNet16(root, False, test_transform, 200)
    #     assert len(train_data) == 254775 and len(test_data) == 10000
    else:
        raise TypeError("Unknow dataset : {:}".format(name))

    class_num = Dataset2Class[name]
    return train_data, test_data, xshape, class_num
