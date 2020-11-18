
### INSTALL

To install idle_checker on any Linux or MacOSX instance with cron:

1. Check that you can run  `/your/path/to/bin-utils/idle_checker/shutdown_if_idle` directly

2. Add shutdown_if_idle to root crontab

```
sudo su  # switch to root  
crontab -e  # edit crontab
#  add this line:
@reboot /your/path/to/bin-utils/idle_checker/shutdown_if_idle
```

3. reboot

