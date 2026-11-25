#!/bin/sh
# Generates a self-signed certificate for Nexus and its Docker registry.
# Only for development/testing: in production, put your real certificate
# in ./certs as nexus.crt (full chain) and nexus.key.
set -eu

CERT_DIR=/certs
CRT="$CERT_DIR/nexus.crt"
KEY="$CERT_DIR/nexus.key"

if [ -s "$CRT" ] && [ -s "$KEY" ]; then
  echo "Certificate already present in $CERT_DIR, skipping generation."
  exit 0
fi

echo "Generating self-signed certificate for $NEXUS_HOST and $REGISTRY_HOST..."
openssl req -x509 -nodes -newkey rsa:2048 -sha256 -days 825 \
  -keyout "$KEY" -out "$CRT" \
  -subj "/CN=$NEXUS_HOST" \
  -addext "subjectAltName=DNS:$NEXUS_HOST,DNS:$REGISTRY_HOST,DNS:localhost,IP:127.0.0.1"

chmod 644 "$CRT"
chmod 600 "$KEY"
echo "Certificate created: $CRT"
