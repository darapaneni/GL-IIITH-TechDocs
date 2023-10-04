$app = "techdocs-frontend"
$location = $PWD.ToString() + ":/app"
docker build -t $app .
docker run -d -p 56733:80 --name=$app -v $location $app