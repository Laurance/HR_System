
# Docker-compose local setup

Open a terminal and navigate to the `HR_System/` directory 
(if you are running the project on Windows make sure you have the Docker Desktop app running).
Run the following commands:

```bash
docker-compose build
docker-compose up
```

Leave the previous commands running and open a new terminal tab 
in order to create a superuser and apply the migrations. 
Helper scripts for Linux/WSL are available in the `scripts/` directory:


```bash
/scripts/create_superuser.sh
/scripts/migrate.sh
```

### Possible errors:

_Based on the OS you are using, the bash scripts may fail to run due to line breaks errors 
(e.g. `/bin/bash^M: bad interpreter`).
In this case you will need to apply some command-line file formatting tools 
such as `dos2unix` or `unix2dos` on each of these scripts._

# How to access the application

If running on Windows, add 127.0.0.1 in allowed hosts
   - Open Notepad as an administrator mode
   - Open C:\Windows\System32\drivers\etc\hosts
   - Add 127.0.0.1 at the end of the file

You may now interact with the application at 
[127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
