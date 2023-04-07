oids=[
['4194304000','4194304256','4194304512','4194304768','4194305024','4194305280','4194305536','4194305792','4194306048','4194306304','4194306560','4194306816','4194307072','4194307328','4194307584','4194307840'],
['4194312192','4194312448','4194312704','4194312960','4194313216','4194313472','4194313728','4194313984','4194314240','4194314496','4194314752','4194315008','4194315264','4194315520','4194315776','4194316032'],
['4194320384','4194320640','4194320896','4194321152','4194321408','4194321664','4194321920','4194322176','4194322432','4194322688','4194322944','4194323200','4194323456','4194323712','4194323968','4194324224'],
['4194328576','4194328832','4194329088','4194329344','4194329600','4194329856','4194330112','4194330368','4194330624','4194330880','4194331136','4194331392','4194331648','4194331904','4194332160','4194332416'],
['4194336768','4194337024','4194337280','4194337536','4194337792','4194338048','4194338304','4194338560','4194338816','4194339072','4194339328','4194339584','4194339840','4194340096','4194340352','4194340608'],
['4194344960','4194345216','4194345472','4194345728','4194345984','4194346240','4194346496','4194346752','4194347008','4194347264','4194347520','4194347776','4194348032','4194348288','4194348544','4194348800'],
['4194353152','4194353408','4194353664','4194353920','4194354176','4194354432','4194354688','4194354944','4194355200','4194355456','4194355712','4194355968','4194356224','4194356480','4194356736','4194356992'],
['4194361344','4194361600','4194361856','4194362112','4194362368','4194362624','4194362880','4194363136','4194363392','4194363648','4194363904','4194364160','4194364416','4194364672','4194364928','4194365184']]
from ..func.functions_snmp import *
class SNMPMeta(type):
    _instances={}
    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            instance=super().__call__(*args, **kwds)
            cls._instances[cls]=instance
        return cls._instances[cls]
class SNMPSingleton_MB(metaclass=SNMPMeta):
    def __init__(self) -> None:
        self.__ip='10.100.8.2'
        self.__community='VUG7HZcC4L2a'
        self.__name="manibu"
    def get_ip(self):
        return self.__ip
    def get_community(self):
        return self.__community
    def get_name(self):
        return self.__name
class SNMPSingleton_BJ(metaclass=SNMPMeta):
    def __init__(self) -> None:
        self.__ip='10.100.6.2'
        self.__community='VUG7HZcC4L2a'
        self.__name="bom_jardim"
    def get_name(self):
        return self.__name
    def get_ip(self):
        return self.__ip
    def get_community(self):
        return self.__community
class SNMPSingleton_UB(metaclass=SNMPMeta):
    def __init__(self) -> None:
        self.__ip='10.100.5.2'
        self.__community='ZROdja6ueSJF'
        self.__name="umbuzeiro"
    def get_name(self):
        return self.__name
    def get_ip(self):
        return self.__ip
    def get_community(self):
        return self.__community
class bridge_snmp:
    def status_pon(self,olt,slot,pon):
        return get_dados(olt,['1.3.6.1.4.1.2011.6.128.1.1.2.21.1.10.'+oids[slot][pon]])[0]['1.3.6.1.4.1.2011.6.128.1.1.2.21.1.10.'+oids[slot][pon]]
    def status_pon_all(self,olt):
        l=[]
        for i in oids:
            for j in i:
                if(functions_snmp.get_dados(olt,['1.3.6.1.4.1.2011.6.128.1.1.2.21.1.10.'+j])[0]['1.3.6.1.4.1.2011.6.128.1.1.2.21.1.10.'+j]!=""):
                    l.append(functions_snmp.get_dados(olt,['1.3.6.1.4.1.2011.6.128.1.1.2.21.1.10.'+j])[0]['1.3.6.1.4.1.2011.6.128.1.1.2.21.1.10.'+j])
                else:
                    return l
        return l
    def onu_on(self,olt,slot,pon,id):
        return get_dados(olt,['1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15.'+oids[slot][pon]+'.'+str(id)])[0]['1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15.'+oids[slot][pon]+'.'+str(id)]
    def onu_on_all(self,olt,ret):
        lista=[]
        for l in range(len(ret)):
            lista.append(get_dados(olt,['1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15.'+oids[ret[l][2]][ret[l][1]]+'.'+str(ret[l][0])])[0]['1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15.'+oids[ret[l][2]][ret[l][1]]+'.'+str(ret[l][0])])
        return lista
    def onu_get_signal(self,olt,slot,pon,id):
        return get_dados(olt,['1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4.'+oids[slot][pon]+'.'+str(id)])[0]['1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4.'+oids[slot][pon]+'.'+str(id)]
    def onu_get_tx(self,olt,slot,pon,id):
        return get_dados(olt,['1.3.6.1.4.1.2011.6.128.1.1.2.51.1.6.'+oids[slot][pon]+'.'+str(id)])[0]['1.3.6.1.4.1.2011.6.128.1.1.2.51.1.6.'+oids[slot][pon]+'.'+str(id)]
    def get_modelo_ont(self,olt):
        return get_dados(olt,['1.3.6.1.4.1.2011.6.128.1.1.2.48.1.2.4194315264.0'])
    def ont_auto_find(self,olt,slot,pon,id):
        return get_auto_find(olt,'1.3.6.1.4.1.2011.6.128.1.1.2.48.1.2.'+oids[slot][pon]+'.'+str(id)).upper()
    def ont_modelo(self,olt,slot,pon,id):
        return get_dados(olt,["1.3.6.1.4.1.2011.6.128.1.1.2.48.1.7."+oids[slot][pon]+'.'+str(id)])[0]["1.3.6.1.4.1.2011.6.128.1.1.2.48.1.7."+oids[slot][pon]+'.'+str(id)]
