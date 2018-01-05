from pyhocon import ConfigFactory as TypesafeConfigFactory, ConfigTree

import os

config = ConfigTree(root=True)


def _load(src_invoking_file):
    package_path = os.path.dirname(src_invoking_file)
    print("package_path: {}".format(package_path))

    local_application_conf = TypesafeConfigFactory.parse_file('{}/configs/application.conf'.format(package_path), required=False)
    local_reference_conf = TypesafeConfigFactory.parse_file('{}/configs/reference.conf'.format(package_path), required=False)

    c = local_reference_conf
    if len(local_application_conf) > 0:
        if len(local_reference_conf) > 0:
            c = ConfigTree.merge_configs(local_reference_conf, local_application_conf)
        else:
            c = local_application_conf

    return c


def load_config(file, is_root=False):
    c = _load(file)

    global config
    if is_root:
        config = ConfigTree.merge_configs(config, c)
    else:
        config = ConfigTree.merge_configs(c, config)

    return config
