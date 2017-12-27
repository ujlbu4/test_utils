from pyhocon import ConfigFactory as TypesafeConfigFactory, ConfigTree

# import logging

# don't use singletons: https://stackoverflow.com/a/6760821
# Use a module. It is imported only once. Define some global variables in it - they will be singleton's 'attributes'.
# Add some functions - the singleton's 'methods'.

import pkg_resources

# config = ConfigTree()

import os


# def load(package_path=lambda file: os.path.join(os.path.dirname(file), 'configs')):
#     print("package_path: {}".format(package_path))
#
#     __local_application_conf = TypesafeConfigFactory.parse_file('config/application.conf', required=False)
#     __local_reference_conf = TypesafeConfigFactory.parse_file('config/reference.conf', required=False)
#
#     config = __local_reference_conf
#     if len(__local_application_conf) > 0:
#         config = config.merge_configs(__local_reference_conf, __local_application_conf)

def load(src_invoking_file):
    package_path = os.path.dirname(src_invoking_file)
    print("package_path: {}".format(package_path))

    local_application_conf = TypesafeConfigFactory.parse_file('{}/configs/application.conf'.format(package_path), required=False)
    local_reference_conf = TypesafeConfigFactory.parse_file('{}/configs/reference.conf'.format(package_path), required=False)

    config = local_reference_conf
    if len(local_application_conf) > 0:
        config = config.merge_configs(local_reference_conf, local_application_conf)

    return config



class ConfigFactory:
    # @staticmethod
    # def load():
    # global config
    #
    # # with open('config/application111.conf', 'w+') as fd:
    # #     fd.write("ttt")
    #
    # local_application_conf = TypesafeConfigFactory.parse_file('config/application.conf', required=False)
    # local_reference_conf = TypesafeConfigFactory.parse_file('config/reference.conf', required=False)
    #
    #
    # # # application.conf have higher priority
    # # # local_config = ConfigTree.merge_configs(local_reference_conf, local_application_conf)
    # # local_config = local_reference_conf.with_fallback(local_application_conf)
    # #
    # # # global config have higher priority
    # # # config = ConfigTree.merge_configs(local_config, config)
    # # config = local_config.with_fallback(config)

    @staticmethod
    def load(src_invoking_file):
        package_path = os.path.dirname(src_invoking_file)
        print("package_path: {}".format(package_path))

        __local_application_conf = TypesafeConfigFactory.parse_file('{}/configs/application.conf'.format(package_path), required=False)
        __local_reference_conf = TypesafeConfigFactory.parse_file('{}/configs/reference.conf'.format(package_path), required=False)

        config = __local_reference_conf
        if len(__local_application_conf) > 0:
            config = config.merge_configs(__local_reference_conf, __local_application_conf)

        return config
