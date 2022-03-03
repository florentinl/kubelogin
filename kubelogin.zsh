effective_url=$(curl -Ls https://kubelogin.test.viarezo.fr -o /dev/null -w %{url_effective})
echo '\e]8;;'$effective_url'\e\\Login to staging cluster !\e]8;;\e\\\n'
download_dir = $(xdg-user-dir DOWNLOAD)
#download_dir=/mnt/c/users/flore/Downloads
while [ ! -f $download_dir/config_tmp ]; do
  sleep 5s
done;
echo downloaded
mv $download_dir/config_tmp ~/.kube/config2
if [ -f ~/.kube/config ]; then 
  KUBECONFIG=~/.kube/config:~/.kube/config2 kubectl config view --flatten > /tmp/config;
  mv /tmp/config ~/.kube/config;
  rm ~/.kube/config2;
else
  mv ~/.kube/config2 ~/.kube/config
fi;
echo loaded
