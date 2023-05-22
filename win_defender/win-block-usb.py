from utils import run_cmd
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')

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

if __name__ == '__main__':
    block_root_hubs()