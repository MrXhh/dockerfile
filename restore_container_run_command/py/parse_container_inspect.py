#!/usr/bin/env python
#
"""
author: Song yanlin
mail: hanxiao2100@qq.com
date: 2021-09-24
"""

import docker
from docker.errors import ImageNotFound, APIError

from sys import argv
import re, os


class MYDOCKER(object):
    def __init__(self):
        super(MYDOCKER, self).__init__()
        if not os.path.exists("/var/run/docker.sock"):
            self.help_msg()
            exit(1)
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

        # container name or container id. type is str
        self.container = argv[1]
        self.inspect:dict = {}
        self.docker_run_cmd = "docker run "
        self.options = {"kv": [], "k": []}
        self.image = None  # str
        self.command = None  # str
        self.args = []

    def _print_docker_run_cmd(self):
        if not self.inspect:
            return

    def _get_inspect_container(self):

        """

        * Example for get inspect for a container
        self.api_client.inspect_container("mysql01")
{
    'Id': 'cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955',
    'Created': '2021-04-25T09:52:13.612852757Z',
    'Path': 'docker-entrypoint.sh', 'Args': ['mysqld'],
    'State': {
        'Status': 'running',
        'Running': True,
        'Paused': False,
        'Restarting': False,
        'OOMKilled': False,
        'Dead': False,
        'Pid': 2133,
        'ExitCode': 0,
        'Error': '',
        'StartedAt': '2021-09-11T14:12:05.741885047Z',
        'FinishedAt': '2021-09-11T22:12:03.260400088+08:00'
    },
    'Image': 'sha256:0627ec6901db4b2aed6ca7ab35e43e19838ba079fffe8fe1be66b6feaad694de',
    'ResolvConfPath': '/var/lib/docker/containers/cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955/resolv.conf',
    'HostnamePath': '/var/lib/docker/containers/cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955/hostname',
    'HostsPath': '/var/lib/docker/containers/cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955/hosts',
    'LogPath': '/var/lib/docker/containers/cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955/cff524e16f5cc4512c5aea22436668fe73364341e88ec8bcba8283523092c955-json.log',
    'Name': '/mysql01',
    'RestartCount': 0,
    'Driver': 'overlay2',
    'Platform': 'linux',
    'MountLabel': '',
    'ProcessLabel': '',
    'AppArmorProfile': '',
    'ExecIDs': None,
    'HostConfig': {
        'Binds': None,
        'ContainerIDFile': '',
        'LogConfig': {'Type': 'json-file', 'Config': {}},
        'NetworkMode': 'default',
        'PortBindings': {
            '3306/tcp': [
                {'HostIp': '', 'HostPort': '13306'}
            ]
        },
        'RestartPolicy': {
            'Name': 'always',
            'MaximumRetryCount': 0
        },
        'AutoRemove': False,
        'VolumeDriver': '',
        'VolumesFrom': None,
        'CapAdd': None,
        'CapDrop': None,
        'CgroupnsMode': 'host',
        'Dns': [],
        'DnsOptions': [],
        'DnsSearch': [],
        'ExtraHosts': None,
        'GroupAdd': None,
        'IpcMode': 'private',
        'Cgroup': '',
        'Links': None,
        'OomScoreAdj': 0,
        'PidMode': '',
        'Privileged': False,
        'PublishAllPorts': False,
        'ReadonlyRootfs': False,
        'SecurityOpt': None,
        'UTSMode': '',
        'UsernsMode': '',
        'ShmSize': 67108864,
        'Runtime': 'runc',
        'ConsoleSize': [0, 0],
        'Isolation': '',
        'CpuShares': 0,
        'Memory': 0,
        'NanoCpus': 0,
        'CgroupParent': '',
        'BlkioWeight': 0,
        'BlkioWeightDevice': [],
        'BlkioDeviceReadBps': None,
        'BlkioDeviceWriteBps': None,
        'BlkioDeviceReadIOps': None,
        'BlkioDeviceWriteIOps': None,
        'CpuPeriod': 0,
        'CpuQuota': 0,
        'CpuRealtimePeriod': 0,
        'CpuRealtimeRuntime': 0,
        'CpusetCpus': '',
        'CpusetMems': '',
        'Devices': [],
        'DeviceCgroupRules': None,
        'DeviceRequests': None,
        'KernelMemory': 0,
        'KernelMemoryTCP': 0,
        'MemoryReservation': 0,
        'MemorySwap': 0,
        'MemorySwappiness': None,
        'OomKillDisable': False,
        'PidsLimit': None,
        'Ulimits': None,
        'CpuCount': 0,
        'CpuPercent': 0,
        'IOMaximumIOps': 0,
        'IOMaximumBandwidth': 0,
        'MaskedPaths': [
            '/proc/asound', '/proc/acpi', '/proc/kcore', '/proc/keys', '/proc/latency_stats',
            '/proc/timer_list', '/proc/timer_stats', '/proc/sched_debug', '/proc/scsi',
            '/sys/firmware'
        ],
        'ReadonlyPaths': ['/proc/bus', '/proc/fs', '/proc/irq', '/proc/sys', '/proc/sysrq-trigger']
    },
    'GraphDriver': {
        'Data': {
            'LowerDir': '/var/lib/docker/overlay2/b29f5b9c07b807f6eba2f6d211f19f44e586fa8be48251c8b1cda8b816d23b5c-init/diff:/var/lib/docker/overlay2/bac38b553cca1c699e52cb93363d1a8480bfa2b881f0f62bb58549fd8f91f26a/diff:/var/lib/docker/overlay2/59d145469aba9d31081bd44decae7f97595d48befa1f63f4bfa70e7a6f126e75/diff:/var/lib/docker/overlay2/4e2678dbfad6da11df7c3f5812d344560ec4b55e0f70b81f28b0d02797cafacd/diff:/var/lib/docker/overlay2/8f051956166a117b761cfffbc23ae0ecf25575ec9756e037cc8e6877d4d0a834/diff:/var/lib/docker/overlay2/46974c7adc17c06e6b00720ff4797ff0c3b3a71454e89698fdae4aa030859488/diff:/var/lib/docker/overlay2/d714cc813d881b0281d4a63e45cec659ce0476e5c1464a17608b03a9554f1810/diff:/var/lib/docker/overlay2/96ed59222c210bacb377c2a23fec49b695f40d44fc12cfa7194ce865f231d6ec/diff:/var/lib/docker/overlay2/1f6bb66f8a09f556743e8e7ba5844cf7d9e8fd0fc1a9fee634cfba89bd233448/diff:/var/lib/docker/overlay2/abd94392e67ede2992a75ecdc00d5d01af4d581b24929a63d7e751a8d0f7eba3/diff:/var/lib/docker/overlay2/3cf69fc044e1a9c3936627f6a8a2ee4f30ade78a4fc26c02802416b2a7120a6e/diff:/var/lib/docker/overlay2/498d52bfc59807623d172a07df8e7afa631995452098711a954459dd07364ab7/diff:/var/lib/docker/overlay2/65224c6b7f4880dbedc01e02b903b21b0e032bd28ffdaf4a2d758ec35c1fcc31/diff',
            'MergedDir': '/var/lib/docker/overlay2/b29f5b9c07b807f6eba2f6d211f19f44e586fa8be48251c8b1cda8b816d23b5c/merged',
            'UpperDir': '/var/lib/docker/overlay2/b29f5b9c07b807f6eba2f6d211f19f44e586fa8be48251c8b1cda8b816d23b5c/diff',
            'WorkDir': '/var/lib/docker/overlay2/b29f5b9c07b807f6eba2f6d211f19f44e586fa8be48251c8b1cda8b816d23b5c/work'
        },
        'Name': 'overlay2'
    },
    'Mounts': [
        {'Type': 'volume',
         'Name': 'c69b2a1b7f8ff84bf90f52306c7ca86a944633d11e61ea7c29b75e8aeda4da34',
         'Source': '/var/lib/docker/volumes/c69b2a1b7f8ff84bf90f52306c7ca86a944633d11e61ea7c29b75e8aeda4da34/_data',
         'Destination': '/var/lib/mysql',
         'Driver': 'local',
         'Mode': '',
         'RW': True,
         'Propagation': ''
         }
    ],
    'Config': {
        'Hostname': 'cff524e16f5c',
        'Domainname': '',
        'User': '',
        'AttachStdin': False,
        'AttachStdout': False,
        'AttachStderr': False,
        'ExposedPorts': {
            '3306/tcp': {},
            '33060/tcp': {}
        },
        'Tty': False,
        'OpenStdin': False,
        'StdinOnce': False,
        'Env': [
            'MYSQL_ROOT_PASSWORD=py123456',
            'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
            'GOSU_VERSION=1.12', 'MYSQL_MAJOR=8.0', 'MYSQL_VERSION=8.0.24-1debian10'
        ],
        'Cmd': ['mysqld'],
        'Image': 'mysql',
        'Volumes': {'/var/lib/mysql': {}},
        'WorkingDir': '',
        'Entrypoint': ['docker-entrypoint.sh'],
        'OnBuild': None,
        'Labels': {}
    },
    'NetworkSettings': {
        'Bridge': '',
        'SandboxID': '4ff2100de411cf4eb0761f25bb8f9bf5d8fc99fc7dd8a9a566fe736de181bbcd',
        'HairpinMode': False,
        'LinkLocalIPv6Address': '',
        'LinkLocalIPv6PrefixLen': 0,
        'Ports': {
            '3306/tcp': [
                {'HostIp': '0.0.0.0', 'HostPort': '13306'}, {'HostIp': '::', 'HostPort': '13306'}
            ],
            '33060/tcp': None
        },
        'SandboxKey': '/var/run/docker/netns/4ff2100de411',
        'SecondaryIPAddresses': None,
        'SecondaryIPv6Addresses': None,
        'EndpointID': 'b8466e7784f624f17b55fad2c6fc31486c26444505d4315beb67cf53faa55e6b',
        'Gateway': '172.17.0.1',
        'GlobalIPv6Address': '',
        'GlobalIPv6PrefixLen': 0,
        'IPAddress': '172.17.0.3',
        'IPPrefixLen': 16,
        'IPv6Gateway': '',
        'MacAddress': '02:42:ac:11:00:03',
        'Networks': {
            'bridge': {
                'IPAMConfig': None,
                'Links': None,
                'Aliases': None,
                'NetworkID': 'ae3745bc55a172f99410058e94d5800b538dc8b7d08715a836ae4b929a1e3df5',
                'EndpointID': 'b8466e7784f624f17b55fad2c6fc31486c26444505d4315beb67cf53faa55e6b',
                'Gateway': '172.17.0.1',
                'IPAddress': '172.17.0.3',
                'IPPrefixLen': 16,
                'IPv6Gateway': '',
                'GlobalIPv6Address': '',
                'GlobalIPv6PrefixLen': 0,
                'MacAddress': '02:42:ac:11:00:03',
                'DriverOpts': None
            }
        }
    }
}

        :return:
        """

        try:
            self.inspect = self.api_client.inspect_container(self.container)

        except APIError as e:
            print(e)

    def _parse_inspect_container(self):
        if not self.inspect:
            return

        # options  --start
        ## --hostname
        if not self.inspect['Id'].startswith(self.inspect['Config']['Hostname']):
            self.options['kv'].append(
                {"--hostname", self.inspect['Config']['Hostname']}
            )

        ## --detach. Run container in background and print container ID
        self.options['k'].append("d")

        ## tty and stdin
        if self.inspect['Congif']['Tty']:
            self.options['k'].append("t")
        if self.inspect['Config']['OpenStdin']:
            self.options['k'].append("i")

        ## --attach
        if self.inspect['Congif']['AttachStdin'] and self.inspect['Congif']['AttachStdout'] and self.inspect['Congif']['AttachStderr']:
            self.options['k'].append("a")

        ## --name
        if "Name" in self.inspect:
            self.options['kv'].append(
                {"--name": self.inspect['name'].replace("/", "")}
            )

        ## --restart
        _restart_policy = self.inspect['HostConfig']['RestartPolicy']
        if _restart_policy['Name'] == "on-failure":
            self.options['kv'].append(
                {"--restart=": f"on-failure:{_restart_policy['MaximumRetryCount']}"}
            )
        if _restart_policy['Name'] in ("unless-stopped", "always"):
            self.options['kv'].append(
                {"--restart=": _restart_policy['Name']}
            )

        ## --volume, -v
        for mount in self.inspect['Mounts']:
            if mount['Type'] == "bind":
                if mount['RW']:
                    self.options['kv'].append(
                        {"-v": f"{mount['Source']}:{mount['Destination']}"}
                    )
                else:
                    self.options['kv'].append(
                        {"-v": f"{mount['Source']}:{mount['Destination']}:ro"}
                    )

        ## --publish, -p
        if self.inspect['HostConfig']['PortBindings']:
            _pbs = self.inspect['HostConfig']['PortBindings']
            for p in _pbs:
                for psub in _pbs[p]:
                    if psub['HostIp']:
                        self.options['kv'].append(
                            {"-p": f"{psub['HostIp']}:{psub['HostPort']}:{p}"}
                        )
                    else:
                        self.options['kv'].append(
                            {"-p": f"{psub['HostPort']}:{p}"}
                        )


        ## --env, -e
        if self.inspect['Config']['Env']:
            for e in self.inspect['Config']['Env']:
                self.options['kv'].append(
                    {"--env": e}
                )

        ## --workdir, -w
        if self.inspect['Config']['WorkingDir']:
            self.options['kv'].append(
                {"-w": self.inspect['Config']['WorkingDir']}
            )

        ## --rm, Auto Remove
        if self.inspect['HostConfig']['AutoRemove']:
            self.options["kv"].append(
                {"--rm", ""}
            )


        # options  --end

        # image
        self.image = self.inspect['Config']['Image']

        # command and args
        if not self.inspect['Config']['Cmd'] == self.inspect['Args']:
            self.command = self.inspect['Config']['Cmd'][0]
            if len(self.inspect['Args']) > 0:
                self.args = self.inspect['Args']
            # if len(self.inspect['Config']['Cmd']) > 1:
            #     _args = self.inspect['Config']['Cmd'][1:]

    def help_msg(self):
        _MSG = """Usage:
# Command alias
echo "alias image2df='docker run -v /var/run/docker.sock:/var/run/docker.sock --rm cucker/image2df'" >> ~/.bashrc
. ~/.bashrc

# Excute command
image2df <CONTAINER>
"""
        print(_MSG)

    def start(self):
        pass


if __name__ == '__main__':
    mydocker = MYDOCKER()
    if len(argv) < 2 or argv[1] == "--help":
        mydocker.help_msg()
        exit(1)
    ret = mydocker.start()
