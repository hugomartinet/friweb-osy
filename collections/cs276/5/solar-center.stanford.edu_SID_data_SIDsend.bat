rem this script can be used to send sid monitor files to stanford rem rem run this script to send data in the tosend directory rem rem the following lines should be set to describe your site rem the tosend directory must be created to enable automatic rem copies of the data files to be put there rem this version of sidsend bat for versions of sidsend exe after may 2006 rem a record of files sent will be put into eventlog uploadlog txt set sid_log eventlog uploadlog txt rem move up from bin directory this is sid root cd rem make a temp directory move files to the sending dir rem this prevents a possibility of losing data mkdir tosend sending move tosend csv tosend sending rem the next line connects to stanford and sends your file rem ftp does not return success fail code ftp i s conf ftp_cmds txt a sid ftp stanford edu rem make a log entry date t sid_log time t sid_log dir tosend sending csv b sid_log rem now remove the files just sent & temp sending directory del tosend sending csv rmdir tosend sending
