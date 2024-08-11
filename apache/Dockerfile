# Use the official Apache HTTP Server image
FROM httpd:2.4

# Enable necessary modules, switch from prefork to event MPM
RUN sed -i \
    -e 's/#LoadModule mpm_event_module modules\/mod_mpm_event.so/LoadModule mpm_event_module modules\/mod_mpm_event.so/' \
    -e 's/LoadModule mpm_prefork_module modules\/mod_mpm_prefork.so/#LoadModule mpm_prefork_module modules\/mod_mpm_prefork.so/' \
    /usr/local/apache2/conf/httpd.conf

# Create a directory for Apache logs
RUN mkdir -p /usr/local/apache2/logs/

# Copy custom configuration file into the container
COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf

# Set a default server name
RUN echo "ServerName lapierredelune.net" >> /usr/local/apache2/conf/httpd.conf

# Make sure we expose port 80 for HTTP traffic
EXPOSE 80
