import sys,os
import argparse

from components import utils
from components import ENIProvisioner
from components import UserScript
from components import EBSProvisioner

def main(argv=sys.argv):
  parser = argparse.ArgumentParser()
  g = parser.add_mutually_exclusive_group(required=True)
  g.add_argument(
    '--get-instance-tag',
    default=None,
    nargs=1,
    dest='get_instance_tag',
    metavar=('tag'),
    help='\n'.join([
      'tag: The tag name to query on this instance (returns VALUE in TAG:VALUE)',
    ]),
  )
  g.add_argument(
    '--eni',
    default=None,
    nargs=1,
    dest='eni_tag',
    metavar=('eni_tag'),
    help='\n'.join([
      'eni_tag: ENI to attach, defined by a single tag ("Key:Value")',
    ]),
  )

  g.add_argument(
    '--ebs',
    default=None,
    nargs=1,
    dest='ebs_tag',
    metavar=('ebs_tag'),
    help='\n'.join([
      'ebs_tag: EBS volume to attach, defined by a single tag ("Key:Value")',
    ]),
  )

  g.add_argument(
    '--user-script',
    default=None,
    nargs=5,
    dest='user_script',
    metavar=('instance_tag','ssh_key','ec2_user','script','script_args'),
    help='\n'.join([
      'instances_tag: instances to connect to defined by a single tag ("Key:Value")',
      'ssh_key: path to ssh key',
      'ec2_user: ec2 user (ubuntu for Ubuntu, ec2-user for amazon-linux or debian)',
      'script: path to script to run',
      'script_args: args to pass to the script',
    ]),
  )
  args = parser.parse_args()

  if args.get_instance_tag:
    sys.stdout.write(utils.get_instance_tag_value(args.get_instance_tag[0]))

  if args.eni_tag:
    tag = args.eni_tag[0]
    P = ENIProvisioner(tag)
    P.provision()

  if args.ebs_tag:
    tag = args.ebs_tag[0]
    P = EBSProvisioner(tag)
    P.provision()  

  if args.user_script:
    tag,key,ec2_user,script,script_args = args.user_script
    P = UserScript(tag,key,ec2_user,script,script_args)
    P.run()

if __name__ == '__main__':
  main()


