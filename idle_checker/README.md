
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

