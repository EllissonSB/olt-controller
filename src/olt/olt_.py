import os
import paramiko

class OLT:
    MODELOS_PON_PORTS=['H806GPFD','H805GPFD','H903GPSF','H901GPSF']
    def __init__(self, modelo, ip):
        self.modelo = modelo
        self.ip = ip
        self.username = os.getenv("username")
        self.password = os.getenv("password")
        if not self.username or not self.password:
            raise Exception("As variáveis de ambiente 'username' e 'password' devem ser definidas.")
        self.boards_pons = []
        self.boards_pons_autofind = []
        self.define_boards_gpons()
        self.defines_boards_autofind()
    def conectar(self):
        #Inicia a conexão
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(self.ip, username=self.username, password=self.password)
            print(f"Conexão estabelecida com {self.ip}")
        except paramiko.AuthenticationException:
            raise Exception("Falha na autenticação. Verifique as credenciais.")
        except paramiko.SSHException as e:
            raise Exception(f"Erro na conexão SSH: {str(e)}")
        #comando de enable e config para ficar no modo de configuração da olt
        self.client.exec_command("en")
        self.client.exec_command("conf")

    def _ssh_execute(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        error = stderr.read().decode('utf-8')
        if error:
            raise Exception(f"Erro ao executar comando '{command}': {error}")
        return stdout.read().decode('utf-8')
    def _define_boards(self, keyword, target_list):
        stdout, stderr = self._ssh_execute("display board 0\n")
        stdout = stdout.split("\n")
        for line in stdout:
            if any(modelo in line for modelo in self.MODELOS_PON_PORTS) and keyword in line:
                parts = line.split()
                if len(parts) > 0:
                    try:
                        target_list.append(int(parts[0]))
                    except ValueError:
                        continue

    def define_boards_gpons(self):
        self._define_boards("Normal", self.boards_pons)

    def defines_boards_autofind(self):
        self._define_boards("AutoFind", self.boards_pons_autofind)