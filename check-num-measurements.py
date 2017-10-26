#!/usr/bin/env python                                                                                                                                                                                                                                                            
  
  '''
  Get the 10 top consuming measurements (# of series)
  '''
  
  import os, re, operator, json
  from subprocess import Popen, PIPE
  from collections import Counter
  
  measurements=[]
  database='telegraf'
  port='8086'
  host='localhost' 

  def os_system(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
      line = process.stdout.readline()
      if not line:
        break
      # skip the the header
      if re.match(r'^key ', line) or re.match(r'^---', line):
        continue
      yield line
  
  
  def main():
    for line in os_system("influx -host "+host+" -database "+database+" -port "+port+" -execute \"show series\""):
      measure = line.split(',')[0]
      measurements.append(measure)
    counter = Counter(measurements)
    top_measurements = dict(sorted(counter.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
    print json.dumps(top_measurements)
  
  
  if __name__ == "__main__":
    main()
