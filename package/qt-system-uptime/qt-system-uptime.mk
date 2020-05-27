################################################################################
#
# qt-system-uptime
#
################################################################################

QT_SYSTEM_UPTIME_SITE = $(TOPDIR)/../qt-system-uptime
QT_SYSTEM_UPTIME_SITE_METHOD = local

QT_SYSTEM_UPTIME_DEPENDENCIES = qt5base qt5charts

define QT_SYSTEM_UPTIME_CONFIGURE_CMDS
	(cd $(@D); $(QT5_QMAKE))
endef

define QT_SYSTEM_UPTIME_BUILD_CMDS
	$(TARGET_MAKE_ENV) $(MAKE) -C $(@D)
endef

define QT_SYSTEM_UPTIME_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/qt-system-uptime $(TARGET_DIR)/usr/bin/qt-system-uptime

endef

define QT_SYSTEM_UPTIME_INSTALL_INIT_SYSV
	$(INSTALL) -D -m 755 package/qt-system-uptime/S99qt-system-uptime $(TARGET_DIR)/etc/init.d/S99qt-system-uptime
endef

$(eval $(generic-package))
