#!/usr/bin/python
# -*- coding: gbk -*-
"""
    @author: Justin Shen
    Created on 2017/5/5

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

import re


class JBytes(object):
    __RE_PATTERN_REMOVE_SPACE = re.compile(r"\s+")

    @staticmethod
    def fromInt(value, byteLength=4, isBigEndian=True):
        if not isinstance(value, int):
            raise ValueError(
                "JBytes.fromInt: parameter 'value' must be integer")
        if byteLength == 0:
            return bytearray()
        try:
            return bytearray(value.to_bytes(byteLength, byteorder='big' if isBigEndian else 'little'))
        except OverflowError:
            raise ValueError(
                "JBytes.fromInt: parameter 'value' too big to convert to byte array in 'byteLength' bytes")

    @staticmethod
    def __transfer_int__(arg):
        """
        Transfer integer to byte array according its value.
        value must >= 0
        if value is between 0~0xFF, one byte is transferred
        if value is between 0x100 ~ 0xFFFF, 2 bytes is transferred
        if value is between 0x10000~0xFFFFFF, 3 bytes is transferred
        if value is between 0x1000000~0xFFFFFFFF, 4 bytes is transferred
        """
        l = 1
        if arg < 0:
            raise ValueError("Integer should not be negative")
        elif arg < 0x100:
            l = 1
        elif arg < 0x10000:
            l = 2
        elif arg < 0x1000000:
            l = 3
        else:
            l = 4
        return bytearray(arg.to_bytes(l, byteorder='big'))

    @staticmethod
    def __transfer__(*args):
        """
        Transfer arguments to byte array.
        Acceptable arguments:
        1. integer: must >=0.
                    If between 0~0xFF, one byte is transferred
                    If between 0x100~0xFFFF, two bytes is transfered
                    If 
        """
        ret = bytearray(0)
        for arg in args:
            # integer
            if isinstance(arg, int):
                ret.extend(JBytes.__transfer_int__(arg))
            # string
            elif isinstance(arg, str):
                ret.extend(bytes.fromhex(
                    JBytes.__RE_PATTERN_REMOVE_SPACE.sub("", arg)))
            # bytes
            elif isinstance(arg, bytes):
                ret.extend(arg)
            # bytearray
            elif isinstance(arg, bytearray):
                ret.extend(arg)
            elif arg is None:
                pass
            else:
                ret.extend(bytes(arg))
        return ret

    @staticmethod
    def __formatbytes(data):
        return "".join('{:02X}'.format(x) for x in data)

    def __init__(self, *args):
        self.BYTES = JBytes.__transfer__(*args)
        self.INDEX = 0

    def __str__(self):
        if self:
            return r'{0:s}("{1:s}")'.format(self.__class__.__name__, self.BYTES.hex().upper())
        else:
            return '{0:s}()'.format(self.__class__.__name__)

    def __repr__(self):
        return self.BYTES.hex().upper()

    def __bytes__(self):
        return bytes(self.BYTES)

    def __len__(self):
        return len(self.BYTES)

    def __bool__(self):
        return len(self.BYTES) > 0

    def __iter__(self):
        for item in self.BYTES:
            yield item

    def append(self, *args):
        self.BYTES.extend(JBytes.__transfer__(*args))
        return self

    def putByte(self, arg):
        if not isinstance(arg, int):
            raise ValueError("JBytes.putByte: arg should be integer")
        self.BYTES.append(arg & 0xFF)
        return self

    def putShort(self, arg):
        if not isinstance(arg, int):
            raise ValueError("JBytes.putShort: arg should be integer")
        self.BYTES.extend((arg & 0xFFFF).to_bytes(2, byteorder='big'))
        return self

    def putShortLE(self, arg):
        if not isinstance(arg, int):
            raise ValueError("JBytes.putShortLE: arg should be integer")
        self.BYTES.extend((arg & 0xFFFF).to_bytes(2, byteorder='little'))
        return self

    def putInt3Bytes(self, arg):
        if not isinstance(arg, int):
            raise ValueError("JBytes.putInt3Bytes: arg should be integer")
        self.BYTES.extend((arg & 0xFFFFFF).to_bytes(3, byteorder='big'))
        return self

    def putInt3BytesLE(self, arg):
        if not isinstance(arg, int):
            raise ValueError("JBytes.putInt3BytesLE: arg should be integer")
        self.BYTES.extend((arg & 0xFFFFFF).to_bytes(3, byteorder='little'))
        return self

    def putInt(self, arg):
        if not isinstance(arg, int):
            raise ValueError("JBytes.putInt: arg should be integer")
        self.BYTES.extend((arg & 0xFFFFFFFF).to_bytes(4, byteorder='big'))
        return self

    def putIntLE(self, arg):
        if not isinstance(arg, int):
            raise ValueError("JBytes.putIntLE: arg should be integer")
        self.BYTES.extend((arg & 0xFFFFFFFF).to_bytes(4, byteorder='little'))
        return self

    def putHexString(self, arg):
        if not isinstance(arg, str):
            raise ValueError("JBytes.putHexString: arg must be string")
        self.BYTES.extend(bytes.fromhex(
            JBytes.__RE_PATTERN_REMOVE_SPACE.sub("", arg)))
        return self

    def putBytes(self, arg):
        self.BYTES.extend(bytes(arg))
        return self

    def clear(self):
        self.BYTES = bytearray()
        self.INDEX = 0
        return self

    def reset(self):
        self.INDEX = 0
        return self

    def length(self):
        return len(self.BYTES)

    def getByte(self):
        ret = self.BYTES[self.INDEX]
        self.INDEX += 1
        return ret

    def getBytes(self, length):
        ret = self[self.INDEX:self.INDEX + length]
        self.INDEX += length
        return ret

    def getShort(self):
        return (self.getByte() << 8) + self.getByte()

    def getShortLE(self):
        return self.getByte() + (self.getByte() << 8)

    def getInt(self):
        return (self.getShort() << 16) + self.getShort()

    def getIntLE(self):
        return self.getShortLE() + (self.getShortLE() << 16)

    def getString(self, length):
        ret = self.BYTES[self.INDEX:self.INDEX + length]
        self.INDEX += length
        return ret.decode("utf-8")

    def remain(self):
        return len(self.BYTES) - self.INDEX

    def isBegin(self):
        return self.INDEX == 0

    def isEnd(self):
        return self.INDEX >= len(self.BYTES)

    def isEmpty(self):
        return len(self.BYTES) <= 0

    def bytes(self):
        return self.__bytes__()

    def hex(self):
        return self.BYTES.hex().upper()


if __name__ == "__main__":
    pass
