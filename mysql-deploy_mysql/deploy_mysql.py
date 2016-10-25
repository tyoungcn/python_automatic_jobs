#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Tyoung
# Date: 2016-10-17 15:59:51

import os


# Path separator
sep = os.sep


def get_instance_number():
    """Get the number of instances.

    :return: A int number that represents total number of instances.
    """

    instance_number = input('\nInput the number of instances.\n'
                            '[default: 1]: ')
    try:
        if instance_number == '':
            instance_number = 1
            return instance_number
        else:
            if int(instance_number) > 0:
                instance_number = int(instance_number)
                return instance_number
            else:
                print('The value must be a unsigned int number, please input again!')
                return get_instance_number()
    except:
        print('The value must be a unsigned int number, please input again!')
        return get_instance_number()


def get_port_list():
    """Get all the ports number.

    :return: A list that contains all the ports number.
    """

    port_list = input('\nInput all the ports(separated by comma, such as: 3306,3307)\n'
                      '[default: 3306]: ')
    try:
        if port_list == '':
            port_list = [3306]
            return port_list
        else:
            if port_list.replace(',', '').isdigit():
                port_list = port_list.split(',')
                port_list = [int(i) for i in port_list]
                return port_list
            else:
                print('The ports must be unsigned int number and separated by comma, please input again!')
                return get_port_list()
    except:
        print('The ports must be unsigned int number and separated by comma, please input again!')
        return get_port_list()


def get_install_path():
    """Get the installation path.

    :return: A str that represents the installation path.
    """

    install_path = input('\nInput the path which MySQL will be installed to.\n'
                         '[default: /opt/mysql]: ')

    if install_path == '':
        install_path = '/opt/mysql'

    # If the path not exists, create it.
    if os.path.isdir(install_path):
        return install_path
    else:
        os.makedirs(r'{path}'.format(path=install_path), mode=0o755)
        return install_path


def get_data_path():
    """Get the data path which MySQL data will be stored.

    :return: A str that represents the data path.
    """

    data_path = input('\nInput the path which MySQL data will be stored in.\n'
                      '[default: /data/mysql]: ')

    if data_path == '':
        data_path = '/data/mysql'

    # If the path not exists, create it.
    if os.path.isdir(data_path):
        return data_path
    else:
        os.makedirs(r'{path}'.format(path=data_path), mode=0o755)
        return data_path


def verify_instance_and_port():
    """Get the number of instances and port list, and verify whether the number of instances and ports are equal.

    :return: A tuple that contains the result of get_instance_number() and get_port_list().
    """

    instance_number = get_instance_number()
    port_list = get_port_list()

    if instance_number == len(port_list):
        return instance_number, port_list
    else:
        print('Number of instances and ports are not equal, please input again!')
        return verify_instance_and_port()


def get_mysql_package():
    """Get the MySQL generic linux package name, and the package is stored in directory 'generic_linux_packages'.

    :return: A string that contains MySQL generic linux package name and path.
    """

    package_name = input("\nInput the MySQL generic linux package name, "
                         "which must be put in directory 'generic_linux_packages'\n"
                         "[Default: mysql-5.6.29-linux-glibc2.5-x86_64.tar.gz]: ")

    if package_name == '':
        package_name = r'mysql-5.6.29-linux-glibc2.5-x86_64.tar.gz'

    current_dir = os.getcwd()
    mysql_package = '{current_dir}{sep}generic_linux_packages{sep}{package_name}'.format(sep=sep,
                                                                                         current_dir=current_dir,
                                                                                         package_name=package_name)

    if os.path.exists(mysql_package):
        return mysql_package
    else:
        print("The MySQL generic linux package not exists in directory 'generic_linux_packages', please input again.")
        return get_mysql_package()


def get_config_file():
    """Get configuration file name, and the file is stored in directory 'my_cnf'

    :return: A string that contains configuration file name and path.
    """

    config_name = input("\nInput the MySQL configuration file name, "
                        "which must be put in directory 'my_cnf'\n"
                        "[Default: my.cnf]: ")

    if config_name == '':
        package_name = r'my.cnf'

    current_dir = os.getcwd()
    config_file = '{current_dir}{sep}my_cnf{sep}{package_name}'.format(sep=sep, current_dir=current_dir,
                                                                       package_name=package_name)

    if os.path.exists(config_file):
        return config_file
    else:
        print("The MySQL configuration file not exists in directory 'my_cnf', please input again.")
        return get_config_file()


def create_dir(directory, mode):
    """Create the given directory. If the directory exists, its mode will be changed to the given mode.
       Otherwise, it will be creted, and the mode will be set as the given.

    :return: None
    """

    if os.path.exists(directory):
        os.chmod(directory, mode)
    else:
        os.makedirs(r'{directory}'.format(directory=directory), mode=mode, exist_ok=True)


def create_user_group(user, group):
    """Create the given user and corresponding group.

    :return: None
    """
    # If the given user and group not exist, create them.
    if os.system("grep -E '^{group}' /etc/group > /dev/null".format(group=group)) != 0:
        os.system('groupadd {group}'.format(group=group))

    if os.system('id {user} > /dev/null'.format(user=user)) != 0:
        os.system('useradd -g {group} -r -s /sbin/nologin {user}'.format(user=user, group=group))


def create_instance_dir(data_path, port):
    """Create the relevant MySQL data directories for each instance.

    :return: A string that represents instance directory.
    """

    print('Create directories for instance {port}...'.format(port=port))
    print('Directories: data, tmp, logs...')
    print('\n')

    # Create relevant MySQL data directories: data, tmp, etc.
    instance_dir = '{data_path}{sep}mysql{port}'.format(data_path=data_path, port=port, sep=sep)
    data_dir = '{instance_dir}{sep}{dir_name}'.format(instance_dir=instance_dir, dir_name='data', sep=sep)
    tmp_dir = '{instance_dir}{sep}{dir_name}'.format(instance_dir=instance_dir, dir_name='tmp', sep=sep)
    log_dir = '{instance_dir}{sep}{dir_name}'.format(instance_dir=instance_dir, dir_name='logs', sep=sep)

    create_dir(data_dir, mode=0o700)
    create_dir(tmp_dir, mode=0o700)
    create_dir(log_dir, mode=0o700)

    # Change the ownership of relevant MySQL directories
    create_user_group(user='mysql', group='mysql')
    os.system('chown -R {user}:{group} {dir}'.format(user='mysql', group='mysql', dir=instance_dir))

    return instance_dir


def add_config_file(instance_dir, config_file, data_path, port):
    """Add configuration file for each instance, including modify data path, and port.

    :return: A string that represents instance configuration file path.
    """

    print('Create configuration file for instance {port}...'.format(port=port))
    print('\n')

    # The config file name for each instance
    instance_config_file = '{instance_dir}/my{port}.cnf'.format(instance_dir=instance_dir, port=port)

    os.system('cp -f {config_file} {instance_config_file}'.format(config_file=config_file,
                                                                  instance_config_file=instance_config_file))
    # Modify the default data path in config file
    data_path_e = data_path.replace('/', r'\/')
    os.system(r"sed -i 's/\/data\/mysql/{0}/g' {1}".format(data_path_e, instance_config_file))

    # Modify the port in config file
    os.system("sed -i 's/3306/{port}/g' {instance_config_file}".format(port=port,
                                                                       instance_config_file=instance_config_file))

    return instance_config_file


def install_mutiple_instances():
    """Install all the instances in the installation path.

    :return: None
    """

    ins_port = verify_instance_and_port()
    instance_number = ins_port[0]
    port_list = ins_port[1]
    install_path = get_install_path()
    data_path = get_data_path()
    mysql_package = get_mysql_package()
    config_file = get_config_file()

    print('==================================================')
    print('Installation details:')
    print('Number of instances:', instance_number)
    print('Port list:', port_list)
    print('Installation path:', install_path)
    print('MySQL data path:', data_path)
    print('MySQL generic linux package:', mysql_package)
    print('MySQL configuration file:', config_file)
    print('==================================================')
    print('\n')

    print('==================================================')
    print('Extract and install MysQL...')
    print('\n')

    # Extract and install the package in directory 'generic_linux_packages'
    mysql_package_name = os.path.split(mysql_package)[1]
    mysql_package_folder = mysql_package_name.replace('.tar.gz', '')
    # THe folder which MySQL package is extract to
    mysql_install_folder = '{install_path}{sep}{mysql_package_folder}'.format(install_path=install_path, sep=sep,
                                                                              mysql_package_folder=mysql_package_folder)

    if os.path.isdir(mysql_install_folder):
        print('The following MySQL install path already exists. The provided MySQL generic linux package will not be '
              'intalled!\n'
              '{mysql_install_folder}'.format(mysql_install_folder=mysql_install_folder))
    else:
        os.system('tar -xzf {mysql_package} -C {install_path}'.format(mysql_package=mysql_package,
                                                                      install_path=install_path))

    if os.path.lexists('/usr/local/mysql'):
        print("\nThe symbolic link '/usr/local/mysql' already exists, please check whether the link target is right!")
    else:
        os.symlink(mysql_install_folder, '/usr/local/mysql')

    print('==================================================')
    print('Add environment variables:')
    print(r"PATH=$PATH:/usr/local/mysql/bin")
    print('\n')

    # Add environment variables
    os.system(r"echo 'export PATH=$PATH:/usr/local/mysql/bin' > /etc/profile.d/mysql.sh")
    os.system('source /etc/profile.d/mysql.sh')

    # Setup Python environment variables
    path = os.getenv(r'PATH')
    path = path + r':/usr/local/mysql/bin'
    os.putenv('PATH', path)

    print('==================================================')
    print('Create directories and configuration file for every instance...')
    print('\n')

    # Create directories for every instance
    # And add configuration file for each instance
    for port in port_list:
        instance_dir = create_instance_dir(data_path=data_path, port=port)
        instance_config_file = add_config_file(instance_dir=instance_dir, config_file=config_file,
                                               data_path=data_path, port=port)

    # If only install one instance, setup the configuration file and autostart
    if len(port_list) == 1:
        os.system('cp -f {instance_config_file} /etc/my.cnf'.format(instance_config_file=instance_config_file))

        print('==================================================')
        print('Setup autostart for MySQL...')
        print('\n')

        # Setup autostart
        os.system('cp -f /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql')
        os.system('chkconfig --add mysql')
        os.system('chkconfig mysql on')

        print('==================================================')
        print('Initialize MySQL installation...')
        print('\n')

        # Initialize MySQL data
        os.chdir('/usr/local/mysql')
        os.system(r'/usr/local/mysql/scripts/mysql_install_db --defaults-file=/etc/my.cnf --user=mysql')

        print('==================================================')
        print('Setup MySQL security...')
        print('\n')

        # Setup MySQL security
        socket = '/tmp/mysql{port}.sock'.format(port=port_list[0])

        os.system('/etc/init.d/mysql start')
        os.system('ln -s {socket} /tmp/mysql.sock'.format(socket=socket))
        os.system('/usr/local/mysql/bin/mysql_secure_installation')
        os.system('rm -f /tmp/mysql.sock')


if __name__ == '__main__':
    install_mutiple_instances()
