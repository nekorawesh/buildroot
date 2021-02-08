################################################################################
#
# hss
#
################################################################################

HSS_SITE = $(TOPDIR)/../hss
HSS_SITE_METHOD = local
CJSON_INSTALL_STAGING = YES

HSS_DEPENDENCIES = paho-mqtt-c cjson 

define HSS_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/hss $(TARGET_DIR)/usr/bin/hss

endef

define HSS_INSTALL_INIT_SYSV
        $(INSTALL) -D -m 755 package/hss/S99hss \
                $(TARGET_DIR)/etc/init.d/S99hss
endef

$(eval $(cmake-package))