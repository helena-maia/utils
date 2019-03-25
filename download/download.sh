count=16

for train in $( ls ../io/list/train/_train1[6-9]* ); do
    python download.py $train ../io/video$count/ tmp$count/
    rm -r tmp$count/    
    let count=count+1
done
