# Pull Image from docker hub
FROM conda/miniconda3

# Set working directory
WORKDIR /root

# Copy all of the current dicetories content so the docker container
COPY . /root/

# print out the content of what was uploaded to our root folder
RUN ls -la /root/*

# Update Conda
RUN conda update -n base -c defaults conda # Update conda
RUN conda config --add channels conda-forge

# Create Conda Virtual Enviroment
RUN conda create --name airflow python=3.6 -y
# RUN echo "source activate airflow" > ~/.bashrc
# ENV PATH /opt/conda/envs/env/bin:$PATH

# Conda Package Installations
RUN /bin/bash -c "source activate airflow \
  && conda install pandas -y \
  && conda install -c conda-forge gspread -y \
  && conda install -c conda-forge jupyterlab -y \
  && conda install -c conda-forge gspread -y \
  && conda install -c anaconda boto -y \
  && conda install -c conda-forge tqdm -y \
  && conda install -c annetheagile httplib2 -y \
  && conda install -c conda-forge oauth2client -y \
  && conda install -c conda-forge python-utils -y \
  && conda install mysql-connector-python==2.2.3 -y \
  && conda install mysql-connector-c==6.1.6 -y \
  && conda install pandas -y \
  && conda install airflow=1.10.3 -y \
  && pip install -r requirements/requirements.txt \
  && conda deactivate"

# Installing Postgres Command Line Client
RUN apt-get update
RUN apt-get install sudo  -y
RUN sudo apt-get install postgresql postgresql-contrib -y

# Installting Nano
RUN sudo apt install nano

# Setting Airflow Enviroment Variable

ENV AIRFLOW_HOME="/root"

# Make port 8080
EXPOSE 8080
EXPOSE 54320
EXPOSE 5432
