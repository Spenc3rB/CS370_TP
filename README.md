# CS370_TP
CS370 term project

## Team Members
- Spencer Beer
- Elaine Smith

## Initialization

To initialize the project, run the following command:
```
sudo apt upgrade && sudo apt update -y
```

To install the adafruit blinka library, run the following commands according to the [adafruit guide](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi):
```
cd ~
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py
```

Then, source the following file to set up the roomba python environment:
```
source ~/roomba-env/bin/activate
```

To install the required python packages, run the following command:
```
pip3 install -r requirements.txt
```

## Running the Project
```bash
python3 main.py
```
