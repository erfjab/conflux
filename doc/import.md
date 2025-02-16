# Update System and Install Python3 and Pip

First, update your system and install Python 3 and Pip:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3 python3-pip -y
```

# Clone Conflux Project to Root

Clone the Conflux project to the root directory:

```bash
cd /root
git clone https://github.com/erfjab/conflux.git
```

# Install uv

Install `uv` using pip:

```bash
pip3 install uv
```

# Add export.json File to Conflux

Add the `export.json` file (from the previous step) to the Conflux folder.

# Return to the Conflux Folder

Go back to the Conflux folder:

```bash
cd /root/conflux
```

# Copy and Edit the .env File

Copy the `.env.example` file to `.env` and fill in the details for `import host`, `import username`, and `import password`:

```bash
cp .env.example .env
nano .env
```

# Ensure All Protocols Are Active in Marzban

Before proceeding, ensure that all required protocols (vmess, vless, trojan, shadowsocks) are active in your Marzban panel.

# Map Files

Edit the `docker-compose.yml` file for Marzban:

```bash
nano /opt/marzban/docker-compose.yml
```

Add the following line under the `volumes` section:

```yaml
volumes:
  - /var/lib/marzban:/var/lib/marzban
  - /root/conflux/docker/import/usermodel.py:/code/app/models/user.py
  - /root/conflux/docker/import/crud.py:/code/app/db/crud.py
```

Then restart the Marzban service:

```bash
marzban restart
```

# Execute Final Commands

Run the following commands:

```bash
uv sync
```

```bash
uv run import.py
```

# Execution Process

1. First, duplicate users are checked, and the number of duplicates is displayed.
2. Then, a list of admin and non-duplicate admin users for import is shown.
   After the process is complete, a file named `duplicates.json` will be created. Make sure to back up this file.
3. If you enter `y`, all non-duplicate users will be added to your Marzban.

# Final Step

After the process is complete, remove the Docker volume mappings to ensure the changes persist.
