# Not so reliable. Usually better to use Audacity

audio_file=$1
export audio_file
ffmpeg -i $audio_file -filter_complex "[0:a]silencedetect=n=-50dB:d=0.3[outa]" -map [outa] -f s16le -y /dev/null |& F='-aq 70 -v warning' perl -MPOSIX -ne 'INIT { $ss=0; $se=0; } if (/silence_start: (\S+)/) { $ss=$1; $ctr+=1; printf "ffmpeg -nostdin -i $ENV{audio_file} -ss %f -t %f $ENV{F} -y %03d.wav\n", $se, ($ss-$se), $ctr; }  if (/silence_end: (\S+)/) { $se=$1; } END { printf "ffmpeg -nostdin -i $ENV{audio_file} -ss %f $ENV{F} -y %03d.wav\n", $se, $ctr+1; }' | bash -x
