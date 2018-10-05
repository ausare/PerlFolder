#!/Users/scripting/perl5/perlbrew/perls/perl-5.24.0/bin/Perl
##########################################
#
#	by Larry Gonyea
#      TMS
#   Common functions used by many scripts for the Features Editor Site.
#
#############################
#use lib "/opt/local/lib/perl5/site_perl/5.8.9";
#use lib "/Users/scripting/perl5/perlbrew/perls/perl-5.22.0/lib/5.22.0";
use Time::Local;
use Net::FTP;
use Mail::Send;
use MIME::Lite;
use Tie::File;
use Text::Wrapper;
use XML::LibXML;
use utf8;
#use encoding 'UTF-8';
#use lib '/Users/scripting/perl5/perlbrew/perls/perl-5.22.0/lib/site_perl/5.22.0';
#use Image::ExifTool;
require("PD_web_elements.cgi");

my $scriptloginID = "scripting";
my $scriptloginPWD = "alaska";
my $pathUNIX;
my $baseFEfolder = "/Library/WebServer/CGI-Executables/Operations";
my $FeatFolder = "/Library/WebServer/OPS";
my $PhotoDir = "/Library/WebServer/CGI-Executables/Operations/";
my $templateDir = "/Library/WebServer/CGI-Executables/Operations/templates/"; 
my $specDir = "/Library/WebServer/CGI-Executables/Operations/specs/"; 
my ($ThisIP,$systemType) = getHomeAddress();

#Called to get the base directories to Features and Feature scripts.
sub getFilesLocal {
my $CGIscriptslocal = "/Library/WebServer/CGI-Executables/Operations";
my $FeatureFilesLocal = "/Library/WebServer/OPS";
return($CGIscriptslocal,$FeatureFilesLocal)
}

#Determines home machine web browser address. $ThisIP should be change to change all other scripts to direct links correctly.
## $systemOn dictates how scripts react to certain steps. Development is used to prevent filtering to live. Live is used to make everything work in a live environment. 
sub getHomeAddress {
my $ThisIP = "pmsgf.tmsgf.trb";
my $systemOn = "Live";
return($ThisIP,$systemOn);
}

# basic logic that creates a array. every line in a file becomes a list item. Filters out blank lines.
sub arrayFile {
## Need one param. Full file path
## This filters out blank lines.
my @fileArray;
my $thisFile = $_[0];
open FH,"<$thisFile";
my @fileSplit = <FH>;
close FH;
		foreach my $line (@fileSplit) {
		if ($line ne "") {
			chomp($line);
			push (@fileArray,$line);
		}
		}
return(@fileArray);
}

sub findCustomer {
my $find_what = uc($_[0]);
my @foundCustomer = ("NONE","NONE","NONE","NONE");
my $cust_master_file = "/Library/WebServer/Becky/allcust.txt";
my @Becky_Master = arrayFile($cust_master_file);
foreach (@Becky_Master) {
	my @allParts = split('\|',$_);
	if ($allParts[0] eq $find_what) {
		my @foundCustomer = @allParts;
		return(@foundCustomer);
	}
}
}
### Not Currently used ###
# make a dropdown list of writers from the getWriters subroutine.
sub makeWriterDropdown {
my $defWriter = $_[0];
my @writerlist = getWriters();
my $optionslist = "";
		foreach my $writer (@writerlist) {
			if ($writer eq $defWriter) {
				$optionslist = ("$optionslist<option value=\"$writer\" selected>$writer</option>\n");
			} else {
				$optionslist = ("$optionslist<option value=\"$writer\">$writer</option>\n");
			}
		}	
return($optionslist);	
}


#Make a radio button list of steps a feature can be in. This list is used in the Editor to submit what step the feature will move to.
sub makeStateRadio {
my $currentStat = $_[0];
my @statelist = getstatelist();
my $optionslist = "";
		foreach my $states (@statelist) {
			my $choiceList = $states;
			if ($choiceList eq "Filtered") {
				$choiceList = "Filter";
			}
			if (($currentStat eq "new") || ($currentStat eq "autoGen")) {
				$currentStat = "In Progress";
			}

			if ($states eq $currentStat) {
				$optionslist = ("$optionslist<div class=SidebarRadio><input type=\"radio\" form=\"Mover\" name=\"newstate\" value=\"$states\" checked>$states</div>");
			} else {
				$optionslist = ("$optionslist<div class=SidebarRadio><input type=\"radio\" form=\"Mover\" name=\"newstate\" value=\"$states\">$states<br></div>");
			}
		}	
return($optionslist);	
}


# Gets specific exif data from a photo and returns it. 
sub getPhotoExif {
my $photoInfo = $_[0];
my $exifTool = new Image::ExifTool;
###  Use for directories of files when needed
#	opendir(TMPDIR, $photoDir);
#	my @photoList = readdir TMPDIR;
#	closedir(TMPDIR);
#	foreach (@photoList) {
#	if (($_ =~ /^\./m) || ($_ eq "") || (!defined($_))) {
#		next;
#	} else {
#	}
	my $info = $exifTool->ImageInfo("$photoInfo");
		my $name_value = $exifTool->GetValue('FileName');
		my $caption_value = $exifTool->GetValue('Caption-Abstract');
		my $res_value = $exifTool->GetValue('XResolution');
		my $dimensions_value = $exifTool->GetValue('ImageSize');
		my $colorMode = $exifTool->GetValue('ColorMode');
#name,caption,resolution,dimensions,colormode
return($name_value,$caption_value,$res_value,$dimensions_value,$colorMode);
}

# Not currently used by any scripts. Could prove to be helpful in the future. 
sub convertQuotesToHTML { 
	my $returnText = "";
	my $tmpline = $_[0];
	my $problems;
		my @allrecords = split('\<\/p\>',$tmpline);
			while ($tmpline =~ m/ \``\w/g) { #as long as there's a html quote replace them. 
 		 		$tmpline =~ s/ \`\`/ \&ldquo;/;
			}
			while ($tmpline =~ m/ \"\w /g) { #as long as there's a html quote replace them. 
 		 		$tmpline =~ s/ \"/ \&ldquo;/;
			}
			while ($tmpline =~ m/ &quot;\w/g) { #as long as there's a html quote replace them. 
 		 		$tmpline =~ s/ &quot;/ \&ldquo;/;
			}
			while ($tmpline =~ m/\w\" /g) { #as long as there's a html quote replace them. 
 		 		$tmpline =~ s/\" / \&rdquo;/;
			}
			while ($tmpline =~ m/&quot; /g) { #as long as there's a html quote replace them. 
 		 		$tmpline =~ s/&quot; / \&rdquo; /;
			}
			while ($tmpline =~ m/ \`\w/g) { #as long as there's a html quote replace them. 
 		 		$tmpline =~ s/ \`/ \&lsquo;/;
			}
			while ($tmpline =~ m/\w\' /g) { #as long as there's a html quote replace them. 
 		 		$tmpline =~ s/\' / \&rsquo;/;
			}
			while ($tmpline =~ m/\w\&#39;s /g) { #as long as there's a html quote replace them. 
 		 		$tmpline =~ s/\'/\&rsquo;/;
			}
			while ($tmpline =~ m/\w\&#39;d /g) { #as long as there's a html quote replace them. 
 		 		$tmpline =~ s/\'/\&rsquo;/;
			}
			while ($tmpline =~ m/\w\'s /g) { #as long as there's a html quote replace them. 
 		 		$tmpline =~ s/\'/\&rsquo;/;
			}
			
			
	return($tmpline);
} #end sub convertQuotes


#  This is used to search and replace text based on a filter file.
#  the filter files should contain the search for and replace with a pipe (|) between. 
#  Each search/replace should be on a separate line. 
sub runFilter {
	my $useFilter = $_[0];
	my $tmpline = $_[1];
	#print "Filter is $useFilter\n";
	if ($useFilter eq "cpstyle") {
		my $thisFilter = "/Library/WebServer/CGI-Executables/operations/filters/cpconvert.txt";
		#print "Using filter $thisFilter\n";
		}
	my %filterList = hashAFile($thisFilter);
	my $hashCount = scalar(keys %filterList);
	#print "Key count is $hashCount\n";
	while ( my ($key, $value) = each %filterList ) {
		print "switching $key to $value\n";
		$tmpline =~ s/$key/$value/g;
	}
	return($tmpline);
}

# returns the Merl markup value found in the TMP file based on the given fieldname field.
sub getTmpColValue {
my @returnlist;
my $colToAdd = "";
my $tmpfile = $_[0];
my $fieldname = $_[1];
open TH,"<",$tmpfile or die $!;
my @fieldlists = <TH>;
close TH;
	foreach $line (@fieldlists) {
			@splitList = split('\|',$line); 
			my $namefield = $splitList[0];
			my $markupfield = $splitList[2];
			if ($namefield eq $fieldname) {
				$colToAdd = $markupfield;
			}
		}
return($colToAdd);
}



sub makeHeaderTopper {

OpenDIV("class","HeaderTopper");
ClosedDIV ("class","TopperRight","<a href=\"http://$ThisIP/cgi-bin/Operations/monitor.cgi?pageMode=monitor\">Normal Screen Monitor</a>");
ClosedDIV ("class","TopperRight","<a href=\"http://$ThisIP/cgi-bin/Operations/monitor.cgi?screenMode=BIG&pageMode=Monitor&pageType=fails\">BIG Screen Fails</a>");
ClosedDIV ("class","TopperRight","<a href=\"http://$ThisIP/cgi-bin/Operations/monitor.cgi?screenMode=BIG&pageMode=Monitor&pageType=runs\">BIG Screen Executing</a>");
EndDIV();

}


 # end makeNAVbar
sub makeNAVbar {
#my $home_page = $_[0];
my ($ThisIP,$systemOn) = getHomeAddress();
#my $home_page = "$ThisIP/";
my ($week1,$week2,$week3,$week4,$week5,$week6,$week7) = getweeks(); 
#my @allsteps = getstatelist();
#my @allbaseweeks = getweeks();
my @allTemplates = ArrayADir($templateDir,"No");
#bottom NAV
print "<nav>\n";
print "	<ul>\n";
#print "	<li><a href=\"#\">Templates &darr;</a>\n";
#print "	<ul>\n";
#	foreach my $Thistemp (@allTemplates) {
#		print "	<li><a href=\"http://featuremanager.tmsgf.trb/cgi-bin/Operations/operations.cgi?template=$Thistemp&pageType=new\">$Thistemp</a>\n";
#	}
#	print "</li>\n";
#print "	</ul>\n";
print "	<li><a href=\"http://$ThisIP/cgi-bin/Operations/monitor.cgi?pageMode=Monitor\">Monitor Production</a>\n";
print "</li>\n";
print "	<li><a href=\"http://$ThisIP/cgi-bin/Operations/monitor.cgi?pageType=CronacleProd\">Show Completed Cronacle</a>\n";
print "</li>\n";
print "	<li><a href=\"http://$ThisIP/cgi-bin/Operations/monitor.cgi?pageType=CronacleSched\">Show Scheduled Cronacle</a>\n";
print "</li>\n";
print "	<li><a href=\"http://$ThisIP/cgi-bin/Operations/monitor.cgi?pageType=fails&pageMode=monitor\">Monitor Fails</a>\n";
print "</li>\n";
print "	<li><a href=\"http://$ThisIP/cgi-bin/Operations/monitor.cgi?pageType=runs&pageMode=monitor\">Monitor Running</a>\n";
print "</li>\n";
print "	<li><a href=\"http://$ThisIP/cgi-bin/Operations/monitor.cgi?pageType=AutoPag&pageMode=monitor\">Monitor AutoPag</a>\n";
print "</li>\n";

print "	</ul>\n";
print "</nav>\n";

} # end makeNAVbar


sub MakeASideBar {
	my ($TFile,$OFile,$storyName,$viewType) = @_;
	my @cgiListNames = getTmpNameList($TFile);
	#print "$OFile";
		my @fileParts = split '\/',$OFile;
		my $featureName = $fileParts[6];
		my @storyParts = split '\.',$featureName;
		my $featWeek = $storyParts[1];
		my $specFile = "$baseFEfolder/specs/$storyName.spc";
		my $photoDir = "/Library/WebServer/Documents/Images/$featWeek";
		my @photoList = ArrayADir($photoDir);
		my %specHash = hashAFile($specFile);
		my $photoList = $specHash{'photo'};
		$photoList =~ s/MDD/$featWeek/g;
		my @allPhotos = split '\,',$photoList;
		#print "@allPhotos";
		open FP,"<",$OFile;
			my @thisList = <FP>;
		close FP;
	
		my $allrecords = join "", @thisList;

	foreach my $CGIlist (@cgiListNames) {
		my $this_line;
		chomp($CGIlist);
		#utf8::decode($this_line);
		my @lineValues = getTMPLinevalues($TFile,$CGIlist);
					#ClosedDIV("class","NotesField","Placement for $CGIlist is $lineValues[4]");

		if ($lineValues[4] eq "SideBar") {
			my $this_line = $allrecords;
			$this_line =~ /\<$CGIlist\>(.*)\<\/$CGIlist\>/; 
			$this_line = $1;
			#print "Placement for $CGIlist is $lineValues[4]<br>";
			#ClosedDIV("class","NotesField","Placement for $CGIlist is $lineValues[4]");
			ClosedDIV("class","SidebarTitle","$CGIlist");
			OpenDIV("class","SidebarGroup");
			#$this_line =~ s/\<br\>/\n/g;
			if ($this_line eq "") {
				$this_line = "No data for $CGIlist";
			}

			if ($viewType eq "edit") {	
				ClosedDIV("class","ContentFormField","<textarea rows=\"10\" name=\"$CGIlist\">$this_line</textarea>");
			} else {
				ClosedDIV("class","NotesField","$this_line");
			}	
			
			EndDIV();

		}
		
	}
}
sub getTmpNameList {
my @returnlist;
my $tmpfile = $_[0];
open TH,"<",$tmpfile or die $!;
my @fieldlists = <TH>;
close TH;
	foreach $line (@fieldlists) {
		if ($line ne "") {
			@splitList = split('\|',$line); 
			my $colToAdd = $splitList[0];
			push (@returnlist,$colToAdd);
		}
	}
return(@returnlist);
}
sub getTMPLinevalues { 
# gets an array of the values from feature template file. 
# requires 2 arguments full tmp file path and field name
# returns all values from the line matching the field name in an array. Array values listed
# [0] = field name
# [1] = text field type
# [2] = merlmarkup 
# [3] = default text
# [4] = optional field marker indicated by "Opt"
my @returnlist;
my $colToAdd = "";
my $tmpfile = $_[0];
my $fieldname = $_[1];
open TH,"<",$tmpfile or die $!;
my @fieldlists = <TH>;
close TH;
	foreach $line (@fieldlists) {
			@splitList = split('\|',$line); 
			my $namefield = $splitList[0];
			if ($namefield eq $fieldname) {
				@returnlist = @splitList;
			}
		}
return(@returnlist);
}

sub MakeAWebPage {
	my ($TFile,$OFile,$storyName,$photo,$caption) = @_;
	my @cgiListNames = getTmpNameList($TFile);
	#my @featSpecs = getFeatSpecs("$storyName");
	my $col_val = $featSpecs[1];
	#print @featSpecs;
	my $columnMaker = "";
	my $NewspaprCol;
	open FP,"<",$OFile;
	my @thisList = <FP>;
	close FP;
	my $allrecords = join "", @thisList;
	foreach my $CGIlist (@cgiListNames) {
		#print "Field: $CGIlist\n";
		chomp($CGIlist);
		my $markEnd = "";
		my @lineValues = getTMPLinevalues($TFile,$CGIlist);
		
		# [0] = field name
		# [1] = text field type
		# [2] = merlmarkup 
		# [3] = default text
		# [4] = optional field marker indicated by "Opt"
		# [5] = number of columns for feature. Should be in the Body line Defaults to 1
		
		my $markStart = getMerltoHtmlMark($TFile,$CGIlist);

		#my $markStart = $lineValues[2];
		if (($CGIlist eq "EP") || ($CGIlist eq "Hidden") || ($CGIlist eq "EOF")) { 
			$featPreview = "$featPreview<br>";#Don't add these until we are ready for production.
		} else {
			my $this_line = $allrecords;
			$this_line =~ /\<$CGIlist\>(.*)\<\/$CGIlist\>/; 
			$this_line = $1;
			utf8::decode($this_line);
			#print "$CGIlist is $this_line\n";
			$this_line =~ s/\s+/ /g; #find more than one space together replace with single space
			$this_line =~ s/\n+/\<br>/g; #change new lines to html breaks 
			$this_line =~ s/\<br \/>/\<\/p> \<p>/g; #change new lines to html breaks
			$this_line =~ s/<\/strong><\/p> <p>/<\/p> <p><\/strong>/g;
			$this_line =~ s/\"/ \&quot /g; #change double quotes to html double quote
			#print  "<${CGIlist}>${this_line}</${CGIlist}>\n";
			#print "Field $CGIlist is $this_line\n";
			
			if ($CGIlist eq "Headline") {
				$featPreview = "$featPreview<headline>${markStart}<h1><b>${this_line}</b></h1></headline><br><article>";
			} elsif ($CGIlist eq "Copyright") {
				$columnMaker = "$columnMaker${markStart}${this_line}";
			} elsif ($CGIlist eq "Byline") {
				$columnMaker = "$columnMaker${markStart}${this_line}</b><br>";
			} elsif ($CGIlist eq "Body") {
				if ($photo ne "") {
					$featPreview = "$featpreview<img src=\"$photo\" alt=\"$photo\" width=\"100\" height=\"200\" style=\"float:right\">\n";
				}
				#$columnMaker = "$columnMaker";
				if ($col_val eq "3") {
					$NewspaprCol = "$columnMaker<div class=\"Content3col\">${markStart}${this_line}</div>";
				} elsif ($col_val eq "2") {
					$NewspaprCol = "$columnMaker<div class=\"Content2col\">${markStart}${this_line}</div>";
				} else {
					$NewspaprCol = "$columnMaker${markStart}${this_line}";
				}
				#	$columnMaker = "$columnMaker<hr><div class=\"Content3col\">${markStart}${this_line}</div><br>";
				#my $NewspaprCol = "$columnMaker<div class=\"Content3col\">${markStart}${this_line}</div>";
				$featPreview = "$featPreview${NewspaprCol}</article>";	
			}
		} 	
	}
return($featPreview);
}



sub hashAFile {
#returns hash for a file with | (pipe) delims
my ($thisFile) = $_[0];
		my %FileHash;
		my $line;
		my @records = arrayFile($thisFile);
		foreach $line (@records) {
			chomp($line);
			my @twoParts = split('\|',$line);
			my $thisKey = $twoParts[0];
			my $thisValue = $twoParts[1];
			$FileHash{$twoParts[0]} = $twoParts[1]; 
		}
return(%FileHash);
}


sub makeadir {
	my $fold1 = $_[0];
	my $fold2 = $_[1];
	my $directory1 = "$FeatFolder/$fold1";
	#print "attempting to create directory $directory\n";

	unless(-e $directory1 or mkdir $directory1) {
		die "Unable to create $directory\n";
	}
	chmod(0777,$directory1);
		my $directory2 = "$FeatFolder/$fold1/$fold2";
	unless(-e $directory2 or mkdir $directory2) {
		die "Unable to create $directory\n";
	}
	chmod(0777,$directory2);

}


sub makeaPhotoSetdir {
	my $fold1 = $_[0];
	#my $fold2 = $_[1];
	my $directory1 = "/Library/WebServer/Documents/ImageSets/$fold1";
	#print "attempting to create directory $directory\n";

	unless(-e $directory1 or mkdir $directory1) {
		die "Unable to create $directory\n";
	}
	chmod(0777,$directory1);
}


sub downloadFile
{
	my @parameters = @_;
	my $server = "$parameters[0]";
	my $user = "$parameters[1]";
	my $pass = "$parameters[2]";
	my $init = "$parameters[3]";	#supports only one level
	my $path = "$parameters[4]";
	my $downloadname = "$parameters[5]";

	my $ftp = Net::FTP->new("$server", Debug => 0, Passive => 0);
	$ftp->login("$user","$pass");
	$ftp->binary();
	$ftp->cwd("$init");
	$ftp->get("$downloadname","$path") or warn (print "**WARNING** - Cannot find $photo on Features FTP\n");
	$ftp->quit;
	return 1;
}

## creates 2 levels of directory in the FF/History directory of MDD/Step
## takes 2 parameters: (baseweek(MDD), Step name)


sub getweeks {
#  gets a list of Sunday baseweeks for use in filenames, etc. 
#  returns next for Sunday baseweeks in MDD format
	
	my ($f_second, $f_minute, $f_hour, $f_day, $f_month, $f_year, $f_weekDay, $f_dayOfYear, $IsDST) = localtime(time);
	my ($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear);
	my  @forwardsOfWeek = qw( 0 -86400 -172800 -259200 -345600 -432000 -518400 );
	my $time = time();
	my  $shiftZero = "$forwardsOfWeek[$f_weekDay]";
	$shiftZero = $time + $shiftZero;
	my $epochweekback = -604800;
	my $epochweekforward = 604800;
	my $shiftbackone = $shiftZero + $epochweekback;
	my $shiftbacktwo = $shiftbackone + $epochweekback;
	my $shiftbackthree = $shiftbackone + $epochweekback;
	my $shiftupone = $shiftZero + $epochweekforward;
	my $shiftuptwo = $shiftupone + $epochweekforward;
	my $shiftupthree = $shiftuptwo + $epochweekforward;
	my $shiftupfour = $shiftupthree + $epochweekforward;
	my $shiftupfive = $shiftupfour + $epochweekforward;
	my $shiftupsix = $shiftupfive + $epochweekforward;
	my $shiftupseven = $shiftupsix + $epochweekforward;

	#print "$time\n";
	# Takes current time in seconds and shifts it to the correct day of log cycle.
	($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($shiftbacktwo); 
		$mm++;
	if($day < 10)
	{
	 $day = "0$day";
	}
	if($mm == 10)
	{
		 $mm = "o";
	}
	elsif($mm == 11)
	{
		$mm =  "n";
	}
	elsif($mm == 12)
	{
		 $mm =  "d";
	}
	my $weekback2 = "$mm$day";
		
	($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($shiftbackone); 
		$mm++;
		if ($day < 10)
	{
		 $day = "0$day";
	}
	if($mm == 10)
	{
		 $mm = "o";
	}
	elsif($mm == 11)
	{
		 $mm =  "n";
	}
	elsif($mm == 12)
	{
		 $mm =  "d";
	}
	my $weekback1 = "$mm$day";
	
		($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($shiftZero); 
		$mm++;
	if($day < 10)
	{
		 $day = "0$day";
	}
	if($mm == 10)
	{
		 $mm = "o";
	}
	elsif($mm == 11)
	{
		 $mm =  "n";
	}
	elsif($mm == 12)
	{
		 $mm =  "d";
	}
	my $thisweek = "$mm$day";
	
			($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($shiftupone); 
		$mm++;
	if($day < 10)
	{
		 $day = "0$day";
	}
	if($mm == 10)
	{
		 $mm = "o";
	}
	elsif($mm == 11)
	{
		 $mm =  "n";
	}
	elsif($mm == 12)
	{
		 $mm =  "d";
	}
	my $weekup1 = "$mm$day";
	
		
			($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($shiftuptwo); 
		$mm++;
	if($day < 10)
	{
		 $day = "0$day";
	}
	if($mm == 10)
	{
		 $mm = "o";
	}
	elsif($mm == 11)
	{
		 $mm =  "n";
	}
	elsif($mm == 12)
	{
		 $mm =  "d";
	}
	my $weekup2 = "$mm$day";
	
		
			($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($shiftupthree); 
		$mm++;
	if($day < 10)
	{
		 $day = "0$day";
	}
	if($mm == 10)
	{
		 $mm = "o";
	}
	elsif($mm == 11)
	{
		 $mm =  "n";
	}
	elsif($mm == 12)
	{
		 $mm =  "d";
	}
	my $weekup3 = "$mm$day";
	
		
			($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($shiftupfour); 
		$mm++;
	if($day < 10)
	{
		 $day = "0$day";
	}
	if($mm == 10)
	{
		 $mm = "o";
	}
	elsif($mm == 11)
	{
		 $mm =  "n";
	}
	elsif($mm == 12)
	{
		 $mm =  "d";
	}
	my $weekup4 = "$mm$day";
	
				($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($shiftupfive); 
		$mm++;
	if($day < 10)
	{
		 $day = "0$day";
	}
	if($mm == 10)
	{
		 $mm = "o";
	}
	elsif($mm == 11)
	{
		 $mm =  "n";
	}
	elsif($mm == 12)
	{
		 $mm =  "d";
	}
	my $weekup5 = "$mm$day";

					($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($shiftupsix); 
		$mm++;
	if($day < 10)
	{
		 $day = "0$day";
	}
	if($mm == 10)
	{
		 $mm = "o";
	}
	elsif($mm == 11)
	{
		 $mm =  "n";
	}
	elsif($mm == 12)
	{
		 $mm =  "d";
	}
	my $weekup6 = "$mm$day";
	
				($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($shiftupseven); 
		$mm++;
	if($day < 10)
	{
		 $day = "0$day";
	}
	if($mm == 10)
	{
		 $mm = "o";
	}
	elsif($mm == 11)
	{
		 $mm =  "n";
	}
	elsif($mm == 12)
	{
		 $mm =  "d";
	}
	my $weekup7 = "$mm$day";

	#return("o12","o05","928","921","914","907","831","824");
	return($weekup7,$weekup6,$weekup5,$weekup4,$weekup3,$weekup2,$weekup1,$thisweek);
}

sub getweeksout {
#  gets the mdd date of the number of weeks offset
#  returns next for Sunday baseweeks in MDD format
	my $numofweeksout = $_[0];
	#my $numofweeksout += 0;
	my ($f_second, $f_minute, $f_hour, $f_day, $f_month, $f_year, $f_weekDay, $f_dayOfYear, $IsDST) = localtime(time);
	my ($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear);
	my  @forwardsOfWeek = qw( 0 -86400 -172800 -259200 -345600 -432000 -518400 );
	my $time = time();
	my  $shiftZero = "$forwardsOfWeek[$f_weekDay]";
	$shiftZero = $time + $shiftZero;
	my $epochweekback = -604800;
	my $epochweekforward = 604800;
	my $epochOffset = $numofweeksout * $epochweekforward;
	my $epochweek = $shiftZero + $epochOffset;
	
	
	#print "$time\n";
	# Takes current time in seconds and shifts it to the correct day of log cycle.
	($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($epochweek); 
		$mm++;
	if($day < 10)
	{
	 $day = "0$day";
	}
	if($mm == 10)
	{
		 $mm = "o";
	}
	elsif($mm == 11)
	{
		$mm =  "n";
	}
	elsif($mm == 12)
	{
		 $mm =  "d";
	}
	my $thisweek = "$mm$day";
		
	
	return($thisweek);
}

## Sends feature out via email. 
# This can determine who gets the email based upon the step it was changed to.
# If the step does not change (with the exception of Filtered), this routine will not be called upon.
sub emailnotifier {
	use MIME::Lite;
	my @parameters = @_;
	my $subjectLine = $parameters[0];
#	my $thisstatus = $parameters[1];
	my ($toLine,$ccLine,$bccLine);
	my $thisfile = $parameters[2];
	my $thisstory = $parameters[1];
	my $thisspec = $parameters[3];
	my %GetFeatSpecs = hashAFile($thisspec);
	my $emailGroup = $GetFeatSpecs{'emailgroup'};
	my $toList =  $GetFeatSpecs{'toLine'};
	my $ccList =  $GetFeatSpecs{'ccLine'};
	my $bccList =  $GetFeatSpecs{'bccLine'};
	#print "Found a list of emails - $emailGroup\n";
	#my @Specs = getFeatSpecs($thisstory);
	#my $emailDist = $Specs[4];
	my $gLogFilePath = "$thisstory";
	#my @fileparts = split('/',$thisfile);
### TESTING
#	my $ccLIne =  "";
#	my $bccLIne =  "";
###
	my @allEmails = split(',',$toList);
	#print "Found email $thisspec and it's list @allEmails\n";
	foreach (@allEmails) {
		if ($toLine eq "") {
		$toLine = "$_\@gracenote.com"
		} else {
		$toLine = "$toLine,$_\@gracenote.com"
		}
	}
	
	my @allEmails = split(',',$ccList);
	#print "Found email $thisspec and it's list @allEmails\n";
	foreach (@allEmails) {
		if ($ccLine eq "") {
		$ccLine = "$_\@gracenote.com"
		} else {
		$ccLine = "$ccLine,$_\@gracenote.com"
		}
	}
	my @allEmails = split(',',$bccList);
	#print "Found email $thisspec and it's list @allEmails\n";
	foreach (@allEmails) {
		if ($bccLine eq "") {
		$bccLine = "$_\@gracenote.com"
		} else {
		$bccLine = "$bccLine,$_\@gracenote.com"
		}
	}

	#my $filename = $fileparts[6];
	#my $toLine = "$emailDistm"; # by default
#	if ($systemType eq "Development") {
#		my	$toLine = "lgonyea\@gracenote.com,jagifford\@gracenote.com";	
#	}
#	my $subjectLine = "$filename has changed status from $oldstatus to $thisstatus";

	my $runninglog = "";
	my $mailline = "";
	#my $addr = "163.193.250.55";
	open (MAILLOGFILE, "$gLogFilePath") || die "Could not open log file to email!";
	while ($mailline = <MAILLOGFILE>)
	{
		$runninglog = "$runninglog$mailline<br>";
	}
	close(MAILLOGFILE);
    #  print "Created Email\nGoing to $toLine\nSubject is $subjectLine";
  #print "Sending email message with error.\n";
  #	$toLine = "lrgonyea\@gracenote.com, gdickie\@gracenote.com";

    my $msg = MIME::Lite->new (
    From    => "OperationsNotifier\@gracenote.com",
    To      => "$toLine",
    Cc      => "$ccLine",
    Bcc      => "$bccLine",  
    Subject => "$subjectLine",
    #Subject => "Where is my Subject?",
    Type    => "text/html",
    Data    => "$runninglog",
    
    );
    $msg->send();
    
}


#returns a list of files in a directory (Parameter 1) with a specific extension (Parameter 2) and created a option value drop down.
# used to create a drop down of feature names based upon available tmp file in the template directory
sub getFileList {
	#/Library/WebServer/CGI-Executables/templates
	my $filenameList = "";
	my $tempfolder = $_[0];
	my $extOption = $_[1];
	opendir(TMPDIR, $tempfolder);
	my @tmpfiles = readdir TMPDIR;
	closedir(TMPDIR);
		foreach my $name (@tmpfiles) {
			my @parts = split (/\./,$name);
				if ($parts[0] ne "") {
					if ($extOption eq "No") {
						my $fileList = "$parts[0]";
						$filenameList = ("$filenameList<option value=\"$fileList\">$fileList</option>\n");
					} else {
						my $fileList = "$parts[0].$parts[1]";
						$filenameList = ("$filenameList<option value=\"$fileList\">$fileList</option>\n");
					}
				}
		}	
return($filenameList);				    
}


sub ArrayADir {
	my @filenameListArray;
	my $tempfolder = $_[0];
	my $extOption = $_[1];
	opendir(TMPDIR, $tempfolder);
	my @tmpfiles = readdir TMPDIR;
	closedir(TMPDIR);
		foreach my $name (@tmpfiles) {
			my @parts = split (/\./,$name);
				if ($parts[0] ne "") {
					if ($extOption eq "No") {
						my $fileList = "$parts[0]";
						push(@filenameListArray,"$fileList");
					} else {
						#my $fileList = "$parts[0].$parts[1]";
						push(@filenameListArray,"$name");
					}
				}
		}	
return(@filenameListArray);				    

}


sub findDAW {
my $dawNum = $_[0];
	my ($f_second, $f_minute, $f_hour, $f_day, $f_month, $f_year, $f_weekDay, $f_dayOfYear, $IsDST) = localtime(time);
	my @daysOfWeek = ("SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT");
	my $three_day = $daysOfWeek[$f_weekDay];
	return($three_day);
}

sub whenDue {
	my $due_diff;
	my $due_off;
	my $dawNum = $_[0];
	my $time_due = $_[1];
	my %hash_days = ("SUN" => "0", "MON" => "1","TUE" => "2","WED" => "3","THU" => "4","FRI" => "5","SAT" => "6");
	my ($f_second, $f_minute, $f_hour, $f_day, $f_month, $f_year, $f_weekDay, $f_dayOfYear, $IsDST) = localtime(time);
	my @daysOfWeek = ("SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT");
	my @forwardsOfWeek = qw( 0 86400 172800 259200 345600 432000 518400 );
	my $now_three_day = $daysOfWeek[$f_weekDay];
		my $today_num = $hash_days{$now_three_day};
		my $due_num = $hash_days{$dawNum};
		if ($today_num == $due_num) {
			$due_diff = "due Today at $time_due";
			$due_off = "0";
		} elsif ($today_num > $due_num) {
			$due_diff = "Late! Was due $dawNum at $time_due.";
			$due_off = "";
		} else {
			$due_diff = $due_num - $today_num;
			$due_off = $due_diff;
			if ($due_diff == 1) {$due_diff = "Due Tomorrow at $time_due"} else {$due_diff = "Due in $due_diff Days";}
		}
	return($due_diff,$due_off);
}


sub uploadFeatureLIVE {
use Net::FTP;
	my $outfilename = $_[0];
	my $server = "becky.tmsgf.trb";
	my $user = "printpro";
	my $pass = "printpro";
	my $init = "";	#supports only one level
	my $path = "";
	#my $uploadname = "$_";

	my $ftp = Net::FTP->new("$server", Debug => 0, Passive => 0);
	$ftp->login("$user","$pass");
	#$ftp->ascii();
	$ftp->binary();	
   #$ftp->cwd("OPDISK:[USERS.OPERATIONS.LGONYEA.FEATURES]");
	$ftp->cwd("NFSDISK:[200301]");
#	$ftp->cwd("BECKY_D2:[PCSA.FILES.ELECFEAT.WORK.WIRE2]");
	$ftp->put("$outfilename") or die "Upload of ${outfilename} failed";

	$ftp->quit;
	#print "$server $user $pass $init $path $uploadname\n";
	return 1;
}

### Returns the last modified value of a given value.
### time is converted from epoch time to a readable time format.
sub getFileStats {
	my $thisFile = $_[0];
	my $modtime = int((stat($thisFile))[9]);
	my $lastAccessTime = int((stat($thisFile))[8]);
	my @daysOfWeek = qw( Sunday Monday Tuesday Wednesday Thursday Friday Saturday );
	my @shortdaysOfWeek = qw( Sun Mon Tue Wed Thu Fri Sat );
	my @monthsOfYear = qw( January Febuary March April May June July August September October November December );
	my @shortmonthsOfYear = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
	my ($f_second, $f_minute, $f_hour, $f_day, $f_month, $f_year, $f_weekDay, $f_dayOfYear, $IsDST) = localtime(time);
	(my $second, my $minute, my $hour, my $day, my $mm, my $year, my $weekDay, my $dayOfYear, $IsDST) = localtime($modtime); 
	my $weekAsWord = "$shortdaysOfWeek[$weekDay]";
	my $monthAsWord = "$shortmonthsOfYear[$mm]";
				if ($minute < 10){
					$minute = "0$minute";
				}
			if ($f_day != $day) {
			$lastmod = "$weekAsWord, $monthAsWord $day at $hour:$minute";
			} else {
			$lastmod = "Today at $hour:$minute";
			}	
			
	(my $second, my $minute, my $hour, my $day, my $mm, my $year, my $weekDay, my $dayOfYear, $IsDST) = localtime($lastAccessTime); 
	my $weekAsWord = "$shortdaysOfWeek[$weekDay]";
	my $monthAsWord = "$shortmonthsOfYear[$mm]";
				if ($minute < 10){
					$minute = "0$minute";
				}
			if ($f_day != $day) {
			$lastaccess = "$weekAsWord, $monthAsWord $day at $hour:$minute";
			} else {
			$lastaccess = "Today at $hour:$minute";
			}	

	return($lastmod);
}
sub checkReportAge {
	my $thisFile = $_[0];
	my $file_status;
	my $modtime = int((stat($thisFile))[9]);
	my $lastAccessTime = int((stat($thisFile))[8]);
	my @daysOfWeek = qw( Sunday Monday Tuesday Wednesday Thursday Friday Saturday );
	my @shortdaysOfWeek = qw( Sun Mon Tue Wed Thu Fri Sat );
	my @monthsOfYear = qw( January Febuary March April May June July August September October November December );
	my @shortmonthsOfYear = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
	my ($f_second, $f_minute, $f_hour, $f_day, $f_month, $f_year, $f_weekDay, $f_dayOfYear, $IsDST) = localtime(time);
	(my $second, my $minute, my $hour, my $day, my $mm, my $year, my $weekDay, my $dayOfYear, $IsDST) = localtime($modtime); 
	my $weekAsWord = "$shortdaysOfWeek[$weekDay]";
	my $monthAsWord = "$shortmonthsOfYear[$mm]";
				#if ($minute < 10){
				#	$minute = "0$minute";
				#}
			if ($f_day != $day) {
				$lastmod = "$weekAsWord, $monthAsWord $day at $hour:$minute";
			} else {
				$lastmod = "Today at $hour:$minute";
			}	
	my $lastmodTot = ($hour * 60) + $minute;
	my $nowtimeTot = ($f_hour * 60) + $f_minute;
	my $timsDiff = $nowtimeTot - $lastmodTot;
	my $timeNumber = int($timsDiff);
	if ($timeNumber > 6) {
		@file_status = ("CategoryHeaderAlert","!!!!! This report is $timsDiff minutes old !!!!!");
	} else {
		@file_status = ("CategoryHeader","");
	}
#	(my $second, my $minute, my $hour, my $day, my $mm, my $year, my $weekDay, my $dayOfYear, $IsDST) = localtime($lastAccessTime); 
#	my $weekAsWord = "$shortdaysOfWeek[$weekDay]";
#	my $monthAsWord = "$shortmonthsOfYear[$mm]";
#				if ($minute < 10){
#					$minute = "0$minute";
#				}
#			if ($f_day != $day) {
#			$lastaccess = "$weekAsWord, $monthAsWord $day at $hour:$minute";
#			} else {
#			$lastaccess = "Today at $hour:$minute";
#			}	

	return(@file_status);
}

### Returns current time in a readable format. 
sub GetDateTime {
my $time = time;
my ($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($time); 
my @daysOfWeek = qw( Sunday Monday Tuesday Wednesday Thursday Friday Saturday );
my @shortdaysOfWeek = qw( Sun Mon Tue Wed Thu Fri Sat );

my @monthsOfYear = qw( January Febuary March April May June July August September October November December );
my @shortmonthsOfYear = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
my $weekAsWord = "$shortdaysOfWeek[$weekDay]";
my $monthAsWord = "$shortmonthsOfYear[$mm]";
			
				my $realMinute = "";
	#If needed add leading zero to minute
	if($minute < 10)
	{
		$realMinute = "0$minute";
	}
	else
	{
		$realMinute = "$minute";
	}
	
		if($hour >= 13)
	{
		$realHour = $hour - 12;
		my $AMPM = "PM";
	}
	else
	{
		$realHour = $hour;
		my $AMPM = "AM";

	}

my $nowtime = " $hour:$realMinute $AMPM - $weekAsWord, $monthAsWord $day";
return($nowtime);
}
sub GetTimeStamp {
my $time = time;
my ($second, $minute, $hour, $day, $mm, $year, $weekDay, $dayOfYear, $IsDST) = localtime($time); 
my @daysOfWeek = qw( Sunday Monday Tuesday Wednesday Thursday Friday Saturday );
my @shortdaysOfWeek = qw( Sun Mon Tue Wed Thu Fri Sat );

my @monthsOfYear = qw( January Febuary March April May June July August September October November December );
my @shortmonthsOfYear = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
my $weekAsWord = "$shortdaysOfWeek[$weekDay]";
my $monthAsWord = "$shortmonthsOfYear[$mm]";
			
				my $realMinute = "";
	#If needed add leading zero to minute
	if($minute < 10)
	{
		$realMinute = "0$minute";
	}
	else
	{
		$realMinute = "$minute";
	}
	
		if($hour >= 13)
	{
		$realHour = $hour - 12;
		my $AMPM = "PM";
	}
	else
	{
		$realHour = $hour;
		my $AMPM = "AM";

	}

my $nowtime = "$monthAsWord$day$hour$realMinute";
return($nowtime);
}

sub TurboQueFinder {
my $generic_queue = $_[0];
my $sho_holding = $_[1];
my $snapshot = "/Library/WebServer/Becky/snapshot9.txt";
my @snapLast = checkReportAge($snapshot);

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
open FH,">/Perl/turbosnapshot.txt";
print FH $fullFile;
close FH;
my @allLines = split("\n",$fullFile);
my $queu_tracker;
foreach (@allLines) {

	if ($_ =~ /^Generic batch queue TURBO/) {
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
						print "$this_BQ - $bq_status<br>";
						$queu_tracker = "TRUE";
						next;				 
					} elsif (($queu_tracker eq "TRUE") && ($find_queue =~ /^(Gen|Bat)/m)){
						$queu_tracker = "FALSE";
						#print "End of $this_BQ\n";
						next;
					} elsif (($queu_tracker eq "TRUE") && ($find_queue =~ /^\d/m)) {
						my @batch_job = split(' ',$find_queue);
						print "Batch job is $find_queue<br>";
					}
				} #	foreach my $find_queue (@allLines) {

		}#	foreach my $this_BQ (@Batch_q_list) {

	}

}

}


sub CelebLookup {
my $tmdIDfind = $_[0];
#my @OTTlist = ("AMZONOV","HULUOV","NETOV");
 #!/usr/bin/perl
#my @OTTlist = ("AMZONOV","HULUOV","NETOV");
#print "Searching for $tmdIDfind IDs\n";
($mday,$mon,$year) = (localtime)[3..5];
$ymd      = sprintf( "%04d%02d%02d",$year+1900,$mon+1,$mday );
my $completeData;
#$title    = '21 jum';
$filename     = "/Library/WebServer/OPS/ONXML/fancyCelebrity.xml";
$onFilename     = "/Library/WebServer/OPS/ONXML/on_celeb.xml";

$parser       = XML::LibXML->new();
$doc          = $parser->parse_file( $filename );
$onDoc        = $parser->parse_file( $onFilename );
$onXpc        = XML::LibXML::XPathContext->new( $onDoc );
$onQuery      = "//TMSIds/TMSId[contains(., '$tmdIDfind')]";
#@onNodes      = $onXpc->findnodes($onQuery);
my @results;
my @allNames;
#my $totalFinds = scalar(@onNodes);
#my $personCount = 0;
#print "There are $totalFinds Celebs associated with ID $tmdIDfind\n";

foreach  my $onNodes ( $onXpc->findnodes($onQuery) ) {
		$personCount++;
		my $tmsID = $onNodes->textContent;
	
		my $otmsIDNode      = $onNodes->parentNode; 
		my $oproductionNode = $otmsIDNode->parentNode;
		my $omediaNode      = $oproductionNode->parentNode;
		my $opersonNode     = $omediaNode->parentNode;
		my @oPersonName     = $opersonNode->getElementsByTagName( 'personNames' );
		
		foreach  $oPersonName ( @oPersonName ) {		
			my $olName;
			my $omName;
			my @ofirstName   = $oPersonName->getElementsByTagName( 'first' );
			my @omiddleName  = $oPersonName->getElementsByTagName( 'middle' );
			my @olastName    = $oPersonName->getElementsByTagName( 'last' );
			my $ofName       = $ofirstName[0]->textContent;
			my @ofullName    = $ofName;
			 
			if ( scalar (@omiddleName) > 0 ) { 
				$omName = $omiddleName[0]->textContent;
				push ( @ofullName, $omName );
			 } 
			 
			 if ( scalar (@olastName) > 0 ) { 
				$olName = $olastName[0]->textContent;
				push ( @ofullName, $olName );
			 } 
		#	 my $thisName = "$ofName|olName";
	 	#	my @allNames = (@allNames,$thisName);
			my $ocompleteName  = join ( ' ', @ofullName);
		###	my @production = $omediaNode->getElementsByTagName( 'production' );
			#print "Complete Name is $ocompleteName\n\n";
			#print "First: $ofName Middle: $omName Last: $olName\n";
			#push ( @results, ("$ocompleteName\n", "FILMOGRAPHY\n" ));
			#print "FILMOGRAPHY\n";
			my @production = $omediaNode->getElementsByTagName( 'production' );
			
			push ( @results, ("$ocompleteName\n", "FILMOGRAPHY\n" ));
			
			foreach  $production ( @production ) {
				my @onTitle  = $production->getElementsByTagName( 'title' );
				my $onYear   = $production->getElementsByTagName( 'year' );
				my $onCredit = $production->getElementsByTagName( 'credit' );

				foreach  $onTitle ( @onTitle ) {
					my $language    = $onTitle->getAttribute( 'lang' );
					my $goodOnTitle = $onTitle->textContent;
					
					if ( $language =~ 'en' || $language =~ 'es') {
						#print "Title: $goodOnTitle Year: $onYear Credits:$onCredit\n";
						push ( @results, "$goodOnTitle $onYear $onCredit\n" );
					}
				}
			
			}
		#print "\n\n\n";
			#if ($personCount == $totalFinds) {
			#	print "Got to the last one, now exiting\n";
			#	last;
			#}
#		foreach $thisName (@allNames) {
		#my $firstName,$lastName = split '\|',$thisName;
		#print "Looking for $ofName $olName\n";
		$xpc  = XML::LibXML::XPathContext->new( $doc );
		$query = "//NAMES/NAME/FIRST_NAME[text()='$ofName']/../LAST_NAME[text()='$olName']";
		foreach  my $nodes ( $xpc->findnodes($query) ) {
				my $lastName   = $nodes->textContent;
				my $parentName = $nodes->parentNode;
				my $firstName  = $parentName->getElementsByTagName( 'FIRST_NAME' );
				my $middleName = $parentName->getElementsByTagName( 'MIDDLE_NAME' );
				my @fullName   = ( $firstName, $lastName );
	
				#if ( length $middleName > 0 ) { 	
				#	splice @fullName, 1, 0, "$middleName";
				 #}
					my $namesNode        = $parentName->parentNode;
					my $personNode       = $namesNode->parentNode;
					my @awardNode        = $personNode->getElementsByTagName( 'AWARD' );
					my @milestoneNode    = $personNode->getElementsByTagName( 'MILESTONE' );
					my @highlightsNode   = $personNode->getElementsByTagName( 'HIGHLIGHT' );
					my @biographiesNode  = $personNode->getElementsByTagName( 'BIOGRAPHY' );
		
					foreach  $awardNode ( @awardNode ) {
						my $awardGroup    = $awardNode->getElementsByTagName( 'AWARD_GROUP' );
						my $awardYear     = $awardNode->getElementsByTagName( 'AWARD_YEAR' );
						my $awardResult   = $awardNode->getElementsByTagName( 'RESULT' );
						my $awardCatagory = $awardNode->getElementsByTagName( 'AWARD_CATEGORY' );
						my @projectNode   = $awardNode->getElementsByTagName( 'PROJECT_TITLE' );
						my $projectTitle  = $projectNode[0]->textContent;
		
						#print " AWARD: $awardGroup, $awardYear, $awardResult, $awardCatagory, $projectTitle\n";
						push ( @results, " AWARD: $awardGroup, $awardYear, $awardResult, $awardCatagory, $projectTitle\n" );
					}
		
					foreach  $milestoneNode ( @milestoneNode ) {
						my $beginDate    = $milestoneNode->getElementsByTagName( 'BEGIN_DATE' );
						my $thruDate     = $milestoneNode->getElementsByTagName( 'AWARD_YEAR' );
						my $description  = $milestoneNode->getElementsByTagName( 'DESCRIPTION' );
		
						#push ( @results, " MILESTONE:" );
			
						if ( length $beginDate > 0 ) { 
						#	push ( @results, "$beginDate" );
						}
			
						if ( length $thruDate > 0 ) { 
						#	push ( @results, "- $thruDate" );
						}
			
						#push ( @results, "$description\n" );
					}
					
					#print " HIGHLIGHTS:\n";
					foreach  $highlightsNode ( @highlightsNode ) {
						my $highlightText = $highlightsNode->getElementsByTagName( 'TEXT' );
						push ( @results, " HIGHLIGHT: $highlightText\n" );
		
					#	print " $highlightText\n";
					}
				
					#print " BIOGRAPHY:";	
					foreach  $biographiesNode ( @biographiesNode ) {
						my $firstBio   = $biographiesNode->getElementsByTagName( 'FIRST' );
						my $secondBio  = $biographiesNode->getElementsByTagName( 'REST' );
						#print "$firstBio\n";
		
						push ( @results, " BIOGRAPHY: $firstBio\n" );
			
						if ( length $secondBio > 0 ) { 
						#	push ( @results, "$secondBio\n" );
						}
					}
				}

#}
		}

}
my $completeData = join '<br>',@results;
#print join ( "\n", @results ), "\n";
return($completeData);
}

sub SaveAdvancedPlannerLookup {
my $tag = $_[0];
my $tagValue = $_[1];
my @tagValues = split "\-",$tagValue;
#my @OTTlist = ("AMZONOV","HULUOV","NETOV");
#print "Searching for $title in the language $lang\n";
($mday,$mon,$year) = (localtime)[3..5];
$ymd      = sprintf( "%04d%02d%02d",$year+1900,$mon+1,$mday );
my $completeData;
$filename = "/Library/WebServer/OPS/ONXML/on_tv_advance_planner.xml";
#$title    = '21 jum';

$parser   = XML::LibXML->new();
$doc      = $parser->parse_file( $filename );
$xpc      = XML::LibXML::XPathContext->new( $doc );
$query    = "//events/$tag";
#print "Query is $query\n";
@nodes    = $xpc->findnodes($query);
my @results;
foreach (@tagValues) {
$completeData = "$completeData<center><strong>$_</strong></center><br>";
foreach $nodes ( @nodes ) {
	$prog       = $nodes->textContent;
	 my $lcprog = lc($prog);
	 my $lctagValue = lc($tagValue);
	#print "Looking for $prog in @tagValues<br>";
	if ($prog =~ /$_/ ) {  
	#print $prog; 	
    	my $progArea    = $nodes->parentNode;
    	#my @idTag       = $progArea->getElementsByTagName( 'TMSId' );
    	#my @idValue     = $idTag[0]->textContent;
      	my @titleTag       = $progArea->getElementsByTagName( 'progTitle' );
    	my $titleValue     = $titleTag[0]->textContent;
  		my @AirDateTag  = $progArea->getElementsByTagName( 'airDate' );
  		my $AiringY  =  $AirDateTag[0]->textContent;
      	my @AiringDate = split " ", $AiringY;
		my $AirDate = "$AiringDate[1]\/$AiringDate[2]\/$AiringDate[0]";
      	my @networkTag       = $progArea->getElementsByTagName( 'network' );
    	my $networkTag     = $networkTag[0]->textContent;
		my @episodeTag       = $progArea->getElementsByTagName( 'epiTitle' );
    	my $episodeValue     = $episodeTag[0]->textContent;
		my @descTag     = $progArea->getElementsByTagName( 'description' );
    	my $description = $descTag[0]->textContent;
    	
    	if ( $description eq "" ) {
    		$description  = 'No Description Available.'	 
    	}

       # my $completeId    = join ( '=', 'TMS ID', $idValue[0] );
        if ($networkTag eq "AMZONOV") { $networkTag = "AMAZON VIDEO"; } 
        if ($networkTag eq "HULUOV") { $networkTag = "HULU"; } 
        if ($networkTag eq "NETOV") { $networkTag = "NETFLIX"; } 
	    $completeData  = "$completeData<strong>$networkTag<br>\"$titleValue\"</strong><p><b>Episode:</b> $episodeValue</p> <p><b>Available:</b> $AirDate</p> <p>$description</p><br>"
			
	   # push ( @results, $completeData );
    }
}
}
#print join ( "\n", @results ), "\n";
return($completeData);
}

sub AppleScript
{
	my($script) = shift @_;
#	print "\n$script\n";
	system("osascript -e '$script'");
}


sub mountScans {
	system("osascript -e /PerlLib/MountScans.scpt");

}
sub mountVolume
#requires volume name (parameter 1)
#optional second parameter for log file
{
	my @parameters = @_;
	my $volumeName = "$parameters[0]";
	print "Attempting to mount $volumeName\n";
	#my $volumeNameUNIX = makePathUNIX("$volumeName");
	my $mountLocal = "/Volumes/$volumeName";
	my $mountscript = "mount volume \"smb://macserver.tmsgf.trb/$volumeName\" as user name \"scripting\" with password \"alaska\"";
	#my $mountscript = "tell application \"Finder\" to mount volume \"afp://macserver.tmsgf.trb/Scans/\" as user name \"scripting\" with password \"alaska\"";
		unless(-e $mountLocal or mkdir $mountLocal) {
		die "Unable to create $directory\n";
	}
		#makesystem ("mkdir $mountLocal") or die;
#		system("$mountscript");
		AppleScript($mountscript);
}

1;
