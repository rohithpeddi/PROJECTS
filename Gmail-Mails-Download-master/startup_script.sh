#! /bin/bash

# 1. Create ProgressBar function
# 1.1 Input is currentState($1) and totalState($2)
function ProgressBar {
# Process data
    let _progress=(${1}*100/${2}*100)/100
    let _done=(${_progress}*4)/10
    let _left=40-$_done
# Build progressbar string lengths
    _fill=$(printf "%${_done}s")
    _empty=$(printf "%${_left}s")

# 1.2 Build progressbar strings and print the ProgressBar line
# 1.2.1 Output example:
# 1.2.1.1 Progress : [########################################] 100%
printf "\n\n\r Total Progress : [${_fill// /#}${_empty// /-}] ${_progress}%%\n\n"

}

# Variables
_count=0

#download all emails in .eml format
python /src/gmail-backup-master/dobackup.py &&
#put each .eml file into corresponding folder
find . -name "*.eml" -exec sh -c 'NEWDIR=`basename "$1" .eml` ; mkdir "$NEWDIR" ; mv "$1" "$NEWDIR" ' _ {} \; &&
#count no. of total folders created to  display progress
export _end=$(find . -mindepth 1 -type d | wc -l) &&
#rename .eml in each directory with it's corresponding meta data( mail date, to , from, subject)
python3 /src/rename_eml.py &&
mv /src/emailconverter-2.0.1-all.jar /src/emails_backup/ &&
#use the above copied jar to recursively extract email body and attachments from all .eml files
for d in ./*; do   if [ -d "$d" ]; then  java -jar emailconverter-2.0.1-all.jar -a  $d/*.eml; rm $d/*.eml; _count=$((_count+1)); ProgressBar ${_count} ${_end}; fi; done &&
#this jar's work is done
rm /src/emails_backup/emailconverter-2.0.1-all.jar &&
#my work is done
printf '\nDownload Finished!\n'

