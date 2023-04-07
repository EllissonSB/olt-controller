import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp import hlapi
def get_dados(snmp,oids):
    #print(snmp.get_community(),snmp.get_ip(),oids)
    handler = hlapi.getCmd(hlapi.SnmpEngine(),hlapi.CommunityData(snmp.get_community()),hlapi.UdpTransportTarget((snmp.get_ip(), 161)),hlapi.ContextData(),*construct_object_types(oids))
    return fetch(1,handler)
def construct_object_types(oids):
        object_types = []
        for oid in oids:
            object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
        return object_types
def fetch(count,handler):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result
def cast(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                try:
                    return str(value)
                except (ValueError, TypeError):
                    pass
        return value
def get_auto_find(olt,oid):
        SYSNAME=oid
        host=olt.get_ip()
        snmp_ro_comm=olt.get_community()
        auth=cmdgen.CommunityData(snmp_ro_comm)
        cmdGen = cmdgen.CommandGenerator()
        errorIndication,errorStatus,errorIndex,varBinds=cmdGen.getCmd(auth,cmdgen.UdpTransportTarget((host,161)),cmdgen.MibVariable(SYSNAME),lookupMib=False,)
        if errorIndication:
            sys.exit()
        for oids,val in varBinds:
            return val.prettyPrint()