# DOCUMENTATION

In the following we describe the meaning of each tag and attribute that you can use in resourse.xml.

## Tags

| Name                              | Description and use                                                                   |
|:----------------------------------|:--------------------------------------------------------------------------------------|
| \<data\>                          | used like the root tag of the resources.xml                                           |
| \<directory>\                     | used to create a directory under the current working directory                        |
| \<resource\>                      | used to indicate a resource in the operating system                                   |
| \<chocolatey-dependencies\>       | used to indicate the file where is listed the dependenceis to resolve with chocolatey |

## Attributes
The attributes is used to specify some options and important information for each tag.

Description of attributes:
| Name                              | Description and use                                                                       |
|:----------------------------------|:------------------------------------------------------------------------------------------|
|name                               | used to decide the name of the resource on the filesystem                                 |
|url                                | url where to retrieve the resource                                                        |
|install                            | indicate that the resource must be installed                                              |
|manually_install                   | indicate that the resource must be placed under the directory toManuallyInstall           |
|add_to_enviroment_path_variable    | indicate that the path to resource must be placed in the Path enviroment variable         |
|internal_dirs                      | internal directories of path to resource must be place in the Path enviroment variable    |

Properties of attributes:
| Name                              | Type  | Default Value | Optional  | Appliable                     |
|:----------------------------------|:------|:--------------|:----------|:------------------------------|
|name                               |string | not default   | no        | \<directory\>,\<resource\>    |
|url                                |string | not default   | no        | \<resource\>                  |
|install                            |bool   | false         | yes       | \<resource\>                  |
|manually_install                   |bool   | false         | yes       | \<resource\>                  |
|add_to_enviroment_path_variable    |bool   | false         | yes       | \<resource\>                  |
|internal_dirs                      |string | ""            | yes       | \<resource\>                  |

RULES:
when we are writing the resources.xml we must consider certain constraints
- manually_install == True & install == True
- internal_dirs must be a set of string divided by a semicolun, for example: "internal_dir1;internal_dir2"

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