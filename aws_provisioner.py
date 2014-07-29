import sys,os
import argparse
import config

from components import Solr
from components import Zookeeper
from components import GlobalProvisioner
from components import EB
from components import UserScript


def main(argv=sys.argv):
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--zookeeper',
    default=False,
    action='store_true',
    dest='zookeeper',
  )
  parser.add_argument(
    '--solr',
    default=False,
    action='store_true',
    dest='solr',
  )
  parser.add_argument(
    '--adslogging',
    default=False,
    action='store_true',
    dest='adslogging',
  )
  parser.add_argument(
    '--adslogging-forwarder',
    default=False,
    action='store_true',
    dest='adslogging_forwarder',
  )
  parser.add_argument (
    '--global',
    default=False,
    action='store_true',
    dest='global_provision',
  )
  parser.add_argument(
    '--application',
    default=None,
    nargs=3,
    dest='EB',
    metavar=('name','path','version_string'),
    help='\n'.join([
      'name: name of application (must have a corresponding entry in config.py)',
      'path: path to application root directory',
      'version_string: user generated tag to mark this upload',
      ]),
  )

  parser.add_argument(
    '--user-script',
    default=None,
    nargs=3,
    dest='user_script',
    metavar=('instance tags','ssh key','script'),
    help='\n'.join([
      'instances_tags: instances to connect to defined by tags ("Key:Value")',
      'ssh_key: path to ssh key',
      'script: path to script to run',
      ]),
  )


  args = parser.parse_args()

  if args.global_provision:
    P = GlobalProvisioner.GlobalProvisioner(config)
    P.orderedProvision()

  if args.zookeeper:
    P = Zookeeper.Zookeeper()
    P.localProvision()

  if args.solr:
    P = Solr.Solr()
    P.localProvision()

  if args.adslogging:
    P = Adslogging.Adslogging()
    P.localProvision()

  if args.adslogging_forwarder:
    P = Adslogging.Adslogging()
    P.localProvision(certpath='/adslogging_forwarder/certs/')

  if args.EB:
    app,path,version_string = args.EB
    P = EB.EB(config,app,path,version_string)
    P.localProvision()
    P.remoteProvision()

  if args.user_script:
    tags,key,script = args.user_script
    P = UserScript.UserScript(tags,key,script)
    P.localProvision()

if __name__ == '__main__':
  main()