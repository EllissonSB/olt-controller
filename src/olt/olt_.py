import telnetlib
from ..bd import bd_
from ..func.funcitons_ import *
class OLTMETA(type):
    _instances={}
    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            instance=super().__call__(*args, **kwds)
            cls._instances[cls]=instance
        return cls._instances[cls]
class OLTSingleton_BJ(metaclass=OLTMETA):
    def __init__(self):
        self._bd=bd_.bridge_bd()
        self.__ip='ip_olt'
        self.__user='user_olt'
        self.__password="password_olt"
        self.__dic_profile={'145':"Generic_V145",'105':'Generic_2_V105'}
        self.__name="name_olt"
        self.__service_port=self._bd.get_service_port_bj()[0][0]+1
        try:
            self.t=telnetlib.Telnet(self.get_ip())
            self.t.read_until(b">>User name:")
            self.t.write(self.get_user().encode('ascii') + b"\n")
            self.t.read_until(b">>User password:")
            self.t.write(self.get_password().encode('ascii') + b"\n")
            self.t.write(b"enable \n")
            self.t.read_until(b"#")
            self.t.write(b"config \n")
        except:
            self.connect()
    def connect(self):
        try:
            self.t=telnetlib.Telnet(self.get_ip())
            self.t.read_until(b">>User name:")
            self.t.write(self.get_user().encode('ascii') + b"\n")
            self.t.read_until(b">>User password:")
            self.t.write(self.get_password().encode('ascii') + b"\n")
            self.t.write(b"enable \n")
            self.t.read_until(b"#")
            self.t.write(b"config \n")
        except:
            self.connect()
    def set_service_port(self):
        self.__service_port+=1
    def get_service_port(self):
        return self.__service_port
    def get_ip(self):
        return self.__ip
    def get_user(self):
        return self.__user
    def get_password(self):
        return self.__password
    def get_dic(self,value):
        return self.__dic_profile[str(value)]
    def get_name(self):
        return self.__name
class OLTSingleton_UMB(metaclass=OLTMETA):
    def __init__(self):
        self.__ip='ip_olt'
        self.__user='user_olt'
        self.__password="password_olt"
        self.__dic_profile={'145':"Generic_V145"}
        self.__name="nmae_olt"
        try:
            self.t=telnetlib.Telnet(self.get_ip())
            self.t.read_until(b">>User name:")
            self.t.write(self.get_user().encode('ascii') + b"\n")
            self.t.read_until(b">>User password:")
            self.t.write(self.get_password().encode('ascii') + b"\n")
            self.t.write(b"enable \n")
            self.t.read_until(b"#")
            self.t.write(b"config \n")
        except:
            self.connect()
    def connect(self):
        try:
            self.t=telnetlib.Telnet(self.get_ip())
            self.t.read_until(b">>User name:")
            self.t.write(self.get_user().encode('ascii') + b"\n")
            self.t.read_until(b">>User password:")
            self.t.write(self.get_password().encode('ascii') + b"\n")
            self.t.write(b"enable \n")
            self.t.read_until(b"#")
            self.t.write(b"config \n")
        except:
            self.connect()
    def get_ip(self):
        return self.__ip
    def get_user(self):
        return self.__user
    def get_password(self):
        return self.__password
    def get_dic(self,value):
        return self.__dic_profile[str(value)]
    def get_name(self):
        return self.__name
class OLTSingleton_MB(metaclass=OLTMETA):
    def __init__(self):
        self.__ip='ip_olt'
        self.__user='user_olt'
        self.__password="password_olt"
        self.__name="name_olt"
        self.__dic_profile={'145':"Generic_V145"}
        try:
            self.t=telnetlib.Telnet(self.get_ip())
            self.t.read_until(b">>User name:")
            self.t.write(self.get_user().encode('ascii') + b"\n")
            self.t.read_until(b">>User password:")
            self.t.write(self.get_password().encode('ascii') + b"\n")
            self.t.write(b"enable \n")
            self.t.read_until(b"#")
            self.t.write(b"config \n")
        except:
            self.connect()
    def connect(self):
        try:
            self.t=telnetlib.Telnet(self.get_ip())
            self.t.read_until(b">>User name:")
            self.t.write(self.get_user().encode('ascii') + b"\n")
            self.t.read_until(b">>User password:")
            self.t.write(self.get_password().encode('ascii') + b"\n")
            self.t.write(b"enable \n")
            self.t.read_until(b"#")
            self.t.write(b"config \n")
        except:
            self.connect()
    def get_ip(self):
        return self.__ip
    def get_user(self):
        return self.__user
    def get_password(self):
        return self.__password
    def get_name(self):
        return self.__name
    def get_dic(self,value):
        return self.__dic_profile[value]
class bridge_olt:
    def liberar(self,olt,ont):
        liberar_fun(olt,ont)
    def service_port(self,olt,ont):
        service_port_fun(olt,ont)
    def service_port_generic(self,olt,ont):
        service_port_generic_fun(olt,ont)
    def delete(self,olt,ont):
        delete_fun(olt,ont)
    def delet_sn(self,olt,ont):
        delet_sn_fun(olt,ont)