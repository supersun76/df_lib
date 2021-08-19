#!/usr/bin/env python
# -*- coding: gbk -*-
"""
    @author: Justin Shen
    Created on 2021/8/2

    Copyright: Justin Shen (zqshen.pub@gmail.com)
    License: Apache-2.0
    Licensed under the Apache License, Version 2.0 (the "License"); you may
    not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import logging
import platform
import sys
from ctypes import *


class SlabDesFireEnv(object):
    def __init__(self):
        if sys.platform == 'win32':
            self.lib = windll.LoadLibrary(
                './df_lib_x64.dll' if platform.architecture()[0].find('64') >= 0 else './df_lib_x86.dll')
        elif sys.platform == 'linux':
            if platform.architecture()[0].find('64')>=0:
                self.lib = cdll.LoadLibrary('./libdf_lib_x64.so')
            else:
                raise Exception("df_lib do not support Linux x86 (32-bit) environment")
        else:
            raise Exception("Please use in Windows platform")

        self._create = self.lib.desfire_api_create
        self._create.restype = c_void_p

        self._free = self.lib.desfire_api_free
        self._free.argtypes = [c_void_p]

        self._sendStr = self.lib.desfire_api_send_str
        self._sendStr.argtypes = [c_void_p, c_char_p]
        self._sendStr.restype = c_char_p

        self.inst = c_void_p(0)
        self.cmdStr = None
        self.respStr = None
        self.resp = None
        self.sw = 0

    def create(self):
        self.free()
        self.inst = self._create()
        if self.inst == 0:
            raise Exception("Create desfire environment instance failed")
        return self

    def free(self):
        if self.inst != c_void_p(None):
            self._free(self.inst)
            self.inst = c_void_p(None)
        return self

    def sendStr(self, command):
        logging.info('*' + '.' * 78 + '*')
        if command is None or not isinstance(command, str) or len(command) == 0:
            raise Exception("Command is invalid")
        logging.info("* CMD:")
        if len(command) > 0:
            lines = (command[i:i + 32] for i in range(0, len(command), 32))
            for line in lines:
                line = " ".join(line[i:i + 2] for i in range(0, len(line), 2))
                line = " | ".join(line[i:i + 24] for i in range(0, len(line), 24))
                logging.info(f"*     {line}")
        self.cmdStr = command
        self.respStr = self._sendStr(
            self.inst, self.cmdStr.encode(encoding='utf-8')).decode('utf-8')
        parts = self.respStr.split(',')
        if len(parts) != 2:
            raise Exception("Command response error")
        self.sw = int(parts[0])
        self.resp = parts[1]
        if self.sw >= 0:
            logging.info(
                f"* RESULT: SW={hex(self.sw).upper()[2:]}")
            if len(self.resp) > 0:
                lines = (self.resp[i:i + 32]
                         for i in range(0, len(self.resp), 32))
                for line in lines:
                    line = " ".join(line[i:i + 2]
                                    for i in range(0, len(line), 2))
                    line = " | ".join(line[i:i + 24]
                                      for i in range(0, len(line), 24))
                    logging.info(f"*     {line}")
        else:
            logging.info(f'* RESULT: SW={self.sw}, {self.resp}')
        return self

    @staticmethod
    def selftest():
        logger = logging.getLogger()
        logger.setLevel('INFO')
        BASIC_FORMAT = "%(asctime)s: %(message)s"
        DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
        chlr = logging.StreamHandler()
        chlr.setFormatter(formatter)
        chlr.setLevel('INFO')
        logger.addHandler(chlr)

        df = SlabDesFireEnv()
        df.create()
        df.sendStr('60')
        df.free()


if __name__ == '__main__':
    SlabDesFireEnv.selftest()
