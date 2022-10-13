import logging
import os
from scripts.test_common_info import *
import re

name = 'vs1r'
instr = 'vs1r'
instr1 = 'vl1re8'
instr2 = 'vl1re16'
instr3 = 'vl1re32'
instr4 = 'vl1re64'


def generate_macros(f):
    for n in range(1,30):
        print("#define TEST_VSRE1_OP_1%d(  testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x%d, base; "%n + " \\\n\
            li  x30, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x%d); "%n + "\\\n\
            load_inst v14, (x%d); "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        print("#define TEST_VSRE1_OP_rd%d( testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE( testnum, v%d, result, "%n + "\\\n\
            la  x1, base;  \\\n\
            li  x3, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v%d, x3;  "%n + "\\\n\
            VSET_VSEW \\\n\
            store_inst v%d, (x1); "%n + " \\\n\
            load_inst v31, (x1); \\\n\
        )",file=f)

    print("#define TEST_VSRE1_OP_130( testnum, load_inst, store_inst, eew, result, base ) \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x30, base;  \\\n\
            li  x3, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x3; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x30); \\\n\
            load_inst v14, (x30) ;  \\\n\
        )",file=f)

    print("#define TEST_VSRE1_OP_rd31( testnum, load_inst, store_inst, eew, result, base ) \\\n\
        TEST_CASE( testnum, v31, result, \\\n\
            la  x1, base;  \\\n\
            li  x3, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v31, x3; \\\n\
            VSET_VSEW \\\n\
            store_inst v31, (x1); \\\n\
            load_inst v1, (x1);  \\\n\
        )",file=f)

    
def generate_tests(f, rs1_val, rs2_val):
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(1):
        n += 1
        print("  TEST_VSRE1_OP( "+str(n)+",  %s.v, %s.v, "%(instr1,instr)+" 8 "+", "+"0xff"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VSRE1_OP( "+str(n)+",  %s.v, %s.v, "%(instr2,instr)+" 16 "+", "+"0xff00"+",  "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VSRE1_OP( "+str(n)+",  %s.v, %s.v, "%(instr3,instr)+" 32 "+", "+"0xff0000ff"+",  "+"0 + tdat"+" );", file=f)
        # n += 1
        # print("  TEST_VSRE1_OP( "+str(n)+",  %s.v, %s.v, "%(instr4,instr)+" 64 "+", "+"0x00ff000000ff0000"+",  "+"0 + tdat"+" );", file=f)
       
        

    for i in range(100):     
        k = i%30+1
        n+=1
        print("  TEST_VSRE1_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr3,instr)+"32"+", "+"0xf00f00ff"+", "+"0 + tdat"+" );",file=f)
    
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("  TEST_VSRE1_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr3,instr)+"32"+", "+"0xf00fff00"+", "+"-8 + tdat4"+" );",file=f)

    


def create_empty_test_vs1r(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    print(" TEST_VSRE1_OP( 2, vl1re8.v,  vs1r.v, 8,  0xff,  0  + tdat  );", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vs1r(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val)

    # Common const information
    # print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
