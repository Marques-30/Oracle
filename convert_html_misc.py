#!/usr/bin/python

###############################################################################
# This is program is converting the HC email files to HTML files for emailing
# purpose. There are two health check files processed by this program and file
# name is generated using the batch name passed as parameter. Program outputs 
# the html file and pass them to the email program.
#
# Developer : Ramesh Ganesan
#
# Date : 31st Mar 2016
#
###############################################################################

import sys
import os
import glob
import shutil
import datetime
from email_alerts import send_email

if __name__ == "__main__":

  v_batch_name=sys.argv[1]
  v_file_path=sys.argv[2]
  v_cycle_date=sys.argv[3]
  v_emails=sys.argv[4]

  #setting up the directory
  os.chdir(v_file_path+'/')

  outfile='/u1/bidm/edw/CAPPR/scripts/HC_HTML_FILES/'+v_batch_name+'.html'
  file_write=open(outfile,'w')
  file_met=0
  mesg1='<html><head><meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" /><title> HC EMAILS </title></head><body style="font-family: Verdana, Tahoma; font-size:10pt;"><table bgcolor="#ffffff" width="800" cellspacing="1" cellpadding="1" border="0" bordercolor="#494e52" style="font-family: Verdana, Tahoma; font-size:10pt;"><tbody>'
  footer=''
  fail_check=0
  warn_check=0

  for file in glob.glob('HC_FIELD_CHK'+'*'+v_batch_name):
    v_reg_hc_misc_file=file

    if (os.stat(v_file_path+'/'+v_reg_hc_misc_file).st_size > 0 ):
       file_met=file_met+1
       file_obj=open(v_file_path+'/'+v_reg_hc_misc_file)
       a=[]
       i=0 
       for i, row in enumerate(file_obj):
          #print(row)
          a=row.split(";")
          if (i < 4 and file_met < 2):
             footer=footer+'<BR>'+a[0] 
             #print(row)
          if (i > 3 and i < 16 and file_met < 2):
             mesg1=mesg1+'<tr><td nowrap>'+a[0]+'<td nowrap>:<td word-wrap:break-word>'+a[1]+'</td></tr>'
          if i == 14:
             if (a[1].rstrip() == "FAILED"):
                fail_check=1
             if (a[1].rstrip() == "WARNING"):
                warn_check=1
          if i == 15:
             v_mail_subj=a[1].rstrip()
          if i == 16:
             mesg1=mesg1+'</tbody></table>'
             mesg1=mesg1+'<br><h4>'+a[0]+'</h4><br>'
             mesg1=mesg1+'<table bgcolor="#efefef" width="1000" cellspacing="1" cellpadding="1" border="1" bordercolor="#494e52" style="font-family: Verdana, Tahoma; font-size:10pt;"><thead>'
          if i == 17:
  # new changes misc file
             loop_length=len(a)-1

             mesg1=mesg1+'<tr style="font-weight:bold;color:#ffebb5;" bgcolor="#548dd4">'
             for x in range(0, loop_length):
                 mesg1=mesg1+'<th nowrap>'+a[x]
             mesg1=mesg1+'</th></tr></thead><tbody>'
          if i > 17:
             if a[loop_length].rstrip() == "FAIL":
                #fail_check=1
                mesg1=mesg1+'<tr style="color:#ff0000;">'
                for x in range(0, loop_length):
                   try:
                      val = float(a[x])
                      num_flg = 1
                   except ValueError:
                      val = None
                      num_flg = 0

                   if (num_flg == 1):
                      mesg1=mesg1+'<td nowrap align="right">'+a[x]
                   elif (num_flg == 0):
                      mesg1=mesg1+'<td nowrap>'+a[x]
                mesg1=mesg1+'</td></tr></thead>'
             elif a[loop_length].rstrip() == "WARNING":
                #warn_check=1
                mesg1=mesg1+'<tr style="color:#cc7a00;">'
                for x in range(0, loop_length):
                   try:
                      val = float(a[x])
                      num_flg = 1
                   except ValueError:
                      val = None
                      num_flg = 0

                   if (num_flg == 1):
                      mesg1=mesg1+'<td nowrap align="right">'+a[x]
                   elif (num_flg == 0):
                      mesg1=mesg1+'<td nowrap>'+a[x]
                mesg1=mesg1+'</td></tr></thead>'
             else:
                mesg1=mesg1+'<tr style="color:#004d1a;">'
                for x in range(0, loop_length):
                   try:
                      val = float(a[x])
                      num_flg = 1
                   except ValueError:
                      val = None
                      num_flg = 0

                   if (num_flg == 1):
                      mesg1=mesg1+'<td nowrap align="right">'+a[x]
                   elif (num_flg == 0):
                      mesg1=mesg1+'<td nowrap>'+a[x]

                mesg1=mesg1+'</td></tr>'
          file_write.write(mesg1)
          mesg1=''
       mesg1=mesg1+'</tbody></table><BR><BR>'

  if (os.stat(v_file_path+'/'+v_reg_hc_misc_file).st_size > 0 ):
     mesg1=mesg1+footer
     mesg1=mesg1+'</body></html>'
  file_write.write(mesg1)
  file_write.close()
  #Define message subject

  if (fail_check == 1):
     v_mesg_subj='FAILED: Cycle date='+sys.argv[3]+': '+v_mail_subj
  elif (warn_check == 1):
     v_mesg_subj='WARNING: Cycle date='+sys.argv[3]+': '+v_mail_subj
  else:
     v_mesg_subj='SUCCESSFUL: Cycle date='+sys.argv[3]+': '+v_mail_subj

  dttime=datetime.datetime.now()
  bkupfile='/u1/bidm/edw/CAPPR/scripts/HC_HTML_FILES/OLD_FILES/'+v_batch_name+'_'+dttime.strftime("%Y_%m_%d_%H%M%S")+'.html'

  if (os.stat(outfile).st_size > 0):
     send_email(['-f', outfile, v_mesg_subj, 'alerts@bankofthewest.com','html', v_emails])

  shutil.copy(outfile, bkupfile) 

# The End
