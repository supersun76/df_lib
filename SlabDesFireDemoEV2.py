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
import unittest

from SlabDesFireCmd import SlabDesFireCmd as cmd
from SlabDesFireEnv import *


class SlabDesFireDemoEV2(unittest.TestCase):
    # Please set enable_vc to True if PICC active virtual card
    enable_vc = False

    key64_default = '00' * 8
    key128_default = '00' * 16
    key192_default = '00' * 24

    nk64 = '1122334455667788'
    nk64C = '11223344556677881122334455667788'
    nk128 = '112233445566778899aabbccddeeff00'
    nk128_1 = '112233445566778899aabbccddeeff01'
    nk128_2 = '112233445566778899aabbccddeeff02'
    nk128_3 = '112233445566778899aabbccddeeff03'
    nk128_4 = '112233445566778899aabbccddeeff04'
    nk128_5 = '112233445566778899aabbccddeeff05'
    nk128_11 = '112233445566778899aabbccddeeff11'
    nk128_12 = '112233445566778899aabbccddeeff12'
    nk128_13 = '112233445566778899aabbccddeeff13'
    nk128_14 = '112233445566778899aabbccddeeff14'
    nk128_15 = '112233445566778899aabbccddeeff15'
    nk192 = '112233445566778899aabbccddeeff008877665544332211'

    key_picc_vcconfig = 'FF11223344556677 FFEEDDCCBBAA9901'  # PICC level, key_id=0x20
    key_picc_vcproximity = 'FF11223344556677 FFEEDDCCBBAA9902'  # PICC level, key_id=0x21
    key_picc_vcselectMAC = 'FF11223344556677 FFEEDDCCBBAA9902'  # PICC level, key_id=0x22
    key_picc_vcselectENC = 'FF11223344556677 FFEEDDCCBBAA9902'  # PICC level, key_id=0x23

    desfire_aid = 'D2760000850100'

    key_mac = 'FF11223344556677 8877665544332201'
    reader_id = '4f4d4e49534c41425f52454144455231'

    data16 = bytearray((0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
                        0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x00))

    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger()
        logger.setLevel('INFO')
        BASIC_FORMAT = "%(asctime)s: %(message)s"
        DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
        chlr = logging.StreamHandler()
        chlr.setFormatter(formatter)
        chlr.setLevel('INFO')
        fhlr = logging.FileHandler(
            "df_lib_demo.txt".format(cls.__name__), mode="w+")
        fhlr.setFormatter(formatter)
        logger.addHandler(chlr)
        logger.addHandler(fhlr)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        logging.info("#" * 80)
        self.inst = SlabDesFireEnv()
        self.inst.create()

    def tearDown(self):
        self.inst.free()
        self.inst = None

    def log_sep(self):
        logging.info(
            "*==============================================================================*")
        return self

    def log_casename(self, casename):
        logging.info(f"* Demo: {casename}")
        self.log_sep()
        return self

    def log_op(self, opName):
        logging.info(
            '*------------------------------------------------------------------------------*')
        logging.info('* [ {:<72s} ] *'.format(opName))
        return self

    def _send(self, cmd):
        self.inst.sendStr(cmd.toCmdStr())
        if not self.inst.sw in (0,):
            raise Exception("ERROR")
        return self

    def _send_nocheck(self, cmd):
        self.inst.sendStr(cmd.toCmdStr())
        return self

    def _clearCard(self):
        if SlabDesFireDemoEV2.enable_vc:
            self._send_nocheck(cmd.vcISOSelect(SlabDesFireDemoEV2.desfire_aid,
                                               SlabDesFireDemoEV2.key128_default, SlabDesFireDemoEV2.key128_default))

            self._send_nocheck(cmd.vcProximityCheck(
                SlabDesFireDemoEV2.key128_default))
        else:
            self._send(cmd.SelectApp(0))
        self._send(cmd.AuthenticateISO(0, SlabDesFireDemoEV2.key64_default))
        self._send(cmd.Format())

    def test_01(self):
        self.log_casename("Basic demo")
        logging.info('''
        * This demo is to show the basic operation in PICC level
        ''')

        if SlabDesFireDemoEV2.enable_vc:
            self.log_op('Select master application using Virtual Card ISO')
            self._send_nocheck(cmd.vcISOSelect(SlabDesFireDemoEV2.desfire_aid,
                                               SlabDesFireDemoEV2.key128_default, SlabDesFireDemoEV2.key128_default))
            self.log_op('Proxmimity Check')
            self._send_nocheck(cmd.vcProximityCheck(
                SlabDesFireDemoEV2.key128_default))

        self.log_op('Select master application')._send(cmd.SelectApp(0))
        self.log_op('Authenticate PICC default key')
        self._send(cmd.AuthenticateISO(0, SlabDesFireDemoEV2.key64_default))
        self.log_op('Get card UUID')._send(cmd.GetCardUID())
        self.log_op('Get card version information')._send(cmd.GetVersion())
        self.log_op('Get card free memory')._send(cmd.FreeMem())
        self.log_op('Get chip vendor digital signature')._send_nocheck(
            cmd.readSig(0))
        self.log_op('List all applications\' Desfire AID')._send_nocheck(cmd.GetAppIDs())
        self.log_op('List all applications\' ISO AID')._send_nocheck(cmd.GetDFNames())
        self.log_op('Get master application key configuration')._send(cmd.GetKeySettings())
        self.log_op('Get master application master key verion')._send(cmd.GetKeyVersion(0))
        self.log_op('Format card')._send(cmd.Format())

    def test_02(self):
        self.log_casename("Create applications")
        logging.info('''
        * This demo is to create applications, change key(s) and authenticate 
        in each applications with suitable authenticate method
        ''')

        self._clearCard()

        self.log_op('Create application DES_64/128 with ISO AID')
        self._send(cmd.CreateApp(0x01, 0x0B, 0x3E, 0x04, None,
                                 None, None, None, 0xAD11, 'AD 00 00 00 01'))

        self.log_op('Create application DES_192 with ISO AID')
        self._send(cmd.CreateApp(0x02, 0x0B, 0x7E, 0x04, None,
                                 None, None, None, 0xAD12, 'AD 00 00 00 02'))

        self.log_op('Create application AES_128 with ISO AID')
        self._send(cmd.CreateApp(0x03, 0x0B, 0xBE, 0x04, None,
                                 None, None, None, 0xAD13, 'AD 00 00 00 03'))

        self.log_op('Create application AES_128, with 2 key sets, no ISO AID')
        self._send(cmd.CreateApp(0x04, 0x0B, 0x9E,
                                 0x01, 0x01, 0x2, 0x18, 0x00))

        self.log_op(
            'Create application AES_128, with 2 key sets, ISO AID and support CAP data and VC')
        self._send(cmd.CreateApp(0x05, 0x0B, 0xBE, 0x07, 0x01, 0x02,
                                 0x18, 0x00, 0xAD02, 'AD 00 00 00 05'))

        self.log_op('List all applications\' Desfire AID')._send(cmd.GetAppIDs())
        self.log_op('List all applications\' ISO AID')._send(cmd.GetDFNames())

        #####################################################################################
        self.log_sep()
        self.log_op('Select application 1')._send(cmd.SelectApp(1))

        self.log_op('Authenticate application 1 master key in D40 DES_64')._send(
            cmd.Authenticate(0, SlabDesFireDemoEV2.key64_default))
        self.log_op('Change application 1 key 1 to new key, DES_64')._send(cmd.ChangeKey(
            1, SlabDesFireDemoEV2.nk64C, SlabDesFireDemoEV2.key128_default, None))
        self.log_op('Change application 1 key 2 to new key, DES_128')._send(cmd.ChangeKey(
            2, SlabDesFireDemoEV2.nk128, SlabDesFireDemoEV2.key128_default, None))

        self.log_op('Authenticate application 1 key 1 in D40 DES_64')
        self._send(cmd.Authenticate(1, SlabDesFireDemoEV2.nk64))

        self.log_op('Get card UUID')._send(cmd.GetCardUID())

        self.log_op('Authenticate application 1 key 1 in EV1 DES_64')
        self._send(cmd.AuthenticateISO(1, SlabDesFireDemoEV2.nk64))

        self.log_op('Get card UUID')._send(cmd.GetCardUID())

        self.log_op('Authenticate application 1 key 2 in D40 DES_128')
        self._send(cmd.Authenticate(2, SlabDesFireDemoEV2.nk128))

        self.log_op('Get card UUID')._send(cmd.GetCardUID())

        self.log_op('Authenticate application 1 key 2 in EV1 DES_128')
        self._send(cmd.AuthenticateISO(2, SlabDesFireDemoEV2.nk128))

        self.log_op('Get card UUID')._send(cmd.GetCardUID())

        #####################################################################################
        self.log_sep()
        self.log_op('Select application 2')._send(cmd.SelectApp(2))

        self.log_op('Authenticate application 2 master key in EV1 DES_192')
        self._send(cmd.AuthenticateISO(0, SlabDesFireDemoEV2.key192_default))

        self.log_op('Change application 2 key 1 to new key DES_192')
        self._send(cmd.ChangeKey(1, SlabDesFireDemoEV2.nk192,
                                 SlabDesFireDemoEV2.key192_default, None))

        self.log_op('Authenticate application 2 key 1 in EV1 DES_192')
        self._send(cmd.AuthenticateISO(1, SlabDesFireDemoEV2.nk192))

        self.log_op('Get card UUID')._send(cmd.GetCardUID())

        #####################################################################################
        self.log_op('Select application 3')._send(cmd.SelectApp(3))

        self.log_op('Authenticate application 3 master key in EV1 AES_128')
        self._send(cmd.AuthenticateAES(0, SlabDesFireDemoEV2.key128_default))

        self.log_op(
            'Change application 3 key 1 to new key AES_128, new key version=10')
        self._send(cmd.ChangeKey(1, SlabDesFireDemoEV2.nk128,
                                 SlabDesFireDemoEV2.key128_default, 10))

        self.log_op('Authenticate application 3 key 1 EV1 AES_128')
        self._send(cmd.AuthenticateAES(1, SlabDesFireDemoEV2.nk128))

        self.log_op('Get card UUID')._send(cmd.GetCardUID())

        self.log_op('Authenticate application 3 key 1 EV2 AES_128 First')
        self._send(cmd.AuthenticateEV2First(1, SlabDesFireDemoEV2.nk128, None))

        self.log_op('Get card UUID')._send(cmd.GetCardUID())

        self.log_op('Authenticate application 3 key 1 EV2 AES_128 Non First')
        self._send(cmd.AuthenticateEV2NonFirst(1, SlabDesFireDemoEV2.nk128))

        self.log_op('Get card UUID')._send(cmd.GetCardUID())

    def test_03(self):
        self.log_casename("Key and key sets")
        logging.info('''
        * This demo is to show how to change key, get key information, change key setting,
          create key sets, initialize it and roll keys
        ''')

        self._clearCard()

        self.log_op(
            'Create application AES_128, with 2 key sets, ISO AID and support CAP data and VC')
        self._send(cmd.CreateApp(0x01, 0x0B, 0xBE, 0x07, 0x01, 0x02, 0x18, 0x01, 0xAD01, 'AD 00 00 00 01'))

        #####################################################################################
        self.log_op('Select application 1')._send(cmd.SelectApp(1))

        self.log_op('Authenticate application 1 master key in EV2 AES_128')
        self._send(cmd.AuthenticateEV2First(0, SlabDesFireDemoEV2.key128_default, None))

        self.log_op(
            'Change application 1 key 1 to new key AES_128, new key version=1')
        self._send(cmd.ChangeKey(1, SlabDesFireDemoEV2.nk128_1, SlabDesFireDemoEV2.key128_default, 1))

        self.log_op(
            'Change application 1 key 2 to new key AES_128, new key version=2')
        self._send(cmd.ChangeKey(2, SlabDesFireDemoEV2.nk128_2, SlabDesFireDemoEV2.key128_default, 2))

        self.log_op(
            'Change application 1 key 3 to new key AES_128, new key version=3')
        self._send(cmd.ChangeKey(3, SlabDesFireDemoEV2.nk128_3, SlabDesFireDemoEV2.key128_default, 3))

        self.log_op(
            'Change application 1 key 4 to new key AES_128, new key version=4')
        self._send(cmd.ChangeKey(4, SlabDesFireDemoEV2.nk128_4, SlabDesFireDemoEV2.key128_default, 4))

        self.log_op(
            'Change application 1 key 5 to new key AES_128, new key version=5')
        self._send(cmd.ChangeKey(5, SlabDesFireDemoEV2.nk128_5, SlabDesFireDemoEV2.key128_default, 5))

        self.log_op('Authenticate application 1 key 1 EV1 AES_128')
        self._send(cmd.AuthenticateAES(1, SlabDesFireDemoEV2.nk128_1))

        self.log_op('Authenticate application 1 key 2 EV2 AES_128 First')
        self._send(cmd.AuthenticateEV2First(2, SlabDesFireDemoEV2.nk128_2, None))

        self.log_op('Authenticate application 1 key 3 EV2 AES_128 First')
        self._send(cmd.AuthenticateEV2First(3, SlabDesFireDemoEV2.nk128_3, None))

        self.log_op('Get application 1 key 1/2/3/4/5 versions')
        for x in range(1, 6):
            self._send(cmd.GetKeyVersion(x))

        self.log_op('Get application 1 key settings')
        self._send(cmd.GetKeySettings())

        self.log_op(
            'Change application 1 key settings without authenticate key 0, failed')
        self._send_nocheck(cmd.ChangeKeySettings(0x0F))

        self.log_op('Authenticate application 1 master key in EV2 AES_128')
        self._send(cmd.AuthenticateEV2First(
            0, SlabDesFireDemoEV2.key128_default, None))

        self.log_op('Change application 1 key settings')
        self._send_nocheck(cmd.ChangeKeySettings(0x0F))

        self.log_op('Re-Get application 1 key settings to confirm')
        self._send(cmd.GetKeySettings())

        self.log_op('Initialize application 1 key set 1, version=2')
        self._send(cmd.InitializeKeySet(1, 2))

        self.log_op('Change application key 1 in key set 1, new key version = 11')
        self._send(cmd.ChangeKeyEV2(1, 1, SlabDesFireDemoEV2.nk128_11, SlabDesFireDemoEV2.nk128_1, 11))

        self.log_op('Change application key 2 in key set 1, new key version = 12')
        self._send(cmd.ChangeKeyEV2(1, 2, SlabDesFireDemoEV2.nk128_12, SlabDesFireDemoEV2.nk128_2, 12))

        self.log_op(
            'Change application key 3 in key set 1, new key version = 13')
        self._send(cmd.ChangeKeyEV2(1, 3, SlabDesFireDemoEV2.nk128_13, SlabDesFireDemoEV2.nk128_3, 13))

        self.log_op('Change application key 4 in key set 1, new key version = 14')
        self._send(cmd.ChangeKeyEV2(1, 4, SlabDesFireDemoEV2.nk128_14, SlabDesFireDemoEV2.nk128_4, 14))

        self.log_op(
            'Change application key 5 in key set 1, new key version = 15')
        self._send(cmd.ChangeKeyEV2(1, 5, SlabDesFireDemoEV2.nk128_15, SlabDesFireDemoEV2.nk128_5, 15))

        self.log_op('Finalize key set 1, set version as 2')
        self._send(cmd.FinializeKeySet(1, 2))

        self.log_op('Authenticate key 1 to prepare key set rolling')
        self._send(cmd.AuthenticateEV2First(1, SlabDesFireDemoEV2.nk128_1, None))

        self.log_op('Roll to key set 1')
        self._send(cmd.RollKeySet(1))

        self.log_op('Authenticate key 1 in key set 1')
        self._send(cmd.AuthenticateEV2First(1, SlabDesFireDemoEV2.nk128_11, None))

        self.log_op('Authenticate key 2 in key set 1')
        self._send(cmd.AuthenticateEV2NonFirst(2, SlabDesFireDemoEV2.nk128_12))

        self.log_op('Authenticate key 3 in key set 1')
        self._send(cmd.AuthenticateEV2NonFirst(3, SlabDesFireDemoEV2.nk128_13))

        self.log_op('Authenticate key 4 in key set 4')
        self._send(cmd.AuthenticateEV2NonFirst(4, SlabDesFireDemoEV2.nk128_14))

        self.log_op('Authenticate key 5 in key set 5')
        self._send(cmd.AuthenticateEV2NonFirst(5, SlabDesFireDemoEV2.nk128_15))

        self.log_op('Get application 1 key 1/2/3/4/5 versions')
        for x in range(1, 6):
            self._send(cmd.GetKeyVersion(x))

    def test_04(self):
        self.log_casename("Files")
        logging.info('''
        * This demo is to show how to create , operation and delete standard/backup/record
        files.
        ''')

        self._clearCard()

        self.log_op('Create application AES_128, with ISO AID and support CAP data and VC')
        self._send(cmd.CreateApp(0x01, 0x0B, 0xBE, 0x06, None, None, None, None, 0xAD01, 'AD 00 00 00 01'))

        #####################################################################################
        self.log_op('Select application 1')._send(cmd.SelectApp(1))

        self.log_op('Authenticate application 1 master key in EV2 AES_128')
        self._send(cmd.AuthenticateEV2First(0, SlabDesFireDemoEV2.key128_default, None))

        self.log_op(
            'Change application 1 key 1 to new key AES_128, new key version=1')
        self._send(cmd.ChangeKey(1, SlabDesFireDemoEV2.nk128_1, SlabDesFireDemoEV2.key128_default, 1))

        self.log_op(
            'Change application 1 key 2 to new key AES_128, new key version=2')
        self._send(cmd.ChangeKey(2, SlabDesFireDemoEV2.nk128_2, SlabDesFireDemoEV2.key128_default, 2))

        self.log_op(
            'Change application 1 key 3 to new key AES_128, new key version=3')
        self._send(cmd.ChangeKey(3, SlabDesFireDemoEV2.nk128_3, SlabDesFireDemoEV2.key128_default, 3))

        self.log_op(
            'Change application 1 key 4 to new key AES_128, new key version=4')
        self._send(cmd.ChangeKey(4, SlabDesFireDemoEV2.nk128_4, SlabDesFireDemoEV2.key128_default, 4))

        self.log_op('Create file 1 as standard file, plain communication mode, 1024 bytes size')
        self._send(cmd.CreateStdDataFile(0x01, 0x00, 0x1234, 1024, 0xFF01))

        self.log_op('Create file 2 as backup file, full communication mode, 510 bytes size')
        self._send(cmd.CreateBackupDataFile(0x02, 0x03, 0x1234, 510, 0xFF02))

        self.log_op('Create file 4 as linear record file, plain communication mode, 5 records, 16 bytes of each record')
        self._send(cmd.CreateLinearRecordFile(0x04, 0x00, 0x1234, 16, 5, 0xFF04))

        self.log_op('Create file 5 as cyclic record file, full communication mode, 5 records, 16 bytes of each record')
        self._send(cmd.CreateCyclicRecordFile(0x05, 0x03, 0x1234, 16, 5, 0xFF05))

        self.log_op('Create file 6 as transaction MAC file, plain communication mode, open')
        x = cmd.CreateTransactionMacFile(0x06, 0x00, 0xEF30, 0x02, SlabDesFireDemoEV2.key_mac, 0x88)
        print(x.toCmdStr())
        self._send(x)

        self.log_op('List all file IDs')
        self._send(cmd.GetFileIDs())

        self.log_op('Get all file ISO IDs')
        self._send(cmd.GetISOFileIDs())

        self.log_op('Authenticate key 1 for file operation')
        self._send(cmd.AuthenticateEV2NonFirst(3, SlabDesFireDemoEV2.nk128_3))
        ###############################################################################
        # File 1
        self.log_op('Read file 1, write and read again')
        self._send(cmd.ReadData(1, 0, 1024, 'plain'))
        self._send(cmd.WriteData(1, 0, 1024, 'plain', '11' * 1024))
        self._send(cmd.ReadData(1, 0, 1024, 'plain'))
        ###############################################################################
        # File 2
        self.log_op('Commit reader')
        self._send(cmd.commitReaderID(SlabDesFireDemoEV2.reader_id))
        self.log_op('Read file 2')
        self._send(cmd.ReadData(2, 0, 510, 'full'))
        self.log_op('Write file 2')
        self._send(cmd.WriteData(2, 0, 510, 'full', '22' * 510))
        self.log_op('Commit transaction and get MAC counter and MAC')
        self._send(cmd.CommitTransaction(True))
        self.log_op('Read file 2')
        self._send(cmd.ReadData(2, 0, 510, 'full'))
        ###############################################################################
        # File 4
        self.log_op('Commit reader')
        self._send(cmd.commitReaderID(SlabDesFireDemoEV2.reader_id))

        self.log_op('Write 4 records to file 4')
        SlabDesFireDemoEV2.data16[15] = 0x40
        self._send(cmd.WriteRecord(4, 0, 16, 'plain', SlabDesFireDemoEV2.data16))
        self.log_op('Commit transaction')
        self._send(cmd.CommitTransaction(True))

        SlabDesFireDemoEV2.data16[15] += 1
        self.log_op('Commit reader')
        self._send(cmd.commitReaderID(SlabDesFireDemoEV2.reader_id))
        self._send(cmd.WriteRecord(4, 0, 16, 'plain', SlabDesFireDemoEV2.data16))
        self.log_op('Commit transaction')
        self._send(cmd.CommitTransaction(True))

        self.log_op('Read all records')
        self._send(cmd.ReadRecord(4, 0, 0, 'plain'))

        ###############################################################################
        # File 5
        self.log_op('Commit reader')
        self._send(cmd.commitReaderID(SlabDesFireDemoEV2.reader_id))

        self.log_op('Write 4 records to file 5')
        SlabDesFireDemoEV2.data16[15] = 0x50
        self._send(cmd.WriteRecord(5, 0, 16, 'full', SlabDesFireDemoEV2.data16))
        self.log_op('Commit transaction')
        self._send(cmd.CommitTransaction(True))

        SlabDesFireDemoEV2.data16[15] += 1
        self.log_op('Commit reader')
        self._send(cmd.commitReaderID(SlabDesFireDemoEV2.reader_id))
        self._send(cmd.WriteRecord(5, 0, 16, 'full', SlabDesFireDemoEV2.data16))
        self.log_op('Commit transaction')
        self._send(cmd.CommitTransaction(True))

        self.log_op('Read all records')
        self._send(cmd.ReadRecord(5, 0, 0, 'full'))

        ###############################################################################
        self.log_op('Authenticate application 1 key 4 in EV2 AES_128')
        self._send(cmd.AuthenticateEV2First(4, SlabDesFireDemoEV2.nk128_4, None))
        self.log_op('Change file 1 settings')
        self._send(cmd.ChangeFileSettings(1, 0x03, 0x3333))
        self.log_op('Authenticate application 1 master key in EV2 AES_128')
        self._send(cmd.AuthenticateEV2NonFirst(
            0, SlabDesFireDemoEV2.key128_default))
        self.log_op('Get file 1 settings')
        self._send(cmd.GetFileSettings(1))
        ###############################################################################
        self.log_op('Authenticate application 1 master key in EV2 AES_128')
        self._send(cmd.AuthenticateEV2NonFirst(
            0, SlabDesFireDemoEV2.key128_default))
        self.log_op('Delete all files')
        self.log_op('Delete')
        for x in (1, 2, 4, 5, 6):
            self._send(cmd.DeleteFile(x))

    def test_05(self):
        self.log_casename("Files")
        logging.info('''
        * This demo is to show how to create , operation and delete value files,
          and transaction with transaction MAC.
        ''')

        self._clearCard()

        self.log_op('Create application AES_128, with ISO AID and support CAP data and VC')
        self._send(cmd.CreateApp(0x01, 0x0B, 0xBE, 0x06, None, None, None, None, 0xAD01, 'AD 00 00 00 01'))

        #####################################################################################
        self.log_op('Select application 1')._send(cmd.SelectApp(1))

        self.log_op('Authenticate application 1 master key in EV2 AES_128')
        self._send(cmd.AuthenticateEV2First(0, SlabDesFireDemoEV2.key128_default, None))

        self.log_op('Change application 1 key 1 to new key AES_128, new key version=1')
        self._send(cmd.ChangeKey(1, SlabDesFireDemoEV2.nk128_1, SlabDesFireDemoEV2.key128_default, 1))

        self.log_op('Change application 1 key 2 to new key AES_128, new key version=2')
        self._send(cmd.ChangeKey(2, SlabDesFireDemoEV2.nk128_2, SlabDesFireDemoEV2.key128_default, 2))

        self.log_op('Change application 1 key 3 to new key AES_128, new key version=3')
        self._send(cmd.ChangeKey(3, SlabDesFireDemoEV2.nk128_3, SlabDesFireDemoEV2.key128_default, 3))

        self.log_op(
            'Change application 1 key 4 to new key AES_128, new key version=4')
        self._send(cmd.ChangeKey(4, SlabDesFireDemoEV2.nk128_4, SlabDesFireDemoEV2.key128_default, 4))

        self.log_op(
            'Create file 3 as value file, mac communication mode, support limited credit, value=0x1000, range between 0~0x10000')
        self._send(cmd.CreateValueFile(0x03, 0x01, 0x1234, 0, 0x10000, 0x1000, True))

        self.log_op('Create file 6 as transaction MAC file, plain communication mode, open')
        x = cmd.CreateTransactionMacFile(0x06, 0x00, 0xEF30, 0x02, SlabDesFireDemoEV2.key_mac, 0x88)
        print(x.toCmdStr())
        self._send(x)

        self.log_op('List all file IDs')
        self._send(cmd.GetFileIDs())

        self.log_op('Get all file ISO IDs')
        self._send(cmd.GetISOFileIDs())

        self.log_op('Get all file settings')
        for x in (3, 6):
            self._send(cmd.GetFileSettings(x))

        self.log_op('Authenticate key 1 for file operation')
        self._send(cmd.AuthenticateEV2NonFirst(3, SlabDesFireDemoEV2.nk128_3))
        ###############################################################################
        # File 3
        self.log_op('Commit reader')
        self._send(cmd.commitReaderID(SlabDesFireDemoEV2.reader_id))
        self.log_op('Get value of file 3, value=0x1000')
        self._send(cmd.GetValue(3, 'mac'))
        self.log_op('Credit value +0x123')
        self._send(cmd.Credit(3, 0x123, 'mac'))
        self.log_op('Commit transaction')
        self._send(cmd.CommitTransaction(True))
        self.log_op('Get value of file 3, value=0x1123')
        self._send(cmd.GetValue(3, 'mac'))
        self.log_op('Commit reader')
        self._send(cmd.commitReaderID(SlabDesFireDemoEV2.reader_id))
        self.log_op('Debit value -0x23')
        self._send(cmd.Debit(3, 0x23, 'mac'))
        self.log_op('Commit transaction')
        self._send(cmd.CommitTransaction(True))
        self.log_op('Get value of file 3, value=0x1100')
        self._send(cmd.GetValue(3, 'mac'))
        self.log_op('Commit reader')
        self._send(cmd.commitReaderID(SlabDesFireDemoEV2.reader_id))
        self.log_op('Limited Credit value +0x08')
        self._send(cmd.LimitedCredit(3, 0x08, 'mac'))
        self.log_op('Commit transaction')
        self._send(cmd.CommitTransaction(True))
        self.log_op('Get value of file 3, value=0x1108')
        self._send(cmd.GetValue(3, 'mac'))
        ###############################################################################
        # File 6
        self.log_op('Read file 6')
        self._send(cmd.ReadData(6, 0, 0, 'plain'))
        ###############################################################################
        self.log_op('Authenticate application 1 master key in EV2 AES_128')
        self._send(cmd.AuthenticateEV2First(0, SlabDesFireDemoEV2.key128_default, None))
        self.log_op('Delete all files')
        self.log_op('Delete')
        for x in (3, 6):
            self._send(cmd.DeleteFile(x))

    def Ntest_06(self):
        self.log_casename("PICC configuration")
        logging.info('''
        * This demo is to change PICC configuration to:
          1. enable virtual card
          2. enable proximity check
          3. change PICC master key
        ''')

        self._clearCard()

        self.log_op('Change PICC virtual card configuration key')
        self._send(cmd.ChangeKey(0x20, SlabDesFireDemoEV2.key128_default, SlabDesFireDemoEV2.key128_default, 1))

        self.log_op(
            'Authenticate PICC virtual card configuration key using EV2 AES_128')
        self._send(cmd.AuthenticateEV2First(0x20, SlabDesFireDemoEV2.key128_default, None))

        self.log_op('Change PICC proximity check key')
        self._send(cmd.ChangeKey(0x21, SlabDesFireDemoEV2.key128_default, SlabDesFireDemoEV2.key128_default, 1))

        self.log_op('Change PICC virtual card MAC key')
        self._send(cmd.ChangeKey(0x22, SlabDesFireDemoEV2.key128_default, SlabDesFireDemoEV2.key128_default, 1))

        self.log_op('Change PICC virutal card encryption key')
        self._send(cmd.ChangeKey(0x23, SlabDesFireDemoEV2.key128_default, SlabDesFireDemoEV2.key128_default, 1))

        self.log_op('Authenticate PICC master key')
        self._send(cmd.AuthenticateISO(0, SlabDesFireDemoEV2.key64_default))

        self.log_op('Change PICC configuration to enable virtual card and proximity check mandatory')
        self._send(cmd.SetConfiguration(0, '0C'))

        self.log_op('Change PICC default application key')
        self._send(cmd.SetConfiguration(1, '0000000000000000 0000000000000000 0000000000000000 00'))

    def Ntest_07(self):
        self.log_casename("Delegated Application")
        logging.info('''
        * This demo is to demo how to setup and create delegated application
          1. enable and change PICC delegated keys
          2. create a delegated application
          3. check delegated application parameter
          4. delete delegated application
        ''')

        self._clearCard()

        self.log_op('Change PICC delegated application authenticate key and enable it')
        self._send(cmd.ChangeKey(0x10, SlabDesFireDemoEV2.key128_default, SlabDesFireDemoEV2.key128_default, None))

        self.log_op('Change PICC delegated application mac key and enable it')
        self._send(cmd.ChangeKey(0x11, SlabDesFireDemoEV2.key128_default, SlabDesFireDemoEV2.key128_default, None))

        self.log_op('Change PICC delegated application enc key and enable it')
        self._send(cmd.ChangeKey(0x12, SlabDesFireDemoEV2.key128_default, SlabDesFireDemoEV2.key128_default, None))

        self.log_op('Authenticate delegated application authenticate key')
        self._send(cmd.AuthenticateISO(0x10, SlabDesFireDemoEV2.key64_default))

        self.log_op('Create delegated application, 1K memory, 2 slot')
        self._send(cmd.CreateDelegatedApplication(desfireAid=2, damSlotNo=2, damSlotVer=1, quotaLimit=32,
                                                  keyEncrypted='57C6D5D2AD5575328ACFDF56FD11037A6E804A926B5471B15518F498CB4D17A2',
                                                  damMac='3A2C64E6DACC5694',
                                                  keyConf1=0x0B, keyConf2=0x8E))

        self.log_op('Authenticate PICC master key')
        self._send(cmd.AuthenticateISO(0x0, SlabDesFireDemoEV2.key64_default))

        self.log_op('List all applications\' Desfire AID')._send(cmd.GetAppIDs())

        self.log_op('Get delegated application information')
        self._send(cmd.GetDelegatedInfo(2))

        self.log_op('Select application 2')
        self._send(cmd.SelectApp(2))

        self.log_op('Authenticate application 2 key 0')
        self._send(cmd.AuthenticateAES(0, SlabDesFireDemoEV2.nk128))

        self.log_op(
            'Create file 1 as standard file, full communication mode, 512 bytes size')
        self._send(cmd.CreateStdDataFile(0x01, 0x03, 0x0000, 512, None))

        self.log_op('List all file IDs')
        self._send(cmd.GetFileIDs())

        self.log_op('Read file 1, write and read again')
        self._send(cmd.ReadData(1, 0, 512, 'full'))
        self._send(cmd.WriteDataISO(1, 0, 512, 'full', '11' * 512))
        self._send(cmd.ReadData(1, 0, 512, 'full'))


if __name__ == "__main__":
    unittest.main()
