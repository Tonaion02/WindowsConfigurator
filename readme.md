# WINDOWS-CONFIGURATOR

## What/Why
When i format my pc, and i must re-setup my windows' configuration i feel:

frustration - hatred - dismayed

This little project born from this annoyance.

There are so many things that can be automated.....so why not?

## How to execute the script
1. Open a powershell with admin permissions

2. Go to the directory of windows-configurator

3. execute the current command:

    ``` BASH
    $ setup.bat
    ```

## How personalize your setup
The way windows is setupped is expressed via resources.xml file.
A resource is a simple file that we want to handle in a certain manner. To indicate how we want to handle this resource we use the attribute.

Let's show an example:
``` XML
<?xml version="1.0"?>
<data>
    <!-- an empty directory named utils -->
    <directory name="utils"/>
    
    <!-- a directory named tools with three different resources placed in that -->
    <directory name="tools">
        <!-- a resource named premak5 that is downloaded like zip from the url, unzipped and placed under the tools directory -->
        <!-- with add_to_enviroment_path_variable="true" we add to the Path enviroment variable the path to this 
        resource -->
        <resource name="premake5" add_to_enviroment_path_variable="true" url="https://github.com/premake/premake-core/releases/download/v5.0.0-beta2/premake-5.0.0-beta2-windows.zip"/>
        <!-- a case similar to premake5, but in this case we don't add the path to the resource to the Path enviroment variable, we add an internal directory to the resource through internal_dirs attribute-->
        <resource name="cmake" internal_dirs="cmake-3.30.2-windows-x86_64" url="https://github.com/Kitware/CMake/releases/download/v3.30.2/cmake-3.30.2-windows-x86_64.zip"/>

        <!-- a new directory that is placed under tools directory -->
        <directory name="internal">
            <!-- this resource is marked with manually, so it is only an executable file that is put under the
            toManuallyInstall directory under BaseDir directory -->
            <resource name="firefox-installer" manually="true" extension="exe" url="https://download.mozilla.org/?product=firefox-stub&amp;os=win&amp;lang=it"/>
        </directory>
    </directory>

    <!-- You can use chocolatey to soddisfy some depencies -->
    <chocolatey-dependencies path="packages.config"/>
</data>
```

For a complete guide about tags and attribute to use to build your perfect setup for Windows, see [doc.md](./doc.md)  