# Use the official Golang image as the base image
FROM golang:1.23-alpine
# Set the Current Working Directory inside the container

RUN apk add --no-cache python3 py3-pip
RUN apk add --no-cache py3-psycopg2
RUN apk add --no-cache py3-dotenv

WORKDIR /api
# Copy go mod file
COPY go.mod go.sum ./
# Download all dependencies. Dependencies will be cached if the go.mod file is not changed
RUN go mod download
# Copy the source from the current directory to the Working Directory inside the container
COPY . .
# Build the Go app
#RUN go build -o main .
# Expose port 8080 to the outside world
EXPOSE 8080
# Command to run the executable
CMD ["go", "run", "main.go"]
