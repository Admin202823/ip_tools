# **ip_tools**

## Download and Installation :

You can download only the python script do you need (The 2 files are not linked and run just 1 script work)

> [!WARNING]
> This is a python project and it need's python was installed on your computer to work.

**Windows :**

- Open cmd :
`win+r`, type `cmd` and press `enter`.
> [!IMPORTANT]
> If you launch it in administator (you are in "System32" foler) it's recommanded to go in an other foler, your desktop folder for exemple (C:/Users/{your username}/Desktop/).
- Create a folder : `mkdir ip_tools`
- Go to the folder : `cd ip_tools`
- Download the files : `wget https://github.com/Admin202823/ip_tools/archive/refs/heads/main.zip`
- Extract the files : `tar -xf main.zip`
- Go to "script" foler : `cd script`
- You can see the 2 files with this command : `dir`
- To execute script use : `python {script_name}`

## How to use :

### The script [ip_extractor.py](script/ip_extractor.py) :

This script can used to extract a list of IP from a file (a log for example, I have used this script to extract IP from my sshd log).

To use this script : execute his (`python ip_extractor.py`) in the "script" folder.

### The script [country_extractor.py](script/country_extractor.py) :

This script can get the country of a ip list (extracted by [ip_extractor.py](script/ip_extractor.py) for exemple), it generates a graph and a output list with the country of the ip.

