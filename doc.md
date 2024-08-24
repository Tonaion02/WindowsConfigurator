# DOCUMENTATION

In the following we describe the meaning of each tag and attribute that you can use in resourse.xml.

## Tags
- \<data\>: this tag is used as root tag of the resources.xml.
- \<directory\>: this tag is used to create a directory under the current working directory. 
- \<resource\>: this tag is used.  
- \<chocolatey-dependencies\>: this tag is used to 

## Attributes

| Name                              | Type  | Default Value | Optional  | Appliable                     |
|:----------------------------------|:------|:--------------|:----------|:------------------------------|
|name                               |string | not default   | no        | \<directory\>,\<resource\>    |
|url                                |string | not default   | no        | \<resource\>                  |
|install                            |bool   | false         | yes       | \<resource\>                  |
|manually_install                   |bool   | false         | yes       | \<resource\>                  |
|add_to_enviroment_path_variable    |bool   | false         | yes       | \<resource\>                  |
|internal_dirs                      |string | ""            | yes       | \<resource\>                  |

## Example

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