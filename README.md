<img src="https://raw.githubusercontent.com/BirknerAlex/hacs_1komma5grad/main/images/icon.png" alt="1KOMMA5GRAD Logo" title="1KOMMA5GRAD Home Assistant Integration" align="right" height="60" />

# 1KOMMA5GRAD Home Assistant Integration

This is a custom integration for [Home Assistant](https://www.home-assistant.io/) to integrate 1KOMMA5GRAD 
into your Home Assistant instance.

This integration is not related to 1KOMMA5GRAD.



## Installation

### Automatic:
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Sergey842248&repository=hacs_1komma5grad)

### Manual:
1. Navigate in your Home Assistant frontend to **Supervisor** -> **Settings** -> **HACS** -> **Custom repositories** -> **Paste ```https://github.com/Sergey842248/hacs_1komma5grad```** -> choose **Integration** -> **Click "ADD"**
3. **Reload** the site
4. Find/Search the **"1KOMMA5GRAD"** add-on and click it.
5. Click on the **"INSTALL"** button.


## Support
### Supported devices
- 1KOMMA5GRAD Heartbeat 2024 (gen 2)
  
### Unsupported devices
- 1KOMMA5GRAD Heartbeat 2024 (gen 1) (for this device use https://github.com/derlangemarkus/1komma5grad_ha) 



## Features

### Sensors
#### Grid 
- Grid Consumption
- Grid Feed In
- Grid Power

#### Power
- Power Consumption
- Power Production
</br>

### Controls
#### Modes
- Heartbeat: Toggle Automatic Mode
- Battery: Control Battery Mode (Feed In, Self Consumtion, Backup, Auto)
