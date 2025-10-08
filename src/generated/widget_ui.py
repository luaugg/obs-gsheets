# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QFormLayout, QFrame, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpinBox, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(381, 364)
        MainWindow.setMinimumSize(QSize(381, 364))
        MainWindow.setMaximumSize(QSize(381, 364))
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 0, 381, 341))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.label_8 = QLabel(self.frame_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 10, 131, 16))
        self.formLayoutWidget = QWidget(self.frame_2)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(0, 50, 381, 157))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(2)
        self.formLayout.setContentsMargins(12, 0, 10, 10)
        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.api_key = QLineEdit(self.formLayoutWidget)
        self.api_key.setObjectName(u"api_key")
        self.api_key.setAcceptDrops(False)
        self.api_key.setInputMask(u"")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.api_key)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.spreadsheet_id = QLineEdit(self.formLayoutWidget)
        self.spreadsheet_id.setObjectName(u"spreadsheet_id")
        self.spreadsheet_id.setAcceptDrops(False)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spreadsheet_id)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.tab_name = QLineEdit(self.formLayoutWidget)
        self.tab_name.setObjectName(u"tab_name")
        self.tab_name.setAcceptDrops(False)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.tab_name)

        self.label_5 = QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.range = QLineEdit(self.formLayoutWidget)
        self.range.setObjectName(u"range")
        self.range.setAcceptDrops(False)
        self.range.setInputMask(u"")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.range)

        self.label_6 = QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.update_interval = QSpinBox(self.formLayoutWidget)
        self.update_interval.setObjectName(u"update_interval")
        self.update_interval.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.update_interval.setMinimum(1000)
        self.update_interval.setMaximum(60000)
        self.update_interval.setSingleStep(100)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.update_interval)

        self.label_7 = QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.dimension = QComboBox(self.formLayoutWidget)
        self.dimension.addItem("")
        self.dimension.addItem("")
        self.dimension.setObjectName(u"dimension")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.dimension)

        self.label_13 = QLabel(self.frame_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 30, 271, 16))
        self.label_13.setTextFormat(Qt.TextFormat.RichText)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(0, 200, 381, 111))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.label_9 = QLabel(self.frame_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 10, 191, 16))
        self.formLayoutWidget_2 = QWidget(self.frame_3)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(0, 50, 381, 80))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setVerticalSpacing(2)
        self.formLayout_2.setContentsMargins(12, 0, 10, 15)
        self.label_10 = QLabel(self.formLayoutWidget_2)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_10)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.server = QLineEdit(self.formLayoutWidget_2)
        self.server.setObjectName(u"server")
        self.server.setAcceptDrops(False)

        self.horizontalLayout_2.addWidget(self.server)

        self.port = QSpinBox(self.formLayoutWidget_2)
        self.port.setObjectName(u"port")
        self.port.setProperty(u"showGroupSeparator", False)
        self.port.setMaximum(65535)
        self.port.setValue(4455)

        self.horizontalLayout_2.addWidget(self.port)


        self.formLayout_2.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)

        self.label_12 = QLabel(self.formLayoutWidget_2)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_12)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.auth_enabled = QCheckBox(self.formLayoutWidget_2)
        self.auth_enabled.setObjectName(u"auth_enabled")

        self.horizontalLayout.addWidget(self.auth_enabled)

        self.password = QLineEdit(self.formLayoutWidget_2)
        self.password.setObjectName(u"password")
        self.password.setAcceptDrops(False)
        self.password.setReadOnly(True)

        self.horizontalLayout.addWidget(self.password)


        self.formLayout_2.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout)

        self.label_11 = QLabel(self.frame_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 30, 271, 16))
        self.label_11.setTextFormat(Qt.TextFormat.RichText)
        self.frame = QFrame(self.frame_2)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 310, 381, 31))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayoutWidget = QWidget(self.frame)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 381, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(12, 0, 8, 0)
        self.label_14 = QLabel(self.horizontalLayoutWidget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(389, 29))
        self.label_14.setTextFormat(Qt.TextFormat.RichText)
        self.label_14.setOpenExternalLinks(True)

        self.horizontalLayout_3.addWidget(self.label_14)

        self.browse = QPushButton(self.horizontalLayoutWidget)
        self.browse.setObjectName(u"browse")
        self.browse.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.browse)

        self.start = QPushButton(self.horizontalLayoutWidget)
        self.start.setObjectName(u"start")
        self.start.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.start)

        self.stop = QPushButton(self.horizontalLayoutWidget)
        self.stop.setObjectName(u"stop")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop.sizePolicy().hasHeightForWidth())
        self.stop.setSizePolicy(sizePolicy)
        self.stop.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.stop)

        MainWindow.setCentralWidget(self.centralwidget)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)
        self.auth_enabled.toggled.connect(self.password.setEnabled)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"obs-gsheets", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">Google Sheet Details</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"API Key", None))
#if QT_CONFIG(statustip)
        self.api_key.setStatusTip(QCoreApplication.translate("MainWindow", u"Google API key", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.api_key.setWhatsThis(QCoreApplication.translate("MainWindow", u"A Google API key with permission and access to the Google Sheets API.", None))
#endif // QT_CONFIG(whatsthis)
        self.api_key.setText("")
        self.api_key.setPlaceholderText(QCoreApplication.translate("MainWindow", u"API key with Google Sheets enabled", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Spreadsheet ID", None))
#if QT_CONFIG(statustip)
        self.spreadsheet_id.setStatusTip(QCoreApplication.translate("MainWindow", u"Spreadsheet ID", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.spreadsheet_id.setWhatsThis(QCoreApplication.translate("MainWindow", u"The ID of your Google Spreadsheet. The sheet this refers to must be set such that anyone with a link can view it.", None))
#endif // QT_CONFIG(whatsthis)
        self.spreadsheet_id.setText("")
        self.spreadsheet_id.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your spreadsheet's ID. Must be visible to all", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Tab Name", None))
#if QT_CONFIG(statustip)
        self.tab_name.setStatusTip(QCoreApplication.translate("MainWindow", u"Spreadsheet tab name", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.tab_name.setWhatsThis(QCoreApplication.translate("MainWindow", u"Tab name (lower left corner) of your Google spreadsheet.", None))
#endif // QT_CONFIG(whatsthis)
        self.tab_name.setInputMask("")
        self.tab_name.setText("")
        self.tab_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Tab to read from - e.g. Sheet1", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Range", None))
#if QT_CONFIG(statustip)
        self.range.setStatusTip(QCoreApplication.translate("MainWindow", u"Value range", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.range.setWhatsThis(QCoreApplication.translate("MainWindow", u"Range of values to collect in A1 notation. By default, this is A1:Z1000.", None))
#endif // QT_CONFIG(whatsthis)
        self.range.setText("")
        self.range.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Range of values in A1 notation - e.g. A1:B2", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Update Interval", None))
#if QT_CONFIG(statustip)
        self.update_interval.setStatusTip(QCoreApplication.translate("MainWindow", u"Update interval in milliseconds", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.update_interval.setWhatsThis(QCoreApplication.translate("MainWindow", u"How often to poll Google Sheets. The lowest this can go is 1000ms, but 1500ms is recommended.", None))
#endif // QT_CONFIG(whatsthis)
        self.update_interval.setSpecialValueText("")
        self.update_interval.setSuffix(QCoreApplication.translate("MainWindow", u"ms", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Dimension", None))
        self.dimension.setItemText(0, QCoreApplication.translate("MainWindow", u"Rows", None))
        self.dimension.setItemText(1, QCoreApplication.translate("MainWindow", u"Columns", None))

#if QT_CONFIG(statustip)
        self.dimension.setStatusTip(QCoreApplication.translate("MainWindow", u"Sheet dimension - order by rows or by columns", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.dimension.setWhatsThis(QCoreApplication.translate("MainWindow", u"Return results ordered by row or by column. Rows is the default.", None))
#endif // QT_CONFIG(whatsthis)
        self.dimension.setCurrentText(QCoreApplication.translate("MainWindow", u"Rows", None))
        self.dimension.setPlaceholderText("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-style:italic;\">API Key, Spreadsheet URL and Tab Name are required.</span></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">OBS WebSocket Server Details</span></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Server", None))
#if QT_CONFIG(statustip)
        self.server.setStatusTip(QCoreApplication.translate("MainWindow", u"Server host", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.server.setWhatsThis(QCoreApplication.translate("MainWindow", u"The server host. Like with the port, you can leave this alone most of the time.", None))
#endif // QT_CONFIG(whatsthis)
        self.server.setPlaceholderText(QCoreApplication.translate("MainWindow", u"localhost", None))
#if QT_CONFIG(statustip)
        self.port.setStatusTip(QCoreApplication.translate("MainWindow", u"Server port", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.port.setWhatsThis(QCoreApplication.translate("MainWindow", u"The server port. You can leave this alone most of the time.", None))
#endif // QT_CONFIG(whatsthis)
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Authentication", None))
#if QT_CONFIG(statustip)
        self.auth_enabled.setStatusTip(QCoreApplication.translate("MainWindow", u"Toggle authentication", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.auth_enabled.setWhatsThis(QCoreApplication.translate("MainWindow", u"Whether or not to try connecting with a password. Enabling this will allow you to edit the password box.", None))
#endif // QT_CONFIG(whatsthis)
        self.auth_enabled.setText(QCoreApplication.translate("MainWindow", u" Enabled?", None))
#if QT_CONFIG(statustip)
        self.password.setStatusTip(QCoreApplication.translate("MainWindow", u"Password", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.password.setWhatsThis(QCoreApplication.translate("MainWindow", u"Password required to connect to OBS. Becomes editable when you tick the Enabled box.", None))
#endif // QT_CONFIG(whatsthis)
        self.password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password (if there is one)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:8pt; font-style:italic;\">OBS Studio -&gt; Tools -&gt; WebSocket Server Settings</span></p></body></html>", None))
#if QT_CONFIG(statustip)
        self.label_14.setStatusTip(QCoreApplication.translate("MainWindow", u"Link to the latest release of obs-gsheets", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.label_14.setWhatsThis(QCoreApplication.translate("MainWindow", u"Link to the latest release of obs-gsheets.", None))
#endif // QT_CONFIG(whatsthis)
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>v0.2.0 - <a href=\"https://github.com/luaugg/obs-gsheets/releases/latest\"><span style=\" text-decoration: underline; color:#f0c0f4;\">check for updates!</span></a></p></body></html>", None))
#if QT_CONFIG(statustip)
        self.browse.setStatusTip(QCoreApplication.translate("MainWindow", u"Select a config.toml configuration file", None))
#endif // QT_CONFIG(statustip)
        self.browse.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
#if QT_CONFIG(statustip)
        self.start.setStatusTip(QCoreApplication.translate("MainWindow", u"Start the update loop", None))
#endif // QT_CONFIG(statustip)
        self.start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
#if QT_CONFIG(statustip)
        self.stop.setStatusTip(QCoreApplication.translate("MainWindow", u"Stop the update loop", None))
#endif // QT_CONFIG(statustip)
        self.stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
    # retranslateUi

