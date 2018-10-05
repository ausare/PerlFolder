#!/Users/scripting/perl5/perlbrew/perls/perl-5.24.0/bin/Perl
## Larry Gonyea TMS 8/6/2013
### FF_mover basically moves files around to the various directories based on the cgi parameters.
### See what actions happen in the comments below to see where certain actions happen.
 
#use warnings;
use strict;
use Tie::File;
use File::Copy;
use CGI;
use File::Find;
use URI::Escape;
require("FF_common_func.cgi");
require("FF_web_elements.cgi");
my ($baseFEfolder,$FeatFolder) = getFilesLocal();
my ($homeIP,$systemType) = getHomeAddress();
my $homeDir = "$FeatFolder/";

my $hasPhotos;
my $CanCopy;
my @copyNameSP;
my $copyTmp;
my $copyFile;
my $date;
my $featPreview;
my $sidebarfile;
my $completeAction;
my @errorList = "";

my $query = new CGI;
my $thistmp = $query->param('tmp');
my $thisfile = $query->param('fileLoc');
my $newstatParam = $query->param('newstate');
my $oldstate = $query->param('oldstate');
my $thisstory = $query->param('story');
my $actionDo = $query->param('actionDo');
my $prevFilter = $query->param('backlink');


my $sidebarName = $thisstory;
my $sidebarfile = $thisfile;
my $refiltered = "FALSE";
my $RecycleThis = "FALSE";
my $problemsFound = "False";

# Split apart the given filename and use the pieces from the directory to assign strings.
my @fileparts = split('/',$thisfile);
my $filename = $fileparts[6];
my $tempOrDate = $fileparts[4];
my $process_time = 10;

my @storyparts = split('\.',$filename);
my $featName = $storyparts[0];

my $specFile = "$baseFEfolder/specs/$featName.spc";

if (($oldstate eq "filtered") && ($newstatParam eq "filtered")) {
	my $refiltered = "TRUE";
	my $refilterText = $query->param('refiltext');
}

# Check the file's directory and determine if the path was Temp or a date. If this was in the Temp directory, the date will be gotten from the filename
if ($tempOrDate eq "Temp") {
	$date = $storyparts[1];
} else {
	$date = $fileparts[4];
}

# Used to determine if feature is to be deleted. 
if ($oldstate eq "trash") {
 my $newstatParam = "trash";
}

#Get variables from the spec file to determine environmental specs
my %GetFeatSpecs = hashAFile($specFile);
my $checkCopy = $GetFeatSpecs{'copy'};
my $checkRecycle = $GetFeatSpecs{'recycle'};
my $checkTest = $GetFeatSpecs{'status'};
my $checkPhotos = $GetFeatSpecs{'photo'};

if ($checkPhotos ne "") {
	$hasPhotos = "TRUE";
} else { 
	$hasPhotos = "FALSE"; 
}

if ($checkTest eq "live") {
	$checkTest = "LIVE";
} else {
	$checkTest = "TEST";
}

if ($systemType eq "Development") {
	$checkTest = "TEST";
}
if ($checkRecycle eq "Yes") {
 $checkRecycle = "TRUE";
} else {
 $checkRecycle = "FALSE"; 
}

if ($checkCopy ne "copy") {
my $CanCopy = "TRUE";
} else {
my $CanCopy = "FALSE"; 
}

# If this is being copied from another feature, the template will be the new feature
if ($newstatParam eq "copy") {
	@copyNameSP = split('\.',$thisstory);
	$copyTmp = "$baseFEfolder/templates/$copyNameSP[0].tmp";
	$copyFile = "$FeatFolder/$date/In Progress/$thisstory";
}

## establish base directories.
my $histDir = "$FeatFolder/History/$date/$newstatParam/$filename"; #where file will go for back up.
my $RecycleDir = "$FeatFolder/Recycle/$filename"; #where file will go for back up.
my $filterfeat = "$FeatFolder/$date/Posted/$filename"; #where filtered version will go while having an html version still in the Posted folder.
my $tempFeat = "$FeatFolder/$date/TEMP/${featName}${date}.txt";#temporary txt file for downloading packages);
my $newfeat = "$FeatFolder/$date/$newstatParam/$filename"; #where new feature will go when saved.
if ($newstatParam eq "reset") {
	my $newfeat = "$FeatFolder/$date/$oldstate/$filename"; #where new feature will go when saved.
} 

makeHTML5type();
LoadCSS();
LoadJS();
JQfadeIn("#Content","slow");
HTMLtitle("Gracenote Feature Writer $systemType");
OpenDIV("ID","Header");
makeHeaderTopper();
ClosedDIV("class","HeaderLeft","<b>$filename</b></br>");
EndDIV();

OpenDIV("ID","Nav");
## Create the navigation bar links.
OpenDIV("class","NavLeft",);
	print "<nav>\n";
	print "	<ul>\n";
	print "	<li><a href=\"http://$homeIP/cgi-bin/FE2/featuremanager.cgi\">Return to Main Page</a>\n";
if (($newstatParam eq "reset") || ($oldstate eq "reset")) { 
	my @dirParts = split('/',$thisfile);
	my $stepPart = $dirParts[5];
	my @storyparts = split('\.',$thisstory);
	my $dateFolder = $storyparts[1];
	my $moveToFile = "$FeatFolder/$dateFolder/$stepPart/$thisstory";
		print "	<li><a href=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi?tmp=$thistmp&fileLoc=$moveToFile&status=$stepPart&story=$filename&viewtype=Edit\">Edit $filename again</a>\n";		
		if ($hasPhotos eq "TRUE") {
		print "	<li><a href=\"http://$homeIP/cgi-bin/FE2/featurePhotos.cgi?tmp=$specFile&fileLoc=$date&status=$stepPart&story=$filename&viewtype=Edit\">Manage $filename Photos</a>\n";
	}
} else {
		if ($newstatParam eq "copy") {
			print "	<li><a href=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi?tmp=$copyTmp&fileLoc=$copyFile&status=In Progress&story=$thisstory&viewtype=Edit\">Edit $thisstory</a>\n";
		} else {
			print "	<li><a href=\"http://$homeIP/cgi-bin/FE2/feature_editor.cgi?tmp=$thistmp&fileLoc=$newfeat&status=$newstatParam&story=$filename&viewtype=Edit\">Edit $filename again</a>\n";
		}
		if ($hasPhotos eq "TRUE") {
		print "	<li><a href=\"http://$homeIP/cgi-bin/FE2/featurePhotos.cgi?tmp=$specFile&fileLoc=$date&status=$newstatParam&story=$filename&viewtype=Edit\">Manage $filename Photos</a>\n";
	}
}

	print "	</ul>\n";
	print "</nav>\n";
EndDIV();

EndDIV();

OpenDIV("ID","Container");

OpenDIV("ID","Content");

## if reset was passed, in both old and new states, this is a new feature that hasn't been written to yet.

if (($newstatParam eq "reset") && ($oldstate eq "reset")) { 

	my $moveFromFile = $thisfile;
	my @dirParts = split('/',$thisfile);
	my $stepPart = $dirParts[5];
	my @storyparts = split('\.',$thisstory);
	my $dateFolder = $storyparts[1];
	my $moveToFile = "$FeatFolder/$dateFolder/$stepPart/$thisstory";
	my $sidebarfile = "$moveToFile";
	move($moveFromFile,$moveToFile);
	$completeAction = "$filename has been reset and can be Edited again.";
	ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");
	OpenDIV("ID","Sidebar");
	MakeASideBar($thistmp,$moveToFile,$featName,"view");

# The copy function works by getting the tags for the feature to be copied to and pulling the information from the same
#      tag names in the feature being copied from. These name fields need to match, or the copied to feature will not pull correctly. 
} elsif ($newstatParam eq "copy") {
	makeadir($date,"In Progress");
	my $record;
	my $Tagged;
	my $lineToCopy;
	my %oldFeatHash;
	my $CGIlist;
	open FH, "<", $thisfile; #Get existing feature and put all together to grab text between name tags
	my @records = <FH>;
	my $allrecords = join "", @records;	
	close FH;
	my @cgiListNames = getTmpNameList($thistmp);
		foreach $CGIlist (@cgiListNames) {
			if (($CGIlist eq "EP") || ($CGIlist eq "Hidden") || ($CGIlist eq "EOF")) { 
				#Do nothing. Don't want these.
			} else {
				$allrecords =~ /\<$CGIlist\>(.*)\<\/$CGIlist\>/; 
				$record = $1;
				chomp($record);
				#print "$CGIlist record is: $record<br>";
				$oldFeatHash{$CGIlist} = $record;
			}
		}

	open CF, ">", $copyFile; #Get existing feature and put all together to grab text between name tags
	my @copyTags = getTmpNameList($copyTmp);
		foreach $Tagged (@copyTags) {
			$lineToCopy = $oldFeatHash{$Tagged};
			if ($Tagged eq "Name") {
				print CF "<Name>$thisstory</Name>\n";
			} else {
				## ADD CPSTYLE here. When features for Toronto are copied, we convert know words to CPstyle. 
				##		
				if ($thisstory =~ /^tor/) {
				#$lineToCopy = convertToCPStyle($lineToCopy);
				$lineToCopy = runFilter("cpstyle",$lineToCopy);
			}
				print CF "<$Tagged>$lineToCopy</$Tagged>\n";
			}
		}
	close CF;
	#copy($thisfile,$copyFile)
	$completeAction = "Successfully copied from $filename. Feature $thisstory is now available to edit.";
				if ($thisstory =~ /^tor/) {
					$completeAction = "Feature converted to CP style\<br>$completeAction";
				}
	ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");
	$featPreview = MakeAPreview($copyTmp,$copyFile,$thisstory);
	ClosedDIV("class","ContentEditFull",$featPreview);
	ClosedDIV("class","ContentInfoFoot","End of $thisstory");
	EndDIV();	
	OpenDIV("ID","Sidebar");
	MakeASideBar($copyTmp,$copyFile,$thisstory,"view");

## Resetting a feature involves moving it from the TEMP directory back to where it used to exist. 
#	We can determine where it was by the step folder in the Temp directory and the date extension in the story name. 
## This function is also used when the user clicks the Quit Without Saving button.
} elsif ($newstatParam eq "reset") {
	my $moveFromFile = $thisfile;
	my @dirParts = split('/',$thisfile);
	my $stepPart = $dirParts[5];
	my @storyparts = split('\.',$thisstory);
	my $dateFolder = $storyparts[1];
	my $moveToFile = "$FeatFolder/$dateFolder/$stepPart/$thisstory";
	if ($oldstate ne "new") {
		move($moveFromFile,$moveToFile);
	} 
	$completeAction = "Successfully quit - $filename without making changes.";
	ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");
	$featPreview = MakeAPreview($thistmp,$moveToFile,$thisstory);
	my $newfeat = $moveToFile;
	ClosedDIV("class","ContentEditFull",$featPreview);
	ClosedDIV("class","ContentInfoFoot","End of $thisstory");
	EndDIV();
	OpenDIV("ID","Sidebar");
	MakeASideBar($thistmp,$moveToFile,$featName,"view");

## Trashing a feature happens from the feature_editor script. 	
## This moves the feature to a Trash folder created in the dated folder. 
## Currently, this feature can only be recovered by manually moving it from the Trash folder to the date/step folder.

} elsif ($newstatParam eq "trash") { 
	my @dirParts = split('/',$thisfile);
	my $stepPart = $dirParts[5];
	my @storyparts = split('\.',$thisstory);
	my $dateFolder = $storyparts[1];
	makeadir("Trash");
 	my $moveFromFile = $thisfile;
	my $moveToFile = "${homeDir}Trash/$thisstory";
 	move($moveFromFile,$moveToFile);
	$completeAction = "$filename has been deleted and will now show in the list of new features available.";
	ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");

## If this feature is not being reset or trashed, it must be moving. 
## This mover script will display a preview of the feature once it has moved. This preview is called when a feature has been moved.
} elsif ($oldstate eq "preview") { 
	$featPreview = MakeAPreview($thistmp,$thisfile,$featName);
	ClosedDIV("class","ContentEditFull",$featPreview);
	ClosedDIV("class","ContentInfoFoot","End of $filename");
	EndDIV();
	OpenDIV("ID","Sidebar");
	MakeASideBar($thistmp,$thisfile,$featName,"view");


} else { 
	#my $featPreview = "";
	my @cgiListNames = getTmpNameList($thistmp);
	makeadir($date,$newstatParam);
	makeahistdir($date,$newstatParam);
	#print "Making $newfeat\n";
	open FEAT,">",$newfeat;

	foreach my $CGIlist (@cgiListNames) {
		chomp($CGIlist);
		my $markEnd = "";
		my @lineValues = getTMPLinevalues($thistmp,$CGIlist);
		
		# [0] = field name
		# [1] = text field type
		# [2] = merlmarkup 
		# [3] = default text
		# [4] = optional field marker indicated by "Opt"

		my $markStart = getMerltoHtmlMark($thistmp,$CGIlist);
		if (($CGIlist eq "EP") || ($CGIlist eq "Hidden") || ($CGIlist eq "EOF")) { 
			#$featPreview = "$featPreview<br>";#Don't add these until we are ready for production.
		} elsif ($CGIlist eq "Notes") {
			my $this_line = $query->param($CGIlist);
			$this_line =~ s/\n+/\<br>/g; #change new lines to html breaks 
			print FEAT "<${CGIlist}>${this_line}</${CGIlist}>\n";
		} elsif ($CGIlist eq "Photo") {
			my $this_line = $query->param($CGIlist);
			$this_line =~ s/\n+/\<br>/g; #change new lines to html breaks 
			print FEAT "<${CGIlist}>${this_line}</${CGIlist}>\n";
		} else {
			my $this_line = $query->param($CGIlist);
			#$this_line =~ uri_escape_utf8($this_line);
			utf8::decode($this_line);
			#print "Line is $this_line\n";
			$this_line =~ s/\s+/ /g; #find more than one space together replace with single space
			$this_line =~ s/\n+/\<br>/g; #change new lines to html breaks 
			$this_line =~ s/\<br \/>/\<\/p> \<p>/g; #change new lines to html breaks
			if (($featName ne "soapsyn") && ($featName ne "selspsyn") && ($featName ne "whatdvr")) {
			$this_line =~ s/<\/strong><\/p> <p>/<\/p> <p><\/strong>/g;
			}
			print FEAT "<${CGIlist}>${this_line}</${CGIlist}>\n";
		}
	}

	close FEAT;
	chmod(0755,$newfeat);
	$featPreview = MakeAPreview($thistmp,$newfeat,$featName);

	#put the  file in the history directory for feature forensics. 
	if ($oldstate ne 'new') {
		move($thisfile,$histDir); 
	}
	$completeAction = "$filename has been updated from <b>$oldstate</b> to step <b>$newstatParam</b>.";
	if ($newstatParam ne "Filtered") {
		ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");
		ClosedDIV("class","ContentEditFull",$featPreview);
		ClosedDIV("class","ContentInfoFoot","End of $filename");
		EndDIV();
		OpenDIV("ID","Sidebar");
		MakeASideBar($thistmp,$newfeat,$featName,"view");
	}


}

## If this feature was moved to the FILTERED step, we need to make this into a file that is compatible with the VMS Systems.
## This will take the Merl Markup value found in the TMP file and add it to the correct feature sections.
## Other substitutions happen here that are only relevant to the MERL markup file, like adding <EP>, hidden and EOF markup.
## double quotes are converted to `` and '' for opening and closing quotes. 
## HTML markup styles are either converted to MERL markup styles or removed if it's not relevant. 
## There's also a function to reduce line size to 180 or less characters. 
## This file is copied to the DATE/POSTED directory. These files will NOT show up in the featureman main page to be edited. 

if ($newstatParam eq "Filtered") {

	my @cgiListNames = getTmpNameList($thistmp);
	makeadir($date,"Posted");
	makeadir($date,"TEMP");
	$completeAction = "Filtered to Becky.";		
		if ($checkRecycle eq "TRUE") {
			copy($newfeat,$RecycleDir);
		}

	open FH, "<", $newfeat; #Get existing feature and put all together to grab text between name tags
	my @records = <FH>;
	my $allrecords = join "", @records;	
	close FH;
	### We need special instructions for crossword features. These get tabs and extra spaces. 
if (($thistmp =~ /cross.tmp$/) || ($thistmp =~ /puzz.tmp$/)) {
	open FMERL,">:encoding(UTF-8)",$filterfeat;
	#print FMERL "Before Filter:\n\n$allrecords\n\n";
		foreach my $CGIlist (@cgiListNames) {
		if ($CGIlist eq "EP") {
			print FMERL "<ep>\n";
		} elsif ($CGIlist eq "EOF") {
			print FMERL "<2><4><30>\n";
		} elsif (($CGIlist =~ m/^Hidden/) || ($CGIlist eq "Hidden")) {
			my $markup = getTmpColValue($thistmp,$CGIlist);
			chomp($markup);
			print FMERL "$markup<ep>\n";
		} elsif (($CGIlist eq "Notes") || ($CGIlist eq "Photo")) {
			# We don't want Notes in the final product.	
		} else {
			my @allLines180;
			my @lineValues = getTMPLinevalues($thistmp,$CGIlist);
			my $markup = $lineValues[2];
			chomp($markup);
			$allrecords =~ /\<$CGIlist\>(.*)\<\/$CGIlist\>/; 
			my $this_line = $1;
			if ($this_line ne "") {
				my $quotesLine = convertQuotes($this_line);
				my $merlline = htmltomerlMarkup($quotesLine);
				my $line180 = "$markup";
				my @each_line = split('\|\|',$merlline);
				foreach (@each_line) {
						my $line2add = make180($_);
						if ($line2add ne '') {
						if ($line2add =~ /^\d+\./) {
								$line2add =~ s/\.\s{2,}/\.\t/g;
						}	
							if ($line2add =~ /^\d\./) {
								$line2add = "  $line2add";							
							}
						$line180 = "$line180${line2add}<ep>\n";
						}
				}
				print FMERL "$line180";
			}
		}
	}
	close FMERL;
} else {
	open FMERL,">",$filterfeat;
	open TFEAT, ">",$tempFeat;
	#print FMERL "Before Filter:\n\n$allrecords\n\n";
		foreach my $CGIlist (@cgiListNames) {
		if ($CGIlist eq "EP") {
			print FMERL "<ep>\n";
			print TFEAT "\n";
		} elsif ($CGIlist eq "EOF30") {
			print FMERL "<30>\n";
		} elsif ($CGIlist eq "EOF") {
			print FMERL "<2><4><30>\n";
		} elsif (($CGIlist =~ m/^Hidden/) || ($CGIlist eq "Hidden")) {
			my $markup = getTmpColValue($thistmp,$CGIlist);
			chomp($markup);
			print FMERL "$markup<ep>\n";
		} else {
			my @allLines180;
			my @lineValues = getTMPLinevalues($thistmp,$CGIlist);
			if ($lineValues[4] ne "") { next; } ## Anything in this parameter does not get filtered.
			my $markup = $lineValues[2];
			chomp($markup);
			$allrecords =~ /\<$CGIlist\>(.*)\<\/$CGIlist\>/; 
			my $this_line = $1;
			print TFEAT "$this_line\n";

			if ($this_line ne "") {
				my $quotesLine = convertQuotes($this_line);
				my $merlline = htmltomerlMarkup($quotesLine);
				my $line180 = "$markup";
				my @each_line = split('\|\|',$merlline);
				foreach (@each_line) {
						my $line2add = make180($_);
						if ($line2add ne '') {
							$line180 = "$line180${line2add}<ep>\n";
						}
						if (($line2add eq '') && (($thistmp =~ /cnot.tmp$/) || ($thistmp =~ /filmog.tmp$/) || ($thistmp =~ /tastytv.tmp$/))) {
							$line180 = "$line180<ep>\n";
						}
				}
				print FMERL "$line180";
			}
		}
	}
	close FMERL;
	close TFEAT;

}

	## uploads finished feature to the NFSDISK[200301] directory on the VMS system
		if ($checkTest eq "LIVE") {
			uploadFeatureLIVE($filterfeat);
			uploadFeatureTEST($filterfeat);
			$completeAction = "Feature has been Filtered to Becky.";
		} else {
			uploadFeatureTEST($filterfeat);
			$completeAction = "Feature has been Filtered to Becky. <br>This feature is in Testing mode.\n Filtered to becky's TEST area for review.\n";
		}
			emailnotifier($oldstate,"posted",$filterfeat,$featName,$specFile);
		if ($oldstate eq 'Filtered') {
			emailnotifier($oldstate,"Refiltered",$filterfeat,$featName,$specFile);		
		}
		ClosedDIV("class","ContentInfo","Action Completed!<br>$completeAction");
		ClosedDIV("class","ContentEditFull",$featPreview);
		ClosedDIV("class","ContentInfo","End of $filename");
		EndDIV();
		OpenDIV("ID","Sidebar");
		MakeASideBar($thistmp,$newfeat,$featName,"view");

} 
	if ($oldstate ne $newstatParam) {
		emailnotifier($oldstate,$newstatParam,$newfeat,$featName,$specFile);
	if ($newstatParam eq "Copy Edit") {
		CopyEditnotifier($oldstate,$newstatParam,$newfeat,$featName,$specFile);
	}
}
EndDIV();

EndDIV();
HTMLend();
