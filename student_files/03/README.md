# Homework

Modify existing playbooks:

1. Install snmpd
    * Configure snmpd via template module
    * Get snmp community string as from variable
2. Open via template module & loops ports:
    * 161 udp
    * 443 tcp
3. Reload iptables only if is modified.
4. Make your playbook idempotent


# Notice

ansible execution on localhost

ansible-playbook -c local -i localhost, provision_me.yml 