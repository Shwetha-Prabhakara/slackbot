from fabric.api import *
import re
env.hosts=['nimbus-gateway.eng.vmware.com']
env.user=''# Active Directory username
env.password=''# Active Directory password
vm_name=""

def find_vcenter(output):
    for x in reversed(output.splitlines()):
      if re.search('"done"',x):
          pass
      elif re.search('".*: %s"'%vm_name,x):
          return "Found......"+x.strip('"')
          break;
      elif re.search('".*:.*"',x):
          pass
      else:
           break;
    return False

def check():
    global vm_name
    print("checking Sc datacenter........")
    with hide('output','running'),settings(prompts={'\n> ':'/this.children.each{|k,v| begin; if v.is_a?(VIM); '+
                                'v.children.first[1].children["vms"].children["CoreOS"].children.each{|vm,_| p "#{k}: #{vm}";}; end; rescue; next; end;};p"done";exit;'
                           ,'/dinesha> ': 'cd /'}):
        output=run('NIMBUS_LOCATION=sc NIMBUS_CONTEXTS=cat,general /mts/git/bin/nimbus-rvc')
    if output.return_code !=0:
        return "Error checking sc2"
    result=find_vcenter(output)
    if result:
        return result
    print("Checking Wdc datacenter.....")
    with hide('output','running'),settings(prompts={'\n> ':'/this.children.each{|k,v| begin; if v.is_a?(VIM); '+
                                'v.children.first[1].children["vms"].children["CoreOS"].children.each{|vm,_| p "#{k}: #{vm}";}; end; rescue; next; end;};p"done";exit;'
                           ,'/dinesha> ': 'cd /'}):
        output=run('NIMBUS_LOCATION=wdc NIMBUS_CONTEXTS=general /mts/git/bin/nimbus-rvc')
    if output.return_code != 0:
        return "Error checking wdc"
    result = find_vcenter(output)
    if result:
        return result
    return "No Matches"


def search():
    global vm_name
    vm_name=raw_input("Enter the minion name.....")
    vm_name.strip("\n")
    if len(vm_name)>0:
        answer=execute(check)
        answer=answer['nimbus-gateway.eng.vmware.com']
        print(answer)

if __name__=='__main__':
    search()
