import os
import paramiko

class OLT:
    MODELOS_PON_PORTS=['H806GPFD','H805GPFD','H903GPSF','H901GPSF']
    def __init__(self, modelo, ip):
        """
        Initializes an instance of the class with the specified model and IP address.

        Args:
            modelo (str): The model of the OLT device.
            ip (str): The IP address of the OLT device.

        Raises:
            Exception: If the environment variables 'username' or 'password' are not set.

        Attributes:
            modelo (str): The model of the OLT device.
            ip (str): The IP address of the OLT device.
            username (str): The username for authentication, retrieved from environment variables.
            password (str): The password for authentication, retrieved from environment variables.
            boards_pons (list): List to store board PONs.
            boards_pons_autofind (list): List to store automatically found board PONs.
        """
        self.modelo = modelo
        self.ip = ip
        self.username = os.getenv("username")
        self.password = os.getenv("password")
        if not self.username or not self.password:
            raise Exception("As variáveis de ambiente 'username' e 'password' devem ser definidas.")
        self.boards_pons = []
        self.boards_pons_autofind = []
    def _conectar(self):
        """
        Establishes an SSH connection to the device using Paramiko.

        Initializes the SSH client, sets the policy to automatically add the host key,
        and attempts to connect using the provided IP address, username, and password.
        Prints a success message if the connection is established.

        Raises:
            Exception: If authentication fails or if there is an SSH connection error.
        """
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
    def _ssh_execute(self, command):
        """
        Executes a command on a remote server via SSH.

        Args:
            command (str): The command to execute on the remote server.

        Returns:
            str: The standard output from the executed command.

        Raises:
            Exception: If there is an error during command execution, with the error message.
        """
        stdin, stdout, stderr = self.client.exec_command(command)
        error = stderr.read().decode('utf-8')
        if error:
            raise Exception(f"Erro ao executar comando '{command}': {error}")
        return stdout.read().decode('utf-8')
    def _define_boards(self, keyword, target_list):
        """
        Identifies and appends board numbers to the target list based on SSH output and filtering criteria.

        Args:
            keyword (str): A string used to filter lines in the SSH output.
            target_list (list): A list to which identified board numbers will be appended.

        Returns:
            None

        Side Effects:
            Modifies the target_list by appending integers representing board numbers found in the SSH output.

        Notes:
            - Uses self._ssh_execute to retrieve board information.
            - Filters lines containing any model from self.MODELOS_PON_PORTS and the specified keyword.
            - Handles ValueError if the board number cannot be converted to an integer.
        """
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
        """
        Defines GPON boards by invoking the internal _define_boards method with the type "Normal"
        and the list of boards specified in self.boards_pons.

        This method is typically used to set up or register GPON boards for further processing.

        Returns:
            None
        """
        self._define_boards("Normal", self.boards_pons)

    def defines_boards_autofind(self):
        """
        Defines boards with the 'AutoFind' status by invoking the internal _define_boards method
        with the type "AutoFind" and the list of boards specified in self.boards_pons_autofind.

        This method is typically used to identify and register boards that have been automatically found.

        Returns:
            None
        """
        self._define_boards("AutoFind", self.boards_pons_autofind)
    def init_connection(self):
        """
        Initializes the connection to the OLT device and prepares it for configuration.
        This method performs the following steps:
        1. Establishes an SSH connection to the device.
        2. Executes the 'en' command to enter privileged mode.
        3. Executes the 'config' command to enter configuration mode.
        4. Defines GPON boards.
        5. Defines autofind boards.
        Raises:
            Exception: If executing 'en' or 'config' commands fails.
        """
        self._conectar()
        try:
            self._ssh_execute("en")
        except Exception as e:
            print(f"Erro ao executar 'en': {e}")
            raise

        try:
            self._ssh_execute("config")
        except Exception as e:
            print(f"Erro ao executar 'config': {e}")
            raise

        self.define_boards_gpons()
        self.define_boards_autofind()