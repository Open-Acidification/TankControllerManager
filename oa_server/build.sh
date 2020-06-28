# Build the frontend
cd oa_frontend
npm run build

# Migrate database models
cd ..
python3 manage.py makemigrations
python3 manage.py migrate