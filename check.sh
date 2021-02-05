#cont =  docker ps -a --format "{{.Names}}"

#cont=()
#while IFS= read -r line; do
#   cont+=( "$line" )
#done < <( docker ps -a --format "{{.Names}}" )
#chk="scrp"
#[[ " ${cont[@]} " =~ " ${chk} " ]] && echo "true" || echo "false"

##mapfile -t cont < <( docker ps -a --format "{{.Names}}" )
#echo ${cont[@]}
#chk="scrp"
#if [ chk == ${cont[@]} ]; then
#   echo "cont exists"
#else
#   echo "don't exist"
#fia


cont=()
while IFS= read -r line; do
   cont+=( "$line" )
done < <( docker ps -a --format "{{.Names}}" )
chk="scrp"
[[ " ${cont[@]} " =~ " ${chk} " ]] && docker stop scrp; docker container rm scrp; docker run -d --name scrp -p 8000:8000 auto || docker run -d --name scrp -p 8000:8000 auto

