# get all the .kicad_pro files in the current directory and its subdirectories to find each project folder
# then remove the name.kicad_pro and print each project folder path
l=`find -name "*.kicad_pro"`
# remove duplicates
l=`echo "$l" | sort -u`
# remove path with .kiri
l=`echo "$l" | grep -v '\.kiri/'`
l=`echo "$l" | grep -v 'PANEL'`
for li in $l; do
    echo "$li"
    kicad-cli jobset run --file jobs.kicad_jobset --output LDRendering "$li"
done
# kicad-cli jobset run --file jobs.kicad_jobset --output LDRendering "$li"