from shutil import copy, rmtree
from paramiko import SSHClient, AutoAddPolicy
import subprocess
from config import ssh_conf
from datetime import datetime
from os import path, getcwd, makedirs, remove



LOCAL_DO_SOFFICE = r'C:\Program Files\LibreOffice\program\soffice.exe'
barra_invertida = LOCAL_DO_SOFFICE[2]


def logging(string):
    try:
        __location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))
        now = datetime.now()
        dia = now.strftime('%Y-%m-%d')
        with open(path.join(__location__ + "\\\\log\\\\", str(dia+'.txt')), "a") as arq:
            momento = now.strftime('\n[%d/%m/%Y - %H:%M:%S] - ')
            if string != "==================================":
                arq.write(momento + string)
                print(momento + string)
            else:
                arq.write(string)
                print(string)
    except FileNotFoundError:
        print("Programa não encontrou a pasta log. Criando...")
        pasta_log = r'log'
        makedirs(pasta_log)
        logging("Programa não encontrou a pasta log. Ela foi criada e o programa reiniciado")


class Ssh():
    def __init__(self, hostname, username, password):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(hostname=hostname, username=username, password=password)

    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        if stderr.channel.recv_exit_status() != 0:
            try:
                logging(stderr.read())
            except Exception:
                pass


def copy_export(src_file, dst_file, lock):
    try:
        if lock and (src_file.endswith('.odt') or src_file.endswith('.doc') or src_file.endswith('.docx')):
            tsd = dst_file[::-1]
            for i in range(len(tsd)):
                if tsd[i] == barra_invertida:
                    tsd = tsd[i + 1:len(tsd)]
                    break
            tsd = tsd[::-1]
            logging(f"Exportar para pdf {src_file} para {tsd}")
            generate_pdf(src_file, tsd)
        else:
            logging(f"Copiando {src_file} para {dst_file}")
            copy(src_file, dst_file)
    except Exception as e:
        logging(f"Erro copy_export - {e}")


def __delete_file(dst_file):
    hostname = ''
    username = ''
    password = ''
    try:
        hostname, username, password = ssh_conf()
    except Exception as e:
        logging(f"Erro tentando pegar arquivo ssh.conf - {e}")
    if hostname:
        if hostname in dst_file:
            #arquivo no server
            try:
                ssh = Ssh(hostname, username, password)
                __string = dst_file
                __num = __string.index('dados')
                __string = __string[__num:]
                __string = __string.replace(barra_invertida, '/')
                __string = f'/{__string}'
                logging(f"Remove: {dst_file}")
                ssh.exec_cmd(f"rm -rf '{__string}'")
                ssh.exec_cmd("exit")
            except Exception as e:
                logging(f"Erro tentando apagar arquivo - {e}")
        else:
            try:
                if path.isdir(dst_file):
                    rmtree(dst_file)
                    logging(f"Remove: {dst_file}")
                else:
                    remove(dst_file)
                    logging(f"Remove: {dst_file}")
            except Exception as e:
                logging(f"Erro tentando deletar arquivo local: {e}")


def generate_pdf(doc_path, path):
    subprocess.run([LOCAL_DO_SOFFICE,
                      '--headless',
                     '--convert-to',
                     'pdf',
                     '--outdir',
                     path,
                     doc_path])

