# autochoice-app

#Test Local

#start customer-service
cd latest/customer-service
sh ./start.sh

#start api-gateway
cd latest/api-gateway
sh ./start.sh

#minikube k8s testing
#Create images
cd latest/customer-service
sh ./build.sh
cd latest/api-gateway
sh ./build.sh

#Setup minikube
#Deploy the services
minikube image load customer-svc:latest
minikube image load gateway-svc:latest
cd latest/deployment
kubectl apply -f deployment.yaml

minikube ip

curl http://<minikube ip>:<port-defined-in-the-deployement-file>/customers
