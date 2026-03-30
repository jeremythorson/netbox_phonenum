# Netbox_Phonenum Plugin
A Telephone Number Management Plugin for [NetBox](https://github.com/netbox-community/netbox).

> This plugin was forked from (and extends) the netbox_phonenum project:
> https://github.com/panaceya/netbox_phonenum
> (which, in turn was forked from the original phonebox_plugin:
> https://gitub.com/iDebugAll/phonebox_plugin)
> Compared to voipbox, this project extends the pools objects to also contain non-pool 'Number' objects.

## Compatibility

| NetBox Version | VoipBox Plugin Version | Netbox_phonenum Version |
|:--------------:|:----------------------:|:-----------------------:|
|  4.3.0-4.3.2   |     0.0.3              |                         |
|  4.3.0-4.3.3   |     0.0.4              |                         |
|  4.3.0-4.3.7   |     0.0.5              |                         |
|  4.3.0-4.5.0   |     0.0.6              |                         |
|  4.3.0-4.5.0   |     0.0.7              |                         |
|  4.4.X-4.5.X   |     0.0.8, 0.0.9       |      0.0.10             |


### Preview

![](docs/media/preview_01.png)


# Supported Features and Models


### Pool 

A 'Pool' represents a range of numbers, defined by inclusive 'start' and 'end' values for that range.
- Pools may be nested (i.e. pools can contain other pools).
- Pools may also contain 'Number' objects (described below).
- Child pool ranges must lie within the parent pool range.
- Pool ranges can not overlap with sibling pools under the same parent.
- Pools can can also represent a single number, if desired, by setting the 'start' and 'end value' to the same number. (This was the recommended approach for storing single numbers within the voipbox plugin.)
- Pool 'start' and 'end' values can consist of valid DTMF characters and leading plus sign for E.164 support:
  - leading plus ("+") sign (optional)
  - digits 0-9
  - characters A, B, C, D
  - pound sign ("#")
  - asterisk sign ("*")
- Pool 'start' and 'end' range numbers are stored without delimiters.
Number values can be not unique.
- A Pool can optionally be assigned Tenant, Site, Provider, and Region relationships.
- A Pool can contain an optional Description.
- A Pool can optionally be tagged with Tags.
- The plugin supports Bulk Edit and Delete operations for Pools.

### Numbers
A 'Number' is intended to represent a single phone number entry within a pool.
Numbers have the same formatting options and restrictions as pools, described above.

> Sample valid numbers/pool range delimeters: +12341234567, 1000, 123#2341234567, *100#.

### Voice Circuits

Voice Circuit is an entity on a voice-enabled device representing a physical or virtual connection to another voice-enabled device.
The plugin supports the following voice circuit types:
- SIP Trunk.
- Digital Voice Circuit (PRI/BRI/etc).
- Analog Voice Circuit (CO lines/etc).

A Voice Circuit must be assigned to an interface of a Device or Virtual Machine.

### Plugin API

The plugin introduces a NetBox REST API extension `/api/plugins/voipbox/`.<br/>
It supports all create, read, update, and delete operations for Numbers or Pools via `/api/plugins/netbox_phonenum/pools/` and '/api/plugins/netbox_phonenum/numbers/'.<br/>
The API is compatible with [pynetbox](https://github.com/digitalocean/pynetbox):
```
>>> nb.plugins.voipbox.pool.get(1)
```
# Installation

General installation steps and considerations follow the [official guidelines](https://netbox.readthedocs.io/en/stable/plugins/).

### Package Installation from PyPi

Assuming you use a Virtual Environment for Netbox:
```
$ source /opt/netbox/venv/bin/activate
(venv) $ pip3 install netbox-phonenum
```

### Package Installation from Source Code
The source code is available on [GitHub](https://github.com/jeremythorson/netbox_phonenum).<br/>
Download and install the package. Assuming you use a Virtual Environment for Netbox:
```
$ git clone https://github.com/jeremythorson/netbox_phonenum.git
$ cd netbox_phonenum
$ source /opt/netbox/venv/bin/activate
(venv) $ pip3 install .
```

To ensure NextBox UI plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the NetBox root directory (alongside `requirements.txt`) and list the `netbox_phonenum` package:

```no-highlight
# echo netbox_phonenum >> local_requirements.txt
```

### Enable the Plugin
In a global Netbox **configuration.py** configuration file, update or add PLUGINS parameter:
```python
PLUGINS = [
    'netbox_phonenum',
]
```

### Collect Static Files
The Plugin contains static files for topology visualization. They should be served directly by the HTTP frontend. In order to collect them from the package to the Netbox static root directory use the following command:
```
(venv) $ cd /opt/netbox/netbox/
(venv) $ python3 manage.py collectstatic
```

### Apply Database Migrations

Apply database migrations with Django `manage.py`:
```
(venv) $ python3 manage.py migrate
```

### Restart Netbox
Restart the WSGI service to apply changes:
```
sudo systemctl restart netbox
```

# Installation with Docker
The Plugin may be installed in a Netbox Docker deployment. 
The package contains a Dockerfile for [Netbox-Community Docker](https://github.com/netbox-community/netbox-docker) extension. Latest-LDAP version is used by default as a source.<br/>
Download the Plugin and build from source:
```
$ git clone https://github.com/jeremythorson/netbox_phonenum
$ cd netbox_phonenum
$ docker build -t netbox-custom .
```
Update a netbox image name in **docker-compose.yml** in a Netbox Community Docker project root:
```yaml
services:
  netbox: &netbox
    image: netbox-custom:latest
```
Update a **configuration.py**. It is stored in netbox-docker/configuration/ by default. Update or add PLUGINS parameter and PLUGINS_CONFIG parameter as described above.

Rebuild the running docker containers:
```
$ cd netbox-docker
$ docker-compose down
$ docker-compose up -d
```
Netbox Community Docker setup performs static files collection on every startup. No manual actions required.
