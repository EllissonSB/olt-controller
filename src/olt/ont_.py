class ont:
    def __init__(self):
        self.__sn=''
        self.__gpon=''
        self.__port=''
        self.__descricao=''
        self.__vlan=''
        self.__service_port=''
        self.__id=''
        self.__zone=''
        self.__modelo=''
        self.__number=''
        self.__abrev=''
        self.__generic=0
        self.__status=''
        self.__signal=''
        self.__signal_2=''
        self.__olt=''
    def set_olt(self,value):
        self.__olt=value
    def set_olt_id(self,value):
        self.__olt_id=value
    def set_signal_2(self,value):
        self.__signal_2 = value
    def set_signal(self,value):
        self.__signal=value
    def set_status(self,value):
        self.__status=value
    def set_generic(self, value):
        self.__generic=value
    def set_abrev(self,value):
        self.__abrev = value
    def set_modelo(self,value):
        self.__modelo=value
    def set_number(self,value):
        self.__number=value
    def set_zone(self,value):
        self.__zone=value
    def set_id(self,value):
        self.__id=value
    def set_service_port(self,value):
        self.__service_port=value
    def set_vlan(self,value):
        self.__vlan=value
    def set_sn(self, dado):
        self.__sn=dado
    def set_port(self, dado):
        self.__port=dado
    def set_gpon(self, value):
        self.__gpon=value
    def set_descricao(self,value):
        self.__descricao=value
    def get_olt_id(self):
        return self.__olt_id
    def get_olt(self):
        return self.__olt
    def get_signal_2(self):
        return self.__signal_2
    def get_signal(self):
        return self.__signal
    def get_status(self):
        return self.__status
    def get_generic(self):
        return self.__generic
    def get_abrev(self):
        return self.__abrev
    def get_modelo(self):
        return self.__modelo
    def get_number(self):
        return self.__number
    def get_zone(self):
        return self.__zone
    def get_descricao(self):
        return self.__descricao
    def get_gpon(self):
        return self.__gpon
    def get_port(self):
        return self.__port
    def get_sn(self):
        return self.__sn
    def get_vlan(self):
        return self.__vlan
    def get_service_port(self):
        return self.__service_port
    def get_id(self):
        return self.__id