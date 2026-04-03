#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "  Resetting compliance range and fleet..."
echo ""

bash "$SCRIPT_DIR/destroy-lab.sh"
bash "$SCRIPT_DIR/setup-lab.sh"
