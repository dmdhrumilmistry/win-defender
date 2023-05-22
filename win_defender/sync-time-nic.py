from utils import run_cmd


def sync_time(hostname:str='samay1.nic.in'):
    '''Synchronize time with specified hostname time server on windows machine
    
    Args:
        hostname (str): NTP hostname/IP. default: samay1.nic.1

    Returns:
        None
    '''
    _, rcode = run_cmd(
        cmd='net start w32time',
        succ_msg='w32time service started',
        err_msg='Failed to start w32time service',
        succ_rcode=0,
    )

    if rcode == 0:
         run_cmd(
            cmd=f'w32tm /config /update /manualpeerlist:{hostname}',
            succ_msg=f'Time Synced with {hostname} successfully',
            err_msg=f'Failed to sync time with {hostname}',
            succ_rcode=0,
        )


if __name__ == '__main__':
    sync_time('samay1.nic.in')