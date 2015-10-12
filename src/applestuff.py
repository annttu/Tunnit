# encoding: utf-8

#from Foundation import *
from AppKit import *
#from PyObjCTools import AppHelper

def hide_from_dock():
    """hide icon from dock"""
    NSApplicationActivationPolicyProhibited = 2
    NSApp.setActivationPolicy_(NSApplicationActivationPolicyProhibited)

