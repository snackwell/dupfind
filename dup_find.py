# coding=utf-8

import os
import itertools
import re
import sys
from threading import Thread
from datetime import datetime
import subprocess
import cPickle
import argparse
import hashlib
import collections
import win32file

reload(sys)
sys.setdefaultencoding('utf-8')

size_dict = collections.defaultdict(list)
sizehash_dict = collections.defaultdict(list)

def all_equal(elements):
    first_element = elements[0]
    for other_element in elements[1:]:
        if other_element != first_element : return False
    return True

def common_prefix(*sequences):
    if not sequences: return[],[]
    common = []
    for elements in itertools.izip(*sequences):
        if not all_equal(elements):break
        common.append(elements[0])
    print common
    print [sequence[len(common):] for sequence in sequences]
    return common,[sequence[len(common):] for sequence in sequences]

def relpath(p1,p2, sep=os.path.sep, pardir=os.path.pardir):
    # common,(u1,u2) = common_prefix(p1.split(sep),p2.split(sep))
    common,(u1,u2) = common_prefix(os.path.dirname(p1).split(sep),os.path.dirname(p2).split(sep))
    if not common:
        return p2
    return sep.join([os.path.curdir]+[pardir] * len(u1) + u2)

def md5(fname,size=8192):
    hash_md5 = hashlib.md5()
    i = 0
    with open(fname, 'rb') as f:
        # for chunk in iter(lambda: f.read(size), "b"):
        while 1:
            chunk = f.read(size)
            if not chunk : break
            hash_md5.update(chunk)
            i += 1
            if (i % 10000)==0:
                print i," trunks read...\n"
    return hash_md5.hexdigest()


def all_duplicate(file_dict, path=""):
    file_txt = open("duplicate.txt", "w")
    total_dup_size = 0
    duplicate_count = 0



    #all_file_list = [v for k,v in file_dict.items()]
    #for each in all_file_list:
    for (size, hash), filelist in file_dict.items():
        #print filelist
        if (len(filelist)>=2) :
            filelist.sort(lambda x,y: cmp(len(x), len(y)))
            if size > 1000000: # only compare for file size > 10MB
                file_txt.write("-------------------Duplicated for size, hash pair (")
                file_txt.write(str(size))
                file_txt.write(",")
                file_txt.write(str(hash))
                file_txt.write(")-------------------\n")
                total_dup_size += size * len(filelist) - size
                duplicate_count += len(filelist) - 1
                for afile in filelist:
                    print afile
                    str1 = afile + "\n"
                    file_txt.write(str1)
                    if cmp(afile, filelist[0]):
                        file_txt.write(relpath(afile,filelist[0])+os.path.sep+os.path.basename(filelist[0]))
                        file_txt.write("\n")
                        try:
                            os.remove(afile)
                        except Exception as e :
                            file_txt.write("Error ")
                            file_txt.write(e.message)
                            file_txt.write(" with remove file: " + afile)
                            file_txt.write("\n")
                        try:
                            win32file.CreateSymbolicLink(afile, relpath(afile,filelist[0])+os.path.sep+os.path.basename(filelist[0]))
                        except Exception as e:
                            file_txt.write("Error ")
                            file_txt.write(e.message)
                            file_txt.write(" with create symbolic link for: " + afile)
                            file_txt.write("\n")
                print "Now total_dup_size is: ", total_dup_size
    file_txt.write("----------------Total Duplicate ")
    file_txt.write(str(duplicate_count))
    file_txt.write(" files, Size is: ")
    file_txt.write(str(total_dup_size))
    file_txt.write("----------------\n")
    file_txt.close()


def get_paths():
    response = os.popen("wmic logicaldisk get caption")
    pathList = []
    #total_file = []
    #t1= datetime.now()
    for line in response.readlines():
        line = line.strip("\n")
        line = line.strip("\r")
        line = line.strip(" ")
        if (line == "Caption" or line == ""):
            continue
        pathList.append(line)
    #return driverList
    pathList = []
    #pathList.append(unicode("D:\\zyang", "utf-8"))
    #pathList.append(unicode("D:\\Qiaohu\\初中课程\\初中化学", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\小学课程\\其他课程", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\初中课程\\初中化学", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\小学课程\\小学英语", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\小学课程\\小学语文", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\小学课程\\小学数学", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\初中课程\\初中数学\\初中数学A", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\初中课程\\初中英语", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\初中课程\\初中语文", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\初中课程\\初中数学\\初中数学B", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\初中课程\\初中物理", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\初中课程\\初中科学", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\高中课程\\高中化学", "utf-8"))
    #pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\高中课程\\高中数学", "utf-8"))
    pathList.append(unicode("H:\\中文-【动画、语文、数学、识字】\\26.学而思全套（小学初中高中）\\高中课程\\高中物理", "utf-8"))
    return pathList

def search1(drive,size, hash_dict):
    clean_list=[]
    print "length of hash_dict is: ", len(hash_dict)
    print "length of sizehash_dict is:", len(sizehash_dict)
    for (fsize, fhash), filelist in hash_dict.items():
        for file_name in filelist:
            if not os.access(file_name, os.F_OK):
                clean_list.append((fsize,fhash, file_name))
                #assert isinstance(file_name, object)
                #file_dict[(size,hash)].remove(file_name)
    for csize, chash, cfile in clean_list:
        print "Need to clean ", csize, chash, cfile
        hash_dict[(csize, chash)].remove(cfile)

    for path, folders, files in os.walk(drive, topdown = True):
        #print "Tuple of os.walk for : ", path
        try:
            for afile in files:
                try:
                    if os.access(path, os.X_OK):                       #orig = file
                        afile = path+"\\"+afile
                        if os.access(afile, os.F_OK):
                            if os.access(afile, os.R_OK):
                                fsize=os.stat(afile).st_size
                                if fsize > 100000 :
                                    #fhash=md5(afile)
                                    print "(", fsize,"): file: ", afile
                                    size_dict[fsize].append(afile)
                except Exception as e : pass
        except Exception as e : pass

    for size, filelist in size_dict.items():
        if (len(filelist) >= 2):  # only calc hash for file with possible conflict
            for afile in filelist:
                if [(fsize, fhash, afile) for (fsize,fhash), sfilelist in hash_dict.items() if afile in sfilelist and fsize==size ]:
                    print "already existing for ", afile, " with size: ", fsize, " and hash: ", fhash
                else:
                    fhash = md5(afile)
                    print "Need to add new (", size, ",", fhash,"): file: ", afile
                    sizehash_dict[(size, fhash)].append(afile)

def create(size, hash_dict):
    t1= datetime.now()
    list2 = []   # empty list is created
    list1 = get_paths()
    print "Paths are \n"
    for d in list1:
        print d, " ",
    print "\nCreating Index..."

    for each in list1:
        process1 = Thread(target=search1, args=(each,size, hash_dict))
        process1.start()
        list2.append(process1)

    for t in list2:
        t.join() # Terminate the threads
    global size_dict
    print len(size_dict)
    pickle_file = open("size_dict.dup1","w")
    cPickle.dump(size_dict,pickle_file)
    pickle_file.close()

    print len(sizehash_dict)
    pickle_file = open ("sizehash_dict.dup1","w")
    cPickle.dump(sizehash_dict,pickle_file)
    pickle_file.close()
    t2= datetime.now()
    total =t2-t1
    print "Time taken to create sizedict", total


def file_open():
    try:
        pickle_file  = open("sizehash_dict.dup1", "r")
        file_dict = cPickle.load(pickle_file)
        if len(file_dict) == 0 :
            file_dict = collections.defaultdict(list)
        pickle_file.close()

    except Exception as e:
        file_dict=collections.defaultdict(list)
    return file_dict

def file_search(file_name):
    t1= datetime.now()
    try:
        file_dict  = file_open()
    except IOError:
        create()
        file_dict  = file_open()
    except Exception as e :
        print e
        sys.exit()
    file_name1 = file_name.rsplit("\\",1)
    os.chdir(file_name1[0])

    file_to_be_searched = file_name1[1]
    if  os.access(file_name, os.F_OK):
        if os.access(file_name, os.R_OK):
            sign = md5(file_to_be_searched)
            files=  file_dict.get(sign, None)
            if files:
                print "File(s) are "
                files.sort()
                for index, item in enumerate(files):
                    print index+1," ", item
                    print "---------------------"
    else :
        print "File is not present or accessible"
    t2= datetime.now()
    total =t2-t1
    print "Time taken to search ", total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", nargs='?', help="Give file with path in double quotes")
    parser.add_argument('-c', nargs='?', help="For creating MD5 hash of all files", const=4096, type=int)
    parser.add_argument('-a', help="To get all duplicate files in duplicate.txt in running current folder", action='store_true')
    parser.add_argument('-f', help="To find the MD5 hash,provide file with path in double quotes ", nargs=1,)
    global sizehash_dict
    print len(sizehash_dict)
    args = parser.parse_args()
    try:
        if args.c:
            print args.c
            sizehash_dict = file_open()
            create(args.c, sizehash_dict)
        elif args.a:
            file_dict = file_open()
            all_duplicate(file_dict)

        elif args.f:
            if os.access(args.f[0], os.R_OK):
                print "Md5 Signature are : ", md5(args.f[0],4096)
                print "\n"
            else :
                print "Check the file path and file name\n"
        else:
            file_search(args.file_name)

        #print "Thanks for using L4wisdom.com"
        #print "Email id mohitraj.cs@gmail.com"
        #print "URL: http://l4wisdom.com/finder_go.php"

    except Exception as e:
        print e
        print "Please use proper format to search a file use following instructions"
        print "dupl file-name"
        print "Use <dupl -h >  For help"


if __name__ == '__main__':
    main()

