#!/Users/scripting/perl5/perlbrew/perls/perl-5.24.0/bin/Perl
#use warnings;
## Larry Gonyea - Gracenote
## This script (featuremanager.cgi) is a features controller for finding and organizing Feature text and Feature photos. 
## 	This will help users navigate to viewing an existing feature or starting a new feature by passing along CGI parameters to the 
##    script feature_editor.cgi
use strict;
use Tie::File;
use File::Copy;
use CGI;
use File::Find;
use utf8;
#use encoding 'UTF-8';
require("PD_common_func.cgi");
require("PD_web_elements.cgi");
my $homeIP = "featuremanager.tmsgf.trb";
my $currenttime = GetDateTime();
my $pageMode = "";
my @daysOfWeek = qw( Sunday Monday Tuesday Wednesday Thursday Friday Saturday );
my @shortdaysOfWeek = qw( Sun Mon Tue Wed Thu Fri Sat );
my @monthsOfYear = qw( January Febuary March April May June July August September October November December );
my @shortmonthsOfYear = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
my $selfPage = "$homeIP/cgi-bin/Operations/monitor.cgi";

#pickup any CGI parameters fed to the page
my $query = new CGI;
my $pageType = $query->param('pageType');
my $pageMode = $query->param('pageMode');
my $mysearch = $query->param('search');
my $prodType = $query->param('prodType');
my $pageStatus = $query->param('refresh');
my $screenMode = $query->param('screenMode');
my $scriptStatDir = "/Library/WebServer/AS/";
my $cronacleFailRpt = "/Library/WebServer/Cronacle/FailReport/FailReport.txt";
my $cronacleRunRpt = "/Library/WebServer/Cronacle/Running/RunningReport.txt";
my $cronacleComplete = "/Library/WebServer/Cronacle/Reports/Completed.txt";
my $cronacleSchedule = "/Library/WebServer/Cronacle/Reports/Scheduled.txt";
my $ripeFailRpt = "/Library/WebServer/Becky/data_production_fail.electronic";
my $ripeRunRpt = "/Library/WebServer/Becky/data.production_status";
my $cust_master_file = "/Library/WebServer/Becky/allcust.txt";
my @Becky_Master = arrayFile($cust_master_file);
my @CronFails = arrayFile($cronacleFailRpt);
my @CronRuns = arrayFile($cronacleRunRpt);
my @CronComp = arrayFile($cronacleComplete);
my @CronSched = arrayFile($cronacleSchedule);
my @RipeFails = arrayFile($ripeFailRpt);
my @RipeRuns = arrayFile($ripeRunRpt);
my $AVtot = 0;
my $RipeFailTot = 0;
my $CronacleFailTot = 0;
my $script_FailTot = 0;
my $snapshot = "/Library/WebServer/Becky/snapshot9.txt";
my @AlphaJobs = allBeckyQueuesII();

makeHTML5type($pageMode);
LoadCSS("operations.css");
LoadJS();
if ($screenMode ne "BIG") {
	JQfadeIn("#Content","slow");
} else {
	JQfadeIn("#ContentBig","slow");
}
JQtoggleAPhold(".APHolding","APbutton");

print "</script>";

HTMLtitle("Gracenote Operations Monitor");
OpenDIV("ID","Header");
makeHeaderTopper();
ClosedDIV("class","HeaderLeft","Gracenote Operations Monitor - $currenttime");
#my $AllFeatList = getFileList("$baseFEfolder/templates/","No");
EndDIV();
OpenDIV("ID","Container");

if ($screenMode ne "BIG") {

	#start the navigation bar
	OpenDIV("ID","Nav");
	OpenDIV("class","NavLeft",);
	makeNAVbar();
	EndDIV();
	EndDIV();
}
#############

if ($screenMode ne "BIG") {
	OpenDIV("ID","Content");
} else {
	OpenDIV("ID","ContentBig");
}

if ($pageType eq "AutoPag") {
	OpenDIV("class","toggleBar");
		ClosedDIV("class","toggleButtons","<APbutton>Show Holding AutoPag</APbutton>");
	EndDIV();
#	ClosedDIV("class","ContentBoxPlain","AutoPag Status");
	TurboProd();
	#my @allSCstats = ArrayADir("$scriptStatDir","");
	#foreach my $turboStat (@allSCstats) {
	#	open FH,"<$scriptStatDir$turboStat";
	#	my @fileSplit = <FH>;
	#	my $line = join "\n", @fileSplit;
	#	close FH;
	#	my @turboFacts = split('\|',$line);
	#	my $step = $turboFacts[0];
	#	my $scriptName = $turboFacts[1];
	#	my $machine = $turboFacts[2];
	#	my $timeStamp = $turboFacts[3];		
	#	OpenDIV("class","ASrow","");
	#	ClosedDIV("class","AScol","$scriptName");
	#	ClosedDIV("class","AScol","$machine");
	#	ClosedDIV("class","AScol","$step");
	#	ClosedDIV("class","AScol","$timeStamp");
	#	EndDIV();
	#}
	
} elsif ($pageType eq "CronacleProd") {
my @headerSizes = ("7","0","20","20","0","7","12","12","7","12");
#my @CronComp = arrayFile($cronacleComplete);
#my @CronSched = arrayFile($cronacleSchedule);
#Job Id|Client ID|Customer Code/Name|Product Name|Hybrid Id|System|Completed Date|Elapsed Time|Job Chain
	foreach (@CronComp) {
		my $colCount = 0;
		my @lineElements = split('\|',$_);
		if ($_ =~ m/^Job Id/) {
			OpenDIV("class","ApoHeader","");				
		} elsif ($_ !~ m/^\d/) {
			next; 
		} else {
			OpenDIV("class","ApoRow","");		
		}
		
		foreach my $element (@lineElements) {
			if (($colCount == 5) && ($_ !~ m/^Job Id/)) {
				$element = substr($element,9,length($element));
			}	
			if (($colCount != 1) && ($colCount != 4)) {
				#print "$element"; 
					ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
			}
			$colCount++;
		}
		EndDIV();
		print "<br>";	
		if ($_ =~ m/^Job Id/) {  
				print "<br><hr>"; 
		}	
	}
			print "<br>";	
			print "<br>";	
			

} elsif ($pageType eq "CronacleSched") {
my @mainHeaderSize = ("7","20","20","7","12","12","7","12");
my @HeaderNames = ("Job","Customer","Product","System","Step/Status","Date","");
my @headerSizes = ("7","0","20","20","0","7","12","12","7","12");
#my @CronComp = arrayFile($cronacleComplete);
#my @CronSched = arrayFile($cronacleSchedule);
#Job Id|Client ID|Customer Code/Name|Product Name|Hybrid Id|System|Completed Date|Elapsed Time|Job Chain
	foreach (@CronSched) {
		my $colCount = 0;
		my @lineElements = split('\|',$_);
		if ($_ =~ m/^Job Id/) {
			OpenDIV("class","ApoHeader","");				
		} elsif ($_ !~ m/^\d/) {
			next; 
		} else {
			OpenDIV("class","ApoRow","");		
		}
		
		foreach my $element (@lineElements) {
			if (($colCount == 5) && ($_ !~ m/^Job Id/)) {
				$element = substr($element,9,length($element));
			}	
			if (($colCount != 1) && ($colCount != 4)) {
				#print "$element"; 
					ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
			}
			$colCount++;
		}
		EndDIV();
		print "<br>";	
		if ($_ =~ m/^Job Id/) {  
				print "<br><hr>"; 
		}	
	}
			print "<br>";	
			print "<br>";	
			
} elsif ($pageType eq "AVMON") {
my @headerSizes = ("7","30","7","15","15","7");
my $snapLast = getFileStats($snapshot);
	ClosedDIV("class","CategoryHeader","AV MONITOR - $snapLast");
	
tie my @records, 'Tie::File', $snapshot;
my $fullFile = join "\n",@records;
untie @records;
$fullFile =~ s/\s+/ /g;
$fullFile =~ s/ Generic/\nGeneric/g;
$fullFile =~ s/Batch/\nBatch/g;
$fullFile =~ s/Entry Jobname Username Status ----- ------- -------- ------/ /g;
$fullFile =~ s/.COM\;\d+/.COM\n/g;
$fullFile =~ s/\(executing\)//g;
$fullFile =~ s/Logical(.*)\n/\n/g;
$fullFile =~ s/Printer(.*)\n/\n/g;
$fullFile =~ s/\/RETAIN=ERROR\s\s\s/\/RETAIN=ERROR\n/g;
$fullFile =~ s/\)\s\s\s/\)\n/g;
$fullFile =~ s/\n\s+/\n/g;
$fullFile =~ s/\/BASE_PRIORITY=\d\s//g;
$fullFile =~ s/\/OWNER=\[\d,\d\]//g;
$fullFile =~ s/\/PROTECTION=((.*))//g;
$fullFile =~ s/Completed \d-\w\w\w-\d\d\d\d \d\d:\d\d:\d\d\.\d\d on queue VERIFY_BECKY //g;
$fullFile =~ s/Completed \d-\w\w\w-\d\d\d\d \d\d:\d\d:\d\d\.\d\d on queue VERIFY_NORM //g;
#open FH,">/PerlTemp/newsnapshot.txt";
#print FH $fullFile;
#close FH;
my @allLines = split("\n",$fullFile);
my $queu_tracker;
my @colHeads = ("ENTRY","FILENAME","CID","TIME","DAY","STATUS");
OpenDIV("class","ApoHeader","");				
my $colCount = 0;
foreach my $element (@colHeads) {
    ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
    $colCount++;
}

EndDIV();
foreach (@allLines) {

    if ($_ =~ /^Generic batch queue VERIFY_GENERIC/) {
	my @Gen_que_parts = split('\s',$_);
	my $this_GQ = $Gen_que_parts[3];
	#print "$this_GQ\n";
	my @find_batch_que = split('/GENERIC=');
	my @Batch_q_list = split(',',$find_batch_que[1]);
	#print join("\n",@Batch_q_list);
	foreach my $this_BQ (@Batch_q_list) {
	    $this_BQ =~ s/\(|\)//g;		
	    $this_BQ =~ s/\s//g;	
	    $queu_tracker = "FALSE";
	    #print "\t Looking for -$this_BQ-\n";
	    foreach my $find_queue (@allLines) {
		my @batch_q_parts = split(',',$find_queue);
		#print "Looking at $batch_q_parts[0]\n";
		if (($queu_tracker eq "FALSE") && ($find_queue =~ /^Batch queue $this_BQ/m)) {
		    my $bq_status = $batch_q_parts[1];
		    #print "$this_BQ - $bq_status\n";
		    $queu_tracker = "TRUE";
		    next;				 
		} elsif (($queu_tracker eq "TRUE") && ($find_queue =~ /^(Gen|Bat)/m)){
		    $queu_tracker = "FALSE";
		    #print "End of $this_BQ\n";
		    next;
		} elsif (($queu_tracker eq "TRUE") && ($find_queue =~ /^\d/m)) {
		    my $AVstatus;
		    my @batch_job = split(' ',$find_queue);
		    my @AVParts = split("_",$batch_job[1]);
		    my $AVcid = $AVParts[1];
		    my $AVDay = $AVParts[2];
		    my $dueHour = substr($batch_job[1],2,2);
		    my $dueMin = substr($batch_job[1],4,2);
		    my $dueTime = "$dueHour:$dueMin";					
		    my $nospace_list = $find_queue;
		    my $jobStatus = $batch_job[3];
		    $nospace_list =~ s/\s//g; 
		    $nospace_list =~ /PARAM\=(.*)\/PRIORITY/;
		    my $params = $1;
		    $params =~ s/\(//g;
		    $params =~ s/\)//g;
		    $params =~ s/\"//g;
		    my @allParams = split(',',$params);
		    my $local = $allParams[0]; 
		    my $file = $allParams[1]; 
		    #foreach my $thisSection (@batch_job) {
		    #	if ($thisSection =~ /^\/PARAM/m) {
		    #		$Params = $thisSection;
		    #		#$Params = split(',',$thisSection);
		    #		$Params =~ s/\/PARAM=\(//g;
		    #		$Params =~ s/\)//g;
		    #	}		
		    #}
		    #my $find_queue =~ /\/PARAM=(.*)\s\/PRIORITY/;
		    if ($batch_job[1] =~ /^AV/m) {
			$AVstatus = "Verifying";
		    } else {
			$AVstatus = "Missing";
		    }
		    my @AVCOls = ($batch_job[0],$file,$AVcid,$dueTime,$AVDay,$AVstatus);
		    my $colCount = 0;
		    if ($jobStatus eq "Retained") {
			OpenDIV("class","ApoRowFail","");
		    } else {
			OpenDIV("class","ApoRow","");							
		    }							
		    foreach my $element (@AVCOls) {
			ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
			$colCount++;
		    }
		    EndDIV();
		    
		    #	 print "Verifying...\t$file CID:$AVcid Day:$AVDay Due at $dueTime\n\n";
		    #} else {
		    #	 print "Missing!\t$file CID:$AVcid Day:$AVDay Due at $dueTime\n\n";						 
		    #}
		}
	    }
	}
    }

}
ClosedDIV("class","CategoryHeader","Alpha problems - $snapLast");
foreach (@AlphaJobs) {
    my $colCount = 0;
    my $thisrow = $_;
    my @jobParts = split('\|',$thisrow);
    #ClosedDIV("class","ApoHeader","$thisrow");		
    #"JOB|$script_status|$now_queue|$job_num|$job_name|$these_params";
    if ($thisrow =~ /^GenQ/) {
	#ClosedDIV("ID","GenQue","$jobParts[1]");			
    }
    if (($thisrow =~ /^BatchQ/) && ($jobParts[2] =~ /idle/)) {
	#ClosedDIV("ID","BatchQue","$jobParts[1]");			
    }			
    if (($thisrow =~ /^BatchQ/) && ($jobParts[2] =~ /stopped/)) {
	OpenDIV("class","ApoRowFail","");
	foreach my $element (@jobParts) {
	    ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
	    $colCount++;
	}
	#ClosedDIV("class","ApoRowFail","$jobParts[1] queue is stopped");			
	EndDIV();
    }			
    if (($thisrow =~ /^JOB/) && ($jobParts[1] =~ /Executing/)) {
	#				ClosedDIV("ID","JobExe","$jobParts[4] is in Queue $jobParts[2] Entry: $jobParts[3]");			
    }			
    if (($thisrow =~ /^JOB/) && ($jobParts[1] =~ /Pending/)) {
	#				ClosedDIV("ID","JobPend","$jobParts[4] is in Queue $jobParts[2] Entry: $jobParts[3]");			
    }			
    if (($thisrow =~ /^JOB/) && ($jobParts[1] =~ /Retained/)) {
	OpenDIV("class","ApoRowFail","");
	foreach my $element (@jobParts) {
	    ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
	    $colCount++;
	}
	EndDIV();
    }			
    #$thisrow =~ s/\|/&nbsp\;&nbsp\;&nbsp\;&nbsp\;/g;
    #ClosedDIV("class","ApoHeader","$thisrow");		
}


} else {
    my @HeaderNames = ("Customer","Product","System","Step/Status","Date","Job");
    my @headerSizes = ("20","20","17","12","12","7","12","10");
    my $colCount = 0;
    OpenDIV("class","ApoHeader","");				
    foreach my $element (@HeaderNames) {
	ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
	$colCount++;
    }
    EndDIV();
    #	my @CronFails = arrayFile($cronacleRunRpt);
    #my @headerSizes = ("10","15","25","15","15","7","15","10","10","10");
    my @failLast = checkReportAge($cronacleFailRpt);
    my @runLast = checkReportAge($cronacleRunRpt);
    my $ripeFailRpt = "/Library/WebServer/Becky/data_production_fail.electronic";
    my $ripeRunRpt = "/Library/WebServer/Becky/data.production_status";
    my @ripefailLast = checkReportAge($ripeFailRpt);
    my @riperunLast = checkReportAge($ripeRunRpt);
    if ($pageType ne "runs") {
	ClosedDIV("class","$failLast[0]","CRONACLE FAILS $failLast[1]");
	foreach (@CronFails) {
	    my $colCount = 0;
	    my @lineElements = split('\|',$_);
	    my $cid = substr($lineElements[2],0,3);
	    my @timeFile = split(' ',$lineElements[8]);
	    my @hour_Min = split(':',$timeFile[1]);
	    my $eventTime = "$hour_Min[0]$hour_Min[1]";
	    if ($_ =~ m/^Job Id/) {
		next;
		OpenDIV("class","ApoHeader","");				
	    } else {
		$CronacleFailTot++;
		if ($screenMode ne "BIG") {
		    OpenDIV("class","ApoRowFail","");
		} else {
		    OpenDIV("class","ApoRowFailBig","");			
		}
	    }
	    #Job Id|Client ID|Customer Code/Name|Product Name|Hybrid Id|System|Step|Start|End|Job Chain
	    my $shrt_cus = substr($lineElements[2],0,23);
	    my $short_system = substr($lineElements[5],9,length($lineElements[5]));
	    my @ColsNeeded = ($shrt_cus,$lineElements[3],$short_system,$lineElements[6],$lineElements[8],$lineElements[0]);
	    foreach my $element (@ColsNeeded) {
		ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
		$colCount++;
	    }
	    if ($_ =~ m/^Job Id/) {  
		print "<br><hr>"; 
	    }	
	    EndDIV();
	    #print "<br>";	
	    if ($_ =~ m/^Job Id/) {  
		print "<br><hr>"; 
	    }	
	}

	#my @RipeheaderSizes = ("10","15","25","15","15","10","10");
	ClosedDIV("class","$ripefailLast[0]","RIPE FAILS $ripefailLast[1]");
	#my @lineElements = ("Sched ID","Cust Code","Product Name","System","Step","Time","Prod ID");
	my $colCount = 0;

	my $inHungProc = "FALSE";
	foreach my $RipeLine (@RipeFails) {
	    if (($RipeLine =~ m/POSSIBLE HUNG PROCESSES/) || ($inHungProc eq "TRUE"))  {
		$inHungProc = "TRUE";
		next;
	    } 
	    my $colCount = 0;
	    my $lineopen = substr($RipeLine,0,13);
	    my $schedID = substr($RipeLine,14,10);
	    my $prodID = substr($RipeLine,25,9);
	    my $cuscode = substr($RipeLine,35,9);
	    my $prodName = substr($RipeLine,45,30);
	    my $date = substr($RipeLine,76,8);
	    my $notes = substr($RipeLine,85,14);
	    my $system = substr($RipeLine,103,8);
	    my $step = substr($RipeLine,112,8);
	    my $statNum = substr($RipeLine,121,3);
	    my $StartTime = substr($RipeLine,125,17);
	    my $EndTime = substr($RipeLine,143,17);
	    my $DueTime = substr($RipeLine,161,4);
	    my @dateTime = split(' ',$EndTime);
	    my $screenDate = $dateTime[0];
	    my $screenTime = substr($dateTime[1],0,5);
	    my $notes = lc($notes);
	    if (($step =~ m/ROUTE/) & ($notes =~ m/if route/)) {
		next;
	    }
	    if ($notes =~ m/test/) { next; }
	    if (($system =~ m/^qa/) || ($system =~ m/^re/)) {
		next;
	    }
	    if ($schedID !~ m/\d/) {
		next;
	    }	
	    my $shrt_cus = substr($cuscode,0,23);
	    my @lineElements = ($shrt_cus,$prodName,$system,$step,$screenTime,$schedID,$prodID);
	    if ($screenMode ne "BIG") {
		OpenDIV("class","ApoRowFail","");
	    } else {
		OpenDIV("class","ApoRowFailBig","");			
	    }
	    $RipeFailTot++;
	    foreach my $element (@lineElements) {
		ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
		$colCount++;
	    }
	    EndDIV();
	    print "<br>";	
	    print "<br>";	
	}

	#### AVs
	my ($f_second, $f_minute, $f_hour, $f_day, $f_month, $f_year, $f_weekDay, $f_dayOfYear, $IsDST) = localtime(time);
	my $nowtime = ($f_hour * 60) + $f_minute;
	#my @headerSizes = ("7","30","5","30","5","5","5","10");
	my $snapshot = "/Library/WebServer/Becky/snapshot9.txt";
	my @snapLast = checkReportAge($snapshot);
	ClosedDIV("class","$snapLast[0]","AV MONITOR $snapLast[1]");
	
	my @allLines = allBeckyQueuesII();
	my $queu_tracker;
	foreach (@allLines) {
	    my $colCount = 0;
	    my $thisrow = $_;
	    #print "$thisrow<br>";
	    my @jobParts = split('\|',$thisrow);
	    #my $recordThis = "JOB|$script_status|$now_queue|$job_num|$job_name|$these_params";

	    if (($jobParts[0] eq "JOB") && ($jobParts[2] =~ /^VERIFY/)) {
		my $AVstatus;
		#	my @batch_job = split(' ',$find_queue);
		my @AVParts = split("_",$jobParts[4]);
		my $AVcid = $AVParts[1];
		my @custMaster = findCustomer($AVcid);
		my $custName = $custMaster[1];
		my $deptName = $custMaster[2];
		my $thisDept;
		if ($deptName eq "IS") {
		    $thisDept = "CCE";
		} else {
		    $thisDept = "CCN";	
		}
		my $AVDay = $AVParts[2];
		my $dueHour = substr($jobParts[4],2,2);
		my $dueMin = substr($jobParts[4],4,2);
		my $whenDew = ($dueHour * 60) + $dueMin;
		my $howLate = $nowtime - $whenDew;
		my $dueTime = "$dueHour:$dueMin";					
		#		my $nospace_list = $find_queue;
		#	my $jobStatus = $batch_job[3];
		#	$nospace_list =~ s/\s//g; 
		#	$nospace_list =~ /PARAM\=(.*)\/PRIORITY/;
		#	my $params = $1;
		#	$params =~ s/\(//g;
		#	$params =~ s/\)//g;
		#	$params =~ s/\"//g;
		my @allParams = split(',',$jobParts[5]);
		my $local = $allParams[0]; 
		my $file = $allParams[1]; 
		#foreach my $thisSection (@batch_job) {
		#	if ($thisSection =~ /^\/PARAM/m) {
		#		$Params = $thisSection;
		#		#$Params = split(',',$thisSection);
		#		$Params =~ s/\/PARAM=\(//g;
		#		$Params =~ s/\)//g;
		#	}		
		#}
		#my $find_queue =~ /\/PARAM=(.*)\s\/PRIORITY/;
		if ($jobParts[4] =~ /^MA/m) {
		    $AVstatus = "$howLate mins late";
		    my $AvDIV = "";
		    if ($howLate > 25) {
			$AvDIV = "25";
		    }
		    if ($howLate > 35) {
			$AvDIV = "35";
		    }								
		    if ($howLate > 60) {
			$AvDIV = "60";
		    }	
		    if ($howLate > 120) {
			$AvDIV = "120";
		    }	
		    $AVtot++;
		    my $cust_col = "$AVcid - $custName";
		    my $shrt_cus = substr($cust_col,0,25);							
		    #my @AVCOls = ($batch_job[0],$file,$AVcid,$custName,$dueTime,$AVDay,$thisDept,$AVstatus);
		    #my $recordThis = "JOB|$script_status|$now_queue|$job_num|$job_name|$these_params";
		    #		my @AVCOls = ($jobParts[0],$jobParts[1],$jobParts[2],$jobParts[3],$jobParts[4],$jobParts[5]);
		    my @AVCOls = ($shrt_cus,$file,$thisDept,$AVstatus,"$AVDay at $dueTime",$jobParts[1]);
		    my $colCount = 0;
		    #OpenDIV("class","AVstat$AvDIV","");
		    OpenDIV("class","AVstat$AvDIV","");
		    foreach my $element (@AVCOls) {
			ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
			$colCount++;
		    }
		    EndDIV();
		}
	    }
	    #}
	    #}
	    #}


	}
	ClosedDIV("class","CategoryHeader","ALPHA QUEUES $snapLast[1]");
	my @AlphaJobs = allBeckyQueuesII();
	my @ignore_alpha = ("EDDIE_ELEC_EXT","XXX","ZIP9","RIPE_EXT_DEVRIPE10");
	foreach (@AlphaJobs) {
	    my $colCount = 0;
	    my $thisrow = $_;
	    #print "$thisrow<br>";
	    my @jobParts = split('\|',$thisrow);
	    #ClosedDIV("class","ApoHeader","$thisrow");		
	    #"JOB|$script_status|$now_queue|$job_num|$job_name|$these_params";
	    if ($jobParts[2] =~ /^VERIFY/) {			
		next;
	    }
	    if ($jobParts[2] ~~ @ignore_alpha) {
		next;
	    }
	    if ($thisrow =~ /^GenQ/) {
		#ClosedDIV("ID","GenQue","$jobParts[1]");			
	    }
	    if (($thisrow =~ /^BatchQ/) && ($jobParts[2] =~ /idle/)) {
		#ClosedDIV("ID","BatchQue","$jobParts[1]");			
	    }			
	    if (($thisrow =~ /^BatchQ/) && ($jobParts[2] =~ /stopped/)) {
		OpenDIV("class","ApoRowFail","");
		my @line_list = ("&nbsp;",$jobParts[1],"&nbsp;","STOPPED","&nbsp;","&nbsp;");
		foreach my $element (@line_list) {
		    ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
		    $colCount++;
		}
		#ClosedDIV("class","ApoRowFail","$jobParts[1] queue is stopped");			
		EndDIV();
	    }			
	    if (($thisrow =~ /^JOB/) && ($jobParts[1] =~ /Executing/)) {
		#				ClosedDIV("ID","JobExe","$jobParts[4] is in Queue $jobParts[2] Entry: $jobParts[3]");			
	    }			
	    if (($thisrow =~ /^JOB/) && ($jobParts[1] =~ /Pending/)) {
		#				ClosedDIV("ID","JobPend","$jobParts[4] is in Queue $jobParts[2] Entry: $jobParts[3]");			
	    }			
	    if ($jobParts[1] =~ /Retained/) {
		
		if (($thisrow =~ /^JOB/) && ($jobParts[2] =~ /^TURBO/)) {
		    #print "$jobParts[5]\n";
		    my @allParams = split(',',$jobParts[5]);
		    my $scriptName = $allParams[0];
		    my $listdate = 	$allParams[1];		
		    my $CID = $allParams[3];
		    my $Status = $allParams[4];
		    my @custMaster = findCustomer($CID);
		    my $custName = $custMaster[1];
		    my $deptName = $custMaster[2];
		    my @line_list = ($custName,$scriptName,$jobParts[2],"&nbsp;",$listdate,$jobParts[3]);				
		    OpenDIV("class","ApoRowFail","");
		    foreach my $element (@line_list) {
			ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
			$colCount++;
		    }
		    EndDIV();						
		} elsif ($jobParts[2] =~ /^VERIFY/) {
		    next;
		    
		} else {
		    
		    OpenDIV("class","ApoRowFail","");
		    my @line_list = ($jobParts[1],$jobParts[4],$jobParts[2],"&nbsp;","&nbsp;",$jobParts[3]);
		    foreach my $element (@line_list) {
			ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
			$colCount++;
		    }
		    EndDIV();
		}
	    }			
	    #$thisrow =~ s/\|/&nbsp\;&nbsp\;&nbsp\;&nbsp\;/g;
	    #ClosedDIV("class","ApoHeader","$thisrow");		
	}
    }
    

    #Job Id|Client ID|Customer Code/Name|Product Name|Hybrid Id|System|Step|Date|Job Chain
    #my @headerSizes = ("10","15","25","15","15","7","15","10","10");
    if ($pageType ne "fails") {	
	ClosedDIV("class","$runLast[0]","CRONACLE EXECUTING $runLast[1]");
	foreach (@CronRuns) {
	    my $colCount = 0;
	    my @lineElements = split('\|',$_);
	    if ($_ =~ m/^Job Id/) {
		next;
		OpenDIV("class","ApoHeader","");				
	    } else {
		OpenDIV("class","ApoRow","");		
	    }
	    my $shrt_cus = substr($lineElements[2],0,25);
	    my $short_system = substr($lineElements[5],9,length($lineElements[5]));
	    my @cronacleNeeded = ($shrt_cus,$lineElements[3],$short_system,$lineElements[6],$lineElements[7],$lineElements[0]);
	    foreach my $element (@cronacleNeeded) {
		#if (($colCount == 5) && ($_ !~ m/^Job Id/)) {
		#	$element = substr($element,9,length($element));
		#}	
		$element =~ s/_CHAIN//g;
		#if (($colCount != 1) && ($colCount != 4) ) {
		#print "$element"; 
		ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
		#}
		$colCount++;
	    }
	    if ($_ =~ m/^Job Id/) {  
		print "<br><hr>"; 
	    }	
	    EndDIV();
	    #print "<br>";	
	}
	print "<br>";	
	print "<br>";	

	### RIPE RUNNING
	#my @RipeheaderSizes = ("10","15","25","7","15","10","10");
	ClosedDIV("class","$riperunLast[0]","RIPE EXECUTING $riperunLast[1]");
	#my @lineElements = ("Sched ID","Cust Code","Product Name","System","Step","Start Time","Last Time");
	my $inHungProc = "FALSE";
	foreach my $RipeLine (@RipeRuns) {
	    if (($RipeLine =~ m/POSSIBLE HUNG PROCESSES/) || ($inHungProc eq "TRUE"))  {
		$inHungProc = "TRUE";
		next;
	    } 
	    my $colCount = 0;
	    my $schedID = substr($RipeLine,1,9);
	    #my $prodID = substr($RipeLine,25,9);
	    my $cuscode = substr($RipeLine,10,10);
	    my $prodName = substr($RipeLine,19,21);
	    #my $notes = substr($RipeLine,85,14);
	    my $system = substr($RipeLine,51,8);
	    my $status = substr($RipeLine,69,10);
	    my $step = substr($RipeLine,91,9);
	    #my $StartTime = substr($RipeLine,125,17);
	    my $startTime = substr($RipeLine,103,16);
	    my $EndTime = substr($RipeLine,123,16);
	    #my $DueTime = substr($RipeLine,161,4);
	    my @startdateTime = split(' ',$startTime);
	    my $StartscreenDate = $startdateTime[0];
	    my $StartscreenTime = substr($startdateTime[1],0,5);
	    
	    my @dateTime = split(' ',$EndTime);
	    my $screenDate = $dateTime[0];
	    my $screenTime = substr($dateTime[1],0,5);
	    #my $notes = lc($notes);
	    if (($schedID !~ m/\d/) && ($RipeLine !~ m/row aff/)){
		next;
	    }	
	    if (($system =~ m/qaripe/) || ($system =~ m/regripe/)) {
		next;
	    }
	    
	    if ($status =~ m/Process/) {
		my @lineElements = ($cuscode,$prodName,$system,$step,"$StartscreenTime to $screenTime",$schedID);
		OpenDIV("class","ApoRow","");
		foreach my $element (@lineElements) {
		    ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
		    $colCount++;
		}
		EndDIV();
	    }
	}
	

    }
}
EndDIV();

#my $AVtot = 0;
#my $RipeFailTot = 0;
#my $CronacleFailTot = 0;

if (($screenMode ne "BIG") && ($pageType ne "runs")) {
    #Begin building content area based on any filters applied
    OpenDIV("ID","Sidebar");
    my $AVstat = "Good";
    my $Ripestat = "Good";
    my $Cronstat = "Good";

    ClosedDIV("class","SidebarTitle","Stats");
    if ($AVtot > 0) { $AVstat = "Bad";}
    if ($RipeFailTot > 0) { $Ripestat = "Bad";}
    if ($CronacleFailTot > 0) { $Cronstat = "Bad";}	
    OpenDIV("class","SidebarGroup$AVstat","Late to Client - $AVtot");
    EndDIV();
    OpenDIV("class","SidebarGroup$Ripestat","Ripe Fail - $RipeFailTot");
    EndDIV();
    OpenDIV("class","SidebarGroup$Cronstat","Cronacle Fails - $CronacleFailTot");
    EndDIV();
    OpenDIV("class","SidebarGroup$Cronstat","Turbo Fails - $script_FailTot");
    EndDIV();

    EndDIV();
}


EndDIV();
HTMLend();

sub TurboProd {
    my $script_FailTot = 0;
    my @ignore_X2 = ("TURBOX2_MAC3","TURBOX2_MAC4","TURBOX2_MAC5","TURBOX2_MAC6","TURBOX2_MAC7","TURBOX2_MAC8","TURBOX2_MAC9");
    my @ignore_adgen = ("TURBOX6ADGEN_MAC3","TURBOX6ADGEN_MAC4");
    my @ignore_x6 = ("TURBOX6_MAC12");
    my @ignore_xq = ("TURBOXQ_MAC4");
    my @ignore_x = ("TURBOX_MAC3","TURBOX_MAC5");
    my @ignore_queues = (@ignore_X2,@ignore_adgen,@ignore_x6,@ignore_xq,@ignore_x);
    my @HeaderNames = ("Customer","Script Name","Listing Date","Status","Due","Job");
    my @headerSizes = ("25","25","12","12","12","7","12","10");
    my $colCount = 0;
    OpenDIV("class","ApoHeader","");				
    foreach my $element (@HeaderNames) {
	ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
	$colCount++;
    }
    EndDIV();
    my $snapshot = "/Library/WebServer/Becky/snapshot9.txt";
    my @snapLast = checkReportAge($snapshot);
    #ClosedDIV("class","$snapLast[0]","AV MONITOR $snapLast[1]");
    tie my @records, 'Tie::File', $snapshot;
    my $fullFile = join "\n",@records;
    untie @records;
    $fullFile =~ s/\s+/ /g;
    $fullFile =~ s/ Generic/\nGeneric/g;
    $fullFile =~ s/Batch/\nBatch/g;
    $fullFile =~ s/Entry Jobname Username Status ----- ------- -------- ------/ /g;
    $fullFile =~ s/Completed \d\d-\w\w\w-\d\d\d\d \d\d:\d\d:\d\d.\d\d on queue \w //g;
    $fullFile =~ s/Completed \d\d-\w\w\w-\d\d\d\d \d\d:\d\d:\d\d.\d\d on queue VERIFY_NORM //g;
    $fullFile =~ s/.COM\;\d+/.COM\n/g;
    $fullFile =~ s/\(executing\)//g;
    $fullFile =~ s/Logical(.*)\n/\n/g;
    $fullFile =~ s/Printer(.*)\n/\n/g;
    $fullFile =~ s/\/RETAIN=ERROR\s\s\s/\/RETAIN=ERROR\n/g;
    $fullFile =~ s/\)\s\s\s/\)\n/g;
    $fullFile =~ s/\n\s+/\n/g;
    $fullFile =~ s/\/BASE_PRIORITY=\d\s//g;
    $fullFile =~ s/\/OWNER=\[\d,\d\]//g;
    $fullFile =~ s/\/PROTECTION=((.*))//g;
    #open FH,">/PerlTemp/newsnapshot.txt";
    #print FH $fullFile;
    #close FH;
    my @allLines = split("\n",$fullFile);
    my $queu_tracker;
    foreach (@allLines) {

	if ($_ =~ /^Generic batch queue TURBO/) {
	    #print "found generic queue \n $_\n";
	    my $find_generic = /queue\s(.*)\s\//;
	    my $GenQ_name = $1;
	    ClosedDIV("class","CategoryHeader","$GenQ_name");
	    #print "$GenQ_name<br>";
	    my $found_gen = "FALSE";
	    foreach my $getQ (@allLines) {
		if ($getQ =~ /^Generic batch queue $GenQ_name/) {
		    $found_gen = "TRUE";
		    next;
		}
		if (($found_gen eq "TRUE") && ($getQ =~ /^\d/)) {
		    #my @batch_job = split(' ',$getQ);
		    #print "$find_queue<br>";
		    my @job_parts = split(' ',$getQ);
		    my $job_num = $job_parts[0];
		    #my $scriptName = $job_parts[1];
		    my $script_status = $job_parts[3];
		    #if ($script_status eq "Holding") {
		    #	next; 
		    #}
		    my $params = $getQ;
		    $params =~ s/\s//g; 
		    $params =~ /PARAM\=(.*)\/PRIORITY/;
		    my $these_params = $1;
		    $these_params =~ s/\(//g;
		    $these_params =~ s/\)//g;
		    $these_params =~ s/\"//g;
		    my @allParams = split(',',$these_params);
		    my $scriptName = $allParams[0];
		    my $listdate = 	$allParams[1];		
		    my $CID = $allParams[3];
		    my $Status = $allParams[4];
		    my @custMaster = findCustomer($CID);
		    my $custName = $custMaster[1];
		    my $deptName = $custMaster[2];
		    if ($scriptName =~ /ADGEN/) {
			$Status = "ADGEN";
		    }
		    my $FullName = substr("$CID - $custName",0,25);
		    my @ScriptCOls = ($FullName,$scriptName,$listdate,$script_status,$Status,$job_num);
		    my $colCount = 0;
		    if ($script_status =~ /Pending/) {
			OpenDIV("class","ApoRowWarn","");
		    } elsif  ($script_status eq "Holding") {
			OpenDIV("class","APHolding","");							
		    } else  {
			OpenDIV("class","ApoRow","");
		    }
		    foreach my $element (@ScriptCOls) {
			ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
			$colCount++;
		    }
		    EndDIV();						
		    #	print "\t$getQ <br>";
		    next;
		}
		if (($found_gen eq "TRUE") && ($getQ !~ /^\d/)) {
		    last;
		}
	    }
	    my @Gen_que_parts = split('\s',$_);
	    my $this_GQ = $Gen_que_parts[3];
	    #print "$this_GQ\n";
	    my @find_batch_que = split('/GENERIC=');
	    my @Batch_q_list = split(',',$find_batch_que[1]);

	    foreach my $this_BQ (@Batch_q_list) {
		$this_BQ =~ s/\(|\)//g;		
		$this_BQ =~ s/\s//g;	
		$queu_tracker = "FALSE";
		#print "\t Looking for -$this_BQ-\n";
		foreach my $find_queue (@allLines) {
		    my @batch_q_parts = split(',',$find_queue);
		    #print "Looking at $batch_q_parts[0]\n";
		    if (($queu_tracker eq "FALSE") && ($find_queue =~ /^Batch queue $this_BQ/m)) {
			my $bq_status = $batch_q_parts[1];
			my @batch_name_parts = split(' ',$batch_q_parts[0]);
			my $batch_name = $batch_name_parts[2];
			if ($batch_name ~~ @ignore_queues) {
			    $queu_tracker = "TRUE";
			    next;				 		
			} elsif ($bq_status =~ m/stopped/) {
			    ClosedDIV("class","CategoryHeaderAlert","$batch_name is STOPPED");
			}
			$queu_tracker = "TRUE";
			next;				 
		    } elsif (($queu_tracker eq "TRUE") && ($find_queue =~ /^(Gen|Bat)/m)){
			$queu_tracker = "FALSE";
			#print "End of $this_BQ\n";
			next;
		    } elsif (($queu_tracker eq "TRUE") && ($find_queue =~ /^\d/m)) {
			my @batch_job = split(' ',$find_queue);
			#print "$find_queue<br>";
			my @job_parts = split(' ',$find_queue);
			my $job_num = $job_parts[0];
			#my $scriptName = $job_parts[1];
			my $script_status = $job_parts[3];
			my $params = $find_queue;
			$params =~ s/\s//g; 
			$params =~ /PARAM\=(.*)\/PRIORITY/;
			my $these_params = $1;
			$these_params =~ s/\(//g;
			$these_params =~ s/\)//g;
			$these_params =~ s/\"//g;
			my @allParams = split(',',$these_params);
			my $scriptName = $allParams[0];
			my $listdate = 	$allParams[1];		
			my $CID = $allParams[3];
			my $Status = $allParams[4];
			my @custMaster = findCustomer($CID);
			if ($scriptName =~ /ADGEN/) {
			    $Status = "ADGEN";
			}
			my $custName = $custMaster[1];
			my $deptName = $custMaster[2];
			my $FullName = substr("$CID - $custName",0,25);
			my @queParts = split('_',$this_BQ);
			my $queuShort = $queParts[1];
			my @ScriptCOls = ($FullName,$scriptName,$listdate,"On $queuShort",$Status,$job_num);
			my $colCount = 0;
			if ($script_status =~ /Pending/) {
			    OpenDIV("class","ApoRowWarn","");
			} else {
			    OpenDIV("class","ApoRow","");
			}
			foreach my $element (@ScriptCOls) {
			    ClosedDIV("class","ApoCol$headerSizes[$colCount]","$element");
			    $colCount++;
			}
			EndDIV();						
			
		    }
		} #	foreach my $find_queue (@allLines) {

	    }#	foreach my $this_BQ (@Batch_q_list) {

	}
    }
}



sub allBeckyQueuesII {

    my $justStats = "FALSE";
    if ($_[0] eq "stat") {
	$justStats = "TRUE";	
    }
    my @allbatch_queues;
    my $Questopped = 0;
    my $ExecTot = 0;
    my $PendTot = 0;
    my $HoldTot = 0;
    my $FailTot = 0;
    my @allJobs;
    my @ignore_X2 = ("TURBOX2_MAC3","TURBOX2_MAC4","TURBOX2_MAC5","TURBOX2_MAC6","TURBOX2_MAC7","TURBOX2_MAC8","TURBOX2_MAC9");
    my @ignore_adgen = ("TURBOX6ADGEN_MAC3","TURBOX6ADGEN_MAC4");
    my @ignore_x6 = ("TURBOX6_MACD","TURBOX6_MAC12");
    my @ignore_xq = ("TURBOXQ_MAC4","TURBOXQ_MAC3");
    my @ignore_x = ("TURBOX_MAC3","TURBOX_MAC4","TURBOX_MAC5");
    my @ignore_alpha = ("EDDIE_ELEC_EXT","XXX","ZIP9");
    my @ignore_queues = (@ignore_X2,@ignore_adgen,@ignore_x6,@ignore_xq,@ignore_x,@ignore_alpha);
    my @ignore_generic = ("GENERIC_SAMPLES_EXT");
    my @HeaderNames = ("Customer","Script Name","Listing Date","Status","Due","Job");
    my @headerSizes = ("25","25","12","12","12","7","12","10");
    my $colCount = 0;

    my $snapshot = "/Library/WebServer/Becky/snapshot9.txt";
    my @snapLast = checkReportAge($snapshot);
    #ClosedDIV("class","$snapLast[0]","AV MONITOR $snapLast[1]");	
    tie my @records, 'Tie::File', $snapshot;
    my $fullFile = join "\n",@records;
    untie @records;
    $fullFile =~ s/\s+/ /g;
    $fullFile =~ s/ Generic/\nGeneric/g;
    $fullFile =~ s/Batch/\nBatch/g;
    $fullFile =~ s/Entry Jobname Username Status ----- ------- -------- ------/ /g;
    #$fullFile =~ s/Completed \d-\w\w\w-\d\d\d\d \d\d:\d\d:\d\d.\d\d on queue VERIFY_NORM //g;
    #Completed 7-DEC-2016 14:58:48.13 on queue VERIFY_BECKY
    
    $fullFile =~ s/on\squeue\sVERIFY_NORM\s/on\squeue\sVERIFY_NORM\n/g;
    $fullFile =~ s/on\squeue\sVERIFY_BECKY\s/on\squeue\sVERIFY_BECKY\n/g;
    #$fullFile =~ s/.COM\;\d+/.COM\n/g;
    $fullFile =~ s/\(executing\)//g;
    $fullFile =~ s/Logical(.*)\n/\n/g;
    $fullFile =~ s/Printer(.*)\n/\n/g;
    $fullFile =~ s/\/RETAIN=ERROR\s\s\s/\/RETAIN=ERROR\n/g;
    $fullFile =~ s/\)\s\s\s/\)\n/g;
    $fullFile =~ s/\n\s+/\n/g;
    $fullFile =~ s/\/BASE_PRIORITY=\d\s//g;
    $fullFile =~ s/\/OWNER=\[\d,\d\]//g;
    $fullFile =~ s/\/PROTECTION=((.*))//g;
    $fullFile =~ s/Completed \d-\w-\d\d\d\d \d\d:\d\d:\d\d\.\d\d on queue VERIFY_BECKY //g;
    #	$fullFile =~ s/.COM\s\d/.COM\n\d/g;
    open FH,">/PerlTemp/newsnapshot.txt";
    print FH $fullFile;
    close FH;
    my @allLines = split("\n",$fullFile);
    my $queu_tracker;
    my $now_queue;
    my @found_batchQs;
    foreach my $list_batch_w_generic (@allLines) {
	if ($list_batch_w_generic =~ /^Generic batch queue/) {
	    my @makebatchlist = split('/GENERIC=',$list_batch_w_generic);
	    my @Batch_track_list = split(',',$makebatchlist[1]);
	    foreach my $clean_Q (@Batch_track_list) {
		$clean_Q =~ s/\(|\)//g;		
		$clean_Q =~ s/\s//g;	
		@found_batchQs = (@found_batchQs,$clean_Q);		
	    }
	}
    }
    #print join " ",@found_batchQs;
    foreach (@allLines) {
	if ($_ =~ /^Generic batch queue/) {
	    if ($_ ~~ @ignore_generic) {
		next; }
	    #print "found generic queue \n $_\n";
	    my $find_generic = /queue\s(.*)\s\//;
	    my $GenQ_name = $1;
	    $now_queue = $GenQ_name;
	    my @Gen_que_parts = split('\s',$_);
	    my $this_GQ = $Gen_que_parts[3];
	    #print "$this_GQ\n";
	    my @find_batch_que = split('/GENERIC=');
	    my @Batch_q_list = split(',',$find_batch_que[1]);
	    my $recordThis = "GenQue|$now_queue|@Batch_q_list";
	    @allJobs = (@allJobs,$recordThis);

	    
	    ###
	} elsif ($_ =~ /^Batch queue/) {
	    my @batch_q_parts = split(',',$_);
	    my $bq_status = $batch_q_parts[1];
	    my @batch_name_parts = split(' ',$batch_q_parts[0]);
	    my $batch_name = $batch_name_parts[2];
	    $now_queue = $batch_name;
	    if ($batch_name ~~ @found_batchQs) { next; }
	    my $find_limit = $_;
	    my $find_limit = /JOB_LIMIT\=(.*)\s/;
	    my $job_limit = $1;
	    if ($job_limit =~ /\//g) {
		my @limit_parts = split('\s',$job_limit);
		$job_limit = $limit_parts[0];
	    }
	    $now_queue = $batch_name;
	    if ($batch_name ~~ @ignore_queues) {
		next;	
	    } else {
		my $recordThis = "BatchQue|$now_queue|$bq_status|Job Limit = $job_limit";
		@allJobs = (@allJobs,$recordThis);						
		$Questopped++;
	    }
	} elsif ($_ =~ /^\d/) {
	    my $job_state;
	    my $these_params;
	    my @job_parts = split(' ',$_);
	    my $job_num = $job_parts[0];
	    my $job_name = substr($job_parts[1],0,19);
	    my $script_status = $job_parts[3];
	    my $params = $_;
	    if ($_ =~ m/\/PARAM/) {
		$params =~ s/\s//g; 
		$params =~ /PARAM\=(.*)\/PRIORITY/;
		$these_params = $1;
		$these_params =~ s/\(//g;
		$these_params =~ s/\)//g;
		$these_params =~ s/\"//g;
	    } else {
		$these_params = "NO PARAMS";
	    }
	    if ($script_status =~ /Pending/) {
		$job_state = "Pending";
		#	OpenDIV("class","ApoRowWarn","");
		$PendTot++;
	    } elsif  ($script_status eq "Holding") {
		$job_state = "Holding";
		$HoldTot;
	    } elsif  ($script_status =~ "Retain") {
		$job_state = "Holding";
		$FailTot++;						
	    } else  {
		$job_state = "Executing";
		$ExecTot++;						
	    }
	    my $recordThis = "JOB|$script_status|$now_queue|$job_num|$job_name|$these_params";
	    #my $recordThis = "JOB|$this_BQ|$script_status|$job_num|$job_name|$these_params";
	    @allJobs = (@allJobs,$recordThis);
	    next;				
	    
	}
    } #	foreach (@allLines) {

    return(@allJobs);
}

sub allBeckyQueues {

    my $justStats = "FALSE";
    if ($_[0] eq "stat") {
	$justStats = "TRUE";	
    }
    my @allbatch_queues;
    my $Questopped = 0;
    my $ExecTot = 0;
    my $PendTot = 0;
    my $HoldTot = 0;
    my $FailTot = 0;
    my @allJobs;
    my @ignore_X2 = ("TURBOX2_MAC3","TURBOX2_MAC4","TURBOX2_MAC5","TURBOX2_MAC6","TURBOX2_MAC7","TURBOX2_MAC8","TURBOX2_MAC9");
    my @ignore_adgen = ("TURBOX6ADGEN_MAC3","TURBOX6ADGEN_MAC4");
    my @ignore_x6 = ("TURBOX6_MACD","TURBOX6_MAC12");
    my @ignore_xq = ("TURBOXQ_MAC4","TURBOXQ_MAC3");
    my @ignore_x = ("TURBOX_MAC3","TURBOX_MAC4","TURBOX_MAC5");
    my @ignore_alpha = ("EDDIE_ELEC_EXT","XXX","ZIP9","RIPE_EXT_DEVRIPE10");
    my @ignore_queues = (@ignore_X2,@ignore_adgen,@ignore_x6,@ignore_xq,@ignore_x,@ignore_alpha);
    my @ignore_generic = ("GENERIC_SAMPLES_EXT");
    my @HeaderNames = ("Customer","Script Name","Listing Date","Status","Due","Job");
    my @headerSizes = ("25","25","12","12","12","7","12","10");
    my $colCount = 0;

    my $snapshot = "/Library/WebServer/Becky/snapshot9.txt";
    my @snapLast = checkReportAge($snapshot);
    #ClosedDIV("class","$snapLast[0]","AV MONITOR $snapLast[1]");	
    tie my @records, 'Tie::File', $snapshot;
    my $fullFile = join "\n",@records;
    untie @records;
    $fullFile =~ s/\s+/ /g;
    $fullFile =~ s/ Generic/\nGeneric/g;
    $fullFile =~ s/Batch/\nBatch/g;
    $fullFile =~ s/Entry Jobname Username Status ----- ------- -------- ------/ /g;
    #	$fullFile =~ s/Completed \d\d-\w\w\w-\d\d\d\d \d\d:\d\d:\d\d.\d\d on queue \w //g;
    #$fullFile =~ s/Completed \d\d-\w\w\w-\d\d\d\d \d\d:\d\d:\d\d.\d\d on queue VERIFY_BECKY //g;
    #$fullFile =~ s/Completed \d\d-\w\w\w-\d\d\d\d \d\d:\d\d:\d\d.\d\d on queue VERIFY_NORM //g;
    $fullFile =~ s/.COM\;\d+/.COM\n/g;
    $fullFile =~ s/.COM\nCompleted/.COM\sCompleted/g;
    $fullFile =~ s/\(executing\)//g;
    $fullFile =~ s/Logical(.*)\n/\n/g;
    $fullFile =~ s/Printer(.*)\n/\n/g;
    $fullFile =~ s/\/RETAIN=ERROR\s\s\s/\/RETAIN=ERROR\n/g;
    $fullFile =~ s/\)\s\s\s/\)\n/g;
    $fullFile =~ s/\n\s+/\n/g;
    $fullFile =~ s/\/BASE_PRIORITY=\d\s//g;
    $fullFile =~ s/\/OWNER=\[\d,\d\]//g;
    $fullFile =~ s/\/PROTECTION=((.*))//g;
    #	$fullFile =~ s/.COM\s\d/.COM\n\d/g;
    #open FH,">/PerlTemp/newsnapshot.txt";
    #print FH $fullFile;
    #close FH;
    my @allLines = split("\n",$fullFile);
    my $queu_tracker;
    my $now_queue;
    my @found_batchQs;
    foreach my $list_batch_w_generic (@allLines) {
	if ($list_batch_w_generic =~ /^Generic batch queue/) {
	    my @makebatchlist = split('/GENERIC=',$list_batch_w_generic);
	    my @Batch_track_list = split(',',$makebatchlist[1]);
	    foreach my $clean_Q (@Batch_track_list) {
		$clean_Q =~ s/\(|\)//g;		
		$clean_Q =~ s/\s//g;	
		@found_batchQs = (@found_batchQs,$clean_Q);		
	    }
	}
    }
    #print join " ",@found_batchQs;
    foreach (@allLines) {
	if ($_ =~ /^Generic batch queue/) {
	    if ($_ ~~ @ignore_generic) {
		next; }
	    #print "found generic queue \n $_\n";
	    my $find_generic = /queue\s(.*)\s\//;
	    my $GenQ_name = $1;
	    $now_queue = $GenQ_name;
	    my @Gen_que_parts = split('\s',$_);
	    my $this_GQ = $Gen_que_parts[3];
	    #print "$this_GQ\n";
	    my @find_batch_que = split('/GENERIC=');
	    my @Batch_q_list = split(',',$find_batch_que[1]);
	    my $recordThis = "GenQue|$now_queue|@Batch_q_list";
	    @allJobs = (@allJobs,$recordThis);
	    ###Try to get Generic's batch queue. 
	    foreach my $this_BQ (@Batch_q_list) {
		$this_BQ =~ s/\(|\)//g;		
		$this_BQ =~ s/\s//g;	
		$queu_tracker = "FALSE";
		#print "\t Looking for -$this_BQ-\n";
		foreach my $find_queue (@allLines) {
		    my @batch_q_parts = split(',',$find_queue);
		    #print "Looking at $batch_q_parts[0]\n";
		    if (($queu_tracker eq "FALSE") && ($find_queue =~ /^Batch queue $this_BQ/m)) {
			my $bq_status = $batch_q_parts[1];
			my @batch_name_parts = split(' ',$batch_q_parts[0]);
			my $batch_name = $batch_name_parts[2];
			#@found_batchQs = (@found_batchQs,$batch_name);
			if ($batch_name ~~ @ignore_queues) {
			    $queu_tracker = "TRUE";
			    next;				 		
			} else {
			    my $recordThis = "BatchQue|$this_BQ|$bq_status";
			    @allJobs = (@allJobs,$recordThis);						
			    $Questopped++;
			}
			$queu_tracker = "TRUE";
			next;				 
		    } elsif (($queu_tracker eq "TRUE") && ($find_queue =~ /^(Gen|Bat)/m)){
			$queu_tracker = "FALSE";
			#print "End of $this_BQ\n";
			next;
		    } elsif (($queu_tracker eq "TRUE") && ($find_queue =~ /^\d/)) {
			my $job_state;
			my $these_params;
			my @batch_job = split(' ',$find_queue);
			#print "$find_queue<br>";
			my @job_parts = split(' ',$find_queue);
			my $job_num = $job_parts[0];
			my $job_name = $job_parts[1];
			#my $scriptName = $job_parts[1];
			my $script_status = $job_parts[3];
			my $params = $find_queue;
			if ($params =~ m/\/PARAM\=/g) {
			    $params =~ s/\s//g; 
			    $params =~ /PARAM\=(.*)\/PRIORITY/;
			    my $these_params = $1;
			    $these_params =~ s/\(//g;
			    $these_params =~ s/\)//g;
			    $these_params =~ s/\"//g;
			} else {
			    my $these_params = "NO PARAMS";
			}
			#my @ScriptCOls = ($FullName,$scriptName,$listdate,"On $queuShort",$Status,$job_num);
			if ($script_status =~ /Pending/) {
			    $job_state = "Pending";
			    #	OpenDIV("class","ApoRowWarn","");
			    $PendTot++;
			} elsif  ($script_status eq "Holding") {
			    $job_state = "Holding";
			    $HoldTot;
			} elsif  ($script_status =~ "Retain") {
			    $job_state = "Holding";
			    $FailTot++;						
			} else  {
			    $job_state = "Executing";
			    $ExecTot++;						
			}
			my $recordThis = "JOB|$script_status|$this_BQ|$job_num|$job_name|$these_params";
			@allJobs = (@allJobs,$recordThis);			
		    } #if (($queu_tracker eq "FALSE") && ($find_queue =~ /^Batch queue $this_BQ/m))
		} #	foreach my $find_queue (@allLines) {

	    }#	foreach my $this_BQ (@Batch_q_list) {
	    
	    ###
	} elsif ($_ =~ /^Batch queue/) {
	    my @batch_q_parts = split(',',$_);
	    my $bq_status = $batch_q_parts[1];
	    my @batch_name_parts = split(' ',$batch_q_parts[0]);
	    my $batch_name = $batch_name_parts[2];
	    $now_queue = $batch_name;
	    if ($batch_name ~~ @found_batchQs) { next; }
	    my $find_limit = $_;
	    my $find_limit = /JOB_LIMIT\=(.*)\s/;
	    my $job_limit = $1;
	    if ($job_limit =~ /\//g) {
		my @limit_parts = split('\s',$job_limit);
		$job_limit = $limit_parts[0];
	    }
	    $now_queue = $batch_name;
	    if ($batch_name ~~ @ignore_queues) {
		next;	
	    } elsif ($batch_name ~~ @found_batchQs)	 {
		next;	 		
	    } else {
		my $recordThis = "BatchQue|$now_queue|$bq_status|Job Limit = $job_limit";
		@allJobs = (@allJobs,$recordThis);						
		$Questopped++;
	    }
	} elsif ($_ =~ /^\d/) {
	    my $job_state;
	    my $these_params;
	    my @job_parts = split(' ',$_);
	    my $job_num = $job_parts[0];
	    my $job_name = substr($job_parts[1],0,19);
	    my $script_status = $job_parts[3];
	    my $params = $_;
	    if ($_ =~ m/\/PARAM/) {
		$params =~ s/\s//g; 
		$params =~ /PARAM\=(.*)\/PRIORITY/;
		$these_params = $1;
		$these_params =~ s/\(//g;
		$these_params =~ s/\)//g;
		$these_params =~ s/\"//g;
	    } else {
		$these_params = "NO PARAMS";
	    }
	    if ($script_status =~ /Pending/) {
		$job_state = "Pending";
		#	OpenDIV("class","ApoRowWarn","");
		$PendTot++;
	    } elsif  ($script_status eq "Holding") {
		$job_state = "Holding";
		$HoldTot;
	    } elsif  ($script_status =~ "Retain") {
		$job_state = "Holding";
		$FailTot++;						
	    } else  {
		$job_state = "Executing";
		$ExecTot++;						
	    }
	    my $recordThis = "JOB|$script_status|$now_queue|$job_num|$job_name|$these_params";
	    #my $recordThis = "JOB|$this_BQ|$script_status|$job_num|$job_name|$these_params";
	    @allJobs = (@allJobs,$recordThis);
	    next;				
	    
	}
    } #	foreach (@allLines) {

    return(@allJobs);
}
