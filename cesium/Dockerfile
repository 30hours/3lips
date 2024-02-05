# Use a lightweight base image
FROM httpd:2.4-alpine

# Set the working directory to Apache's document root
WORKDIR /usr/local/apache2/htdocs/

# Download and extract CesiumJS 1.114 release from GitHub
RUN apk --no-cache add curl unzip && \
    curl -L -o cesium.zip https://github.com/CesiumGS/cesium/releases/download/1.114/Cesium-1.114.zip && \
    unzip cesium.zip -d cesium && mv cesium/* . && rm cesium.zip && rm -r cesium

# Expose port 80
EXPOSE 80

# Start Apache in the foreground
CMD ["httpd-foreground"]
