from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QColorDialog
#
from struct import pack
import configparser
import threading
import keyboard
import win32gui
from colorama import init, Fore
init(autoreset=True)
import time
import sys
import re
import os

# cheat stuff
import pymem
import pymem.process
from offsets import *

# Extra windows


Game_Process = "csgo.exe"
Game_Name    = "Counter-Strike: Global Offensive - Direct3D 9"
dev          = "cookie0_o"
v            = "1.0"

min_max_key  = 'INSERT'
current_dir = os.path.dirname(os.path.abspath(__file__))

def f2b(num):
    return ''.join(bin(c).replace('0b', '').rjust(8, '0') for c in pack('!f', num))

# get all states and save it to config\config.ini
def save_config(self, MainWindow):
    # load config.ini
    config = configparser.ConfigParser()
    config.read(current_dir + '\\config\\config.ini')

    # save misc settings
    config['MISC']['RADAR']             = str(self.RADARcheckBox.isChecked())
    config['MISC']['NOFLASH']           = str(self.NOFLASHcheckBox.isChecked())
    config['MISC']['BUNNYHOP']          = str(self.BUNNYHOPcheckBox.isChecked())
    config['MISC']['MONEYREVEAL']       = str(self.MONEYREVEALcheckBox.isChecked())
    config['MISC']['FOVCHANGER']        = str(self.FOVCHANGERcheckBox.isChecked())
    config['MISC']['THIRDPERSON']       = str(self.THIRDPERSONcheckBox.isChecked())
    config['MISC']['TRIGGERBOT']        = str(self.TRIGGERBOTcheckBox.isChecked())
    # values
    config['VALUES']['TRIGGERBOTdelay'] = str(self.TRIGGERBOTdelayRaw.text())
    config['VALUES']['NIGHTMODEvalue']  = str(self.NIGHTMODEvalueRaw.text())
    config['VALUES']['FOV']             = str(self.FOVCHANGERSlider.value())
    # keys
    config['KEYS']['THIRDPERSONkey']    = str(self.THIRDPERSONkeyRaw.text())
    config['KEYS']['TRIGGERBOTkey']     = str(self.TRIGGERBOTkeyRaw.text())
    # ESP
    config['ESP']['ESP']                = str(self.ESPcheckBox.isChecked())
    config['ESP']['AllyESP']            = str(self.AllyESPcheckBox.isChecked())
    config['ESP']['EnemyESP']           = str(self.EnemyESPcheckBox.isChecked())
    config['ESP']['AllyCHAMS']          = str(self.AllyCHAMScheckBox.isChecked())
    config['ESP']['EnemyCHAMS']         = str(self.EnemyCHAMScheckBox.isChecked())
    config['ESP']['LightCHAMS']         = str(self.LightCHAMScheckBox.isChecked())
    # colors
    config['COLORS']['AllyColor']       = (str(self.PickAllyColorButton.palette().button().color().getRgb())).replace(", 255)", ")")
    config['COLORS']['EnemyColor']      = (str(self.PickEnemyColorButton.palette().button().color().getRgb())).replace(", 255)", ")")
    config['COLORS']['AllyChamsColor']  = (str(self.PickAllyColorCHAMSButton.palette().button().color().getRgb())).replace(", 255)", ")")
    config['COLORS']['EnemyChamsColor'] = (str(self.PickEnemyColorCHAMSButton.palette().button().color().getRgb())).replace(", 255)", ")")
    with open(current_dir + "\\config\\config.ini", 'w') as configfile: # save
        config.write(configfile)
    
    return


def load_config(self, MainWindow):
    # load config.ini
    config = configparser.ConfigParser()
    config.read(current_dir + '\\config\\config.ini')

    # load misc settings
    self.RADARcheckBox.setChecked(config.getboolean('MISC', 'RADAR'))
    self.NOFLASHcheckBox.setChecked(config.getboolean('MISC', 'NOFLASH'))
    self.BUNNYHOPcheckBox.setChecked(config.getboolean('MISC', 'BUNNYHOP'))
    self.MONEYREVEALcheckBox.setChecked(config.getboolean('MISC', 'MONEYREVEAL'))
    self.FOVCHANGERcheckBox.setChecked(config.getboolean('MISC', 'FOVCHANGER'))
    self.THIRDPERSONcheckBox.setChecked(config.getboolean('MISC', 'THIRDPERSON'))
    self.TRIGGERBOTcheckBox.setChecked(config.getboolean('MISC', 'TRIGGERBOT'))
    # values
    self.TRIGGERBOTdelayRaw.setText(config.get('VALUES', 'TRIGGERBOTdelay'))
    self.NIGHTMODEvalueRaw.setText(config.get('VALUES', 'NIGHTMODEvalue'))
    self.FOVCHANGERSlider.setValue(config.getint('VALUES', 'FOV'))
    
    # keys
    self.THIRDPERSONkeyRaw.setText(config.get('KEYS', 'THIRDPERSONkey'))
    self.TRIGGERBOTkeyRaw.setText(config.get('KEYS', 'TRIGGERBOTkey'))
    # ESP
    self.ESPcheckBox.setChecked(config.getboolean('ESP', 'ESP'))
    self.AllyESPcheckBox.setChecked(config.getboolean('ESP', 'AllyESP'))
    self.EnemyESPcheckBox.setChecked(config.getboolean('ESP', 'EnemyESP'))
    self.AllyCHAMScheckBox.setChecked(config.getboolean('ESP', 'AllyCHAMS'))
    self.EnemyCHAMScheckBox.setChecked(config.getboolean('ESP', 'EnemyCHAMS'))
    self.LightCHAMScheckBox.setChecked(config.getboolean('ESP', 'LightCHAMS'))
    # colors
    self.PickAllyColorButton.setStyleSheet("background-color: rgb" + str(config.get('COLORS', 'AllyColor')))
    self.PickEnemyColorButton.setStyleSheet("background-color: rgb" + str(config.get('COLORS', 'EnemyColor')))
    self.PickAllyColorCHAMSButton.setStyleSheet("background-color: rgb" + str(config.get('COLORS', 'AllyChamsColor')))
    self.PickEnemyColorCHAMSButton.setStyleSheet("background-color: rgb" + str(config.get('COLORS', 'EnemyChamsColor')))

    return


def ESP(self, MainWindow):
    # csgo dlls
    pm = pymem.Pymem(Game_Process)    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    while True:
        try:
            player = pm.read_int(client + dwLocalPlayer)

            time.sleep(0.0001)
            if self.ESPcheckBox.isChecked():
                glow_manager = pm.read_int(client + dwGlowObjectManager)

                for i in range(1, 64):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)

                    if entity:
                        entity_glow = pm.read_int(entity + m_iGlowIndex)
                        localPlayerTeam = pm.read_int(player + m_iTeamNum)
                        team_id = pm.read_int(entity + m_iTeamNum)
                        if team_id == localPlayerTeam:
                        # ALLY TEAM
                            if self.AllyESPcheckBox.isChecked():
                                # get ally color from pick color button
                                colorA = self.PickAllyColorButton.palette().button().color().getRgb()
                                rA = colorA[0]
                                gA = colorA[1]
                                bA = colorA[2]
                                # set glow color
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(rA))   # R
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(gA))   # G
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(bA))  # B
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(255)) # Alpha
                                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)            # Enable glow  
                            else:
                                pass
                        else:
                        # ENEMY TEAM
                            if self.EnemyESPcheckBox.isChecked():
                                # get ally color from pick color button
                                colorE = self.PickEnemyColorButton.palette().button().color().getRgb()
                                rE = colorE[0]
                                gE = colorE[1]
                                bE = colorE[2]
                                # set glow color
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(rE))   # R
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(gE))   # G
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(bE))  # B
                                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(255)) # Alpha
                                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)            # Enable glow 
                            else:
                                pass
            else:
                pass
        except:
            pass
        finally:
            pass

def RADAR(self, MainWindow):
    # csgo dlls
    pm = pymem.Pymem(Game_Process)
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    while True:
        try:

            time.sleep(0.01)
            if self.RADARcheckBox.isChecked():
                for i in range(1,32):
                    entity=pm.read_int(client+dwEntityList+i*16)
                    if entity:
                        pm.write_uchar(entity+m_bSpotted,1)    
            else:
                time.sleep(0.1)
                pass
        except:
            pass
        finally:
            pass

def NOFLASH(self, MainWindow):
    # csgo dlls
    pm = pymem.Pymem(Game_Process)    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    while True:
        try:
            player = pm.read_int(client + dwLocalPlayer)

            time.sleep(0.01)
            if self.NOFLASHcheckBox.isChecked():
                if player:
                    flash_value=player+m_flFlashMaxAlpha
                    if flash_value:
                        pm.write_float(flash_value,float(0))        

            else:
                pass
        except:
            pass
        finally:
            pass


def FOVCHANGER(self, MainWindow):
    # csgo dlls
    pm = pymem.Pymem(Game_Process)
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    while True:
        try:
            player = pm.read_int(client + dwLocalPlayer)

            time.sleep(0.01)
            if self.FOVCHANGERcheckBox.isChecked():
                value = self.FOVCHANGERSlider.value()
                inputFOV = int(round(value, 0))
                inputFOV = int(round(value, 0))
                fov = player + m_iFOV
                pm.write_int(fov, inputFOV)
            # if not self.FOVCHANGERcheckBox.isChecked(): then reset fov to default value (90)
            else:
                inputFOV = int(round(90, 0))
                inputFOV = int(round(90, 0))
                fov = player + m_iFOV
                pm.write_int(fov, inputFOV)
        except:
            pass
        finally:
            pass

def MONEYREVEAL(self, MainWindow):
    # csgo dlls
    pm = pymem.Pymem(Game_Process)    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    MONEYREVEALON = 0
    MONEYREVEALOFF = 1
    OFF = 0
    while True:
        try:
            client_money_reveal = pymem.process.module_from_name(pm.process_handle, 'client.dll')
            clientModule = pm.read_bytes(client_money_reveal.lpBaseOfDll, client_money_reveal.SizeOfImage)
            address = client_money_reveal.lpBaseOfDll + re.search(rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF', clientModule).start()

            time.sleep(0.01)
            if self.MONEYREVEALcheckBox.isChecked() and MONEYREVEALON == 0:
                pm.write_uchar(address, 0xEB if pm.read_uchar(address) == 0x75 else 0x75)
                MONEYREVEALON = 1
                MONEYREVEALOFF = 0
            if not self.MONEYREVEALcheckBox.isChecked() and MONEYREVEALOFF == 0:
                pm.write_uchar(address, 0x75 if pm.read_uchar(address) == 0xEB else 0xEB)
                MONEYREVEALOFF = 1
                MONEYREVEALON = 0

        except:
            pass
        finally:
            pass

def THIRDPERSON(self, MainWindow):
    # csgo dlls
    pm = pymem.Pymem(Game_Process)    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    THIRDPERSON = 0
    while True:
        try:
            player = pm.read_int(client + dwLocalPlayer)

            time.sleep(0.01)
            # get third person toggle key
            third_person_key = self.THIRDPERSONkeyRaw.text()
            if keyboard.is_pressed(third_person_key) and THIRDPERSON == 0:
                THIRDPERSON = 1
                time.sleep(0.1)
            if keyboard.is_pressed(third_person_key) and THIRDPERSON == 1:
                THIRDPERSON = 0
                time.sleep(0.1)

            if self.THIRDPERSONcheckBox.isChecked() and THIRDPERSON == 1:
                time.sleep(0.1)
                pm.write_int(player + m_iObserverMode, 1)
                fov = player + m_iFOV
                pm.write_int(fov)
            elif self.THIRDPERSONcheckBox.isChecked() and THIRDPERSON == 0:
                time.sleep(0.1)
                pm.write_int(player + m_iObserverMode, 0)
                fov = player + m_iFOV
                pm.write_int(fov)
        except:
            pass
        finally:
            pass

def LIGHTCHAMS(self, MainWindow):
    # csgo dlls
    pm = pymem.Pymem(Game_Process)    
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
    while True:
        try:
            time.sleep(0.01)
            if self.LightCHAMScheckBox.isChecked():
                point = pm.read_int(engine + model_ambient_min - 0x2c)
                yourval = int(f2b(25), 2) ^ point
                pm.write_int(engine + model_ambient_min, yourval)
            else:
                point = pm.read_int(engine + model_ambient_min - 0x2c)
                yourval = int(f2b(0), 2) ^ point
                pm.write_int(engine + model_ambient_min, yourval)
        except:
            pass
        finally:
            pass

def CHAMS(self, MainWindow):
    # csgo dlls
    pm = pymem.Pymem(Game_Process)    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    while True:
        try:
            player = pm.read_int(client + dwLocalPlayer)

            time.sleep(0.01)
            for i in range(1, 64):
                entity = pm.read_int(client + dwEntityList + i * 0x10)
                if entity:
                    localPlayerTeam = pm.read_int(player + m_iTeamNum)
                    team_id = pm.read_int(entity + m_iTeamNum)

                    # chams
                    if team_id == localPlayerTeam:
                        if self.AllyCHAMScheckBox.isChecked()and self.ESPcheckBox.isChecked():
                            colorA = self.PickAllyColorCHAMSButton.palette().button().color().getRgb()
                            rA = colorA[0]
                            gA = colorA[1]
                            bA = colorA[2]
                            pm.write_int(entity + m_clrRender, (rA))
                            pm.write_int(entity + m_clrRender + 0x1, (gA))
                            pm.write_int(entity + m_clrRender + 0x2, (bA))
                        else:
                            pm.write_int(entity + m_clrRender, (255))
                            pm.write_int(entity + m_clrRender + 0x1, (255))
                            pm.write_int(entity + m_clrRender + 0x2, (255))
                    else:
                        if self.EnemyCHAMScheckBox.isChecked() and self.ESPcheckBox.isChecked():
                            colorE = self.PickEnemyColorCHAMSButton.palette().button().color().getRgb()
                            rE = colorE[0]
                            gE = colorE[1]
                            bE = colorE[2]
                            pm.write_int(entity + m_clrRender, (rE))
                            pm.write_int(entity + m_clrRender + 0x1, (gE))
                            pm.write_int(entity + m_clrRender + 0x2, (bE))
                        else:
                            pm.write_int(entity + m_clrRender, (255))
                            pm.write_int(entity + m_clrRender + 0x1, (255))
                            pm.write_int(entity + m_clrRender + 0x2, (255))
        except:
            pass
        finally:
            pass

def BUNNYHOP(self, MainWindow):
    # csgo dlls
    pm = pymem.Pymem(Game_Process)    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    while True:
        try:
            player = pm.read_int(client + dwLocalPlayer)

            time.sleep(0.01)
            if self.BUNNYHOPcheckBox.isChecked():
                if pm.read_int(client+dwLocalPlayer):
                    force_jump=client+dwForceJump
                    on_ground=pm.read_int(player+m_fFlags)
                    velocity=pm.read_float(player+m_vecVelocity)
                    if keyboard.is_pressed('space')and on_ground==257:
                        if velocity<1 and velocity>-1:
                            pass
                        else:
                            pm.write_int(force_jump,5)
                            time.sleep(0.001)
                            pm.write_int(force_jump,4)
            else:
                pass
        except:
            pass
        finally:
            pass

def TRIGGERBOT(self, MainWindow):
    # csgo dlls
    pm = pymem.Pymem(Game_Process)    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    while True:
        try:
            player = pm.read_int(client + dwLocalPlayer)
            entity_id = pm.read_int(player + m_iCrosshairId)     
            entity = pm.read_int(client + dwEntityList + (entity_id - 1) * 0x10)
            entity_team = pm.read_int(entity + m_iTeamNum)
            player_team = pm.read_int(player + m_iTeamNum)

            # get trigger bot hold key
            trigger_bot_hold_key = self.TRIGGERBOTkeyRaw.text()
            # get trigger bot delay
            trigger_bot_delay = self.TRIGGERBOTdelayRaw.text()

            time.sleep(0.01)
            if self.TRIGGERBOTcheckBox.isChecked():
                if keyboard.is_pressed(trigger_bot_hold_key):
                    if entity_id > 0 and entity_id <= 64 and player_team != entity_team:
                        time.sleep(float(trigger_bot_delay))
                        pm.write_int(client + dwForceAttack, 6)
                    else:
                        pass
                else:
                    pass
            else:
                pass
        except:
            pass
        finally:
            pass

def NIGHTMODE(self, MainWindow):
    # csgo dlls
    pm = pymem.Pymem(Game_Process)
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    while True:
        try:
            # get night mode value
            night_mode_value = self.NIGHTMODEvalueRaw.text()

            time.sleep(0.01)
            if self.NIGHTMODEcheckBox.isChecked():
                for i in range(0, 2048):
                    entity = pm.read_uint(client + dwEntityList + i * 0x10)
                    if entity:
                        EntityClassID = pm.read_int(entity + 0x8)
                        a = pm.read_int(EntityClassID + 2 * 0x4)
                        b = pm.read_int(a + 0x1)
                        c = pm.read_int(b + 20)

                        if (c != 69):
                            continue
                        
                        if True:
                            pm.write_int(entity + m_bUseCustomAutoExposureMin, 1)
                            pm.write_int(entity + m_bUseCustomAutoExposureMax, 1)
                            pm.write_float(entity + m_flCustomAutoExposureMin, float(night_mode_value))
                            pm.write_float(entity + m_flCustomAutoExposureMax, float(night_mode_value))
                        else:
                            pm.write_bool(entity + m_bUseCustomAutoExposureMin, 0)
                            pm.write_bool(entity + m_bUseCustomAutoExposureMax, 0)
            else:
                for i in range(0, 2048):
                    entity = pm.read_uint(client + dwEntityList + i * 0x10)
                    if entity:
                        EntityClassID = pm.read_int(entity + 0x8)
                        a = pm.read_int(EntityClassID + 2 * 0x4)
                        b = pm.read_int(a + 0x1)
                        c = pm.read_int(b + 20)

                        if (c != 69):
                            continue
                        
                        if True:
                            pm.write_int(entity + m_bUseCustomAutoExposureMin, 1)
                            pm.write_int(entity + m_bUseCustomAutoExposureMax, 1)
                            pm.write_float(entity + m_flCustomAutoExposureMin, 0.1)
                            pm.write_float(entity + m_flCustomAutoExposureMax, 0.9)
                        else:
                            pm.write_bool(entity + m_bUseCustomAutoExposureMin, 0)
                            pm.write_bool(entity + m_bUseCustomAutoExposureMax, 0)                       
        except:
            pass
        finally:
            pass



def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    

def KEY_listener(MainWindow):
    # print log to cmd
    print (f"{Fore.GREEN}- Key listener started! hide/show window with [{min_max_key}]")
    hide = 0
    while True:
        time.sleep(0.01)
        if keyboard.is_pressed(min_max_key) and hide == 0:
            MainWindow.hide()
            time.sleep(0.1)
            hide = 1
        elif keyboard.is_pressed(min_max_key) and hide == 1:
            MainWindow.show()
            time.sleep(0.1)
            hide = 0


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        # print to cmd "WARNING: QApplication was not created in the main() thread." can be ignored
        print (f"{Fore.GREEN}- (you can ignore this!)")
        print (" ")

        # print log to cmd
        print (f"{Fore.GREEN}- In game window created!")

        #/////////////////////////////////
        #//    Set Window attributes    //
        #/////////////////////////////////
        # get game window position
        hwnd = win32gui.FindWindow(None, Game_Name)
        windowrect = win32gui.GetWindowRect(hwnd)
        x = windowrect[0] - 10
        y = windowrect[1] - 31
        # change position of window
        MainWindow.move(x, y)

        # set window attributes
        MainWindow.setWindowOpacity(0.7)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # MainWindow.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        
        # set size of window
        MainWindow.resize(500, 265)
        # set max min size
        MainWindow.setMaximumSize(500, 265)
        MainWindow.setMinimumSize(500, 265)
        #/////////////////////////////////
        #//             END             //
        #/////////////////////////////////


        #/////////////////////////////////
        #//            WINDOW           //
        #/////////////////////////////////
        self.TitleBar = QtWidgets.QLabel(MainWindow)
        self.TitleBar.setGeometry(QtCore.QRect(0, 0, 501, 16))
        self.TitleBar.setStyleSheet("background-color: rgb(0, 85, 255);")
        self.TitleBar.setText("")
        self.TitleBar.setObjectName("TitleBar")
        self.Title_TitleBar = QtWidgets.QLabel(MainWindow)
        self.Title_TitleBar.setGeometry(QtCore.QRect(5, 0, 161, 16))
        self.Title_TitleBar.setStyleSheet("background-color: rgb(0, 85, 255);")
        self.Title_TitleBar.setObjectName("Title_TitleBar")
        self.ShowHideKey_TitleBar = QtWidgets.QLabel(MainWindow)
        self.ShowHideKey_TitleBar.setGeometry(QtCore.QRect(310, 0, 191, 16))
        self.ShowHideKey_TitleBar.setStyleSheet("background-color: rgb(0, 85, 255);")
        self.ShowHideKey_TitleBar.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ShowHideKey_TitleBar.setObjectName("ShowHideKey_TitleBar")
        self.stackedWidget = QtWidgets.QStackedWidget(MainWindow)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 35, 501, 241))
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.MiscTab = QtWidgets.QWidget()
        self.MiscTab.setObjectName("MiscTab")
        self.NOFLASHcheckBox = QtWidgets.QCheckBox(self.MiscTab)
        self.NOFLASHcheckBox.setGeometry(QtCore.QRect(5, 30, 81, 21))
        self.NOFLASHcheckBox.setStyleSheet("color: rgb(0, 85, 255);")
        self.NOFLASHcheckBox.setObjectName("NOFLASHcheckBox")
        self.RADARcheckBox = QtWidgets.QCheckBox(self.MiscTab)
        self.RADARcheckBox.setGeometry(QtCore.QRect(5, 5, 81, 21))
        self.RADARcheckBox.setStyleSheet("color: rgb(0, 85, 255);")
        self.RADARcheckBox.setObjectName("RADARcheckBox")
        self.FOVCHANGERcheckBox = QtWidgets.QCheckBox(self.MiscTab)
        self.FOVCHANGERcheckBox.setGeometry(QtCore.QRect(330, 5, 90, 20))
        self.FOVCHANGERcheckBox.setStyleSheet("color: rgb(0, 85, 255);")
        self.FOVCHANGERcheckBox.setObjectName("FOVCHANGERcheckBox")
        self.FOVCHANGERSlider = QtWidgets.QSlider(self.MiscTab)
        self.FOVCHANGERSlider.setGeometry(QtCore.QRect(330, 30, 160, 20))
        self.FOVCHANGERSlider.setStyleSheet("QSlider::handle:horizontal {\n"
"    background-color: rgb(65, 65, 65);\n"
"}")
        self.FOVCHANGERSlider.setOrientation(QtCore.Qt.Horizontal)
        self.FOVCHANGERSlider.setObjectName("FOVCHANGERSlider")
        self.MONEYREVEALcheckBox = QtWidgets.QCheckBox(self.MiscTab)
        self.MONEYREVEALcheckBox.setGeometry(QtCore.QRect(5, 80, 101, 21))
        self.MONEYREVEALcheckBox.setStyleSheet("color: rgb(0, 85, 255);")
        self.MONEYREVEALcheckBox.setObjectName("MONEYREVEALcheckBox")
        self.THIRDPERSONcheckBox = QtWidgets.QCheckBox(self.MiscTab)
        self.THIRDPERSONcheckBox.setGeometry(QtCore.QRect(330, 60, 171, 20))
        self.THIRDPERSONcheckBox.setStyleSheet("color: rgb(0, 85, 255);")
        self.THIRDPERSONcheckBox.setObjectName("THIRDPERSONcheckBox")
        self.THIRDPERSONkeyRaw = QtWidgets.QLineEdit(self.MiscTab)
        self.THIRDPERSONkeyRaw.setGeometry(QtCore.QRect(370, 80, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.THIRDPERSONkeyRaw.setFont(font)
        self.THIRDPERSONkeyRaw.setStyleSheet("background-color: rgb(40, 40, 40);\n"
"color: rgb(0, 0, 255);")
        self.THIRDPERSONkeyRaw.setFrame(True)
        self.THIRDPERSONkeyRaw.setAlignment(QtCore.Qt.AlignCenter)
        self.THIRDPERSONkeyRaw.setObjectName("THIRDPERSONkeyRaw")
        self.TRIGGERBOTcheckBox = QtWidgets.QCheckBox(self.MiscTab)
        self.TRIGGERBOTcheckBox.setGeometry(QtCore.QRect(330, 110, 171, 20))
        self.TRIGGERBOTcheckBox.setStyleSheet("color: rgb(0, 85, 255);")
        self.TRIGGERBOTcheckBox.setObjectName("TRIGGERBOTcheckBox")
        self.TRIGGERBOTkeyRaw = QtWidgets.QLineEdit(self.MiscTab)
        self.TRIGGERBOTkeyRaw.setGeometry(QtCore.QRect(370, 130, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.TRIGGERBOTkeyRaw.setFont(font)
        self.TRIGGERBOTkeyRaw.setStyleSheet("background-color: rgb(40, 40, 40);\n"
"color: rgb(0, 0, 255);")
        self.TRIGGERBOTkeyRaw.setFrame(True)
        self.TRIGGERBOTkeyRaw.setAlignment(QtCore.Qt.AlignCenter)
        self.TRIGGERBOTkeyRaw.setObjectName("TRIGGERBOTkeyRaw")
        self.TRIGGERBOTdelayRaw = QtWidgets.QLineEdit(self.MiscTab)
        self.TRIGGERBOTdelayRaw.setGeometry(QtCore.QRect(370, 160, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.TRIGGERBOTdelayRaw.setFont(font)
        self.TRIGGERBOTdelayRaw.setStyleSheet("background-color: rgb(40, 40, 40);\n"
"color: rgb(0, 0, 255);")
        self.TRIGGERBOTdelayRaw.setFrame(True)
        self.TRIGGERBOTdelayRaw.setAlignment(QtCore.Qt.AlignCenter)
        self.TRIGGERBOTdelayRaw.setObjectName("TRIGGERBOTdelayRaw")
        self.label = QtWidgets.QLabel(self.MiscTab)
        self.label.setGeometry(QtCore.QRect(330, 80, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 0, 255);")
        self.label.setObjectName("label")
        self.label_7 = QtWidgets.QLabel(self.MiscTab)
        self.label_7.setGeometry(QtCore.QRect(330, 130, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.MiscTab)
        self.label_8.setGeometry(QtCore.QRect(330, 160, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_8.setObjectName("label_8")
        self.BUNNYHOPcheckBox = QtWidgets.QCheckBox(self.MiscTab)
        self.BUNNYHOPcheckBox.setGeometry(QtCore.QRect(5, 55, 101, 21))
        self.BUNNYHOPcheckBox.setStyleSheet("color: rgb(0, 85, 255);")
        self.BUNNYHOPcheckBox.setObjectName("BUNNYHOPcheckBox")
        self.NIGHTMODEcheckBox = QtWidgets.QCheckBox(self.MiscTab)
        self.NIGHTMODEcheckBox.setGeometry(QtCore.QRect(170, 5, 151, 20))
        self.NIGHTMODEcheckBox.setStyleSheet("color: rgb(0, 85, 255);")
        self.NIGHTMODEcheckBox.setObjectName("NIGHTMODEcheckBox")
        self.label_9 = QtWidgets.QLabel(self.MiscTab)
        self.label_9.setGeometry(QtCore.QRect(167, 30, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_9.setObjectName("label_9")
        self.NIGHTMODEvalueRaw = QtWidgets.QLineEdit(self.MiscTab)
        self.NIGHTMODEvalueRaw.setGeometry(QtCore.QRect(210, 30, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.NIGHTMODEvalueRaw.setFont(font)
        self.NIGHTMODEvalueRaw.setStyleSheet("background-color: rgb(40, 40, 40);\n"
"color: rgb(0, 0, 255);")
        self.NIGHTMODEvalueRaw.setFrame(True)
        self.NIGHTMODEvalueRaw.setAlignment(QtCore.Qt.AlignCenter)
        self.NIGHTMODEvalueRaw.setObjectName("NIGHTMODEvalueRaw")
        self.NOFLASHcheckBox.raise_()
        self.RADARcheckBox.raise_()
        self.FOVCHANGERcheckBox.raise_()
        self.FOVCHANGERSlider.raise_()
        self.MONEYREVEALcheckBox.raise_()
        self.THIRDPERSONcheckBox.raise_()
        self.TRIGGERBOTcheckBox.raise_()
        self.TRIGGERBOTkeyRaw.raise_()
        self.TRIGGERBOTdelayRaw.raise_()
        self.label.raise_()
        self.THIRDPERSONkeyRaw.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.BUNNYHOPcheckBox.raise_()
        self.NIGHTMODEcheckBox.raise_()
        self.label_9.raise_()
        self.NIGHTMODEvalueRaw.raise_()
        self.stackedWidget.addWidget(self.MiscTab)
        self.EspTab = QtWidgets.QWidget()
        self.EspTab.setObjectName("EspTab")
        self.ESPcheckBox = QtWidgets.QCheckBox(self.EspTab)
        self.ESPcheckBox.setGeometry(QtCore.QRect(5, 5, 81, 21))
        self.ESPcheckBox.setStyleSheet("color: rgb(0, 85, 255);")
        self.ESPcheckBox.setObjectName("ESPcheckBox")
        self.AllyESPcheckBox = QtWidgets.QCheckBox(self.EspTab)
        self.AllyESPcheckBox.setGeometry(QtCore.QRect(5, 50, 81, 21))
        self.AllyESPcheckBox.setStyleSheet("color: rgb(0, 0, 255);")
        self.AllyESPcheckBox.setObjectName("AllyESPcheckBox")
        self.line = QtWidgets.QLabel(self.EspTab)
        self.line.setGeometry(QtCore.QRect(-280, 120, 541, 2))
        self.line.setStyleSheet("background-color: rgb(130, 130, 130);")
        self.line.setText("")
        self.line.setObjectName("line")
        self.EnemyESPcheckBox = QtWidgets.QCheckBox(self.EspTab)
        self.EnemyESPcheckBox.setGeometry(QtCore.QRect(150, 50, 81, 21))
        self.EnemyESPcheckBox.setStyleSheet("color: rgb(0, 85, 255);")
        self.EnemyESPcheckBox.setObjectName("EnemyESPcheckBox")
        self.label_2 = QtWidgets.QLabel(self.EspTab)
        self.label_2.setGeometry(QtCore.QRect(-10, 40, 541, 2))
        self.label_2.setStyleSheet("background-color: rgb(130, 130, 130);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.EspTab)
        self.label_3.setGeometry(QtCore.QRect(5, 70, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.EspTab)
        self.label_4.setGeometry(QtCore.QRect(150, 70, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_4.setObjectName("label_4")
        self.PickEnemyColorButton = QtWidgets.QPushButton(self.EspTab)
        self.PickEnemyColorButton.setGeometry(QtCore.QRect(215, 70, 20, 20))
        self.PickEnemyColorButton.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.PickEnemyColorButton.setText("")
        self.PickEnemyColorButton.setObjectName("PickEnemyColorButton")
        self.PickAllyColorButton = QtWidgets.QPushButton(self.EspTab)
        self.PickAllyColorButton.setGeometry(QtCore.QRect(75, 70, 20, 20))
        self.PickAllyColorButton.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.PickAllyColorButton.setText("")
        self.PickAllyColorButton.setObjectName("PickAllyColorButton")
        self.AllyCHAMScheckBox = QtWidgets.QCheckBox(self.EspTab)
        self.AllyCHAMScheckBox.setGeometry(QtCore.QRect(5, 130, 81, 21))
        self.AllyCHAMScheckBox.setStyleSheet("color: rgb(0, 0, 255);")
        self.AllyCHAMScheckBox.setObjectName("AllyCHAMScheckBox")
        self.EnemyCHAMScheckBox = QtWidgets.QCheckBox(self.EspTab)
        self.EnemyCHAMScheckBox.setGeometry(QtCore.QRect(150, 130, 91, 21))
        self.EnemyCHAMScheckBox.setStyleSheet("color: rgb(0, 85, 255);")
        self.EnemyCHAMScheckBox.setObjectName("EnemyCHAMScheckBox")
        self.label_5 = QtWidgets.QLabel(self.EspTab)
        self.label_5.setGeometry(QtCore.QRect(5, 150, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.EspTab)
        self.label_6.setGeometry(QtCore.QRect(150, 150, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_6.setObjectName("label_6")
        self.PickAllyColorCHAMSButton = QtWidgets.QPushButton(self.EspTab)
        self.PickAllyColorCHAMSButton.setGeometry(QtCore.QRect(75, 150, 20, 20))
        self.PickAllyColorCHAMSButton.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.PickAllyColorCHAMSButton.setText("")
        self.PickAllyColorCHAMSButton.setObjectName("PickAllyColorCHAMSButton")
        self.PickEnemyColorCHAMSButton = QtWidgets.QPushButton(self.EspTab)
        self.PickEnemyColorCHAMSButton.setGeometry(QtCore.QRect(215, 150, 20, 20))
        self.PickEnemyColorCHAMSButton.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.PickEnemyColorCHAMSButton.setText("")
        self.PickEnemyColorCHAMSButton.setObjectName("PickEnemyColorCHAMSButton")
        self.label_10 = QtWidgets.QLabel(self.EspTab)
        self.label_10.setGeometry(QtCore.QRect(260, 40, 2, 193))
        self.label_10.setStyleSheet("background-color: rgb(130, 130, 130);")
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.LightCHAMScheckBox = QtWidgets.QCheckBox(self.EspTab)
        self.LightCHAMScheckBox.setGeometry(QtCore.QRect(5, 200, 91, 21))
        self.LightCHAMScheckBox.setStyleSheet("color: rgb(0, 0, 255);")
        self.LightCHAMScheckBox.setObjectName("LightCHAMScheckBox")
        self.stackedWidget.addWidget(self.EspTab)
        self.ConfigTab = QtWidgets.QWidget()
        self.ConfigTab.setObjectName("ConfigTab")
        self.SaveConfigButton = QtWidgets.QPushButton(self.ConfigTab)
        self.SaveConfigButton.setGeometry(QtCore.QRect(5, 5, 75, 23))
        self.SaveConfigButton.setStyleSheet("background-color: rgb(40, 40, 40);")
        self.SaveConfigButton.setObjectName("SaveConfigButton")
        self.LoadConfigButton = QtWidgets.QPushButton(self.ConfigTab)
        self.LoadConfigButton.setGeometry(QtCore.QRect(90, 5, 75, 23))
        self.LoadConfigButton.setStyleSheet("background-color: rgb(40, 40, 40);")
        self.LoadConfigButton.setObjectName("LoadConfigButton")
        self.stackedWidget.addWidget(self.ConfigTab)
        self.MiscTabButton = QtWidgets.QPushButton(MainWindow)
        self.MiscTabButton.setGeometry(QtCore.QRect(0, 15, 51, 21))
        self.MiscTabButton.setStyleSheet("background-color: rgb(40, 40, 40);")
        self.MiscTabButton.setObjectName("MiscTabButton")
        self.EspTabButton = QtWidgets.QPushButton(MainWindow)
        self.EspTabButton.setGeometry(QtCore.QRect(50, 15, 51, 21))
        self.EspTabButton.setStyleSheet("background-color: rgb(40, 40, 40);")
        self.EspTabButton.setObjectName("EspTabButton")
        self.ConfigTabButton = QtWidgets.QPushButton(MainWindow)
        self.ConfigTabButton.setGeometry(QtCore.QRect(100, 15, 51, 21))
        self.ConfigTabButton.setStyleSheet("background-color: rgb(40, 40, 40);")
        self.ConfigTabButton.setObjectName("ConfigTabButton")
        self.MiscTabButton.raise_()
        self.EspTabButton.raise_()
        self.ConfigTabButton.raise_()
        self.stackedWidget.raise_()
        self.TitleBar.raise_()
        self.Title_TitleBar.raise_()
        self.ShowHideKey_TitleBar.raise_()
        #/////////////////////////////////
        self.FOVCHANGERSlider.setValue(90)
        self.FOVCHANGERSlider.setMinimum(20)
        self.FOVCHANGERSlider.setMaximum(150)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #/////////////////////////////////
        #//             END             //
        #/////////////////////////////////

        def pick_color_ally(self, MainWindow):
            # open color picker
            ally_color = QColorDialog.getColor()
            # set style sheet
            self.PickAllyColorButton.setStyleSheet("background-color: rgb(" + str(ally_color.red()) + ", " + str(ally_color.green()) + ", " + str(ally_color.blue()) + ");")

        def pick_color_enemy(self, MainWindow):
            # open color picker
            enemy_color = QColorDialog.getColor()
            # set style sheet
            self.PickEnemyColorButton.setStyleSheet("background-color: rgb(" + str(enemy_color.red()) + ", " + str(enemy_color.green()) + ", " + str(enemy_color.blue()) + ");")

        def pick_color_ally_chams(self, MainWindow):
            # open color picker
            ally_color = QColorDialog.getColor()
            # set style sheet
            self.PickAllyColorCHAMSButton.setStyleSheet("background-color: rgb(" + str(ally_color.red()) + ", " + str(ally_color.green()) + ", " + str(ally_color.blue()) + ");")

        def pick_color_enemy_chams(self, MainWindow):
            # open color picker
            enemy_color = QColorDialog.getColor()
            # set style sheet
            self.PickEnemyColorCHAMSButton.setStyleSheet("background-color: rgb(" + str(enemy_color.red()) + ", " + str(enemy_color.green()) + ", " + str(enemy_color.blue()) + ");")



        #/////////////////////////////////
        #//           THREADS           //
        #/////////////////////////////////
        # define and start key listener thread
        threading.Thread(target=KEY_listener, args=(MainWindow,)).start()

        # ESP thread
        threading.Thread(target=ESP, args=(self, MainWindow)).start()
        # RADAR thread
        threading.Thread(target=RADAR, args=(self, MainWindow)).start()
        # NOFLASH thread
        threading.Thread(target=NOFLASH, args=(self, MainWindow)).start()
        # FOVCHANGER thread
        threading.Thread(target=FOVCHANGER, args=(self, MainWindow)).start()
        # MONEYREVEAL thread
        threading.Thread(target=MONEYREVEAL, args=(self, MainWindow)).start()
        # THIRDPERSON thread
        threading.Thread(target=THIRDPERSON, args=(self, MainWindow)).start()
        # LIGHTCHAMS thread
        threading.Thread(target=LIGHTCHAMS, args=(self, MainWindow)).start()
        # CHAMS thread
        threading.Thread(target=CHAMS, args=(self, MainWindow)).start()
        # BUNNYHOP thread
        threading.Thread(target=BUNNYHOP, args=(self, MainWindow)).start()
        # TRIGGERBOT thread
        threading.Thread(target=TRIGGERBOT, args=(self, MainWindow)).start()
        # NIGHTMODE thread
        threading.Thread(target=NIGHTMODE, args=(self, MainWindow)).start()
        #/////////////////////////////////
        #//             END             //
        #/////////////////////////////////

        #/////////////////////////////////
        #//           BUTTONS           //
        #/////////////////////////////////

        # misc tab button
        self.MiscTabButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        # esp tab button
        self.EspTabButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        # config tab button
        self.ConfigTabButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        # enemy esp color
        self.PickEnemyColorButton.clicked.connect(lambda: pick_color_enemy(self, MainWindow))
        # ally esp color
        self.PickAllyColorButton.clicked.connect(lambda: pick_color_ally(self, MainWindow))

        # enemy chams color
        self.PickEnemyColorCHAMSButton.clicked.connect(lambda: pick_color_enemy_chams(self, MainWindow))
        # ally chams color
        self.PickAllyColorCHAMSButton.clicked.connect(lambda: pick_color_ally_chams(self, MainWindow))

        #/////////////////////////////////
        # save config button
        self.SaveConfigButton.clicked.connect(lambda: save_config(self, MainWindow))

        # load config button
        self.LoadConfigButton.clicked.connect(lambda: load_config(self, MainWindow))

        #/////////////////////////////////
        #//             END             //
        #/////////////////////////////////

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.NOFLASHcheckBox.setText(_translate("MainWindow", "NO FLASH"))
        self.RADARcheckBox.setText(_translate("MainWindow", "RADAR"))
        self.FOVCHANGERcheckBox.setText(_translate("MainWindow", "FOV CHNGER"))
        self.MONEYREVEALcheckBox.setText(_translate("MainWindow", "MONEY REVEAL"))
        self.THIRDPERSONcheckBox.setText(_translate("MainWindow", "THIRD PERSON        [TOGGLE]"))
        self.THIRDPERSONkeyRaw.setText(_translate("MainWindow", "ALT"))
        self.TRIGGERBOTcheckBox.setText(_translate("MainWindow", "TRIGGER BOT              [HOLD]"))
        self.TRIGGERBOTkeyRaw.setText(_translate("MainWindow", "V"))
        self.TRIGGERBOTdelayRaw.setText(_translate("MainWindow", "0.001"))
        self.label.setText(_translate("MainWindow", "key:"))
        self.label_7.setText(_translate("MainWindow", "key:"))
        self.label_8.setText(_translate("MainWindow", "delay:"))
        self.BUNNYHOPcheckBox.setText(_translate("MainWindow", "BUNNYHOP"))
        self.NIGHTMODEcheckBox.setText(_translate("MainWindow", "NIGHTMODE"))
        self.label_9.setText(_translate("MainWindow", "value:"))
        self.NIGHTMODEvalueRaw.setText(_translate("MainWindow", "0.09"))
        self.ESPcheckBox.setText(_translate("MainWindow", " ESP"))
        self.AllyESPcheckBox.setText(_translate("MainWindow", "Ally ESP"))
        self.EnemyESPcheckBox.setText(_translate("MainWindow", "Enemy ESP"))
        self.label_3.setText(_translate("MainWindow", "pick color:"))
        self.label_4.setText(_translate("MainWindow", "pick color:"))
        self.AllyCHAMScheckBox.setText(_translate("MainWindow", "Ally CHAMS"))
        self.EnemyCHAMScheckBox.setText(_translate("MainWindow", "Enemy CHAMS"))
        self.label_5.setText(_translate("MainWindow", "pick color:"))
        self.label_6.setText(_translate("MainWindow", "pick color:"))
        self.LightCHAMScheckBox.setText(_translate("MainWindow", "Light CHAMS"))
        self.SaveConfigButton.setText(_translate("MainWindow", "Save Config"))
        self.LoadConfigButton.setText(_translate("MainWindow", "Load Config"))
        self.MiscTabButton.setText(_translate("MainWindow", "Misc"))
        self.EspTabButton.setText(_translate("MainWindow", "Esp"))
        self.ConfigTabButton.setText(_translate("MainWindow", "Config"))
        #
        MainWindow.setWindowTitle(_translate("MainWindow", "just like otc"))
        self.Title_TitleBar.setText(_translate("MainWindow", f"CS-PRO by[{dev}] - [v{v}]"))
        self.ShowHideKey_TitleBar.setText(_translate("MainWindow", f"\"{min_max_key}\" show/hide key "))


def show_win():
    # print log to cmd
    print (f"{Fore.GREEN}- Creating window...")
    # create window
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# define thread
Window_thread = threading.Thread(target=show_win)

if __name__ == "__main__":
    # clear cmd
    clear()

    # check if csgo is running
    while win32gui.FindWindow(None, Game_Name) == 0:
        print (f"{Fore.RED}- {Game_Name} is not running!", end='\r')
        time.sleep(1)
    else:
        clear()
        print (f"{Fore.GREEN}- {Game_Name} is running!     ")

    # check if in menu
    def IN_MENU():
        try:
            pm = pymem.Pymem(Game_Process)
            x = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll # check if in menu
            pm.read_int(x + dwLocalPlayer)
            print (f"{Fore.GREEN}- In {Game_Name} menu!     ")
            return
        except:
            time.sleep(1)
            print (f"{Fore.RED}- Not in {Game_Name} menu!", end='\r')
            IN_MENU()
    IN_MENU()


    # start thread
    Window_thread.start()
    
