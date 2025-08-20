#/bin/bash
Root=${1:-.}
threshold_gb=${2:-0}
threshold_bytes=$(echo "scale=0; $threshold_gb * 1024 * 1024 * 1024" | bc | awk '{printf "%.0f", $1}')
model_temp=""
find "$Root" -type d -regextype posix-egrep -regex '.*/(FP16|OV_FP16-INT8_ASYM|OV_FP16-4BIT_DEFAULT)$' |while read -r dir
do
prec=$(basename "$dir")
model=`cut -d'/' -f2 <<< $dir`
#size=$(find "$dir" -type f -name "*.bin" -exec du -b {} + | awk '{total += $1} END {printf "%.2fG\n", total/1024/1024/1024}')
size=`find "$dir" -type f -name "*.bin" -exec du -b {} + | awk '{total += $1} END {printf "%.0f\n", total}'`
total_gb=$(awk -v total="$size" 'BEGIN {printf "%.2f", total/1024/1024/1024}')
if [ $threshold_bytes -eq 0 ]; then
    printf "%s %s:%s\n" "$model" "$prec" "${total_gb}GB"
else
    if [ $size -lt $threshold_bytes ]; then
        printf "%s %s:%s\n" "$model" "$prec" "${total_gb}GB"
        # if [ $model_temp !=  $model] ;then
        #     echo -e "\n $model" "prec" >> 1.txt
        # else
        #     echo -e "prec" >> 1.txt
        # fi
    fi
fi
model_temp=$model
done