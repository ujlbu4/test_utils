# from pyhocon import ConfigFactory as TypesafeConfigFactory, ConfigTree
#
# # import logging
#
#
# class ConfigFactory:
#     config = None
#
#     def load(self):
#         # if self.config is not None:
#         #     return self.config
#
#         local_application_conf = TypesafeConfigFactory.parse_file('config/application.conf', required=False)
#         local_reference_conf = TypesafeConfigFactory.parse_file('config/reference.conf', required=False)
#
#         # application.conf have higher priority
#         local_config = ConfigTree.merge_configs(local_reference_conf, local_application_conf)
#
#         if self.config is not None:
#             # global config have higher priority
#             self.config = ConfigTree.merge_configs(local_config, self.config)
#
#         self.config = local_config




#
#
# class Config:
#     pass
#
#
# class ConfigLocal(Config):
#     pass
#
#
# class ConfigSpace(Config):
#     pass
