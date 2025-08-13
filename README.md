# Udacity Robotics Nanodegree: SLAM Project

This repository contains the code for the Simultaneous Localization and Mapping (SLAM) project from the Udacity Robotics Nanodegree program.

## Project Overview

This project focuses on implementing key SLAM algorithms to enable a robot to build a map of an unknown environment while simultaneously keeping track of its own location within that map.

## Software Requirements

The project has been developed and tested on the following platform:

* **Operating System:** Ubuntu 20.04 LTS (Focal Fossa)

* **ROS Distribution:** ROS Noetic Ninjemys

## Cloning the Repository

This project uses **Git Large File Storage (LFS)** to handle large data files, such as maps and log files, efficiently. To properly clone the repository and download these files, you must have Git LFS installed on your system.

### 1. Install Git LFS

First, install the Git LFS command-line extension on your system. You only need to do this once.

```
# Install Git LFS
sudo apt-get update
sudo apt-get install git-lfs

# Configure Git LFS for your user account
git lfs install

```

### 2. Clone the Repository

After installing Git LFS, you can clone the repository as you normally would. The LFS-tracked files will be downloaded automatically during the process.

```
git clone <repository_url>

```

If you already cloned the repository without Git LFS and see small "pointer" files instead of the actual data, navigate into the repository directory and run the following command to download the large files:

```
git lfs pull

```

## Running the Project

To run this project, you need to have ROS Noetic installed and configured on your Ubuntu 20.04 system.

### ROS Noetic Installation (if not already installed)

1. **Set up your sources.list:**

   ```
   sudo sh -c 'echo "deb [http://packages.ros.org/ros/ubuntu](http://packages.ros.org/ros/ubuntu) $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
   
   ```

2. **Set up your keys:**

   ```
   sudo apt install curl # if you haven't already installed curl
   curl -s [https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc](https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc) | sudo apt-key add -
   
   ```

3. **Update packages and install ROS Noetic:**

   ```
   sudo apt update
   sudo apt install ros-noetic-desktop-full
   
   ```

4. **Set up the environment:**

   ```
   echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
   source ~/.bashrc
   