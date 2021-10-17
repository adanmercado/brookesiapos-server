import os, sys, subprocess

current_dir = os.getcwd()
script_dir = os.path.dirname(__file__)
if current_dir != script_dir:
    os.chdir(script_dir)

sys.path.append('..')
from utils import standard_paths

app_data_path = standard_paths.config_path() / 'brookesiapos-server'
try:
    app_data_path.mkdir(parents=True)
except FileExistsError:
    pass

db_name = app_data_path / 'brookesiapos.db'
try:
    db_name.touch()
except:
    print(f'The {str(db_name)} database file could not be created')
    sys.exit(0)

string_db_name = str(db_name)

create_db_script = f'{script_dir}/sql/create_database.sql'
print(f'Executing {create_db_script} script')
subprocess.call(['sqlite3', string_db_name, '.read ' + create_db_script])

setup_db_script = f'{script_dir}/sql/setup_default_data.sql'
print(f'Executing {setup_db_script} script')
subprocess.call(['sqlite3', string_db_name, '.read ' + setup_db_script])