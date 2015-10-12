#!/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# encoding: utf-8

import os
import sys
import logging

d = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, d)

from src.applestuff import hide_from_dock
from src.tunnit import Tunnit

# Apple stuff
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

from Cocoa import *
from Foundation import NSObject


start_time = NSDate.date()

UPDATE_INTERVAL = 1

tunnit = Tunnit()

class TunnitWindow(NSWindowController):

    days_field = objc.IBOutlet()
    hours_field = objc.IBOutlet()
    minutes_field = objc.IBOutlet()
    seconds_field = objc.IBOutlet()
    description_field = objc.IBOutlet()

    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
        self.updateDisplay()

    @objc.IBAction
    def pressOk_(self, sender):
        tunnit.stop()
        self.updateDisplay()

    def updateDisplay(self):
        t = tunnit.get_time()
        self.days_field.setStringValue_(t.days)
        self.hours_field.setStringValue_(t.hours)
        self.minutes_field.setStringValue_(t.minutes)
        self.seconds_field.setStringValue_(t.seconds)


class TunnitDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):

        self.tunnit = tunnit

        self.statusItem = NSStatusBar.systemStatusBar().statusItemWithLength_(
            NSVariableStatusItemLength)
        self.statusImage = NSImage.alloc()

        self.error = False
        # Icons
        self.statusItem.setToolTip_('Working status')
        self.statusItem.setHighlightMode_(TRUE)
        self.statusItem.setEnabled_(TRUE)


        # Menu
        self.error = True
        self.menu = NSMenu.alloc().init()

        #self.description_field = NSTextField.alloc().init()
        #self.description_field.setStringValue_("Foo")
        self.description_display = NSMenuItem.alloc().init()
        #self.description_display.setView_(self.description_field)
        self.description_display.setTitle_("Tunnit")
        self.description_display.setToolTip_("Working status")
        #self.description_display.setKeyEquivalent_('l')
        self.menu.addItem_(self.description_display)

        self.time_display = NSMenuItem.alloc().init()
        self.time_display.setTitle_("0h 0m 0s")
        self.menu.addItem_(self.time_display)



        # Sync and Quit buttons

        self.statusbutton = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Change status', 'syncall:', '')
        self.menu.addItem_(self.statusbutton)

        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Quit', 'terminate:', '')
        self.menu.addItem_(menuitem)
        self.statusItem.setMenu_(self.menu)
        self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(
            start_time, float(UPDATE_INTERVAL), self, 'sync:', None, True)

        NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer,
                                                     NSDefaultRunLoopMode)
        self.timer.fire()
        NSLog("Tunnit started!")

    def syncall_(self, notification):
        self.tunnit.toggle()

        # Show the window
        #viewController.showWindow_(viewController)

        # Bring app to top
        #NSApp.activateIgnoringOtherApps_(True)

        self.sync_(notification)

    def sync_(self, notification):
        if self.tunnit.status:
            self.statusItem.setTitle_(u"Working")
            self.statusbutton.setTitle_("Stop working")
        else:
            self.statusItem.setTitle_(u"Free")
            self.statusbutton.setTitle_("Start working")

        self.time_display.setTitle_(tunnit.get_formatted_time())
        if self.tunnit.status:
            self.statusItem.setTitle_("W: %s" % tunnit.get_formatted_time())

        self.description_display.setTitle_(u"%s" % self.tunnit.description)


    def applicationShouldTerminate_(self, notification):
        self.tunnit.stop()
        return 1


if __name__ == "__main__":
    try:
        logging.basicConfig(format="%(asctime)-15s %(levelname)s %(message)s")
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        app = NSApplication.sharedApplication()
        app.hide_(TRUE)
        delegate = TunnitDelegate.alloc().init()
        app.setDelegate_(delegate)
        hide_from_dock()
        # Initiate the controller with a XIB
        #viewController = TunnitWindow.alloc().initWithWindowNibName_("Tunnit")
        # Show the window
        #viewController.showWindow_(viewController)

        # Bring app to top
        NSApp.activateIgnoringOtherApps_(True)
        AppHelper.runEventLoop()
    except KeyboardInterrupt:
        delegate.terminate_()
        AppHelper.stopEventLoop()
        pass
