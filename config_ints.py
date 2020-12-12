from working.set_ints import base_config
from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

nr = InitNornir(config_file=f"{script_dir}/config.yml")
junos_devices = nr.filter(F(node_type="lab"))


def main(task):
    # base_config()
    data = task.host.data
    int_response = task.run(name='int config', task=pyez_config, template_path='/mnt/c/NornirJunos/interfaces.j2',
                            template_vars=data, data_format='xml')
    if int_response:
        diff = task.run(task=pyez_diff, name='int diff')
    if diff:
        task.run(task=pyez_commit, name='int commit')


if __name__ == "__main__":
    results = junos_devices.run(task=main)
    print_result(results)
