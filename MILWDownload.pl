#!/usr/bin/perl

use Net::FTP;
use warnings;

my @args = @ARGV;
my $subFolder = $args[0];
my $toFolder = "$args[1]";
my $destinationFolder = "/PerlTemp";
#print "downloading $toFolder from $subFolder now\n";
mkdir "$destinationFolder\/$toFolder";
downloadFile("ftp1.tmsgf.trb", "wicusmed", "371gi425", "$subFolder", "$destinationFolder/$toFolder", "$toFolder");

opendir(TMPDIR, "$destinationFolder/$toFolder");
my @allfiles = readdir TMPDIR;
closedir(TMPDIR);
	foreach $unstFile (@allfiles) {
	#print "unstuffing $destinationFolder/$toFolder/$unstFile \n";
	my $fileTounstuff = "$destinationFolder/$toFolder/$unstFile";
		my @fileparts = split('\.',$unstFile);
		foreach (@fileparts) {
			if ($_ eq "bin") {
				system("/usr/bin/unstuff \"$fileTounstuff\" >> /dev/null");
				system("/bin/rm  \"$fileTounstuff\" >> /dev/null");
			}
		}
	}

sub downloadFile
{
	my @parameters = @_;
	my $server = "$parameters[0]";
	my $user = "$parameters[1]";
	my $pass = "$parameters[2]";
	my $multipath = "$parameters[3]";	#supports only one level
	my $path = "$parameters[4]";
	my $toFolder = "$parameters[5]";

	my $ftp = Net::FTP->new("$server", Debug => 0, Passive => 0);
	$ftp->login("$user","$pass");
	$ftp->binary();
	
	my @foldersPath = split('\/',$multipath);
	my $directory = "/";
	foreach my $cdFolder (@foldersPath) {
		$directory = "${directory}${cdFolder}/";
		#print "adding folder $cdFolder\n";
	}
	$directory = "$directory";
	$ftp->cwd("$directory") or warn (print "**Failure** - $directory does not exist on FTP.\n\n");;
	#print "Getting files from $directory\n\n";
	@files = $ftp->ls("$directory/");
	my $totalFileNum = scalar(@files);
	print "There are $totalFileNum files in this directory.\n\n";
	if ($totalFileNum == 0) {
		print "**Failure** there are no files in the $directory folder.\n\n";
	}
	foreach my $downloadname (@files) {
		#print "File to download is: $downloadname";
		my @fileName = split('\/',$downloadname);
		my $folderNumbers = scalar(@fileName);
		#print "There are $folderNumbers in this directory\n";
		my $thisFile = $fileName[$folderNumbers-1];
		print "Downloading $thisFile\n";
		$ftp->get("$downloadname","$destinationFolder/$toFolder/$thisFile") or warn (print "**Failure** - Failed to download file $downloadname. This may be a folder, not a file.\n");
	}
	$ftp->quit;
	return 1;
}