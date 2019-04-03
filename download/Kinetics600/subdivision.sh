for i in {01..40}; do
    cat kinetics_train.csv | head -n 1 > train$i.txt
done

total=$( cat kinetics_train.csv | wc -l )
let total=total-1
cat kinetics_train.csv | tail -n $total > tmp.txt


for train in $( ls train[0-3]* ); do
    cat tmp.txt | head -n 10000 >> $train
    let total=total-10000
    echo $total
    cat tmp.txt | tail -n $total > tmp2.txt
    mv tmp2.txt tmp.txt
done

cat tmp.txt >> train40.txt
