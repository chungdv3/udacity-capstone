#!/bin/bash
export FLASK_APP="app.py"
export FLASK_DEBUG=1
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/capstone"
export EXCITED="true"
export AUTH0_DOMAIN="dev-uizy8vy4polqae3g.us.auth0.com"
export API_AUDIENCE="capstone-app"
echo "setup.sh script executed successfully!"
