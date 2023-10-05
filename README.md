# Receipt Interceptor

This is a python program that will intercept requests from a Receipt Printer. You can use this to perform actions in addition to printing

## Setup

### Interfaces

In order to do this you first need a rasperry pi that has an ehternet port "eth0" and also a second usb adapter "eth1"

#### Step1:

To intercept this data we need to use the brctl ( bridge control ) command to create a bridge "br0" and add "eth0" and "eth1" to that bridge

For eas of setup we have included a `create-bridge.sh` bash script that will create the bridge for you ( assuming two network interfaces )

**Note:** Before you attept to run this script, you must first disable dhcp on the interface facing the router. This prevents the raspberry pi from acting like a host itself.

Assuming "eth1" is plugged into your router, open up the following file on your raspberry pi `sudo vim /etc/dhcpcd.conf` and add the following line to the bottom

```
denyinterfaces eth1 
```

Now reboot the raspberry pi for the changes to take effect.

#### Step2: 

Ok now that we have made sure the interface plugged into the router does not try to use DHCP we can run our script to create the bridge :)


```bash
sudo ./create-bridge.sh
```

This will create the bridge interface and bring it up!

#### Step3

Now plug your printer into one interface and the router into another


### Python Installation

Its reccomended that you set up a viruall python envirnment.

Run the following in the root of the project.

```bash
python3.9.2 -m venv venv
```

The above will set up a virtual envirnment directory. Next you simply activate it.

```bash
source venv/bin/activate
```

This will activate the virtual envirnment. Now all thats left is to install the dependencies

```bash
python -m pip install -r requirements.txt
```


## Running

The `logger.py` script will log any reciepts sent to the printer. In order to run you must first figure out the IP address of the POS ( Purchase Of Sale ) device and the Printer.

Once you have those IP addresses, update the two variables in the `logger.py` file

```python
# IP addresses for configuration
printer_ip = "192.168.0.101"
pos_ip = "192.168.0.106"
```

Now that we have the ips set its time to run the progarm


```bash
sudo venv/bin/python logger.py 
``

**Note** Its important to use sudo so it can access the interfaces
