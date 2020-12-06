from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

nr = InitNornir(config_file=f"{script_dir}/config.yml")

junos_devices = nr.filter(F(node_type="PE"))


def lacp_config(task):
    data = task.host.data
    if data['mc_lag']:
        print(data)
        chassis_response = task.run(name='lacp chassis config', task=pyez_config, template_path='/mnt/c/NornirJunos/mc-lag.j2',
                                    template_vars=data, data_format='xml')
        diff = task.run(task=pyez_diff, name='int diff')
        if diff:
            commit = task.run(task=pyez_commit, name='int commit')


send_result = junos_devices.run(
    task=lacp_config)
print_result(send_result)
