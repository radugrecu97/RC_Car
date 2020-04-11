# RC_Car

####1 Pre-requisites
Expect needed for interactive config script
>sudo apt-get install expect

Make sure your user is part of the docker group
>sudo usermod -aG docker radugrecu97

Add a group reserved for git if you don't have one already.
>sudo groupadd -g 7777 gitusers

Add desired users to previously created group
>sudo usermod -G gitusers 'name_user

Change git repo permissions
>sudo chgrp -R gitusers .git/objects/
>sudo chmod -R g+rws .git/objects


####2 Preparing the build environment
>sudo ./setup

P.S. To clean the generated files, run:
>sudo ./setup -c

or
>sudo ./setup --clean