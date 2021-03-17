# Remove a conda enviroment if it ExperimentStatus
cd ~/Repos/Airflow
echo Removing any existing "Conda" environment...
conda env remove -n direct || echo conda remove command failed! Install conda


echo Installing "Direct" Conda Environment..
conda env create --file environment.yml
echo Finished "Direct" Environment Installation.

cd ~/Airflow
echo Finished Installation
# conda env remove -n direct
