
source: https://queirozf.com/entries/jupyter-kernels-how-to-add-change-remove#add-virtualenv-as-python-kernel

# Jupyter Notebook Kernels: How to Add, Change, Remove
Last updated: 08 Aug 2020

Examples were run on Ubuntu Linux

## Add Virtualenv as Python Kernel


Replace your-venv with your virtualenv name

Activate the virtualenv

    $ source your-venv/bin/activate

Install jupyter in the virtualenv

    (your-venv)$ pip install jupyter

Add the virtualenv as a jupyter kernel

    (your-venv)$ ipython kernel install --name "local-venv" --user

You can now select the created kernel your-env when you start Jupyter


## List kernels


Use jupyter kernelspec list

    $ jupyter kernelspec list
    Available kernels:
      global-tf-python-3    /home/felipe/.local/share/jupyter/kernels/global-tf-python-3
      local_venv2           /home/felipe/.local/share/jupyter/kernels/local_venv2
      python2               /home/felipe/.local/share/jupyter/kernels/python2
      python36              /home/felipe/.local/share/jupyter/kernels/python36
      scala                 /home/felipe/.local/share/jupyter/kernels/scala

## Remove kernel

Use jupyter kernelspec remove <kernel-name>

    $ jupyter kernelspec remove old_kernel
    Kernel specs to remove:
      old_kernel            /home/felipe/.local/share/jupyter/kernels/old_kernel
    Remove 1 kernel specs [y/N]: y
    [RemoveKernelSpec] Removed /home/felipe/.local/share/jupyter/kernels/old_kernel

## Change Kernel name

1) Use $ jupyter kernelspec list to see the folder the kernel is located in

2) In that folder, open up file kernel.json and edit option "display_name"
