#!/bin/bash
# Cắt 1 đoạn từ source, chuẩn hoá 1080x1920@30, encode (không làm đẹp — chủ kênh đã bỏ bước này).
# usage: render_segment.sh <work_dir> <n> <src_name> <start> <dur> <zoom 0|1|2> [speed]
#   zoom 1 = zoom chậm 7% suốt đoạn; 2 = như 1 nhưng bắt đầu cận hơn 12% (dùng cho cú cắt nhảy trong cùng 1 clip)
#   speed < 1 = chạy chậm (vd 0.88) khi clip ngắn hơn đoạn voice cần phủ; <dur> luôn là độ dài ĐẦU RA
W=$1; n=$2; src=$3; ss=$4; d=$5; z=$6; sp=${7:-1}
case "$z" in
  1) b=1;    vf="scale=w='trunc(1080*($b+0.07*t/$d)/2)*2':h='trunc(1920*($b+0.07*t/$d)/2)*2':eval=frame,crop=1080:1920" ;;
  2) b=1.12; vf="scale=w='trunc(1080*($b+0.07*t/$d)/2)*2':h='trunc(1920*($b+0.07*t/$d)/2)*2':eval=frame,crop=1080:1920" ;;
  *) vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" ;;
esac
in_d=$(python3 -c "print(round($d*$sp,3))")
mkdir -p "$W/seg"
ffmpeg -v error -y -ss "$ss" -t "$in_d" -i "$W/src/$src" -an \
  -vf "setpts=PTS/$sp,fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,$vf" \
  -t "$d" -c:v libx264 -preset fast -crf 17 -pix_fmt yuv420p "$W/seg/$n.mp4"
echo "seg $n done $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/seg/$n.mp4")"
