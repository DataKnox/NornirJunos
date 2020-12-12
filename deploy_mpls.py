from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

nr = InitNornir(config_file=f"{script_dir}/config.yml")

junos_devices = nr.filter(F(topo_type="PE") | F(topo_type="P"))


def rsvp_config(task):
    data = task.host.data
    net_response = task.run(task=pyez_config, template_path='/mnt/c/NornirJunos/mpls_proto.j2',
                            template_vars=data, data_format='xml', name='Config RSVP')
    if net_response:
        diff = task.run(task=pyez_diff, name='RSVP diff')
    if diff:
        task.run(task=pyez_commit, name='RSVP commit')


send_result = junos_devices.run(
    task=rsvp_config)
print_result(send_result)
