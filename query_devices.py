import datetime
import os
from multiprocessing.pool import Pool
from warnings import warn

import paramiko as paramiko
from paramiko.client import WarningPolicy
from paramiko.ssh_exception import SSHException
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import relationship, sessionmaker, joinedload

import monitoring.settings

Base = declarative_base()


class Device(Base, DeferredReflection):
    __tablename__ = 'app_device'

    def __str__(self, *args, **kwargs):
        return '%s@%s' % (self.human_readable, self.ip_address)


class DeviceParams(Base, DeferredReflection):
    __tablename__ = 'app_deviceparams'
    device = relationship('Device', backref='params')


SCRIPTS_PREFIX = '/root'

engine = create_engine(
    'sqlite:///%s' % monitoring.settings.DATABASES['default']['NAME'],
)

db_session = sessionmaker(bind=engine)()


def main():
    DeferredReflection.prepare(engine)  # Autoload the tables from DB schema
    try:
        db_session.execute(
            Device.__table__.update().values({'query_status': 'queue'})
        )
        db_session.commit()
    except ProgrammingError:
        db_session.rollback()

    with Pool() as pool:
        pool.map(
            query_device,
            db_session.query(
                Device.id
            ).filter_by(
                is_active=True
            ),
            chunksize=1,
        )


def query_device(device_id):
    engine.dispose()  # Убить соединения до базы от старого процесса, чтобы избежать конфликта
    device = db_session.query(
        Device
    ).options(
        joinedload(Device.params)
    ).get(device_id)

    try:

        try:
            print('Querying %s' % device)
            device.status = 'querying'
            db_session.commit()

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(WarningPolicy)
            client.load_system_host_keys()

            client.connect(
                device.ip_address,
                username=device.login,
                password=device.password,
                timeout=5,

            )

            for device_param in device.params:
                process_param(client, device_param)

        except SSHException as e:
            warn(str(e))
            device.query_status = 'failure'
        else:
            device.query_status = 'success'
        finally:
            device.last_queried = datetime.datetime.now()
            db_session.commit()

    except ProgrammingError as e:
        db_session.rollback()
        raise


def process_param(client, device_param):
    remote_script_path = os.sep.join([SCRIPTS_PREFIX, '%s.sh' % device_param.param_name])
    chan = client.get_transport().open_session()
    stdout = chan.makefile('r', -1)
    stderr = chan.makefile('r', -1)
    chan.exec_command(remote_script_path)
    content = stdout.read()
    if chan.recv_exit_status() != 0:
        raise SSHException('Remote process rerturned non-zero exit code: %d\n'
                           'With output:\n%s' % (chan.recv_exit_status(), stderr.read()))
    if device_param.param_type == 'bool':
        device_param.param_value = bool(content) and content.lower() not in ('n', 'no', 'off', 'down')
    else:
        device_param.param_value = content.strip().decode('utf8')
    print('\t%s = %s' % (device_param.param_name, device_param.param_value))


if __name__ == '__main__':
    main()
