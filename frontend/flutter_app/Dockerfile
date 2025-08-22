FROM nginx:stable-alpine

# Nettoyer les fichiers Nginx par défaut
RUN rm -rf /usr/share/nginx/html/*

# Copier le build Flutter web
COPY build/web /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]