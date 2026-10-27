# Elasticsearch con Docker Compose
Servicio local de Elasticsearch en un solo nodo, pensado para desarrollo, pruebas y entornos de laboratorio. Incluye persistencia de datos, healthcheck y autenticación básica mediante usuario elastic.

## Configuración
Crea un archivo .env en la misma carpeta que docker-compose.yml:
```env
ELASTIC_PASSWORD=CambiaEstaPasswordSegura
```
No subas el archivo .env a Git. Añádelo a .gitignore.

## Arrancar el servicio
```bash
docker compose up -d
```
Verificar el estado:

```bash
docker compose ps
```

Comprobar que Elasticsearch responde:

```bash
curl -u elastic:${ELASTIC_PASSWORD} http://localhost:9200
```
Ejemplo de respuesta esperada:

```json
{
  "name": "elasticsearch",
  "cluster_name": "docker-cluster",
  "cluster_uuid": "...",
  "version": {
    "number": "8.19.0"
  },
  "tagline": "You Know, for Search"
}
```

Comprobar salud del clúster
```bash
curl -u elastic:${ELASTIC_PASSWORD} \
  http://localhost:9200/_cluster/health?pretty
```

Estado recomendado en un nodo único:
* **yellow**: normal, porque no hay réplicas disponibles con un solo nodo.
* **red**: revisa los logs y el estado de los índices.

### Puertos expuestos

| Puerto | Uso |
|---|---|
| 9200 | API HTTP / REST de Elasticsearch | 
| 9300 | Transporte interno entre nodos |

Para acceso desde otras aplicaciones, usa:
```
http://localhost:9200
```

### Variables y recursos

| Variable | Valor por defecto | Descripción |
|---|---|---|
| ELASTIC_PASSWORD | Definida en .env | Contraseña del usuario elastic |
| ES_JAVA_OPTS | -Xms1g -Xmx1g | Memoria asignada a la JVM |
| discovery.type | single-node | Configuración para un nodo único | 
| xpack.security.enabled | true | Habilita autenticación y seguridad básica | 

Para aumentar la memoria de la JVM, modifica en docker-compose.yml:

```text
ES_JAVA_OPTS=-Xms2g -Xmx2g
```

Ambos valores deben ser iguales para evitar resizing frecuente de la JVM.

## Volúmenes

Los datos se almacenan en el volumen Docker:

```text
elasticsearch_data
```

Para inspeccionarlo:

```bash
docker volume ls
docker volume inspect elasticsearch_data
```

Los índices persisten aunque se detenga o recree el contenedor.

## Operaciones habituales

Ver logs
```bash
docker compose logs -f elasticsearch
```
Parar el servicio
```bash
docker compose down
```

Parar y conservar datos
```bash
docker compose down
```

El volumen no se elimina con down.

Eliminar contenedor y datos
```bash
docker compose down -v
```

Esto borra todos los índices y documentos almacenados en Elasticsearch.

Reiniciar desde cero
```bash
docker compose down -v
docker compose up -d
```
Crear un índice de prueba
```bash
curl -u elastic:${ELASTIC_PASSWORD} \
  -X PUT "http://localhost:9200/test-index" \
  -H "Content-Type: application/json" \
  -d '{
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  }'
```

Insertar un documento:
```bash
curl -u elastic:${ELASTIC_PASSWORD} \
  -X POST "http://localhost:9200/test-index/_doc" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hola Elasticsearch",
    "level": "INFO",
    "timestamp": "2026-10-21T15:00:00Z"
  }'
```

Consultar documentos:

```bash
curl -u elastic:${ELASTIC_PASSWORD} \
  "http://localhost:9200/test-index/_search?pretty"
```

Integración con aplicaciones
Ejemplo para una aplicación .NET:

```text
Elasticsearch__Url=http://localhost:9200
Elasticsearch__Username=elastic
Elasticsearch__Password=CambiaEstaPasswordSegura
```

Ejemplo para Docker Compose en otra pila:

```yaml
environment:
  - ELASTICSEARCH_URL=http://elasticsearch:9200
  - ELASTICSEARCH_USERNAME=elastic
  - ELASTICSEARCH_PASSWORD=${ELASTIC_PASSWORD}
``` 
Si ambos servicios están en la misma red de Docker, usa el nombre del servicio:
```text
http://elasticsearch:9200
```

### Seguridad
Esta configuración habilita seguridad con usuario y contraseña, pero está pensada para desarrollo local.

Para producción se recomienda:
* Usar al menos tres nodos master-eligible. 
* Configurar TLS para transporte HTTP y entre nodos. 
* Crear usuarios y roles con privilegios mínimos. 
* No exponer 9200 directamente a Internet. 
* Configurar snapshots y backups. 
* Usar secretos gestionados, por ejemplo HashiCorp Vault, en lugar de .env.
