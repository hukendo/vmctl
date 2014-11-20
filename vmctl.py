#!/usr/bin/python
import argparse
import sys
import getpass
import os
import os.path
import string
import subprocess


user = getpass.getuser()
vms = "/Users/" + user + "/Documents/Virtual Machines.localized/"
VMPATH = 4

class VMrun:
  vmrun = "/Applications/VMware Fusion.app/Contents/Library/vmrun"
  vcom = [vmrun, "-T", "fusion"]

  @staticmethod
  def start(vm, gui=False):
    guistate = "gui" if gui else "nogui"
    return subprocess.check_output(VMrun.vcom + ["start", vm, guistate])

  @staticmethod
  def list():
    return subprocess.check_output(VMrun.vcom + ["list"])

  @staticmethod
  def pause(vm):
    return subprocess.check_output(VMrun.vcom + ["pause", vm])

  @staticmethod
  def unpause(vm):
    return subprocess.check_output(VMrun.vcom + ["unpause", vm])

  @staticmethod
  def stop(vm, hard=False):
    hardsoft = "hard" if hard else "soft"
    return subprocess.check_output(VMrun.vcom + ["stop", vm, hardsoft])

  @staticmethod
  def reset(vm, hard=False):
    hardsoft = "hard" if hard else "soft"
    return subprocess.check_output(VMrun.vcom + ["reset", vm, hardsoft])

  @staticmethod
  def suspend(vm, hard=False):
    hardsoft = "hard" if hard else "soft"
    return subprocess.check_output(VMrun.vcom + ["suspend", vm, hardsoft])

  @staticmethod
  def guestip(vm, hard=False):
    return subprocess.check_output(VMrun.vcom + ["getGuestIPAddress", vm])

def vmForNumber(number):
  vmlist = [vm for vm in os.listdir(vms) if vm[0] != "."]
  try:
    title = string.rstrip(vmlist[number], ".vmwarevm")
    path = os.path.join(vms, vmlist[number], title + ".vmx")
    return {"title": title, "path": path}
  except:
    print str(args.target) + " does not specify a virtual machine."
    sys.exit(1)
  
def unpauseVm(args):
  target = vmForNumber(args.target)
  
  print "Playing " + str(args.target) + ":" + target["title"] + ":" + target["path"]
  print VMrun.unpause(target["path"])

def pauseVm(args):
  target = vmForNumber(args.target)
  
  print "Pausing " + str(args.target) + ":" + target["title"] + ":" + target["path"]
  print VMrun.pause(target["path"])

def runVm(args):
  target = vmForNumber(args.target)

  print "Running " + str(args.target) + ":" + target["title"] + ":" + target["path"]
  print VMrun.start(target["path"])

def sshVm(args):
  target = vmForNumber(args.target)
  ip = VMrun.guestip(target["path"])
  print "Connecting to " + str(args.target) + ":" + target["title"] + " " + str(ip)
  os.execlp("ssh", "ssh", ip.strip())

def printVms(args):
  vmlist = [string.rstrip(vm, ".vmwarevm") for vm in os.listdir(vms) if vm[0] != "."]
  running = VMrun.list()
  i = 0
  print "=== Virtual Machines ==="
  for vm in vmlist:
    print str(i) + ": " + vm
  print
  print "=== Running Machines ==="
  print running

parser = argparse.ArgumentParser(description='Control VMware virtual machines.')
subparsers = parser.add_subparsers()

listparse = subparsers.add_parser("list")
listparse.set_defaults(func=printVms)

vmrunparse = subparsers.add_parser("run")
vmrunparse.add_argument("-t", "--target", type=int, help="the target virtual machine", default=0)
vmrunparse.set_defaults(func=runVm)

vmpauseparse = subparsers.add_parser("pause")
vmpauseparse.add_argument("-t", "--target", type=int, help="the target virtual machine", default=0)
vmpauseparse.set_defaults(func=pauseVm)

vmplayparse = subparsers.add_parser("play")
vmplayparse.add_argument("-t", "--target", type=int, help="the target virtual machine", default=0)
vmplayparse.set_defaults(func=unpauseVm)

vmsshparse = subparsers.add_parser("ssh")
vmsshparse.add_argument("-t", "--target", type=int, help="the target virtual machine", default=0)
vmsshparse.add_argument("-i", "--ip", help="print the ip")
vmsshparse.add_argument("-o", "--opts", help="custom ssh options")
vmsshparse.set_defaults(func=sshVm)

args = parser.parse_args()
args.func(args)

