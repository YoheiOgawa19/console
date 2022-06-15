#================================================================
#================================================================
# API-DIO(LNX) (BusMaster)
# 同期サンプリングサンプル
#                                                CONTEC Co., Ltd.
#================================================================
#================================================================
import ctypes
import sys
import cdio
sys.path.append('../common')
import TermLib


#================================================================
# マクロ定義
#================================================================
MENU_MASTER         = 0
MENU_SLAVE          = 1
MENU_EXIT           = 2
MENU_DIO_OPEN       = 0
MENU_CONDITION      = 1
MENU_START          = 2
MENU_STOP           = 3
MENU_DATA           = 4
MENU_COUNT          = 5
NENU_STATUS         = 6
MENU_DIO_CLOSE      = 7
MENU_RETURN         = 8
SET_MENU_START      = 0
SET_MENU_CLOCK      = 1
SET_MENU_STOP       = 2
SET_MENU_BUF_CON    = 3
SET_MENU_NOTIF      = 4
SET_MENU_OK         = 5
SET_MENU_CANCEL     = 6
STS_COUNT_POS       = 'Count'
STS_STATUS_POS      = 'Status'
STS_ERROR_POS       = 'Error'
STS_RET_POS         = 'Ret'
SET_NUM_COMP_PTN    = 0
SET_NUM_PTN_MASK    = 1
SET_NUM_CLOCK       = 2
SET_NUM_STOP_NUM    = 3
SET_NUM_NOTIF       = 4
SET_SLAVE_NUM_NOTIF = 0
DATA_SIZE_MASTER    = 1000                                  # マスターデータサイズ
DATA_SIZE_SLAVE     = 1000                                  # スレーブデータサイズ
#================================================================
# 外部変数
#================================================================
file_name_master    = 'sync_master.txt'                     # マスター保存ファイル名
file_name_slave     = 'sync_slave.txt'                      # スレーブ保存ファイル名
data_buff_master_type = ctypes.c_uint * DATA_SIZE_MASTER    # create the array type(データバッファ)
data_buff_slave_type = ctypes.c_uint * DATA_SIZE_SLAVE      # create the array type(データバッファ)
data_buff_master = data_buff_master_type()                  # マスターデータバッファ
data_buff_slave = data_buff_slave_type()                    # スレーブデータバッファ
dio_id_master = ctypes.c_short()                            # マスターデバイスID
dio_id_slave = ctypes.c_short()                             # スレーブデバイスID
is_ring_master = cdio.DIODM_WRITE_ONCE
is_ring_slave = cdio.DIODM_WRITE_ONCE


#----------------------------------------
# メイン画面データ
#----------------------------------------
main_scr = {
    #----------------------------------------
    # アプリケーション名
    #----------------------------------------
    'app_name':'<< Sync Sample >>',
    #----------------------------------------
    # 上部ステータスエリア名
    #----------------------------------------
    'status_top_name':'[Master Status]',
    #----------------------------------------
    # 下部ステータスエリア名
    #----------------------------------------
    'status_buttom_name':'[Slave Status]',
    #----------------------------------------
    # メニュー[階層][メニュー個数]
    #----------------------------------------
    'menu':[['Master','Slave','Exit'],
            ['DioInit','Condition...','Start','Stop','Data','Count','Status','DioExit','Return'],
            ['DioInit','Condition...','Start','Stop','Data','Count','Status','DioExit','Return'],
            []],
    #----------------------------------------
    # 上部ステータスエリアデータ
    #----------------------------------------
    'status_top':['Count','Status','Error','Ret'],
    #----------------------------------------
    # 下部ステータスエリアデータ
    #----------------------------------------
    'status_buttom':['Count','Status','Error','Ret']
}
#----------------------------------------
# 設定マスター画面データ
#----------------------------------------
set_master_scr = {
    #----------------------------------------
    # 設定画面名
    #----------------------------------------
    'window_name':'<< Master Sampling Condition >>',
    #----------------------------------------
    # メニュー[階層][メニュー個数]
    #----------------------------------------
    'menu':[['Start','Clock','Stop','Buffer','Notification','OK','Cancel'],[]],
    #----------------------------------------
    # 項目選択タイプ用設定データ
    #----------------------------------------
    'select_item':[{'pos_y':0,                          # 設定値表示画面で何段目に表示するか？
                    'set_item_name':'Start(ExtSig2)',   # 項目名
                    #----------------------------------------
                    # 選択肢, メニューに対応するマクロ
                    #----------------------------------------
                    'item':[{'name':'Software Start','num':cdio.DIODM_START_SOFT},
                            {'name':'External UP','num':cdio.DIODM_START_EXT_RISE},
                            {'name':'External DOWN','num':cdio.DIODM_START_EXT_FALL},
                            {'name':'Pattern','num':cdio.DIODM_START_PATTERN}],
                    'set_num':0                         # 設定値(何番目の選択肢か)
                    },
                    {'pos_y':2,
                    'set_item_name':'Clock(ExtSig1)',
                    'item':[{'name':'Internal Clock','num':cdio.DIODM_CLK_CLOCK},
                            {'name':'External Clock','num':cdio.DIODM_CLK_EXT_TRG},
                            {'name':'Hand Shake','num':cdio.DIODM_CLK_HANDSHAKE}],
                    'set_num':0
                    },
                    {'pos_y':3,
                    'set_item_name':'Stop(ExtSig3)',
                    'item':[{'name':'Software Stop','num':cdio.DIODM_STOP_SOFT},
                            {'name':'External UP','num':cdio.DIODM_STOP_EXT_RISE},
                            {'name':'External DOWN','num':cdio.DIODM_STOP_EXT_FALL},
                            {'name':'Number','num':cdio.DIODM_STOP_NUM}],
                    'set_num':0
                    },
                    {'pos_y':4,
                    'set_item_name':'Buffer',
                    'item':[{'name':'Write Once','num':cdio.DIODM_WRITE_ONCE},
                            {'name':'Write Ring','num':cdio.DIODM_WRITE_RING}],
                    'set_num':0
                    }],
    #----------------------------------------
    # 数値入力タイプ用設定データ
    #----------------------------------------
    'input_num':[{'pos_y':0,                            # 設定値表示画面で何段目に表示するか？
                  'set_item_name':'Compare Pattern',    # 項目名
                  'unit_name':'Hex',                    # 単位名
                  'set_num':0x55,                       # 設定値
                  'hex_or_dec':TermLib.HEX_NUM          # 何進数か？ HEX_NUM or DEC_NUM
                },
                {'pos_y':1,
                  'set_item_name':'Pattern Mask',
                  'unit_name':'Hex',
                  'set_num':0xFF,
                  'hex_or_dec':TermLib.HEX_NUM
                },
                {'pos_y':2,
                  'set_item_name':'Internal Clock',
                  'unit_name':'ns',
                  'set_num':1000,
                  'hex_or_dec':TermLib.DEC_NUM
                },
                {'pos_y':3,
                  'set_item_name':'Stop Number',
                  'unit_name':'',
                  'set_num':1000,
                  'hex_or_dec':TermLib.DEC_NUM
                },
                {'pos_y':4,
                  'set_item_name':'Number of Data',
                  'unit_name':'',
                  'set_num':500,
                  'hex_or_dec':TermLib.DEC_NUM
                }]
}
#----------------------------------------
# 設定スレーブ画面データ
#----------------------------------------
set_slave_scr = {
    #----------------------------------------
    # 設定画面名
    #----------------------------------------
    'window_name':'<< Slave Sampling Condition >>',
    #----------------------------------------
    # メニュー[階層][メニュー個数]
    #----------------------------------------
    'menu':[['Start','Clock','Stop','Buffer','Notification','OK','Cancel'],[]],
    #----------------------------------------
    # 項目選択タイプ用設定データ
    #----------------------------------------
    'select_item':[{'pos_y':0,                          # 設定値表示画面で何段目に表示するか？
                    'set_item_name':'Start',            # 項目名
                    #----------------------------------------
                    # 選択肢, メニューに対応するマクロ
                    #----------------------------------------
                    'item':[{'name':'ExtSig1','num':cdio.DIODM_START_EXTSIG_1},
                            {'name':'ExtSig2','num':cdio.DIODM_START_EXTSIG_2},
                            {'name':'ExtSig3','num':cdio.DIODM_START_EXTSIG_3}],
                    'set_num':1                         # 設定値(何番目の選択肢か)
                    },
                    {'pos_y':2,
                    'set_item_name':'Clock',
                    'item':[{'name':'ExtSig1','num':cdio.DIODM_CLK_EXTSIG_1},
                            {'name':'ExtSig2','num':cdio.DIODM_CLK_EXTSIG_2},
                            {'name':'ExtSig3','num':cdio.DIODM_CLK_EXTSIG_3}],
                    'set_num':0
                    },
                    {'pos_y':3,
                    'set_item_name':'Stop',
                    'item':[{'name':'ExtSig1','num':cdio.DIODM_STOP_EXTSIG_1},
                            {'name':'ExtSig2','num':cdio.DIODM_STOP_EXTSIG_2},
                            {'name':'ExtSig3','num':cdio.DIODM_STOP_EXTSIG_3}],
                    'set_num':2
                    },
                    {'pos_y':4,
                    'set_item_name':'Buffer',
                    'item':[{'name':'Write Once','num':cdio.DIODM_WRITE_ONCE},
                            {'name':'Write Ring','num':cdio.DIODM_WRITE_RING}],
                    'set_num':0
                    }],
    #----------------------------------------
    # 数値入力タイプ用設定データ
    #----------------------------------------
    'input_num':[{'pos_y':1,                            # 設定値表示画面で何段目に表示するか？
                  'set_item_name':'Number of Data',     # 項目名
                  'unit_name':'',                       # 単位名
                  'set_num':500,                        # 設定値
                  'hex_or_dec':TermLib.DEC_NUM          # 何進数か？ HEX_NUM or DEC_NUM
                }]
}


#================================================================
# マスターの転送完了コールバック関数
#================================================================
def stop_callback_master(dev_id, message, dir, param):
    #----------------------------------------
    # 割り込みメッセージの処理
    #----------------------------------------
    if message == cdio.DIO_DMM_STOP:
        TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_STATUS_POS, 'Stopped!')
    #----------------------------------------
    # それ以外
    #----------------------------------------
    else:
        TermLib.TermSetStatus(TermLib.STATUS_AREA_YOP, STS_STATUS_POS, f'Message Number : {message}')
    return


#================================================================
# スレーブの転送完了コールバック関数
#================================================================
def stop_callback_slave(dev_id, message, dir, param):
    #----------------------------------------
    # 割り込みメッセージの処理
    #----------------------------------------
    if message == cdio.DIO_DMM_STOP:
        TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_STATUS_POS, 'Stopped!')
    #----------------------------------------
    # それ以外
    #----------------------------------------
    else:
        TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_STATUS_POS, f'Message Number : {message}')
    return


#================================================================
# マスターの指定個数転送完了コールバック関数
#================================================================
def count_callback_master(dev_id, message, dir, param):
    count = ctypes.c_ulong()
    carry = ctypes.c_ulong()
    err_str = ctypes.create_string_buffer(256)

    #----------------------------------------
    # 割り込みメッセージの処理
    #----------------------------------------
    if message == cdio.DIO_DMM_COUNT:
        lret =  cdio.DioDmGetCount(dev_id, cdio.DIODM_DIR_IN, ctypes.byref(count), ctypes.byref(carry))
        if lret == cdio.DIO_ERR_SUCCESS:
            TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_COUNT_POS, str(count.value))
        cdio.DioGetErrorString(lret, err_str)
        TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, 'DioDmGetCount ' + str(lret) + ':' + err_str.value.decode('sjis'))
    #----------------------------------------
    # それ以外
    #----------------------------------------
    else:
        TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_STATUS_POS, f'Message Number : {message}')
    return


#================================================================
# スレーブの指定個数転送完了コールバック関数
#================================================================
def count_callback_slave(dev_id, message, dir, param):
    count = ctypes.c_ulong()
    carry = ctypes.c_ulong()
    err_str = ctypes.create_string_buffer(256)

    #----------------------------------------
    # 割り込みメッセージの処理
    #----------------------------------------
    if message == cdio.DIO_DMM_COUNT:
        lret =  cdio.DioDmGetCount(dev_id, cdio.DIODM_DIR_IN, ctypes.byref(count), ctypes.byref(carry))
        if lret == cdio.DIO_ERR_SUCCESS:
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_COUNT_POS, str(count.value))
        cdio.DioGetErrorString(lret, err_str)
        TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, 'DioDmGetCount ' + str(lret) + ':' + err_str.value.decode('sjis'))
    #----------------------------------------
    # それ以外
    #----------------------------------------
    else:
        TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_STATUS_POS, f'Message Number : {message}')
    return


pstop_callback_master = cdio.PDIO_STOP_CALLBACK(stop_callback_master)
pstop_callback_slave = cdio.PDIO_STOP_CALLBACK(stop_callback_slave)
pcount_callback_master = cdio.PDIO_COUNT_CALLBACK(count_callback_master)
pcount_callback_slave = cdio.PDIO_COUNT_CALLBACK(count_callback_slave)


#================================================================
# マスターの転送条件設定関数
#================================================================
def master_condition(err_str):
    menu_num = -1
    start = clock = stop = -1
    comp_ptn = ptn_mask = internal_clock = stop_num = notification = -1
    get_str = ctypes.create_string_buffer(256)
    dir = cdio.DIODM_DIR_IN
    global is_ring_master

    #----------------------------------------
    # 外部信号用設定データ
    #----------------------------------------
    #----------------------------------------
    # Start Condition
    #----------------------------------------
    stnStart = [
        {'Str':'Software Start',    'Num':cdio.DIODM_START_SOFT,     'ExtSig':cdio.DIODM_EXT_START_SOFT_IN},
        {'Str':'External UP',       'Num':cdio.DIODM_START_EXT_RISE, 'ExtSig':cdio.DIODM_EXT_START_EXT_RISE_IN},
        {'Str':'External Down',     'Num':cdio.DIODM_START_EXT_FALL, 'ExtSig':cdio.DIODM_EXT_START_EXT_FALL_IN},
        {'Str':'Pattern',           'Num':cdio.DIODM_START_PATTERN,  'ExtSig':cdio.DIODM_EXT_START_PATTERN_IN}]
    #----------------------------------------
    # Clock Condition
    #----------------------------------------
    stnClock = [
        {'Str':'Internal Clock',    'Num':cdio.DIODM_CLK_CLOCK,      'ExtSig':cdio.DIODM_EXT_CLOCK_IN},
        {'Str':'External Clock',    'Num':cdio.DIODM_CLK_EXT_TRG,    'ExtSig':cdio.DIODM_EXT_EXT_TRG_IN},
        {'Str':'Hand Shake',        'Num':cdio.DIODM_CLK_HANDSHAKE,  'ExtSig':cdio.DIODM_EXT_HANDSHAKE_IN}]
    #----------------------------------------
    # Stop Condition
    #----------------------------------------
    stnStop = [
        {'Str':'Software Stop',     'Num':cdio.DIODM_STOP_SOFT,      'ExtSig':cdio.DIODM_EXT_STOP_SOFT_IN},
        {'Str':'External UP',       'Num':cdio.DIODM_STOP_EXT_RISE,  'ExtSig':cdio.DIODM_EXT_STOP_EXT_RISE_IN},
        {'Str':'External Down',     'Num':cdio.DIODM_STOP_EXT_FALL,  'ExtSig':cdio.DIODM_EXT_STOP_EXT_FALL_IN},
        {'Str':'Number',            'Num':cdio.DIODM_STOP_NUM,       'ExtSig':cdio.DIODM_EXT_TRNSNUM_IN}]
    #----------------------------------------
    # 設定データ初期化
    #----------------------------------------
    def_set_num = set_master_scr['select_item'][SET_MENU_START]['set_num']
    start = set_master_scr['select_item'][SET_MENU_START]['item'][def_set_num]['num']
    def_set_num = set_master_scr['select_item'][SET_MENU_CLOCK]['set_num']
    clock = set_master_scr['select_item'][SET_MENU_CLOCK]['item'][def_set_num]['num']
    def_set_num = set_master_scr['select_item'][SET_MENU_STOP]['set_num']
    stop = set_master_scr['select_item'][SET_MENU_STOP]['item'][def_set_num]['num']
    comp_ptn = set_master_scr['input_num'][SET_NUM_COMP_PTN]['set_num']
    ptn_mask = set_master_scr['input_num'][SET_NUM_PTN_MASK]['set_num']
    internal_clock = set_master_scr['input_num'][SET_NUM_CLOCK]['set_num']
    stop_num = set_master_scr['input_num'][SET_NUM_STOP_NUM]['set_num']
    notification = set_master_scr['input_num'][SET_NUM_NOTIF]['set_num']
    #----------------------------------------
    # 設定ウインドウ初期化
    #----------------------------------------
    lret = TermLib.TermSetWindowOpen(set_master_scr)
    if lret != TermLib.TERM_ERR_SUCCESS:
        err_str = 'TermSetWindowOpen ' + str(lret)
        return 1, err_str
    #----------------------------------------
    # メニュー処理
    #----------------------------------------
    err_str = ''
    while True:
        #----------------------------------------
        # 前回エラーだったら設定画面終了
        #----------------------------------------
        if err_str != '':
            TermLib.TermSetWindowClose()
            return 1, err_str
        #----------------------------------------
        # メニュー番号入力
        #----------------------------------------
        lret, menu_num = TermLib.TermGetMenuNum('Please input a menu number(0-6).', menu_num)
        if lret != TermLib.TERM_ERR_SUCCESS:
            err_str = 'TermGetMenuNum ' + str(lret)
            return 1, err_str
        #----------------------------------------
        # スタート条件設定
        #----------------------------------------
        if menu_num == SET_MENU_START:
            lret, start = TermLib.TermGetSelectItem(set_master_scr, SET_MENU_START, start)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
            if start == cdio.DIODM_START_PATTERN:
                lret, comp_ptn = TermLib.TermGetInputNum(set_master_scr, SET_NUM_COMP_PTN, comp_ptn)
                if lret != TermLib.TERM_ERR_SUCCESS:
                    err_str = 'TermGetInputNum ' + str(lret)
                lret, ptn_mask = TermLib.TermGetInputNum(set_master_scr, SET_NUM_PTN_MASK, ptn_mask)
                if lret != TermLib.TERM_ERR_SUCCESS:
                    err_str = 'TermGetInputNum ' + str(lret)
        #----------------------------------------
        # クロック条件設定
        #----------------------------------------
        elif menu_num == SET_MENU_CLOCK:
            lret, clock = TermLib.TermGetSelectItem(set_master_scr, SET_MENU_CLOCK, clock)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
            if clock == cdio.DIODM_CLK_CLOCK:
                lret, internal_clock = TermLib.TermGetInputNum(set_master_scr, SET_NUM_CLOCK, internal_clock)
                if lret != TermLib.TERM_ERR_SUCCESS:
                    err_str = 'TermGetInputNum ' + str(lret)
        #----------------------------------------
        # ストップ条件設定
        #----------------------------------------
        elif menu_num == SET_MENU_STOP:
            lret, stop = TermLib.TermGetSelectItem(set_master_scr, SET_MENU_STOP, stop)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
            if stop == cdio.DIODM_STOP_NUM:
                lret, stop_num = TermLib.TermGetInputNum(set_master_scr, SET_NUM_STOP_NUM, stop_num)
                if lret != TermLib.TERM_ERR_SUCCESS:
                    err_str = 'TermGetInputNum ' + str(lret)
        #----------------------------------------
        # バッファ転送設定
        #----------------------------------------
        elif menu_num == SET_MENU_BUF_CON:
            lret, is_ring_master = TermLib.TermGetSelectItem(set_master_scr, SET_MENU_BUF_CON, is_ring_master)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
        #----------------------------------------
        # 通知カウント設定
        #----------------------------------------
        elif menu_num == SET_MENU_NOTIF:
            lret, notification = TermLib.TermGetInputNum(set_master_scr, SET_NUM_NOTIF, notification)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetInputNum ' + str(lret)
        #----------------------------------------
        # OK処理
        #----------------------------------------
        elif menu_num == SET_MENU_OK:
            #----------------------------------------
            # Direction
            #----------------------------------------
            lret = cdio.DioDmSetDirection(dio_id_master, cdio.PI_32)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetDirection ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Master
            #----------------------------------------
            #----------------------------------------
            # parameter exchange
            #----------------------------------------
            ExtSig2 = 0
            for i in stnStart:
                if start == i['Num']:
                    ExtSig2 = i['ExtSig']
                    break
            ExtSig1 = 0
            for i in stnClock:
                if clock == i['Num']:
                    ExtSig1 = i['ExtSig']
                    break
            ExtSig3 = 0
            for i in stnStop:
                if stop == i['Num']:
                    ExtSig3 = i['ExtSig']
                    break
            lret = cdio.DioDmSetMasterCfg(dio_id_master, ExtSig1, ExtSig2, ExtSig3, 1, 1)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetMasterCfg ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Start Condition
            #----------------------------------------
            lret = cdio.DioDmSetStartTrg(dio_id_master, dir, start)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetStartTrg ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Clock Condition
            #----------------------------------------
            lret = cdio.DioDmSetClockTrg(dio_id_master, dir, clock)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetClockTrg ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Stop Condition
            #----------------------------------------
            lret = cdio.DioDmSetStopTrg(dio_id_master, dir, stop)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetStopTrg ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Pattern/Mask
            #----------------------------------------
            lret = cdio.DioDmSetStartPattern(dio_id_master, comp_ptn, ptn_mask)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetStartPattern ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Internal Clock
            #----------------------------------------
            lret = cdio.DioDmSetInternalClock(dio_id_master, dir, internal_clock, cdio.DIODM_TIM_UNIT_NS)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetInternalClock ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # StopNumber
            #----------------------------------------
            lret = cdio.DioDmSetStopNum(dio_id_master, dir, stop_num)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetStopNum ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # 設定画面終了
            #----------------------------------------
            TermLib.TermSetWindowClose()
            return 0, err_str
        #----------------------------------------
        # Cancel処理
        #----------------------------------------
        elif menu_num == SET_MENU_CANCEL:
            #----------------------------------------
            # 設定画面終了
            #----------------------------------------
            TermLib.TermSetWindowClose()
            return 0, err_str

    return 0, err_str


#================================================================
# スレーブの転送条件設定関数
#================================================================
def slave_condition(err_str):
    menu_num = -1
    start = clock = stop = -1
    notification = -1
    get_str = ctypes.create_string_buffer(256)
    dir = cdio.DIODM_DIR_IN
    global is_ring_slave

    #----------------------------------------
    # 設定データ初期化
    #----------------------------------------
    def_set_num  = set_slave_scr['select_item'][SET_MENU_START]['set_num']
    start        = set_slave_scr['select_item'][SET_MENU_START]['item'][def_set_num]['num']
    def_set_num  = set_slave_scr['select_item'][SET_MENU_CLOCK]['set_num']
    clock        = set_slave_scr['select_item'][SET_MENU_CLOCK]['item'][def_set_num]['num']
    def_set_num  = set_slave_scr['select_item'][SET_MENU_STOP]['set_num']
    stop         = set_slave_scr['select_item'][SET_MENU_STOP]['item'][def_set_num]['num']
    notification = set_slave_scr['input_num'][SET_SLAVE_NUM_NOTIF]['set_num']
    #----------------------------------------
    # 設定ウインドウ初期化
    #----------------------------------------
    lret = TermLib.TermSetWindowOpen(set_slave_scr)
    if lret != TermLib.TERM_ERR_SUCCESS:
        err_str = 'TermSetWindowOpen ' + str(lret)
        return 1, err_str
    #----------------------------------------
    # メニュー処理
    #----------------------------------------
    err_str = ''
    while True:
        #----------------------------------------
        # 前回エラーだったら設定画面終了
        #----------------------------------------
        if err_str != '':
            TermLib.TermSetWindowClose()
            return 1, err_str
        #----------------------------------------
        # メニュー番号入力
        #----------------------------------------
        lret, menu_num = TermLib.TermGetMenuNum('Please input a menu number(0-6).', menu_num)
        if lret != TermLib.TERM_ERR_SUCCESS:
            err_str = 'TermGetMenuNum ' + str(lret)
            return 1, err_str
        #----------------------------------------
        # スタート条件設定
        #----------------------------------------
        if menu_num == SET_MENU_START:
            lret, start = TermLib.TermGetSelectItem(set_slave_scr, SET_MENU_START, start)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
        #----------------------------------------
        # クロック条件設定
        #----------------------------------------
        elif menu_num == SET_MENU_CLOCK:
            lret, clock = TermLib.TermGetSelectItem(set_slave_scr, SET_MENU_CLOCK, clock)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
        #----------------------------------------
        # ストップ条件設定
        #----------------------------------------
        elif menu_num == SET_MENU_STOP:
            lret, stop = TermLib.TermGetSelectItem(set_slave_scr, SET_MENU_STOP, stop)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
        #----------------------------------------
        # バッファ条件設定
        #----------------------------------------
        elif menu_num == SET_MENU_BUF_CON:
            lret, is_ring_slave = TermLib.TermGetSelectItem(set_slave_scr, SET_MENU_BUF_CON, is_ring_slave)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
        #----------------------------------------
        # 通知カウント設定
        #----------------------------------------
        elif menu_num == SET_MENU_NOTIF:
            lret, notification = TermLib.TermGetInputNum(set_slave_scr, SET_SLAVE_NUM_NOTIF, notification)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetInputNum ' + str(lret)
        #----------------------------------------
        # OK処理
        #----------------------------------------
        elif menu_num == SET_MENU_OK:
            #----------------------------------------
            # Direction
            #----------------------------------------
            lret = cdio.DioDmSetDirection(dio_id_slave, cdio.PI_32)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetDirection ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # スレーブの外部信号設定
            #----------------------------------------
            ExtSig1 = 1
            ExtSig2 = 1
            ExtSig3 = 1
            lret = cdio.DioDmSetSlaveCfg(dio_id_slave, ExtSig1, ExtSig2, ExtSig3, 1, 1)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetSlaveCfg ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Start Condition
            #----------------------------------------
            lret = cdio.DioDmSetStartTrg(dio_id_slave, dir, start)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetStartTrg ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Clock Condition
            #----------------------------------------
            lret = cdio.DioDmSetClockTrg(dio_id_slave, dir, clock)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetClockTrg ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Stop Condition
            #----------------------------------------
            lret = cdio.DioDmSetStopTrg(dio_id_slave, dir, stop)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetStopTrg ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # 設定画面終了
            #----------------------------------------
            TermLib.TermSetWindowClose()
            return 0, err_str
        #----------------------------------------
        # Cancel処理
        #----------------------------------------
        elif menu_num == SET_MENU_CANCEL:
            #----------------------------------------
            # 設定画面終了
            #----------------------------------------
            TermLib.TermSetWindowClose()
            return 0, err_str

    return 0, err_str


#================================================================
# マスター関数
#================================================================
def master():
    dir = cdio.DIODM_DIR_IN
    count = ctypes.c_ulong()
    carry = ctypes.c_ulong()
    status = ctypes.c_ulong()
    err = ctypes.c_ulong()
    get_str = ctypes.create_string_buffer(256)
    menu_num = -1
    dev_name = ''
    err_str = ''

    #----------------------------------------
    # メニュー項目設定
    #----------------------------------------
    TermLib.TermMenuSet(main_scr['menu'][1])
    #----------------------------------------
    # メニュー処理
    #----------------------------------------
    while True:
        lret, menu_num = TermLib.TermGetMenuNum('Please input a menu number(0-8).', menu_num)
        if lret != TermLib.TERM_ERR_SUCCESS:
            print('RetCode = {}'.format(lret))
            return 0
        #----------------------------------------
        # 初期化処理
        #----------------------------------------
        if menu_num == MENU_DIO_OPEN:
            lret, dev_name = TermLib.TermGetStr('Please input a device name.', dev_name)
            if lret != TermLib.TERM_ERR_SUCCESS:
                print('RetCode = {}'.format(lret))
                return 0
            lret = cdio.DioInit(dev_name.encode(), ctypes.byref(dio_id_master))
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioInit {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
        #----------------------------------------
        # 設定
        #----------------------------------------
        elif menu_num == MENU_CONDITION:
            lret, err_str = master_condition(err_str)
            if  lret == 1:
                TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, err_str)
        #----------------------------------------
        # 転送スタート
        #----------------------------------------
        elif menu_num == MENU_START:
            #----------------------------------------
            # Notification
            #----------------------------------------
            lret = cdio.DioDmSetStopEvent(dio_id_master, dir, pstop_callback_master, "")
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmSetStopEvent {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
                continue
            notification = set_master_scr['input_num'][SET_NUM_NOTIF]['set_num']
            lret = cdio.DioDmSetCountEvent(dio_id_master, dir, notification, pcount_callback_master, "")
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmSetCountEvent {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
                continue
            #----------------------------------------
            # Reset
            #----------------------------------------
            lret = cdio.DioDmReset(dio_id_master, cdio.DIODM_RESET_FIFO_IN)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmReset {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
                continue
            #----------------------------------------
            # Set Buffer
            #----------------------------------------
            lret = cdio.DioDmSetBuff(dio_id_master, dir, ctypes.cast(data_buff_master, ctypes.POINTER(ctypes.c_ulong)), DATA_SIZE_MASTER, is_ring_master)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmSetBuff {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
                continue
            #----------------------------------------
            # Start
            #----------------------------------------
            lret = cdio.DioDmStart(dio_id_master, dir)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioDmStart {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
        #----------------------------------------
        # 転送停止
        #----------------------------------------
        elif menu_num == MENU_STOP:
            lret = cdio.DioDmStop(dio_id_master, dir)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioDmStop {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
        #----------------------------------------
        # データをファイルに保存
        #----------------------------------------
        elif menu_num == MENU_DATA:
            #----------------------------------------
            # ファイルオープン
            #----------------------------------------
            try:
                the_file = open(file_name_master, 'w')
            except:
                buf = str.format('open : file open error.')
                TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
                continue
            #----------------------------------------
            # ファイルに書き込み
            #----------------------------------------
            for i in range(DATA_SIZE_MASTER):
                buf = str.format('{0:8d} : {1:08X}\n', i, data_buff_master[i])
                the_file.write(buf)
            #----------------------------------------
            # ファイルクローズ
            #----------------------------------------
            the_file.close()
            buf = str.format('{} にデータを保存しました。', file_name_master)
            TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
        #----------------------------------------
        # 転送カウント取得
        #----------------------------------------
        elif menu_num == MENU_COUNT:
            lret = cdio.DioDmGetCount(dio_id_master, dir, ctypes.byref(count), ctypes.byref(carry))
            if lret == TermLib.TERM_ERR_SUCCESS:
                buf = str.format('{}', count.value)
                TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_COUNT_POS, buf)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioDmGetCount {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
        #----------------------------------------
        # ステータス取得
        #----------------------------------------
        elif menu_num == NENU_STATUS:
            lret = cdio.DioDmGetStatus(dio_id_master, dir, ctypes.byref(status), ctypes.byref(err))
            if lret == TermLib.TERM_ERR_SUCCESS:
                #----------------------------------------
                # Status
                #----------------------------------------
                buf = ''
                if status.value & cdio.DIODM_STATUS_BMSTOP:     buf += 'BmStop,'
                if status.value & cdio.DIODM_STATUS_PIOSTART:   buf += 'PioStart,'
                if status.value & cdio.DIODM_STATUS_PIOSTOP:    buf += 'PioStop,'
                if status.value & cdio.DIODM_STATUS_TRGIN:      buf += 'TrgIn,'
                if status.value & cdio.DIODM_STATUS_OVERRUN:    buf += 'Overrun'
                TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_STATUS_POS, buf)
                #----------------------------------------
                # Error
                #----------------------------------------
                buf = ''
                if err.value & cdio.DIODM_STATUS_FIFOEMPTY:     buf += 'FifoEmpty,'
                if err.value & cdio.DIODM_STATUS_FIFOFULL:      buf += 'FifoFull,'
                if err.value & cdio.DIODM_STATUS_SGOVERIN:      buf += 'S/GOverIn,'
                if err.value & cdio.DIODM_STATUS_TRGERR:        buf += 'TrgErr,'
                if err.value & cdio.DIODM_STATUS_CLKERR:        buf += 'ClkErr,'
                if err.value & cdio.DIODM_STATUS_SLAVEHALT:     buf += 'SlaveHalt,'
                if err.value & cdio.DIODM_STATUS_MASTERHALT:    buf += 'MasterHalt'
                TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_ERROR_POS, buf)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioDmGetStatus {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
        #----------------------------------------
        # 終了処理
        #----------------------------------------
        elif menu_num == MENU_DIO_CLOSE:
            lret = cdio.DioExit(dio_id_master)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioExit {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_TOP, STS_RET_POS, buf)
        #----------------------------------------
        # マスター画面終了
        #----------------------------------------
        elif menu_num == MENU_RETURN:
            TermLib.TermMenuSet(main_scr['menu'][0])
            return 0

    return 0


#================================================================
# スレーブ関数
#================================================================
def slave():
    dir = cdio.DIODM_DIR_IN
    count = ctypes.c_ulong()
    carry = ctypes.c_ulong()
    status = ctypes.c_ulong()
    err = ctypes.c_ulong()
    get_str = ctypes.create_string_buffer(256)
    menu_num = -1
    dev_name = ''
    err_str = ''

    #----------------------------------------
    # メニュー項目設定
    #----------------------------------------
    TermLib.TermMenuSet(main_scr['menu'][2])
    #----------------------------------------
    # メニュー処理
    #----------------------------------------
    while True:
        lret, menu_num = TermLib.TermGetMenuNum('Please input a menu number(0-8).', menu_num)
        if lret != TermLib.TERM_ERR_SUCCESS:
            print('RetCode = {}'.format(lret))
            return 0
        #----------------------------------------
        # 初期化処理
        #----------------------------------------
        if menu_num == MENU_DIO_OPEN:
            lret, dev_name = TermLib.TermGetStr('Please input a device name.', dev_name)
            if lret != TermLib.TERM_ERR_SUCCESS:
                print('RetCode = {}'.format(lret))
                return 0
            lret = cdio.DioInit(dev_name.encode(), ctypes.byref(dio_id_slave))
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioInit {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # 設定
        #----------------------------------------
        elif menu_num == MENU_CONDITION:
            lret, err_str = slave_condition(err_str)
            if  lret == 1:
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, err_str)
        #----------------------------------------
        # 転送スタート
        #----------------------------------------
        elif menu_num == MENU_START:
            #----------------------------------------
            # Notification
            #----------------------------------------
            lret = cdio.DioDmSetStopEvent(dio_id_slave, dir, pstop_callback_slave, "")
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmSetStopEvent {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
                continue
            notification = set_slave_scr['input_num'][SET_SLAVE_NUM_NOTIF]['set_num']
            lret = cdio.DioDmSetCountEvent(dio_id_slave, dir, notification, pcount_callback_slave, "")
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmSetCountEvent {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
                continue
            #----------------------------------------
            # Reset
            #----------------------------------------
            lret = cdio.DioDmReset(dio_id_slave, cdio.DIODM_RESET_FIFO_IN)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmReset {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
                continue
            #----------------------------------------
            # Set Buffer
            #----------------------------------------
            lret = cdio.DioDmSetBuff(dio_id_slave, dir, ctypes.cast(data_buff_slave, ctypes.POINTER(ctypes.c_ulong)), DATA_SIZE_SLAVE, is_ring_slave)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmSetBuff {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
                continue
            #----------------------------------------
            # Start
            #----------------------------------------
            lret = cdio.DioDmStart(dio_id_slave, dir)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioDmStart {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # 転送停止
        #----------------------------------------
        elif menu_num == MENU_STOP:
            lret = cdio.DioDmStop(dio_id_slave, dir)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioDmStop {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # データをファイルに保存
        #----------------------------------------
        elif menu_num == MENU_DATA:
            #----------------------------------------
            # ファイルオープン
            #----------------------------------------
            try:
                the_file = open(file_name_slave, 'w')
            except:
                buf = str.format('open : file open error.')
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
                continue
            #----------------------------------------
            # ファイルに書き込み
            #----------------------------------------
            for i in range(DATA_SIZE_SLAVE):
                buf = str.format('{0:8d} : {1:08X}\n', i, data_buff_slave[i])
                the_file.write(buf)
            #----------------------------------------
            # ファイルクローズ
            #----------------------------------------
            the_file.close()
            buf = str.format('{} にデータを保存しました。', file_name_slave)
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # 転送カウント取得
        #----------------------------------------
        elif menu_num == MENU_COUNT:
            lret = cdio.DioDmGetCount(dio_id_slave, dir, ctypes.byref(count), ctypes.byref(carry))
            if lret == TermLib.TERM_ERR_SUCCESS:
                buf = str.format('{}', count.value)
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_COUNT_POS, buf)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioDmGetCount {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # ステータス取得
        #----------------------------------------
        elif menu_num == NENU_STATUS:
            lret = cdio.DioDmGetStatus(dio_id_slave, dir, ctypes.byref(status), ctypes.byref(err))
            if lret == TermLib.TERM_ERR_SUCCESS:
                #----------------------------------------
                # Status
                #----------------------------------------
                buf = ''
                if status.value & cdio.DIODM_STATUS_BMSTOP:     buf += 'BmStop,'
                if status.value & cdio.DIODM_STATUS_PIOSTART:   buf += 'PioStart,'
                if status.value & cdio.DIODM_STATUS_PIOSTOP:    buf += 'PioStop,'
                if status.value & cdio.DIODM_STATUS_TRGIN:      buf += 'TrgIn,'
                if status.value & cdio.DIODM_STATUS_OVERRUN:    buf += 'Overrun'
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_STATUS_POS, buf)
                #----------------------------------------
                # Error
                #----------------------------------------
                buf = ''
                if err.value & cdio.DIODM_STATUS_FIFOEMPTY:     buf += 'FifoEmpty,'
                if err.value & cdio.DIODM_STATUS_FIFOFULL:      buf += 'FifoFull,'
                if err.value & cdio.DIODM_STATUS_SGOVERIN:      buf += 'S/GOverIn,'
                if err.value & cdio.DIODM_STATUS_TRGERR:        buf += 'TrgErr,'
                if err.value & cdio.DIODM_STATUS_CLKERR:        buf += 'ClkErr,'
                if err.value & cdio.DIODM_STATUS_SLAVEHALT:     buf += 'SlaveHalt,'
                if err.value & cdio.DIODM_STATUS_MASTERHALT:    buf += 'MasterHalt'
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_ERROR_POS, buf)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioDmGetStatus {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # 終了処理
        #----------------------------------------
        elif menu_num == MENU_DIO_CLOSE:
            lret = cdio.DioExit(dio_id_slave)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioExit {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # スレーブ画面終了
        #----------------------------------------
        elif menu_num == MENU_RETURN:
            TermLib.TermMenuSet(main_scr['menu'][0])
            return 0

    return 0


#================================================================
# メイン関数
#================================================================
def main():
    menu_num = -1

    #----------------------------------------
    # TermLib初期化
    #----------------------------------------
    lret = TermLib.TermInit(main_scr)
    if lret != TermLib.TERM_ERR_SUCCESS:
        print('RetCode = {}'.format(lret))
        sys.exit()
    #----------------------------------------
    # メニュー処理
    #----------------------------------------
    while True:
        lret, menu_num = TermLib.TermGetMenuNum('Please input a menu number(0-2)', menu_num)
        if lret != TermLib.TERM_ERR_SUCCESS:
            print('RetCode = {}'.format(lret))
            break
        #----------------------------------------
        # マスター
        #----------------------------------------
        if menu_num == MENU_MASTER:
            master()
        #----------------------------------------
        # スレーブ
        #----------------------------------------
        elif menu_num == MENU_SLAVE:
            slave()
        #----------------------------------------
        # サンプル終了
        #----------------------------------------
        elif menu_num == MENU_EXIT:
            TermLib.TermExit()
            break
    sys.exit()


#----------------------------------------
# main関数呼び出し
#----------------------------------------
if __name__ == "__main__":
    main()
