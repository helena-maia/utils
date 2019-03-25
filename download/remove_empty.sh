lista=$(echo {01..40})

for x in $lista; do
    echo video$x
    ls ../io/video$x | wc -l
    python remove_empty.py ../io/video$x/
    ls ../io/video$x | wc -l
    echo " "
done
