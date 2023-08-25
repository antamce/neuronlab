Neuronlab is a virtual laboratory allowing for visualisation of electrophysiological processes of neurones. The project is made as a supplementary educational resource.  Neuronlab is currently in active development, so it is a good idea to keep up with the updates.

INSTALLATION:

1. Install [Anaconda](https://www.anaconda.com/download).
2. Create a virtual environment: 
- Open Anaconda command prompt, type in  `conda create -n <name> python=3.9.12 -y`, where <name> is the desired name of your environment. Before activating the environment, update conda by typing `conda update conda`. Activate the environment using `conda activate <name>`. This should automatically switch you from the base environment to the <name> environment.
3. Install Brian2
- After switching to the new environment, type in `conda install -c conda-forge brian2 -y` and wait for the installation of the package.
4. Install matplotlib
- Run `conda install matplotlib`
5. Install C++ build tools
Brian2 library requires  C++ build tools:
- Install the [Microsoft Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
- In Build tools, install C++ build tools and ensure the latest versions of MSVCv… build tools and Windows 10 SDK are checked (or Windows 11 SDK if you are using Windows 11).
- Switch to the base environment by typing `conda deactivate`
- Run `conda update setuptools -y` and make sure that your `setuptools` package has at least version 34.4.0
6. Install pyglet
- Re-activate your virtual environment by typing `conda activate <name>`
- Find the path to your newly created environment (usually in your `Users\username\anaconda3\envs\<name>`).
- In the command prompt, type `pip install --target=<path to venv>\Lib\site-packages pyglet`, where `<path to venv>` is the path to your virtual environment.
7. Copy the repository.
- Install [Git](https://git-scm.com/download/win) on your computer
- Create a folder for the local copy of the project. Go into the folder, right-click anywhere and choose ”Open Git Bash here”
- Type in `git clone https://github.com/Volkova-Ekaterina/neuronlab.git`
8. Change the directory 
- Open anaconda prompt and run `cd <path to venv>` to change the directory to the directory with the project.
9. Run the app 
- Type in `python run.py`

HOW TO USE NEURONLAB:

1. Open Neuronlab. 
2. The sliders on the panel to the right of the synaptic image are used to set the times of synaptic inputs. Set inhibitory and excitatory spike times using the sliders. No more than three excitatory and three inhibitory inputs are allowed. With the timings set, you may choose the mediators using respective dropdown lists. If not modified, the app will automatically use default values that are displayed in the bottom right panel.
3. Modify other parameters of the system using designated boxes below the sliders. If not modified, the app will automatically use default values. 
4. Press the ‘START’ button. Calculations may take time and depend on the technical specifications of your PC. The first-ever calculation may take 1-2 minutes and is usually significantly longer than the subsequent ones. 
5. A graph of the post-synaptic transmembrane potential will appear on the scope below the synaptic image as soon as the calculation is finished. 
6. To create a different graph, modify parameters to desired values and press ‘START’ again.

