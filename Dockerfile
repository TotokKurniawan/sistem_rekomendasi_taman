FROM php:8.2-cli

# Install dependensi sistem yang dibutuhkan
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www/html

# Copy seluruh file project
COPY . /var/www/html

# Install vendor dependencies lewat composer
RUN composer install --no-dev --optimize-autoloader

# Set permission folder storage
RUN chmod -R 777 storage bootstrap/cache

# Jalankan server bawaan PHP yang langsung mengarah ke folder public
EXPOSE 8080
CMD ["php", "-S", "0.0.0.0:8080", "-t", "public"]
