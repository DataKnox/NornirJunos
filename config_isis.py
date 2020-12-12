from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

nr = InitNornir(config_file=f"{script_dir}/config.yml")

junos_devices = nr.filter(F(topo_type="PE") | F(topo_type="P"))


def isis_config(task):
    data = task.host.data
    net_response = task.run(task=pyez_config, template_path='/mnt/c/NornirJunos/isis_interfaces.j2',
                            template_vars=data, data_format='xml', name='Set ISO and NET')
    if net_response:
        diff = task.run(task=pyez_diff, name='NET and ISO diff')
    if diff:
        task.run(task=pyez_commit, name='NET and ISO commit')
    response = task.run(task=pyez_config, template_path='/mnt/c/NornirJunos/isis_config.j2',
                        template_vars=data, data_format='xml', name='config ISIS Protocol')
    if response:
        diff = task.run(task=pyez_diff, name='ISIS Diff')
    if diff:
        task.run(task=pyez_commit, name='ISIS commit')


send_result = junos_devices.run(
    task=isis_config)
print_result(send_result)
