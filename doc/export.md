# Update System and Install Python3 and Pip

First, update your system and then install Python and Pip:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3 python3-pip -y
```

# Install uv

To install `uv`, use the following command:

```bash
pip3 install uv
```

# Clone the Project to Root

Clone the project to the root directory:

```bash
cd /root
git clone https://github.com/erfjab/conflux.git
```

# Map Docker Files

Edit the `docker-compose.yml` file related to Marzban:

```bash
nano /opt/marzban/docker-compose.yml
```

Add the following lines under the `volumes` section:

```yaml
volumes:
    - /var/lib/marzban:/var/lib/marzban
    - /root/conflux/docker/export/usermodel.py:/code/app/models/user.py
```

Then restart the Marzban service:

```bash
marzban restart
```

# Return to the Conflux Folder

Go back to the Conflux folder:

```bash
cd /root/conflux
```

# Copy the .env File

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Edit the `.env` file with `nano .env` and fill in the details for `export host`, `export username`, and `export password` (with or without sudo access). After completing, save and close the file.

# Run the Export Script

Execute the following commands:

```bash
uv sync
```

```bash
uv run export.py
```

After the process is complete, a file named `export.json` will be created. Make sure to back up this file, as you will need it during the import step.

# Final Step

After the process is complete, remove the Docker volume mappings to ensure the changes persist.