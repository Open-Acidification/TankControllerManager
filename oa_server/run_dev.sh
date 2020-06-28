# To be run within the Vagrant VM

# Serve frontend
cd oa_frontend
npm run serve &

# Serve backend
cd ..
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py qcluster &
python3 manage.py runserver 0.0.0.0:8080