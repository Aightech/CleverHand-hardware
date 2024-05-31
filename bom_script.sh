#merge all BOM file from KiCad/type/*/production/*_bom.csv into one file
#type: controller, modules
type_list="controller modules"

touch all_bom.csv
echo "" > all_bom.csv
for type in $type_list
do
#get all directory in KiCad/$type/
dir_list=$(ls -d KiCad/$type/*/)
for dir in $dir_list
do
    #remove the last character '/'
    dir=${dir%?}
    #get the bom file
    f=`ls $dir/production/*_bom.csv`
    cat $f >> all_bom.csv

done
done

sed -i '/^$/d' all_bom.csv
#get the first line and remove all identical lines
head -n 1 all_bom.csv > all_bom.csv.tmp
#remove all lines that contains "Reference"
sed -i '/Reference/d' all_bom.csv
#add the first line to the file
cat all_bom.csv >> all_bom.csv.tmp
mv all_bom.csv.tmp all_bom.csv
rm -f all_bom.csv.tmp 

# #remove all lines from all_bom.csv that contain two " in a row at the end of the line
# sed -i '/""$/d' all_bom.csv
