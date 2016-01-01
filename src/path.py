# -*- coding: utf-8 -*-
from os.path import join, abspath, dirname
import os
import bottle

src = dirname(abspath(__file__))
root = dirname(src)
www = join(root, 'www')
mp4 = r'C:\rec\REC-MP4'
bottle.TEMPLATE_PATH.insert(0, join(src, 'views'))

