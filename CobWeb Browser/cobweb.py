#
# import all from PyQt5 Library to build our app
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
# standard imports
import os
import sys
import requests

# sorry in advance for not using doctrings.

# create a dialog box class about our app
class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs) # use inherited QDialog template

        QBtn = QDialogButtonBox.Ok  # no cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("CobWeb Browser")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'cobweb-128.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("""

        Python-based, minimal, lightweight (and maybe not 100% secure) web browser.
        
        Get tangled in the Web.

        """))

        layout.addWidget(QLabel("Version 2.10.0"))
        layout.addWidget(QLabel("Copyright 2022 CobWeb")) # there literally is no official copyright

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

# this is the main window class, where all the 'magic' happens.
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs) # inherit from the QT class

        self.default_homepage = "https://www.duckduckgo.com" # because you know why
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # building up our navigation bar from here on out
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('images', 'back.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images', 'next.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'redo.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images', 'home-page-64.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()  # yes, really, we need this on instance
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('images', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        # uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        # uncomment below to begin work on toolbar custom features (bookmarks, plugins etc.)
        # navtb.addSeparator()

        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save Page As...", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About CobWeb", self)
        about_action.setStatusTip("Find out more about CobWeb")  # Hungry!
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage') # because majority still use google
        self.add_new_tab(QUrl(self.default_homepage), 'Homepage') # but i use this sometimes

        self.show()

        self.setWindowTitle("CobWeb Browser")
        self.setWindowIcon(QIcon(os.path.join('images', 'cobweb-64.png')))

    # widget, open a new tab on the default homepage
    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl(self.default_homepage)

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        # we only want to update the url when it's from the correct tab
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  # if no tab under the click, open new tab
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        # if we only have one tab we cant really close that
        if self.tabs.count() < 2: 
            return

        self.tabs.removeTab(i)

    # responsible for updating the current web view's title
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - CobWeb" % title)

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    # widget, open file
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    # widget, save page in HTML
    # (in utf8)
    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")

        if filename:
            html = self.tabs.currentWidget().page().toHtml()
            with open(filename, 'w') as f:
                f.write(html.encode('utf8'))

    # widget for printing selected page
    def print_page(self):
        # dlg = QPrintPreviewDialog()
        # dlg.paintRequested.connect(self.browser.print_)
        # dlg.exec_()

        self._printer = QPrinter()
        self._printer.setPaperSize(QSizeF(80 ,297), QPrinter.Millimeter)
        r = QPrintDialog(self._printer)
        if r.exec_() == QPrintDialog.Accepted:
            self._page.print(self._printer, self.print_completed)

    # the designated homepage (when home icon is clicked)
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl(self.default_homepage))

    def navigate_to_url(self):  # does not receive the url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("https")

        self.tabs.currentWidget().setUrl(q)

    # responsible for updating the url bar in the correct
    # web view
    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        if q.scheme() == 'https':
            # secure padlock icon if scheme is SSL
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))

        else:
            # insecure padlock icon if scheme is not SSL
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

# run everything basically, if we're in the main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("CobWeb")
    app.setOrganizationName("CobWeb")
    app.setOrganizationDomain("CobWeb")

    window = MainWindow()

    app.exec_()
