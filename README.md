# Open Acidification Server
Software for the Open Acidification central web server which interfaces with the individual pH-Stat units.


## Deployment:
Navigate to the main project directory and execute the following commands:
* `sudo sh scripts/install.sh` (Vagrant runs this automatically when provisioning)
* `sudo sh scripts/install_vue_dependencies.sh ` (If using Vagrant, run this on the host machine, NOT the guest)
* `scripts/build.sh`
* `sudo sh scripts/run_prod.sh`