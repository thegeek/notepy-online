# ⚙️ Configuration Guide

Complete guide to configuring Notepy Online for your needs.

## 🚀 Overview

Notepy Online uses TOML configuration files for all settings. The configuration is automatically created during bootstrap initialization and can be customized to suit your requirements.

## 📁 Configuration File Location

The configuration file is automatically created in the appropriate location for your operating system:

- **Windows**: `%APPDATA%/notepy-online/config.toml`
- **macOS**: `~/Library/Application Support/notepy-online/config.toml`
- **Linux**: `~/.local/share/notepy-online/config.toml`

## 🔧 Configuration Sections

### Server Configuration

```toml
[server]
# Server host address
host = "localhost"

# Server port number
port = 8443

# Enable SSL/HTTPS
ssl_enabled = true

# File upload size limit (bytes)
file_upload_size_limit = 10485760  # 10MB

# Maximum notes per user
max_notes_per_user = 1000

# Session timeout (seconds)
session_timeout = 3600  # 1 hour

# Enable CORS
cors_enabled = true

# Allowed CORS origins
cors_origins = ["*"]

# Enable request logging
request_logging = true

# Server timeout (seconds)
timeout = 30
```

### Notes Configuration

```toml
[notes]
# Auto-save interval (seconds)
auto_save_interval = 30

# Maximum title length
max_title_length = 200

# Maximum content length (bytes)
max_content_length = 100000  # 100KB

# Maximum tags per note
allowed_tags = 20

# Default theme (light, dark, auto)
default_theme = "dark"

# Enable note versioning
versioning_enabled = true

# Maximum versions per note
max_versions = 10

# Enable auto-backup
auto_backup_enabled = true

# Backup interval (hours)
backup_interval = 24

# Backup retention (days)
backup_retention = 30
```

### Security Configuration

```toml
[security]
# Minimum password length (for future auth)
password_min_length = 8

# Session secret length
session_secret_length = 32

# Rate limiting requests per window
rate_limit_requests = 100

# Rate limiting window (seconds)
rate_limit_window = 60

# Enable input sanitization
input_sanitization = true

# Allowed file types for uploads
allowed_file_types = ["txt", "md", "json"]

# Maximum file size (bytes)
max_file_size = 5242880  # 5MB

# Enable CSRF protection
csrf_protection = true
```

### Logging Configuration

```toml
[logging]
# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
level = "INFO"

# Maximum log file size (bytes)
max_file_size = 10485760  # 10MB

# Number of backup log files
backup_count = 5

# Log to file
log_to_file = true

# Log to console
log_to_console = true

# Log format
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Date format
date_format = "%Y-%m-%d %H:%M:%S"

# Enable request logging
request_logging = true

# Enable error logging
error_logging = true
```

### Database Configuration

```toml
[database]
# Storage type (json, sqlite)
storage_type = "json"

# Database file path (for JSON storage)
db_file = "notes.json"

# Enable database encryption
encryption_enabled = false

# Encryption key (auto-generated if not provided)
encryption_key = ""

# Database backup enabled
backup_enabled = true

# Backup frequency (hours)
backup_frequency = 24

# Backup retention (days)
backup_retention = 7
```

### SSL Configuration

```toml
[ssl]
# SSL certificate file path
cert_file = "ssl/server.crt"

# SSL private key file path
key_file = "ssl/server.key"

# Certificate validity days
validity_days = 365

# Certificate country
country = "US"

# Certificate state
state = "CA"

# Certificate locality
locality = "San Francisco"

# Certificate organization
organization = "Notepy Online"

# Certificate common name
common_name = "localhost"

# Enable SSL verification
verify_ssl = true
```

### Performance Configuration

```toml
[performance]
# Enable caching
caching_enabled = true

# Cache size limit (MB)
cache_size_limit = 100

# Cache TTL (seconds)
cache_ttl = 3600

# Enable compression
compression_enabled = true

# Compression level (1-9)
compression_level = 6

# Worker threads
worker_threads = 4

# Connection pool size
connection_pool_size = 10

# Request timeout (seconds)
request_timeout = 30
```

## 🔄 Environment Variables

You can override configuration values using environment variables:

```bash
# Server settings
export NOTEPY_HOST="0.0.0.0"
export NOTEPY_PORT="8080"
export NOTEPY_SSL_ENABLED="false"

# Logging
export NOTEPY_LOG_LEVEL="DEBUG"
export NOTEPY_LOG_TO_FILE="true"

# Security
export NOTEPY_RATE_LIMIT_REQUESTS="200"
export NOTEPY_RATE_LIMIT_WINDOW="60"

# Notes
export NOTEPY_MAX_CONTENT_LENGTH="200000"
export NOTEPY_AUTO_SAVE_INTERVAL="60"
```

## 🛠️ Configuration Management

### View Current Configuration

```bash
# Check configuration status
notepy-online bootstrap check

# View configuration file
cat ~/.local/share/notepy-online/config.toml
```

### Reset Configuration

```bash
# Reinitialize with default configuration
notepy-online bootstrap init
```

### Backup Configuration

```bash
# Backup current configuration
cp ~/.local/share/notepy-online/config.toml config_backup.toml
```

### Restore Configuration

```bash
# Restore from backup
cp config_backup.toml ~/.local/share/notepy-online/config.toml
```

## 🎯 Common Configuration Scenarios

### Development Environment

```toml
[server]
host = "localhost"
port = 8080
ssl_enabled = false

[logging]
level = "DEBUG"
log_to_console = true
log_to_file = false

[performance]
caching_enabled = false
compression_enabled = false
```

### Production Environment

```toml
[server]
host = "0.0.0.0"
port = 8443
ssl_enabled = true
timeout = 60

[logging]
level = "WARNING"
log_to_file = true
log_to_console = false

[security]
rate_limit_requests = 50
rate_limit_window = 60
input_sanitization = true

[performance]
caching_enabled = true
compression_enabled = true
worker_threads = 8
```

### High-Security Environment

```toml
[security]
password_min_length = 12
rate_limit_requests = 20
rate_limit_window = 60
input_sanitization = true
csrf_protection = true

[ssl]
verify_ssl = true
validity_days = 90

[logging]
level = "INFO"
log_to_file = true
backup_count = 10
```

### Resource-Constrained Environment

```toml
[performance]
caching_enabled = false
compression_enabled = true
worker_threads = 2
connection_pool_size = 5

[notes]
max_content_length = 50000  # 50KB
max_notes_per_user = 100

[logging]
level = "WARNING"
log_to_file = false
log_to_console = true
```

## 🔍 Configuration Validation

### Automatic Validation

The application automatically validates configuration on startup:

```bash
# Start server (will validate config)
notepy-online server
```

### Manual Validation

```bash
# Check configuration syntax
python -c "import toml; toml.load('config.toml')"
```

## 🚨 Configuration Errors

### Common Issues

#### Invalid TOML Syntax
```
Error: Invalid TOML syntax in config file
```
**Solution**: Check for syntax errors in the TOML file

#### Missing Required Fields
```
Error: Missing required configuration field 'server.host'
```
**Solution**: Ensure all required fields are present

#### Invalid Values
```
Error: Invalid port number: 99999
```
**Solution**: Use valid values within acceptable ranges

#### Permission Errors
```
Error: Cannot read configuration file
```
**Solution**: Check file permissions and ownership

## 🔧 Advanced Configuration

### Custom SSL Certificates

```toml
[ssl]
cert_file = "/path/to/custom/certificate.crt"
key_file = "/path/to/custom/private.key"
verify_ssl = true
```

### Custom Logging

```toml
[logging]
level = "DEBUG"
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
log_to_file = true
log_to_console = true
```

### Custom Rate Limiting

```toml
[security]
rate_limit_requests = 1000
rate_limit_window = 3600  # 1 hour
```

### Custom File Upload Settings

```toml
[server]
file_upload_size_limit = 52428800  # 50MB

[security]
allowed_file_types = ["txt", "md", "json", "pdf", "docx"]
max_file_size = 10485760  # 10MB
```

## 📊 Configuration Monitoring

### Log Configuration Changes

```toml
[logging]
level = "INFO"
log_config_changes = true
```

### Configuration Health Check

```bash
# Check configuration health
notepy-online bootstrap check
```

## 🔄 Configuration Migration

### Version Migration

When upgrading Notepy Online, the configuration may need updates:

1. **Backup current configuration**
2. **Run bootstrap init** to generate new defaults
3. **Merge custom settings** from backup
4. **Test configuration** with new version

### Example Migration Script

```bash
#!/bin/bash
# Configuration migration script

# Backup current config
cp ~/.local/share/notepy-online/config.toml config_backup.toml

# Reinitialize with new defaults
notepy-online bootstrap init

# Restore custom settings (manual process)
echo "Please manually restore custom settings from config_backup.toml"
```

## 💡 Best Practices

### Security
- Use strong SSL certificates in production
- Enable rate limiting for public deployments
- Regularly rotate session secrets
- Enable input sanitization

### Performance
- Adjust worker threads based on server capacity
- Enable caching for better performance
- Use compression for network efficiency
- Monitor resource usage

### Maintenance
- Regular configuration backups
- Log rotation and cleanup
- SSL certificate renewal
- Configuration validation

### Monitoring
- Enable appropriate log levels
- Monitor error rates
- Track performance metrics
- Regular health checks

---

**Related Documentation**:
- [Installation Guide](installation.md) - Initial setup
- [User Guide](user-guide.md) - Usage instructions
- [CLI Reference](cli-reference.md) - Command-line options
- [Troubleshooting Guide](troubleshooting.md) - Problem solving 