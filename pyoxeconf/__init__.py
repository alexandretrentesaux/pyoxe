#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pkg_resources

__version__ = pkg_resources.require("pyoxeconf")[0].version
# __version__ = '1.0.0'