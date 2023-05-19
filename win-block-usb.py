from subprocess import PIPE, run
from shlex import split
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


def run_cmd(cmd:str) -> tuple:
    '''Run shell commands
    
    Arguments:
        cmd (string): command to be executed

    Returns:
        tuple: returns executed command output/error along with status code
    '''
    result = run(split(cmd), stderr=PIPE, stdout=PIPE)
    return (result.stdout.decode('utf-8') or result.stderr.decode('utf-8'), result.returncode)


def block_root_hubs():
    rcode, res = run_cmd('pnputil /enum-devices /class "USB" | findstr "USB\ROOT_HUB"')

    if rcode == 0:
        for line in res.splitlines():
            device_id = line.split(':')[-1].strip()
            rcode, res = run_cmd(f'pnputil /disable-device "{device_id}"')
            if rcode == 0:
                logger.info(f'USB {device_id} blocked')
            else:
                logger.error(f'Cannot disable USB {device_id}')
    else:
        logger.error('Error occurred while gettings device ids')

if __name__ == '__main__':
    block_root_hubs()