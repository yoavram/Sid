#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Sid.
# https://github.com/yoavram/Sid

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Yoav Ram <yoav@yoavram.com>

from __future__ import absolute_import

__license__ = u'MIT'
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from . import take_cover
