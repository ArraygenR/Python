import re
import more_itertools as mit
import os
def continuous_insertion_deletion_indel1(file_op, line1_seq, line3_seq,line1_start,line3_start, empty_index, protein_seq):
    for empty_index_iter1 in empty_index:
        if len(empty_index_iter1) > 1:
            sub_line1 = line1_seq[empty_index_iter1[0]:empty_index_iter1[len(empty_index_iter1) - 1] + 1]
            sub_line3 = line3_seq[empty_index_iter1[0]:empty_index_iter1[len(empty_index_iter1) - 1] + 1]

            status = ""
            if "-" in sub_line3 or "-" in sub_line1:
                o1 = sub_line3 + " --> " + sub_line1
                o2 = str(line3_start + empty_index_iter1[0]) + " <--> " + str(line1_start + empty_index_iter1[0])
                o4 = ""
                status = ""
                if "-" * len(empty_index_iter1) == sub_line3:
                    #print(empty_index_iter1[0], empty_index_iter1[len(empty_index_iter1) - 1] + 1)
                    if protein_seq != None:
                        o4 = str(line3_start + empty_index_iter1[0]) + "," + protein_seq[line3_start + empty_index_iter1[
                        0]:line3_start + empty_index_iter1[len(empty_index_iter1) - 1] + 1] + "," + sub_line1
                    else:
                        o4 = str(line3_start + empty_index_iter1[0]) + "," + sub_line3+ "," + sub_line1
                    status = "insertion"
                    o3 = status
                    if protein_seq == None:
                        file_op.append([o1, o2, o3])
                    else:
                        file_op.append([o1, o2, o3, o4])

                elif "-" * len(empty_index_iter1) == sub_line1:
                    o4 = str(line3_start + empty_index_iter1[0]) + "," + sub_line3 + ",."
                    status = "deletion"
                    o3 = status
                    if protein_seq == None:
                        file_op.append([o1, o2, o3])
                    else:
                        file_op.append([o1, o2,  o3, o4])
                else:
                    #print("Combination of snp/indel and (insertion/deletion or both)")
                    if "-" in sub_line1:

                        dash_index = [m.start() for m in re.finditer('-', sub_line1)]
                        remaining_index = list(set(range(len(sub_line1))) - set(dash_index))
                        remaining_index = [list(group) for group in mit.consecutive_groups(remaining_index)]
                        remaining_index.append(dash_index)
                        file_op = continuous_insertion_deletion_indel1(
                            file_op, sub_line1, sub_line3, line1_start+empty_index_iter1[0], line3_start+empty_index_iter1[0],remaining_index, protein_seq)
                        #print(dash_index)

                    elif "-" in sub_line3:
                        #print(sub_line1, sub_line3)
                        dash_index = [m.start() for m in re.finditer('-', sub_line3)]
                        remaining_index = list(set(range(len(sub_line3))) - set(dash_index))
                        remaining_index = [list(group) for group in mit.consecutive_groups(remaining_index)]
                        remaining_index.append(dash_index)
                        file_op = continuous_insertion_deletion_indel1(
                            file_op, sub_line1, sub_line3,line1_start+empty_index_iter1[0], line3_start+empty_index_iter1[0],remaining_index, protein_seq)
                        #print(remaining_index)

                        #print(dash_index)


            else:
                for empty_index_iter2 in empty_index_iter1:
                    #print(empty_index_iter2)
                    file_op = continuous_insertion_deletion_indel1(
                        file_op, line1_seq, line3_seq, line1_start,line3_start, [[empty_index_iter2],], protein_seq)
                """

                o1 = sub_line3 + " --> " + sub_line1
                o2 = str(line3_start + empty_index_iter1[0]) + " --> " + str(line1_start + empty_index_iter1[0])
                o4 = str(line3_start + empty_index_iter1[0]) + "," + ",".join(o1.split(" --> "))
                status = "indel"
                o3 = status
                if protein_seq == None:
                    file_op.append([o1, o2, o3])
                else:
                    file_op.append([o1, o2, o3, o4])
                    """
        else:
            empty_index_iter = empty_index_iter1[0]
            o1 = line3_seq[empty_index_iter] + " <--> " + line1_seq[empty_index_iter]
            o2 = str(line3_start + empty_index_iter) + " <--> " + str(line1_start + empty_index_iter)
            o4 = str(line3_start + empty_index_iter) + "," + line3_seq[empty_index_iter] + "," + line1_seq[
                empty_index_iter]
            status = ""
            if "-" in line3_seq[empty_index_iter]:
                status = "insertion"
            elif "-" in line1_seq[empty_index_iter]:
                status = "deletion"
            else:
                status= "SNP"
            o3 = status

            if protein_seq == None:
                file_op.append([o1, o2, o3])
            else:
                file_op.append([o1, o2, o3, o4])
    return  file_op

def step1_make_input_for_provean(gene_blast, protein_blast=None, protein= None):
    if protein != None:
        #protein = "ampd.protein.fa"
        f_seq = open(protein, "r")
        data = f_seq.readlines()
        protein_seq = "".join(data[1:]).strip()

    #gene_blast = "AMPD.gene.Blast.Results1.txt"
    f = open(gene_blast, "r")
    dictionary = {}
    data = f.read()
    splitted_data = data.split("Query=")
    splitted_data.pop(0)
    for splitted_data_1 in splitted_data:
        dictionary[splitted_data_1[:splitted_data_1.find("\n\n")].strip()] = [splitted_data_1[splitted_data_1.find("\n\n"):].strip() , ]


    if protein_blast != None:
        #protein_blast = "AMPD.protein.Blast.Results1.txt"
        f = open(protein_blast, "r")
        data = f.read()
        splitted_data = data.split("Query=")
        splitted_data.pop(0)
        for splitted_data_1 in splitted_data:
            if splitted_data_1[:splitted_data_1.find("\n\n")].strip() in dictionary.keys():
                list1 = dictionary[splitted_data_1[:splitted_data_1.find("\n\n")].strip()]
                list1.append(splitted_data_1[splitted_data_1.find("\n\n"):].strip())
                dictionary[splitted_data_1[:splitted_data_1.find("\n\n")].strip()] = list1


    if protein_blast != None:
        OP_file_name = gene_blast.split("/")
        OP_file_name.pop()
        OP_file_name.append("output.txt")
        OP_file_name = "/".join(OP_file_name)
        #fw = open(os.getcwd() + "/static/files/input_files/output.txt", "w")
        fw = open(OP_file_name, "w")
        print("Query\tLength\tGene\tLength\tScore\tExcept\tIdentities\tGaps\tVariation\tPosition\tMutation Type\tProtein\tLength\tScore\tExcept\tIdentities\tGaps\tVariation\tPosition\tMutation Type\tPROVEAN Input Variants\tPROVEAN_Score\tPrediction (cutoff = -2.5)", file=fw)
    else:
        OP_file_name = gene_blast.split("/")
        f_name = "OP_"+OP_file_name.pop()
        OP_file_name.append(f_name)
        OP_file_name = "/".join(OP_file_name)
        fw = open(OP_file_name, "w")
        print("Query\tLength\tGene\tLength\tScore\tExcept\tIdentities\tGaps\tVariation\tPosition\tMutation Type", file=fw)

    if protein_blast != None:
        for k, v in dictionary.items():
            if len(v) >1:
                file1_op = []
                # for 1st file
                s1 = v[0]
                len_of_k1 = s1[s1.find("Length="):s1.find("\n")].replace("Length=","")
                s1_data = s1.split(">")[1]
                header_name1 = s1_data[:s1_data.find("\n")].strip()
                header_name1 = header_name1[:header_name1.find(":")].strip()
                s1_data = s1_data[s1_data.find("\n"):].strip()
                len_of_header1 = s1_data[s1_data.find("Length="):s1_data.find("\n",s1_data.find("Length="))].replace("Length=", "")
                s1_data = s1_data[s1_data.find("\n",s1_data.find("Length=")):].strip()
                score1= s1_data[s1_data.find("Score ="):s1_data.find(",",s1_data.find("Score ="))].replace("Score =", "").strip()
                expect1 = s1_data[s1_data.find("Expect ="):s1_data.find("\n", s1_data.find("Expect ="))].replace("Expect =", "").strip()
                identities1 = s1_data[s1_data.find("Identities ="):s1_data.find(",", s1_data.find("Identities ="))].replace("Identities =", "").strip()
                gaps1 = s1_data[s1_data.find("Gaps ="):s1_data.find("\n", s1_data.find("Gaps ="))].replace("Gaps =",  "").strip()
                align_seq1= s1_data[s1_data.find("\n\nQuery"):s1_data.find("\n\n\n")].strip()
                splitted_align_seq1 = align_seq1.split("\n\n")
                #print(len(splitted_align_seq1))
                for s_align_seq1 in splitted_align_seq1:
                    lines = s_align_seq1.split("\n")
                    line1 = lines[0]
                    empty_index_line1 = [m.start() for m in re.finditer('  ', line1)]
                    line1_start = int(line1[empty_index_line1[0]:empty_index_line1[1]].strip())
                    line1_end = int(line1[empty_index_line1[len(empty_index_line1) - 1]:].strip())
                    line1_seq = line1[line1.find(str(line1_start)) + len(str(line1_start)):line1.find(str(line1_end))].strip()
                    # print(line1_start,line1_end)
                    # print(line1_seq)

                    if len(line1) > 30:
                        start_line1_seq = line1.find(line1_seq[:5])
                        end_line1_seq = line1.find(line1_seq[len(line1_seq) - 25:]) + 25
                        # print(start_line1_seq, end_line1_seq)
                        line2 = lines[1][start_line1_seq:end_line1_seq]
                    else:
                        line2 = lines[1].strip()
                    empty_index = [m.start() for m in re.finditer(' ', line2)]
                    # print(empty_index)
                    empty_index = [list(group) for group in mit.consecutive_groups(empty_index)]
                    # print(empty_index)

                    # print(line2)
                    line3 = lines[2]
                    empty_index_line3 = [m.start() for m in re.finditer('  ', line3)]
                    line3_start = int(line3[empty_index_line3[0]:empty_index_line3[1]].strip())
                    line3_end = int(line3[empty_index_line3[len(empty_index_line3) - 1]:].strip())
                    line3_seq = line3[line3.find(str(line3_start)) + len(str(line3_start)):line3.find(str(line3_end))].strip()
                    # print(line3_start, line3_end)
                    # print(line3_seq)
                    file1_op = continuous_insertion_deletion_indel1(
                        file1_op,line1_seq, line3_seq, line1_start, line3_start, empty_index, None)


                file2_op = []
                # for 2nd file
                s2 = v[1]
                len_of_k2 = s2[s2.find("Length="):s2.find("\n")].replace("Length=","")
                s2_data = s2.split(">")[1]
                header_name2 = s2_data[:s2_data.find("\n")].strip()
                s2_data = s2_data[s2_data.find("\n"):].strip()
                len_of_header2 = s2_data[s2_data.find("Length="):s2_data.find("\n", s2_data.find("Length="))].replace("Length=","")
                s2_data = s2_data[s2_data.find("\n", s2_data.find("Length=")):].strip()
                score2 = s2_data[s2_data.find("Score ="):s2_data.find(",", s2_data.find("Score ="))].replace("Score =", "").strip()
                expect2 = s2_data[s2_data.find("Expect ="):s2_data.find(",", s2_data.find("Expect ="))].replace("Expect =", "").strip()
                identities2 = s2_data[s2_data.find("Identities ="):s2_data.find(",", s2_data.find("Identities ="))].replace("Identities =", "").strip()
                gaps2 = s2_data[s2_data.find("Gaps ="):s2_data.find("\n", s2_data.find("Gaps ="))].replace("Gaps =", "").strip()
                align_seq2 = s2_data[s2_data.find("\n\nQuery"):s2_data.find("\n\n\n")].strip()
                splitted_align_seq2 = align_seq2.split("\n\n")

                for s_align_seq2 in splitted_align_seq2:
                    lines = s_align_seq2.split("\n")
                    line1 = lines[0]
                    empty_index_line1 = [m.start() for m in re.finditer('  ', line1)]
                    line1_start= int(line1[empty_index_line1[0]:empty_index_line1[1]].strip())
                    line1_end = int(line1[empty_index_line1[len(empty_index_line1)-1]:].strip())
                    line1_seq = line1[line1.find(str(line1_start))+len(str(line1_start)):line1.find(str(line1_end))].strip()
                    #print(line1_start,line1_end)
                    #print(line1_seq)

                    if len(line1) > 30:
                        start_line1_seq = line1.find(line1_seq[:5])
                        end_line1_seq = line1.find(line1_seq[len(line1_seq) - 25:]) + 25
                        # print(start_line1_seq, end_line1_seq)
                        line2 = lines[1][start_line1_seq:end_line1_seq]
                    else:
                        line2 = lines[1].strip()
                    empty_index = [m.start() for m in re.finditer(' ', line2)]
                    #print(empty_index)
                    empty_index = [list(group) for group in mit.consecutive_groups(empty_index)]
                    #print(empty_index)
                    #print(line2)

                    line3 = lines[2]
                    empty_index_line3 = [m.start() for m in re.finditer('  ', line3)]
                    line3_start = int(line3[empty_index_line3[0]:empty_index_line3[1]].strip())
                    line3_end = int(line3[empty_index_line3[len(empty_index_line3) - 1]:].strip())
                    line3_seq = line3[line3.find(str(line3_start)) + len(str(line3_start)):line3.find(str(line3_end))].strip()
                    #print(line3_start, line3_end)
                    #print(line3_seq)

                    file2_op = continuous_insertion_deletion_indel1(
                        file2_op,line1_seq, line3_seq, line1_start, line3_start, empty_index, protein_seq)



                if len(file1_op) > len(file2_op) :
                    max_len = len(file1_op)
                else:
                    max_len = len(file2_op)

                for i in range(max_len):
                    if i == 0:
                        if i < len(file1_op) and i < len(file2_op) :
                            print(k.strip()+"\t"+len_of_k1+"\t"
                              +header_name1+"\t"+len_of_header1+"\t"+score1+"\t"+expect1+"\t"+identities1+"\t"+gaps1+"\t"+
                              "\t".join(file1_op[i])+"\t"
                              +header_name2+"\t"+len_of_header2+"\t"+score2+"\t"+expect2+"\t"+identities2+"\t"+gaps2+"\t"+
                                  "\t".join(file2_op[i]) , file = fw)

                        elif i < len(file1_op):
                            print(k.strip() + "\t" + len_of_k1 + "\t"
                                  + header_name1 + "\t" + len_of_header1 + "\t" + score1 + "\t" + expect1 + "\t" + identities1 + "\t" + gaps1 + "\t" +
                                  "\t".join(file1_op[i]) + "\t"
                                  + header_name2 + "\t" + len_of_header2 + "\t" + score2 + "\t" + expect2 + "\t" + identities2 + "\t" + gaps2
                                  , file = fw)

                        elif i < len(file2_op):
                            print(k.strip() + "\t" + len_of_k1 + "\t"
                                  + header_name1 + "\t" + len_of_header1 + "\t" + score1 + "\t" + expect1 + "\t" + identities1 + "\t" + gaps1 + "\t" +
                                  "\t"*2 + "\t"
                                  + header_name2 + "\t" + len_of_header2 + "\t" + score2 + "\t" + expect2 + "\t" + identities2 + "\t" + gaps2+"\t"+
                                  "\t".join(file2_op[i]) , file = fw)

                    else:
                        if i < len(file1_op) and i < len(file2_op):
                            print("\t"*8 +"\t".join(file1_op[i])+"\t"*7 +"\t".join(file2_op[i]), file = fw)
                        elif i < len(file1_op):
                            print("\t" * 8 + "\t".join(file1_op[i]), file = fw)
                        elif i < len(file2_op):
                            print("\t" * 17 + "\t".join(file2_op[i]), file = fw)
                print(file = fw)

            else:
                print("Unmatch :",k)

                #pass
    else:
        for k, v in dictionary.items():
            #print(k)
            file1_op = []
            # for 1st file
            s1 = v[0]
            len_of_k1 = s1[s1.find("Length="):s1.find("\n")].replace("Length=", "")
            s1_data = s1.split(">")[1]
            header_name1 = s1_data[:s1_data.find("\n")].strip()
            header_name1 = header_name1[:header_name1.find(":")].strip()
            s1_data = s1_data[s1_data.find("\n"):].strip()
            len_of_header1 = s1_data[s1_data.find("Length="):s1_data.find("\n", s1_data.find("Length="))].replace(
                "Length=", "")
            s1_data = s1_data[s1_data.find("\n", s1_data.find("Length=")):].strip()
            score1 = s1_data[s1_data.find("Score ="):s1_data.find(",", s1_data.find("Score ="))].replace("Score =",
                                                                                                         "").strip()
            expect1 = s1_data[s1_data.find("Expect ="):s1_data.find("\n", s1_data.find("Expect ="))].replace("Expect =",
                                                                                                             "").strip()
            identities1 = s1_data[s1_data.find("Identities ="):s1_data.find(",", s1_data.find("Identities ="))].replace(
                "Identities =", "").strip()
            gaps1 = s1_data[s1_data.find("Gaps ="):s1_data.find("\n", s1_data.find("Gaps ="))].replace("Gaps =",
                                                                                                       "").strip()
            align_seq1 = s1_data[s1_data.find("\n\nQuery"):s1_data.find("\n\n\n")].strip()
            splitted_align_seq1 = align_seq1.split("\n\n")
            # print(len(splitted_align_seq1))
            for s_align_seq1 in splitted_align_seq1:
                lines = s_align_seq1.split("\n")
                line1 = lines[0]
                empty_index_line1 = [m.start() for m in re.finditer('  ', line1)]
                line1_start = int(line1[empty_index_line1[0]:empty_index_line1[1]].strip())
                line1_end = int(line1[empty_index_line1[len(empty_index_line1) - 1]:].strip())
                line1_seq = line1[
                            line1.find(str(line1_start)) + len(str(line1_start)):line1.find(str(line1_end))].strip()
                # print(line1_start,line1_end)
                # print(line1_seq)

                if len(line1) > 30:
                    start_line1_seq = line1.find(line1_seq[:5])
                    end_line1_seq = line1.find(line1_seq[len(line1_seq) - 25:]) + 25
                    # print(start_line1_seq, end_line1_seq)
                    line2 = lines[1][start_line1_seq:end_line1_seq]
                else:
                    line2 = lines[1].strip()
                empty_index = [m.start() for m in re.finditer(' ', line2)]
                # print(empty_index)
                empty_index = [list(group) for group in mit.consecutive_groups(empty_index)]
                #print(empty_index)

                # print(line2)
                line3 = lines[2]
                empty_index_line3 = [m.start() for m in re.finditer('  ', line3)]
                line3_start = int(line3[empty_index_line3[0]:empty_index_line3[1]].strip())
                line3_end = int(line3[empty_index_line3[len(empty_index_line3) - 1]:].strip())
                line3_seq = line3[
                            line3.find(str(line3_start)) + len(str(line3_start)):line3.find(str(line3_end))].strip()
                # print(line3_start, line3_end)
                # print(line3_seq)
                file1_op = continuous_insertion_deletion_indel1(
                    file1_op, line1_seq, line3_seq, line1_start, line3_start, empty_index, None)

            for i in range(len(file1_op)):
                if i == 0:
                    print(k.strip() + "\t" + len_of_k1 + "\t"
                              + header_name1 + "\t" + len_of_header1 + "\t" + score1 + "\t" + expect1 + "\t" + identities1 + "\t" + gaps1 + "\t" +
                              "\t".join(file1_op[i]) , file=fw)
                else:
                    print("\t" * 8 + "\t".join(file1_op[i]), file=fw)
    fw.close()

