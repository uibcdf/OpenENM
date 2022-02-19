# Developing guide

## Developers' Guide in the documentation

Check, first of all, the "Developers' Guide" section of the online documentation.

## Adding the required dependencies

This library needs some third python packages to work. And not only to work, but be documented,
tested or developed, for instance. The file 'requirements.yaml' contains a list of conda
channels and packages required to:

- Run the setup.py script ('setup' section)
- Use the library for production ('production' section)
- Run the library tests ('test' section)
- Compile the documentation ('docs' section)
- Work in the library development ('development' section)
- Build a conda package with this library ('conda-build')

This is the file where the library dependencies need to be included. And once the file has been
updated, execute the Python script 'broadcast\_requirements.py'. This last step will produce
individual yaml files to create and update, following the instructions of the next section, different conda
environments depending on the tasks you need to do.

## How to prepare the conda environments to work with this repository

You will find here a directory called 'conda-envs'. This directory contains all the info and
scripts you need to create and update a conda environment. Let's first have a look to the yaml
files:

```python
cd conda-envs
ls *.yaml
build_env.yaml  development_env.yaml  docs_env.yaml  production_env.yaml  setup_env.yaml  test_env.yaml
```

Each yaml file has the list of required packages and conda channels in case you want to:
- Build a conda package with this library ('build_env.yaml').
- Work in the library development ('development_env.yaml')
- Compile the documentation of this library ('docs_env.yaml')
- Use the library just for production ('production_env.yaml')
- Run the setup.py script ('setup_env.yaml')
- Run the library tests ('test_env.yaml')

This yaml files were produced with the script 'broadcast_requirements.py' and the file
'requirements.yaml' as indicated in the previous exception.

Finnally, to create a conda environment use the script 'create_conda_env.py' the following way:

```bash
# In this case the name of the environment is also "OpenGNM"
# the Python version of our new environment is 3.7
# and the yaml file will be the one to work on the library development
python create_conda_env.py -n OpenGNM -p 3.7 development_env.yaml
```

You can already activate the environment to start working in the library development:

```bash
conda activate OpenGNM
```

In case the list of dependencies changed and the environment needs to be updated, use the Python
script 'update_conda_env.py' with the environment activated:

```bash
conda activate OpenGNM
python update_conda_env.py development_env.yaml
```

## How to contribute changes
- Clone the repository if you have write access to the main repo, fork the repository if you are a collaborator.
- Make a new branch with `git checkout -b {your branch name}`
- Make changes and test your code
- Ensure that the test environment dependencies (`conda-envs`) line up with the build and deploy dependencies (`conda-recipe/meta.yaml`)
- Push the branch to the repo (either the main or your fork) with `git push -u origin {your branch name}`
  * Note that `origin` is the default name assigned to the remote, yours may be different
- Make a PR on GitHub with your changes
- We'll review the changes and get your code into the repo after lively discussion!

## Checklist for updates
- [ ] Make sure there is an/are issue(s) opened for your specific update
- [ ] Create the PR, referencing the issue
- [ ] Debug the PR as needed until tests pass
- [ ] Tag the final, debugged version 
   *  `git tag -a X.Y.Z [latest pushed commit] && git push --follow-tags`
- [ ] Get the PR merged in

## Versioneer Auto-version
[Versioneer](https://github.com/warner/python-versioneer) will automatically infer what version 
is installed by looking at the `git` tags and how many commits ahead this version is. The format follows 
[PEP 440](https://www.python.org/dev/peps/pep-0440/) and has the regular expression of:
```regexp
\d+.\d+.\d+(?\+\d+-[a-z0-9]+)
```
If the version of this commit is the same as a `git` tag, the installed version is the same as the tag, 
e.g. `pyunitwizard-0.1.2`, otherwise it will be appended with `+X` where `X` is the number of commits 
ahead from the last tag, and then `-YYYYYY` where the `Y`'s are replaced with the `git` commit hash.
