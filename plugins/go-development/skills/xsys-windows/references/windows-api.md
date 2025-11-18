# Windows API Reference for golang.org/x/sys/windows

## Core Windows Types and Handles

### Handle Types
```go
type Handle uintptr

// Common handle constants
const (
    INVALID_HANDLE_VALUE = Handle(^uintptr(0))
    NULL                 = Handle(0)
)

// Handle management functions
func CloseHandle(handle Handle) (err error)
func DuplicateHandle(hSourceProcessHandle Handle, hSourceHandle Handle,
    hTargetProcessHandle Handle, lpTargetHandle *Handle,
    dwDesiredAccess uint32, bInheritHandle bool, dwOptions uint32) (err error)
```

### Error Types
```go
type Errno uint32

// Windows error checking
func GetLastError() (err Errno)
func SetLastError(err Errno)

// Common Windows error codes
const (
    ERROR_FILE_NOT_FOUND     Errno = 2
    ERROR_ACCESS_DENIED      Errno = 5
    ERROR_INVALID_HANDLE     Errno = 6
    ERROR_NOT_ENOUGH_MEMORY  Errno = 8
    ERROR_BAD_FORMAT         Errno = 11
    ERROR_INVALID_DATA       Errno = 13
    ERROR_BROKEN_PIPE        Errno = 109
    ERROR_MORE_DATA          Errno = 234
    ERROR_NO_MORE_ITEMS      Errno = 259
    ERROR_OPERATION_ABORTED  Errno = 995
)
```

## File Operations

### File Creation and Management
```go
func CreateFile(name *uint16, access uint32, share uint32, sa *SecurityAttributes,
    createmode uint32, attrs uint32, templatefile Handle) (handle Handle, err error)

func ReadFile(handle Handle, buf []byte, done *uint32, overlapped *Overlapped) error
func WriteFile(handle Handle, buf []byte, done *uint32, overlapped *Overlapped) error

// File access constants
const (
    GENERIC_READ    uint32 = 0x80000000
    GENERIC_WRITE   uint32 = 0x40000000
    GENERIC_EXECUTE uint32 = 0x20000000
    GENERIC_ALL     uint32 = 0x10000000

    DELETE                   uint32 = 0x00010000
    READ_CONTROL             uint32 = 0x00020000
    WRITE_DAC                uint32 = 0x00040000
    WRITE_OWNER              uint32 = 0x00080000
    SYNCHRONIZE              uint32 = 0x00100000

    FILE_SHARE_READ   uint32 = 0x00000001
    FILE_SHARE_WRITE  uint32 = 0x00000002
    FILE_SHARE_DELETE uint32 = 0x00000004
)

// File creation and access modes
const (
    CREATE_NEW          uint32 = 1
    CREATE_ALWAYS       uint32 = 2
    OPEN_EXISTING       uint32 = 3
    OPEN_ALWAYS         uint32 = 4
    TRUNCATE_EXISTING   uint32 = 5

    FILE_ATTRIBUTE_READONLY         uint32 = 0x00000001
    FILE_ATTRIBUTE_HIDDEN           uint32 = 0x00000002
    FILE_ATTRIBUTE_SYSTEM           uint32 = 0x00000004
    FILE_ATTRIBUTE_DIRECTORY        uint32 = 0x00000010
    FILE_ATTRIBUTE_ARCHIVE          uint32 = 0x00000020
    FILE_ATTRIBUTE_NORMAL           uint32 = 0x00000080
    FILE_ATTRIBUTE_TEMPORARY        uint32 = 0x00000100
    FILE_ATTRIBUTE_COMPRESSED       uint32 = 0x00000800
    FILE_ATTRIBUTE_OFFLINE          uint32 = 0x00001000
)
```

### File Information
```go
func GetFileAttributes(name *uint16) (attrs uint32, err error)
func SetFileAttributes(name *uint16, attrs uint32) (err error)

func GetFileSize(handle Handle, filesizeHigh *uint32) (filesizeLow uint32, err error)
func SetFilePointer(handle Handle, distanceToMove int32, distanceToMoveHigh *int32, moveMethod uint32) (newFilePointerLow uint32, err error)

const (
    FILE_BEGIN   uint32 = 0
    FILE_CURRENT uint32 = 1
    FILE_END     uint32 = 2
)
```

## Registry Operations

### Registry Access
```go
func RegOpenKeyEx(key Handle, subkey *uint16, options uint32, desiredAccess uint32, result *Handle) (regerrno error)
func RegCreateKeyEx(key Handle, subkey *uint16, reserved uint32, class *uint16,
    options uint32, desiredAccess uint32, sa *SecurityAttributes,
    result *Handle, disposition *uint32) (regerrno error)

func RegQueryValueEx(key Handle, valueName *uint16, reserved *uint32,
    valtype *uint32, buf *byte, buflen *uint32) (regerrno error)
func RegSetValueEx(key Handle, valueName *uint16, reserved uint32, vtype uint32,
    buf *byte, buflen uint32) (regerrno error)

func RegCloseKey(key Handle) (regerrno error)
func RegDeleteKey(key Handle, subkey *uint16) (regerrno error)
func RegDeleteValue(key Handle, valueName *uint16) (regerrno error)

// Registry constants
const (
    HKEY_CLASSES_ROOT     Handle = 0x80000000
    HKEY_CURRENT_USER     Handle = 0x80000001
    HKEY_LOCAL_MACHINE    Handle = 0x80000002
    HKEY_USERS            Handle = 0x80000003
    HKEY_PERFORMANCE_DATA Handle = 0x80000004
    HKEY_CURRENT_CONFIG   Handle = 0x80000005

    KEY_QUERY_VALUE        uint32 = 0x0001
    KEY_SET_VALUE          uint32 = 0x0002
    KEY_CREATE_SUB_KEY     uint32 = 0x0004
    KEY_ENUMERATE_SUB_KEYS uint32 = 0x0008
    KEY_NOTIFY             uint32 = 0x0010
    KEY_CREATE_LINK        uint32 = 0x0020
    KEY_READ               uint32 = 0x20019
    KEY_WRITE              uint32 = 0x20006
    KEY_EXECUTE            uint32 = 0x20019
    KEY_ALL_ACCESS         uint32 = 0xf003f
)

// Registry value types
const (
    REG_NONE                    uint32 = 0
    REG_SZ                      uint32 = 1
    REG_EXPAND_SZ               uint32 = 2
    REG_BINARY                  uint32 = 3
    REG_DWORD                   uint32 = 4
    REG_DWORD_LITTLE_ENDIAN     uint32 = 4
    REG_DWORD_BIG_ENDIAN        uint32 = 5
    REG_LINK                    uint32 = 6
    REG_MULTI_SZ                uint32 = 7
    REG_RESOURCE_LIST           uint32 = 8
    REG_FULL_RESOURCE_DESCRIPTOR uint32 = 9
    REG_RESOURCE_REQUIREMENTS_LIST uint32 = 10
    REG_QWORD                   uint32 = 11
    REG_QWORD_LITTLE_ENDIAN     uint32 = 11
)
```

## Process and Thread Management

### Process Creation
```go
type ProcessInformation struct {
    Process   Handle
    Thread    Handle
    ProcessId uint32
    ThreadId  uint32
}

type StartupInfo struct {
    Cb            uint32
    Reserved      *uint16
    Desktop       *uint16
    Title         *uint16
    X, Y, XSize, YSize uint32
    XCountChars, YCountChars uint32
    FillAttribute uint32
    Flags         uint32
    ShowWindow    uint16
    CbReserved2   uint16
    LpReserved2   *byte
    StdInput, StdOutput, StdError Handle
}

func CreateProcess(appName *uint16, commandLine *uint16,
    procSecurity *SecurityAttributes, threadSecurity *SecurityAttributes,
    inheritHandles bool, creationFlags uint32, env *uint16, currentDir *uint16,
    startupInfo *StartupInfo, outProcInfo *ProcessInformation) (err error)

func OpenProcess(desiredAccess uint32, inheritHandle bool, processId uint32) (Handle, error)
func TerminateProcess(handle Handle, exitCode uint32) (err error)
func GetExitCodeProcess(handle Handle, exitCode *uint32) (err error)

// Process constants
const (
    PROCESS_TERMINATE                 uint32 = 0x0001
    PROCESS_CREATE_THREAD             uint32 = 0x0002
    PROCESS_SET_SESSIONID             uint32 = 0x0004
    PROCESS_VM_OPERATION              uint32 = 0x0008
    PROCESS_VM_READ                   uint32 = 0x0010
    PROCESS_VM_WRITE                  uint32 = 0x0020
    PROCESS_DUP_HANDLE                uint32 = 0x0040
    PROCESS_CREATE_PROCESS            uint32 = 0x0080
    PROCESS_SET_QUOTA                 uint32 = 0x0100
    PROCESS_SET_INFORMATION           uint32 = 0x0200
    PROCESS_QUERY_INFORMATION         uint32 = 0x0400
    PROCESS_SUSPEND_RESUME            uint32 = 0x0800
    PROCESS_QUERY_LIMITED_INFORMATION uint32 = 0x1000
    PROCESS_ALL_ACCESS                uint32 = 0x1F0FFF

    CREATE_SUSPENDED              uint32 = 0x00000004
    DETACHED_PROCESS              uint32 = 0x00000008
    CREATE_NEW_CONSOLE            uint32 = 0x00000010
    NORMAL_PRIORITY_CLASS         uint32 = 0x00000020
    IDLE_PRIORITY_CLASS           uint32 = 0x00000040
    HIGH_PRIORITY_CLASS           uint32 = 0x00000080
    REALTIME_PRIORITY_CLASS       uint32 = 0x00000100
    CREATE_NEW_PROCESS_GROUP      uint32 = 0x00000200
    CREATE_UNICODE_ENVIRONMENT    uint32 = 0x00000400
    CREATE_SEPARATE_WOW_VDM       uint32 = 0x00000800
    CREATE_SHARED_WOW_VDM         uint32 = 0x00001000
    CREATE_FORCEDOS               uint32 = 0x00002000
    BELOW_NORMAL_PRIORITY_CLASS   uint32 = 0x00004000
    ABOVE_NORMAL_PRIORITY_CLASS   uint32 = 0x00008000
    CREATE_BREAKAWAY_FROM_JOB     uint32 = 0x01000000
    CREATE_PRESERVE_CODE_AUTHZ_LEVEL uint32 = 0x02000000
    CREATE_NO_WINDOW              uint32 = 0x08000000
    CREATE_PROTECTED_PROCESS      uint32 = 0x00040000
    CREATE_EXTENDED_STARTUPINFO_PRESENT uint32 = 0x00080000
    CREATE_PROTECTED_PROCESS      uint32 = 0x00040000
)
```

## Memory Management

### Virtual Memory Operations
```go
func VirtualAlloc(address uintptr, size uintptr, alloctype uint32, protect uint32) (uintptr, error)
func VirtualFree(address uintptr, size uintptr, freetype uint32) error
func VirtualProtect(address uintptr, size uintptr, newprotect uint32, oldprotect *uint32) error

// Memory allocation constants
const (
    MEM_COMMIT      uint32 = 0x1000
    MEM_RESERVE     uint32 = 0x2000
    MEM_DECOMMIT    uint32 = 0x4000
    MEM_RELEASE     uint32 = 0x8000
    MEM_RESET       uint32 = 0x80000
    MEM_TOP_DOWN    uint32 = 0x100000
    MEM_WRITE_WATCH uint32 = 0x200000
    MEM_PHYSICAL    uint32 = 0x400000
    MEM_LARGE_PAGES uint32 = 0x20000000

    PAGE_EXECUTE           uint32 = 0x10
    PAGE_EXECUTE_READ      uint32 = 0x20
    PAGE_EXECUTE_READWRITE uint32 = 0x40
    PAGE_EXECUTE_WRITECOPY uint32 = 0x80
    PAGE_NOACCESS          uint32 = 0x01
    PAGE_READONLY          uint32 = 0x02
    PAGE_READWRITE         uint32 = 0x04
    PAGE_WRITECOPY         uint32 = 0x08
    PAGE_GUARD             uint32 = 0x100
    PAGE_NOCACHE           uint32 = 0x200
    PAGE_WRITECOMBINE      uint32 = 0x400
)
```

## Cryptography and Certificates

### Certificate Operations
```go
type CertContext struct {
    EncodingType uint32
    EncodedCert  *byte
    Length       uint32
    CertInfo     *CertInfo
    Store        Handle
    hCryptProv   Handle
    hKey         Handle
}

func CertOpenStore(storeProvider uintptr, encodingType uint32, cryptProv Handle,
    flags uint32, para uintptr) (handle Handle, err error)
func CertCloseStore(store Handle, flags uint32) error

func CertCreateCertificateContext(encodingType uint32, certEncoded *byte,
    encodedLen uint32) (*CertContext, error)

func CertEnumCertificatesInStore(store Handle, prevCertContext *CertContext) (*CertContext, error)

// Certificate constants
const (
    CERT_STORE_PROV_SYSTEM uintptr = 10
    CERT_SYSTEM_STORE_CURRENT_USER uint32 = 1
    CERT_SYSTEM_STORE_LOCAL_MACHINE uint32 = 2
    CERT_STORE_READONLY_FLAG uint32 = 0x00008000
)
```

### Data Protection
```go
type DataBlob struct {
    Size uint32
    Data *byte
}

func CryptProtectData(dataIn *DataBlob, dataDesc *uint16,
    optionalEntropy *DataBlob, reserved *byte,
    promptStruct *void, flags uint32, dataOut *DataBlob) error

func CryptUnprotectData(dataIn *DataBlob, dataDesc *uint16,
    optionalEntropy *DataBlob, reserved *byte,
    promptStruct *void, flags uint32, dataOut *DataBlob) error

// Protection constants
const (
    CRYPTPROTECT_UI_FORBIDDEN uint32 = 0x1
    CRYPTPROTECT_LOCAL_MACHINE uint32 = 0x4
    CRYPTPROTECT_AUDIT        uint32 = 0x10
)
```

## System Information

### System Information Functions
```go
func GetSystemTime(systemTime *Systemtime) error
func GetLocalTime(systemTime *Systemtime) error

type Systemtime struct {
    Year         uint16
    Month        uint16
    DayOfWeek    uint16
    Day          uint16
    Hour         uint16
    Minute       uint16
    Second       uint16
    Milliseconds uint16
}

func GetComputerName(name *uint16, size *uint32) (err error)
func GetSystemDirectory(dir *uint16, size uint32) (len uint32, err error)
func GetWindowsDirectory(dir *uint16, size uint32) (len uint32, err error)
```

### Version Information
```go
func GetVersionEx(versionInfo *Osversioninfoex) error

type Osversioninfoex struct {
    OsversioninfoexSize uint32
    MajorVersion         uint32
    MinorVersion         uint32
    BuildNumber          uint32
    PlatformId           uint32
    CsdVersion           [128]uint16
    ServicePackMajor     uint16
    ServicePackMinor     uint16
    SuiteMask            uint16
    ProductType          uint8
    Reserved             uint8
}
```

## Network Operations

### Windows Sockets (Winsock)
```go
func WSAStartup(ver uint32, data *WSAData) (sockerr error)
func WSACleanup() (sockerr error)

func Socket(af int32, typ int32, protocol int32) (handle Handle, err error)
func WSASocket(af int32, typ int32, protocol int32, protocolInfo *WSAProtocolInfo,
    group uint32, flags uint32) (handle Handle, err error)

func Bind(s Handle, name *RawSockaddrAny, namelen int32) (err error)
func Connect(s Handle, name *RawSockaddrAny, namelen int32) (err error)
func Listen(s Handle, backlog int32) (err error)
func Accept(s Handle, rsa *RawSockaddrAny, addrlen *int32) (newsock Handle, err error)

// Socket constants
const (
    AF_UNSPEC     int32 = 0
    AF_UNIX       int32 = 1
    AF_INET       int32 = 2
    AF_INET6      int32 = 23
    AF_NETBIOS    int32 = 17
    AF_MAX        int32 = 24

    SOCK_STREAM    int32 = 1
    SOCK_DGRAM     int32 = 2
    SOCK_RAW       int32 = 3
    SOCK_SEQPACKET int32 = 5

    IPPROTO_TCP int32 = 6
    IPPROTO_UDP int32 = 17

    WSA_FLAG_OVERLAPPED uint32 = 0x01
)
```

## String Utilities

### UTF-16 String Conversion
```go
func UTF16PtrFromString(s string) (*uint16, error)
func UTF16ToString(s []uint16) string
func UTF16ToStrings(s [][]uint16) []string

func StringToUTF16(s string) []uint16
func StringToUTF16Ptr(s string) *uint16
func StringToUTF16Slice(s []string) ([][]uint16, error)
```

## Security and Access Control

### Security Descriptor
```go
type SecurityDescriptor struct {
    revision byte
    sbz1     byte
    control  uint16
    owner    *SID
    group    *SID
    sacl     *ACL
    dacl     *ACL
}

func NewSecurityDescriptor() (*SecurityDescriptor, error)
func (sd *SecurityDescriptor) SetControl(controlBitsRequired, controlBitsSet uint32) error

type SecurityAttributes struct {
    Length             uint32
    SecurityDescriptor *SecurityDescriptor
    InheritHandle      bool
}
```

### Access Control Lists
```go
type ACL struct {
    aRevision byte
    sbz1      byte
    aclSize   uint16
    aceCount  uint16
    sbz2      uint16
}

type SID struct {
    revision byte
    subAuthorityCount byte
    identifierAuthority [6]byte
    subAuthority []uint32
}
```

## Event Log Operations

### Event Log Functions
```go
func RegisterEventSource(uncServerName *uint16, sourceName *uint16) (Handle, error)
func DeregisterEventSource(handle Handle) error

func ReportEvent(handle Handle, eventType uint16, category uint16,
    eventID uint32, userSID *uintptr, numStrings uint16, dataSize uint32,
    strings **uint16, rawData *byte) error

// Event log constants
const (
    EVENTLOG_SUCCESS          uint16 = 0x0000
    EVENTLOG_ERROR_TYPE       uint16 = 0x0001
    EVENTLOG_WARNING_TYPE     uint16 = 0x0002
    EVENTLOG_INFORMATION_TYPE uint16 = 0x0004
    EVENTLOG_AUDIT_SUCCESS    uint16 = 0x0008
    EVENTLOG_AUDIT_FAILURE    uint16 = 0x0010
)
```

## DLL Loading

### Dynamic Library Operations
```go
type LazyDLL struct {
    mu  sync.Mutex
    dll *DLL
    name string

    sys *LazyProc
}

type LazyProc struct {
    mu  sync.Mutex
    name string
    addr *uintptr
    l   *LazyDLL
}

func NewLazyDLL(name string) *LazyDLL
func (d *LazyDLL) Load() error
func (d *LazyDLL) NewProc(name string) *LazyProc
func (d *LazyDLL) FindProc(name string) (uintptr, error)
func (d *LazyDLL) MustFindProc(name string) uintptr

func LoadLibrary(libname string) (Handle, error)
func GetProcAddress(module Handle, procname string) (uintptr, error)
func FreeLibrary(module Handle) error
```