# Informacion util software y hardware
# https://github.com/juanmfer
# pip install psutil
# pip install py-cpuinfo
import os
import platform
import psutil
from cpuinfo import get_cpu_info, cpuinfo
from datetime import datetime

veros1 = platform.platform()
login = os.getlogin()
arquitectura = platform.architecture()
sistema = platform.uname()
proc = cpuinfo.get_cpu_info_json()
memv = psutil.virtual_memory()
particiones = psutil.disk_partitions()


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f'{bytes:.2f}{unit}{suffix}'
        bytes /= factor


print('#' * 100)
print('# Bienvenido', login, 'a la informacion de tu Hardware y Software')
print('')
print('#### Hardware')
print('')
# procesador
for key, value in get_cpu_info().items():
    if key == 'brand_raw':
        print('###   Procesador: ', value)
print('    Arquitectura', arquitectura[0])
print('    Nucleos fisicos: ', psutil.cpu_count(logical=False))
print('    Nucleos Totales:', psutil.cpu_count(logical=True))
print('    Uso de CPU por nucleo:')
for i, prcen in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(' ' * 26, f"Nucleo {i}: {prcen}%")
print(' ' * 40, f"Total: {psutil.cpu_percent()}%")

# memoria
print('###   Memoria: ')
print(' ' * 8, f'Total: {get_size(memv.total)}')
print(' ' * 8, f'Disponible: {get_size(memv.available)}')
print(' ' * 8, f'Usada: {get_size(memv.used)}')
print('\n')

# disco
print('###   Discos:')
for particion in particiones:
    print(f"       Dispositivo: {particion.device} ")
    print(f"       Punto de montaje : {particion.mountpoint}")
    print(f"       Sistema de Archivo: {particion.fstype}")
    try:
        particion_usada = psutil.disk_usage(particion.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"           Tamaño total: {get_size(particion_usada.total)}")
    print(f"           Usado: {get_size(particion_usada.used)}")
    print(f"           Libre: {get_size(particion_usada.free)}")
    print(f"           Porcentaje: {particion_usada.percent}%")
print('\n')
# Red
print('###   Informacion de Red:')
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"    Interfaz: {interface_name}")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"         IP Address: {address.address}")
            print(f"         Netmask: {address.netmask}")
            print(f"         Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"         MAC Address: {address.address}")
            print(f"         Netmask: {address.netmask}")
            print(f"         Broadcast MAC: {address.broadcast}")
# get IO statistics since boot
net_io = psutil.net_io_counters()
print(f"    Bytes totales enviados: {get_size(net_io.bytes_sent)}")
print(f"    Bytes totales recibidos: {get_size(net_io.bytes_recv)}")
# Soft
print('\n')
print('#### Software')
uname = platform.uname()
print(f"         Sistema: {uname.system}")
print('         Login: ', login)
print(f"         Release: {uname.release}")
print(f"         Version: {uname.version}")
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"         Ingreso al sistema: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
print('         Python version:', platform.python_version())
