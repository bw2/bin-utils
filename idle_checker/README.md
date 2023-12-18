The `idle_checker` script can run in the background and shutdown a VM if load stays below a certain threshold (0.4 by default) for more than a certain time (30 minutes by default). This is useful for cloud VMs that are occasionally used for manual tasks or batch processing.


### INSTALL

To install idle_checker on any Linux or MacOSX instance with cron:

1. Check that you can run  `/your/path/to/bin-utils/idle_checker/shutdown_if_idle` directly

2. Edit root crontab
```
sudo crontab -e  # edit root crontab
```
3. Add the line below, then save and exit the editor 
```
@reboot /your/path/to/bin-utils/idle_checker/shutdown_if_idle
```
4. reboot


# INSTALL ON UBUNTU v20

To install on Ubuntu with systemd, copy the `shutdown_if_idle` script from this repo to to /usr/local/sbin/shutdown_if_idle 

1. Make the script executable
```
chmod 777 /usr/local/sbin/shutdown_if_idle
```

2. Make the script run at startup  

```
# cat /etc/systemd/system/shutdown_if_idle.service
[Unit]
Description=Shutdown machine if idle
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/sbin/shutdown_if_idle
TimeoutStartSec=0
Restart=on-abort

[Install]
WantedBy=default.target
```
