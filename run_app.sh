#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python -c "from app.app import app; app.run(debug=True, host='127.0.0.1', port=5000)"

