# menuTitle: ZenExtensions

import AppKit

from mojo.tools import CallbackWrapper
from mojo.subscriber import Subscriber, registerRoboFontSubscriber, registerSubscriberEvent, getRegisteredSubscriberEvents


class ZenExtensions(Subscriber):

    debug = True

    ## https://stackoverflow.com/questions/7367438/sort-nsmenuitems-alphabetically-and-by-whether-they-have-submenus-or-not
    def sortMenu(self, menu):
        itemArray = menu.itemArray().copy()

        # Create a descriptor that will sort files alphabetically
        alphaDescriptor = AppKit.NSSortDescriptor.alloc().initWithKey_ascending_("title", True)
        # itemArray = itemArray.sortedArrayUsingDescriptors_([alphaDescriptor])

        # Create a descriptor that will sort files alphabetically and based on existance of submenus
        submenuDescriptor = AppKit.NSSortDescriptor.alloc().initWithKey_ascending_("hasSubmenu", False)
        itemArray = itemArray.sortedArrayUsingDescriptors_([submenuDescriptor, alphaDescriptor])
        bottomItems = []
        newItemArray = AppKit.NSMutableArray.alloc().init()
        for item in itemArray:
            if item.title() in ["Mechanic 2", "Update Menu", "Reveal Script folder"]:
                bottomItems.append(item)
                continue
            newItemArray.addObject_(item)
            # The following code fixes NSPopUpButton's confusion that occurs when
            # we sort this list. NSPopUpButton listens to the NSMenu's add notifications
            # and hides the first item. Sorting this blows it up.
            if item.isHidden():
                item.setHidden_(False)

            # While we're looping, if there's a submenu, go ahead and sort that, too.
            # if item.hasSubmenu():
            #     self.sortMenu(item.submenu())

        newItemArray.addObject_(AppKit.NSMenuItem.separatorItem())
        for item in bottomItems:
            newItemArray.addObject_(item)
        test = AppKit.NSArray.alloc().initWithArray_(newItemArray)
        menu.setItemArray_(test)
        return

    def sortExtensionsMenu(self):
        menubar = AppKit.NSApp().mainMenu()
        extensionsItem = menubar.itemWithTitle_("Extensions")
        extensionsMenu = extensionsItem.submenu()
        scriptsItem = menubar.itemWithTitle_("Scripts")
        scriptsMenu = scriptsItem.submenu()
        try:
            self.sortMenu(extensionsMenu)
            self.sortMenu(scriptsMenu)
        except:
            import traceback
            print("Err")
            print(traceback.format_exc())

    def roboFontDidFinishLaunching(self, info):
        self.sortExtensionsMenu()

    def extensionDidRemoteInstall(self, info):
        self.sortExtensionsMenu()
        
    def extensionDidUninstall(self, info):
        self.sortExtensionsMenu()


if "com.rafalbuchner.zenExtensions.extensionInstalledEvent" not in getRegisteredSubscriberEvents().keys():
    registerSubscriberEvent(
        subscriberEventName="com.rafalbuchner.zenExtensions.extensionInstalledEvent",
        methodName="extensionDidRemoteInstall",
        lowLevelEventNames=["com.robofontmechanic.extensionDidRemoteInstall"],
        dispatcher="roboFont",
        delay=1,
        documentation="This is a custom subscriber method that looks for whether an extension installed on Mechanic."
    )

if "com.rafalbuchner.zenExtensions.extensionUninstalledEvent" not in getRegisteredSubscriberEvents().keys():
    registerSubscriberEvent(
        subscriberEventName="com.rafalbuchner.zenExtensions.extensionUninstalledEvent",
        methodName="extensionDidUninstall",
        lowLevelEventNames=["com.robofontmechanic.extensionDidUninstall"],
        dispatcher="roboFont",
        delay=1,
        documentation="This is a custom subscriber method that looks for whether an extension uninstalled on Mechanic."
    )

registerRoboFontSubscriber(ZenExtensions)