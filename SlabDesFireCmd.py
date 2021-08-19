#!/usr/bin/env python
# -*- coding: gbk -*-
"""
    @author: Justin Shen
    Created on 2021/7/12

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
from jbytes import JBytes


class SlabDesFireCmd(object):
    MODES = (None, 'plain', 'mac', 'full')
    MODES_CODE = {None: 0, 'plain': 0, 'mac': 1, 'full': 2}

    @staticmethod
    def _checkParmType(parm, class_type, parm_name):
        if not isinstance(parm, class_type):
            raise Exception(
                f'{parm_name} should be type {class_type.__name__}')

    def __init__(self, cmd, name, mode):
        SlabDesFireCmd._checkParmType(cmd, int, 'cmd')
        if mode not in SlabDesFireCmd.MODES:
            raise Exception("DesFire command should have mode")
        self.cmd = cmd
        self.name = name if name is not None else ""
        self.mode = mode
        self.data = JBytes()

    def __str__(self):
        return f'SlabDesFireCmd(cmd={hex(self.cmd)}, name="{self.name}", mode="{self.mode}", cmd_data="{self.data.hex()}")'

    def toCmdStr(self):
        ret = JBytes().putByte(self.cmd).putBytes(self.data)
        return ret.hex()

    @staticmethod
    def Authenticate(keyNo, key):
        SlabDesFireCmd._checkParmType(keyNo, int, 'keyNo')
        ret = SlabDesFireCmd(0xFF, 'authenticate', None)
        key = JBytes(key)
        ret.data.putByte(0x0A).putByte(keyNo).putByte(len(key)).putBytes(key)
        return ret

    @staticmethod
    def AuthenticateISO(keyNo, key):
        SlabDesFireCmd._checkParmType(keyNo, int, 'keyNo')
        ret = SlabDesFireCmd(0xFF, 'authenticateISO', None)
        key = JBytes(key)
        ret.data.putByte(0x1A).putByte(keyNo).putByte(len(key)).putBytes(key)
        return ret

    @staticmethod
    def AuthenticateAES(keyNo, key):
        SlabDesFireCmd._checkParmType(keyNo, int, 'keyNo')
        ret = SlabDesFireCmd(0xFF, 'authenticateAES', None)
        key = JBytes(key)
        ret.data.putByte(0xAA).putByte(keyNo).putByte(len(key)).putBytes(key)
        return ret

    @staticmethod
    def AuthenticateEV2First(keyNo, key, PCDcap2):
        SlabDesFireCmd._checkParmType(keyNo, int, 'keyNo')
        ret = SlabDesFireCmd(0xFF, 'authenticate_ev2_first', None)
        key = JBytes(key)
        PCDcap2 = JBytes(PCDcap2)
        ret.data.putByte(0x71).putByte(keyNo).putByte(len(key)).putBytes(
            key)
        if len(PCDcap2) > 0:
            ret.data.putByte(len(PCDcap2)).putBytes(PCDcap2)
        return ret

    @staticmethod
    def AuthenticateEV2NonFirst(keyNo, key):
        SlabDesFireCmd._checkParmType(keyNo, int, 'keyNo')
        ret = SlabDesFireCmd(0xFF, 'authenticate_ev2_non_first', None)
        key = JBytes(key)
        ret.data.putByte(0x77).putByte(keyNo).putByte(len(key)).putBytes(key)
        return ret

    @staticmethod
    def FreeMem():
        return SlabDesFireCmd(0x6E, 'free_mem', 'mac')

    @staticmethod
    def Format():
        return SlabDesFireCmd(0xFC, 'format', 'mac')

    @staticmethod
    def SetConfiguration(option, data):
        SlabDesFireCmd._checkParmType(option, int, 'option')
        ret = SlabDesFireCmd(0x5C, 'set_configuration', 'full')
        ret.data.putByte(option).append(data)
        return ret

    @staticmethod
    def GetVersion():
        return SlabDesFireCmd(0x60, 'get_version', 'mac')

    @staticmethod
    def GetCardUID():
        return SlabDesFireCmd(0x51, 'get_card_uid', 'full')

    @staticmethod
    def ChangeKey(keyNo, new_key, old_key, aesVer):
        SlabDesFireCmd._checkParmType(keyNo, int, 'keyNo')
        ret = SlabDesFireCmd(0xFF, 'change_key', None)
        new_key = JBytes(new_key)
        old_key = JBytes(old_key)
        ret.data.putByte(0xC4).putByte(keyNo).putByte(len(new_key)).putBytes(
            new_key).putByte(len(old_key)).putBytes(old_key)
        if aesVer is not None:
            ret.data.putByte(aesVer)
        return ret

    @staticmethod
    def ChangeKeyEV2(keySetNo, keyNo, new_key, old_key, aesVer):
        SlabDesFireCmd._checkParmType(keySetNo, int, 'keySetNo')
        SlabDesFireCmd._checkParmType(keyNo, int, 'keyNo')
        ret = SlabDesFireCmd(0xFF, 'change_key_ev2', None)
        new_key = JBytes(new_key)
        old_key = JBytes(old_key)
        ret.data.putByte(0xC6).putByte(keySetNo).putByte(keyNo).putByte(len(new_key)).putBytes(
            new_key).putByte(len(old_key)).putBytes(old_key)
        if aesVer is not None:
            ret.data.putByte(aesVer)
        return ret

    @staticmethod
    def InitializeKeySet(keySetNo, keySetType):
        SlabDesFireCmd._checkParmType(keySetNo, int, 'keySetNo')
        SlabDesFireCmd._checkParmType(keySetType, int, 'keySetType')
        ret = SlabDesFireCmd(0x56, 'initialize_key_set', 'mac')
        ret.data.putByte(keySetNo).putByte(keySetType)
        return ret

    @staticmethod
    def FinializeKeySet(keySetNo, keySetVersion):
        SlabDesFireCmd._checkParmType(keySetNo, int, 'keySetNo')
        SlabDesFireCmd._checkParmType(keySetVersion, int, 'keySetVersion')
        ret = SlabDesFireCmd(0x57, 'finialize_key_set', 'mac')
        ret.data.putByte(keySetNo).putByte(keySetVersion)
        return ret

    @staticmethod
    def RollKeySet(keySetNo):
        SlabDesFireCmd._checkParmType(keySetNo, int, 'keySetNo')
        ret = SlabDesFireCmd(0x55, 'roll_key_set', 'mac')
        ret.data.putByte(keySetNo)
        return ret

    @staticmethod
    def GetKeySettings():
        return SlabDesFireCmd(0x45, 'get_key_settings', 'mac')

    @staticmethod
    def ChangeKeySettings(settings):
        SlabDesFireCmd._checkParmType(settings, int, 'settings')
        ret = SlabDesFireCmd(0x54, 'change_key_settings', 'full')
        ret.data.putByte(settings)
        return ret

    @staticmethod
    def GetKeyVersion(keyNo, keySetNo=None):
        SlabDesFireCmd._checkParmType(keyNo, int, 'keyNo')
        ret = SlabDesFireCmd(0x64, 'get_key_version', 'mac')
        ret.data.putByte(keyNo)
        if keySetNo is not None:
            SlabDesFireCmd._checkParmType(keySetNo, int, 'keySetNo')
            ret.data.putByte(keySetNo)
        return ret

    @staticmethod
    def CreateApp(desfireAid, keyConf1, keyConf2, keyConf3=None, aksVersion=None, qytKeySets=None, maxKeySize=None,
                  keySetSetting=None,
                  isoFid=None, isoAid=None):
        SlabDesFireCmd._checkParmType(desfireAid, int, 'desfireAid')
        SlabDesFireCmd._checkParmType(keyConf1, int, 'keyConf1')
        SlabDesFireCmd._checkParmType(keyConf2, int, 'keyConf2')
        ret = SlabDesFireCmd(0xCA, 'create_app', 'mac')
        ret.data.putInt3BytesLE(desfireAid).putByte(keyConf1).putByte(keyConf2)
        if keyConf3 is not None:
            SlabDesFireCmd._checkParmType(keyConf3, int, 'keyConf3')
            ret.data.putByte(keyConf3)
        if aksVersion is not None:
            SlabDesFireCmd._checkParmType(aksVersion, int, 'aksVersion')
            ret.data.putByte(aksVersion)
        if qytKeySets is not None:
            SlabDesFireCmd._checkParmType(qytKeySets, int, 'qytKeySets')
            ret.data.putByte(qytKeySets)
        if maxKeySize is not None:
            SlabDesFireCmd._checkParmType(maxKeySize, int, 'maxKeySize')
            ret.data.putByte(maxKeySize)
        if keySetSetting is not None:
            SlabDesFireCmd._checkParmType(keySetSetting, int, 'maxKeySize')
            ret.data.putByte(keySetSetting)
        if isoFid is not None:
            SlabDesFireCmd._checkParmType(isoFid, int, 'isoFid')
            # ret.data.putShortLE(isoFid)
            ret.data.putShort(isoFid)
        if isoAid is not None:
            # ret.data.putBytes(JBytes(isoAid)[::-1])
            ret.data.append(isoAid)
        return ret

    @staticmethod
    def DeleteApp(aid):
        SlabDesFireCmd._checkParmType(aid, int, 'aid')
        ret = SlabDesFireCmd(0xDA, 'delete_app', 'mac')
        ret.data.putInt3BytesLE(aid)
        return ret

    @staticmethod
    def CreateDelegatedApplication(desfireAid, damSlotNo, damSlotVer, quotaLimit, keyEncrypted, damMac,
                                   keyConf1, keyConf2, keyConf3=None, aksVersion=None, qytKeySets=None, maxKeySize=None,
                                   keySetSetting=None,
                                   isoFid=None, isoAid=None
                                   ):
        SlabDesFireCmd._checkParmType(desfireAid, int, 'desfireAid')
        SlabDesFireCmd._checkParmType(damSlotNo, int, 'damSlotNo')
        SlabDesFireCmd._checkParmType(damSlotVer, int, 'damSlotVer')
        SlabDesFireCmd._checkParmType(quotaLimit, int, 'quotaLimit')
        SlabDesFireCmd._checkParmType(keyConf1, int, 'keyConf1')
        SlabDesFireCmd._checkParmType(keyConf2, int, 'keyConf2')
        keyEncrypted = JBytes(keyEncrypted)
        if keyEncrypted.length() != 32:
            raise Exception('key data should be 32 byte')
        damMac = JBytes(damMac)
        if damMac.length() != 8:
            raise Exception('mac data should be 8 byte')
        ret = SlabDesFireCmd(0xC9, 'create_deleteated_app', 'mac')
        ret.data.putInt3BytesLE(desfireAid).putShortLE(damSlotNo).putByte(
            damSlotVer).putShortLE(quotaLimit).putByte(keyConf1).putByte(keyConf2)
        if keyConf3 is not None:
            SlabDesFireCmd._checkParmType(keyConf3, int, 'keyConf3')
            ret.data.putByte(keyConf3)
        if aksVersion is not None:
            SlabDesFireCmd._checkParmType(aksVersion, int, 'aksVersion')
            ret.data.putByte(aksVersion)
        if qytKeySets is not None:
            SlabDesFireCmd._checkParmType(qytKeySets, int, 'qytKeySets')
            ret.data.putByte(qytKeySets)
        if maxKeySize is not None:
            SlabDesFireCmd._checkParmType(maxKeySize, int, 'maxKeySize')
            ret.data.putByte(maxKeySize)
        if keySetSetting is not None:
            SlabDesFireCmd._checkParmType(keySetSetting, int, 'maxKeySize')
            ret.data.putByte(keySetSetting)
        if isoFid is not None:
            SlabDesFireCmd._checkParmType(isoFid, int, 'isoFid')
            # ret.data.putShortLE(isoFid)
            ret.data.putShort(isoFid)
        if isoAid is not None:
            # ret.data.putBytes(JBytes(isoAid)[::-1])
            ret.data.append(isoAid)
        ret.data.putBytes(keyEncrypted).putBytes(damMac)
        return ret

    @staticmethod
    def SelectApp(desfireAid1, desfireAid2=None):
        SlabDesFireCmd._checkParmType(desfireAid1, int, 'desfireAid1')
        ret = SlabDesFireCmd(0x5A, 'select_app', None)
        ret.data.putInt3BytesLE(desfireAid1)
        if desfireAid2 is not None:
            SlabDesFireCmd._checkParmType(desfireAid2, int, 'desfireAid2')
            ret.data.putInt3BytesLE(desfireAid2)
        return ret

    @staticmethod
    def GetAppIDs():
        return SlabDesFireCmd(0x6A, 'get_application_ids', 'mac')

    @staticmethod
    def GetDFNames():
        return SlabDesFireCmd(0x6D, 'get_DF_names', 'mac')

    @staticmethod
    def GetDelegatedInfo(damSlotNo):
        SlabDesFireCmd._checkParmType(damSlotNo, int, 'damSlotNo')
        ret = SlabDesFireCmd(0x69, 'get_delegated_info', 'mac')
        ret.data.putShortLE(damSlotNo)
        return ret

    @staticmethod
    def CreateStdDataFile(fileNo, fileOption, accessRight, fileSize, isoFileID=None):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        ret = SlabDesFireCmd(0xCD, 'create_std_data_file', 'mac')
        ret.data.putByte(fileNo)
        if isoFileID is not None:
            SlabDesFireCmd._checkParmType(isoFileID, int, 'isoFileID')
            ret.data.putShortLE(isoFileID)
        SlabDesFireCmd._checkParmType(fileOption, int, 'fileOption')
        ret.data.putByte(fileOption)
        SlabDesFireCmd._checkParmType(accessRight, int, 'accessRight')
        ret.data.putShortLE(accessRight)
        SlabDesFireCmd._checkParmType(fileSize, int, 'fileSize')
        ret.data.putInt3BytesLE(fileSize)
        return ret

    @staticmethod
    def CreateBackupDataFile(fileNo, fileOption, accessRight, fileSize, isoFileID=None):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        ret = SlabDesFireCmd(0xCB, 'create_std_data_file', 'mac')
        ret.data.putByte(fileNo)
        if isoFileID is not None:
            SlabDesFireCmd._checkParmType(isoFileID, int, 'isoFileID')
            ret.data.putShortLE(isoFileID)
        SlabDesFireCmd._checkParmType(fileOption, int, 'fileOption')
        ret.data.putByte(fileOption)
        SlabDesFireCmd._checkParmType(accessRight, int, 'accessRight')
        ret.data.putShortLE(accessRight)
        SlabDesFireCmd._checkParmType(fileSize, int, 'fileSize')
        ret.data.putInt3BytesLE(fileSize)
        return ret

    @staticmethod
    def CreateValueFile(fileNo, fileOption, accessRight, lowLimit, upperLimit, value, limitedCreditEnable):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(fileOption, int, 'fileOption')
        SlabDesFireCmd._checkParmType(accessRight, int, 'accessRight')
        SlabDesFireCmd._checkParmType(lowLimit, int, 'lowLimit')
        SlabDesFireCmd._checkParmType(upperLimit, int, 'upperLimit')
        SlabDesFireCmd._checkParmType(value, int, 'value')
        SlabDesFireCmd._checkParmType(
            limitedCreditEnable, int, 'limitedCreditEnable')
        ret = SlabDesFireCmd(0xCC, 'create_value_file', 'mac')
        ret.data.putByte(fileNo).putByte(fileOption).putShortLE(
            accessRight).putIntLE(lowLimit).putIntLE(upperLimit).putIntLE(value).putByte(limitedCreditEnable)
        return ret

    @staticmethod
    def CreateLinearRecordFile(fileNo, fileOption, accessRight, recordSize, recordQty, isoFileID=None):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(fileOption, int, 'fileOption')
        SlabDesFireCmd._checkParmType(accessRight, int, 'accessRight')
        SlabDesFireCmd._checkParmType(recordSize, int, 'recordSize')
        SlabDesFireCmd._checkParmType(recordQty, int, 'recordQty')
        ret = SlabDesFireCmd(0xC1, 'create_linear_record_file', 'mac')
        ret.data.putByte(fileNo)
        if isoFileID is not None:
            SlabDesFireCmd._checkParmType(isoFileID, int, 'isoFileID')
            ret.data.putShortLE(isoFileID)
        ret.data.putByte(fileOption).putShortLE(accessRight).putInt3BytesLE(
            recordSize).putInt3BytesLE(recordQty)
        return ret

    @staticmethod
    def CreateCyclicRecordFile(fileNo, fileOption, accessRight, recordSize, recordQty, isoFileID=None):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(fileOption, int, 'fileOption')
        SlabDesFireCmd._checkParmType(accessRight, int, 'accessRight')
        SlabDesFireCmd._checkParmType(recordSize, int, 'recordSize')
        SlabDesFireCmd._checkParmType(recordQty, int, 'recordQty')
        ret = SlabDesFireCmd(0xC0, 'create_cyclic_record_file', 'mac')
        ret.data.putByte(fileNo)
        if isoFileID is not None:
            SlabDesFireCmd._checkParmType(isoFileID, int, 'isoFileID')
            ret.data.putShortLE(isoFileID)
        ret.data.putByte(fileOption).putShortLE(accessRight).putInt3BytesLE(
            recordSize).putInt3BytesLE(recordQty)
        return ret

    @staticmethod
    def CreateTransactionMacFile(fileNo, fileOption, accessRight, macOption, key, keyVer):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(fileOption, int, 'fileOption')
        SlabDesFireCmd._checkParmType(accessRight, int, 'accessRight')
        SlabDesFireCmd._checkParmType(macOption, int, 'macOption')
        SlabDesFireCmd._checkParmType(keyVer, int, 'keyVer')
        key = JBytes(key)
        if key.length() != 16:
            raise Exception("Invalid key")
        ret = SlabDesFireCmd(0xCE, 'create_transaction_mac_file', 'full')
        ret.data.putByte(fileNo).putByte(fileOption).putShortLE(
            accessRight).putByte(macOption).putBytes(key).putByte(keyVer)
        return ret

    @staticmethod
    def DeleteFile(fileNo):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        ret = SlabDesFireCmd(0xDF, 'delete_file', 'mac')
        ret.data.putByte(fileNo)
        return ret

    @staticmethod
    def GetFileIDs():
        return SlabDesFireCmd(0x6F, 'get_file_ids', 'mac')

    @staticmethod
    def GetISOFileIDs():
        return SlabDesFireCmd(0x61, 'get_iso_file_ids', 'mac')

    @staticmethod
    def GetFileSettings(fileNo):
        ret = SlabDesFireCmd(0xF5, 'get_file_settings', 'mac')
        ret.data.putByte(fileNo)
        return ret

    @staticmethod
    def ChangeFileSettings(fileNo, fileOption, accessRight, nrAddARs=None, addAccessRights=None):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(fileOption, int, 'fileOption')
        SlabDesFireCmd._checkParmType(accessRight, int, 'accessRight')
        ret = SlabDesFireCmd(0x5F, 'change_file_settings', 'full')
        ret.data.putByte(fileNo).putByte(fileOption).putShortLE(accessRight)
        if nrAddARs is not None:
            SlabDesFireCmd._checkParmType(nrAddARs, int, 'nrAddARs')
            addAccessRights = JBytes(addAccessRights)
            if nrAddARs * 2 != addAccessRights.length():
                raise Exception('Addtiona access right data error')
            ret.data.putByte(nrAddARs).putBytes(addAccessRights)
        return ret

    @staticmethod
    def ReadData(fileNo, offset, length, commMode):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(offset, int, 'offset')
        SlabDesFireCmd._checkParmType(length, int, 'length')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0xBD, 'read_data', commMode)
        ret.data.putByte(fileNo).putInt3BytesLE(offset).putInt3BytesLE(
            length).putByte(SlabDesFireCmd.MODES_CODE[commMode])
        return ret

    @staticmethod
    def ReadDataISO(fileNo, offset, length, commMode):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(offset, int, 'offset')
        SlabDesFireCmd._checkParmType(length, int, 'length')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0xAD, 'read_data_iso', commMode)
        ret.data.putByte(fileNo).putInt3BytesLE(offset).putInt3BytesLE(
            length).putByte(SlabDesFireCmd.MODES_CODE[commMode])
        return ret

    @staticmethod
    def WriteData(fileNo, offset, length, commMode, *data):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(offset, int, 'offset')
        SlabDesFireCmd._checkParmType(length, int, 'length')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0x3D,
                             'write_data', commMode)
        ret.data.putByte(fileNo).putInt3BytesLE(offset).putInt3BytesLE(
            length).putByte(SlabDesFireCmd.MODES_CODE[commMode]).append(*data)
        return ret

    @staticmethod
    def WriteDataISO(fileNo, offset, length, commMode, *data):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(offset, int, 'offset')
        SlabDesFireCmd._checkParmType(length, int, 'length')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0x8D,
                             'write_data_iso', commMode)
        ret.data.putByte(fileNo).putInt3BytesLE(offset).putInt3BytesLE(
            length).putByte(SlabDesFireCmd.MODES_CODE[commMode]).append(*data)
        return ret

    @staticmethod
    def GetValue(fileNo, commMode):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0x6C, 'get_value', commMode)
        ret.data.putByte(fileNo).putByte(SlabDesFireCmd.MODES_CODE[commMode])
        return ret

    @staticmethod
    def Credit(fileNo, value, commMode):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(value, int, 'value')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0x0C, 'credit', commMode)
        ret.data.putByte(fileNo).putByte(
            SlabDesFireCmd.MODES_CODE[commMode]).putIntLE(value)
        return ret

    @staticmethod
    def LimitedCredit(fileNo, value, commMode):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(value, int, 'value')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0x1C, 'limited_credit', commMode)
        ret.data.putByte(fileNo).putByte(
            SlabDesFireCmd.MODES_CODE[commMode]).putIntLE(value)
        return ret

    @staticmethod
    def Debit(fileNo, value, commMode):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(value, int, 'value')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0xDC, 'debit', commMode)
        ret.data.putByte(fileNo).putByte(
            SlabDesFireCmd.MODES_CODE[commMode]).putIntLE(value)
        return ret

    @staticmethod
    def ReadRecord(fileNo, recNo, recCount, commMode):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(recNo, int, 'recNo')
        SlabDesFireCmd._checkParmType(recCount, int, 'recCount')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0xBB, 'read_record', commMode)
        ret.data.putByte(fileNo).putInt3BytesLE(recNo).putInt3BytesLE(recCount).putByte(
            SlabDesFireCmd.MODES_CODE[commMode])
        return ret

    @staticmethod
    def ReadRecordISO(fileNo, recNo, recCount, commMode):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(recNo, int, 'recNo')
        SlabDesFireCmd._checkParmType(recCount, int, 'recCount')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0xAB, 'read_record_iso', commMode)
        ret.data.putByte(fileNo).putInt3BytesLE(recNo).putInt3BytesLE(recCount).putByte(
            SlabDesFireCmd.MODES_CODE[commMode])
        return ret

    @staticmethod
    def WriteRecord(fileNo, offset, length, commMode, *data):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(offset, int, 'offset')
        SlabDesFireCmd._checkParmType(length, int, 'length')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0x3B, 'write_record', commMode)
        ret.data.putByte(fileNo).putInt3BytesLE(offset).putInt3BytesLE(length).putByte(
            SlabDesFireCmd.MODES_CODE[commMode]).append(*data)
        return ret

    @staticmethod
    def WriteRecordISO(fileNo, offset, length, commMode, *data):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(offset, int, 'offset')
        SlabDesFireCmd._checkParmType(length, int, 'length')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0x8B, 'write_record_iso', commMode)
        ret.data.putByte(fileNo).putInt3BytesLE(offset).putInt3BytesLE(length).putByte(
            SlabDesFireCmd.MODES_CODE[commMode]).append(*data)
        return ret

    @staticmethod
    def UpdateRecord(fileNo, recNo, offset, length, commMode, *data):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(recNo, int, 'recNo')
        SlabDesFireCmd._checkParmType(offset, int, 'offset')
        SlabDesFireCmd._checkParmType(length, int, 'length')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0xDB, 'update_record', commMode)
        ret.data.putByte(fileNo).putInt3BytesLE(
            recNo).putInt3BytesLE(offset).putInt3BytesLE(length).putByte(
            SlabDesFireCmd.MODES_CODE[commMode]).append(*data)
        return ret

    @staticmethod
    def UpdateRecordISO(fileNo, recNo, offset, length, commMode, *data):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        SlabDesFireCmd._checkParmType(recNo, int, 'recNo')
        SlabDesFireCmd._checkParmType(offset, int, 'offset')
        SlabDesFireCmd._checkParmType(length, int, 'length')
        if commMode not in SlabDesFireCmd.MODES:
            raise Exception("Unknonw comm mode")
        ret = SlabDesFireCmd(0xBA, 'update_record_iso', commMode)
        ret.data.putByte(fileNo).putInt3BytesLE(
            recNo).putInt3BytesLE(offset).putInt3BytesLE(length).putByte(
            SlabDesFireCmd.MODES_CODE[commMode]).append(*data)
        return ret

    @staticmethod
    def ClearRecordFile(fileNo):
        SlabDesFireCmd._checkParmType(fileNo, int, 'fileNo')
        ret = SlabDesFireCmd(0xEB, 'write_record', 'mac')
        ret.data.putByte(fileNo)
        return ret

    @staticmethod
    def CommitTransaction(isNeedTMC):
        ret = SlabDesFireCmd(0xC7, 'commit_transaction', 'mac')
        ret.data.putByte(1 if isNeedTMC else 0)
        return ret

    @staticmethod
    def AbortTransaction():
        return SlabDesFireCmd(0xA7, 'abort_transaction', 'mac')

    @staticmethod
    def commitReaderID(readerID):
        readerID = JBytes(readerID)
        if readerID.length() != 16:
            raise Exception("Reader ID should be 16 bytes")
        ret = SlabDesFireCmd(0xC8, 'commit_reader_id', 'mac')
        ret.data.putBytes(readerID)
        return ret

    @staticmethod
    def preparePC():
        return SlabDesFireCmd(0xF0, 'proximity_check', None)

    @staticmethod
    def proximityCheck(randC):
        ret = SlabDesFireCmd(0xF2, 'proximity_check', None)
        d = JBytes(randC)
        ret.data.putByte(d.length()).putBytes(d)
        return ret

    @staticmethod
    def verifyPC(mac):
        ret = SlabDesFireCmd(0xFD, 'verify_pc', None)
        ret.data.append(mac)
        return ret

    @staticmethod
    def readSig(addr):
        SlabDesFireCmd._checkParmType(addr, int, 'addr')
        ret = SlabDesFireCmd(0x3C, 'read_sig', 'full')
        ret.data.putByte(addr)
        return ret

    @staticmethod
    def vcISOSelect(aid, keyEnc, keyMac):
        aid = JBytes(aid)
        keyEnc = JBytes(keyEnc)
        keyMac = JBytes(keyMac)
        if aid.length() == 0 or keyEnc.length() != 16 or keyMac.length() != 16:
            raise Exception("Invalid parameter")
        ret = SlabDesFireCmd(0xFF, 'virtual_card_iso_select', None)
        ret.data.putByte(0xA4)
        ret.data.putByte(aid.length()).putBytes(aid)
        ret.data.putByte(keyEnc.length()).putBytes(keyEnc)
        ret.data.putByte(keyMac.length()).putBytes(keyMac)
        return ret

    @staticmethod
    def vcProximityCheck(key):
        key = JBytes(key)
        if key.length() != 16:
            raise Exception("Invalid key")
        ret = SlabDesFireCmd(0xFF, 'virtual_card_proximity_check', None)
        ret.data.putByte(0xF0).putByte(key.length()).putBytes(key)
        return ret


if __name__ == '__main__':
    pass
