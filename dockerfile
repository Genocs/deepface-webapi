FROM python:3.9.13

# http port exposed outside the container
EXPOSE 5400

# Set the Current Working Directory inside the container
WORKDIR /app


# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# These are for libGL.so issues
# RUN apt-get update
# RUN apt install libgl1-mesa-glx
# RUN apt-get install -y python3-opencv
# RUN pip3 install opencv-python
# RUN pip3 install opencv-python-headless==4.5.3.56

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

RUN echo "Flask==2.1.0" > requirements.txt
RUN pip install -r requirements.txt
RUN pip install deepface
RUN pip install Werkzeug==2.2.2

# Copy the source code into the container 
COPY ./src/ ./src/

# Run the application
CMD ["python", "src/main.py"]