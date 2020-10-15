# ismo_validation
This repository contains the numerical experiments for the arxiv paper [Iterative Surrogate Model Optimization (ISMO): An active learning algorithm for PDE constrained optimization with deep neural networks arXiv:2008.05730
](https://arxiv.org/abs/2008.05730)

Validation runs for the ismo algorithm

Clone with

    git clone --recursive git@github.com:kjetil-lye/ismo_validation.git


## Running in virtualenv

To make sure one has all the python packages required (and that one does not mess up ones python directory), one can use ```virtualenv```. [First install it (for python3)](https://virtualenv.pypa.io/en/latest/installation/) :

    pip3 install --user virtualenv

or you can leave out the ```--user``` option if you want it to be available for all users.

Then create a new virtual environment ([see the documentation for what is going on](https://virtualenv.pypa.io/en/latest/userguide/)):

    virtualenv3 .venv

activate the environment

     source .venv/bin/activate

Then, *only for the first time*, install the needed packages (after doing ```source .venv/bin/activate```):

    pip install -r requirements.txt

Now you can run the commands below. To leave the virtual enviroment, use

    deactivate

which will give you back the ordinary shell.

In general, to use ```virtualenv``` from a new terminal window once you have the ```.venv``` setup, you do

    cd <path to ismo_airfoil>
    source .venv/bin/activate
    # Now you are in the virtual environemnt (promp should have a (.venv) in it)
    cd validation/examples/sine
    bash run.sh --submitter bash
    # do some more
    deactivate



