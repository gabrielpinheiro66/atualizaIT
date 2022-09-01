import os
import sys
from time import strftime, localtime
from functions import copy_export, __delete_file


def __compare_path(src, src_entries, dst_entries, lock):
    add = []
    remove = []
    pdf_src_entries = []
    for src_entry in src_entries:
        if lock and (src_entry.endswith('.odt') or src_entry.endswith('.doc') or src_entry.endswith('.docx')):
            pdf_src_entry = src_entry[:src_entry.rindex('.')]
            pdf_src_entry = pdf_src_entry + '.pdf'
        else:
            pdf_src_entry = src_entry
        pdf_src_entries.append(pdf_src_entry)
        if not (pdf_src_entry in dst_entries):
            if not (os.path.isdir(os.path.join(src, src_entry))):
                add.append(src_entry)
    # end for
    for dst_entry in dst_entries:
        if not (dst_entry in pdf_src_entries):
            remove.append(dst_entry)
    # end for
    return add, remove


def __remove_files(dst, remove):
    for filename in remove:
        file_dst = os.path.join(dst, filename)
        __delete_file(file_dst)


def __add_files(src, dst, add, lock):
    for filename in add:
        file_src = os.path.join(src, filename)
        file_dst = os.path.join(dst, filename)
        copy_export(file_src, file_dst, lock)


def __compare_files(src_entries, dst_entries, src, dst, lock):
    pdf_src_entries = []
    for src_entry in src_entries:
        if lock and (src_entry.endswith('.odt') or src_entry.endswith('.doc') or src_entry.endswith('.docx')):
            pdf_src_entry = src_entry[:src_entry.rindex('.')]
            pdf_src_entry = pdf_src_entry + '.pdf'
        else:
            pdf_src_entry = src_entry
        pdf_src_entries.append(pdf_src_entry)
    # end for
    for i, pdf_src_entry in enumerate(pdf_src_entries):
        if pdf_src_entry in dst_entries:
            index_dst = dst_entries.index(pdf_src_entry)
            dst_entry = dst_entries[index_dst]
            src_entry = src_entries[i]
            __compare(src, dst, src_entry, dst_entry, lock)


def __compare(src, dst, src_entry, dst_entry, lock):
    file_src = os.path.join(src, src_entry)
    file_dst = os.path.join(dst, dst_entry)
    if os.path.isdir(file_src) or os.path.isdir(file_dst):
        return
    if last_modify(file_dst) < last_modify(file_src):
        __att_file(file_src, file_dst, lock)


def last_modify(file):
    mtime = strftime('%Y-%m-%d %H:%M:%S', localtime(os.path.getmtime(file)))
    ctime = strftime('%Y-%m-%d %H:%M:%S', localtime(os.path.getctime(file)))
    return max(mtime, ctime)


def __att_file(file_src, file_dst, lock):
    __delete_file(file_dst)
    copy_export(file_src, file_dst, lock)


def __tree(src_entries, src, dst, lock):
    for src_entry in src_entries:
        path_src = os.path.join(src, src_entry)
        path_dst = os.path.join(dst, src_entry)
        if os.path.isdir(path_src):
            if os.path.isdir(path_dst):
                tree(path_src, path_dst, lock)
            else:
                os.makedirs(path_dst)
                tree(path_src, path_dst, lock)


def tree(src, dst, lock):
    sys.audit("copytree", src, dst)
    if not(os.path.isdir(dst)):
        os.makedirs(dst)
    src_entries = sorted(os.listdir(src))
    dst_entries = sorted(os.listdir(dst))
    add, remove = __compare_path(src, src_entries, dst_entries, lock)
    if len(add) > 0:
        __add_files(src, dst, add, lock)
    if len(remove) > 0:
        __remove_files(dst, remove)
    #######
    del src_entries, dst_entries
    #######
    src_entries = sorted(os.listdir(src))
    dst_entries = sorted(os.listdir(dst))
    __compare_files(src_entries, dst_entries, src, dst, lock)
    #######
    return __tree(src_entries, src, dst, lock)