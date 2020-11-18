The `idle_checker` script can run in the background and shutdown a VM if load stays below a certain threshold (0.2 by default) for more than a certain time (60 minutes by default). This is useful for cloud VMs that are occasionally used for manual tasks or batch processing.


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

