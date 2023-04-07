from ..olt.ont_ import ont as ont_
def auto_find(snmp,facade):
    arr=[]
    for j in range(16):
        f=0
        l=0
        while(f==0):
            a=facade.ont_auto_find(snmp,1,j,l)
            if "NO SUCH" in a:
                f=1
            elif (l==5):
                f=1
            else:
                arr.append(ont_())
                z=len(arr)
                arr[z-1].set_sn(a[2:])
                arr[z-1].set_gpon(str(1))
                arr[z-1].set_port(str(j))
                arr[z-1].set_number(str(z))
                arr[z-1].set_modelo(facade.ont_modelo(snmp,1,j,l))
                arr[z-1].set_olt(snmp.get_name())
                abrev=a[2:10]
                abrev=bytes.fromhex(abrev).decode('utf-8')
                arr[z-1].set_abrev(abrev+"-"+a[10:])
                l+=1
    return arr
def ont_of_fun(snmp,facade,ret):
        off=[]
        for i in range(len(ret)):
            a=set_off(snmp,facade,ret[i])
            if a==0:
                pass
            else:
                off.append(a)
        return off
def ont_on_off_fun(snmp,facade,on_off):
        volt=[0,0]
        for i in range(len(on_off)):
            b=on_off_set(snmp,facade,on_off[i])
            if b==1:
                volt[0]+=1
            else:
                volt[1]+=1
        return volt
def on_off_set(snmp,facade,ret):
        dado=(ont_())
        #dado.set_modelo(ret[9])
        #dado.set_sn(ret[7])
        #dado.set_vlan(ret[8])
        dado.set_id(ret[1])
        dado.set_port(ret[2])
        dado.set_gpon(ret[3])
        #dado.set_zone(ret[4])
        #dado.set_descricao(ret[5])
        #dado.set_service_port(ret[6])
        #dado.set_generic(ret[10])
        #dado.set_status(facade.onu_on(snmp,dado.get_gpon(),dado.get_port(),dado.get_id()))
        if(facade.onu_on(snmp,dado.get_gpon(),dado.get_port(),dado.get_id()))==1:
            return 1
        else:
            return 0
def get_liberadas_fun(snmp,facade,ret):
        volt=[]
        for i in range(len(ret)):
            a=set_ont(snmp,facade,ret[i])
            volt.append(a)
        return volt
def set_ont(snmp,facade,ret):
        dado=(ont_())
        dado.set_modelo(ret[9])
        dado.set_sn(ret[7])
        dado.set_vlan(ret[8])
        dado.set_id(ret[1])
        dado.set_port(ret[2])
        dado.set_gpon(ret[3])
        dado.set_zone(ret[4])
        dado.set_descricao(ret[5])
        dado.set_service_port(ret[6])
        dado.set_generic(ret[10])
        dado.set_status(facade.onu_on(snmp,dado.get_gpon(),dado.get_port(),dado.get_id()))
        dado.set_signal_2(facade.onu_get_tx(snmp,dado.get_gpon(),dado.get_port(),dado.get_id())/1000)
        dado.set_signal(facade.onu_get_signal(snmp,dado.get_gpon(),dado.get_port(),dado.get_id())/100)
        return dado
def liberar_fun(olt,facade,ont)->bool:
    facade.liberar(olt,ont)
def set_off(snmp,facade,ret):
        dado=(ont_())
        dado.set_modelo(ret[9])
        dado.set_sn(ret[7])
        dado.set_vlan(ret[8])
        dado.set_id(ret[1])
        dado.set_port(ret[2])
        dado.set_gpon(ret[3])
        dado.set_zone(ret[4])
        dado.set_descricao(ret[5])
        dado.set_service_port(ret[6])
        dado.set_generic(ret[10])
        dado.set_status(facade.onu_on(snmp,dado.get_gpon(),dado.get_port(),dado.get_id()))
        if dado.get_status()==1:
            return 0
        return dado