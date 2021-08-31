echo "全目录打包"
tar -zcf youget.tar.gz *
echo "打包文件传送到服务器"
scp youget.tar.gz youth:/root/app
echo "触发服务器解包"
ssh youth  '/root/app/deploy-youget.sh'

echo "删除打包文件"
rm youget.tar.gz

echo "you-get部署完成"
