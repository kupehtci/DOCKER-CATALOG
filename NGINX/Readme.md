# NGINX

## NGINX - basic

## NGINX - Application

## NGINX - Html

This NGINX example builds a custom HTML website just by using a custom Dockerfile image that using `nginx` image copies the HTML and serves it. 

```bash
# Build the Dockerfile into a container
docker build -t my-nginx-site .

# To run the created image using 8080 port
docker run -d -p 8080:80 --name mysite my-nginx-site
```

Now just open http://localhost:8080. 

