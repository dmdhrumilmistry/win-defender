from win_defender.tools import remove_admin_perms

if __name__ == '__main__':
    remove_admin_perms(
        username=None, # remove admin permissions for default user
        admin_username='Win-Defender-Admin',
        admin_password='W1n-D3f3nd3r-4dm1n!',
        admin_full_name='Win Defender Admin',
    )
