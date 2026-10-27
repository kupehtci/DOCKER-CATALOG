# APISIX

Apache APISIX is a dynamic, real-time and high performance API Gateway. 

## Modes

It supports various modes: 
* **standalone mode**: Uses `apisix.yaml` as the configuration source for the routing, upstream, consumer and other configurations of the service. 
* **etcd**: uses etcd as teh configuration source. In this mode, the etcd container needs to be started. 

## Container images used

* `apache/apisix`: Apache APISIX
* `bitnamilegacy/etcd`: etcd from bitnami. 

# Versions
## standalone

This version deploys only the **apisix** service without dashboard and using the `apisix.yaml` file as configuration source. 

## complete

This version deploys the **apisix** service together with the dashboard and the **etcd** as backend configuration source. 
