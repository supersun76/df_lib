DF_LIB User Manual
===
Author: Justin Shen  
Version: 1.0.0a  
Date: Aug. 20, 2021
***

## **Introduction**
The purpose of df_lib is to provide a simple way to operate DesFire smart card without 
knowledge of complex security algorithm. The user can focus on DesFire's application.  

This manual is to help user to use df_lib library. If you have any question or issue, 
please email to zqshen.pub@gmail.com.

Please notice that DesFire is the trademark of NXP.

## **OS Supporting**
df_lib supports:
- Microsoft Windows OS. The minimal version is Microsoft Windows XP.
- Linux type OS, such as Redhat, Ubuntu, CentOS and so on.
Please read Prerequirement section for detail.

## **Prerequirement**
To use df_lib, user need to prepare based on operating system used. Here is the checklist.
### **Hardware**
A PC/SC type USB smart card reader with contactless smart card feature is required to operate
DesFire smart card.  
### **Windows OS**
When using windows os, user need to check if it has smart card service that supports PC/SC type
USB smart card reader.  
To check it, use the commands below under command line interface of Windows with administrator
privilege.  

To check smart card service status: `sc query SCardSvr`  

To start smart card service: `sc start SCardSvr`

## **Linux OS**
df_lib uses pcsclite library as interface to operate smart card. The Linux OS needs to install
pcsclite before use df_lib.  
When using Ubuntu 20.04LTS, which is the test platform of df_lib, several package needed to
be installed:
- libpcsclite1
- pcscd  

To install package, use command: `sudo apt install libpcsclite1 pcscd`    
To start PC/SC daemon, use command: `sudo systemctl start pcscd`  
To enable PC/SC daemon start after boot, use command: `sudo systemctl enable pcscd`  

## **Function**
The df_lib provides fully function supporting up to DesFire EV2, including:
- all authentication methods and algorithm
- application/delegated application operation such as create, delete and change
- all file operations including all type files creation, delete, change, data writing and data reading.
- all key operations including key changing, key set operation and key setting operation.
- Virtual card supporting
- Proximity chech supporting
- Transparent ISO type APDU exchange supporting

For most DesFire commands and ISO APDU with class=0, command can be send direct via df_lib.

The df_lib DO NOT supports:
- Transaction MAC verification. The user can get MAC related data via reading MAC file, as well as the transaction MAC related commands. Because card issuer or operation has the responsibility and knowledge to process transaction MAC verification, this function is not included in df_lib.
- external SAM module. df_lib can not co-operate with external SAM module. All security algorithm related operation is included in library, the user can only issue plain commands without any security processing, such as MAC and encryption.

## **API interface**
### **API**
For easy to use, df_lib provides 3 simple API interfaces for use.  
- Create a context instance. The function prototype is:  
`void* desfire_api_create(void)`  
The API has no parameter. If successful, the function will return a void type pointer of
context instance. A NULL pointer will be returned if create context failed.

- Release a context instance. The function prototype is:  
`void desfire_api_free(void* pInst)`  
The API is to release context resource. The parameter is the pointer created by `desfire_api_create`
function. It has no return value.  

- Send DesFire command to smart card and get return data. The function prototype is:  
`const char* DFLIB_CALL desfire_api_send_str(void* pInst, const char* command)`  
The function has 2 parameters:
    - pInst: context instance pointer created by `desfire_api_create` function.
    - command: A hexdigital string of df_lib DesFire command. Use need to create and maintenance
    the buffer of command.  
The function return a string as operation result. The format of return is as:  
`[status_code], [return_data]`  
The status_code is a signed integer. If status_code is negative, it is the error code. If not,
it is the DesFire response status word value.  
When status_code is positive value or 0, the return_data is the hexdigital string of smart card
return data except status word. Please notice that some commands will have no return data. In
such status, the return_data is an empty string.
When status_code is negative, the return_data is an error message to indicate the error reason.

### **Error Code**
The error code of df_lib is a negative integer. The value is between -30100 to -30000.  

### **Multi-Thread Support
Multi thread is supported by df_lib. When context instance shared between multi threads, df_lib used system
mutex mechanism to protect operation sequence. That means only 1 thread can execute commands. The timeout
of thread waiting is 2 seconds.  
 
### **Files**
df_lib includes:
- df_lib_x86.dll: Dynamic link library file for Windows x86 (32-bit) platform
- dl_lib_x64.dll: Dynamic link library file for Windows x64 (64-bit) platform
- libdl_lib_x64.so: Dynamic library file for Linux x64 (64-bit) platform

df_lib provides a python based demo file package to help user understand, test and use df_lib.
The package includes:  
- SlabDesFireCmd.py: encaptured df_lib DesFire command
- SlabDesFireEnv.py: df_lib DesFire library class
- SlabDesFireDemoD40.py: A DesFire D40 operation demo program
- SlabDesFireDemoEV1.py: A DesFire EV1 operation demo program
- SlabDesFireDemoEV2.py: A DesFire EV2 operation demo program
All python program needs Python 3.0 and up.


## **Definition**
### **Commands**
df_lib supports DesFire commands, ISO APDU and df_lib escape commands.
#### **DesFire Command**
DesFire command is defined in NXP DesFire related product documents. It has a command code
 with variable length data.
#### **ISO APDU Command**
ISO APDU command is defined as ISO-7816 standard.
Please notice df_lib only support all ISO APDU commands with class=0x00.
#### **df_lib Escape Command**
All commands with command code (1st byte of commands) = 0xFF, it is df_lib's escape command. 
Escape command is used by df_lib to process security-related operation such as authentication 
and key changing.
#### **Communication Mode**
As DesFire smart card supports 3 type communication mode, df_lib supports all of them named as plain, mac and full.
The byte codes used to represent each communication mode are:
- plain: 0
- mac: 1
- full: 2  

Communication mode byte is named as COMM_MODE in command definition below.

## **Smart Card reader support**
df_lib supports all kinds of smart card reader following PC/SC protocol, or USB CCID type. The dl_lib
 will search all CCID reader attached with system and use the 1st found smard card when first execute
 command.  
df_lib also supports external smart card command exchange mechanism in advance version. 
Please contact auther if needed.

## **DesFire commands**
df_lib supports DesFire commands as below. User can refer to python classes providing with df_lib to find more detail of each commands byte format.
### **Transparent commands**
All DesFire commands below is transparent.
- FreeMem
- Format
- SetConfiguration
- GetVersion
- GetCardUID
- InitializeKeySet
- FinializeKeySet
- RollKeySet
- GetKeySettings
- ChangeKeySettings
- GetKeyVersion
- CreateApp
- DeleteApp
- SelectApp
- GetAppIDs
- GetDFNames
- GetDelegatedInfo
- CreateStdDataFile
- CreateBackupDataFile
- CreateValueFile
- CreateLinearRecordFile
- CreateCyclicRecordFile
- DeleteFile
- GetFileIDs
- GetISOFileIDs
- GEtFileSettings
- ChangeFileSettings
- CreateRecordFile
- CommitTransaction
- AbortTransaction
- CommitReaderID
- PreparePC
- ProximityCheck
- VerifyPC
- ReadSig
  
#### **CreateDelegatedApplication**
The CreateDelegatedApplication command in df_lib uses extended format as the encrypted key and MAC append at the end of command byte stream.  
The format is:  

`[CREATE_DELEGATED_APPLICATION_COMMAND] [ENCRYPTED_KEY] [MAC]`  

The ENCRYPTED_KEY and MAC are provided by card issuer.

#### **ReadData and ReadDataISO**
The ReadData and ReadDataISO command in df_lib is in format as:  

`[BD/AD] [FILE_NO/1Byte] [OFFSET/3Byte] [LENGTH/3Byte] [COMM_MODE/1Byte]`  

#### **WriteData and WriteDataISO**
The WriteData and WriteDataISO command in df_lib is in format as:  

`[3D/8D] [FILE_NO/1Byte] [OFFSET/3Byte] [LENGTH/3Byte] [COMM_MODE/1Byte] [DATA_STREAM]`  

#### **GetValue**
The GetValue command in df_lib is in format as:  

`6C [COMM_MODE/1Byte]`  
  
#### **Credit/LimitedCredit/Debit**
The Credit/LimitedCredit/Debit commands in df_lib is in format as:  

`[0C/1C/DC] [FILE_NO/1Byte] [COMM_MODE/1Byte] [VALUE/4Byte]`  

#### **ReadRecord and ReadRecordISO**
The ReadRecord and ReadRecordISO commands in df_lib is in format as:  

`[BB/AB] [FILE_NO/1Byte] [REC_NO/3Byte] [REC_QTY/3Byte] [COMM_MODE/1Byte]`  

#### **WriteRecord and WriteRecordISO**
The WriteRecord and WriteRecordISO commands in df_lib is in format as:  

`[3B/8B] [FILE_NO/1Byte] [OFFSET/3Byte] [LENGTH/3Byte] [COMM_MODE/1Byte] [DATA_STREAM]`  

#### **UpdateRecord and UpdateRecordISO**
The UpdateRecord and UpdateRecordISO command in df_lib is in fomrat as:  

`[DB/BA] [FILE_NO/1Byte] [REC_NO/3Byte] [OFFSET/3Byte] [LENGTH[3Byte] [COMM_MODE/1Byte] [DATA_STREAM]`  

### **df_lib Escape Commands**
#### **Authenticate**
The Authenticate command in df_lib is in format as:  

`FF 0A [KEY_ID/1Byte] [KEY_LENGTH/1Byte] [KEY_BYTE_STREAM]`  
#### **AuthenticateISO**
The AuthenticateISO command in df_lib is in format as:  

`FF 1A [KEY_ID/1Byte] [KEY_LENGTH/1Byte] [KEY_BYTE_STREAM]`  
#### **AuthenticateAES**
The AuthenticateAES command in df_lib is in format as:  

`FF AA [KEY_ID/1Byte] [KEY_LENGTH/1Byte] [KEY_BYTE_STREAM]`  
#### **AuthenticateEV2First**
The AuthenticateEV2First command in df_lib is in format as:  

`FF 71 [KEY_ID/1Byte] [KEY_LENGTH/1Byte] [KEY_BYTE_STREAM] [PCDCAP2_LENGTH/1Byte] [PCDCAP2_BYTE_STREAM]`  

The PCDCAP2_LENGTH can be 0. If PCDCAP2_LENGTH is 0, PCDCAP2_BYTE_STREAM can not be provided. If provided, it will be ignored.

#### AuthenticateEV2NonFirst
The AuthenticateEV2NonFirst command in df_lib is in format as:  

`FF 77 [KEY_ID/1Byte] [KEY_LENGTH/1Byte] [KEY_BYTE_STREAM]`  

#### **ChangeKey**
The ChangeKey command in df_lib is in format as:  

`FF C4 [KEY_ID/1Byte] [NEW_KEY_LENGTH/1Byte] [NEW_KEY_BYTE_STREAM] [OLD_KEY_LENGTH/1Byte] [OLD_KEY_BYTE_STREAM] [KEY_AES_VERSION/1Byte]`  

OLD_KEY_LENGTH should be 0 if no old key data is needed, and OLD_KEY_BYTE_STREAM should be absent.  
If the target key is AES type, KEY_AES_VERSION must be provided. Otherwise, KEY_AES_VERSION should be absent.

#### **ChangeKeyEV2**
The ChangeKeyEV2 command in df_lib is in format as:  

`FF C4 [KEY_SET_NO/1Byte] [KEY_ID/1Byte] [NEW_KEY_LENGTH/1Byte] [NEW_KEY_BYTE_STREAM] [OLD_KEY_LENGTH/1Byte] [OLD_KEY_BYTE_STREAM] [KEY_AES_VERSION/1Byte]`  

OLD_KEY_LENGTH should be 0 if no old key data is needed, and OLD_KEY_BYTE_STREAM should be absent.  
If the target key is AES type, KEY_AES_VERSION must be provided. Otherwise, KEY_AES_VERSION should be absent.

#### **Visual Card Selection**
The df_lib provides an combined visual card selection command to automatic process visual card selection commands with given keys.  
The command format is:  

`FF A4 [AID_LENGTH/1Byte] [AID_BYTE_STREAM] [ENC_KEY_LENGTH/1Byte] [ENC_KEY_BYTE_STREAM] [MAC_KEY_LENGTH/1Byte] [MAC_KEY_BYTE_STREAM]`  

#### **Visual Card Proximity Check**
The df_lib provides an combined visual card proximity check command to process visual card proximity check with given key.  
The command format is:  

`FF F0 [KEY_LENGTH/1Byte] [KEY_BYTE_STREAM]`  

## **Limitation**
The public version of df_lib has several limitations.  
- Only 2 context instances are supported.
- The maximum quantity of commands can be executed in 1 context instances is 60.
- The library is only provided in binary format.


## **Bug Report**
Please email to zqshen.pub@gmail.com if any bug found.

## **Notes**
Please refer to DesFire product manual for DesFire smart card operation detail. 
