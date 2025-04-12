"""This file acts as the main module for this script."""

import traceback, adsk.core

import xml.etree.ElementTree as ET
import re, os



# Initialize the global variables for the Application and UserInterface objects.
_app = adsk.core.Application.get()
_ui  = _app.userInterface


# Code snipt from: https://github.com/thomasa88/fusion360-thomasa88lib/blob/master/utils.py
def get_fusion_deploy_folder():
    '''
    Get the Fusion 360 deploy folder.

    Typically:
     * Windows: C:/Users/<user>/AppData/Local/Autodesk/webdeploy/production/<hash>
     * Mac: /Users/<user>/Library/Application Support/Autodesk/webdeploy/production/<hash>

    NOTE! The structure within the deploy folder is not the same on Windows and Mac!
    E.g. see the examples for get_fusion_ui_resource_folder().
    '''

    _DEPLOY_FOLDER_PATTERN = re.compile(r'.*/webdeploy/(?:pre-)?production/[^/]+')

    # Strip the suffix from the UI resource folder, i.e.:
    # Windows: /Fusion/UI/FusionUI/Resources
    # Mac: /Autodesk Fusion 360.app/Contents/Libraries/Applications/Fusion/Fusion/UI/FusionUI/Resources

    return _DEPLOY_FOLDER_PATTERN.match(get_fusion_ui_resource_folder()).group(0)

def get_fusion_ui_resource_folder():
    '''
    Get the Fusion UI resource folder. Note: Not all resources reside here.

    Typically:
     * Windows: C:/Users/<user>/AppData/Local/Autodesk/webdeploy/production/<hash>/Fusion/UI/FusionUI/Resources
     * Mac: /Users/<user>/Library/Application Support/Autodesk/webdeploy/production/<hash>/Autodesk Fusion 360.app/Contents/Libraries/Applications/Fusion/Fusion/UI/FusionUI/Resources
    '''

    return adsk.core.Application.get().userInterface.workspaces.itemById('FusionSolidEnvironment').resourceFolder.replace('/Environment/Model', '')



def run(_context: str):
    """This function is called by Fusion when the script is run."""

    try:
        file_path = f'{get_fusion_deploy_folder()}/Neutron/Server/Scene/Resources/Environments/GreyRoom/GreyRoom.xml'
        
        if os.path.exists(file_path):
            tree = ET.parse(file_path)
        else:
            _ui.messageBox('\"GreyRoom.xml\" element not found.')
            return

        # Find the ToneMapping element
        tone_mapping = tree.getroot().find('.//ToneMapping')

        if tone_mapping is not None:
            if tone_mapping.get('ExposureBase') != '0':
                tone_mapping.set('ExposureBase', '0')

                # Save the changes back to the XML file
                tree.write(file_path)
            
            _ui.messageBox('ToneMapping ExposureBase is set to 0')
        else:
            _ui.messageBox('ToneMapping element not found.')

    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
