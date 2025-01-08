from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSizePolicy
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtCore import Qt, QRect
from components.load_stylesheet import load_stylesheet
from components.shutter_btns import ShutterBtns
class CameraView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toolbar()
        self.cam_feed()

        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.toolbar_widget)
        self.layout.addWidget(self.camera_feed_widg, alignment=Qt.AlignTop)
        self.layout.addWidget(ShutterBtns(), alignment=Qt.AlignCenter)
        # self.setStyleSheet(load_stylesheet('camera_view_styles.qss'))
        

    def toolbar(self):
        self.toolbar_widget = QWidget()
        self.toolbar_widget_layout = QHBoxLayout()
        self.toolbar_widget_layout.setContentsMargins(0,0,0,10)
        self.toolbar_widget.setLayout(self.toolbar_widget_layout)

        # camera view lbl
        self.cam_view_lbl = QLabel("Camera View")
        self.cam_view_lbl_font = QFont("Poppins", 10, QFont.Weight.Bold)
        self.cam_view_lbl.setMargin(3)
        self.cam_view_lbl.setFont(self.cam_view_lbl_font)

        self.toolbar_widget_layout.addWidget(self.cam_view_lbl, alignment=Qt.AlignBottom)

        # detach icon btn
        self.detach_btn = QPushButton()
        self.detach_icon_img = QPixmap("../assets/icons/detach-icon.png")
        self.detach_icon = QIcon(self.detach_icon_img)
        self.detach_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.detach_btn.setIcon(self.detach_icon)
        self.detach_btn.setIconSize(self.detach_icon_img.size())
        self.detach_btn.setStyleSheet("width: 36; height: 36; margin-right: 10px; border-radius: 9px; background-color: #1fb141;")

        self.toolbar_widget_layout.addWidget(self.detach_btn, alignment=Qt.AlignRight)

        # camera list dropdown
        self.camera_list = QComboBox()
        self.camera_list.setMaximumWidth(160)
        self.camera_list.setObjectName("cam_list")
        self.camera_list.addItems(['0 - fek cam', '1 - tru cam'])
        self.camera_list.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.camera_list.view().window().setAttribute(Qt.WA_TranslucentBackground)

        self.camera_list.setFont(QFont("Poppins", 10, QFont.Weight.DemiBold))

        self.toolbar_widget_layout.addWidget(self.camera_list)
        self.camera_list.setStyleSheet("""
        
        QComboBox {
            padding-left: 10px;
            border-radius: 10px; 
            border: 3px solid #565b5e;
            height: 30px;
        }
        
        """)


    def cam_feed(self):
        self.camera_feed_widg = QLabel()
        self.camera_feed_pixmap_temp = QPixmap("../assets/imgs/Rectangle.png")
        self.camera_feed_widg.setPixmap(self.camera_feed_pixmap_temp)
