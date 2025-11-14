FROM ghcr.io/datagutten/upsmanager:latest AS static
RUN python /home/app/manage.py collectstatic --noinput

FROM nginx

COPY --from=static /home/app/static /home/app/static

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/nginx.conf
