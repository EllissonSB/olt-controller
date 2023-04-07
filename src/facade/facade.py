from ..mediator import mediator_
from ..snmp import snmp_
from src.olt import olt_
from src.bd import bd_
class Facade:
    def __init__(self) -> None:
        self._mediator = mediator_.concreteMediator()
        self._snmp_=snmp_.bridge_snmp()
        self._olt=olt_.bridge_olt()
        self._bd=bd_.bridge_bd()
    def liberar(self,ont)->bool:
        return self._mediator.liberar(ont)
    def get_liberadas(self):
        return (self._mediator.get_liberadas())
    def ont_of(self):
        return (self._mediator.ont_of())
    def ont_on_off(self):
        return (self._mediator.ont_on_off())
    def onu_on_all(self):
        return(self._mediator.onu_on_all())
    def onu_auto_find(self):
        return (self._mediator.ont_auto_find())
    def apagar(self,ont):
        return (self._mediator.mover(ont))
    def alterar_vlan(self,ont)->bool:
        return self._mediator.alterar_vlan(ont)
    def mover(self,ont)->bool:
        return self._mediator.mover(ont)
    def status_pon(self,olt,slot,pon):
        return self._snmp_.status_pon(olt,slot,pon)
    def status_pon_all(self,olt):
        return self._snmp_.status_pon_all(olt)
    def onu_on(self,olt,slot,pon,id):
        return self._snmp_.onu_on(olt,slot,pon,id)