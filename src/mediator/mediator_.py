from abc import ABC
from ..olt import olt_
from ..bd import bd_
from ..snmp import snmp_
from ..olt import ont_
from ..func.functions_mediator import *
class Mediator(ABC):
    def liberar(self,onu:object)->bool:
        pass
    def apagar(self,onu:object)->bool:
        pass
    def mover(self,onu:object)->bool:
        pass
    def alterar_vlan(self,onu:object)->bool:
        pass
class concreteMediator(Mediator):
    def __init__(self):
        self._olts=[olt_.OLTSingleton_MB(),olt_.OLTSingleton_UMB(),olt_.OLTSingleton_BJ()]
        self._olt=olt_.bridge_olt()
        self._bd=bd_.bridge_bd()
        self._olt.Mediator=self
        self._bd.Mediator=self
        self._snmp=snmp_.bridge_snmp()
        self._snmps=[snmp_.SNMPSingleton_MB(),snmp_.SNMPSingleton_UB(),snmp_.SNMPSingleton_BJ()]
    def get_olt(self,name):
        for i in range(len(self._olts)):
            if self._olts[i].get_name() ==name:
                return i
    def ont_auto_find(self):
        dic={}
        for i in range(len(self._snmps)):
            dic[self._olts[i].get_name()]=auto_find(self._snmps[i],self._snmp)
        return dic
    def ont_of(self):
        dic={}
        for i in range(len(self._snmps)):
            ret=self._bd.get_liberadas(self._olts[i].get_name())
            dic[self._olts[i].get_name()]=ont_of_fun(self._snmps[i],self._snmp,ret)
        return dic
    def ont_on_off(self):
        dic={}
        for i in range(len(self._snmps)):
            ret=self._bd.get_liberadas(self._olts[i].get_name())
            dic[self._olts[i].get_name()]=ont_on_off_fun(self._snmps[i],self._snmp,ret)
        return dic
    def get_liberadas(self):
        dic={}
        for i in range(len(self._snmps)):
            ret=self._bd.get_liberadas(self._olts[i].get_name())
            dic[self._olts[i].get_name()]=get_liberadas_fun(self._snmps[i],self._snmp,ret)
        return dic
    def liberar(self, ont: object) -> bool:
        ont.set_id((self._bd.get_id(ont)))
        ont.set_service_port(self._bd.get_service_port(ont.get_olt()))
        olt=self._olts[self.get_olt(ont.get_olt())]
        if(olt.get_name()=='bom_jardim'):
            print(olt.get_service_port())
            ont.set_service_port(olt.get_service_port())
            olt.set_service_port()
        print(olt,ont.get_service_port(),ont.get_id())
        liberar_fun(olt,self._olt,ont)
        if(ont.get_generic()=='0'):
            self._olt.service_port(olt,ont)
        else:
            self._olt.service_port_generic(olt,ont)
        self._bd.inserir_onu(ont)
    def apagar(self,ont)->bool:
        olt=self._olts[self.get_olt(ont.get_olt())]
        self._olt.delete(olt,ont)
    def mover(self,ont):
        pass
    def alterar_vlan(self,ont)->bool:
        print('FOO')
    def onu_on_all(self):
        dic={}
        for i in range(len(self._snmps)):
            ret=self._bd.get_on_id_port_all(self._olts[i].get_name())
            dic[self._olts[i].get_name()]=self._snmp.onu_on_all(self._snmps[i],ret)
        return dic