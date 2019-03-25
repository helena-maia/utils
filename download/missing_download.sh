lista=$(echo {01..40})


for x in $lista; do
    python missing_download.py ../io/list/train/train$x.txt ../io/video$x/ ../io/missing_download/missing$x.txt
    total_txt=$(cat ../io/missing_download/missing$x.txt | wc -l)
    total_path=$(ls ../io/video$x | wc -l)
    let total=$total_txt+$total_path
    echo video$x $total
done
