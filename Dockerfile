FROM netboxcommunity/netbox:latest-ldap

COPY ./netbox_phonenum /source/netbox_phonenum/netbox_phonenum/
COPY ./setup.py /source/netbox_phonenum/
COPY ./MANIFEST.in /source/netbox_phonenum/
COPY ./README.md /source/netbox_phonenum/
RUN /usr/local/bin/uv pip install --no-cache-dir /source/netbox_phonenum/
