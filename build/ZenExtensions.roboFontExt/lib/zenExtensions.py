from mojo.tools import CallbackWrapper
from mojo import subscriber, events
import AppKit, asyncio
from mojo.subscriber import Subscriber, registerRoboFontSubscriber
import time

## https://stackoverflow.com/questions/7367438/sort-nsmenuitems-alphabetically-and-by-whether-they-have-submenus-or-not
def sortMenu(menu):
    itemArray = menu.itemArray().copy()

    # create a descriptor that will sort files alphabetically
    alphaDescriptor = AppKit.NSSortDescriptor.alloc().initWithKey_ascending_("title", True)
    # itemArray = itemArray.sortedArrayUsingDescriptors_([alphaDescriptor])

    # create a descriptor that will sort files alphabetically and based on existance of submenus
    submenuDescriptor = AppKit.NSSortDescriptor.alloc().initWithKey_ascending_("hasSubmenu", False)
    itemArray = itemArray.sortedArrayUsingDescriptors_([submenuDescriptor, alphaDescriptor])
    mechanicItem = None
    newItemArray = AppKit.NSMutableArray.alloc().init()
    for item in itemArray:
        if item.title() == "Mechanic 2":
            mechanicItem = item
            continue
        newItemArray.addObject_(item)
        # The following code fixes NSPopUpButton's confusion that occurs when
        # we sort this list. NSPopUpButton listens to the NSMenu's add notifications
        # and hides the first item. Sorting this blows it up.
        if item.isHidden():
            item.setHidden_(False)

        # While we're looping, if there's a submenu, go ahead and sort that, too.
        # if item.hasSubmenu():
        #     sortMenu(item.submenu())

    newItemArray.addObject_(AppKit.NSMenuItem.separatorItem())
    if mechanicItem:
        newItemArray.addObject_(mechanicItem)
    test = AppKit.NSArray.alloc().initWithArray_(newItemArray)
    menu.setItemArray_(test)
    return mechanicItem

async def sortExtensionsMenu():
    await asyncio.sleep(0.1)
    menubar = AppKit.NSApp().mainMenu()
    extensionsItem = menubar.itemWithTitle_("Extensions")
    extensionsMenu = extensionsItem.submenu()
    scriptsItem = menubar.itemWithTitle_("Scripts")
    scriptsMenu = scriptsItem.submenu()
    try:
        sortMenu(extensionsMenu)
        sortMenu(scriptsMenu)
    except:
        import traceback
        print("Err")
        print(traceback.format_exc())

async def main():
    await sortExtensionsMenu()

try:
    loop = asyncio.get_running_loop()
except RuntimeError:  # 'RuntimeError: There is no current event loop...'
    loop = None

if loop is not None:
    if loop.is_running():
        tsk = loop.create_task(main())
else:
    result = asyncio.run(main())
