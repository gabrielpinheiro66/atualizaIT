from configparser import ConfigParser

arquivo_pastas = 'pastas.conf'
arquivo_ssh = 'ssh.conf'


def ssh_conf():
    parser = ConfigParser()
    with open(arquivo_ssh) as ssh_data:
        parser.read_string("[top]\n" + ssh_data.read())
        hostname = parser.get('top', 'hostname')
        username = parser.get('top', 'username')
        password = parser.get('top', 'password')
    return hostname, username, password


def pastas_conf():
    pastas = []
    secoes = []
    parser = ConfigParser()
    with open(arquivo_pastas):
        parser.read(arquivo_pastas)
        sections = parser.sections()
        for section in sections:
            lista_de_pasta = []
            pasta_adm = parser.get(section, 'pasta_adm')
            pasta_local = parser.get(section, 'pasta_local')
            pasta_teste = parser.get(section, 'pasta_teste')
            lista_de_pasta.append(pasta_adm)
            lista_de_pasta.append(pasta_local)
            lista_de_pasta.append(pasta_teste)
            secoes.append(section)
            pastas.append(lista_de_pasta)
            del lista_de_pasta
    return secoes, pastas


