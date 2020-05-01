#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -b <path/to/baselines/folder> [options]"
   echo "     This script is used to reproduce the result of DDPG+HER algo attempting"
   echo "     to learn Dexterous hand control on the SHadow Dexterous hand with touch sensors"
   echo " -b <path>: (required) input path to baseline folder"
   echo " -r <env name>: (optional) runs the provided model with HER algo in the provided env"
   echo " -f <path to model file>: (must go with -r option) "
   exit 1 # Exit script after printing help
}

while getopts "b:r:f:" opt
do
   case "$opt" in
      b ) HOME_DIR="$OPTARG" ;;
      r )
        RUN_MODE=1
        ENV_NAME="$OPTARG" ;;
      f )
        MODEL_FILE="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
      * ) exit 0 ;;
   esac
done

if [ ! -d $HOME_DIR ]; then
    HOME_DIR=${CWD}
    echo "Assuming that baselines are present at: ${HOME_DIR}"
fi

# Go to home directory
echo "Move to directory ${HOME_DIR}"
cd "$HOME_DIR"

if [ -z ${RUN_MODE} ]; then
    #DDPG+HER
    BLOCK_ENV=HandManipulateBlock-v0
    EGG_ENV=HandManipulateEgg-v0
    PEN_ENV=HandManipulatePen-v0


    BLOCK_ENV_TOUCH=HandManipulateBlock-v0
    EGG_ENV_TOUCH=HandManipulateEgg-v0
    PEN_ENV_TOUCH=HandManipulatePen-v0

    BLOCK_FILE_TOUCH="${BLOCK_ENV_TOUCH}_her_2M_t0"
    EGG_FILE_TOUCH="${EGG_ENV_TOUCH}_her_2M_t0"
    PEN_FILE_TOUCH="${PEN_ENV_TOUCH}_her_2M_t0"


    BLOCK_FILE="${BLOCK_ENV}_her_2M_t0"
    EGG_FILE="${EGG_ENV}_her_2M_t0"
    PEN_FILE="${PEN_ENV}_her_2M_t0"
    # mkdir ${HOME_DIR}/models/${BLOCK_FILE}

    mpirun -np 10 python -m baselines.run --alg=her --env=$BLOCK_ENV --num_timesteps=2e6 --save_path=${HOME_DIR}/models/${BLOCK_FILE} --log_path="${HOME_DIR}/logs/${BLOCK_FILE}" --seed=23 --num_env=2 
    mpirun -np 10 python -m baselines.run --alg=her --env=$EGG_ENV --num_timesteps=2e6 --save_path=${HOME_DIR}/models/${EGG_FILE} --log_path="${HOME_DIR}/logs/${EGG_FILE}" --seed=23 --num_env=2 
    mpirun -np 10 python -m baselines.run --alg=her --env=$PEN_ENV --num_timesteps=2e6 --save_path=${HOME_DIR}/models/${PEN_FILE} --log_path="${HOME_DIR}/logs/${PEN_FILE}" --seed=23 --num_env=2 


    mpirun -np 10 python -m baselines.run --alg=her --env=$BLOCK_ENV_TOUCH --num_timesteps=2e6 --save_path=${HOME_DIR}/models/${BLOCK_FILE_TOUCH} --log_path="${HOME_DIR}/logs/${BLOCK_FILE_TOUCH}" --seed=83 --num_env=2 
    mpirun -np 10 python -m baselines.run --alg=her --env=$EGG_ENV_TOUCH --num_timesteps=2e6 --save_path=${HOME_DIR}/models/${EGG_FILE_TOUCH} --log_path="${HOME_DIR}/logs/${EGG_FILE_TOUCH}" --seed=83 --num_env=2 
    mpirun -np 10 python -m baselines.run --alg=her --env=$PEN_ENV_TOUCH --num_timesteps=2e6 --save_path=${HOME_DIR}/models/${PEN_FILE_TOUCH} --log_path="${HOME_DIR}/logs/${PEN_FILE_TOUCH}" --seed=83 --num_env=2 
else
    echo "Running Model ${MODEL_FILE}"
    if [ -f ${MODEL_FILE} ]; then
        python -m baselines.run --alg=her --env=$ENV_NAME --num_timesteps=0 --load_path=${MODEL_FILE} --seed=11 --play
    fi
fi