from .utils import run_cmd
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


def sync_time(hostname:str='samay1.nic.in'):
    '''Synchronize time with specified hostname time server on windows machine
    
    Args:
        hostname (str): NTP hostname/IP. default: samay1.nic.1

    Returns:
        None
    '''

    run_cmd(
        cmd='net stop w32time',
        succ_msg='w32time service stopped',
        err_msg='Failed to stop w32time service',
        succ_rcode=2,
    )

    run_cmd(
        cmd='net start w32time',
        succ_msg='w32time service started',
        err_msg='Failed to start w32time service',
        succ_rcode=2,
    )

    run_cmd(
        cmd=f'w32tm /config /update /manualpeerlist:{hostname}',
        succ_msg=f'Time Synced with {hostname} successfully',
        err_msg=f'Failed to sync time with {hostname}',
        succ_rcode=0,
    )
       

def block_root_hubs():
    '''Blocks USB root hubs on windows machine
    
    Args:
        None
    
    Returns:
        None
    '''
    res, rcode = run_cmd(
        cmd='pnputil /enum-devices /class "USB"',
        succ_msg='Fetched USB devices ids list',
        err_msg='Error occurred while device ids list',
    )

    if rcode == 0:
        for line in res.splitlines():
            if "USB\ROOT_HUB" in line:
                device_id = line.split(':')[-1].strip()
                res, rcode = run_cmd(
                    cmd=f'pnputil /disable-device "{device_id}"',
                    succ_msg=f'USB {device_id} blocked',
                    err_msg=f'Cannot disable USB {device_id}'
                )
