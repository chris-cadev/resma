#!/bin/bash -e

show_help() {
  echo "Usage: $(basename "$0") [OPTIONS]

Generates a Gource visualization as an animated GIF.

Options:
  -o DIR    Output directory (default: .demos/progress)
  -n NAME   Base filename (default: progress_YYYY-MM-DD)
  -h        Show this help message
"
  exit 0
}

output_dir="$(dirname "$(realpath "$0")")/../.demos/progress"
filename="progress_$(date +%Y-%m-%d\(%H%M\))"

while getopts "o:n:h" opt; do
  case "$opt" in
    o) output_dir="$OPTARG" ;;
    n) filename="$OPTARG" ;;
    h) show_help ;;
    *) show_help ;;
  esac
done

mkdir -p "$output_dir"
video_path="$output_dir/$filename.mp4"
gif_path="$output_dir/$filename.gif"

gource --seconds-per-day 1 --auto-skip-seconds 1 -800x600 -o - \
  | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - \
    -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 "$video_path"

ffmpeg -i "$video_path" -vf "fps=15,scale=800:-1:flags=lanczos" -c:v gif "$gif_path"

rm "$video_path"
