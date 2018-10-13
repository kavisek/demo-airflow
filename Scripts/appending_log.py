import datetime
path = '/Users/kavi/Documents/Airflow/Python Scripts/Logs/'
with open(path + 'log.txt', 'a') as log_file:
    dt_time = str(datetime.datetime.now())
    log_file.write('\n This script last ran at: ' + dt_time)
