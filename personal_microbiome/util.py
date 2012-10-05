import os
from sys import argv
from qiime.parse import parse_mapping_file_to_dict
from qiime.util import qiime_system_call
from os import makedirs
from os.path import join
from qiime.parse import parse_mapping_file
from qiime.format import format_mapping_file

def create_PersonalID_list(mapping_data):
    result = []
    for i in mapping_data:
        if i[8] not in result: 
            result.append(i[8]) 
        else: 
            pass
    return result
    
def create_personal_mapping_file(map_as_list, header, comments, personal_id_of_interest, output_fp):
    """ creates mapping file on a per-individual basis """
    map_as_list = tuple(map_as_list)
    personal_map = []
    for line in map_as_list:
        personal_map.append(line[:])
    for i in personal_map:   
        if i[8] == personal_id_of_interest: 
            i.insert(9, 'yes')
        else: 
            i.insert(9, 'no')
    print len(map_as_list[0])
    print len(personal_map[0])
    personal_mapping_file = format_mapping_file(header, personal_map, comments) 
    output_f = open(output_fp,'w')
    output_f.write(personal_mapping_file)
    output_f.close()
    
#create color scheme for the individual. The individual of interest will be based on 
#the special_colors. Everyone else will be colored by the 'standard_colors' 
# kinemage_colors = ['hotpink','blue', 'lime','gold','red','sea','purple','green']
# def get_current_color(special_coloring,field_value):
# #define the colors for each body habitat. They are different for individual vs. other
#     standard_colors = {'armpit':'green',
#                        'palm':'green',
#                        'tongue':'blue',
#                        'gut':'gold',
#                        'forehead':'green'}
#     special_colors = {'armpit':'hotpink',
#                       'palm':'hotpink',
#                       'tongue':'red',
#                       'gut':'purple',
#                       'forehead':'hotpink'}
# #determine which color scheme will be used.
#     if special_coloring == True:
#         try:
#             return special_colors[field_value]
#         except KeyError:
# #this exception is for an individual that may not have data for a given habitat.
#             return 'grey'
#     else:
#         try:
#             return standard_colors[field_value]
#         except KeyError:
#             return 'grey'

#This function takes a mapping file, an output path for the prefs file, the
#the personal_id_field and the other_field. it defaults to BodyHabitat, meaning the prefs
#file created will contain coloring based on based on the individual and their body
#habitat
# def personal_prefs_from_map(mapping_data, 
#                             output_fp,
#                             person_of_interest,
#                             personal_id_field='PersonalID', 
#                             other_field='BodyHabitat'):
# #make empty list to put all of the output. 
#     output_lines = []
#     output_field_id = "%s&&%s" % (personal_id_field, other_field)
#     output_lines.append("{'background_color':'black','sample_coloring':{")
#     output_lines.append("'%s':" % output_field_id)
#     output_lines.append('{')
#     output_lines.append("'column':'%s'," % output_field_id)
#     output_lines.append("'colors':{")
# #.items creates a list of the dictionary. Note mapping data is a two dimensional list
# # therefore this becomes a list of dictionarys. and allows for it to be looped through. 
# #sample_id was the key in the original dictionary,. d is that keys values which is a 
# #dictionary of  personalids
#     for sample_id, d in mapping_data.items():
#         if d[personal_id_field] == person_of_interest:
# #here the person_of_interest will determine the color scheme that was defined in 
# #get_current_color
#             current_entry_is_person_of_interest = True
#         else:
#             current_entry_is_person_of_interest = False
#         color = get_current_color(current_entry_is_person_of_interest,d[other_field])
# #create an entry for each individual and other_field.   
#         output_lines.append("'%s%s':'%s'," % (d[personal_id_field],d[other_field],color))
#     output_lines.append('}}}}')
#     output_f = open(output_fp,'w')
#     output_f.write('\n'.join(output_lines))
#     output_f.close()

def create_indiv_3d_plot(mapping_fp, distance_matrix_fp, output_fp, prefs_fp):
    map_as_list, header, comments = parse_mapping_file(open(mapping_fp, 'U'))
    PersonalID_list  = create_PersonalID_list(map_as_list)
    header.insert(9, 'Self')  
    output_directories = []
    makedirs(output_fp)
    for person_of_interest in PersonalID_list:
        makedirs(join(output_fp, person_of_interest))
        personal_output_dir = join(output_fp, person_of_interest, "%s_pcoa_plots" % person_of_interest)
        output_directories.append(personal_output_dir)
        personal_mapping_file_fp = join(output_fp, person_of_interest, "%s_mapping_file.txt" % person_of_interest)
        create_personal_mapping_file(map_as_list,
                                     header,
                                     comments,
                                     person_of_interest,
                                     personal_mapping_file_fp)
        cmd = "make_3d_plots.py -m %s -p %s -i %s -o %s" % (personal_mapping_file_fp, 
                                                            prefs_fp, 
                                                            distance_matrix_fp, 
                                                            personal_output_dir)
        stdout, stderr, return_code = qiime_system_call(cmd)
        if return_code != 0:
            print "Command failed!\nCommand: %s\n Stdout: %s\n Stderr: %s\n" %\
             (cmd, stdout, stderr)
    return output_directories
    
def create_indiv_rarefaction_plot(mapping_fp, collated_dir_fp, output_fp, prefs_fp):
    map_as_list, header, comments = parse_mapping_file(open(mapping_fp, 'U'))
    PersonalID_list = create_PersonalID_list(map_as_list)
    header.insert(9, 'Self')
    output_directories = []
    makedirs(output_fp)
    for person_of_interest in PersonalID_list:
        makedirs(join(output_fp, person_of_interest))
        personal_output_dir = join(output_fp, person_of_interest, "%s_rarefaction" % person_of_interest)
        output_directories.append(personal_output_dir)
        personal_mapping_file_fp = join(output_fp, person_of_interest, "%s_mapping_file.txt" % person_of_interest)
        create_personal_mapping_file(map_as_list,
                                     header,
                                     comments,
                                     person_of_interest,
                                     personal_mapping_file_fp)
        cmd = "make_rarefaction_plots.py -i %s -m %s -p %s -o %s -s" % (collated_dir_fp, 
                                                                        personal_mapping_file_fp,
                                                                        prefs_fp, 
                                                                        personal_output_dir)
        stdout, stderr, return_code = qiime_system_call(cmd)
        if return_code != 0:
            print "Command failed!\nCommand: %s\n Stdout: %s\n Stderr: %s\n" %\
             (cmd, stdout, stderr)
    return output_directories