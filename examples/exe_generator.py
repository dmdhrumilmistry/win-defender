from win_defender.utils import Compilers, ExecutableGenerator

exe = ExecutableGenerator(
    file_path = r'time_syncer.py', # python program file path
    output_dir = '.', # output directory
    compiler = Compilers.DEFAULT, # compile using DEFAULT, CLANG, MINGW
    onefile = True, # creates single exe file
    remove_output = True, # deletes all compiled files and retains only exe
    window_uac_perms=True, # asks user for admin rights on windows (only for windows machine)   
    disable_console=True,
)

return_code = exe.generate_executable()