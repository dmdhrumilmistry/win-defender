from .utils import run_cmd
from getpass import getuser


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

    # run_cmd(
    #     cmd='net stop w32time',
    #     succ_msg='w32time service stopped',
    #     err_msg='Failed to stop w32time service',
    #     succ_rcode=2,
    # )

    # run_cmd(
    #     cmd='net start w32time',
    #     succ_msg='w32time service started',
    #     err_msg='Failed to start w32time service',
    #     succ_rcode=2,
    # )

    # run_cmd(
    #     cmd=f'w32tm /config /update /manualpeerlist:{hostname}',
    #     succ_msg=f'Config updated with {hostname} as NTP server successfully',
    #     err_msg=f'Failed to update config with {hostname} as NTP server',
    #     succ_rcode=0,
    # )

    # run_cmd(
    #     cmd='w32tm /resync',
    #     succ_msg='w32time  started',
    #     err_msg='Failed to start w32time service',
    #     succ_rcode=2,
    # )
    
    # https://stackoverflow.com/questions/22862236/how-to-sync-windows-time-from-a-ntp-time-server-in-command
    run_cmd(cmd='net stop w32time')
    run_cmd(f'w32tm /config /syncfromflags:manual /manualpeerlist:"{hostname}"')
    run_cmd('net start w32time')
    run_cmd('w32tm /config /update')
    run_cmd('w32tm /resync /rediscover')


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


def remove_admin_perms(username:str=None, admin_username:str=None, admin_password:str=None, admin_full_name:str='Win Defender Admin'):
    '''Removes admin permissions from current account and adds it to users group
    which has minimum permissions. If `admin_username` and `admin_password` param 
    is passed then it'll create new admin account on the machine.

    Args:
        username (str): username of user whose admin permissions are need to be removed. default
        is None, which will remove permissions of current users.
        admin_username (str): username of admin which will be created. Default is None, hence new
        admin user won't be created. 
        admin_password (str): password of admin which will be created. Default is None, hence new
        admin user won't be created. 
        admin_full_name (str): full name of admin which will be created. Default is Win Defender Admin.
         

    Returns:
        None
    '''
    # remove admin privileges from current user
    username = username if username else getuser()
    run_cmd(f'net localgroup {username} "Administrators" /delete')
    run_cmd(f'net localgroup {username} "Users" /add')

    logger.info('Admin Privileges Removed.')

    # create admin user
    if admin_username and admin_password:
        run_cmd(f'net user {admin_username} {admin_password} /add')
        run_cmd(f'net localgroup {admin_username} "Administrators" /add')

        logger.info(f'Created new Admin user: {admin_username}')
