# lscom

a crude python script that lists available active com ports on your workstation. this should work cross platform, but has not been extensively tested.

this is useful if you plug in a console cable and you want to quickly identify which COM port is now available. note that actively use COM ports will not show in the output.

# example

```
$ lscom
['COM3']
```

# local installation

to install:

- clone repository.

- from your terminal `cd` into root of the repository.

- run `python -m pip install .`

- you should now be able to run `lscom` from your terminal

to remove:

- `python -m pip uninstall lscom`
