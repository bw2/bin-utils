
#### [CentOS 7](https://geekflare.com/systemd-start-services-linux-7/) - To run shutdown_if_idle as a service:

1. Copy `shutdown_if_idle` to `/usr/local/sbin/shutdown_if_idle`
2. Create `/etc/systemd/system/shutdown_if_idle.service` which contains

```
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
3. Run 
```
cd /etc/systemd/system
sudo systemctl enable shutdown_if_idle.service
sudo systemctl start shutdown_if_idle
```
