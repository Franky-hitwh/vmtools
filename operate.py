#!/usr/bin/env python
import shutil
import sys
import os
import xml.etree.ElementTree as ET
import traceback
from database import *


def undefine(dst_disk):

    command = 'virsh undefine' + ' ' + dst_disk
    flag = os.system(command)

    if flag == 0:
        print "The VM has been undefined."
    else:
        print "VM undefined failed."
        sys.exit()


def create_guest(temp_xml_path):
    print 'creating guest...'

    command = "virsh define" + ' ' + temp_xml_path
    flag = os.system(command)
    if flag == 0:
        print "The VM has been created at %s." % temp_xml_path
    else:
        print "VM created failed."
        sys.exit()

    command_rm = "rm" + ' ' + temp_xml_path
    os.system(command_rm)
    print "The XML file has been deleted."
    return True


def random_mac():
    import random
    mac = [
        0x52,
        0x54, 0x00,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def create_xml(dst_disk, disk_path, virtual_cpus, memory_size, listen_port):

    print 'creating xml...'
    temp_name = 'temp.xml'
    #command_cp = 'cp' + ' ' + XML_PATH + ' ' + temp_name
    temp_xml_path = temp_name
    #flag = os.system(command_cp)
    #if flag != 0:
        #print "copy xml file failed"
        #sys.exit()
    try:
        shutil.copy(XML_PATH, temp_name)
    except Exception, e:
        print e
        sys.exit()

    try:
        tree = ET.parse(temp_xml_path)
# root = tree.getroot()
        name = tree.find("name")
        name.text = dst_disk

        mem = tree.find("memory")
        cmem = tree.find("currentMemory")
        cmem.text = str(memory_size * 1024)
        mem.text = str(memory_size * 1024)

        vcpu = tree.find("vcpu")
        vcpu.text = str(virtual_cpus)

        file_path = tree.findall(".//source")
        disk = file_path[0]
        disk.set("file", disk_path)

        devices = tree.find("devices")
        interface = devices.find("interface")
        mac = interface.find("mac")
        mac.set("address", random_mac())

        graphics = devices.find("graphics")
        graphics.set("port", str(listen_port))

        tree.write(
            temp_xml_path, encoding="UTF-8", xml_declaration=None, method="xml"
        )

    except Exception:
        traceback.print_exc()
        sys.exit()
    print "XML created successfully at: %s" % temp_xml_path
    return temp_xml_path


def create_disk(src_disk, dst_disk):
    
    print 'creating disk...'
    src_path = IMAGE_PATH + src_disk
    dest_path = IMAGE_PATH + dst_disk
    if not os.path.exists(src_path):
        print 'source file is not exists. Please check the path.'
        sys.exit()

    if not os.path.exists(dest_path):
        #command_cp = 'cp' + ' ' + src_path + ' ' + dest_path
        #flag = os.system(command_cp)
        try:
            shutil.copy(src_path, dest_path)
        except Exception, e:
            print e
            sys.exit()
    
    print "Virtual Disk File has been created successfully"
    print "The Disk is at: %s" % dest_path

    return dest_path


def main(argv):
    #get parameters
    username = argv['user']
    src_disk = argv['src_disk']
    dst_disk = argv['dst_disk']
    virtual_cpus = argv['cpu']
    memory_size = argv['memory']
    listen_port = argv['port']
    argv['vnc'] = VM_SERVER + ':' + str(int(listen_port) - 5900)
    disk_size = 100

    db = Database()
    #print username, src_disk, dst_disk, virtual_cpus, memory_size, listen_port
    if argv['create']:
        disk_path = create_disk(src_disk, dst_disk)
        temp_xml_path = create_xml(dst_disk, disk_path, virtual_cpus, memory_size, listen_port)
        create_guest(temp_xml_path)
        db.insert_to_db(argv)

    elif argv['delete']:
        if not os.path.exists(IMAGE_PATH + dst_disk):
            print 'The dest image is not exists.'
            sys.exit()
        db.delete_from_db(username, dst_disk)
        undefine(dst_disk)
    

IMAGE_PATH = '/var/lib/libvirt/images/'
XML_PATH = '/etc/libvirt/qemu/template.xml'
VM_SERVER = '172.29.152.146'
DB_SERVER = '172.29.152.15'
USER = 'root'
PASSWD = 'hitnslab'
DB_NAME = 'VMdb'
PORT = 3306

if __name__ == '__main__':
    """

        To run the script, you should prepare something:
        Image path: /var/lib/libvirt/images/        --your source disk
        XML path: /etc/libvirt/qemu/template.xml    --your template xml
        virtual machine server: 172.29.152.146      --VM server
        web server: 172.29.152.15                   --Web and Database server
        Database user: root

    """
    main(sys.argv)
