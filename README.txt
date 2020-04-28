There are four different python codes and they are related to the vendor of the devices.

	VENDORS:
	--------

	Vendor: HP ARUBA / Software: ArubaOS
	Vendor: HPE / Software: Comware
	Vendor: JUNIPER / Software: Junos
	Vendor: COMNET / Software: ComnetOS

Each script collect devices attributes from a text file and convert them into a dictionary and then Netmiko is used to SSH to the devices and apply some configuraton (mostly related to devices local user credentials).
