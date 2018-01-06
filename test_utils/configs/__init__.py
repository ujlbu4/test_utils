from pyhocon import ConfigFactory as TypesafeConfigFactory, ConfigTree

import os

config = ConfigTree(root=True)


def _load(src_invoking_file, config_folder_name="configs", application_conf="application.conf", reference_conf="reference.conf"):
    package_path = os.path.dirname(src_invoking_file)

    local_application_conf = TypesafeConfigFactory \
        .parse_file('{package_path}/{config_folder_name}/{application_conf}'.format(package_path=package_path,
                                                                                    config_folder_name=config_folder_name,
                                                                                    application_conf=application_conf),
                    required=False)
    local_reference_conf = TypesafeConfigFactory \
        .parse_file('{package_path}/{config_folder_name}/{reference_conf}'.format(package_path=package_path,
                                                                                  config_folder_name=config_folder_name,
                                                                                  reference_conf=reference_conf),
                    required=False)

    c = merge_configs(local_reference_conf, local_application_conf)

    return c


def merge_configs(left, right):
    """
    Merge config right into left
    """
    c = right
    if len(left) > 0:
        if len(right) > 0:
            c = ConfigTree.merge_configs(left, right)
        else:
            c = left

    return c


def merge_root(config_current, config_from_file, is_root):
    if is_root:
        updated_conf = merge_configs(config_current, config_from_file)
    else:
        updated_conf = merge_configs(config_from_file, config_current)

    return updated_conf


def load_config(file, is_root=False, current_config=config):
    # if not isinstance(current_config, ConfigTree):
    #     raise TypeError('A current_config must be a [{}] type'.format(ConfigTree))

    c = _load(file)

    updated_conf = merge_root(current_config, c, is_root)

    set_global(updated_conf)
    return updated_conf


def set_global(new_conf):
    global config
    config = new_conf


def collapse_environment(config, env):
    env_config = ConfigTree()

    if not env:
        return config

    # filter env attr
    for item in config:
        for k, v in config[item].items():
            if k.find("~{env}".format(env=env)) > 0:
                k = k.replace("~{env}".format(env=env), "")
                env_config.put(item, TypesafeConfigFactory.from_dict({k: v}), append=True)

    # merge env values to source config
    config = merge_configs(config, env_config)

    # remove others env attrs
    for item in config:
        for k, v in config[item].items():
            if k.find("~") > 0:
                del config[item][k]

    return config
