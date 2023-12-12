####################################################################
# (C) Copyright 2023 Hewlett Packard Enterprise Development LP.
###################################################################

from __future__ import print_function
log_file = "/tmp/cminstaller.log"
dir_path = "/opt/hpe/wcconsole/be/cxt/Prevalidation"

import json
import os
import subprocess
import re
import platform
import sys
import socket
import argparse
from subprocess import PIPE, Popen
import logging
import shutil

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.handlers = []

file_handler = logging.FileHandler(log_file, mode='a')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

CONFIGURATION_LIST = []
INPUT_LIST = []
without_config_dict = {}
oracle_linux = []
sles = []
rhel = []
distro_name = None
distro_version = None
validation_failure = False
url = "https://github.com/HewlettPackard/serviceguard.git"

def read_input_file():
    try:
        line_output = ""
        global INPUT_LIST
        with open("pre_install_check.config" , "r") as input:
            for line in input.readlines():
                line_output = re.findall("#", line)
                if (not line_output) and (line_output != "\n"):
                    if line is not None:
                        INPUT_LIST.append(line.strip())
            return INPUT_LIST

    except Exception as ex:
         print("Exception in reading the input file",str(ex))
def write_to_json():
    try:
        global INPUT_LIST
        line_output = []
        node_list = []
        config_dict = {}
        for line in INPUT_LIST:
            if line.strip() == '':
                continue
            line_output.append(line.strip())
            for item in line_output:
                i = item.split('=')
                for j in i:
                    if ',' in j:
                        config_dict[i[0]] = i[1].split(',')
                    else:
                        config_dict[i[0]] = [i[1]]
        with open ("preconfig.json" , "w") as final:
            result = json.dumps(config_dict, indent = 4)
            final.write(result)
    except Exception as ex:
        print("Exception in writing to the input file",str(ex))

def execute_parser_functions():
    try:
        read_input_file()
        write_to_json()
    except Exception as ex:
        print("Exception in execute_parser_functions",str(ex))

def exit_onerror(msg):
   try:
       print("Exiting the script as: " + msg)
       sys.exit(0)
   except Exception as ex:
       print("Exception in exit_onerror " + str(ex))

def check_rpm():
    try:
        global dir_path
        cmd = "ls " + dir_path + "/PreconfigureCheck >/dev/null 2>&1"
        ret = os.system(cmd)
        if ret == 0:
            os.system('rm -rf /tmp/PreinstallCheck >/dev/null 2>&1')
            cmd2 = "mv " + dir_path + "/PreinstallCheck /tmp >/dev/null 2>&1"
        else:
            cmd2 = "mkdir -p " + dir_path + " >/dev/null 2>&1"
            os.system(cmd2)
    except Exception as ex:
        print("Exception in check_rpm function" + str(ex))

def copy_prevalidation_files():
    try:
        global dir_path
        file_path = os.getcwd()
        cmd2 = "cp -r " + file_path + "/PreinstallCheck " + dir_path
        link_flag = os.system(cmd2)
        if not link_flag == 0:
            log.log("ERROR: Failed to copy files")
        cmd2 = "chmod +x " + dir_path + "/PreinstallCheck/cmsgpreinstallcheck.py"
        out = os.system(cmd2)
        if out:
            logger.error("ERROR: failed to update permissions")
    except Exception as ex:
        print("Exception in copying prevalidation files" + str(ex))

def cleanup():
    try:
        cur_dir = os.getcwd()
        os.chdir('/tmp')
        dir_path = "serviceguard"
        exclude_dir1 = "PreinstallCheck"
        exclude_dir2 = ".git"
        subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
        subdirs = [d for d in subdirs if d != exclude_dir1 and d != exclude_dir2]
        for subdir in subdirs:
            shutil.rmtree(os.path.join(dir_path, subdir))
        os.chdir(cur_dir)    
    except Exception as ex:
        print("Exception in cleanup",str(ex))


def check_clone_status():
    try:
        clone_flag= get_config_data("git_clone")
        if 'yes' in clone_flag:
            git_cloning()
    except Exception as ex:
        print("Exception in check_clone_status", str(ex))
         
    
def git_cloning():
    try:
        global dir_path
        cur_dir= os.getcwd()
        git_present = os.system("git --version >/dev/null 2>&1") 
        if git_present != 0:
            logger.error("ERROR: Install git to continue")
            return
        os.chdir('/tmp')
        if os.system("ls serviceguard/PreinstallCheck >/dev/null 2>&1") == 0:
            git_update()
            action = "Updation"
        else:
            install_git_repo = os.system("git clone "+ url)
            if install_git_repo != 0:
                print("Proceeding without latest update")
                logger.error("ERROR: git repo specified does not exist")
                os.chdir(cur_dir)
                copy_prevalidation_files()
                return
            os.chdir('serviceguard/PreinstallCheck')
            action = "Cloning"
        flag = check_git_repo()
        if not flag:
            print(str(action) + " Successful")
            logger.info(str(action) + " Successful")
        else:
            print(str(action)+ " Unsuccessful")
            logger.info(str(action) + " Unsuccessful")
        cleanup()
        os.chdir(cur_dir)
        
    except Exception as ex:
        print("Exception inside git_cloning function" + str(ex))

def git_update():
    try:
        os.chdir('serviceguard/PreinstallCheck')
        git_update_flag = os.system("git pull origin >/dev/null 2>&1")
        if git_update_flag:
            logger.error("ERROR: Failed to update git contents")    
    except Exception as ex:
        print("Exception while updating" +str(ex))

def check_git_repo():
    try:
        file1 = os.path.exists("cmsgpreinstallcheck.py")
        file2 = os.path.exists("preinstallUtils.py")
        file3 = os.path.exists("pre_install_check.config")
        file4 = os.path.exists("DB.json")
        if file1 and file2 and file3 and file4:
            os.chdir('/tmp/serviceguard')
            cmd = "cp -r PreinstallCheck " + dir_path + " >/dev/null 2>&1"
            os.system(cmd)
            cmd2 = "chmod +x " + dir_path + "/PreinstallCheck/cmsgpreinstallcheck.py"
            out = os.system(cmd2)
            if out:
                logger.error("ERROR: failed to update permissions")
            return 0
        else:
            logger.error("ERROR: Git repo contents are not correct")
            return 1
    except Exception as ex:
        print("Exception while checking git Repository "+ str(ex)) 

def read_node_names(nodes):
    try:
        global dir_path
        nodes_str = ','.join(nodes)
        exec_path = dir_path + "/PreinstallCheck"
        os.chdir(exec_path)
        update_node_names(nodes_str)
    except Exception as ex:
        print("Exception while reading node names" + str(ex))

def update_node_names(nodes_str):
    try:
        with open ("pre_install_check.config", "a") as file:
            data = "validation_nodes=" + nodes_str
            file.write(data)
    except Exception as ex:
        print("Exception while updating node names" + str(ex))

def run_preinstall_check():
    try:
        check_file = os.path.exists("cmsgpreinstallcheck.py >/dev/null 2>&1")
        if check_file == 0:
            cmd = "./cmsgpreinstallcheck.py -p"
            return_code = os.system(cmd)
            if return_code != 0:
                return 1
            return 0
        return 1
    except Exception as ex:
        print("Exception while preinstall check" + str(ex))


def read_DB_file():
    try:
        with open("DB.json", "r") as input:
            data_dict = json.load(input)
            for key in data_dict:
                if key == 'OS':
                    for item in data_dict[key]:
                        for key2 in item:
                            if key2 == 'OracleLinux':
                                for item2 in item[key2]:
                                    oracle_linux.append(item2)
                            elif key2 == 'SLES':
                                for item2 in item[key2]:
                                    sles.append(item2)
                            elif key2 == 'RHEL':
                                for item2 in item[key2]:
                                    rhel.append(item2)
    except Exception as ex:
        print("Exception in reading contents of DB.json file",str(ex))

def read_orcl_linux():
    try:
        ver_list = []
        res = []
        valid_orcl_os = []
        for i in oracle_linux:
            for key in i:
                if key == 'Version':
                    ver_list.append(i.get(key))
        for item in ver_list:
            c = item.strip("[]").split(".")
            version = "Oracle_Linux " + c[0]
            res.append(version)
        valid_orcl_os = list(set(res))
        return valid_orcl_os
    except Exception as ex:
        print("Exception in reading oracle_linux content",str(ex))

def read_sles():
    try:
        ver_list = []
        res = []
        valid_sles_os = []
        for i in sles:
            for key in i:
                if key == 'Version':
                    ver_list.append(i.get(key))
        for item in ver_list:
            a = item.strip("[]").split(".")
            version = "SLES " + a[0][:2]
            res.append(version)
        valid_sles_os = list(set(res))
        return valid_sles_os
    except Exception as ex:
        print("Exception in reading sles content",str(ex))

def read_rhel():
    try:
        ver_list = []
        res = []
        valid_rhel_os = []
        for i in rhel:
            for key in i:
                if key == 'Version':
                    ver_list.append(i.get(key))
        for item in ver_list:
            b = item.strip("[]").split(".")
            version = "RedHat " + b[0]
            res.append(version)
        valid_rhel_os = list(set(res))
        return valid_rhel_os
    except Exception as ex:
        print("Exception in reading rhel content",str(ex))

def serviceguard_os_list():
    try:
        valid_os_list = []
        read_DB_file()
        orcl_os_version = read_orcl_linux()
        sles_os_version = read_sles()
        rhel_os_version = read_rhel()
        valid_os_list = orcl_os_version + sles_os_version + rhel_os_version
        return valid_os_list
    except Exception as ex:
        print("Exception in serviceguard_os_list function",str(ex))

def get_os(Filename):
    try:
        line = None
        content = None
        distro_name = None
        distro_version = None
        os_name = None
        if os.path.exists(Filename):
            with open(Filename) as f:
                for line in f:
                    content = line.split("=")
                    if 'NAME' in content:
                        if 'Red Hat' in content[1] or 'CentOS' in content[1]:
                            distro_name = 'RedHat'
                        elif 'SLES' in content[1]:
                            distro_name = 'SLES'
                        elif 'Oracle' in content[1]:
                            distro_name = 'Oracle_Linux'
                    if 'VERSION_ID' in content:
                        distro_version = content[1].replace('"', '')
                        distro_version = distro_version.rstrip().split('.')[0]
        if distro_version is None:
            fileName = "/etc/redhat-release";
            if os.path.exists(fileName):
                distro_name = 'RedHat'
                with open("/etc/redhat-release") as f:
                    line = f.read()
                    line = line.split()
                    for i in range(0, len(line)):
                        content = line[i]
                        if content.lower() == 'release':
                            if(i + 1 < len(line)):
                                distro_version = line[i+1].strip().split('.')[0]
                                break
        if distro_version is None:
            fileName = "/etc/SuSE-release";
            if os.path.exists(fileName):
                distro_name = 'SLES'
                select_yum_or_zypper = "zypper"
                with open("/etc/SuSE-release") as f:
                    for line in f:
                        content = line.split("=")
                        if 'VERSION' in str(content):
                            distro_version = content[1].strip().rstrip()
                            break
        return distro_name, distro_version
    except Exception as ex:
        print("Exception in get_os function" + str(ex))

def is_container_environment(node,remote_node_flag):
    try:
        out, return_code = run_shell_command_on_nodes("ls /.dockerenv", remote_node_flag,node)
        if return_code == 0:
            return 0
        out, return_code = run_shell_command_on_nodes("cat /proc/1/cgroup",remote_node_flag,node)
        if any('docker' in line or 'kubepods' in line for line in out.splitlines()):
            return 0
        out, return_code = run_shell_command_on_nodes("cat /proc/self/mountinfo", remote_node_flag,node)
        if any('docker' in line or 'containers' in line for line in out.splitlines()):
            return 0
        return 1
    except Exception as ex:
        print("Exception inside is_container_environment function: " + str(ex))

def get_hostName():
    try:
        hostname = None
        if socket.gethostname():
            hostname = socket.gethostname().split(".")[0]
            return hostname
    except Exception as ex:
        print("Exception in get_hostName " + str(ex))

def get_shortname(hostname):
    try:
        #print "inside get short name::"
        if hostname:
            name = hostname.split(".")[0]
            #print "name::", name
            if name is None:
                return hostname
            return name
    except Exception as ex:
        print("Exception in get_hostName " + str(ex))

def compare_remote_node_file(node,remote_node_flag,each_file_path):
    try:
        cmd = "/usr/bin/ssh -l root " + node + " cat "+ each_file_path + "|" + "diff - " + each_file_path
        response = os.system(cmd)
        return response
    except Exception as ex:
        print("Exception in compare_remote_node_file" + str(ex))

def run_shell_command_on_nodes(cmd, remote_node_flag, node_to_run):
    try:
        stdout = ""
        stderr = ""
        shell = True
        env = None
        if remote_node_flag == True:
            cmd = "/usr/bin/ssh -l root " + str(node_to_run) + " " + str(cmd)
        else:
            cmd = str(cmd)
        proc = Popen(cmd, shell=shell, cwd=None, stdout=PIPE, stderr=PIPE, env=env, universal_newlines=True)
        stdout, stderr = proc.communicate()
        return (stdout + stderr), proc.returncode
    except Exception as ex:
        print("Exception in run_shell_command_on_remote " + str(ex))

def run_shell_command_on_local(cmd, remote_node_flag, node_to_run):
    try:
        result = ""
        result = subprocess.check_output(cmd)
        if result:
            return result,0
        else:
            return result,1
    except Exception as ex:
        print("Exception in run_shell_command_on_local " + str(ex))

def run_os_related_commands_on_shell(hostName):
    try:
        response = os.system("ping -c 1 " + hostName + " >/dev/null 2>&1")
        result = " "
        if response != 0:
            return result, 1
        else:
            return result, 0
    except Exception as ex:
        print("Exception in run_os_related_commands_on_shell " + str(ex))

def print_detailed_summary(output,log_option):
    try:
        global validation_failure
        for i in output:
            preinstall_log_option = log_option
            if preinstall_log_option == False:
                filt_keys = ['test_case_name', 'overall_status']
                res = [i[key] for key in filt_keys]
                final = res[0] + " : " + res[1]
                print(final)
            else:
                filt_keys = ['test_case_name', 'overall_status', 'result']
                res = [i[key] for key in filt_keys]
                final = res[0] + " : " + res[1]
                print(final)
                print()
                for j in res[2]:
                    filt_keys1 = ['msg', 'msg_status']
                    res1 = [j[key] for key in filt_keys1]
                    for i in res1:
                        if(i == "ERROR"):
                            validation_failure = True
                    res2 = res1[0]
                    for k in res2:
                        final2 = res1[1] + " : " + k
                        print(final2)
                print()
        if validation_failure == True:
            return 1
        return 0
    except Exception as ex:
        print("Exception while printing detailed summary" + str(ex))

def get_config_data(key):
    try:
        if not key:
            return None
        with open('preconfig.json') as f:
            data = json.load(f)
        return data.get(key, "")
    except Exception as ex:
        print ("Exception in get_config_data" + str(ex))

def check_reachability(node,remote_node_flag):
    logger.debug("Entering check_reachability function on node " + node)
    try:
        output_dictionary = {}
        output_dictionary["test_case_name"] = "1. Check nodes reachability"
        overall_status = True
        result = []
        final_output =[]
        return_report = {}
        msg1 = []
        cmd = "ping -c 1 " + node + " >/dev/null 2>&1"

        out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)

        if return_code != 0:
            overall_status = False
            return_report[node]=False
            return_report["msg_status"] = "WARNING"
            str1 = "Node " + str(node) + " is not reachable"
            logger.warning(str1)
            msg1.append(str1)
        else:
            return_report[node]=True
            return_report["msg_status"] = "INFO"
            str1 = "Node " + str(node) + " is reachable"
            logger.info(str1)
            msg1.append(str1)
        return_report["msg"] = msg1
        return_report["node_name"] = node

        result.append(return_report)

        output_dictionary["result"] = result

        if overall_status == False:
            output_dictionary["overall_status"] = "FAILED"
        else:
            output_dictionary["overall_status"] = "OK"

        final_output.append(output_dictionary)
        return final_output

    except Exception as ex:
        overall_status = False
        return_report["msg_status"] = "ERROR"
        str1 = "Exception in check_reachability"
        logger.error(str1)
        msg1.append(str1)
        return_report["msg"] = msg1
        return_report["node_name"] = node

        result.append(return_report)

        output_dictionary["result"] = result

        if overall_status == False:
            output_dictionary["overall_status"] = "FAILED"
        else:
            output_dictionary["overall_status"] = "OK"

        final_output.append(output_dictionary)
        return final_output

def check_rpm_installed(node,remote_node_flag):
    logger.debug("check_rpm_installed function on node " + node)
    try:
        global distro_name
        global distro_version
        output_dictionary = {}
        output_dictionary["test_case_name"] = "3. Check rpms installed"
        overall_status = True
        result = []
        final_output =[]
        return_report = {}
        msg1 = []
        user_rpms = []
        common_rpms = ['sg3_utils','net-tools','net-snmp','java','lsof','psmisc','rpm','findutils','openssl','perl','sqlite']
        rh7_rpms = ['authd','xinetd','json-c']
        rh8_9rpms = ['authd','expect','json-c']
        sles12_rpms = ['pidentd','libjson-c2','xinetd','dmidecode','time']
        sles15_rpms = ['pidentd','libjson-c3','expect','dmidecode','time']
        user_rpms = get_config_data("rpms_to_check")
        container_rpms= ['iproute','iputils','net-tools','openssh-clients','bind-utils']
        is_container = is_container_environment(node,remote_node_flag)
        if is_container == 0:
             for rpm_name in container_rpms:
                if rpm_name == "iproute":
                    cmd = "rpm -qi " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 4.0.0 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        for line in tmp_file:
                            if line.startswith('Version'):
                                a = line.split(':')
                                b = a[1].split(".")
                                if int(b[0]) == 4:
                                    if not int(b[1]) >= 0:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm_name) + " of version 4.0.0 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                                elif not int(b[0]) > 4:
                                    overall_status = False
                                    return_report[node]=False
                                    return_report["msg_status"]="WARNING"
                                    str1="rpm " + str(rpm_name) + " of version 4.0.0 or higher is required."
                                    logger.warning(str1)
                                    msg1.append(str1)
                        tmp_file.close()
                elif rpm_name == "iputils":
                    cmd = "rpm -qi " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 20071127 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        for line in tmp_file:
                            if line.startswith('Version'):
                                a = line.split(':')
                                if not int(a[1]) >=20071127 :
                                    overall_status = False
                                    return_report[node]=False
                                    return_report["msg_status"]="WARNING"
                                    str1="rpm " + str(rpm_name) + " of version 20071127 or higher is required."
                                    logger.warning(str1)
                                    msg1.append(str1)
                        tmp_file.close()
                elif rpm_name == "net-tools":
                    cmd = "rpm -qi " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 1.6 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        for line in tmp_file:
                            if line.startswith('Version'):
                                a = line.split(':')
                                if not float(a[1]) >= 1.6:
                                    overall_status = False
                                    return_report[node]=False
                                    return_report["msg_status"]="WARNING"
                                    str1="rpm " + str(rpm_name) + " of version 1.6  or higher is required."
                                    logger.warning(str1)
                                    msg1.append(str1)
                        tmp_file.close()
                elif rpm_name == "bind-utils":
                    cmd = "rpm -qi " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 9.10.00 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        for line in tmp_file:
                            if line.startswith('Version'):
                                a = line.split(':')
                                b = a[1].split(".")
                                if int(b[0]) == 9:
                                    if not int(b[1]) >= 10:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm_name) + " of version 9.10.00 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                                elif not int(b[0]) > 9:
                                    overall_status = False
                                    return_report[node]=False
                                    return_report["msg_status"]="WARNING"
                                    str1="rpm " + str(rpm_name) + " of version 9.10.00 or higher is required."
                                    logger.warning(str1)
                                    msg1.append(str1)
                        tmp_file.close()
                elif rpm_name == "openssh-clients":
                    cmd = "rpm -qi " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 4.0  or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        for line in tmp_file:
                            if line.startswith('Version'):
                                a = line.split(':')
                                b = a[1].split("p")
                                if float(b[0]) == 4.0:
                                    if not int(b[1]) >= 0:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm_name) + " of version 4.0.0 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                                elif not float(b[0]) > 4.0:
                                    overall_status = False
                                    return_report[node]=False
                                    return_report["msg_status"]="WARNING"
                                    str1="rpm " + str(rpm_name) + " of version 4.0.0 or higher is required."
                                    logger.warning(str1)
                                    msg1.append(str1)
                        tmp_file.close()
        if distro_name == "RedHat" and int(distro_version) <= 7:
            overall_status = False
            return_report[node]=False
            return_report["msg_status"]="ERROR"
            str1="Distro version is unsupported to check rpms."
            logger.error(str1)
            msg1.append(str1)
        elif distro_name == "RedHat" or distro_name == "Oracle_Linux":
            for rpm_name in common_rpms:
                if rpm_name == "sg3_utils":
                    cmd = "rpm -qi " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 1.20 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        for line in tmp_file:
                            if line.startswith('Version'):
                                a = line.split(':')
                                if not float(a[1]) >= 1.20:
                                    overall_status = False
                                    return_report[node]=False
                                    return_report["msg_status"]="WARNING"
                                    str1="rpm " + str(rpm_name) + " of version 1.20 or higher is required."
                                    logger.warning(str1)
                                    msg1.append(str1)
                        tmp_file.close()
                elif rpm_name == "net-snmp":
                    cmd = "rpm -qi " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 5.7 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        for line in tmp_file:
                            if line.startswith('Version'):
                                a = line.strip().split(':')
                                b = a[1].split(".")
                                if int(b[0]) == 5:
                                    if not int(b[1]) >= 7:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm_name) + " of version 5.7 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                                elif not int(b[0]) > 5:
                                    overall_status = False
                                    return_report[node]=False
                                    return_report["msg_status"]="WARNING"
                                    str1="rpm " + str(rpm_name) + " of version 5.7 or higher is required."
                                    logger.warning(str1)
                                    msg1.append(str1)
                        tmp_file.close()
                elif rpm_name == "rpm":
                    cmd = "rpm -qi " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 4.4 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        for line in tmp_file:
                            if line.startswith('Version'):
                                a = line.strip().split(':')
                                b = a[1].split('.')
                                if int(b[0]) == 4:
                                    if not int(b[1]) >= 4:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm_name) + " of version 4.4 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                                elif not int(b[0]) > 4:
                                    overall_status = False
                                    return_report[node]=False
                                    return_report["msg_status"]="WARNING"
                                    str1="rpm " + str(rpm_name) + " of version 4.4 or higher is required."
                                    logger.warning(str1)
                                    msg1.append(str1)
                        tmp_file.close()
                elif rpm_name == "java":
                    cmd = str(rpm_name) + " -version"
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 1.8 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        first_line = tmp_file.readline().strip('\n')
                        a = first_line.split('"')
                        b = a[1].split('.',2)
                        if int(b[0]) == 1:
                            if not int(b[1]) >= 8:
                                overall_status = False
                                return_report[node]=False
                                return_report["msg_status"]="WARNING"
                                str1="rpm " + str(rpm_name) + " of version 1.8 or higher is required."
                                logger.warning(str1)
                                msg1.append(str1)
                        elif not int(b[0]) >= 1:
                            overall_status = False
                            return_report[node]=False
                            return_report["msg_status"]="WARNING"
                            str1="rpm " + str(rpm_name) + " of version 1.8 or higher is required."
                            logger.warning(str1)
                            msg1.append(str1)
                        tmp_file.close()
                else:
                    cmd = "rpm -q " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if not out.startswith(str(rpm_name)):
                        cmd2 = "rpm -qa | grep " + str(rpm_name)
                        out2,return_code2 = run_shell_command_on_nodes(cmd2,remote_node_flag,node)
                        if not out2.startswith(str(rpm_name)):
                            overall_status = False
                            return_report[node]=False
                            return_report["msg_status"]="WARNING"
                            str1="rpm " + str(rpm_name) + " is required."
                            logger.warning(str1)
                            msg1.append(str1)
            if int(distro_version) == 7:
                for rpm1 in rh7_rpms:
                    if rpm1 == "authd":
                        cmd = "rpm -qi " + str(rpm1)
                        out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                        if return_code != 0:
                            overall_status = False
                            return_report[node]=False
                            return_report["msg_status"]="WARNING"
                            str1="rpm " + str(rpm1) + " of version 1.4.3 or higher is required."
                            logger.warning(str1)
                            msg1.append(str1)
                        else:
                            tmp_file = open('tmp.txt', 'w')
                            tmp_file.write(out)
                            tmp_file.close()
                            tmp_file = open('tmp.txt', 'r')
                            for line in tmp_file:
                                if line.startswith('Version'):
                                    a = line.strip().split(':')
                                    b = a[1].split('.')
                                    if int(b[0]) == 1:
                                        if int(b[1]) == 4:
                                            if not int(b[2]) >= 3:
                                                overall_status = False
                                                return_report[node]=False
                                                return_report["msg_status"]="WARNING"
                                                str1="rpm " + str(rpm1) + " of version 1.4.3 or higher is required."
                                                logger.warning(str1)
                                                msg1.append(str1)
                                        elif not int(b[1]) > 4:
                                            overall_status = False
                                            return_report[node]=False
                                            return_report["msg_status"]="WARNING"
                                            str1="rpm " + str(rpm1) + " of version 1.4.3 or higher is required."
                                            logger.warning(str1)
                                            msg1.append(str1)
                                    elif not int(b[0]) > 1:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm1) + " of version 1.4.3 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                    else:
                        cmd = "rpm -q " + str(rpm1)
                        out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                        if not out.startswith(str(rpm1)):
                            cmd2 = "rpm -qa | grep " + str(rpm1)
                            out2,return_code2 = run_shell_command_on_nodes(cmd2,remote_node_flag,node)
                            if not out2.starswith(str(rpm1)):
                                overall_status = False
                                return_report[node]=False
                                return_report["msg_status"]="WARNING"
                                str1="rpm " + str(rpm1) + " is required."
                                logger.warning(str1)
                                msg1.append(str1)
            elif int(distro_version) == 8:
                for rpm2 in rh8_9rpms:
                    cmd = "rpm -qi " + str(rpm2)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm2) + " of version 1.4.4-5.el8_0.1 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        if rpm2 == "authd":
                            tmp_file = open('tmp.txt', 'w')
                            tmp_file.write(out)
                            tmp_file.close()
                            tmp_file = open('tmp.txt', 'r')
                            for line in tmp_file:
                                if line.startswith('Version'):
                                    a = line.strip().split(':')
                                    b = a[1].split('.')
                                    if int(b[0]) == 1:
                                        if int(b[1]) == 4:
                                            if not int(b[2]) >= 3:
                                                overall_status = False
                                                return_report[node]=False
                                                return_report["msg_status"]="WARNING"
                                                str1="rpm " + str(rpm2) + " of version 1.4.3 or higher is required."
                                                logger.warning(str1)
                                                msg1.append(str1)
                                        elif not int(b[1]) > 4:
                                            overall_status = False
                                            return_report[node]=False
                                            return_report["msg_status"]="WARNING"
                                            str1="rpm " + str(rpm2) + " of version 1.4.3 or higher is required."
                                            logger.warning(str1)
                                            msg1.append(str1)
                                    elif not int(b[0]) > 1:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm2) + " of version 1.4.3 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                        else:
                            cmd = "rpm -q " + str(rpm2)
                            out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                            if not out.startswith(str(rpm2)):
                                cmd2 = "rpm -qa | grep " + str(rpm2)
                                out2,return_code2 = run_shell_command_on_nodes(cmd2,remote_node_flag,node)
                                if not out2.startswith(str(rpm2)):
                                    overall_status = False
                                    return_report[node]=False
                                    return_report["msg_status"]="WARNING"
                                    str1="rpm " + str(rpm2) + " is required."
                                    logger.warning(str1)
                                    msg1.append(str1)
            elif int(distro_version) >= 9:
                for rpm3 in rh8_9rpms:
                    if not rpm3 == "authd":
                        cmd = "rpm -q " + str(rpm3)
                        out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                        if not out.startswith(str(rpm3)):
                            cmd2 = "rpm -qa | grep " + str(rpm3)
                            out2,return_code2 = run_shell_command_on_nodes(cmd2,remote_node_flag,node)
                            if not out2.startswith(str(rpm3)):
                                overall_status = False
                                return_report[node]=False
                                return_report["msg_status"]="WARNING"
                                str1="rpm " + str(rpm3) + " is required."
                                logger.warning(str1)
                                msg1.append(str1)
        if distro_name == "SLES" and int(distro_version) <= 11:
            overall_status = False
            return_report[node]=False
            return_report["msg_status"]="ERROR"
            str1="Distro version is invalid to check rpms."
            logger.error(str1)
            msg1.append(str1)
        elif distro_name =="SLES" and int(distro_version) >= 12:
            for rpm_name in common_rpms:
                if rpm_name == "sg3_utils":
                    cmd = "rpm -qi " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 1.20 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        for line in tmp_file:
                            if line.startswith('Version'):
                                a = line.strip().split(':')
                                if '~' in a[1]:
                                    c = a[1].split('~')
                                    if not float(c[0]) >= 1.20:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm_name) + " of version 1.20 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                                elif '+' in a[1]:
                                    c = a[1].split('+')
                                    if not float(c[0]) >= 1.20:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm_name) + " of version 1.20 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                        tmp_file.close()
                elif rpm_name == "net-snmp":
                    cmd = "rpm -qi " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 5.7 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        for line in tmp_file:
                            if line.startswith('Version'):
                                a = line.strip().split(':')
                                b = a[1].split(".")
                                if int(b[0]) == 5:
                                    if not int(b[1]) >= 7:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm_name) + " of version 5.7 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                                elif not int(b[0]) > 5:
                                    overall_status = False
                                    return_report[node]=False
                                    return_report["msg_status"]="WARNING"
                                    str1="rpm " + str(rpm_name) + " of version 5.7 or higher is required."
                                    logger.warning(str1)
                                    msg1.append(str1)
                        tmp_file.close()
                elif rpm_name == "rpm":
                    cmd = "rpm -qi " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 4.4 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        for line in tmp_file:
                            if line.startswith('Version'):
                                a = line.strip().split(':')
                                b = a[1].split('.')
                                if int(b[0]) == 4:
                                    if not int(b[1]) >= 4:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm_name) + " of version 4.4 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                                elif not int(b[0]) > 4:
                                    overall_status = False
                                    return_report[node]=False
                                    return_report["msg_status"]="WARNING"
                                    str1="rpm " + str(rpm_name) + " of version 4.4 or higher is required."
                                    logger.warning(str1)
                                    msg1.append(str1)
                        tmp_file.close()
                elif rpm_name == "java":
                    cmd = str(rpm_name) + " -version"
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if return_code != 0:
                        overall_status = False
                        return_report[node]=False
                        return_report["msg_status"]="WARNING"
                        str1="rpm " + str(rpm_name) + " of version 1.8 or higher is required."
                        logger.warning(str1)
                        msg1.append(str1)
                    else:
                        tmp_file = open('tmp.txt', 'w')
                        tmp_file.write(out)
                        tmp_file.close()
                        tmp_file = open('tmp.txt', 'r')
                        first_line = tmp_file.readline().strip('\n')
                        a = first_line.split('"')
                        b = a[1].split('.',2)
                        if int(b[0]) == 1:
                            if not int(b[1]) >= 8:
                                overall_status = False
                                return_report[node]=False
                                return_report["msg_status"]="WARNING"
                                str1="rpm " + str(rpm_name) + " of version 1.8 or higher is required."
                                logger.warning(str1)
                                msg1.append(str1)
                        elif not int(b[0]) >= 1:
                            overall_status = False
                            return_report[node]=False
                            return_report["msg_status"]="WARNING"
                            str1="rpm " + str(rpm_name) + " of version 1.8 or higher is required."
                            logger.warning(str1)
                            msg1.append(str1)
                        tmp_file.close()
                else:
                    cmd = "rpm -q " + str(rpm_name)
                    out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                    if not out.startswith(str(rpm_name)):
                        cmd2 = "rpm -qa | grep " + str(rpm_name)
                        out2,return_code2 = run_shell_command_on_nodes(cmd2,remote_node_flag,node)
                        if not out2.startswith(str(rpm_name)):
                            overall_status = False
                            return_report[node]=False
                            return_report["msg_status"]="WARNING"
                            str1="rpm " + str(rpm_name) + " is required."
                            logger.warning(str1)
                            msg1.append(str1)
            if int(distro_version) == 12:
                for rpm4 in sles12_rpms:
                    if rpm4 == "pidentd":
                        cmd = "rpm -qi " + str(rpm4)
                        out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                        if return_code != 0:
                            overall_status = False
                            return_report[node]=False
                            return_report["msg_status"]="WARNING"
                            str1="rpm " + str(rpm4) + " of version 3.1a25 or higher is required."
                            logger.warning(str1)
                            msg1.append(str1)
                        else:
                            tmp_file = open('tmp.txt', 'w')
                            tmp_file.write(out)
                            tmp_file.close()
                            tmp_file = open('tmp.txt', 'r')
                            for line in tmp_file:
                                if line.startswith('Version'):
                                    a = line.strip().split(':')
                                    b = a[1].split('.')
                                    if int(b[0]) == 3:
                                        if b[1].startswith('1'):
                                            c = b[1].split('a')
                                            if not int(c[0]) >= 1:
                                                overall_status = False
                                                return_report[node]=False
                                                return_report["msg_status"]="WARNING"
                                                str1="rpm " + str(rpm4) + " of version 3.1a25 or higher is required."
                                                logger.warning(str1)
                                                msg1.append(str1)
                                    elif not int(b[0]) > 3:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm4) + " of version 3.1a25 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                    else:
                        cmd = "rpm -q " + str(rpm4)
                        out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                        if not out.startswith(str(rpm4)):
                            cmd2 = "rpm -qa | grep " + str(rpm4)
                            out2,return_code2 = run_shell_command_on_nodes(cmd2,remote_node_flag,node)
                            if not out2.startswith(str(rpm4)):
                                overall_status = False
                                return_report[node]=False
                                return_report["msg_status"]="WARNING"
                                str1="rpm " + str(rpm4) + " is required."
                                logger.warning(str1)
                                msg1.append(str1)
            if int(distro_version) >= 15:
                for rpm5 in sles15_rpms:
                    if rpm5 == "pidentd":
                        cmd = "rpm -qi " + str(rpm5)
                        out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                        if return_code != 0:
                            overall_status = False
                            return_report[node]=False
                            return_report["msg_status"]="WARNING"
                            str1="rpm " + str(rpm5) + " of version 3.0.19 or higher is required."
                            logger.warning(str1)
                            msg1.append(str1)
                        else:
                            tmp_file = open('tmp.txt', 'w')
                            tmp_file.write(out)
                            tmp_file.close()
                            tmp_file = open('tmp.txt', 'r')
                            for line in tmp_file:
                                if line.startswith('Version'):
                                    a = line.strip().split(':')
                                    b = a[1].split('.')
                                    if int(b[0]) == 3:
                                        if int(b[1]) == 0:
                                            if not int(b[2]) >= 19: 
                                                overall_status = False
                                                return_report[node]=False
                                                return_report["msg_status"]="WARNING"
                                                str1="rpm " + str(rpm5) + " of version 3.0.19 or higher is required."
                                                logger.warning(str1)
                                                msg1.append(str1)
                                        elif not int(b[1]) > 0:
                                            overall_status = False
                                            return_report[node]=False
                                            return_report["msg_status"]="WARNING"
                                            str1="rpm " + str(rpm5) + " of version 3.0.19 or higher is required."
                                            logger.warning(str1)
                                            msg1.append(str1)
                                    elif not int(b[0]) > 3:
                                        overall_status = False
                                        return_report[node]=False
                                        return_report["msg_status"]="WARNING"
                                        str1="rpm " + str(rpm5) + " of version 3.0.19 or higher is required."
                                        logger.warning(str1)
                                        msg1.append(str1)
                    else:
                        cmd = "rpm -q " + str(rpm5)
                        out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                        if not out.startswith(str(rpm5)):
                            cmd2 = "rpm -q " + str(rpm5)
                            out2,return_code2 = run_shell_command_on_nodes(cmd2,remote_node_flag,node)
                            if not out2.startswith(str(rpm5)):
                                overall_status = False
                                return_report[node]=False
                                return_report["msg_status"]="WARNING"
                                str1="rpm " + str(rpm5) + " is required."
                                logger.warning(str1)
                                msg1.append(str1)
        if len(user_rpms) > 0:
            for user_rpm in user_rpms:
                cmd = "rpm -q | grep " + str(user_rpm)
                out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
                if not out.startswith(str(user_rpm)):
                    cmd2 = "rpm -qa | grep " + str(user_rpm)
                    out2,return_code2 = run_shell_command_on_nodes(cmd2,remote_node_flag,node)
                    if not out2.startswith(str(user_rpm)):
                        overall_status = False
                        return_report["msg_status"] = "WARNING"
                        str1 = "rpm " + str(user_rpm) + " is not installed"
                        logger.error(str1)
                        msg1.append(str1)

        return_report["msg"] = msg1
        if overall_status == False:
            output_dictionary["overall_status"] = "FAILED"
        else:
            msg2=[]
            return_report["msg_status"]="INFO"
            str1="All the required rpms are installed"
            logger.info(str1)
            msg2.append(str1)
            return_report["msg"] = msg2
            output_dictionary["result"] = result
            output_dictionary["overall_status"] = "OK"
        return_report["node_name"] = node
        result.append(return_report)
        output_dictionary["result"] = result
        final_output.append(output_dictionary)
        return final_output

    except Exception as ex:
        overall_status = False
        return_report["msg_status"] = "ERROR"
        str1 = "Exception in check rpms installed"
        logger.error(str1)
        msg1.append(str1)
        return_report["msg"] = msg1
        return_report["node_name"] = node

        result.append(return_report)

        output_dictionary["result"] = result

        if overall_status == False:
            output_dictionary["overall_status"] = "FAILED"
        else:
            output_dictionary["overall_status"] = "OK"

        final_output.append(output_dictionary)
        return final_output


def check_distro_installed(os_list,node,remote_node_flag):
    logger.debug("Entering check_distro_installed function on node " + node)
    try:
        output_dictionary = {}
        global distro_name
        global distro_version
        output_dictionary["test_case_name"] = "2. Check Distro"
        return_report = {}
        overall_status = True
        result = []
        msg1 = []
        final_output = []
        valid_os_list = os_list
        cmd = "cat /etc/os-release"
        with open ('os-release-version', 'w') as f:
            out,return_code = run_shell_command_on_nodes(cmd,remote_node_flag,node)
            f.write(out)

        (distro_name, distro_version)= get_os('os-release-version')
        os_version = distro_name + " " + distro_version

        if os_version in valid_os_list:
            return_report["msg_status"] = "INFO"
            str1 = "Current distro " + str(distro_name) + str(distro_version) + " is valid"
            msg1.append(str1)
            logger.info(str1)
        else:
            overall_status = False
            #return_report["check_distro_status"]=False
            return_report["msg_status"] = "ERROR"
            str1 = "Current distro " +str(distro_name) + str(distro_version) + " is unsupported"
            msg1.append(str1)
            logger.error(str1)

        return_report["msg"] = msg1
        return_report["node_name"] = node

        result.append(return_report)

        output_dictionary["result"] = result

        if overall_status == False:
            output_dictionary["overall_status"] = "FAILED"
        else:
            output_dictionary["overall_status"] = "OK"

        final_output.append(output_dictionary)
        return final_output

    except Exception as ex:
        overall_status = False
        return_report["msg_status"] = "ERROR"
        str1 = "Exception in check distro installed"
        logger.error(str1)
        msg1.append(str1)
        return_report["msg"] = msg1
        return_report["node_name"] = node

        result.append(return_report)

        output_dictionary["result"] = result

        if overall_status == False:
            output_dictionary["overall_status"] = "FAILED"
        else:
            output_dictionary["overall_status"] = "OK"

        final_output.append(output_dictionary)
        return final_output

check_port_status= False
def check_port(node,remote_node_flag):
    logger.debug("Entering check_port function on node " + node)
    try:
        output_dictionary = {}
        output_dictionary["test_case_name"] = "4. Check Port availability"
        overall_status = True
        msg1 = []
        port_numbers =  get_config_data("ports")
        """
        Test which ports are available
        """
        check_port_status= True
        for index in port_numbers:
            result = []
            final_output = []
            return_report = {}
            cmd = "sudo netstat -tulpn | grep :" + index
            out,return_code = run_shell_command_on_nodes(cmd, remote_node_flag,node)
            if return_code == 0:
                overall_status = False
                return_report["msg_status"] = "WARNING"
                str1 = "Port " + str(index) + " is being used"
                logger.warning(str1)
                msg1.append(str1)
            else:
                return_report["msg_status"] = "INFO"
                str1 = "Port " + str(index) + " is not being used"
                logger.info(str1)
                msg1.append(str1)

            return_report["msg"] = msg1
            return_report["node_name"] = node

            result.append(return_report)

            output_dictionary["result"] = result

            if overall_status == False:
                output_dictionary["overall_status"] = "FAILED"
            else:
                output_dictionary["overall_status"] = "OK"

            final_output.append(output_dictionary)
        return final_output

    except Exception as ex:
        overall_status = False
        return_report[check_port_status]=False
        return_report["msg_status"] = "ERROR"
        str1 = "Exception in check port"
        logger.error(str1)
        msg1.append(str1)
        return_report["msg"] = msg1
        return_report["node_name"] = node

        result.append(return_report)

        output_dictionary["result"] = result

        if overall_status == False:
            output_dictionary["overall_status"] = "FAILED"
        else:
            output_dictionary["overall_status"] = "OK"

        final_output.append(output_dictionary)
        return final_output

