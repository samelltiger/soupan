processname="soupan"

#all_time = $[`ps aux|grep "$processname"|grep -v grep|awk '{print $9}'`]
#echo $all_time

#for tim in $all_time;do
#echo $tim
#done

for pid in $(ps aux |grep $processname |grep -v grep|awk '{print $2}'); do
kill -9 $pid
done

/etc/init.d/mongod restart

/root/anaconda2/envs/python3/bin/python3.5 /data/wwwroot/soupan/pyspider/getReallyUrl.py&
