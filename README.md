# Shadow Hand Experiments (OpenAI gym and Mujoco Simulator)

This repository contains the scripts and results of running HER+DDPG experiments on the shadow dexterous hand.

## Pre-requisites

### OpenAI Gym
Please follow the [instructions](http://gym.openai.com/docs/#installation) to install the OpenAI gym in your system. As part of the OpenAI gym installation, make sure to install the `mujoco_py` wrapper as well with the provided [instructions](https://github.com/openai/mujoco-py#obtaining-the-binaries-and-license-key).

## OpenAI Baselines
The OpenAI Baselines can be installed by following the instructions [here](https://github.com/openai/baselines). Make sure you are able to run the example 1 given in the instructions that runs PPO with mujoco humanoid.

## Reproducing Results
Copy the the (run_shadow_experiments.sh)[./run_shadow_experiments.sh] into the baselines folder. 

### Training Agents
Run the following command to train all 6 agents for 200 epochs.
```
$ bash run_shadow_experiments.sh -b <path to baselines folder>
```

### Plotting Graphs
In order to plot the results from the logs run the following python script

```
$ python ./logs/hand_manipulator_lc_plotter.py -i < Dir path [touch logs]> -i <Dir path [no touch logs]> -t <title> -o <output file path>
```

### Visualizing the Policy
The (run_shadow_experiments.sh)[./run_shadow_experiments.sh] script can also be used to visualize the agent behavior. The following command template runs the the provided trained model in the provided mojovco environement. You can run `bash run_shadow_experiments.sh -h` for the usage message.

```
$ bash run_shadow_experiments.sh -b <path to baselines folder> -r HandManipulateBlock-v0 -f <path to baselines>/models/HandManipulateBlock-v0_her_2M_t0
```

