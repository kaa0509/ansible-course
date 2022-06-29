#!/usr/bin/python
# -*- coding: utf-8 -*-

#from __future__ import (absolute_import, division, print_function)
#__metaclass__ = type
import os
import filecmp
import shutil
from ansible.module_utils.basic import AnsibleModule

def restore(command, syspath):
        cmd = command + "-restore " + syspath
        try:
            os.system(cmd)
            return {"changed":True}
        except Exception as e:
            return {"changed":False, "error":e}

def compare_files(syspath, path):
    file1 = open(syspath, "r")
    file2 = open(path, "r")

    for line1 in file1:
        for line2 in file2:
            if line1 != line2:
                file1.close()
                file2.close()
                return False
            break
    file1.close()
    file2.close()
    return True
                

def change_file(syspath, path):
    try:
        shutil.copy(path, syspath)
    except Exception as e:
        return {"changed":False, "error":e}


def main():
    module_args = dict(
        name=dict(type='str', required=True),
        path=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    
    if module.check_mode:
        module.exit_json(**result)
    
    path = module.params["path"]
    if path:
        if not os.path.exists(path):
            return module.fail_json(msg='File not exist!!!', **result)
    else:
        return module.fail_json(msg='Path not set!!!', **result)

    command = module.params["name"]

    if command:
        if command == 'iptables':
            syspath = '/etc/sysconfig/iptables'
            if syspath == path:
                result = restore(command, syspath)
            else:
                if not compare_files(syspath, path):
                    change_file(syspath, path)
                    result = restore(command, syspath)
        elif command == 'ip6tables':
            syspath = '/etc/sysconfig/ip6tables'
            if syspath == path:
                result = restore(command, syspath)
            else:
                if not compare_files(syspath, path):
                    change_file(syspath, path)
                    result = restore(command, syspath)                 
        else:
            return module.fail_json(msg='Name must be iptables or ip6tables')
    else:
        return module.fail_json(msg='Name not set')  
    


    module.exit_json(**result)


if __name__ == '__main__':
    main()