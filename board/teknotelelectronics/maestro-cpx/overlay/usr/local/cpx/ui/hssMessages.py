from enum import Enum

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# 50 + 5 + 20 + 5 + 50 = 130 total min width
duration_label_width = 20
button_width = 50
min_duration_h_box_width = 5
h_box_total_min_size = duration_label_width + button_width * 2 + min_duration_h_box_width * 2


class SharedValues(Enum):
    actionType = "actionType"
    actionTypeSet = "set"
    actionTypeGet = "get"
    values = "values"


class TimeValues(Enum):
    source = "source"
    isDST = "isDST"
    second = "second"
    minute = "minute"
    hour = "hour"
    day = "day"
    month = "month"
    year = "year"


class UserSettings(Enum):
    isPowerOffSent = "isPowerOffSent"
    isConfigOpen = "isConfigOpen"


class RelayState(Enum):
    isOn = "isOn"


class StartSignalGroupSignals(Enum):
    start = "start"


class StartInputDemand(Enum):
    start = "start"


class GPRSSetting(Enum):
    modemType = "modemType"
    baudRate = "baudRate"
    baudRate9600 = 9600


class LogInfo(Enum):
    index = "index"


class StartInputDemands(Enum):
    start = "start"


class StepCount(Enum):
    phase = "phase"


class StepInfo(Enum):
    phase = "phase"
    count = "count"
    steps = "steps"


class Language(Enum):
    English = 0
    Turkish = 1


class Events(Enum):
    EVENT_NONE = 0
    EVENT_POWER_ON = 1
    EVENT_SO_SWITCH_SHORT_CIRCUIT = 2
    EVENT_SO_SWITCH_OPEN_CIRCUIT = 3
    EVENT_SO_VOLTAGE_SENSOR_FAILURE = 4
    EVENT_SO_LAMPS_DRIVEN_EXTERNALLY = 5
    EVENT_SO_WORKING_LAMP_TOTAL_CHANGE = 6
    EVENT_SIGNAL_AT_SG = 7  # if the dedected signal for an assigned signal changes
    EVENT_INVALID_SIGNAL = 8  # if an invalid signal that is not TRUE for intersection is on SO
    EVENT_INVALID_SIGNAL_SEQUENCE = 9  # if signal is not in followers
    EVENT_SG_RED_LAMP_FAILURE = 10  # when a red lamp failure exist
    EVENT_SG_LAST_RED_LAMP_FAILURE = 11  # the last red lamp failure
    EVENT_SG_NUMBER_OF_RED_LAMPS_FAILURE = 12  # bRedLampFailureNumberTH failure
    EVENT_SG_YELLOW_LAMP_FAILURE = 13
    EVENT_SG_GREEN_LAMP_FAILURE = 14
    EVENT_YELLOW_YELLOW_CONFLICT = 15  # conflicts
    EVENT_YELLOW_GREEN_CONFLICT = 16
    EVENT_GREEN_GREEN_CONFLICT = 17
    EVENT_SO_POWER_RECORD = 18  # power record
    EVENT_MODULE_MISSING = 19  # module missing
    EVENT_MODULE_RESPONDS = 20  # module responds
    EVENT_INFORMATION = 21  # random information
    EVENT_CPMP_COMM_CP_CHECKSUM_ERROR = 22  # cpmp comm checksum errors
    EVENT_CPMP_COMM_MP_CHECKSUM_ERROR = 23
    EVENT_CPMP_COMM_CP_RECEIVE_ERROR = 24  # cpmp comm receive/transmit error
    EVENT_CPMP_COMM_CP_TRANSMIT_ERROR = 25
    EVENT_CPMP_COMM_MP_RECEIVE_ERROR = 26
    EVENT_CPMP_COMM_MP_TRANSMIT_ERROR = 27
    EVENT_POWER_NORMAL_TO_STAND_BY = 28  # switching from normal mode to stand by
    EVENT_POWER_STAND_BY_TO_NORMAL = 29  # switching from stand by to normal mode
    EVENT_CHECKSUM_FLASH_ERROR = 30  # storage error
    EVENT_CPMP_COMM_CP_TIMEOUT = 31  # cpmp comm timeouts
    EVENT_CPMP_COMM_MP_TIMEOUT = 32
    EVENT_MCT_CONFIGURATION_ERROR = 33  # program loading
    EVENT_PROGRAM_LOADING_ERROR = 34
    EVENT_INVALID_PROGRAM = 35
    EVENT_VOLTAGE_VALUE_LOWER_BOUND = 36  # voltage bounds
    EVENT_VOLTAGE_VALUE_UPPER_BOUND = 37
    EVENT_WORK_MODE_CHANGE = 38  # work mode, EVENT_WORK_MODE_CHANGE

    EVENT_RESET_WINDOW_WATCHDOG = 39  # reset sources
    EVENT_RESET_INDEPENDENT_WATCHDOG = 40
    EVENT_RESET_LOW_POWER = 41

    EVENT_SSM_LOG = 42  # module logs
    EVENT_PSM_LOG = 43
    EVENT_IO_LOG = 44
    EVENT_SG_ALL_RED_LAMPS_BROKEN = 45  # lamps broken
    EVENT_SG_ALL_YELLOW_LAMPS_BROKEN = 46
    EVENT_SG_ALL_GREEN_LAMPS_BROKEN = 47
    EVENT_SET_SIGNALING_MODE_CHANGE = 48  # signaling mode
    EVENT_MAIN_STORAGE_BROKEN = 49  # main and backup storages
    EVENT_BACKUP_STORAGE_BROKEN = 50
    EVENT_BACKUP_TO_MAIN_COPY_ERROR = 51
    EVENT_BACKUP_STORAGE_GET_ERROR = 52
    EVENT_BACKUP_STORAGE_SET_ERROR = 53
    EVENT_MAIN_STORAGE_GET_ERROR = 54
    EVENT_MAIN_STORAGE_SET_ERROR = 55
    EVENT_BACKUP_TO_MAIN_COPY_SUCCESS = 56
    EVENT_MAIN_STORAGE_IN_USE = 57
    EVENT_BACKUP_STORAGE_IN_USE = 58
    EVENT_MAIN_TO_BACKUP_COPY_SUCCESS = 59
    EVENT_MAIN_TO_BACKUP_COPY_ERROR = 60
    EVENT_RESET_POWER_ON_CLEAR_CIRCUIT = 61  # reset source is power on clear circuit
    EVENT_BATTERY_LOW = 62  # battery
    EVENT_BATTERY_NORMAL = 63
    EVENT_DOOR_OPEN = 64  # door
    EVENT_DOOR_CLOSED = 65
    EVENT_MCT_CONFIGURATION_STARTS = 66  # Maestro Configuration Tool (MCT)
    EVENT_MCT_CONFIGURATION_ENDS = 67
    EVENT_DEFAULT_LCD_USER_ADD_SUCCESS = 68  # LCD user
    EVENT_DEFAULT_LCD_USER_ADD_ERROR = 69
    EVENT_VOLTAGE_VALUE_NORMAL = 70  # voltage normal value
    EVENT_FREQUENCY_VALUE_LOWER_BOUND = 71  # frequency
    EVENT_FREQUENCY_VALUE_UPPER_BOUND = 72
    EVENT_FREQUENCY_VALUE_NORMAL = 73
    EVENT_USER_REQ_WORK_MODE_TO_ALL_RED = 74  # user requests
    EVENT_USER_REQ_WORK_MODE_TO_DARK = 75
    EVENT_USER_REQ_WORK_MODE_TO_FLASH = 76
    EVENT_USER_REQ_WORK_MODE_TO_WORK_PLAN = 77
    EVENT_USER_REQ_POWER_LEARNING = 78
    EVENT_USER_REQ_SSM_TEST_STARTS = 79
    EVENT_USER_REQ_SSM_TEST_ENDS = 80
    EVENT_USER_REQ_SP_TEST_STARTS = 81
    EVENT_USER_REQ_SP_TEST_ENDS = 82
    EVENT_USER_REQ_TIME_SET = 83
    EVENT_USER_REQ_RELAY_SET_ON = 84
    EVENT_USER_REQ_RELAY_SET_OFF = 85
    EVENT_USER_REQ_LCD_LOG_IN = 86  # user account operations
    EVENT_USER_REQ_LCD_LOG_OUT = 87
    EVENT_USER_REQ_LCD_LOG_IN_USERNAME_ERR = 88
    EVENT_USER_REQ_LCD_LOG_IN_PASSWORD_ERR = 89
    EVENT_SIGNAL_DURATION_LESS_THAN_MIN = 90  # signal duration
    EVENT_SIGNAL_DURATION_GREATER_THAN_MAX = 91
    EVENT_DETECTOR_BROKEN = 92  # detector states
    EVENT_DETECTOR_SAFE = 93
    EVENT_WORK_PLAN_CHANGE = 94
    EVENT_SIGNAL_PROGRAM_PLAN_CHANGE = 95
    EVENT_SIGNAL_PROGRAM_CHANGE = 96
    EVENT_SG_ALL_RED_LAMPS_SAFE = 97  # lamps safe
    EVENT_SG_ALL_YELLOW_LAMPS_SAFE = 98
    EVENT_SG_ALL_GREEN_LAMPS_SAFE = 99

    EVENT_RESET_SOFTWARE = 100
    EVENT_RESET_PIN = 101
    EVENT_RESET_PORRST = 102

    # MCS EVENTS
    EVENT_MCTS_ACTIVE = 103
    EVENT_MCTS_CONNECTED = 104
    EVENT_MCTS_DISCONNECTED = 105
    EVENT_MCTS_CONNECTION_TIMEOUT = 106
    EVENT_MCTS_USER_REQUEST_SP_CHANGE = 107
    EVENT_MCTS_USER_REQUEST_DATE_TIME_ADJUST = 108
    EVENT_MCTS_USER_REQUEST_RESET = 109
    EVENT_MCTS_USER_REQUEST_DOWNLOAD = 110
    EVENT_MCTS_USER_REQUEST_UPLOAD = 111
    EVENT_USER_REQ_PSM_TEST_STARTS = 112
    EVENT_USER_REQ_PSM_TEST_ENDS = 113
    EVENT_GREEN_WAVE_SYNCH_STARTS = 114
    EVENT_GREEN_WAVE_SYNCH_ENDS = 115
    EVENT_MCTS_USER_REQ_WORK_MODE_TO_ALL_RED = 116
    EVENT_MCTS_USER_REQ_WORK_MODE_TO_DARK = 117
    EVENT_MCTS_USER_REQ_WORK_MODE_TO_FLASH = 118
    EVENT_MCTS_USER_REQ_WORK_MODE_TO_WORK_PLAN = 119
    EVENT_MCTS_USER_REQ_START_IAP = 120
    EVENT_MCTS_RESUMED = 121
    EVENT_USER_REQ_START_IAP = 122
    EVENT_LAST = 122


class EventParams(Enum):
    day = "day"
    month = "month"
    year = "year"
    hour = "hour"
    minute = "minute"
    second = "second"
    blog = "event"
    bparam = "param1"
    sparam = "param2"
    lparam = "param3"


class SignalingModes(Enum):
    SIGNALING_MODE_NONE = 0x00
    SIGNALING_MODE_NORMAL = 0x01
    SIGNALING_MODE_FLASH = 0x02
    SIGNALING_MODE_EMERGENCY_FLASH = 0x08
    SIGNALING_MODE_EMERGENCY_DARK = 0x0A
    SIGNALING_MODE_EMERGENCY_FLASH_NEW = 0x0B


class SignalSequence:

    def __init__(self, lights, duration):
        self.lights = []
        for light in lights:
            self.lights.append(light)
        self.duration = duration


selected_sequence = [""]
"""
signal_sequence = {"1": [SignalSequence([1, 2, 4, 3] + 28 * [0], 20),
                         SignalSequence([2, 4, 3, 1] + 28 * [0], 15),
                         SignalSequence([4, 3, 1, 2] + 28 * [0], 10)],

                   "2": [SignalSequence([4, 3, 3, 1] + 28 * [0], 12),
                         SignalSequence([3, 2, 4, 1] + 28 * [0], 17),
                         SignalSequence([1, 1, 4, 3] + 28 * [0], 2),
                         SignalSequence([1, 1, 4, 3] + 28 * [0], 2),
                         SignalSequence([1, 1, 4, 3] + 28 * [0], 2)],

                   "3": [SignalSequence([2, 3, 2, 4] + 28 * [0], 31),
                         SignalSequence([1, 1, 3, 3] + 28 * [0], 22),
                         SignalSequence([3, 4, 4, 4] + 28 * [0], 11)],

                   "1 -> 2": [SignalSequence([3, 4, 1, 2] + 28 * [0], 1),
                              SignalSequence([1, 4, 2, 4] + 28 * [0], 11)],

                   "2 -> 3": [SignalSequence([2, 3, 3, 1] + 28 * [0], 37)],

                   "3 -> 1": [SignalSequence([1, 4, 3, 4] + 28 * [0], 18)]
                   }
"""
seq_length = [0]
seq_count = {}
signal_sequence = {}

phase_language = [
    ["Fazlar:", "Faz Geçişleri:"],
    ["Phases:", "Phase Transitions:"]
]

LogContents = \
    [
        [
            "TANIMSIZ",
            "Cihaz açıldı",
            "{} No.lu sinyal cıkıs anahtarı kısa devre. Ölçülen akım {}",
            "{} No.lu sinyal çıkış anahtarı açık devre",
            "{} No.lu sinyal çıkısı gerilim sensor arızası",
            "{} No.lu sinyal çıkış anahtarı dışarıdan besleniyor",
            "{} No.lu sinyal çıkısında çalışan sinyal verici sayısı değişti. Görülen {}, olması gereken {}",
            "{} No.lu sinyal grubunda yanlış sinyal var. Olması gereken {}, görülen {}",
            "{} No.lu sinyal grubunda geçersiz sinyal var. Görülen sinyal {}",
            "{} No.lu sinyal grubunda sinyal planı sıralamasında hata var. Önceki sinyal {}, görülen {}",
            "{} No.lu sinyal grubunda kırmızı sinyal verici arızası",
            "{} No.lu sinyal grubundaki tüm kırmızı sinyal vericiler bozuk.",
            "{} No.lu sinyal grubunda kırmızı lamba arızası. Lamba sayısı önceden ayarlanan en düşük adete düşmüştür",
            "{} No.lu sinyal grubunda sarı sinyal verici arızası",
            "{} No.lu sinyal grubunda yeşil sinyal verici arızası",
            "Aynı anda sarı sinyale sahip olmaması gereken {} ve {} No.lu sinyal gruplarında aynı anda sarı sinyal görülmüştür",
            "Aynı anda biri sarı digeri yeşil sinyale sahip olmaması gereken {} ve {} No.lu sinyal gruplarından biri sarı digeri yeşil sinyale sahiptir",
            "Aynı anda yeşil sinyale sahip olmaması gereken {} ve {} No.lu sinyal gruplarında aynı anda yeşil sinyal görülmüştür",
            "{} No.lu sinyal çıkısında {}W {}V güç kaydı",
            "{}{} modülü cevap vermiyor.",
            "{}{} modülü devrede. {} süre sonra aktif hale geldi",
            "Bilgi {}, {}, {}",
            "MP'den CP'ye hatalı paket",
            "CP'den MP'ye hatalı paket",
            "CP, MP'den paket alırken hata oluştu",
            "CP, MP'ye paket gönderirken hata oluştu",
            "MP, CP'den paket alırken hata oluştu",
            "MP, MP'ye paket gönderirken hata oluştu",
            "Cihaz uyku moduna geçti",
            "Cihaz uyku modundan çıktı",
            "Bellek'ten veri transferinde doğrulama hatası",
            "CP'nin mesajına MP cevap vermiyor",
            "MP'nin mesajına CP cevap vermiyor",
            "Maestro Konfigürasyon Aracı veri hatası",
            "Bellekten veri yükleme hatası",
            "RAM'deki program verileri hatalı",
            "şebeke gerilimi ölçümü {}VAC en düşük şebeke gerilim seviyesi olan {}V'un altında",
            "şebeke gerilimi ölçümü {}VAC en yüksek şebeke gerilim seviyesi olan {}V'un üstünde",
            "Çalısma modu değişti. Önceki mod {}, yeni mod {}",
            "{} işlemcisi kilitlenip kendine reset attı.",
            "{} işlemcisi saat devresi hatası sebebiyle reset attı",
            "{} işlemcisi düşük gerilim sebebiyle reset attı",
            "SSM olay kaydı",
            "PSM olay kaydı",
            "IO olay kaydı",
            "{} No.lu sinyal grubuna ait tüm kırmızı lambalar arızalı",
            "{} No.lu sinyal grubuna ait tüm sarı lambalar arızalı",
            "{} No.lu sinyal grubuna ait tüm yeşil lambalar arızalı",
            "{} No.lu sinyal grubu kümesinde sinyal modu değişimi. Önceki mod {}, yeni mod {}",
            "Ana bellek bozuldu",
            "Yedek bellek bozuldu",
            "Yedekten ana bellege kopyalama hatası",
            "Yedek bellek okuma hatası",
            "Yedek bellek yazma hatası",
            "Ana bellek okuma hatası",
            "Ana bellek yazma hatası",
            "Yedek bellek ana belleşe kopyalandı",
            "Ana bellek kullanımda",
            "Yedek bellek kullanımda",
            "Ana bellek yedek belleşe kopyalandı",
            "Ana bellek yedek belleşe kopyalanırken hata oluştu",
            "{} işlemcisi POC devresi ile reset oldu",
            "Düşük pil gerilimi. Ölçülen gerilim {}V, alt sınır {}V",
            "Normal pil gerilimi. Olçulen gerilim {}V, alt sınır {}V",
            "Cihaz kapagı açıldı. Kapak sensör gerilimi {}V, ust sınır {}V",
            "Cihaz kapagı kapandı. Kapak sensör gerilimi {}V, alt sınır {}V",
            "Maestro Konfigürasyon Aracı konfigürasyon işlemi başladı",
            "Maestro Konfigürasyon Aracı konfigürasyon işlemi bitti",
            "LCD kullanıcı eklendi",
            "LCD kullanıcı eklenemedi",
            "şebeke gerilimi normal. Ölçülen gerilim {}V",
            "şebeke frekansı çok düşük. Ölçülen gerilim {}Hz, alt sınır {}Hz",
            "şebeke frekansı çok yüksek. Ölçülen frekans {}Hz, üst sınır {}Hz",
            "şebeke frekansı normal. Ölçülen frekans {}Hz",
            "Tüm gruplar kırmızı moduna alındı",
            "Kavşak karanlık moda alındı",
            "Kavşak flaş moduna alındı",
            "Kavşak normal çalışma planına alındı",
            "Kullanıcı güç ölçümü başlattı",
            "Kullanıcı SSM testi başlattı",
            "Kullanıcı SSM testini bitirdi",
            "Kullanıcı sinyal programı testi baslattı",
            "Kullanıcı sinyal programı testini bitirdi",
            "Kullanıcı tarih/saat ayarını değiştirdi",
            "Kullanıcı röleyi iletime soktu",
            "Kullanıcı röleyi devre dışı bıraktı",
            "{} kullanıcısı oturum açtı",
            "{} kullanıcısı oturumu kapatıldı",
            "{} kullanıcısı giriş ismi hatalı",
            "{} kullanıcısı giriş şifresi hatalı",
            "{} No.lu sinyal grubunda {} No.lu sinyal minimum süreden az yandı. Yandıgı süre {}S",
            "{} No.lu sinyal grubunda {} No.lu sinyal maksimum süreden fazla yandı. Yandıgı süre {}S",
            "{} No.lu dedektor arızası. Baglı olduğu sinyal grubu {}",
            "{} No.lu dedektor çalışıyor. Baglı olduğu sinyal grubu {}",
            "Çalışan sabit zaman tablosu değişti. Çalışan plan {}",
            "Çalışan program zaman tablosu değişti. Çalışan sinyal programı {} ",
            "Çalışan sinyal programı değişti. Çalışan sinyal programı {}. Zaman kaynagı {}",
            "Tum kırmızı lambalar sağlam",
            "Tum sarı lambalar sağlam",
            "Tum yeşil lambalar sağlam",
            "Reset yazılım",
            "Reset pin",
            "Reset por",
            "MCS bağlantı aktif",
            "MCS bağlantı kuruldu",
            "MCS bağlantı koptu",
            "MCS bağlantı zaman aşımı",
            "MCS sinyal planı değişti",
            "MCS tarih/zaman ayarı",
            "MCS reset",
            "MCS program yükleme",
            "MCS program okuma",
            "PSM testi başladı",
            "PSM testi bitti",
            "YD senkronizasyon başladı",
            "YD senkronizasyon bitti",
            "MCTS kapalı",
            "MCTS karanlık",
            "MCTS flaş",
            "MCTS normal"
        ],
        [
            "UNDEFINED",
            "Power on",
            "Signal output switch No. {} is short circuit. Measured current is {}A",
            "Signal output switch No. {} is open circuit",
            "Signal output No. {} voltage sensor failure",
            "Signal output No. {} is driven externally",
            "Working lamp count changed on signal output No. {}. Lamp count {}, default No. {}",
            "Wrong signal detected on signal output No. {}. Assigned signal {}, signal on output {}",
            "Invalid signal on group No. {}. Signal on output {}",
            "Invalid signal sequence on group No. {}. Previous signal {}, signal on output {} ",
            "Red lamp failure on group No. {}.",
            "Last red lamp failure on group No. {}.",
            "Specific number of red lamps failure on group No. {}.",
            "Yellow lamp failure on group No. {}.",
            "Green lamp failure on group No. {}.",
            "Yellow - Yellow conflict on groups No. {}. and No. {}.",
            "Yellow - Green conflict on groups No. {}. and No. {}.",
            "Green - Green conflict on groups No. {}. and No. {}.",
            "Signal output power record on group No. {}. Measured power {}W on {}V",
            "Module {}{} does not respond",
            "Module {}{} responds in {} time",
            "Info {}, {}, {}",
            "CP Checksum error",
            "MP Checksum error",
            "CP Receive error",
            "CP Transmission error",
            "MP Receive error",
            "MP Transmission error",
            "Switched to stand-by",
            "Wake up from stand-by.",
            "Data storage memory checksum error",
            "CP Response timeout",
            "MP Response timeout",
            "MCS Data transfer error",
            "Data load error",
            "Working program is corrupt",
            "Measured grid voltage {}V is too low. Minimum value is {}V",
            "Measured grid voltage {}V is too high. Maximum value is {}V",
            "Work mode changed from {} to {}",
            "Watchdog reset on microcontroller {}",
            "Reset by clock monitoring on microcontroller {}",
            "Low voltage reset on microcontroller {}",
            "SSM log",
            "PSM log",
            "IOM log",
            "All red lamps failed in group No. {}",
            "All yellow lamps failed in group No. {}",
            "All green lamps failed in group No. {}",
            "Signaling mode changed on signal group set No. {}. Previous mode {}, current mode {}",
            "Main storage memory failure",
            "Backup storage memory failure",
            "Backup -> Main storage memory copy error",
            "Backup storage memory read error",
            "Backup storage memory write error",
            "Main storage memory read error",
            "Main storage memory write error",
            "Backup -> Main storage memory copied",
            "Main storage memory in use",
            "Backup storage memory in use",
            "Main -> Backup storage memory copied",
            "Main -> Backup storage memory copy error.",
            "{} microcontroller reset by POC circuit",
            "Battery is low. Measured voltage is {}V. Minimum value {}V",
            "Battery is normal. Measured voltage is {}V. Minimum value {}V",
            "Door is opened. Measured sensor voltage is {}V. Maximum value {}V",
            "Door is closed. Measured sensor voltage is {}V. Minimum value {}V",
            "Maestro Configuration Tool started configuration",
            "Maestro Configuration Tool ended configuration",
            "Default user is added",
            "Error while adding default user.",
            "Grid voltage is normal. Measured voltage {}V",
            "Grid voltage frequency is too low. Measured frequency {}Hz. Minimum value {}Hz",
            "Grid voltage frequency is too high. Measured frequency {}Hz. Maximum value {}Hz",
            "Grid voltage frequency is normal. Measured frequency {}Hz",
            "All groups are switched to red manually",
            "All groups are switched to dark manually",
            "All groups are switched to flash manually",
            "Returned to normal working mode",
            "User started power measurement",
            "User started SSM test",
            "User finished SSM test",
            "User started signal program test",
            "User finished signal program test",
            "User changed date/time settings",
            "User set the relay on",
            "User set the relay off",
            "User {} logged in",
            "User {} logged out",
            "{} log in user name error",
            "{} log in password error",
            "Signal duration on signal group No. {} signal output No. {} is {}S. This is lower than minimum value",
            "Signal duration on signal group No. {} signal output No. {} is {}S. This is higher than maximum value",
            "Detector No. {} failed. It is connected to signal group No. {}",
            "Detector No. {} is working. It is connected to signal group No. {}",
            "Active fixed time table changed. Active plan No. {}",
            "Active program time table changed. Active plan No. {}",
            "Active signal program changed to program No. {}. Time source is {}",
            "All red lamps are safe",
            "All yellow lamps are safe",
            "All green lamps are safe",
            "Software reset",
            "Pin reset",
            "RESET POR",
            "MCTS Configuration active",
            "MCTS Configuration succeeded",
            "MCTS Configuration failed",
            "MCTS Configuration timeout",
            "MCTS Signal program change",
            "MCTS Date/Time adjustment",
            "MCTS Reset",
            "MCTS program download",
            "MCTS program upload",
            "PSM test starts",
            "PSM test ends",
            "GW synchronization started",
            "GW synchronization finished",
            "MCTS working mode changed to all red",
            "MCTS working mode changed to all dark",
            "MCTS working mode changed to all flash",
            "MCTS working mode changed to all work plan"
        ]
    ]

LogSignalTypes = \
    [
        [
            "KARANLIK", "KIRMIZI", "SARI", "SARI KIRMIZI", "YEŞİL", "KIRMIZI YEŞİL",
            "SARI YEŞİL", "KIRMIZI SARI YEŞİL", "-", "KIRMIZI FLAŞ", "SARI FLAŞ",
            "SARI KIRMIZI FLAŞ", "YEŞİL FLAŞ", "KIRMIZI YEŞİL FLAŞ", "SARI YEŞİL FLAŞ",
            "KIRMIZI SARI YEŞİL FLAŞ"
        ],
        [
            "DARK", "RED", "YELLOW", "YELLOW RED", "GREEN", "RED GREEN",
            "YELLOW GREEN ", "RED YELLOW GREEN", "-", "RED FLASH", "YELLOW FLASH",
            "YELLOW RED FLASH", "GREEN FLASH", "RED GREEN FLASH", "YELLOW GREEN FLASH",
            "RED YELLOW GREEN FLASH"
        ]
    ]

States = \
    [
        ["-", "DEVRE DIŞI", "FLAŞ", "KAPALI", "FAZ", "FAZ DEĞİŞİMİ", "SEK", "GÜVENLİ GEÇİŞ"],
        ["ANY", "DISABLED", "FLASH", "CLOSED", "PHASE", "PHASE TRANSITION", "SEQ", "SECURE TRANSITION"]
    ]

Controller = ["CP", "MP"]

# TODO change the dashes
# 0-8 are used in MCTS for program runtime states
# 9 is used for signaling mode download
# 10 is used for signaling mode emergency dark
# 11 is used for signaling mode emergency flash
# 12 is used in MCTS for warning state
# 13 is used in MCTS for stop mode
SignalingModesStr = \
    [
        ["-", "Normal", "Flaş", "-", "-", "-", "-", "-", "-", "-", "Acil Durum Karanlık", "Acil Durum Flaş", "-", "-"],
        ["-", "Normal", "Flash", "-", "-", "-", "-", "-", "-", "-", "Emergency State Dark", "Emergency State Flash",
         "-", "-"]
    ]

scroll_bar_stylesheet = """QScrollBar:vertical {
	border: 2px solid;
	border-color: rgb(23, 87, 141);
	background:white;
	width:80px;
	margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
	background-color: rgb(23, 87, 141);
	min-height: 0px;
}
QScrollBar::add-line:vertical {
	background-color: rgb(23, 87, 141);
	height: 0px;
	subcontrol-position: bottom;
	subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
	background-color: rgb(23, 87, 141);
	height: 0 px;
	subcontrol-position: top;
	subcontrol-origin: margin;
}

QScrollBar:horizontal {
	border: 2px solid;
	border-color: rgb(23, 87, 141);
	background:white;
	height:50px;
	margin: 0px 0px 0px 0px;
}
QScrollBar::handle:horizontal {
	background-color: rgb(23, 87, 141);
	min-width: 0px;
}
QScrollBar::add-line:horizontal {
	background-color: rgb(23, 87, 141);
	width: 0px;
	subcontrol-position: bottom;
	subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
	background-color: rgb(23, 87, 141);
	height: 0 px;
	subcontrol-position: top;
	subcontrol-origin: margin;
}"""
