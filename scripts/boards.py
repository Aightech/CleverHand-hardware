"""Generates the v3 draft KiCad projects (schematic with all parts placed and netted by labels).
Usage: python3 scripts/boards.py [--overwrite] [BOARD ...]
Symbols come from ~/KICAD/kicad_libs/easyeda_library/00_lcsc (downloaded with easyeda2kicad, see docs/v3_parts.md)
and from pcb/config_file/clvhd_stack.kicad_sym. Re-running with --overwrite discards manual edits."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from kicad_gen import *
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBS["clvhd_stack"]=REPO+"/pcb/config_file/clvhd_stack.kicad_sym"
TPRO=REPO+"/pcb/hmi/communication/COM_MOD/COM_MOD.kicad_pro"; TPCB=REPO+"/pcb/hmi/communication/COM_MOD/COM_MOD.kicad_pcb"
P3="P:+3.3V"; G="P:GND"; VB="P:+BATT"; VBUS="P:VBUS"
def g(n): return "G:"+n
LC={"PIC":"C26081950","PCA":"C440032","INV":"C2872975","LED":"C2976072","SW":"C455280","DIO":"C78260","HC32":"C493490","PAK":"C5334557","FPC":"C2856802","HDR":"C51889474","IDC":"C41366809","SH":"C160402","E73":"C356849","CHG":"C424093","GAUGE":"C139621","RS":"C41427589","MIC":"C88419","USBC":"C165948","ESD":"C7519","DAC":"C627341","ESP":"C3013940","XTAL":"C47089401","ANT":"C76585","AP":"C51118","DRV":"C553134"}

COLS=[("GND","A0","SDA_L"),("3V3","A1","SCL_L"),("GND","A2","AUX0"),("CLK","A3","AUX1"),("POCI","A4","AUX2"),("PICO","SDA","AUX3"),("SCLK","SCL","AUX4"),("CSB","STOP_IN","AUX5"),("AREF","STOP_OUT","AUX6"),("VIN","GND","AUX7")]
def _net(name):
    return {"GND":G,"3V3":P3}.get(name, g(name))
def field(role):
    """pin number -> net for the 3x10 stack field; role: master | ctrl | bus | hmi(dict of used names)"""
    nets={}
    for c,col in enumerate(COLS):
        for r,name in enumerate(col):
            n=3*c+r+1
            if role=="master": nets[str(n)]=_net(name)
            elif role=="ctrl":
                nets[str(n)]={"STOP_IN":"NC","SDA_L":g("SDA"),"SCL_L":g("SCL"),"VIN":VB}.get(name,_net(name))
            elif role=="bus":
                nets[str(n)]="NC" if name in ("CSB","SDA_L","SCL_L","AUX4","AUX5","AUX6","AUX7") else ("VIN_TP" if name=="VIN" else _net(name))
            else:
                nets[str(n)]=role.get(name,"NC")
    return nets
# v2 cable order (18-way FPC pin -> net); STOP handled per connector
CABLE={"1":g("AUX0"),"2":P3,"3":G,"4":g("AUX2"),"5":g("A0"),"6":g("A1"),"7":g("A2"),"8":g("A3"),"9":g("A4"),"10":g("POCI"),"11":g("PICO"),"12":g("SCLK"),"14":g("AUX3"),"15":g("SDA"),"16":g("SCL"),"17":g("AUX1"),"18":g("AREF"),"19":G,"20":G}

def bridge_block(s,x,y,sda_l="SDA_L",scl_l="SCL_L"):
    s.text("I2C bridge: shared SDA/SCL <-> node-local segment, enabled while CSB is low",x-20,y-22,1.8)
    s.part("U","00_lcsc","PCA9306DQER",x,y,{"1":G,"2":P3,"3":g("SCL"),"4":g("SDA"),"5":g(sda_l),"6":g(scl_l),"7":"VREF2","8":"BR_EN"},lcsc=LC["PCA"])
    s.part("U","00_lcsc","SN74LVC1G04DPWR",x,y+30,{"5":P3,"3":G,"2":g("CSB"),"4":"BR_EN","1":"NC"},lcsc=LC["INV"])
    s.passive("R","200k",x+40,y,P3,"VREF2"); s.passive("C","100nF",x+50,y,P3,G)
    s.passive("R","10k",x+40,y+30,P3,g(sda_l)); s.passive("R","10k",x+50,y+30,P3,g(scl_l)); s.passive("C","100nF",x+60,y+30,P3,G)
def led_block(s,x,y,din="LED_DI"):
    s.part("D","00_lcsc","WS2812C-2020-V1",x,y,{"4":P3,"2":G,"3":din,"1":"NC"},lcsc=LC["LED"])
    s.passive("C","100nF",x+22,y,P3,G)
def drdy_diode(s,x,y):
    s.text("optional wired-OR: node AUX4 (DRDY# by convention) -> bus AUX0 (anode AUX0, cathode AUX4)",x-15,y-10,1.5)
    s.part("D","00_lcsc","BAT54SWT1G",x,y,{"1":g("AUX0"),"3":g("AUX4"),"2":"NC"},lcsc=LC["DIO"])
def button(s,x,y,net,pullup=True):
    s.part("SW","00_lcsc","TS-1088R-02026",x,y,{"1":net,"2":G},lcsc=LC["SW"])
    if pullup: s.passive("R","10k",x+15,y-10,P3,net)
def tp(s,x,y,net,fp="TestPoint:TestPoint_Pad_1.0x1.0mm"):
    s.part("TP","Connector","TestPoint",x,y,{"1":net},value=net.replace("G:",""),footprint=fp,stub=1.27)
def stack_field(s,x,y,role,note):
    s.text(note,x-30,y-65,1.8)
    s.part("J","clvhd_stack","CLVHD_STACK_3x10",x,y,field(role),footprint="clvhd_stack:CLVHD_STACK_3x10",value="STACK 3x10")
def pwr_flags(s,x,y):
    pass

# ============ COM_MOD_PIC ============
def com_mod_pic():
    s=Sheet("COM_MOD_PIC","COM_MOD_PIC - v3 communication module A (PIC16F13145 CLB)")
    s.text("PIC16F13145: CLB compares A0..A4 with CLBSWIN -> CSB (RC5). STOP chain on RB4/RB5. MSSP I2C client on RB6/RB7. LED on RA2. ICSP on RA0/RA1/MCLR. AUX4..7 (node-local, e.g. DRDY#/START/EN/INT by convention) on RC7/RA4/RA5/RC6.",20,20,1.8)
    s.part("U","00_lcsc","PIC16F13145T-I_REB",90,90,{
        "1":"MCLR","2":g("CSB"),"3":g("A4"),"4":g("A3"),"5":g("AUX7"),"6":g("AUX4"),"7":g("SDA"),"8":g("SCL"),"9":g("STOP_OUT"),"10":g("STOP_IN"),
        "11":g("A2"),"12":g("A1"),"13":g("A0"),"14":"LED_DI","15":"ICSPCLK","16":"ICSPDAT","17":G,"18":P3,"19":g("AUX6"),"20":g("AUX5"),"21":G},lcsc=LC["PIC"])
    s.passive("C","100nF",150,80,P3,G); s.passive("C","1uF",160,80,P3,G)
    s.passive("R","10k",150,110,P3,"MCLR"); s.passive("R","10k",160,110,P3,g("CSB")); s.passive("R","10k",170,110,P3,g("AUX6"))
    tp(s,190,80,"ICSPDAT"); tp(s,200,80,"ICSPCLK"); tp(s,210,80,"MCLR")
    button(s,150,140,"MCLR",False)
    bridge_block(s,90,180)
    led_block(s,200,180); drdy_diode(s,250,180)
    stack_field(s,320,110,"master","3x10 stack field: row A = v2 row, row B = bus side (read), row C = local I2C + AUX (driven / read)")
    s.flag("+3.3V",20,250); s.flag("GND",30,250); s.text("power flags: 3V3 and GND come from the bus",15,245,1.3)
    return s
# ============ COM_MOD_PAK ============
def com_mod_pak():
    s=Sheet("COM_MOD_PAK","COM_MOD_PAK - v3 communication module B (HC32L110 + SLG46826)")
    s.text("HC32L110C6UA QFN-20 (CSP-16 rejected: inner balls not routable with JLC rules). v2 pinout kept: SDA P35, SCL P36, STOP_IN P31 (=SWCLK), STOP_OUT P02, LED P01. Freed ADD pins: P34/P33 = private I2C to the GreenPAK, P03/P15/P14/P32 = AUX4..7 (node-local), P23 user button.",20,20,1.8)
    s.part("U","00_lcsc","HC32L110C6UA-SFN20TR",90,100,{
        "1":"RESETB","2":"LED_DI","3":g("STOP_OUT"),"4":G,"5":"VCAP","6":P3,"7":g("AUX4"),"8":g("AUX5"),"9":g("AUX6"),"10":"BTN",
        "11":"NC","12":"NC","13":"NC","14":"SWDIO","15":g("STOP_IN"),"16":g("AUX7"),"17":"PAK_SDA","18":"PAK_SCL","19":g("SDA"),"20":g("SCL"),"21":G},lcsc=LC["HC32"])
    s.passive("C","100nF",150,70,P3,G); s.passive("C","1uF",160,70,P3,G); s.passive("C","1uF",170,70,"VCAP",G)
    s.passive("R","10k",150,100,P3,"RESETB"); s.passive("R","10k",160,100,P3,g("CSB")); s.passive("R","10k",170,100,P3,g("AUX6"))
    s.passive("R","4.7k",150,130,P3,"PAK_SDA"); s.passive("R","4.7k",160,130,P3,"PAK_SCL")
    tp(s,190,70,"SWDIO"); tp(s,200,70,"G:STOP_IN"); tp(s,210,70,"RESETB")
    s.text("SWCLK is shared with STOP_IN as in v2",185,62,1.3)
    button(s,150,160,"RESETB",False); button(s,190,160,"BTN")
    s.text("SLG46826: IO0..IO4 = A0..A4, IO5 = CSB (LUT compare written over PAK_SDA/PAK_SCL at enumeration)",20,215,1.8)
    s.part("U","00_lcsc","SLG46826V_C5334557",70,250,{"1":P3,"14":P3,"11":G,"8":"PAK_SCL","9":"PAK_SDA","2":g("A0"),"3":g("A1"),"4":g("A2"),"5":g("A3"),"6":g("A4"),"7":g("CSB"),
        "10":"NC","12":"NC","13":"NC","15":"NC","16":"NC","17":"NC","18":"NC","19":"NC","20":"NC"},lcsc=LC["PAK"])
    s.passive("C","100nF",110,240,P3,G)
    bridge_block(s,180,250)
    led_block(s,300,200); drdy_diode(s,340,200)
    stack_field(s,330,110,"master","3x10 stack field: row A = v2 row, row B = bus side (read), row C = local I2C + AUX")
    s.flag("+3.3V",20,300); s.flag("GND",30,300); s.text("power flags: 3V3 and GND come from the bus",15,295,1.3)
    return s
# ============ BUS_FPC ============
def bus_fpc():
    s=Sheet("BUS_FPC","BUS_FPC - passive bus board, two 18-way FPC (v2 cable pinout)")
    s.text("IN connector: pin k = v2 cable pin k. OUT connector is pin-reversed (pin k = cable pin 19-k). STOP: IN -> STOP_IN, OUT <- STOP_OUT.",20,20,1.8)
    nin=dict(CABLE); nin["13"]=g("STOP_IN")
    s.part("J","00_lcsc","FPC-05F-18PH20",60,110,nin,lcsc=LC["FPC"],value="FPC IN")
    nout={}
    for k in range(1,19):
        src=str(19-k); nout[str(k)]=g("STOP_OUT") if src=="13" else CABLE[src]
    nout["19"]=G; nout["20"]=G
    s.part("J","00_lcsc","FPC-05F-18PH20",140,110,nout,lcsc=LC["FPC"],value="FPC OUT")
    stack_field(s,250,110,"bus","3x10 stack field on top of a COM module or CTRL node: rows A+B and AUX0..3 connected, row C local lines left open")
    tp(s,60,180,"VIN_TP"); tp(s,90,180,"G:STOP_IN"); tp(s,105,180,"G:STOP_OUT")
    s.text("VIN: not on the v2 cable; test pad only (a v3 cable could reuse the AUX3 conductor)",50,190,1.3)
    s.passive("C","100nF",140,180,P3,G)
    s.flag("+3.3V",20,200); s.flag("GND",30,200)
    return s
# ============ BUS_IDC ============
def bus_idc():
    s=Sheet("BUS_IDC","BUS_IDC - passive bus board, one mid-ribbon 2x9 IDC tap + STOP neighbour link")
    s.text("Ribbon conductor k = v2 cable pin k (2x9 IDC: pin k = conductor k). Conductor 13 (STOP) is not used on the ribbon; STOP goes through J2 to the neighbours.",20,20,1.8)
    s.text("J1 placeholder: generic 2x09 1.27 mm header footprint; replace by the shrouded part (BXCONN / XUNPU 2x9 1.27 mm) once chosen.",20,26,1.5)
    nid={str(k):CABLE[str(k)] for k in range(1,19) if k!=13}; nid["13"]="NC"
    s.part("J","Connector_Generic","Conn_02x09_Odd_Even",70,110,nid,value="IDC 2x9 1.27",footprint="Connector_PinHeader_1.27mm:PinHeader_2x09_P1.27mm_Vertical_SMD")
    s.part("J","00_lcsc","SM02B-SRSS-TB(LF)(SN)",150,110,{"1":g("STOP_IN"),"2":g("STOP_OUT"),"3":G,"4":G},lcsc=LC["SH"],value="STOP link")
    s.text("STOP link: pin1 = STOP_IN (from previous node), pin2 = STOP_OUT (to next node); crossed 2-wire cable",120,125,1.3)
    stack_field(s,250,110,"bus","3x10 stack field: rows A+B and AUX0..3 connected, row C local lines left open")
    tp(s,60,180,"VIN_TP")
    s.passive("C","100nF",140,180,P3,G)
    s.flag("+3.3V",20,200); s.flag("GND",30,200)
    return s
# ============ common controller blocks ============
def usb_block(s,x,y):
    s.text("USB-C (USB 2.0 device): CC pull-downs 5.1k, ESD on D+/D-",x-20,y-30,1.8)
    s.part("J","00_lcsc","TYPE-C-31-M-12",x,y,{"A1B12":G,"B1A12":G,"A4B9":VBUS,"B4A9":VBUS,"A5":"CC1","B5":"CC2","A6":"USB_DP","B6":"USB_DP","A7":"USB_DN","B7":"USB_DN","A8":"NC","B8":"NC","1":G,"2":G,"3":G,"4":G},lcsc=LC["USBC"])
    s.passive("R","5.1k",x+30,y+20,"CC1",G); s.passive("R","5.1k",x+40,y+20,"CC2",G)
    s.part("U","00_lcsc","USBLC6-2SC6",x+70,y,{"1":"USB_DN","6":"D-","3":"USB_DP","4":"D+","2":G,"5":VBUS},lcsc=LC["ESD"])
    s.passive("C","4.7uF",x+100,y,VBUS,G,size="0402")
def battery_block(s,x,y,ldo):
    s.text("LiPo: MCP73831 charger (PROG 4.7k ~ 210 mA), BQ27421 gauge (low-side 10 mR sense), 3V3 LDO from VBAT",x-20,y-30,1.8)
    s.part("U","00_lcsc","MCP73831T-2ACI_OT",x,y,{"4":VBUS,"2":G,"3":VB,"5":"PROG","1":"CHG_STAT"},lcsc=LC["CHG"])
    s.passive("R","4.7k",x+25,y+12,"PROG",G); s.passive("C","4.7uF",x+35,y+12,VB,G,size="0402")
    s.part("U","00_lcsc","BQ27421YZFR-G1A",x+80,y,{"C3":VB,"C2":"BAT_N","B3":"GAUGE_VDD","B1":"GAUGE_BIN","A1":"NC","A2":g("SDA"),"A3":g("SCL"),"B2":G,"C1":G},lcsc=LC["GAUGE"])
    s.passive("C","1uF",x+110,y+12,"GAUGE_VDD",G); s.passive("R","10k",x+120,y+12,"GAUGE_BIN",G); s.passive("C","100nF",x+130,y+12,VB,G)
    s.part("R","00_lcsc","HOJLR0805-1_2W-10MR-1%",x+150,y,{"1":"BAT_N","2":G},lcsc=LC["RS"],value="10mR")
    s.part("J","00_lcsc","SM02B-SRSS-TB(LF)(SN)",x+180,y,{"1":VB,"2":"BAT_N","3":G,"4":G},lcsc=LC["SH"],value="BATTERY")
    if ldo=="MIC":
        s.part("U","00_lcsc","MIC5504-3.3YM5-TR",x+40,y+45,{"1":VB,"3":VB,"2":G,"5":P3,"4":"NC"},lcsc=LC["MIC"])
    else:
        s.part("U","00_lcsc","AP2112K-3.3TRG1",x+40,y+45,{"1":VB,"3":VB,"2":G,"5":P3,"4":"NC"},lcsc=LC["AP"])
    s.passive("C","1uF",x+70,y+45,VB,G); s.passive("C","1uF",x+80,y+45,P3,G); s.passive("C","10uF",x+90,y+45,P3,G,size="0402")
def dac_block(s,x,y):
    s.text("AREF DAC (optional): VOUTA -> AREF",x-10,y-20,1.5)
    s.part("U","00_lcsc","MCP4728A0T-E_UN",x,y,{"1":P3,"10":G,"2":g("SCL"),"3":g("SDA"),"4":G,"5":"NC","6":g("AREF"),"7":"NC","8":"NC","9":"NC"},lcsc=LC["DAC"])
    s.passive("C","100nF",x+30,y,P3,G)
# ============ CTRL_NRF52840 ============
def ctrl_nrf():
    s=Sheet("CTRL_NRF52840","CTRL_NRF52840 - nRF52840 controller node (E73-2G4M08S1C)")
    s.text("E73-2G4M08S1C: VDH tied to VCC (normal voltage mode), VBS = VBUS for USB detect. Mono node or chain head; SDA_L/SCL_L strapped to SDA/SCL (no bridge).",20,20,1.8)
    s.part("U","00_lcsc","E73-2G4M08S1C",80,90,{
        "19":P3,"23":P3,"5":G,"21":G,"24":G,"25":"NC","27":VBUS,"29":"D-","31":"D+","26":"RESET","37":"SWDIO","39":"SWCLK","41":"NC","43":"NC",
        "32":g("SCLK"),"34":g("PICO"),"35":g("POCI"),"36":g("CSB"),"38":"NC","40":g("A0"),"42":g("A1"),"17":g("A2"),"2":g("A3"),"1":g("A4"),
        "6":g("STOP_OUT"),"12":g("SDA"),"14":g("SCL"),"22":g("AUX4"),"16":g("AUX7"),"3":g("AUX5"),"20":g("AUX6"),"28":"LED_DI","30":"BTN","4":g("AUX0"),"8":g("AUX1"),"9":g("AUX2"),"10":g("AUX3"),"33":g("CLK"),"15":"CHG_STAT",
        "7":"NC","11":"NC","13":"NC","18":"NC"},lcsc=LC["E73"])
    s.passive("C","100nF",150,60,P3,G); s.passive("C","10uF",160,60,P3,G,size="0402")
    button(s,150,90,"RESET"); button(s,190,90,"BTN")
    tp(s,150,120,"SWDIO"); tp(s,160,120,"SWCLK"); tp(s,170,120,"RESET")
    led_block(s,150,150)
    usb_block(s,60,210)
    battery_block(s,200,210,"MIC")
    dac_block(s,60,270)
    stack_field(s,330,90,"ctrl","3x10 stack field, CTRL: drives row B (STOP_IN unused), SDA_L/SCL_L strapped to SDA/SCL, VIN = battery, AUX0..3 on ADC pins, AUX4..7 on GPIO")
    s.flag("VBUS",20,250); s.flag("+BATT",30,250); s.flag("GND",40,250); s.flag("+3.3V",50,250)
    return s
# ============ CTRL_ESP32S3 ============
def ctrl_esp():
    s=Sheet("CTRL_ESP32S3","CTRL_ESP32S3 - ESP32-S3FH4R2 controller node (chip-down)")
    s.text("ESP32-S3FH4R2 chip-down: 40 MHz crystal, TDK chip antenna with pi-match (values TBD at tuning), native USB on GPIO19/20. Mono node or chain head; SDA_L/SCL_L strapped.",20,20,1.8)
    s.part("U","00_lcsc","ESP32-S3FH4R2",80,110,{
        "2":P3,"3":P3,"20":P3,"46":P3,"55":P3,"56":P3,"29":P3,"57":G,"4":"CHIP_PU","5":"GPIO0","1":"LNA_IN","53":"XTAL_N","54":"XTAL_P","25":"D-","26":"D+","49":"U0TXD","50":"U0RXD",
        "17":g("SCLK"),"16":g("PICO"),"18":g("POCI"),"15":g("CSB"),"14":g("AUX7"),"9":g("A0"),"10":g("A1"),"11":g("A2"),"12":g("A3"),"13":g("A4"),"19":g("STOP_OUT"),
        "6":g("SDA"),"7":g("SCL"),"8":g("AUX4"),"23":g("AUX7"),"24":g("AUX5"),"27":g("AUX6"),"43":"LED_DI","38":"BTN","39":g("AUX0"),"40":g("AUX1"),"41":g("AUX2"),"42":g("CLK"),"44":"CHG_STAT","45":g("AUX3"),
        "21":"NC","22":"NC","28":"NC","30":"NC","31":"NC","32":"NC","33":"NC","34":"NC","35":"NC","36":"NC","37":"NC","47":"NC","48":"NC","51":"NC","52":"NC"},lcsc=LC["ESP"])
    s.passive("C","10uF",150,60,P3,G,size="0402"); s.passive("C","100nF",160,60,P3,G); s.passive("C","100nF",170,60,P3,G); s.passive("C","100nF",180,60,P3,G); s.passive("C","1uF",190,60,P3,G)
    s.text("CHIP_PU: 10k pull-up + 1uF (RC reset), reset button. GPIO0: 10k pull-up + boot button.",150,80,1.3)
    s.passive("R","10k",150,95,P3,"CHIP_PU"); s.passive("C","1uF",160,95,"CHIP_PU",G); button(s,175,95,"CHIP_PU",False)
    s.passive("R","10k",150,125,P3,"GPIO0"); button(s,175,125,"GPIO0",False); button(s,215,125,"BTN")
    s.part("Y","00_lcsc","40MHZ_3225_12PF_10PPM",150,160,{"1":"XTAL_P","3":"XTAL_N","2":G,"4":G},lcsc=LC["XTAL"],value="40MHz 12pF")
    s.passive("C","12pF",170,160,"XTAL_P",G); s.passive("C","12pF",180,160,"XTAL_N",G)
    s.text("RF: LNA_IN -> C -> L -> ANT with shunt C (pi-match, values TBD)",150,185,1.3)
    s.passive("C","TBD",150,200,"LNA_IN",G); s.passive("L","TBD",160,195,"LNA_IN","ANT",size="0402"); s.passive("C","TBD",170,200,"ANT",G)
    s.part("ANT","00_lcsc","ANT016008LCS2442MA1",200,200,{"4":"ANT","1":"NC","2":"NC","3":"NC","5":"NC","6":"NC"},lcsc=LC["ANT"])
    tp(s,150,235,"U0TXD"); tp(s,160,235,"U0RXD")
    led_block(s,190,235)
    usb_block(s,60,260)
    battery_block(s,200,260,"AP")
    dac_block(s,60,320)
    stack_field(s,330,90,"ctrl","3x10 stack field, CTRL: drives row B (STOP_IN unused), SDA_L/SCL_L strapped to SDA/SCL, VIN = battery, AUX0..3 / AUX4..7 on GPIO")
    s.flag("VBUS",20,250); s.flag("+BATT",30,250); s.flag("GND",40,250); s.flag("+3.3V",50,250)
    return s
# ============ VIB_DRV2625 ============
def vib_drv():
    s=Sheet("VIB_DRV2625","VIB_DRV2625 - haptic submodule (H-i2c profile)")
    s.text("DRV2625 on the node-local I2C (SDA_L/SCL_L, addr 0x5A). NRST on AUX6 (EN by convention), TRIG/INTZ on AUX7. Motor from 3V3; VIN available on the field for a higher-power variant.",20,20,1.8)
    s.part("U","00_lcsc","DRV2625YFFR",80,90,{"C2":P3,"B3":G,"A2":"REG","C3":"OUT-","A3":"OUT+","B1":g("SDA_L"),"C1":g("SCL_L"),"A1":g("AUX7"),"B2":g("AUX6")},lcsc=LC["DRV"])
    s.passive("C","1uF",130,80,"REG",G); s.passive("C","1uF",140,80,P3,G); s.passive("C","10uF",150,80,P3,G,size="0402")
    s.part("J","00_lcsc","SM02B-SRSS-TB(LF)(SN)",80,140,{"1":"OUT+","2":"OUT-","3":G,"4":G},lcsc=LC["SH"],value="MOTOR")
    stack_field(s,250,110,{"GND":G,"3V3":P3,"SDA_L":g("SDA_L"),"SCL_L":g("SCL_L"),"AUX6":g("AUX6"),"AUX7":g("AUX7")},"3x10 stack field, H-i2c: populate row A power pins, C1/C2 (local I2C), C7/C8 (AUX6/AUX7); other positions unpopulated")
    s.flag("+3.3V",20,200); s.flag("GND",30,200)
    return s

BOARDS=[("pcb/hmi/communication/COM_MOD_PIC",com_mod_pic,"../../../config_file"),
        ("pcb/hmi/communication/COM_MOD_PAK",com_mod_pak,"../../../config_file"),
        ("pcb/hmi/communication/BUS_FPC",bus_fpc,"../../../config_file"),
        ("pcb/hmi/communication/BUS_IDC",bus_idc,"../../../config_file"),
        ("pcb/controller/node/CTRL_NRF52840",ctrl_nrf,"../../../config_file"),
        ("pcb/controller/node/CTRL_ESP32S3",ctrl_esp,"../../../config_file"),
        ("pcb/hmi/submodule/feedback/VIB_DRV2625",vib_drv,"../../../../config_file")]
if __name__=="__main__":
    only=[a for a in sys.argv[1:] if not a.startswith("--")]
    for d,fn,rel in BOARDS:
        name=os.path.basename(d)
        if only and name not in only: continue
        full=os.path.join(REPO,d)
        if os.path.exists(os.path.join(full,name+".kicad_sch")) and "--overwrite" not in sys.argv:
            print("exists, skip",name); continue
        sh=fn()
        write_project(full,name,sh,TPRO,TPCB,libtables=rel)
        sh.write(os.path.join(full,name+".kicad_sch"))
        print("generated",name,"symbols:",len(sh.libsyms))
