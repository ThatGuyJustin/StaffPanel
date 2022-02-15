from peewee import MySQLDatabase
from peewee import Model

import yaml

with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.UnsafeLoader)

core_protect = MySQLDatabase(config['coreprotect']['database_name'], user=config['coreprotect']['username'],
                             password=config['coreprotect']['password'],
                             host=config['coreprotect']['database_ip'], port=config['coreprotect']['port'])

litebans = MySQLDatabase(config['litebans']['database_name'], user=config['litebans']['username'],
                         password=config['litebans']['password'],
                         host=config['litebans']['database_ip'], port=config['litebans']['port'])


class LBBaseModel(Model):
    class Meta:
        database = litebans


class CPBaseModel(Model):
    class Meta:
        database = core_protect
