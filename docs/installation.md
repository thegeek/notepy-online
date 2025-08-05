# 📦 Installation Guide

This guide will help you install and set up Notepy Online on your system.

## 🎯 Prerequisites

### System Requirements

- **Python**: 3.12 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 512MB RAM minimum (1GB recommended)
- **Storage**: 100MB free space
- **Network**: Internet connection for initial setup

### Python Installation

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer with "Add Python to PATH" checked
3. Verify installation: `python --version`

#### macOS
```bash
# Using Homebrew (recommended)
brew install python@3.12

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.12 python3.12-pip python3.12-venv
```

## 🚀 Installation Methods

### Method 1: PyPI Installation (Recommended)

```bash
# Install from PyPI
pip install notepy-online

# Verify installation
notepy-online --version
```

### Method 2: Development Installation

```bash
# Clone the repository
git clone https://github.com/your-org/notepy-online.git
cd notepy-online

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[test]"
```

### Method 3: Docker Installation

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install -e .

EXPOSE 8443
CMD ["notepy-online", "server"]
```

```bash
# Build and run
docker build -t notepy-online .
docker run -p 8443:8443 notepy-online
```

## ⚙️ Initial Setup

### 1. Bootstrap the Application

```bash
# Initialize application resources and SSL certificate
notepy-online bootstrap init
```

This command will:
- Create application directories
- Generate default configuration
- Create SSL certificate for HTTPS
- Set up logging configuration

### 2. Verify Installation

```bash
# Check resource status
notepy-online bootstrap check
```

Expected output:
```
✅ Resource directory: /path/to/app/data
✅ Configuration file: /path/to/app/data/config.toml
✅ SSL certificate: /path/to/app/data/ssl/server.crt
✅ SSL private key: /path/to/app/data/ssl/server.key
✅ Notes directory: /path/to/app/data/notes
✅ Logs directory: /path/to/app/data/logs
```

### 3. Start the Server

```bash
# Start web server
notepy-online server
```

Access the application at: `https://localhost:8443`

## 🔧 Configuration

### Default Configuration Locations

- **Windows**: `%APPDATA%/notepy-online/config.toml`
- **macOS**: `~/Library/Application Support/notepy-online/config.toml`
- **Linux**: `~/.local/share/notepy-online/config.toml`

### Basic Configuration

```toml
[server]
host = "localhost"
port = 8443
ssl_enabled = true

[notes]
auto_save_interval = 30
max_title_length = 200
max_content_length = 100000

[security]
password_min_length = 8
session_secret_length = 32

[logging]
level = "INFO"
log_to_file = true
log_to_console = true
```

## 🧪 Testing the Installation

### 1. Create a Test Note

```bash
# Create a note via CLI
notepy-online notes create -t "Welcome Note" -c "Welcome to Notepy Online!" -g welcome
```

### 2. List Notes

```bash
# List all notes
notepy-online notes list
```

### 3. Test Web Interface

1. Start the server: `notepy-online server`
2. Open browser: `https://localhost:8443`
3. Create a note through the web interface
4. Verify it appears in CLI: `notepy-online notes list`

### 4. Test API

```bash
# Test API endpoints
curl -k https://localhost:8443/api/notes
curl -k -X POST https://localhost:8443/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "API Test", "content": "Testing API"}'
```

## 🔒 Security Setup

### SSL Certificate

The application generates a self-signed SSL certificate by default. For production:

```bash
# Generate custom certificate
notepy-online bootstrap init \
  --country "US" \
  --state "California" \
  --locality "San Francisco" \
  --organization "Your Organization" \
  --common-name "your-domain.com"
```

### Custom SSL Certificates

```bash
# Start server with custom certificates
notepy-online server \
  --cert /path/to/certificate.crt \
  --key /path/to/private.key
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using the port
# Windows:
netstat -ano | findstr :8443
# macOS/Linux:
lsof -i :8443

# Use different port
notepy-online server -p 8444
```

#### 2. SSL Certificate Issues
```bash
# Regenerate SSL certificate
notepy-online bootstrap init --force
```

#### 3. Permission Errors
```bash
# Check directory permissions
ls -la ~/.local/share/notepy-online/

# Fix permissions
chmod 755 ~/.local/share/notepy-online/
```

#### 4. Python Version Issues
```bash
# Check Python version
python --version

# Should be 3.12 or higher
# If not, install correct version
```

### Getting Help

1. Check the [troubleshooting guide](../troubleshooting.md)
2. Search [existing issues](../../issues)
3. Create a new [issue](../../issues/new) with:
   - Operating system and version
   - Python version
   - Error messages
   - Steps to reproduce

## 📋 Installation Checklist

- [ ] Python 3.12+ installed
- [ ] Notepy Online installed
- [ ] Bootstrap initialization completed
- [ ] SSL certificate generated
- [ ] Web server starts successfully
- [ ] Web interface accessible
- [ ] CLI commands working
- [ ] API endpoints responding
- [ ] Test note created successfully

## 🔄 Updating

### Update from PyPI
```bash
pip install --upgrade notepy-online
```

### Update from Source
```bash
git pull origin main
pip install -e .
```

## 🗑️ Uninstallation

### Remove Package
```bash
pip uninstall notepy-online
```

### Remove Data (Optional)
```bash
# Windows
rmdir /s "%APPDATA%\notepy-online"

# macOS
rm -rf ~/Library/Application\ Support/notepy-online

# Linux
rm -rf ~/.local/share/notepy-online
```

---

**Next Steps**: 
- Read the [User Guide](user-guide.md) to learn how to use Notepy Online
- Check the [Configuration Guide](configuration.md) for customization options
- Explore the [API Reference](api-reference.md) for programmatic access 