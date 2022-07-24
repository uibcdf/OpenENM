# How to create and update a conda environment

## To develop the library

### Create env

If the name of the conda environment is `OpenENM`:

```bash
python create create_conda_env.py -n OpenENM -p 3.7 development_env.yaml
```

Now you can activate the environment with:

```bash
conda activate OpenENM
```

### Update env

With the environment activated:

```bash
update_conda_env.py conda_file
```bash

