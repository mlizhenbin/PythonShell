#!/usr/bin/env bash
cd /log/canvas
grep "#WebLog#" canvas.log|awk -F " " '{print $8" "$7}'|awk -F "ms " '{print $1" "$2}'|awk '{s[$2] += $1; b[$2]++;max[$2]=max[$2]>$1?max[$2]:$1}END{ for(i in s){  print max[i], s[i]/b[i], b[i], i} }'|awk '{if($1>99){print $1"ms "int($2)"ms "$3" "$4}}'|sort -nr
