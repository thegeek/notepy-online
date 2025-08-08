"""Resource management for the Notepy Online application.

This module provides comprehensive resource management for the Notepy Online
application, including cross-platform application data directory management,
configuration file handling, and SSL certificate generation.

Features:
- Cross-platform application data directory management
- Configuration file creation and management using TOML format
- SSL certificate and private key generation for HTTPS support
- Certificate validation and expiration checking
- Resource structure verification and bootstrap commands
- Secure file permissions and access control
- Platform-specific directory handling (Windows, macOS, Linux)

The ResourceManager class provides a unified interface for managing all application
resources, ensuring consistent behavior across different operating systems and
providing secure, configurable SSL certificate generation for web server security.
"""

import ipaddress
import os
import platform
import stat
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import toml
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID


class ResourceManager:
    """Manages application resources and configuration."""

    def __init__(self) -> None:
        """Initialize the resource manager."""
        self.app_name: str = "notepy-online"
        self.resource_dir: Path = self._get_app_data_dir()
        self.config_file: Path = self.resource_dir / "config.toml"
        self.ssl_dir: Path = self.resource_dir / "ssl"
        self.ssl_cert_file: Path = self.ssl_dir / "server.crt"
        self.ssl_key_file: Path = self.ssl_dir / "server.key"
        self.notes_dir: Path = self.resource_dir / "notes"
        self.logs_dir: Path = self.resource_dir / "logs"

    def _get_app_data_dir(self) -> Path:
        """Get the application data directory for the current OS.

        Returns:
            Path to the application data directory

        Raises:
            RuntimeError: If the operating system is not supported
        """
        system: str = platform.system().lower()

        if system == "windows":
            app_data: Optional[str] = os.environ.get("APPDATA")
            if not app_data:
                raise RuntimeError("APPDATA environment variable not found")
            return Path(app_data) / self.app_name

        elif system == "darwin":  # macOS
            home_dir_mac: Path = Path.home()
            return home_dir_mac / "Library" / "Application Support" / self.app_name

        elif system == "linux":
            home_dir_linux: Path = Path.home()
            return home_dir_linux / ".local" / "share" / self.app_name

        else:
            raise RuntimeError(f"Unsupported operating system: {system}")

    def create_resource_structure(self) -> None:
        """Create the resource directory structure.

        Raises:
            RuntimeError: If directory creation fails
        """
        try:
            # Create main resource directory
            self.resource_dir.mkdir(parents=True, exist_ok=True)

            # Create SSL directory
            self.ssl_dir.mkdir(parents=True, exist_ok=True)

            # Create notes directory
            self.notes_dir.mkdir(parents=True, exist_ok=True)

            # Create logs directory
            self.logs_dir.mkdir(parents=True, exist_ok=True)

            print(f"✅ Created resource directory: {self.resource_dir}")
            print(f"✅ Created SSL directory: {self.ssl_dir}")
            print(f"✅ Created notes directory: {self.notes_dir}")
            print(f"✅ Created logs directory: {self.logs_dir}")

        except Exception as e:
            raise RuntimeError(f"Failed to create resource structure: {e}")

    def get_default_config(self) -> Dict[str, Any]:
        """Get the default configuration.

        Returns:
            Dictionary containing default configuration values
        """
        return {
            "app": {
                "name": "Notepy Online",
                "version": "0.1.0",
                "description": "A professional note-taking and management platform",
            },
            "server": {
                "host": "localhost",
                "port": 8443,
                "ssl_enabled": True,
                "auto_start": False,
            },
            "notes": {
                "auto_save": True,
                "max_title_length": 200,
                "max_content_length": 100000,
                "default_tags": [],
            },
            "ui": {
                "theme": "dark",
                "language": "en",
                "timezone": "UTC",
            },
            "security": {
                "ssl_cert_days": 365,
                "ssl_country": "US",
                "ssl_state": "CA",
                "ssl_locality": "San Francisco",
                "ssl_organization": "Notepy Online",
                "ssl_common_name": "localhost",
            },
        }

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file.

        Returns:
            Configuration dictionary

        Note:
            If the configuration file doesn't exist, returns default configuration.
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config: Dict[str, Any] = toml.load(f)
                    return config
            except Exception as e:
                print(f"Warning: Failed to load config, using defaults: {e}")

        return self.get_default_config()

    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file.

        Args:
            config: Configuration dictionary to save

        Raises:
            RuntimeError: If configuration cannot be saved
        """
        try:
            # Ensure resource directory exists
            self.resource_dir.mkdir(parents=True, exist_ok=True)

            with open(self.config_file, "w", encoding="utf-8") as f:
                toml.dump(config, f)
            print(f"✅ Configuration saved to: {self.config_file}")
        except Exception as e:
            raise RuntimeError(f"Failed to save configuration: {e}")

    def generate_ssl_certificate(
        self,
        days_valid: int = 365,
        country: str = "US",
        state: str = "CA",
        locality: str = "San Francisco",
        organization: str = "Notepy Online",
        common_name: str = "localhost",
    ) -> None:
        """Generate SSL certificate and private key.

        Args:
            days_valid: Number of days the certificate is valid
            country: Country code for certificate
            state: State/province for certificate
            locality: City/locality for certificate
            organization: Organization name for certificate
            common_name: Common name for certificate

        Raises:
            RuntimeError: If certificate generation fails
        """
        try:
            # Ensure SSL directory exists
            self.ssl_dir.mkdir(parents=True, exist_ok=True)

            # Generate private key
            private_key: rsa.RSAPrivateKey = rsa.generate_private_key(
                public_exponent=65537, key_size=2048
            )

            # Create certificate
            subject: x509.Name = x509.Name(
                [
                    x509.NameAttribute(NameOID.COUNTRY_NAME, country),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
                    x509.NameAttribute(NameOID.COMMON_NAME, common_name),
                ]
            )
            issuer: x509.Name = subject

            cert: x509.Certificate = (
                x509.CertificateBuilder()
                .subject_name(subject)
                .issuer_name(issuer)
                .public_key(private_key.public_key())
                .serial_number(x509.random_serial_number())
                .not_valid_before(datetime.utcnow())
                .not_valid_after(datetime.utcnow() + timedelta(days=days_valid))
                .add_extension(
                    x509.SubjectAlternativeName(
                        [
                            x509.DNSName(common_name),
                            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                        ]
                    ),
                    critical=False,
                )
                .sign(private_key, hashes.SHA256())
            )

            # Save private key
            with open(self.ssl_key_file, "wb") as f:
                f.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                )

            # Save certificate
            with open(self.ssl_cert_file, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))

            # Set secure permissions on key file
            os.chmod(self.ssl_key_file, stat.S_IRUSR | stat.S_IWUSR)

            print(f"✅ SSL certificate generated: {self.ssl_cert_file}")
            print(f"✅ SSL private key generated: {self.ssl_key_file}")
            print(f"✅ Certificate valid for {days_valid} days")

        except Exception as e:
            raise RuntimeError(f"Failed to generate SSL certificate: {e}")

    def check_ssl_certificate(self) -> Dict[str, Any]:
        """Check SSL certificate status.

        Returns:
            Dictionary with certificate information
        """
        result: Dict[str, Any] = {
            "cert_file_exists": False,
            "key_file_exists": False,
            "cert_valid": False,
            "days_remaining": 0,
            "expires": None,
        }

        if not self.ssl_cert_file.exists():
            return result

        result["cert_file_exists"] = True

        if not self.ssl_key_file.exists():
            return result

        result["key_file_exists"] = True

        try:
            # Load and validate certificate
            with open(self.ssl_cert_file, "rb") as f:
                cert_data: bytes = f.read()
                cert: x509.Certificate = x509.load_pem_x509_certificate(cert_data)

            now: datetime = datetime.utcnow()
            not_after: datetime = cert.not_valid_after

            result["cert_valid"] = now < not_after
            result["expires"] = not_after.isoformat()

            if result["cert_valid"]:
                days_remaining: timedelta = not_after - now
                result["days_remaining"] = days_remaining.days

        except Exception as e:
            print(f"Warning: Failed to check SSL certificate: {e}")

        return result

    def check_resource_structure(self) -> Dict[str, Any]:
        """Check resource structure status.

        Returns:
            Dictionary with resource structure information
        """
        return {
            "resource_dir_path": str(self.resource_dir),
            "resource_dir_exists": self.resource_dir.exists(),
            "ssl_dir_exists": self.ssl_dir.exists(),
            "notes_dir_exists": self.notes_dir.exists(),
            "logs_dir_exists": self.logs_dir.exists(),
            "config_file_exists": self.config_file.exists(),
        }
