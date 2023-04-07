import mysql.connector
from mysql.connector import Error
def verify_connection(lista:list):
    for i in lista:
        if 'olt2' in i:
            return True
class BDMeta(type):
    _instances={}
    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            instance=super().__call__(*args, **kwds)
            cls._instances[cls]=instance
        return cls._instances[cls]
class BDSingleton(metaclass=BDMeta):
    def __init__(self):
        try:
            self.__connection = mysql.connector.connect(host='localhost',database='',user='user',password='password')
            if self.__connection.is_connected():
                self.__cursor = self.__connection.cursor()
        except Error as e:
            print("Error while connecting to MySQL", e)
        #self.create_database()
    def commit(self,command,dado):
        try:
            self.__cursor.execute(command,dado)
            self.__connection.commit()
        except:
            self.connect()
            self.commit(command,dado)
    def execute(self,comand):
        try:
            self.__cursor.execute(comand)
        except Error as e:
            print(e)
            self.connect()
            self.execute(comand)
        return(self.__cursor.fetchall())
    def create_database(self):
        if(verify_connection(self.execute('show databases;'))):
            return True
        else:
            self.execute("create database olt2;")
            self.execute("use olt2;")
            self.execute("CREATE TABLE IF NOT EXISTS `oltma5680` (`id` int(10) NOT NULL AUTO_INCREMENT,  `ont_id` int(10) NOT NULL,  `gpon_port` int(3) NOT NULL,`gpon_interface` int(3) NOT NULL,`zone` varchar(50) NOT NULL,`name` varchar(100) NOT NULL,`service_port` int(10) NOT NULL,`ont_sn` varchar(50) NOT NULL,`vlan` int(10) NOT NULL,PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;")
            self.execute("CREATE TABLE IF NOT EXISTS `usuarios` (`id` int(3) NOT NULL AUTO_INCREMENT,`user` varchar(20) NOT NULL,`password` varchar(20) NOT NULL,`privilegio` int(2) NOT NULL,`nome` varchar(50) NOT NULL,PRIMARY KEY (`id`)) ENGINE=MyISAM DEFAULT CHARSET=utf8;")
            self.execute("INSERT INTO `usuarios` (`id`, `user`, `password`, `privilegio`, `nome`) VALUES (NULL, 'ellisson', '12345', '10', 'Ellisson Barbosa');")
            self.execute("COMMIT;")
    def connect(self):
       self.__connection.connect()
       self.__cursor = self.__connection.cursor()
class bridge_bd(BDSingleton):
    #olt/onts
    def inserir_onu(self,ont):
        string=("INSERT INTO `olt2`.`"+ont.get_olt()+"`" "(ont_id, gpon_port, gpon_interface, zone, name, service_port, ont_sn, vlan, Modelo, Generic)" "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        dados=(ont.get_id(),ont.get_port(),ont.get_gpon(),ont.get_zone(),ont. get_descricao(),ont.get_service_port(),ont.get_sn(),ont.get_vlan(),ont.get_modelo(),ont.get_generic())
        self.commit(string,dados)
    def remover_ont(self,ont):
        self.execute(";")
    def alterar_ont(self,ont):
        self.execute(";")
    def get_ont_sn(self,sn):
        return self.execute("select * FROM olt WHERE sn="+sn+";")
    def get_on_id_port_all(self,olt):
        return self.execute("SELECT ont_id,gpon_port,gpon_interface FROM `olt2`.`"+olt+"`;")
    def get_on_port_all(self,olt):
        return self.execute("SELECT gpon_port,gpon_interface FROM `olt2`.`"+olt+"`;")
    def get_id(self,ont):
        board=ont.get_gpon()
        port=ont.get_port()
        comand="select ont_id from `olt2`.`"+ont.get_olt()+"` where gpon_interface='"+str(board)+"' and gpon_port='"+str(port)+"';"
        saida=self.execute(comand)
        saida=sorted(saida)
        if len(saida) == 0:
            return 0
        else:
            for j  in range (len(saida)):
                if saida[j][0]!=j:
                    return j
        return len(saida)
    def get_service_port(self,olt):
        c=self.execute("select service_port from `olt2`.`"+olt+"`;")
        if len(c)==0:
            return 0
        else:
            for j in range (len(c)):
                if c[j][0]!=j:
                    print(j)
                    return j
        return len(c)
    def get_liberadas(self,olt):
        a="select * from `olt2`.`"+olt+"` order by id desc;"
        return self.execute(a)

    #user
    def inserir_user(self,user):
        self.execute(";")
    def remover_user(self,user):
        self.execute(";")
    def alterar_user(self,user):
        self.execute(";")
    def get_user(self,user,password):
        return (self.execute("SELECT COUNT(*) FROM `olt2`.`usuarios` WHERE `user` ='" +user+"' AND `password` = '"+password+"';")[0][0])
    #gerencia_datas
    def get_datas(self):
        a= self.execute("select * from `olt2`.`datas` order by id desc;")
        if(len(a)<5):
            return a
        else: return a[:5]
    def set_datas(self,datas):
        quantidade=self.execute("select quantidade from `olt2`.`data` where data="+datas+";")
        if(len(quantidade)==0):
             string=("INSERT INTO `olt2`.`datas`" "(data,quantidade)" "VALUES(%s, %s)")
             values=(datas,1)
             self.commit(string,values)
        else:
            quantidade=int(quantidade[0])
            quantidade+=1
            id=self.execute("select id from `olt2`.`datas` where data="+datas+";")
            string=("UPDATE `olt2`.`datas` SET quantidade='%s' WHERE id='%s';")
            values=(quantidade,id)
            self.commit(string,values)
    def get_on_dias(self):
        dados=self.execute('select * from `olt2`.`onoff` order by id desc;')
        if(len(dados)<5):
            return dados
        return dados[:5]
    def set_on_dias(self,data,on,off):
        string=("INSERT INTO `olt2`.`onoff`" "data,quantidade_on,quantidade_off" "VALUES(%s, %s,%s)")
        dados=(data,on,off)
        self.commit(string,dados)
    def get_service_port_bj(self):
        return self.execute('select service_port from `olt2`.`bom_jardim` order by service_port desc limit 1;')