
#### [CentOS 7](https://geekflare.com/systemd-start-services-linux-7/) - To run shutdown_if_idle automatically on startup:

1. Copy `shutdown_if_idle` to `/usr/local/sbin/shutdown_if_idle`
1. Create `/etc/systemd/system/shutdown_if_idle.service` which contains

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
