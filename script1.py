import math
from typing import Tuple
from krita import *
from PyQt5.QtCore import QByteArray
import random

Pixel = Tuple[float, float, float, float]

def blending(a: Pixel, b: Pixel, blending_mode: str) -> Pixel:
    """
    a: 底图层像素
    b: 顶图层像素
    blending_mode: 混合模式
    return: 结果像素
    """
    doc = Krita.instance().activeDocument()
    group = doc.createGroupLayer('')
    a_layer = doc.createNode('', 'paintlayer')
    a_layer.setPixelData(QByteArray.fromRawData(bytes(map(lambda x: round(x * 255), a))), 0, 0, 1, 1)

    b_layer = doc.createNode('', 'paintlayer')
    b_layer.setBlendingMode(blending_mode)
    b_layer.setPixelData(QByteArray.fromRawData(bytes(map(lambda x: round(x * 255), b))), 0, 0, 1, 1)

    group.setChildNodes([a_layer, b_layer])
    b_layer.mergeDown()
    target = group.childNodes()[0]
    pixel = target.pixelData(0, 0, 1, 1)
    r = ord(pixel[0])
    g = ord(pixel[1])
    b = ord(pixel[2])
    a = ord(pixel[3])
    return tuple(map(lambda x: x / 255, [r, g, b, a]))

RGB = Tuple[float, float, float]

def pixelEqual(name: str, a: RGB, b: RGB):
    def equal(a: float, b: float):
        return abs(a - b) <= 0.02
    if equal(a[0], b[0]) and equal(a[1], b[1]) and equal(a[2], b[2]):
        return
    raise BaseException(f"test '{name}' failed, expect: {a}, got: {b}")

def alpha_composite(a: float, b: float) -> float:
    return b + a - a * b

VA = Tuple[float, float]

def normal_blend_(a: VA, b: VA) -> float:
    return b[0] * b[1] + a[0] * (1 - b[1])

def normal_blend(a: Pixel, b: Pixel) -> RGB:
    return tuple(map(lambda x: x, (normal_blend_([a[0], a[3]], [b[0], b[3]]), normal_blend_([a[1], a[3]], [b[1], b[3]]), normal_blend_([a[2], a[3]], [b[2], b[3]]))))


for i in range(100):
    a = [random.random(), random.random(), random.random(), 1]
    b = [random.random(), random.random(), random.random(), random.random()]
    pixelEqual(f"normal-{i}", blending(a, b, 'normal')[:3], normal_blend(a,b)) 

