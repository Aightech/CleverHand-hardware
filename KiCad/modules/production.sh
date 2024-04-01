#bash file to generate production files for all folders
source ~/.bashrc
#use the kicad-plot function from the .bashrc file
export -f kicad-plot

#for each folder in the current directory
for d in */ ; do
    #remove the last character of the folder name
    folder=${d%?}
    echo -e "Generating production files for \e[1m$folder\e[0m"
    cd $folder
    #kicad-plot $folder
    #meshlabserver -i plots/${folder}_pcb.wrl -o plots/${folder}.stl
    mv plots/${folder}.stl plots/${folder}_pcb.stl
    # cp plots/${folder}_pcb.wrl ../../../3d_model/modules/$folder.wrl
    # cp config.json ../../../3d_model/modules/$folder.json
    cd ..
    echo ""
    
done

