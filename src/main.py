from panda3d.core import VirtualFileSystem
from panda3d.core import Multifile
from panda3d.core import Filename
from direct.showbase import VFSImporter
from panda3d.core import *
print(ConfigVariableString("model-path"))
from panda3d.core import loadPrcFileData
from panda3d import core
import sys
from direct.stdpy import file, glob
import os
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog


if sys.version_info >= (3, 0):
    import builtins
else:
    import __builtin__ as builtins

root = Tk()
root.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("p3d files","*.p3d"),("all files","*.*")))

p3dname = root.filename
root.destroy()
multifileRoot = str(ExecutionEnvironment.getCwd())
sys.path.append(multifileRoot)
ExecutionEnvironment.setEnvironmentVariable("MAIN_DIR", Filename(multifileRoot).toOsSpecific())
getModelPath().appendDirectory(multifileRoot)
trueFileIO = False
if not trueFileIO:
        # Replace the builtin open and file symbols so user code will get
        # our versions by default, which can open and read files out of
        # the multifile.
        builtins.open = file.open
 #       if sys.version_info < (3, 0):
  #              builtins.file = file.open
   #             builtins.execfile = file.execfile
        os.listdir = file.listdir
        os.walk = file.walk
        os.path.join = file.join
        os.path.isfile = file.isfile
        os.path.isdir = file.isdir
        os.path.exists = file.exists
        os.path.lexists = file.lexists
        os.path.getmtime = file.getmtime
        os.path.getsize = file.getsize
        sys.modules['glob'] = glob
vfs = VirtualFileSystem.getGlobalPtr()

mf = Multifile()
mf.openRead(p3dname)
i = mf.findSubfile('p3d_info.xml')
p3dInfo = None
p3dPackage = None
p3dConfig = None
allowPythonDev = False
if i >= 0 and hasattr(core, 'readXmlStream'):
    stream = mf.openReadSubfile(i)
    p3dInfo = core.readXmlStream(stream)
    mf.closeReadSubfile(stream)
if p3dInfo:
    p3dPackage = p3dInfo.FirstChildElement('package')
if p3dConfig:
    allowPythonDev = p3dConfig.Attribute('allow_python_dev')
if allowPythonDev:
    allowPythonDev = int(allowPythonDev)
    guiApp = p3dConfig.Attribute('gui_app')

vfs.mount(Filename(p3dname), multifileRoot, VirtualFileSystem.MFReadOnly)
moduleName = '__main__'
if p3dPackage:
    mainName = p3dPackage.Attribute('main_module')
    if mainName:
        moduleName = mainName
print(moduleName)
VFSImporter.register()
VFSImporter.reloadSharedPackages()
loadPrcFileData('', 'default-model-extension .bam')
dirName = Filename(multifileRoot).toOsSpecific()
importer = VFSImporter.VFSImporter(dirName)

loaderr = importer.find_module(moduleName)

mainModule = loaderr.load_module(moduleName)
