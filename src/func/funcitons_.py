def liberar_fun(olt,ont):
    try:
        olt.t.read_until(b"(config)#")
        olt.t.write(str.encode('interface gpon 0/'+str(ont.get_gpon())+ "\n"))
        olt.t.read_until(str.encode("(config-if-gpon-0/"+str(ont.get_gpon())+")#"))
        desc=ont.get_descricao().replace(' ','_')
        if(ont.get_generic()=='0'):
            comando="ont add "+str(ont.get_port())+" "+str(ont.get_id())+" sn-auth "+ont.get_sn()+" omci ont-lineprofile-name GPON ont-srvprofile-name "+ont.get_modelo()+" desc '"+desc+"'\n"
            olt.t.write(str.encode(comando))
            olt.t.write(b"\n")
            native='ont port native-vlan '+str(ont.get_port())+' '+str(ont.get_id())+' eth 1 vlan '+str(ont.get_vlan())+' priority 0 \n'
            olt.t.write(str.encode(native))
        else:
            comando2="ont add "+str(ont.get_port())+" "+str(ont.get_id())+" sn-auth "+ont.get_sn()+" omci ont-lineprofile-name "+olt.get_dic(str(ont.get_vlan()))+" ont-srvprofile-name "+olt.get_dic(str(ont.get_vlan()))+" desc '"+desc+"'\n"
            olt.t.write(str.encode(comando2))
            olt.t.write(b"\n")
            olt.t.write(str.encode('ont port native-vlan '+str(ont.get_port())+' '+str(ont.get_id())+' eth 1 vlan '+str(ont.get_vlan())+' priority 0 \n'))
            olt.t.write(str.encode('ont port native-vlan '+str(ont.get_port())+' '+str(ont.get_id())+' eth 2 vlan '+str(ont.get_vlan())+' priority 0 \n'))
            olt.t.write(str.encode('ont port native-vlan '+str(ont.get_port())+' '+str(ont.get_id())+' eth 3 vlan '+str(ont.get_vlan())+' priority 0 \n'))
            olt.t.write(str.encode('ont port native-vlan '+str(ont.get_port())+' '+str(ont.get_id())+' eth 4 vlan '+str(ont.get_vlan())+' priority 0 \n'))
        olt.t.write(b"quit \n")
    except:
        olt.connect()
        liberar_fun(olt,ont)
def service_port_fun(olt,ont):
    try:
        olt.t.read_until(b"(config)#")
        olt.t.write(str.encode("service-port "+str(ont.get_service_port())+" vlan "+str(ont.get_vlan())+" gpon 0/"+str(ont.get_gpon())+"/"+str(ont.get_port())+" ont "+str(ont.get_id())+" gemport 37 multi-service user-vlan "+str(ont.get_vlan())+" tag-transform translate \n"))
        olt.t.write(b"\n")
    except:
        olt.connect()
        service_port_fun(olt,ont)
def service_port_generic_fun(olt,ont):
    try:
        print("service-port "+str(ont.get_service_port())+" vlan "+str(ont.get_vlan())+" gpon 0/"+str(ont.get_gpon())+"/"+str(ont.get_port())+" ont "+str(ont.get_id())+" gemport 8 multi-service user-vlan "+str(ont.get_vlan())+" tag-transform translate \n")
        olt.t.read_until(b"(config)#")
        olt.t.write(str.encode("service-port "+str(ont.get_service_port())+" vlan "+str(ont.get_vlan())+" gpon 0/"+str(ont.get_gpon())+"/"+str(ont.get_port())+" ont "+str(ont.get_id())+" gemport 8 multi-service user-vlan "+str(ont.get_vlan())+" tag-transform translate \n"))
        olt.t.write(b"\n")
    except:
        olt.connect()
        service_port_generic_fun(olt,ont)
def delete_fun(olt,ont):
    try:
        olt.t.write('interface gpon 0/'+str(ont.get_gpon())+ " \n")
        olt.t.read_until("(config-if-gpon-0/"+str(ont.get_gpon())+")#")
        olt.t.write("ont delete "+ont.get_port()+" "+ont.get_id()+" \n")
        olt.t.write("\n")
        olt.t.write("quit \n")
    except:
        olt.connect()
        delete_fun(olt,ont)
def delet_sn_fun(olt,ont):
    try:
        ont.t.write("undo service-port "+ont.get_service_port()+" \n")
    except:
        ont.connect()
        delet_sn_fun(olt,ont)