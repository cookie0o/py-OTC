import requests, re, math
from math import sqrt, pi, atan

r = requests.get("https://raw.githubusercontent.com/JokinAce/CSGO-Offsets/master/csgo.hpp")
r = r.text


offsets = ["dwEntityList", "dwLocalPlayer","m_flFlashMaxAlpha", "m_iTeamNum", "dwGlowObjectManager", "m_iGlowIndex", "dwForceJump", "m_fFlags", "dwForceAttack", "m_iCrosshairId", "m_bSpotted", "m_iShotsFired", "m_aimPunchAngle", "dwClientState", "dwClientState_ViewAngles","m_iObserverMode","m_bIsDefusing","m_bGunGameImmunity","m_iHealth","m_dwBoneMatrix","m_vecOrigin","m_vecViewOffset","m_bDormant","dwbSendPackets","dwInput","clientstate_last_outgoing_command","clientstate_net_channel"]


d = {}
offs = []
for i in range(len(offsets)):
    if offsets[i] in r:
        search = re.findall(str(offsets[i]) + '\s'"= (.*);", r)
        offs += search


import requests, json, sys, os



import os
dirname = os.path.dirname(__file__)
classes_file = os.path.join(dirname, 'classes/netvars.json')
n = open(classes_file, "r")

response = json.load(n)

m_totalHitsOnServer = int(response["DT_CSPlayer"]["m_totalHitsOnServer"])
m_iViewModelIndex = int(response["DT_BaseCombatWeapon"]["m_iViewModelIndex"])
m_nModelIndex = int(response["DT_BaseViewModel"]["m_nModelIndex"])
m_hViewModel = int(response["DT_BasePlayer"]["m_hViewModel[0]"])

url = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(url).json()

cs_gamerules_data = int(response["netvars"]["cs_gamerules_data"])

m_ArmorValue = int(response["netvars"]["m_ArmorValue"])
m_Collision = int(response["netvars"]["m_Collision"])
m_CollisionGroup = int(response["netvars"]["m_CollisionGroup"])
m_Local = int(response["netvars"]["m_Local"])
m_MoveType = int(response["netvars"]["m_MoveType"])
m_OriginalOwnerXuidHigh = int(response["netvars"]["m_OriginalOwnerXuidHigh"])
m_OriginalOwnerXuidLow = int(response["netvars"]["m_OriginalOwnerXuidLow"])
m_SurvivalGameRuleDecisionTypes = int(response["netvars"]["m_SurvivalGameRuleDecisionTypes"])
m_SurvivalRules = int(response["netvars"]["m_SurvivalRules"])
m_aimPunchAngleVel = int(response["netvars"]["m_aimPunchAngleVel"])
m_aimPunchAngle = int(response["netvars"]["m_aimPunchAngle"])
m_angEyeAnglesX = int(response["netvars"]["m_angEyeAnglesX"])
m_angEyeAnglesY = int(response["netvars"]["m_angEyeAnglesY"])
m_bBombPlanted = int(response["netvars"]["m_bBombPlanted"])
m_bFreezePeriod = int(response["netvars"]["m_bFreezePeriod"])
m_bGunGameImmunity = int(response["netvars"]["m_bGunGameImmunity"])
m_bHasDefuser = int(response["netvars"]["m_bHasDefuser"])
m_bHasHelmet = int(response["netvars"]["m_bHasHelmet"])
m_bInReload = int(response["netvars"]["m_bInReload"])
m_bIsDefusing = int(response["netvars"]["m_bIsDefusing"])
m_bIsQueuedMatchmaking = int(response["netvars"]["m_bIsQueuedMatchmaking"])
m_bIsScoped = int(response["netvars"]["m_bIsScoped"])
m_bIsValveDS = int(response["netvars"]["m_bIsValveDS"])
m_bSpotted = int(response["netvars"]["m_bSpotted"])
m_bSpottedByMask = int(response["netvars"]["m_bSpottedByMask"])
m_bStartedArming = int(response["netvars"]["m_bStartedArming"])
m_bUseCustomAutoExposureMax = int(response["netvars"]["m_bUseCustomAutoExposureMax"])
m_bUseCustomAutoExposureMin = int(response["netvars"]["m_bUseCustomAutoExposureMin"])
m_bUseCustomBloomScale = int(response["netvars"]["m_bUseCustomBloomScale"])
m_clrRender = int(response["netvars"]["m_clrRender"])
m_dwBoneMatrix = int(response["netvars"]["m_dwBoneMatrix"])
m_fAccuracyPenalty = int(response["netvars"]["m_fAccuracyPenalty"])
m_fFlags = int(response["netvars"]["m_fFlags"])
m_flC4Blow = int(response["netvars"]["m_flC4Blow"])
m_flCustomAutoExposureMax = int(response["netvars"]["m_flCustomAutoExposureMax"])
m_flCustomAutoExposureMin = int(response["netvars"]["m_flCustomAutoExposureMin"])
m_flCustomBloomScale = int(response["netvars"]["m_flCustomBloomScale"])
m_flDefuseCountDown = int(response["netvars"]["m_flDefuseCountDown"])
m_flDefuseLength = int(response["netvars"]["m_flDefuseLength"])
m_flFallbackWear = int(response["netvars"]["m_flFallbackWear"])
m_flFlashDuration = int(response["netvars"]["m_flFlashDuration"])
m_flFlashMaxAlpha = int(response["netvars"]["m_flFlashMaxAlpha"])
m_flLastBoneSetupTime = int(response["netvars"]["m_flLastBoneSetupTime"])
m_flLowerBodyYawTarget = int(response["netvars"]["m_flLowerBodyYawTarget"])
m_flNextAttack = int(response["netvars"]["m_flNextAttack"])
m_flNextPrimaryAttack = int(response["netvars"]["m_flNextPrimaryAttack"])
m_flSimulationTime = int(response["netvars"]["m_flSimulationTime"])
m_flTimerLength = int(response["netvars"]["m_flTimerLength"])
m_hActiveWeapon = int(response["netvars"]["m_hActiveWeapon"])
m_hMyWeapons = int(response["netvars"]["m_hMyWeapons"])
m_hObserverTarget = int(response["netvars"]["m_hObserverTarget"])
m_hOwner = int(response["netvars"]["m_hOwner"])
m_hOwnerEntity = int(response["netvars"]["m_hOwnerEntity"])
m_iAccountID = int(response["netvars"]["m_iAccountID"])
m_iClip1 = int(response["netvars"]["m_iClip1"])
m_iCompetitiveRanking = int(response["netvars"]["m_iCompetitiveRanking"])
m_iCompetitiveWins = int(response["netvars"]["m_iCompetitiveWins"])
m_iCrosshairId = int(response["netvars"]["m_iCrosshairId"])
m_iEntityQuality = int(response["netvars"]["m_iEntityQuality"])
m_iFOV = int(response["netvars"]["m_iDefaultFOV"])
m_iFOVStart = int(response["netvars"]["m_iFOVStart"])
m_iGlowIndex = int(response["netvars"]["m_iGlowIndex"])
m_iHealth = int(response["netvars"]["m_iHealth"])
m_iItemDefinitionIndex = int(response["netvars"]["m_iItemDefinitionIndex"])
m_iItemIDHigh = int(response["netvars"]["m_iItemIDHigh"])
m_iMostRecentModelBoneCounter = int(response["netvars"]["m_iMostRecentModelBoneCounter"])
m_iObserverMode = int(response["netvars"]["m_iObserverMode"])
m_iShotsFired = int(response["netvars"]["m_iShotsFired"])
m_iState = int(response["netvars"]["m_iState"])
m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
m_lifeState = int(response["netvars"]["m_lifeState"])
m_nFallbackPaintKit = int(response["netvars"]["m_nFallbackPaintKit"])
m_nFallbackSeed = int(response["netvars"]["m_nFallbackSeed"])
m_nFallbackStatTrak = int(response["netvars"]["m_nFallbackStatTrak"])
m_nForceBone = int(response["netvars"]["m_nForceBone"])
m_nTickBase = int(response["netvars"]["m_nTickBase"])
m_rgflCoordinateFrame = int(response["netvars"]["m_rgflCoordinateFrame"])
m_szCustomName = int(response["netvars"]["m_szCustomName"])
m_szLastPlaceName = int(response["netvars"]["m_szLastPlaceName"])
m_thirdPersonViewAngles = int(response["netvars"]["m_thirdPersonViewAngles"])
m_vecOrigin = int(response["netvars"]["m_vecOrigin"])
m_vecVelocity = int(response["netvars"]["m_vecVelocity"])
m_vecViewOffset = int(response["netvars"]["m_vecViewOffset"])
m_viewPunchAngle = int(response["netvars"]["m_viewPunchAngle"])

anim_overlays = int(response["signatures"]["anim_overlays"])
clientstate_choked_commands = int(response["signatures"]["clientstate_choked_commands"])
clientstate_delta_ticks = int(response["signatures"]["clientstate_delta_ticks"])
clientstate_last_outgoing_command = int(response["signatures"]["clientstate_last_outgoing_command"])
clientstate_net_channel = int(response["signatures"]["clientstate_net_channel"])
convar_name_hash_table = int(response["signatures"]["convar_name_hash_table"])
dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
dwClientState = int(response["signatures"]["dwClientState"])
dwClientState_GetLocalPlayer = int(response["signatures"]["dwClientState_GetLocalPlayer"])
dwClientState_IsHLTV = int(response["signatures"]["dwClientState_IsHLTV"])
dwClientState_Map = int(response["signatures"]["dwClientState_Map"])
dwClientState_MapDirectory = int(response["signatures"]["dwClientState_MapDirectory"])
dwClientState_MaxPlayer = int(response["signatures"]["dwClientState_MaxPlayer"])
dwClientState_PlayerInfo = int(response["signatures"]["dwClientState_PlayerInfo"])
dwClientState_State = int(response["signatures"]["dwClientState_State"])
dwClientState_ViewAngles = int(response["signatures"]["dwClientState_ViewAngles"])
dwEntityList = int(response["signatures"]["dwEntityList"])
dwForceAttack = int(response["signatures"]["dwForceAttack"])
dwForceAttack2 = int(response["signatures"]["dwForceAttack2"])
dwForceBackward = int(response["signatures"]["dwForceBackward"])
dwForceForward = int(response["signatures"]["dwForceForward"])
dwForceJump = int(response["signatures"]["dwForceJump"])
dwForceLeft = int(response["signatures"]["dwForceLeft"])
dwForceRight = int(response["signatures"]["dwForceRight"])
dwGameDir = int(response["signatures"]["dwGameDir"])
dwGameRulesProxy = int(response["signatures"]["dwGameRulesProxy"])
dwGetAllClasses = int(response["signatures"]["dwGetAllClasses"])
dwGlobalVars = int(response["signatures"]["dwGlobalVars"])
dwGlowObjectManager = int(response["signatures"]["dwGlowObjectManager"])
dwInput = int(response["signatures"]["dwInput"])
dwInterfaceLinkList = int(response["signatures"]["dwInterfaceLinkList"])
dwMouseEnable = int(response["signatures"]["dwMouseEnable"])
dwMouseEnablePtr = int(response["signatures"]["dwMouseEnablePtr"])
dwPlayerResource = int(response["signatures"]["dwPlayerResource"])
dwSensitivity = int(response["signatures"]["dwSensitivity"])
dwSensitivityPtr = int(response["signatures"]["dwSensitivityPtr"])
dwRadarBase = int(response["signatures"]["dwRadarBase"])
dwSetClanTag = int(response["signatures"]["dwSetClanTag"])
dwViewMatrix = int(response["signatures"]["dwViewMatrix"])
dwWeaponTable = int(response["signatures"]["dwWeaponTable"])
dwWeaponTableIndex = int(response["signatures"]["dwWeaponTableIndex"])
dwYawPtr = int(response["signatures"]["dwYawPtr"])
dwZoomSensitivityRatioPtr = int(response["signatures"]["dwZoomSensitivityRatioPtr"])
dwbSendPackets = int(response["signatures"]["dwbSendPackets"])
dwppDirect3DDevice9 = int(response["signatures"]["dwppDirect3DDevice9"])
find_hud_element = int(response["signatures"]["find_hud_element"])
force_update_spectator_glow = int(response["signatures"]["force_update_spectator_glow"])
interface_engine_cvar = int(response["signatures"]["interface_engine_cvar"])
is_c4_owner = int(response["signatures"]["is_c4_owner"])
m_bDormant = int(response["signatures"]["m_bDormant"])
m_flSpawnTime = int(response["signatures"]["m_flSpawnTime"])
m_pStudioHdr = int(response["signatures"]["m_pStudioHdr"])
m_pitchClassPtr = int(response["signatures"]["m_pitchClassPtr"])
m_yawClassPtr = int(response["signatures"]["m_yawClassPtr"])
model_ambient_min = int(response["signatures"]["model_ambient_min"])
set_abs_angles = int(response["signatures"]["set_abs_angles"])
set_abs_origin = int(response["signatures"]["set_abs_origin"])


def normalizeAngles(viewAngleX, viewAngleY):
    if viewAngleX > 89:
        viewAngleX -= 360
    if viewAngleX < -89:
        viewAngleX += 360
    if viewAngleY > 180:
        viewAngleY -= 360
    if viewAngleY < -180:
        viewAngleY += 360
    return viewAngleX, viewAngleY

def checkangles(x, y):
    if x > 89:
        return False
    elif x < -89:
        return False
    elif y > 360:
        return False
    elif y < -360:
        return False
    else:
        return True

def nanchecker(first, second):
    if math.isnan(first) or math.isnan(second):
        return False
    else:
        return True

def calc_distance(current_x, current_y, new_x, new_y):
    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    if distancex < 0.0:
        distancex = -distancex
 
    distancey = new_y - current_y
    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    if distancey < 0.0:
        distancey = -distancey
    return distancex, distancey

def calcangle(localpos1, localpos2, localpos3, enemypos1, enemypos2, enemypos3):
    try:
        delta_x = localpos1 - enemypos1
        delta_y = localpos2 - enemypos2
        delta_z = localpos3 - enemypos3
        hyp = sqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z)
        x = atan(delta_z / hyp) * 180 / pi
        y = atan(delta_y / delta_x) * 180 / pi
        if delta_x >= 0.0:
            y += 180.0
        return x, y
    except:
        pass