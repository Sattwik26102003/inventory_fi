# Dockerfile

# --- Stage 1: Build ---
# Use an official Node.js runtime as a parent image.
# The 'alpine' version is a lightweight Linux distribution, resulting in a smaller image.
FROM node:18-alpine AS build

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (if available)
# This is done as a separate step to leverage Docker's layer caching.
# Dependencies will only be re-installed if these files change.
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# --- Stage 2: Production ---
# Use a clean, smaller base image for the final production stage
FROM node:18-alpine

# Set the working directory
WORKDIR /usr/src/app

# Copy the installed dependencies from the 'build' stage
COPY --from=build /usr/src/app/node_modules ./node_modules

# Copy the application code from the 'build' stage
COPY --from=build /usr/src/app .

# The application listens on a port defined by the PORT environment variable.
# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime.
# It does not actually publish the port.
EXPOSE 8080

# Define the command to run the application.
# 'npm start' is used as it's the standard way to run a production Node.js app.
CMD [ "npm", "start" ]
