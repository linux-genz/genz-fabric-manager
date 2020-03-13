Fabric Manager is a proxy between the ResourceCreator and [LLamaS](https://github.com/linux-genz/llamas)

### Ways to Install

##### PIP3

Make sure pip3 is installed

    sudo apt install python3-pip
 
 Point to a fabric-manager git project:
 
    pip3 install git+https://github.com/linux-genz/genz-fabric-manager@latest

#### Raw source
Create a symlink from the cloned project into python3 dist-packages

    git clone https://github.com/linux-genz/genz-fabric-manager
  
Add path for Current user (without sudo)

    sudo ln -s <path_to_genz-fabric-manager>/fabric_manager ~/.local/lib/python3.6/site-packages/fabric_manager
  
Add path for all users (need sudo):

    sudo ln -s <path_to_genz-fabric-manager>/fabric_manager /usr/lib/python3/dist-packages/fabric_manager
  
### How To Use

##### If installed using pip3

    python3 fabric_manager -vvvvv
    
##### If installed from source

    cd <path_to_cloned_genz-fabric-manager>/fabric_manager    
    ./fm_server.py -vvvv

### Ways to Build/Package

##### Using python's setuptools

To build/rebuild pip3 dist, run the following from the top of the project (where setup.py is):

    python3 setup.py sdist bdist_wheel

##### .rpm build

    python setup.py bdist_rpm

More info on how to build rpm from python source:

https://docs.python.org/2.0/dist/creating-rpms.html

https://docs.python.org/2/distutils/builtdist.html

##### deb build
Run from top of the project:

    python setup.py --command-packages=stdeb.command bdist_deb
    
For more info:

https://pypi.org/project/stdeb/#quickstart-1-install-something-from-pypi-now-i-don-t-care-about-anything-else
