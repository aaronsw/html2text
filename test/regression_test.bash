#!/bin/bash

echo Direct invocation

fileToProcess=GoogleDocSaved
echo Testing $fileToProcess.html...
python ../html2text.py -g -d -b 0 -s $fileToProcess.html > tmp.mkd
diff $fileToProcess.mkd tmp.mkd > /dev/null
if [ $? -ne 0 ]; then
  echo Failed on $fileToProcess.html
  exit 1
fi

fileToProcess=GoogleDocMassDownload
echo Testing $fileToProcess.html...
python ../html2text.py -g -d -b 0 -s $fileToProcess.html > tmp.mkd
diff $fileToProcess.mkd tmp.mkd > /dev/null
if [ $? -ne 0 ]; then
  echo Failed on $fileToProcess.html
  exit 1
fi

fileToProcess=normal
echo Testing $fileToProcess.html...
python ../html2text.py $fileToProcess.html > tmp.mkd
diff $fileToProcess.mkd tmp.mkd > /dev/null
if [ $? -ne 0 ]; then
  echo Failed on $fileToProcess.html
  exit 1
fi

echo Run through import

fileToProcess=GoogleDocSaved
echo Testing $fileToProcess.html...
python regression_google.py -g -d -b 0 -s $fileToProcess.html > tmp.mkd
diff $fileToProcess.mkd tmp.mkd > /dev/null
if [ $? -ne 0 ]; then
  echo Failed on $fileToProcess.html
  exit 1
fi

fileToProcess=GoogleDocMassDownload
echo Testing $fileToProcess.html...
python regression_google.py -g -d -b 0 -s $fileToProcess.html > tmp.mkd
diff $fileToProcess.mkd tmp.mkd > /dev/null
if [ $? -ne 0 ]; then
  echo Failed on $fileToProcess.html
  exit 1
fi

fileToProcess=normal
echo Testing $fileToProcess.html...
python regression_standard.py $fileToProcess.html > tmp.mkd
diff $fileToProcess.mkd tmp.mkd > /dev/null
if [ $? -ne 0 ]; then
  echo Failed on $fileToProcess.html
  exit 1
fi

rm tmp.mkd

echo Regression tests passed successfully
