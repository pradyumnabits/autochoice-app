## autochoice-app

## Test Local

### start customer-service
```
cd latest/customer-service
sh ./start.sh
```

### start api-gateway
```
cd latest/api-gateway
sh ./start.sh

cd latest/customer-service
python test.py

cd latest/api-gateway/test
python customer-service-test.py
```

## minikube k8s testing
### Create images
```
cd latest/customer-service
sh ./build.sh
cd latest/api-gateway
sh ./build.sh
```

## Setup minikube
### Deploy the services
```
minikube image load customer-svc:latest
minikube image load gateway-svc:latest
cd latest/deployment
kubectl apply -f deployment.yaml

minikube ip

curl http://<minikube ip>:<port-defined-in-the-deployement-file>/customers
```

## **How to run in EKS:**

- Install eksctl on your machine
```
$> brew tap weaveworks/tap
$> brew install weaveworks/tap/eksctl
```

- Create a Cluster
```
eksctl create cluster \
--name autohub-cluster \
--version 1.31 \
--region ap-south-1 \
--nodegroup-name ubuntu-nodes \
--node-type t2.micro \
--nodes 2
```

- create a namespace:
```
kubectl create namespace autohub
```

- Now tag the docker builds and push it to Docker hub
```
docker tag gateway-svc:latest <yourusername>/gateway-svc:<version>
docker push qlikstar/gateway-svc:0.1
```

- Update the AWS to use the newly created cluster. Prerequisite: Install AWS first
```
aws eks update-kubeconfig --name autohub-cluster --region ap-south-1
```

- Now apply the deployment file:
```
kubectl apply -f eks_deploy.yaml
```

- In order to get an endpoint, run the command:
```kubectl get service autohub-app -n autohub```

```
NAME              TYPE           CLUSTER-IP      EXTERNAL-IP                                                              PORT(S)        AGE
autohub-gateway   LoadBalancer   10.100.14.241   a376e54ff6ac947b3961003e7239a583-85014629.ap-south-1.elb.amazonaws.com   80:32247/TCP   90s
```


- Finally, Delete the cluster
```
eksctl delete cluster --name autohub-cluster --region ap-south-1
```