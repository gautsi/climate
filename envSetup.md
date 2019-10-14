# Environment setup

## make a google cloud instance
- g1-small
- ubuntu

## python
- python 3.6.8 preinstalled
- pip3 installed with
```
sudo apt upgrade
sudo apt-get install python3-pip
```
- venv installed with
```
sudo apt-get install -y python3-venv
```
- made a new environment with
```
python3 -m venv my_env
```
- before committing, needed to set up git with
```
git config --global user.email "email"
git config --global user.name "name"
```
- activate the environment with 
```
source my_env/bin/activate
```
- install jupyter lab with
```
pip3 install jupyterlab
```
- to access jupyter lab from the browser, run
```
jupyter lab --no-browser --port PORT_NUMBER
```
and connect to SSH from gcloud with
```
"gcloud ssh command" -- -4 -L 5000:localhost:5000
```
then go to IP_ADDRESS:PORT_NUMBER in the browser, type in the token
