import datetime
import os
from warnings import warn
import paramiko as paramiko
from paramiko.client import WarningPolicy
from paramiko.ssh_exception import SSHException
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import relationship, Session, sessionmaker, joinedload
import monitoring.settings

Base = declarative_base()


def rollback_on_exception(fn):
    def wrapper(*args, db_session, **kwargs):
        try:
            return fn(*args, db_session=db_session, **kwargs)
        except ProgrammingError as e:
            db_session.rollback()
            raise

    return wrapper


class Device(Base, DeferredReflection):
    __tablename__ = 'app_device'

    def __str__(self, *args, **kwargs):
        return '%s@%s' % (self.human_readable, self.ip_address)


class DeviceParams(Base, DeferredReflection):
    __tablename__ = 'app_deviceparams'
    device = relationship('Device', backref='params')


SCRIPTS_PREFIX = '/root'


class QueryingError(Exception):
    pass


def main():
    engine = create_engine(
        'sqlite:///%s' % monitoring.settings.DATABASES['default']['NAME']
    )
    db_session = sessionmaker(bind=engine)()
    DeferredReflection.prepare(engine)  # Autoload the tables from DB schema

    for device in db_session.query(
            Device
    ).filter_by(
        is_active=True
    ).options(
        joinedload(Device.params)
    ):
        query_device(device, db_session=db_session)


@rollback_on_exception
def query_device(device,db_session=None):
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

    except SSHException as e:
        warn(str(e))
        device.query_status = 'failure'
    else:
        device.query_status = 'success'
    finally:
        device.last_queried = datetime.datetime.now()
        db_session.commit()


if __name__ == '__main__':
    main()
