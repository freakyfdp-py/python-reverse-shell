# Python Reverse Shell

This is a reverse shell.
- Custom commands:
* cls - clear
* help
* ping
* stop
- Customized command:
* ls / dir ( CUSTOM LAYOUT )
* cd

Just a `client.py` ( that the victim need to execute ), make the victim run it as admin if you want all permissions.
and the `server.py` that the attacker need to open, it just sends the commands to the client and receive the output.
( `server.py` NEEDS TO BE RAN AS ADMIN )
