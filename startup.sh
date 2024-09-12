python -m uvicorn main:app --host 0.0.0.0

# add below line to app service -> configuration -> startup script
gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app