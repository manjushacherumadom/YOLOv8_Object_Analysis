# Use an official Python image as a base
FROM python:3.10

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first (for better caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r /app/requirements.txt


# Copy only the `app/` folder into `/app/`
COPY app/ /app/  

RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Expose the Flask port
EXPOSE 5000

# Run the application
CMD ["python", "/app/app.py"]