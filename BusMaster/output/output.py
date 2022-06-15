#================================================================
#================================================================
# API-DIO(LNX) (BusMaster)
# ジェネレーティングサンプル
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
MENU_DIO_OPEN       = 0
MENU_CONDITION      = 1
MENU_DATA_SET       = 2
MENU_START          = 3
MENU_STOP           = 4
MENU_COUNT          = 5
NENU_STATUS         = 6
MENU_DIO_CLOSE      = 7
MENU_EXIT           = 8
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
SET_NUM_CLOCK       = 0
SET_NUM_STOP_NUM    = 1
SET_NUM_NOTIF       = 2
DATA_SIZE           = 1000                      # データサイズ
#================================================================
# 外部変数
#================================================================
file_name = 'output.txt'                        # 保存ファイル名
data_buff_type = ctypes.c_uint * DATA_SIZE      # create the array type(データバッファ)
data_buff = data_buff_type()                    # allocate several instances of that type(データバッファ)
is_ring = int(0)                                # 1回転送 or 無限回転送


#----------------------------------------
# メイン画面データ
#----------------------------------------
main_scr = {
    #----------------------------------------
    # アプリケーション名
    #----------------------------------------
    'app_name':'<< Generating Sample >>',
    #----------------------------------------
    # 上部ステータスエリア名
    #----------------------------------------
    'status_top_name':'',
    #----------------------------------------
    # 下部ステータスエリア名
    #----------------------------------------
    'status_buttom_name':'',
    #----------------------------------------
    # メニュー[階層][メニュー個数]
    #----------------------------------------
    'menu':[['DioInit','Condition...','DataSet','Start','Stop','Count','Status','DioExit','Exit'],[]],
    #----------------------------------------
    # 上部ステータスエリアデータ
    #----------------------------------------
    'status_top':[],
    #----------------------------------------
    # 下部ステータスエリアデータ
    #----------------------------------------
    'status_buttom':['Count','Status','Error','Ret']
}
#----------------------------------------
# 設定画面データ
#----------------------------------------
set_scr = {
    #----------------------------------------
    # 設定画面名
    #----------------------------------------
    'window_name':'<< Sampling Condition >>',
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
                    'item':[{'name':'Software Start','num':cdio.DIODM_START_SOFT},
                            {'name':'External UP','num':cdio.DIODM_START_EXT_RISE},
                            {'name':'External DOWN','num':cdio.DIODM_START_EXT_FALL}],
                    'set_num':0                         # 設定値(何番目の選択肢か)
                    },
                    {'pos_y':2,
                    'set_item_name':'Clock',
                    'item':[{'name':'Internal Clock','num':cdio.DIODM_CLK_CLOCK},
                            {'name':'External Clock','num':cdio.DIODM_CLK_EXT_TRG},
                            {'name':'Hand Shake','num':cdio.DIODM_CLK_HANDSHAKE}],
                    'set_num':0
                    },
                    {'pos_y':3,
                    'set_item_name':'Stop',
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
                  'set_item_name':'Internal Clock',     # 項目名
                  'unit_name':'ns',                     # 単位名
                  'set_num':1000,                       # 設定値
                  'hex_or_dec':TermLib.DEC_NUM          # 何進数か？ HEX_NUM or DEC_NUM
                },
                {'pos_y':1,
                  'set_item_name':'Stop Number',
                  'unit_name':'',
                  'set_num':1000,
                  'hex_or_dec':TermLib.DEC_NUM
                },
                {'pos_y':2,
                  'set_item_name':'Number of Data',
                  'unit_name':'',
                  'set_num':500,
                  'hex_or_dec':TermLib.DEC_NUM
                }]
}


#================================================================
# 転送完了コールバック関数
#================================================================
def stop_callback(dev_id, message, dir, param):
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
# 指定個数転送完了コールバック関数
#================================================================
def count_callback(dev_id, message, dir, param):
    count = ctypes.c_ulong()
    carry = ctypes.c_ulong()
    err_str = ctypes.create_string_buffer(256)

    #----------------------------------------
    # 割り込みメッセージの処理
    #----------------------------------------
    if message == cdio.DIO_DMM_COUNT:
        lret =  cdio.DioDmGetCount(dev_id, cdio.DIODM_DIR_OUT, ctypes.byref(count), ctypes.byref(carry))
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


pstop_callback = cdio.PDIO_STOP_CALLBACK(stop_callback)
pcount_callback = cdio.PDIO_COUNT_CALLBACK(count_callback)


#================================================================
# データファイル作成
#================================================================
def initial_data_file():
    #----------------------------------------
    # ファイルオープン
    #----------------------------------------
    try:
        the_file = open(file_name, 'w')
    except:
        buf = str.format('open : file open error.')
        TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        return 1
    #----------------------------------------
    # データ書き込み
    #----------------------------------------
    for i in range(DATA_SIZE):
        buf = str.format('{0:8d} : {1:08X}\n', i, i)
        the_file.write(buf)
    #----------------------------------------
    # ファイルクローズ
    #----------------------------------------
    the_file.close()
    return 0


#================================================================
# 転送条件設定関数
#================================================================
def condition(dev_id, err_str):
    menu_num = -1
    start = clock = stop = -1
    internal_clock = stop_num = notification = -1
    get_str = ctypes.create_string_buffer(256)
    dir = cdio.DIODM_DIR_OUT
    global is_ring

    #----------------------------------------
    # 設定データ初期化
    #----------------------------------------
    def_set_num = set_scr['select_item'][SET_MENU_START]['set_num']
    start = set_scr['select_item'][SET_MENU_START]['item'][def_set_num]['num']
    def_set_num = set_scr['select_item'][SET_MENU_CLOCK]['set_num']
    clock = set_scr['select_item'][SET_MENU_CLOCK]['item'][def_set_num]['num']
    def_set_num = set_scr['select_item'][SET_MENU_STOP]['set_num']
    stop = set_scr['select_item'][SET_MENU_STOP]['item'][def_set_num]['num']
    internal_clock = set_scr['input_num'][SET_NUM_CLOCK]['set_num']
    stop_num = set_scr['input_num'][SET_NUM_STOP_NUM]['set_num']
    notification = set_scr['input_num'][SET_NUM_NOTIF]['set_num']
    #----------------------------------------
    # 設定ウインドウ初期化
    #----------------------------------------
    lret = TermLib.TermSetWindowOpen(set_scr)
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
            lret, start = TermLib.TermGetSelectItem(set_scr, SET_MENU_START, start)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
        #----------------------------------------
        # クロック条件設定
        #----------------------------------------
        elif menu_num == SET_MENU_CLOCK:
            lret, clock = TermLib.TermGetSelectItem(set_scr, SET_MENU_CLOCK, clock)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
            if clock == cdio.DIODM_CLK_CLOCK:
                lret, internal_clock = TermLib.TermGetInputNum(set_scr, SET_NUM_CLOCK, internal_clock)
                if lret != TermLib.TERM_ERR_SUCCESS:
                    err_str = 'TermGetInputNum ' + str(lret)
        #----------------------------------------
        # ストップ条件設定
        #----------------------------------------
        elif menu_num == SET_MENU_STOP:
            lret, stop = TermLib.TermGetSelectItem(set_scr, SET_MENU_STOP, stop)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
            if stop == cdio.DIODM_STOP_NUM:
                lret, stop_num = TermLib.TermGetInputNum(set_scr, SET_NUM_STOP_NUM, stop_num)
                if lret != TermLib.TERM_ERR_SUCCESS:
                    err_str = 'TermGetInputNum ' + str(lret)
        #----------------------------------------
        # バッファ設定
        #----------------------------------------
        elif menu_num == SET_MENU_BUF_CON:
            lret, is_ring = TermLib.TermGetSelectItem(set_scr, SET_MENU_BUF_CON, is_ring)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetSelectItem ' + str(lret)
        #----------------------------------------
        # 通知カウント設定
        #----------------------------------------
        elif menu_num == SET_MENU_NOTIF:
            lret, notification = TermLib.TermGetInputNum(set_scr, SET_NUM_NOTIF, notification)
            if lret != TermLib.TERM_ERR_SUCCESS:
                err_str = 'TermGetInputNum ' + str(lret)
        #----------------------------------------
        # OK処理
        #----------------------------------------
        elif menu_num == SET_MENU_OK:
            #----------------------------------------
            # Direction
            #----------------------------------------
            lret = cdio.DioDmSetDirection(dev_id, cdio.PO_32)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetDirection ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # StandAlone
            #----------------------------------------
            lret = cdio.DioDmSetStandAlone(dev_id)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetStandAlone ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Start Condition
            #----------------------------------------
            lret = cdio.DioDmSetStartTrg(dev_id, dir, start)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetStartTrg ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Clock Condition
            #----------------------------------------
            lret = cdio.DioDmSetClockTrg(dev_id, dir, clock)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetClockTrg ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Stop Condition
            #----------------------------------------
            lret = cdio.DioDmSetStopTrg(dev_id, dir, stop)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetStopTrg ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # Internal Clock
            #----------------------------------------
            lret = cdio.DioDmSetInternalClock(dev_id, dir, internal_clock, cdio.DIODM_TIM_UNIT_NS)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                err_str = 'DioDmSetInternalClock ' + str(lret) + str(get_str.value.decode('sjis'))
                continue
            #----------------------------------------
            # StopNumber
            #----------------------------------------
            lret = cdio.DioDmSetStopNum(dev_id, dir, stop_num)
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
# メイン関数
#================================================================
def main():
    dio_id = ctypes.c_short()
    dir = cdio.DIODM_DIR_OUT
    count = ctypes.c_ulong()
    carry = ctypes.c_ulong()
    status = ctypes.c_ulong()
    err = ctypes.c_ulong()
    get_str = ctypes.create_string_buffer(256)
    menu_num = -1
    dev_name = ''
    err_str = ''

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
        lret, menu_num = TermLib.TermGetMenuNum('Please input a menu number(0-8)', menu_num)
        if lret != TermLib.TERM_ERR_SUCCESS:
            print('RetCode = {}'.format(lret))
            break
        #----------------------------------------
        # 初期化処理
        #----------------------------------------
        if menu_num == MENU_DIO_OPEN:
            lret, dev_name = TermLib.TermGetStr('Please input a device name.', dev_name)
            if lret != TermLib.TERM_ERR_SUCCESS:
                print('RetCode = {}'.format(lret))
                break
            lret = cdio.DioInit(dev_name.encode(), ctypes.byref(dio_id))
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioInit {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # 設定
        #----------------------------------------
        elif menu_num == MENU_CONDITION:
            lret, err_str = condition(dio_id, err_str)
            if  lret == 1:
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, err_str)
        #----------------------------------------
        # データ設定
        #----------------------------------------
        elif menu_num == MENU_DATA_SET:
            try:
                #----------------------------------------
                # ファイルオープン
                #----------------------------------------
                the_file = open(file_name, 'r')
            except:
                #----------------------------------------
                # データファイルが開けなかったのでデータを作成
                #----------------------------------------
                if initial_data_file() != 0:
                    continue
                try:
                    #----------------------------------------
                    # 作成したデータファイルを開く
                    #----------------------------------------
                    the_file = open(file_name, 'r')
                except:
                    buf = str.format('open : file open error.')
                    TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
                    continue
            #----------------------------------------
            # データをファイルから読み取り
            #----------------------------------------
            i = 0
            for line in the_file:
                data = line.partition(':')[2]
                data.lstrip('')
                data_buff[i] = int(data, 16)
                i += 1
            #----------------------------------------
            # ファイルクローズ
            #----------------------------------------
            the_file.close()
            buf = str.format('{} からデータを設定しました。', file_name)
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # 転送スタート
        #----------------------------------------
        elif menu_num == MENU_START:
            #----------------------------------------
            # Notification
            #----------------------------------------
            lret = cdio.DioDmSetStopEvent(dio_id, dir, pstop_callback, "")
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmSetStopEvent {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
                continue
            notification = set_scr['input_num'][SET_NUM_NOTIF]['set_num']
            lret = cdio.DioDmSetCountEvent(dio_id, dir, notification, pcount_callback, "")
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmSetCountEvent {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
                continue
            #----------------------------------------
            # Reset
            #----------------------------------------
            lret = cdio.DioDmReset(dio_id, cdio.DIODM_RESET_FIFO_IN)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmReset {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
                continue
            #----------------------------------------
            # Set Buffer
            #----------------------------------------
            lret = cdio.DioDmSetBuff(dio_id, dir, ctypes.cast(data_buff, ctypes.POINTER(ctypes.c_ulong)), DATA_SIZE, is_ring)
            if lret != cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, get_str)
                buf = str.format('DioDmSetBuff {}:{}', lret, get_str.value.decode('sjis'))
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
                continue
            #----------------------------------------
            # Start
            #----------------------------------------
            lret = cdio.DioDmStart(dio_id, dir)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioDmStart {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # 転送停止
        #----------------------------------------
        elif menu_num == MENU_STOP:
            lret = cdio.DioDmStop(dio_id, dir)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioDmStop {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # 転送カウント取得
        #----------------------------------------
        elif menu_num == MENU_COUNT:
            lret = cdio.DioDmGetCount(dio_id, dir, ctypes.byref(count), ctypes.byref(carry))
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
            lret = cdio.DioDmGetStatus(dio_id, dir, ctypes.byref(status), ctypes.byref(err))
            if lret == TermLib.TERM_ERR_SUCCESS:
                #----------------------------------------
                # Status
                #----------------------------------------
                buf = ''
                if status.value & cdio.DIODM_STATUS_BMSTOP:    buf += 'BmStop,'
                if status.value & cdio.DIODM_STATUS_PIOSTART:  buf += 'PioStart,'
                if status.value & cdio.DIODM_STATUS_PIOSTOP:   buf += 'PioStop,'
                if status.value & cdio.DIODM_STATUS_TRGIN:     buf += 'TrgIn,'
                if status.value & cdio.DIODM_STATUS_OVERRUN:   buf += 'Overrun'
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_STATUS_POS, buf)
                #----------------------------------------
                # Error
                #----------------------------------------
                buf = ''
                if err.value & cdio.DIODM_STATUS_FIFOEMPTY:    buf += 'FifoEmpty,'
                if err.value & cdio.DIODM_STATUS_FIFOFULL:     buf += 'FifoFull,'
                if err.value & cdio.DIODM_STATUS_SGOVERIN:     buf += 'S/GOverIn,'
                if err.value & cdio.DIODM_STATUS_TRGERR:       buf += 'TrgErr,'
                if err.value & cdio.DIODM_STATUS_CLKERR:       buf += 'ClkErr,'
                if err.value & cdio.DIODM_STATUS_SLAVEHALT:    buf += 'SlaveHalt,'
                if err.value & cdio.DIODM_STATUS_MASTERHALT:   buf += 'MasterHalt'
                TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_ERROR_POS, buf)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioDmGetStatus {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
        #----------------------------------------
        # 終了処理
        #----------------------------------------
        elif menu_num == MENU_DIO_CLOSE:
            lret = cdio.DioExit(dio_id)
            cdio.DioGetErrorString(lret, get_str)
            buf = str.format('DioExit {}:{}', lret, get_str.value.decode('sjis'))
            TermLib.TermSetStatus(TermLib.STATUS_AREA_BOTTOM, STS_RET_POS, buf)
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
