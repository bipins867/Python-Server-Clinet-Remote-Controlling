import os
import myStringLib2 as ms


wfName='Bqkksl_lkf_11234'
def exc(command):

    data=os.popen(command).read()

    return data
def showNetworks():
    command='netsh wlan show networks'
    data=exc(command)
    data=ms.get_all_mid_text(data,'SSID ','\n')
    tdata=[]
    for i in data:
        d=ms.distributeString(i,' : ')
        tdata.append(d[1])
    return tdata

def showProfile():
    command='netsh wlan show profile'
    data=exc(command)
    data=ms.get_all_mid_text(data,'All User Profile     : ','\n')
    return data

def showPartProf(ssid):
    command='netsh wlan show profile {0} key=clear'.format(ssid)
    return exc(command)

def connect(ssid,name=''):
    if(name==''):
        name=ssid
    command='netsh wlan connect ssid="{0}" name="{0}"'.format(ssid,name)

    data=exc(command)

    return data

def exp_profile(name,folder):
    command='netsh wlan export profile {0} folder={1}'.format(name,folder)
    return exc(command)

def exp_profile_c(name,folder):
    command='netsh wlan export profile {0} key=clear folder={1}'.format(name,folder)
    
    return exc(command)

def imp_profile(fileName,interface='Wi-Fi' ,user='current'):

    command='netsh wlan add profile fileName="{0}" interface={1} user={2}'.format(fileName,interface,user)

    return exc(command)

def disconnect():
    command='netsh wlan disconnect'
    return exc(command)

def remove_profile(ssid):
    command='netsh wlan delete profile {0}'.format(ssid)

    return exc(command)


def createProfile(ssid,name,key):
    file='.\WiFi\\f.xml'
    f=open(file,'r')
    data=f.read(1024)
    
    hex_name=name.encode().hex()

    data=ms.replaceBy_String(data,'WIFI_NAME',name)
    data=ms.replaceBy_String(data,'SSID_HEX',hex_name)
    data=ms.replaceBy_String(data,'SSID_NAME',ssid)
    data=ms.replaceBy_String(data,'WIFI_PASSWORDS',key)
    
    tf=open('.\WiFi\\tf.xml','w')
    tf.write(data)
    tf.close()
    f.close()
    return True

def set_net_priority(name,interface='Wi-Fi', priority=1):
    command='netsh wlan set profileorder name={0} interface={1} priority={2}'.format(name,interface,priority)
    return exc(command)

def set_net_mode(name,mode='manual'):
    command='netsh wlan set profileparameter name={0} connectionmode={1}'.format(name,mode)
    return exc(command)



def conn_new_wifi(ssid,name,key):
    p=createProfile(ssid,name,key)
    if(p):
        fileName='.\Wifi\\tf.xml'
        dp=imp_profile(fileName)
        print(dp)
        print(connect(ssid,name))
        return True
    else:
        print("Unable to Create Profile")
        return False


def create_hotspot(ssid,key,mode='allow'):
    command='netsh wlan set hostednetwork mode={0} ssid={1} key={2}'.format(mode,ssid,key)
    return exc(command)

def start_hotspot():
    command='netsh wlan start hostednetwork'
    return exc(command)

def stop_hotspot():
    command='netsh wlan stop hostednetwork'
    return exc(command)

def show_hotspot_prof():
    command='netsh wlan show hostednetwork'
    return exc(command)

def change_hotspot_password(password):
    command='netsh wlan refresh hostednetwork {0}'.format(password)
    return exc(command)


def check_conn():
    command='netsh wlan show interfaces'
    p=exc(command)

    index=p.index("State")
    data=p[index:index+50]
    td=data.index(":")
    data=data[td:td+18]

    if('connected' in data):
        if('disconnected' in data):
            return False
        else:
            return True
    else:
        return False
